// Form handlers for School Scheduler

let currentGroupName = '';
let currentTeacherName = '';
// guard to prevent concurrent / repeated favorites list fetches
let _favoritesLoading = false;
// timestamp of last showFavoritesModal invocation (ms) to debounce rapid calls
let _lastFavoritesCall = 0;

function _cleanupBackdropsIfNoVisibleModals() {
    // small timeout to let any Bootstrap handlers finish
    setTimeout(() => {
        try {
            const visible = Array.from(document.querySelectorAll('.modal')).some(m => {
                try {
                    const style = window.getComputedStyle(m);
                    const rect = m.getBoundingClientRect();
                    return m.classList.contains('show') && style.display !== 'none' && rect.width > 0 && rect.height > 0;
                } catch (e) { return false; }
            });
            if (!visible) {
                document.querySelectorAll('.modal-backdrop').forEach(e => e.remove());
                document.body.classList.remove('modal-open');
                document.body.style.paddingRight = '';
            }
        } catch (e) { console.warn('cleanupBackdrops failed', e); }
    }, 50);
}

// Teachers
async function loadTeachers() {
    try {
        // Load time slots first for formatting
        if (!window.timeSlots || Object.keys(window.timeSlots).length === 0) {
            await loadTimeSlots();
        }
        
        const teachers = await API.get('/api/teachers');
        const tbody = $('#teachersTable tbody');
        tbody.empty();
        
        teachers.forEach(teacher => {
            const subjectsText = (teacher.subjects || []).map(s => {
                const name = s.name || '';
                const hours = parseInt(s.hours) || 0;
                let grp = s.group;
                if (grp === null || grp === undefined) grp = '';
                if (String(grp).toLowerCase() === 'null') grp = '';
                return `${name}:${hours}:${grp}`;
            }).join('; ');
            
            const assigned = teacher.subjects.reduce((sum, s) => sum + s.hours, 0);
            const available = Object.values(teacher.available_slots || {})
                .reduce((sum, arr) => sum + arr.length, 0);
            
            // Format weekly hours for display
            const weeklyHoursText = formatWeeklyHours(teacher.check_in_hours, teacher.check_out_hours);
            
            const row = $('<tr>')
                .data('teacher', teacher)
                .append($('<td>').text(teacher.name))
                .append($('<td>').text(subjectsText))
                .append($('<td>').text(weeklyHoursText))
                .append($('<td>').addClass('text-end').text(`${assigned}/${available}`));
            
            tbody.append(row);
        });
        
        // Highlight selected row on click
        $('#teachersTable tbody tr').click(function() {
            $(this).addClass('table-active').siblings().removeClass('table-active');
        });
    } catch (error) {
        console.error('Failed to load teachers:', error);
    }
}

// Handle deep-links like ?tab=teacher-scheduler&editTeacher=Name
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const params = new URLSearchParams(window.location.search);
        const tab = params.get('tab');
        const editTeacher = params.get('editTeacher');
        if (tab === 'teacher-scheduler') {
            try { document.querySelector('#teacher-scheduler-tab').click(); } catch(e){}
        }
        if (editTeacher) {
            const teacherName = decodeURIComponent(editTeacher);
            // ensure the teacher scheduler tab is active
            try { document.querySelector('#teacher-scheduler-tab').click(); } catch(e){}
            // Ensure the teacher select is populated by explicitly loading the scheduler and prefer desired teacher
            try { await loadTeacherScheduler(teacherName); } catch(e) { console.warn('loadTeacherScheduler failed', e); }

            // Wait for #teacherSelect options to be populated, then select and open edit modal
            const maxAttempts = 40; // ~4 seconds
            const interval = 100;
            let attempts = 0;
            const waiter = setInterval(()=>{
                attempts++;
                try {
                    const select = document.querySelector('#teacherSelect');
                    if (select) {
                        const opts = Array.from(select.options || []);
                        const found = opts.find(o => (o.value === teacherName) || (o.text === teacherName));
                        if (found) {
                            // set value and trigger change
                            try { $('#teacherSelect').val(found.value).change(); } catch(e){}
                            // wait 5 seconds so user can inspect the Teacher Scheduler, then open edit modal
                            setTimeout(()=>{ openEditTeacherByName(found.value || teacherName); }, 5000);
                            clearInterval(waiter);
                            return;
                        }
                    }
                } catch(e) { /* ignore and retry */ }
                if (attempts >= maxAttempts) {
                    clearInterval(waiter);
                    // as fallback, wait 5 seconds then try opening edit modal
                    try { setTimeout(()=>{ openEditTeacherByName(teacherName); }, 5000); } catch(e){ console.warn('fallback openEditTeacher failed', e); }
                }
            }, interval);
        }
    } catch(e) { console.warn('deep-link handler error', e); }
});

function addTeacher() {
    $('#teacherModalTitle').text(_('Add Teacher'));
    $('#teacherForm')[0].reset();
    $('#teacherForm input[name="original_name"]').val('');
    loadAvailableSubjects();
    loadGroupsForSubjects();
    $('#selectedSubjects').empty();
    // init interactive interval UI
    initIntervalUI();
    bootstrap.Modal.getOrCreateInstance(document.getElementById('teacherModal')).show();
}

async function editTeacher() {
    const selected = $('#teachersTable tbody tr.table-active');
        if (selected.length === 0) {
            alert(_('Select a teacher to edit'));
            return;
    }
    const teacherRow = selected.data('teacher') || {};
    const teacherName = teacherRow.name || selected.find('td').first().text();
    // Fetch fresh teacher data from server to ensure Subjects/Hours are up-to-date
    let teacher = teacherRow;
    try {
        const teachers = await API.get('/api/teachers');
        const found = teachers.find(t => t.name === teacherName);
        if (found) teacher = found;
    } catch (e) {
        console.warn('Could not refresh teacher data, using table copy', e);
    }
    populateTeacherModal(teacher);
}

// Populate the Edit Teacher modal from a teacher object and show it
function populateTeacherModal(teacher) {
    if (!teacher) return;
    console.log('Populating teacher modal for:', teacher.name);
    $('#teacherModalTitle').text(_('Edit Teacher'));
    $('#teacherForm input[name="original_name"]').val(teacher.name || '');
    $('#teacherForm input[name="name"]').val(teacher.name || '');

    const weeklyHours = formatWeeklyHours(teacher.check_in_hours, teacher.check_out_hours);
    $('#teacherForm textarea[name="weekly_hours"]').val(weeklyHours);

    const timeSlots = formatTimeSlots(teacher.available_slots);
    $('#teacherForm textarea[name="time_slots"]').val(timeSlots);

    const availability = formatAvailability(teacher.available_slots);
    $('#teacherForm textarea[name="availability"]').val(availability);

    loadAvailableSubjects();
    loadGroupsForSubjects();

    const selectedList = $('#selectedSubjects');
    selectedList.empty();
    (teacher.subjects || []).forEach(s => {
        const name = s.name || '';
        const hours = parseInt(s.hours) || 0;
        let grp = s.group || '';
        if (String(grp).toLowerCase() === 'null') grp = '';
        const val = `${name}:${hours}:${grp}`;
        const option = $('<option>').val(val).text(val);
        selectedList.append(option);
    });

    initIntervalUI();
    populateIntervalsFromTeacher(teacher);
    bootstrap.Modal.getOrCreateInstance(document.getElementById('teacherModal')).show();
}

// Open Edit Teacher modal by teacher name without switching away from Teacher Scheduler
async function openEditTeacherByName(teacherName) {
    if (!teacherName) return;
    try {
        const teachers = await API.get('/api/teachers');
        const found = teachers.find(t => t.name === teacherName);
        if (found) {
            populateTeacherModal(found);
        } else {
            console.warn('Teacher not found:', teacherName);
        }
    } catch (e) {
        console.warn('Failed to fetch teachers for openEditTeacherByName', e);
    }
}

function formatWeeklyHours(checkIn, checkOut) {
    if (!checkIn) return '';
    const lines = [];
    for (const day in checkIn) {
        for (let i = 0; i < checkIn[day].length; i++) {
            lines.push(`${day}:${checkIn[day][i]}-${checkOut[day][i]}`);
        }
    }
    return lines.join('\n');
}

function formatAvailability(availableSlots) {
    if (!availableSlots) return '';
    const lines = [];
    for (const day in availableSlots) {
        const lessons = availableSlots[day];
        if (lessons.length > 0) {
            const min = Math.min(...lessons);
            const max = Math.max(...lessons);
            lines.push(`${day}:${min}-${max}`);
        }
    }
    return lines.join('\n');
}

function formatTimeSlots(availableSlots) {
    if (!availableSlots) return '';
    const lines = [];
    
    // Get time slots from global config
    const slots = window.timeSlots || {};
    
    // Debug logging
    console.log('formatTimeSlots - slots:', slots);
    console.log('formatTimeSlots - availableSlots:', availableSlots);
    
    for (const day in availableSlots) {
        const lessons = availableSlots[day];
        if (lessons.length > 0) {
            const min = Math.min(...lessons);
            const max = Math.max(...lessons);
            
            console.log(`Day: ${day}, lessons: ${min}-${max}, slot[${min}]:`, slots[min]);
            
            // Convert lesson numbers to time ranges if available
            const startTime = slots[min] ? slots[min].split('-')[0].trim() : `${_('Lesson')}${min}`;
            const endTime = slots[max] ? slots[max].split('-')[1].trim() : `${_('Lesson')}${max}`;
            
            lines.push(`${day}:${startTime}-${endTime}`);
        }
    }
    return lines.join('\n');
}

// Helper function to find lesson number by time
function findLessonByTime(slots, time, isEnd = false) {
    // Remove extra spaces
    time = time.replace(/\s/g, '');
    
    for (const [lessonNum, timeRange] of Object.entries(slots)) {
        const [start, end] = timeRange.split('-').map(t => t.replace(/\s/g, ''));
        
        if (isEnd) {
            // For end time, match the end of a lesson
            if (time === end) return parseInt(lessonNum);
        } else {
            // For start time, match the start of a lesson
            if (time === start) return parseInt(lessonNum);
        }
    }
    
    // If exact match not found, try to find closest lesson
    const timeMinutes = timeToMinutes(time);
    let closestLesson = null;
    let minDiff = Infinity;
    
    for (const [lessonNum, timeRange] of Object.entries(slots)) {
        const [start, end] = timeRange.split('-').map(t => t.replace(/\s/g, ''));
        const targetTime = isEnd ? end : start;
        const targetMinutes = timeToMinutes(targetTime);
        const diff = Math.abs(timeMinutes - targetMinutes);
        
        if (diff < minDiff) {
            minDiff = diff;
            closestLesson = parseInt(lessonNum);
        }
    }
    
    return closestLesson;
}

// Convert real check-in/out time to first/last lessons fully contained in the range
function convertRealTimeToLessons(slots, checkinStr, checkoutStr) {
    try {
        const [ci_h, ci_m] = checkinStr.split(':').map(Number);
        const [co_h, co_m] = checkoutStr.split(':').map(Number);
        const checkinMinutes = ci_h * 60 + ci_m;
        const checkoutMinutes = co_h * 60 + co_m;
        let first = null;
        let last = null;

        const entries = Object.entries(slots).sort((a,b)=>parseInt(a[0]) - parseInt(b[0]));
        for (const [lessonNum, timeRange] of entries) {
            if (!timeRange || timeRange.indexOf('-') === -1) continue;
            const [ls, le] = timeRange.split('-').map(s => s.trim());
            const [ls_h, ls_m] = ls.split(':').map(Number);
            const [le_h, le_m] = le.split(':').map(Number);
            const lessonStart = ls_h * 60 + ls_m;
            const lessonEnd = le_h * 60 + le_m;

            if (checkinMinutes <= lessonStart && checkoutMinutes >= lessonEnd) {
                if (first === null) first = parseInt(lessonNum);
                last = parseInt(lessonNum);
            }
        }

        return [first, last];
    } catch (e) {
        return [null, null];
    }
}

// Convert an arbitrary time-range (HH:MM-HH:MM) to lesson numbers fully contained
function convertTimeRangeToLessons(slots, startStr, endStr) {
    return convertRealTimeToLessons(slots, startStr, endStr);
}

// Convert time string HH:MM to minutes
function timeToMinutes(time) {
    const [hours, minutes] = time.split(':').map(Number);
    return hours * 60 + minutes;
}

// Compute deterministic color for a subject name (used in modal and on save)
// Minimal MD5 implementation (adapted) to match server ColorService hashing
function md5cycle(x, k) {
    var a = x[0], b = x[1], c = x[2], d = x[3];

    a = ff(a, b, c, d, k[0], 7, -680876936);
    d = ff(d, a, b, c, k[1], 12, -389564586);
    c = ff(c, d, a, b, k[2], 17, 606105819);
    b = ff(b, c, d, a, k[3], 22, -1044525330);
    a = ff(a, b, c, d, k[4], 7, -176418897);
    d = ff(d, a, b, c, k[5], 12, 1200080426);
    c = ff(c, d, a, b, k[6], 17, -1473231341);
    b = ff(b, c, d, a, k[7], 22, -45705983);
    a = ff(a, b, c, d, k[8], 7, 1770035416);
    d = ff(d, a, b, c, k[9], 12, -1958414417);
    c = ff(c, d, a, b, k[10], 17, -42063);
    b = ff(b, c, d, a, k[11], 22, -1990404162);
    a = ff(a, b, c, d, k[12], 7, 1804603682);
    d = ff(d, a, b, c, k[13], 12, -40341101);
    c = ff(c, d, a, b, k[14], 17, -1502002290);
    b = ff(b, c, d, a, k[15], 22, 1236535329);

    a = gg(a, b, c, d, k[1], 5, -165796510);
    d = gg(d, a, b, c, k[6], 9, -1069501632);
    c = gg(c, d, a, b, k[11], 14, 643717713);
    b = gg(b, c, d, a, k[0], 20, -373897302);
    a = gg(a, b, c, d, k[5], 5, -701558691);
    d = gg(d, a, b, c, k[10], 9, 38016083);
    c = gg(c, d, a, b, k[15], 14, -660478335);
    b = gg(b, c, d, a, k[4], 20, -405537848);
    a = gg(a, b, c, d, k[9], 5, 568446438);
    d = gg(d, a, b, c, k[14], 9, -1019803690);
    c = gg(c, d, a, b, k[3], 14, -187363961);
    b = gg(b, c, d, a, k[8], 20, 1163531501);
    a = gg(a, b, c, d, k[13], 5, -1444681467);
    d = gg(d, a, b, c, k[2], 9, -51403784);
    c = gg(c, d, a, b, k[7], 14, 1735328473);
    b = gg(b, c, d, a, k[12], 20, -1926607734);

    a = hh(a, b, c, d, k[5], 4, -378558);
    d = hh(d, a, b, c, k[8], 11, -2022574463);
    c = hh(c, d, a, b, k[11], 16, 1839030562);
    b = hh(b, c, d, a, k[14], 23, -35309556);
    a = hh(a, b, c, d, k[1], 4, -1530992060);
    d = hh(d, a, b, c, k[4], 11, 1272893353);
    c = hh(c, d, a, b, k[7], 16, -155497632);
    b = hh(b, c, d, a, k[10], 23, -1094730640);
    a = hh(a, b, c, d, k[13], 4, 681279174);
    d = hh(d, a, b, c, k[0], 11, -358537222);
    c = hh(c, d, a, b, k[3], 16, -722521979);
    b = hh(b, c, d, a, k[6], 23, 76029189);
    a = hh(a, b, c, d, k[9], 4, -640364487);
    d = hh(d, a, b, c, k[12], 11, -421815835);
    c = hh(c, d, a, b, k[15], 16, 530742520);
    b = hh(b, c, d, a, k[2], 23, -995338651);

    a = ii(a, b, c, d, k[0], 6, -198630844);
    d = ii(d, a, b, c, k[7], 10, 1126891415);
    c = ii(c, d, a, b, k[14], 15, -1416354905);
    b = ii(b, c, d, a, k[5], 21, -57434055);
    a = ii(a, b, c, d, k[12], 6, 1700485571);
    d = ii(d, a, b, c, k[3], 10, -1894986606);
    c = ii(c, d, a, b, k[10], 15, -1051523);
    b = ii(b, c, d, a, k[1], 21, -2054922799);
    a = ii(a, b, c, d, k[8], 6, 1873313359);
    d = ii(d, a, b, c, k[15], 10, -30611744);
    c = ii(c, d, a, b, k[6], 15, -1560198380);
    b = ii(b, c, d, a, k[13], 21, 1309151649);
    a = ii(a, b, c, d, k[4], 6, -145523070);
    d = ii(d, a, b, c, k[11], 10, -1120210379);
    c = ii(c, d, a, b, k[2], 15, 718787259);
    b = ii(b, c, d, a, k[9], 21, -343485551);

    x[0] = add32(a, x[0]);
    x[1] = add32(b, x[1]);
    x[2] = add32(c, x[2]);
    x[3] = add32(d, x[3]);
}

function cmn(q, a, b, x, s, t) {
    a = add32(add32(a, q), add32(x, t));
    return add32((a << s) | (a >>> (32 - s)), b);
}

function ff(a, b, c, d, x, s, t) { return cmn((b & c) | ((~b) & d), a, b, x, s, t); }
function gg(a, b, c, d, x, s, t) { return cmn((b & d) | (c & (~d)), a, b, x, s, t); }
function hh(a, b, c, d, x, s, t) { return cmn(b ^ c ^ d, a, b, x, s, t); }
function ii(a, b, c, d, x, s, t) { return cmn(c ^ (b | (~d)), a, b, x, s, t); }

function md51(s) {
    var txt = '';
    var n = s.length,
            state = [1732584193, -271733879, -1732584194, 271733878],
            i;
    for (i = 64; i <= s.length; i += 64) {
        md5cycle(state, md5blk(s.substring(i - 64, i)));
    }
    s = s.substring(i - 64);
    var tail = new Array(16).fill(0);
    for (i = 0; i < s.length; i++) tail[i >> 2] |= s.charCodeAt(i) << ((i % 4) << 3);
    tail[i >> 2] |= 0x80 << ((i % 4) << 3);
    if (i > 55) {
        md5cycle(state, tail);
        tail = new Array(16).fill(0);
    }
    tail[14] = n * 8;
    md5cycle(state, tail);
    return state;
}

/* there needs to be support for Unicode here, unless we pretend that we can call this on only ASCII */
function md5blk(s) {
    var md5blks = [], i; /* Andy King said do it this way. */
    for (i = 0; i < 64; i += 4) {
        md5blks[i >> 2] = s.charCodeAt(i) + (s.charCodeAt(i + 1) << 8) + (s.charCodeAt(i + 2) << 16) + (s.charCodeAt(i + 3) << 24);
    }
    return md5blks;
}

function rhex(n) {
    var s = '', j;
    for (j = 0; j < 4; j++) s += hexChr[(n >> (j * 8 + 4)) & 0x0F] + hexChr[(n >> (j * 8)) & 0x0F];
    return s;
}

var hexChr = '0123456789abcdef'.split('');

function hex(x) {
    for (var i = 0; i < x.length; i++) x[i] = rhex(x[i]);
    return x.join('');
}

function md5(s) {
    return hex(md51(s));
}

function add32(a, b) {
    return (a + b) & 0xFFFFFFFF;
}

// compute color using same algorithm as server ColorService.get_color (md5 -> first 6 hex -> lighten 60%)
function computeColor(name) {
    try {
        const h = md5(String(name || ''));
        const r = parseInt(h.substr(0,2), 16);
        const g = parseInt(h.substr(2,2), 16);
        const b = parseInt(h.substr(4,2), 16);
        const lr = Math.round(r + (255 - r) * 0.6);
        const lg = Math.round(g + (255 - g) * 0.6);
        const lb = Math.round(b + (255 - b) * 0.6);
        const bg = `#${lr.toString(16).padStart(2,'0')}${lg.toString(16).padStart(2,'0')}${lb.toString(16).padStart(2,'0')}`;
        const luminance = 0.299 * lr + 0.587 * lg + 0.114 * lb;
        const fg = luminance > 128 ? '#000000' : '#FFFFFF';
        return { bg, fg };
    } catch (e) {
        return { bg: '#E0E0E0', fg: '#000000' };
    }
}

// Get color from server ColorService if available, fallback to local computeColor
async function getColor(name) {
    try {
        const esc = encodeURIComponent(String(name || ''));
        const res = await API.get(`/api/color/${esc}`);
        if (res && res.bg && res.fg) return { bg: res.bg, fg: res.fg };
    } catch (e) {
        // ignore and fallback
    }
    try {
        return computeColor(name || '');
    } catch (e) {
        return { bg: '#E0E0E0', fg: '#000000' };
    }
}

async function loadAvailableSubjects() {
    try {
        const subjects = await API.get('/api/subjects');
        const select = $('#availableSubjects');
        select.empty();

        // Optionally filter by selected group
        const groupFilter = ($('#subjectGroup').val() || '').trim();
        // Build entries per subject-group so we keep hours info
        const entries = (subjects || []).filter(s => {
            if (!s) return false;
            if (!groupFilter) return true;
            if (groupFilter === '') return true;
            return (s.group || '') === groupFilter;
        });

        // Populate select with entries containing hours and group
        entries.forEach(s => {
            const rawGroup = (s.group === null || s.group === undefined) ? '' : s.group;
            const groupSafe = (String(rawGroup).toLowerCase() === 'null') ? '' : rawGroup;
            const val = `${s.name}:${s.hours_per_week || 1}:${groupSafe}`;
            const text = `${s.name} (${groupSafe || ''}) — ${s.hours_per_week || 1}`;
            select.append($('<option>').val(val).text(text));
        });

        // When a subject is selected, populate the hours input with its default hours
        select.off('change.subjectHours').on('change.subjectHours', function(){
            const v = $(this).val();
            if (!v) return;
            const parts = v.split(':');
            const h = parseInt(parts[1]) || '';
            $('#subjectHours').val(h);
        });
    } catch (error) {
        console.error('Failed to load subjects:', error);
    }
}

async function loadGroupsForSubjects() {
    try {
        const groups = await API.get('/api/groups');
        const select = $('#subjectGroup');
        select.empty();
        select.append($('<option>').val('').text(_('All')));
        groups.forEach(g => {
            select.append($('<option>').val(g.name).text(g.name));
        });
    } catch (error) {
        console.error('Failed to load groups:', error);
    }
}

async function addSubjectToTeacher() {
    const availableSelect = $('#availableSubjects');
    const selectedSubject = availableSelect.val();

    if (!selectedSubject) {
        alert(_('Please select a subject from available subjects'));
        return;
    }

    // selectedSubject may be in the form 'name' or 'name:hours:group'
    const parts = (selectedSubject || '').split(':');
    const baseName = parts[0] || selectedSubject;
    const defaultHours = parseInt(parts[1]) || 1;
    let defaultGroup = parts[2] || '';
    if (String(defaultGroup).toLowerCase() === 'null') defaultGroup = '';

    const hours = parseInt($('#subjectHours').val()) || defaultHours;
    const group = defaultGroup;  // Group removed from UI

    // Check if already added to this teacher's selected list
    const existing = $('#selectedSubjects option').map(function() {
        return $(this).val().split(':')[0];
    }).get();

    if (existing.includes(selectedSubject)) {
        alert(_('This subject is already added'));
        return;
    }

    // Determine current teacher being edited (if any)
    const form = $('#teacherForm');
    const currentTeacher = (form.find('input[name="original_name"]').val() || '').trim();

    try {
        // Check other teachers assignments
        const teachers = await API.get('/api/teachers');
        const otherTeachers = (teachers || []).filter(t => {
            if (!t.subjects) return false;
            // skip current teacher
            if (currentTeacher && t.name === currentTeacher) return false;
            return t.subjects.some(s => (s.name === baseName));
        }).map(t => t.name);

        if (otherTeachers.length > 0) {
            const msg = `${_('Subject')} ${selectedSubject} ${_('is already assigned to other teachers')}: ${otherTeachers.join(', ')}. ${_('Assigning it again will split the class into subgroups. Proceed?')}`;
            if (!confirm(msg)) {
                return;
            }
        }
    } catch (e) {
        console.warn('Failed to fetch teachers for subject-assignment check', e);
        // proceed on error
    }

    // Ensure we add option in canonical name:hours:group format
    const value = `${baseName}:${hours}:${group}`;
    const option = $('<option>').val(value).text(value);
    $('#selectedSubjects').append(option);

    // Reset inputs
    $('#subjectHours').val('');
}

function removeSubjectFromTeacher() {
    const selectedList = $('#selectedSubjects');
    selectedList.find(':selected').remove();
}

async function saveTeacher() {
    // Синхронизируем текстовые поля с teacherIntervals перед сохранением
    syncTextareasFromIntervals();
    console.log('[DEBUG] saveTeacher: teacherIntervals перед сохранением', teacherIntervals);
    const form = $('#teacherForm');
        const originalName = form.find('input[name="original_name"]').val();
        const name = form.find('input[name="name"]').val().trim();
        const weeklyHours = (form.find('textarea[name="weekly_hours"]').val() || '').trim();
        const timeSlots = (form.find('textarea[name="time_slots"]').val() || '').trim();
        const availability = (form.find('textarea[name="availability"]').val() || '').trim();
    
        // Validate name
        if (!name) {
            alert(_('Teacher name is required'));
            return;
    }
    
    // Parse subjects from selected list
    const subjects = [];
    $('#selectedSubjects option').each(function() {
        const parts = $(this).val().split(':');
        if (parts.length >= 3) {
            let grp = parts[2];
            if (String(grp).toLowerCase() === 'null') grp = '';
            subjects.push({
                name: parts[0],
                hours: parseInt(parts[1]) || 0,
                group: grp
            });
        }
    });
    
    // Parse weekly hours (multiline: each line is Day:HH:MM-HH:MM)
    const checkInHours = {};
    const checkOutHours = {};
    if (weeklyHours) {
        weeklyHours.split('\n').forEach(line => {
            line = line.trim();
            if (line && line.includes(':') && line.includes('-')) {
                // Split by first colon only (day might contain spaces)
                const firstColonIdx = line.indexOf(':');
                if (firstColonIdx === -1) return;
                
                const day = line.substring(0, firstColonIdx).trim();
                const timeRange = line.substring(firstColonIdx + 1).trim();
                const [start, end] = timeRange.split('-', 2);
                
                if (day && start && end) {
                    if (!checkInHours[day]) {
                        checkInHours[day] = [];
                        checkOutHours[day] = [];
                    }
                    checkInHours[day].push(start.trim());
                    checkOutHours[day].push(end.trim());
                }
            }
        });
    }
    
    // Build availableSlots with precedence: weeklyHours (PRIMARY) -> timeSlots (SECONDARY) -> availability (TERTIARY)
    const availableSlots = {};
    const slots = window.timeSlots || {}; // Global time slots

    if (weeklyHours) {
        // Derive availableSlots from weeklyHours (checkIn/Out) - PRIMARY
        Object.keys(checkInHours).forEach(day => {
            const ins = Array.isArray(checkInHours[day]) ? checkInHours[day] : [checkInHours[day]];
            const outs = Array.isArray(checkOutHours[day]) ? checkOutHours[day] : (checkOutHours[day] ? [checkOutHours[day]] : []);
            for (let i = 0; i < Math.min(ins.length, outs.length); i++) {
                const ci = ins[i].trim();
                const co = outs[i].trim();
                if (!ci || !co) continue;
                const [startLesson, endLesson] = convertRealTimeToLessons(slots, ci, co);
                if (startLesson && endLesson) {
                    if (!availableSlots[day]) availableSlots[day] = [];
                    for (let j = startLesson; j <= endLesson; j++) {
                        if (!availableSlots[day].includes(j)) availableSlots[day].push(j);
                    }
                }
            }
        });
    } else {
        // SECONDARY / TERTIARY: parse provided timeSlots or availability text
        const slotsInput = timeSlots || availability;  // Use time_slots if provided, otherwise availability
        if (slotsInput) {
            slotsInput.split('\n').forEach(line => {
                line = line.trim();
                if (line && line.includes(':') && line.includes('-')) {
                    // Split by first colon only
                    const firstColonIdx = line.indexOf(':');
                    if (firstColonIdx === -1) return;

                    const day = line.substring(0, firstColonIdx).trim();
                    const range = line.substring(firstColonIdx + 1).trim();
                    const [start, end] = range.split('-', 2);

                    if (day && start && end) {
                        const startTrimmed = start.trim();
                        const endTrimmed = end.trim();

                        // Check if it's a time format (HH:MM) or lesson number
                        if (startTrimmed.includes(':') && endTrimmed.includes(':')) {
                            // Time format - convert to lesson numbers, require full containment
                            const [startLesson, endLesson] = convertTimeRangeToLessons(slots, startTrimmed, endTrimmed);

                            if (startLesson && endLesson) {
                                if (!availableSlots[day]) {
                                    availableSlots[day] = [];
                                }
                                for (let i = startLesson; i <= endLesson; i++) {
                                    if (!availableSlots[day].includes(i)) {
                                        availableSlots[day].push(i);
                                    }
                                }
                            }
                        } else {
                            // Lesson number format
                            const startNum = parseInt(startTrimmed);
                            const endNum = parseInt(endTrimmed);
                            if (!isNaN(startNum) && !isNaN(endNum)) {
                                if (!availableSlots[day]) {
                                    availableSlots[day] = [];
                                }
                                for (let i = startNum; i <= endNum; i++) {
                                    if (!availableSlots[day].includes(i)) {
                                        availableSlots[day].push(i);
                                    }
                                }
                            }
                        }
                    }
                }
            });
        }
    }
    
    const teacherData = {
        name: name,
        subjects: subjects,
        check_in_hours: checkInHours || {},
        check_out_hours: checkOutHours || {},
        available_slots: availableSlots || {}
    };
    
    console.log('Saving teacher data:', teacherData);
    console.log('Original weekly hours input:', weeklyHours);
    console.log('Original time slots input:', timeSlots);
    console.log('Original availability input:', availability);
    console.log('Parsed check_in_hours:', checkInHours);
    console.log('Parsed check_out_hours:', checkOutHours);
    console.log('Parsed available_slots:', availableSlots);
    
    try {
        if (originalName) {
            await API.put(`/api/teachers/${originalName}`, teacherData);
        } else {
            await API.post('/api/teachers', teacherData);
        }
        bootstrap.Modal.getInstance(document.getElementById('teacherModal')).hide();
        loadTeachers();
    } catch (error) {
        alert(_('Failed to save teacher: ') + error.message);
        console.error('Save error:', error);
    }
}

// ---------------- Interactive Intervals (Desktop-like) ----------------
let teacherIntervals = [];
const defaultWeekdays = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];

function initIntervalUI() {
    // populate day select
    const daySelect = $('#intervalDay');
    daySelect.empty();
    const configWeekdays = ($('#configForm input[name="WEEKDAYS"]').val() || defaultWeekdays.join(',')).split(',');
    configWeekdays.forEach(d => daySelect.append($('<option>').val(d.trim()).text(d.trim())));

    // populate start/end time selects using global timeSlots
    const slots = window.timeSlots || {};
    const start = $('#intervalStart');
    const end = $('#intervalEnd');
    start.empty(); end.empty();
    Object.keys(slots).sort((a,b)=>parseInt(a)-parseInt(b)).forEach(k => {
        const label = `${k}: ${slots[k]}`;
        start.append($('<option>').val(k).text(label));
        end.append($('<option>').val(k).text(label));
    });

    // wire buttons
    $('#addTimeSlotBtn').off('click').on('click', () => addIntervalFromSlots());
    $('#addRealHoursBtn').off('click').on('click', () => addIntervalFromRealHours());
    $('#intervalsTable').off('click', '.delete-interval').on('click', '.delete-interval', function(){
        const idx = $(this).data('idx'); removeInterval(idx);
    });
    
}

function addIntervalFromSlots() {
    const day = $('#intervalDay').val();
    const s = parseInt($('#intervalStart').val());
    const e = parseInt($('#intervalEnd').val());
    if (!day || !s || !e) { alert(_('Choose day, start and end')); return; }
    if (s > e) { alert(_('Start must be before end')); return; }
    const slots = window.timeSlots || {};
    const timeStart = slots[s] ? slots[s].split('-')[0].trim() : '';
    const timeEnd = slots[e] ? slots[e].split('-')[1].trim() : '';
    const timeslots = timeStart && timeEnd ? `${timeStart}-${timeEnd}` : '';
    const lessons = `${s}-${e}`;
    teacherIntervals.push({day: day, lessons: lessons, timeslots: timeslots, real: ''});
    console.log('[DEBUG] addIntervalFromSlots: teacherIntervals после добавления', teacherIntervals);
    renderIntervals();
    syncTextareasFromIntervals();
}

function addIntervalFromRealHours() {
    const day = $('#intervalDay').val();
    const checkIn = $('#checkIn').val().trim();
    const checkOut = $('#checkOut').val().trim();
    if (!day || !checkIn || !checkOut) { alert(_('Choose day and enter check in/out')); return; }
    const slots = window.timeSlots || {};
    const [startLesson, endLesson] = convertRealTimeToLessons(slots, checkIn, checkOut);
    if (!startLesson || !endLesson) { alert(_('Times do not match any lessons')); return; }
    const timeStart = slots[startLesson] ? slots[startLesson].split('-')[0].trim() : '';
    const timeEnd = slots[endLesson] ? slots[endLesson].split('-')[1].trim() : '';
    const timeslots = timeStart && timeEnd ? `${timeStart}-${timeEnd}` : '';
    const lessons = `${startLesson}-${endLesson}`;
    const real = `${checkIn}-${checkOut}`;
    teacherIntervals.push({day: day, lessons: lessons, timeslots: timeslots, real: real});
    console.log('[DEBUG] addIntervalFromRealHours: teacherIntervals после добавления', teacherIntervals);
    renderIntervals();
    syncTextareasFromIntervals();
}

function renderIntervals() {
    const tbody = $('#intervalsTable tbody');
    tbody.empty();
    teacherIntervals.forEach((it, idx) => {
        const row = $('<tr>').append(
            $('<td>').html('<input type="checkbox"/>'),
            $('<td>').text(it.day),
            $('<td>').text(it.lessons),
            $('<td>').text(it.timeslots),
            $('<td>').text(it.real),
            $('<td>').html(`<button class="btn btn-sm btn-outline-danger delete-interval" data-idx="${idx}">${_('Delete')}</button>`)
        );
        tbody.append(row);
    });
}

function removeInterval(idx) {
    if (idx>=0 && idx<teacherIntervals.length) {
        teacherIntervals.splice(idx,1);
        renderIntervals();
        syncTextareasFromIntervals();
    }
}

function syncTextareasFromIntervals() {
    // Build weekly_hours (real hours), time_slots, availability
    const weekly = [];
    const times = [];
    const avail = [];
    const slots = window.timeSlots || {};
    teacherIntervals.forEach(it => {
        console.log('[DEBUG] syncTextareasFromIntervals: interval', it);
        // weekly_hours: real > timeslots > lessons (fallback)
        let weeklyStr = '';
        if (it.real && it.real.includes(':')) {
            weeklyStr = `${it.day}:${it.real}`;
        }
        if (!weeklyStr && it.timeslots && it.timeslots.includes('-')) {
            weeklyStr = `${it.day}:${it.timeslots}`;
        }
        if (!weeklyStr && it.lessons && it.lessons.includes('-')) {
            const [lStart, lEnd] = it.lessons.split('-');
            if (slots && Object.keys(slots).length > 0 && lStart && lEnd) {
                const tStart = slots[lStart] ? slots[lStart].split('-')[0].trim() : '';
                const tEnd = slots[lEnd] ? slots[lEnd].split('-')[1].trim() : '';
                if (tStart && tEnd) weeklyStr = `${it.day}:${tStart}-${tEnd}`;
                else weeklyStr = `${it.day}:${it.lessons}`;
            } else {
                weeklyStr = `${it.day}:${it.lessons}`;
            }
        }
        if (weeklyStr) {
            console.log('[DEBUG] syncTextareasFromIntervals: weeklyStr', weeklyStr);
            weekly.push(weeklyStr);
        }

        // time_slots: real > timeslots > lessons (fallback)
        let timesStr = '';
        if (it.real && it.real.includes(':')) {
            const [checkIn, checkOut] = it.real.split('-');
            let tStart = '', tEnd = '';
            if (checkIn && checkOut) {
                const [startLesson, endLesson] = convertRealTimeToLessons(slots, checkIn, checkOut);
                tStart = slots[startLesson] ? slots[startLesson].split('-')[0].trim() : '';
                tEnd = slots[endLesson] ? slots[endLesson].split('-')[1].trim() : '';
            }
            if (tStart && tEnd) timesStr = `${it.day}:${tStart}-${tEnd}`;
        }
        if (!timesStr && it.timeslots && it.timeslots.includes('-')) {
            timesStr = `${it.day}:${it.timeslots}`;
        }
        if (!timesStr && it.lessons && it.lessons.includes('-')) {
            const [lStart, lEnd] = it.lessons.split('-');
            if (slots && Object.keys(slots).length > 0 && lStart && lEnd) {
                const tStart = slots[lStart] ? slots[lStart].split('-')[0].trim() : '';
                const tEnd = slots[lEnd] ? slots[lEnd].split('-')[1].trim() : '';
                if (tStart && tEnd) timesStr = `${it.day}:${tStart}-${tEnd}`;
                else timesStr = `${it.day}:${it.lessons}`;
            } else {
                timesStr = `${it.day}:${it.lessons}`;
            }
        }
        if (timesStr) {
            console.log('[DEBUG] syncTextareasFromIntervals: timesStr', timesStr);
            times.push(timesStr);
        }

        // availability: real > timeslots > lessons (fallback)
        let availStr = '';
        if (it.real && it.real.includes(':')) {
            const [checkIn, checkOut] = it.real.split('-');
            let lStart = '', lEnd = '';
            if (checkIn && checkOut) {
                const [startLesson, endLesson] = convertRealTimeToLessons(slots, checkIn, checkOut);
                lStart = startLesson; lEnd = endLesson;
            }
            if (lStart && lEnd) availStr = `${it.day}:${lStart}-${lEnd}`;
        }
        if (!availStr && it.timeslots && it.timeslots.includes('-')) {
            const [start, end] = it.timeslots.split('-');
            if (start && end) {
                const [startLesson, endLesson] = convertTimeRangeToLessons(slots, start.trim(), end.trim());
                if (startLesson && endLesson) availStr = `${it.day}:${startLesson}-${endLesson}`;
            }
        }
        if (!availStr && it.lessons && it.lessons.includes('-')) {
            availStr = `${it.day}:${it.lessons}`;
        }
        if (availStr) {
            console.log('[DEBUG] syncTextareasFromIntervals: availStr', availStr);
            avail.push(availStr);
        }
    });
    $('textarea[name="weekly_hours"]').val(weekly.join('\n'));
    $('textarea[name="time_slots"]').val(times.join('\n'));
    $('textarea[name="availability"]').val(avail.join('\n'));
    console.log('[DEBUG] textarea weekly_hours:', $('textarea[name="weekly_hours"]').val());
    console.log('[DEBUG] textarea time_slots:', $('textarea[name="time_slots"]').val());
    console.log('[DEBUG] textarea availability:', $('textarea[name="availability"]').val());
}

function populateIntervalsFromTeacher(teacher) {
    console.log('[DEBUG] populateIntervalsFromTeacher: исходные данные teacher', teacher);
    teacherIntervals = [];
    const slots = window.timeSlots || {};
    // If check_in/check_out exist, use them (PRIMARY)
    const ci = teacher.check_in_hours || {};
    const co = teacher.check_out_hours || {};
    Object.keys(ci).forEach(day => {
        const ins = Array.isArray(ci[day]) ? ci[day] : [ci[day]];
        const outs = Array.isArray(co[day]) ? co[day] : [co[day]];
        for (let i=0;i<Math.min(ins.length, outs.length); i++) {
            const inT = ins[i]; const outT = outs[i];
            const [s, e] = convertRealTimeToLessons(slots, inT, outT);
            if (s && e) {
                const timeStart = slots[s] ? slots[s].split('-')[0].trim() : '';
                const timeEnd = slots[e] ? slots[e].split('-')[1].trim() : '';
                teacherIntervals.push({day: day, lessons: `${s}-${e}`, timeslots: timeStart && timeEnd ? `${timeStart}-${timeEnd}` : '', real: `${inT}-${outT}`});
            }
        }
    });
    // Fallback: available_slots
    if (teacherIntervals.length===0 && teacher.available_slots) {
        Object.keys(teacher.available_slots).forEach(day => {
            const lessons = teacher.available_slots[day];
            if (lessons && lessons.length>0) {
                const min = Math.min(...lessons); const max = Math.max(...lessons);
                const timeStart = slots[min] ? slots[min].split('-')[0].trim() : '';
                const timeEnd = slots[max] ? slots[max].split('-')[1].trim() : '';
                teacherIntervals.push({day: day, lessons: `${min}-${max}`, timeslots: timeStart && timeEnd ? `${timeStart}-${timeEnd}` : '', real: ''});
            }
        });
    }
    renderIntervals();
    syncTextareasFromIntervals();
    console.log('[DEBUG] populateIntervalsFromTeacher: teacherIntervals после заполнения', teacherIntervals);
}


function parseWeeklyHours(str) {
    const checkIn = {};
    const checkOut = {};
    str.split(';').forEach(entry => {
        const trimmed = entry.trim();
        if (!trimmed) return;
        const [day, timeRange] = trimmed.split(':');
        const [start, end] = timeRange.split('-');
        if (!checkIn[day]) {
            checkIn[day] = [];
            checkOut[day] = [];
        }
        checkIn[day].push(start);
        checkOut[day].push(end);
    });
    return {checkIn, checkOut};
}

function parseAvailability(str) {
    const slots = {};
    str.split(';').forEach(entry => {
        const trimmed = entry.trim();
        if (!trimmed) return;
        const [day, range] = trimmed.split(':');
        const [start, end] = range.split('-');
        slots[day] = [];
        for (let i = parseInt(start); i <= parseInt(end); i++) {
            slots[day].push(i);
        }
    });
    return slots;
}

async function deleteTeacher() {
    const selected = $('#teachersTable tbody tr.table-active');
        if (selected.length === 0) {
            alert(_('Select a teacher to delete'));
            return;
    }
    
    const teacher = selected.data('teacher');
    Confirmations.deleteItem(teacher.name, async (confirmed) => {
        if (confirmed) {
            try {
                await API.delete(`/api/teachers/${teacher.name}`);
                loadTeachers();
            } catch (error) {
                alert(_('Failed to delete teacher: ') + error.message);
            }
        }
    });
}

async function moveTeacher(direction) {
    const selected = $('#teachersTable tbody tr.table-active');
        if (selected.length === 0) {
            alert(_('Select a teacher to move'));
            return;
    }
    
    const teacher = selected.data('teacher');
    try {
        await API.post(`/api/teachers/${teacher.name}/move`, {direction: direction});
        loadTeachers();
    } catch (error) {
        alert(_('Failed to move teacher: ') + error.message);
    }
}

// Move Group
async function moveGroup(direction) {
    const selected = $('#groupsTable tbody tr.table-active');
    if (selected.length === 0) {
        alert(_('Select a group to move'));
        return;
    }
    const group = selected.data('group');
    try {
        await API.post(`/api/groups/${encodeURIComponent(group.name)}/move`, {direction: direction});
        loadGroups();
    } catch (error) {
        alert(_('Failed to move group: ') + error.message);
    }
}

// Move Subject
async function moveSubject(direction) {
    const selected = $('#subjectsTable tbody tr.table-active');
    if (selected.length === 0) {
        alert(_('Select a subject to move'));
        return;
    }
    const subject = selected.data('subject');
    try {
        await API.post(`/api/subjects/${encodeURIComponent(subject.name)}/move`, {direction: direction});
        loadSubjects();
    } catch (error) {
        alert(_('Failed to move subject: ') + error.message);
    }
}

// Groups
async function loadGroups() {
    try {
        const groups = await API.get('/api/groups');
        const tbody = $('#groupsTable tbody');
        tbody.empty();
        
        groups.forEach(group => {
            const subjectsArr = Array.isArray(group.subjects) ? group.subjects : (group.subjects ? [group.subjects] : []);
            const commentsText = subjectsArr.join('; ');
            const totalRequired = group.total_required || 0;
            const totalAssigned = group.total_assigned || 0;
            const totalsText = `${totalRequired} / ${totalAssigned}`;
            const row = $('<tr>')
                .data('group', group)
                .append($('<td>').text(group.name))
                .append($('<td>').text(commentsText))
                .append($('<td>').text(totalsText));
            tbody.append(row);
        });
        
        $('#groupsTable tbody tr').click(function() {
            $(this).addClass('table-active').siblings().removeClass('table-active');
        });
    } catch (error) {
        console.error('Failed to load groups:', error);
    }
}

function addGroup() {
    $('#groupModalTitle').text(_('Add Group'));
    $('#groupForm')[0].reset();
    $('#groupForm input[name="original_name"]').val('');
    bootstrap.Modal.getOrCreateInstance(document.getElementById('groupModal')).show();
}

function editGroup() {
    const selected = $('#groupsTable tbody tr.table-active');
    if (selected.length === 0) {
        alert(_('Select a group to edit'));
        return;
    }
    
    const group = selected.data('group');
    $('#groupModalTitle').text(_('Edit Group'));
    $('#groupForm input[name="original_name"]').val(group.name);
    $('#groupForm input[name="name"]').val(group.name);
    // populate comments (subjects used to carry comments as single-element list)
    const comments = Array.isArray(group.subjects) ? group.subjects.join('; ') : (group.subjects || '');
    $('#groupForm textarea[name="comments"]').val(comments);
    bootstrap.Modal.getOrCreateInstance(document.getElementById('groupModal')).show();
}

async function saveGroup() {
    const form = $('#groupForm');
    const originalName = form.find('input[name="original_name"]').val();
    const name = form.find('input[name="name"]').val();
    
    const commentsVal = form.find('textarea[name="comments"]').val();
    const groupData = {
        name: name,
        subjects: commentsVal ? [commentsVal] : []
    };
    
    try {
        if (originalName) {
            console.log('[DEBUG] Updating group:', originalName, '->', name);
            await API.put(`/api/groups/${originalName}`, groupData);
            // If name changed, refresh Teachers and Subjects tabs to reflect updated references
            if (originalName !== name) {
                console.log('[DEBUG] Group name changed, refreshing Teachers and Subjects');
                // Small delay to ensure backend has saved changes
                await new Promise(resolve => setTimeout(resolve, 200));
                loadTeachers();
                loadSubjects();
            }
        } else {
            console.log('[DEBUG] Creating new group:', name);
            await API.post('/api/groups', groupData);
        }
        bootstrap.Modal.getInstance(document.getElementById('groupModal')).hide();
        loadGroups();
    } catch (error) {
        alert(_('Failed to save group: ') + error.message);
    }
}

async function deleteGroup() {
    const selected = $('#groupsTable tbody tr.table-active');
        if (selected.length === 0) {
            alert(_('Select a group to delete'));
            return;
    }
    
    const group = selected.data('group');
    Confirmations.deleteItem(group.name, async (confirmed) => {
        if (confirmed) {
            try {
                await API.delete(`/api/groups/${group.name}`);
                loadGroups();
            } catch (error) {
                alert(_('Failed to delete group: ') + error.message);
            }
        }
    });
}

// Subjects
async function loadSubjects() {
    try {
        const subjects = await API.get('/api/subjects');
        const teachers = await API.get('/api/teachers');
        const tbody = $('#subjectsTable tbody');
        tbody.empty();
        
        subjects.forEach(subject => {
            // Find all teachers who teach this subject in this group
            const teachersForSubject = teachers.filter(teacher => {
                return teacher.subjects && teacher.subjects.some(s => 
                    s.name === subject.name && 
                    (s.group === subject.group || (!s.group && !subject.group))
                );
            }).map(t => t.name);
            
            const teachersText = teachersForSubject.join(', ');
            
            const row = $('<tr>')
                .data('subject', subject)
                .append($('<td>').text(subject.name))
                .append($('<td>').text(subject.group))
                .append($('<td>').text(subject.hours_per_week))
                .append($('<td>').text(teachersText || ''));
            tbody.append(row);
        });
        
        $('#subjectsTable tbody tr').click(function() {
            $(this).addClass('table-active').siblings().removeClass('table-active');
        });
    } catch (error) {
        console.error('Failed to load subjects:', error);
    }
}

async function addSubject() {
    $('#subjectModalTitle').text(_('Add Subject'));
    $('#subjectForm')[0].reset();
    $('#subjectForm input[name="original_name"]').val('');
    
    // Load groups into select
    const groups = await API.get('/api/groups');
    const select = $('#subjectForm select[name="group"]');
    select.empty();
    groups.forEach(g => {
        select.append($('<option>').val(g.name).text(g.name));
    });
    
    bootstrap.Modal.getOrCreateInstance(document.getElementById('subjectModal')).show();
}

async function editSubject() {
    const selected = $('#subjectsTable tbody tr.table-active');
    if (selected.length === 0) {
        alert(_('Select a subject to edit'));
        return;
    }
    
    const subject = selected.data('subject');
    $('#subjectModalTitle').text(_('Edit Subject'));
    $('#subjectForm input[name="original_name"]').val(subject.name);
    $('#subjectForm input[name="name"]').val(subject.name);
    $('#subjectForm input[name="hours_per_week"]').val(subject.hours_per_week);
    
    // Load groups into select
    const groups = await API.get('/api/groups');
    const select = $('#subjectForm select[name="group"]');
    select.empty();
    groups.forEach(g => {
        select.append($('<option>').val(g.name).text(g.name));
    });
    select.val(subject.group);
    
    bootstrap.Modal.getOrCreateInstance(document.getElementById('subjectModal')).show();
}

async function saveSubject() {
    const form = $('#subjectForm');
    const originalName = form.find('input[name="original_name"]').val();
    const name = form.find('input[name="name"]').val();
    const group = form.find('select[name="group"]').val();
    const hoursPerWeek = parseInt(form.find('input[name="hours_per_week"]').val());
    
    const subjectData = {
        name: name,
        group: group,
        hours_per_week: hoursPerWeek,
        teacher: ''
    };
    
    try {
        if (originalName) {
            await API.put(`/api/subjects/${originalName}`, subjectData);
        } else {
            await API.post('/api/subjects', subjectData);
        }
        const modalEl = document.getElementById('subjectModal');
        const modalInstance = bootstrap.Modal.getInstance(modalEl);
        // Ensure focused element is blurred so assistive tech isn't hidden
        try { if (document.activeElement) document.activeElement.blur(); } catch (e) {}
        // Hide modal and wait for it to finish hiding to avoid aria-hidden focus issues
        if (modalInstance) {
            modalInstance.hide();
            await new Promise(resolve => {
                function handler() { modalEl.removeEventListener('hidden.bs.modal', handler); resolve(); }
                modalEl.addEventListener('hidden.bs.modal', handler);
                // Safety timeout in case event doesn't fire
                setTimeout(resolve, 300);
            });
        }
        await loadSubjects();
        // Refresh teachers list so teacher selected-subjects reflect subject changes
        await loadTeachers();
    } catch (error) {
        alert(_('Failed to save subject: ') + error.message);
    }
}

async function deleteSubject() {
    const selected = $('#subjectsTable tbody tr.table-active');
        if (selected.length === 0) {
            alert(_('Select a subject to delete'));
            return;
    }
    
    const subject = selected.data('subject');
    Confirmations.deleteItem(subject.name, async (confirmed) => {
        if (confirmed) {
            try {
                await API.delete(`/api/subjects/${subject.name}`);
                // If any element inside the modal has focus, blur it first
                try { if (document.activeElement) document.activeElement.blur(); } catch (e) {}
                // If modal is open, hide and wait for it to finish
                const modalEl = document.getElementById('subjectModal');
                const modalInstance = bootstrap.Modal.getInstance(modalEl);
                if (modalInstance) {
                    modalInstance.hide();
                    await new Promise(resolve => {
                        function handler() { modalEl.removeEventListener('hidden.bs.modal', handler); resolve(); }
                        modalEl.addEventListener('hidden.bs.modal', handler);
                        setTimeout(resolve, 300);
                    });
                }
                await loadSubjects();
                await loadTeachers();
                } catch (error) {
                alert(_('Failed to delete subject: ') + error.message);
            }
        }
    });
}

// Configuration
let timeSlots = {}; // Global time slots storage

async function loadConfiguration() {
    try {
        const config = await API.get('/api/config');
        const form = $('#configForm');
        for (const key in config) {
            form.find(`[name="${key}"]`).val(config[key]);
        }
        
        // Load time slots
        await loadTimeSlots();
    } catch (error) {
        console.error('Failed to load configuration:', error);
    }
}

async function loadTimeSlots() {
    try {
        timeSlots = await API.get('/api/time-slots');
        window.timeSlots = timeSlots; // Make globally accessible
        renderTimeSlots();
    } catch (error) {
        console.error('Failed to load time slots:', error);
        timeSlots = {};
        window.timeSlots = {};
    }
}

function renderTimeSlots() {
    const tbody = $('#timeSlotsBody');
    tbody.empty();
    
    // Get current lesson count for sync
    const lessonCount = parseInt($('#lessonsInput').val() || 10);

    // Ensure timeSlots keys align with lessonCount: add empty slots or remove extras
    const currentCount = Object.keys(timeSlots).length;
    if (currentCount < lessonCount) {
        for (let i = currentCount + 1; i <= lessonCount; i++) {
            if (!timeSlots[i]) timeSlots[i] = '';
        }
    } else if (currentCount > lessonCount) {
        for (let i = lessonCount + 1; i <= currentCount; i++) {
            if (timeSlots.hasOwnProperty(i)) delete timeSlots[i];
        }
    }

    // Sort by lesson number
    const sortedSlots = Object.entries(timeSlots).sort((a, b) => parseInt(a[0]) - parseInt(b[0]));
    
    sortedSlots.forEach(([lessonNum, timeRange]) => {
        const row = $(`
            <tr data-lesson="${lessonNum}">
                <td>${lessonNum}</td>
                <td class="editable-time-cell" data-lesson="${lessonNum}" style="cursor: pointer;" title="${_('Click to edit')}">${timeRange || `<em class="text-muted">${_('Click to set time')}</em>`}</td>
                <td>
                    <button class="btn btn-sm btn-danger delete-slot" data-lesson="${lessonNum}" title="${_('Delete slot')}">
                        ×
                    </button>
                </td>
            </tr>
        `);
        tbody.append(row);
    });
    
    // Info: slots now synced to lesson count
    console.debug(`Time slots synced: ${sortedSlots.length} slots (lessons setting: ${lessonCount})`);
}

// Validate time format - flexible H:MM or HH:MM
function validateTimeFormat(timeStr) {
    // Flexible regex: allows single or double digit hours (0-23), minutes (00-59)
    const timeRegex = /^([0-9]|[0-1][0-9]|2[0-3]):([0-5][0-9])-([0-9]|[0-1][0-9]|2[0-3]):([0-5][0-9])$/;
    if (!timeRegex.test(timeStr)) {
        return { valid: false, message: 'Invalid format. Use H:MM-H:MM or HH:MM-HH:MM (e.g., 9:15-10:00)' };
    }
    
    // Validate start < end
    const [start, end] = timeStr.split('-');
    const [startH, startM] = start.split(':').map(Number);
    const [endH, endM] = end.split(':').map(Number);
    const startMinutes = startH * 60 + startM;
    const endMinutes = endH * 60 + endM;
    
    if (startMinutes >= endMinutes) {
        return { valid: false, message: 'End time must be after start time' };
    }
    
    return { valid: true };
}

// Add new time slot
$(document).on('click', '#addSlotBtn', async function() {
    const lessonNum = parseInt($('#editLessonNum').val());
    const timeRange = $('#editTimeRange').val().trim();
    
    if (!lessonNum || lessonNum < 1 || lessonNum > 30) {
        alert(_('Lesson number must be between 1 and 30'));
        return;
    }
    
    if (!timeRange) {
        alert(_('Please enter a time range'));
        return;
    }
    
    // Validate time format
    const validation = validateTimeFormat(timeRange);
    if (!validation.valid) {
        alert(validation.message);
        return;
    }
    
    try {
        await API.post('/api/time-slots', { lesson: lessonNum, time: timeRange });
        timeSlots[lessonNum] = timeRange;
        renderTimeSlots();
        
        // Clear inputs and increment lesson number
        $('#editLessonNum').val(parseInt($('#editLessonNum').val()) + 1);
        $('#editTimeRange').val('');
        
        console.log('Time slot added:', lessonNum, timeRange);
    } catch (error) {
        alert(_('Failed to add time slot: ') + error.message);
        console.error('Add error:', error);
    }
});

// Inline editing for time cells
$(document).on('click', '.editable-time-cell', function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const cell = $(this);
    const lessonNum = cell.data('lesson');
    const currentTime = timeSlots[lessonNum] || '';
    
    // Don't create input if already editing
    if (cell.find('input').length > 0) return;
    
    // Replace cell content with input
    const input = $('<input>')
        .attr('type', 'text')
        .addClass('form-control form-control-sm')
        .val(currentTime)
        .attr('placeholder', '9:15-10:00')
        .css('width', '100%');
    
    cell.html(input);
    input.focus().select();
    
    // Save on Enter or blur
    const saveEdit = async function() {
        const newTime = input.val().trim();
        
        if (!newTime) {
            cell.html(`<em class="text-muted">${_('Click to set time')}</em>`);
            return;
        }
        
        // Validate format
        const validation = validateTimeFormat(newTime);
        if (!validation.valid) {
            alert(validation.message);
            input.focus();
            return;
        }
        
            try {
            await API.post('/api/time-slots', { lesson: lessonNum, time: newTime });
            timeSlots[lessonNum] = newTime;
            cell.text(newTime);
            console.log('Time slot updated:', lessonNum, newTime);
        } catch (error) {
            alert(_('Failed to save: ') + error.message);
            cell.text(currentTime || '');
        }
    };
    
    // Handle Enter key
    input.on('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            saveEdit();
        } else if (e.key === 'Escape') {
            e.preventDefault();
            cell.html(currentTime ? currentTime : `<em class="text-muted">${_('Click to set time')}</em>`);
        }
    });
    
    // Handle blur (click outside)
    input.on('blur', function() {
        setTimeout(saveEdit, 100);
    });
});

// Delete slot button handler
$(document).on('click', '.delete-slot', async function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const lessonNum = parseInt($(this).data('lesson'));
    
    if (!confirm(`Delete time slot for lesson ${lessonNum}?`)) {
        return;
    }
    
    try {
        await API.delete(`/api/time-slots/${lessonNum}`);
        delete timeSlots[lessonNum];
        renderTimeSlots();
        console.log('Time slot deleted:', lessonNum);
    } catch (error) {
        alert(_('Failed to delete: ') + error.message);
    }
});

// Sync time slots when lessons count changes
$(document).on('change', '#lessonsInput', function() {
    const newCount = parseInt($(this).val());
    const currentCount = Object.keys(timeSlots).length;
    if (isNaN(newCount) || newCount < 1) {
        alert(_('Invalid lessons number'));
        $(this).val(currentCount);
        return;
    }

    if (newCount > currentCount) {
        // Auto-generate missing slots with empty times
        for (let i = currentCount + 1; i <= newCount; i++) {
            if (!timeSlots[i]) {
                timeSlots[i] = '';
            }
        }
        renderTimeSlots();
    } else if (newCount < currentCount) {
        // Confirm destructive action before deleting extra slots
        const confirmMsg = `Уменьшить число уроков с ${currentCount} до ${newCount}?\n` +
            `Будут удалены временные слоты для уроков ${newCount + 1}..${currentCount}. Продолжить?`;
        if (!confirm(confirmMsg)) {
            // revert input back
            $(this).val(currentCount);
            return;
        }

        // Remove extra slots
        for (let i = currentCount; i > newCount; i--) {
            if (timeSlots.hasOwnProperty(i)) delete timeSlots[i];
        }
        renderTimeSlots();
    }
});

$('#configForm').submit(async function(e) {
    e.preventDefault();
    
    const config = {};
    $(this).serializeArray().forEach(item => {
        config[item.name] = item.value;
    });
    
    Confirmations.saveConfig(async (confirmed) => {
        if (confirmed) {
            try {
                await API.post('/api/config', config);
                alert(_('Configuration saved successfully'));
                location.reload(); // Reload to apply language changes
            } catch (error) {
                alert(_('Failed to save configuration: ') + error.message);
            }
        }
    });
});

// Group Scheduler
async function loadGroupScheduler() {
    const groups = await API.get('/api/groups');
    const select = $('#groupSelect');
    select.empty();
    groups.forEach(g => {
        select.append($('<option>').val(g.name).text(g.name));
    });
    
    if (groups.length > 0) {
        currentGroupName = groups[0].name;
        loadGroupSchedule();
    }
    
    select.change(loadGroupSchedule);
}

async function loadGroupSchedule() {
    currentGroupName = $('#groupSelect').val();
    if (!currentGroupName) return;
    
    try {
        const schedule = await API.get(`/api/schedules/group/${currentGroupName}`);
        await ScheduleGrid.render('#groupScheduleGrid', schedule, {
            editable: true,
            onCellClick: (day, lesson, lessonData) => showLessonModal(day, lesson, lessonData)
        });
    } catch (error) {
        console.error('Failed to load schedule:', error);
    }
}

function autofillGroup() {
    const groupName = $('#groupSelect').val();
    if (!groupName) return;
    
    Confirmations.autofillSchedule(groupName, async (confirmed) => {
        if (confirmed) {
            try {
                const result = await API.post('/api/schedules/autofill', {group: groupName});
                
                // Always reload the schedule to show what was placed
                loadGroupSchedule();
                
                if (result.success) {
                    alert(_('Schedule created successfully'));
                } else {
                    // Build informative message with incomplete details if available
                    let msg = _('Autofill completed with some issues:\n');
                    if (result.incomplete && result.incomplete.length > 0) {
                        result.incomplete.forEach(it => {
                            const teachers = (it.teachers || []).join(', ');
                            msg += `${it.subject}: ${it.placed}/${it.required} (teachers: ${teachers})\n`;
                        });
                    } else if (result.errors && result.errors.length > 0) {
                        msg += result.errors.join('\n');
                    }
                    alert(msg);
                }
            } catch (error) {
                alert(_('Failed to autofill: ') + error.message);
            }
        }
    });
}

async function clearGroupSchedule() {
    const groupName = $('#groupSelect').val();
    if (!groupName) return;
    
    Confirmations.deleteItem(`schedule for ${groupName}`, async (confirmed) => {
        if (confirmed) {
            try {
                await API.post(`/api/schedules/group/${groupName}`, {});
                loadGroupSchedule();
            } catch (error) {
                alert(_('Failed to clear schedule: ') + error.message);
            }
        }
    });
}

// Teacher Scheduler
async function loadTeacherScheduler(desiredTeacher) {
    const teachers = await API.get('/api/teachers');
    const select = $('#teacherSelect');
    select.empty();
    teachers.forEach(t => {
        select.append($('<option>').val(t.name).text(t.name));
    });
    
    if (teachers.length > 0) {
        if (desiredTeacher) {
            // If a desired teacher was requested, try to select it and load its schedule
            const opts = Array.from(select.find('option') || []).map(o => ({ val: o.value, text: o.text }));
            const found = opts.find(o => o.val === desiredTeacher || o.text === desiredTeacher);
            if (found) {
                currentTeacherName = found.val;
                try { $('#teacherSelect').val(found.val).change(); } catch(e){}
                await loadTeacherSchedule();
            } else {
                // fallback to first teacher if desired not found
                currentTeacherName = teachers[0].name;
                loadTeacherSchedule();
            }
        } else {
            currentTeacherName = teachers[0].name;
            loadTeacherSchedule();
        }
    }
    
    select.change(loadTeacherSchedule);
    
    // day-scheduler loading is bound globally on document ready (avoid double-binding)
}

// Day Scheduler
async function loadDayScheduler() {
    try {
        // Load weekdays from config
        const config = await API.get('/api/config');
        const weekdays = (config.WEEKDAYS || 'Monday,Tuesday,Wednesday,Thursday,Friday').split(',').map(d => d.trim());
        const select = $('#weekdaySelect');
        select.empty();
        weekdays.forEach(d => select.append($('<option>').val(d).text(d)));

        // Load when weekday is changed (ensure single handler)
        select.off('change').on('change', loadDayView);

        // Load initial view
        loadDayView();
    } catch (error) {
        console.error('Failed to load Day Scheduler:', error);
    }
}

async function loadDayView() {
    const day = $('#weekdaySelect').val();
    if (!day) return;

    try {
        // Build a single table: rows = lessons, columns = groups
        const groups = await API.get('/api/groups');
        const container = $('#daySchedulerGrid');
        container.empty();

        // Get lessons count from config
        const config = await API.get('/api/config');
        const lessonsCount = parseInt(config.lessons || 8);

        // Build table skeleton
        const table = $('<table>').addClass('table table-sm table-bordered day-scheduler-table');
        const thead = $('<thead>');
        const headerRow = $('<tr>');
        headerRow.append($('<th>').addClass('lesson-header').text(_('Lesson')));
        groups.forEach(g => headerRow.append($('<th>').text(g.name)));
        thead.append(headerRow);
        table.append(thead);

        const tbody = $('<tbody>');
        const slots = window.timeSlots || {};
        for (let lesson = 1; lesson <= lessonsCount; lesson++) {
            const row = $('<tr>');
            const timeStr = slots[lesson] || '';
            const lessonCell = $('<td>').addClass('lesson-number');
            lessonCell.append($('<div>').text(lesson));
            lessonCell.append($('<div>').addClass('time-slot small text-muted').text(timeStr));
            row.append(lessonCell);
            groups.forEach(g => {
                const cell = $('<td>').attr('data-group', g.name).attr('data-lesson', lesson).addClass('schedule-cell');
                row.append(cell);
            });
            tbody.append(row);
        }
        table.append(tbody);
        container.append(table);

        // Fetch schedules for all groups in parallel and populate cells
        const promises = groups.map(g =>
            API.get(`/api/schedules/group/${encodeURIComponent(g.name)}`)
                .then(schedule => ({ group: g, schedule }))
                .catch(error => ({ group: g, error }))
        );

        const results = await Promise.all(promises);
        for (const res of results) {
            const g = res.group;
            if (res.error) {
                console.error('Failed to load schedule for group', g.name, res.error);
                continue;
            }
            const schedule = res.schedule || {};
            const daySchedule = schedule[day] || {};

            for (let lesson = 1; lesson <= lessonsCount; lesson++) {
                const lessonData = daySchedule[lesson];
                // Find cell by data attributes safely (avoid selector-escaping issues)
                const cell = container.find('td').filter(function() {
                    return $(this).data('group') === g.name && parseInt($(this).data('lesson')) === lesson;
                }).first();

                if (!cell || cell.length === 0) continue;

                if (lessonData) {
                    cell.empty();
                    cell.addClass('filled')
                        .css('background-color', lessonData.color_bg)
                        .css('color', lessonData.color_fg);
                    const content = $('<div>').addClass('cell-content');
                    content.append($('<div>').addClass('subject').text(lessonData.subject));
                    content.append($('<div>').addClass('teacher').text(lessonData.teacher));
                    cell.append(content);
                } else {
                    cell.removeClass('filled').empty().css('background-color', '').css('color', '');
                }
            }
        }

        // Normalize column widths: filled columns wider, empty columns narrower
        const headers = container.find('thead th');
        groups.forEach((g, idx) => {
            const colIndex = idx + 1; // header 0 is Lesson
            let hasContent = false;
            for (let lesson = 1; lesson <= lessonsCount; lesson++) {
                const cell = container.find('td').filter(function() {
                    return $(this).data('group') === g.name && parseInt($(this).data('lesson')) === lesson;
                }).first();
                if (cell && cell.hasClass('filled')) { hasContent = true; break; }
            }

            // Apply width styles
            const header = headers.eq(colIndex);
            const colCells = container.find('td').filter(function() { return $(this).data('group') === g.name; });
            if (hasContent) {
                header.css('min-width', '180px');
                colCells.css('min-width', '180px');
            } else {
                header.css('min-width', '90px');
                colCells.css('min-width', '90px');
            }
        });
    } catch (error) {
        console.error('Failed to load day view:', error);
    }
}

async function loadTeacherSchedule() {
    currentTeacherName = $('#teacherSelect').val();
    if (!currentTeacherName) return;
    
    try {
        const schedule = await API.get(`/api/schedules/teacher/${currentTeacherName}`);
        // Get teacher details to obtain availability slots
        const teachers = await API.get('/api/teachers');
        const teacher = teachers.find(t => t.name === currentTeacherName) || {};
        const avail = teacher.available_slots || {};

        await ScheduleGrid.render('#teacherScheduleGrid', schedule, {
            editable: false,
            teacherAvailableSlots: avail
        });
    } catch (error) {
        console.error('Failed to load teacher schedule:', error);
    }
}

// Lesson Modal
async function showLessonModal(day, lesson, lessonData) {
    $('#lessonForm input[name="day"]').val(day);
    $('#lessonForm input[name="lesson"]').val(lesson);
    try {
        // Reset aggressive overlay and hidden fields every time modal opens
        try {
            $('#aggressiveOverlay').show();
            $('#aggressiveSubjects').css('outline', '');
            $('#lessonForm input[name="aggressive_assigned"]').val('0');
            $('#lessonForm input[name="aggressive_subject"]').val('');
        } catch (e) {}
        const filtered = await getEligibleSubjectsForCell(currentGroupName, day, lesson, lessonData);

        const subjectSelect = $('#lessonForm select[name="subject"]');
        subjectSelect.empty();
        filtered.forEach(f => {
            subjectSelect.append($('<option>').val(f.subj.name).text(f.subj.name + (f.remaining <= 0 ? ' (full)' : '')));
        });

        const teacherSelect = $('#lessonForm select[name="teacher"]');
        teacherSelect.empty();

        // When subject changes, populate teacher list accordingly
        subjectSelect.off('change.filterTeachers').on('change.filterTeachers', function() {
            const subj = $(this).val();
            teacherSelect.empty();
            try { subjectSelect.css('outline', ''); } catch (e) {}
            const found = filtered.find(x => x.subj.name === subj);
            if (found) {
                found.availTeachers.forEach(tn => teacherSelect.append($('<option>').val(tn).text(tn)));
                // apply subject color to select background for quick visual cue
                if (found.color) {
                    try {
                        subjectSelect.css('background-color', found.color.bg).css('color', found.color.fg);
                    } catch (e) {}
                }
            }
        });

        // Preselect values: if lessonData has subject, try to select it
        if (lessonData && lessonData.subject) {
            const opt = subjectSelect.find(`option[value="${lessonData.subject}"]`);
            if (opt.length) {
                subjectSelect.val(lessonData.subject).trigger('change.filterTeachers');
                setTimeout(() => {
                    const tOpt = teacherSelect.find(`option[value="${lessonData.teacher}"]`);
                    if (tOpt.length) teacherSelect.val(lessonData.teacher);
                }, 50);
            }
        } else {
            // select first subject if available
            const first = subjectSelect.find('option').first();
            if (first.length) {
                subjectSelect.val(first.val()).trigger('change.filterTeachers');
            }
        }

        // Populate Aggressive Assigned combobox with all subjects for this group
        try {
            const allSubjects = await API.get('/api/subjects') || [];
            const aggressive = $('#aggressiveSubjects');
            aggressive.empty();
            allSubjects.filter(s => (s.group || '') === currentGroupName).forEach(s => {
                aggressive.append($('<option>').val(s.name).text(s.name));
            });
            // reset flags
            $('#lessonForm input[name="aggressive_assigned"]').val('0');
            $('#lessonForm input[name="aggressive_subject"]').val('');

            // overlay handles dblclick to enable/activate aggressive select
            const overlay = $('#aggressiveOverlay');
            overlay.off('dblclick.activateAgg').on('dblclick.activateAgg', function() {
                try {
                    // enable visually by hiding overlay
                    overlay.hide();
                    // mark aggressive assigned and store currently selected aggressive subject
                    const sel = $('#aggressiveSubjects').val() || '';
                    $('#lessonForm input[name="aggressive_assigned"]').val('1');
                    $('#lessonForm input[name="aggressive_subject"]').val(sel);
                    // visual cue: outline the aggressive select
                    try { $('#aggressiveSubjects').css('outline','3px solid #ff9800'); } catch(e) {}
                } catch (e) { console.warn('activateAgg error', e); }
            });

            // clicking the aggressive select updates the hidden subject value when enabled
            aggressive.off('change.aggChoose').on('change.aggChoose', function() {
                const cur = $(this).val() || '';
                if ($('#lessonForm input[name="aggressive_assigned"]').val() === '1') {
                    $('#lessonForm input[name="aggressive_subject"]').val(cur);
                }
            });

        } catch (e) {
            console.warn('Failed to populate aggressiveSubjects', e);
        }

        bootstrap.Modal.getOrCreateInstance(document.getElementById('lessonModal')).show();
        // Ensure when modal closes we reset aggressive state for next open
        try {
            const modalEl = $('#lessonModal');
            modalEl.off('hidden.bs.modal.resetAgg').on('hidden.bs.modal.resetAgg', function() {
                try {
                    $('#aggressiveOverlay').show();
                    $('#aggressiveSubjects').css('outline', '');
                    $('#lessonForm input[name="aggressive_assigned"]').val('0');
                    $('#lessonForm input[name="aggressive_subject"]').val('');
                } catch (e) {}
            });
        } catch (e) {}
    } catch (e) {
        console.error('Failed to prepare lesson modal:', e);
        const subjectSelect = $('#lessonForm select[name="subject"]');
        subjectSelect.empty();
        const teacherSelect = $('#lessonForm select[name="teacher"]');
        teacherSelect.empty();
        bootstrap.Modal.getOrCreateInstance(document.getElementById('lessonModal')).show();
    }
}

// Compute eligible subjects and available teachers for a particular group's cell
async function getEligibleSubjectsForCell(groupName, day, lesson, lessonData) {
    // Use same data sources as Autofill (subjects, group schedule, teachers, all teacher schedules)
    const subjects = await API.get('/api/subjects') || [];
    const groupSubjects = (subjects || []).filter(s => (s.group || '') === groupName);

    const groupSchedule = await API.get(`/api/schedules/group/${encodeURIComponent(groupName)}`) || {};
    const teachers = await API.get('/api/teachers') || [];
    const allTeacherSchedules = await API.get('/api/schedules/all-teachers') || {};

    // Count occurrences per subject in group's schedule
    const placedCounts = {};
    Object.keys(groupSchedule).forEach(d => {
        const dayObj = groupSchedule[d] || {};
        Object.keys(dayObj).forEach(ln => {
            const ld = dayObj[ln] || {};
            const subj = ld.subject || '';
            if (!subj) return;
            placedCounts[subj] = (placedCounts[subj] || 0) + 1;
        });
    });

    function availableTeachersForSubject(subjName) {
        const list = [];
        teachers.forEach(t => {
            // teacher teaches subj
            const teaches = (t.subjects || []).some(s => s.name === subjName && ((s.group || '') === groupName || !(s.group)));
            if (!teaches) return;

            // availability slots
            if (t.available_slots && Object.keys(t.available_slots).length > 0) {
                const daySlots = t.available_slots[day] || [];
                if (!daySlots.includes(lesson)) return;
            }

            // check teacher schedule occupancy
            const tSched = allTeacherSchedules[t.name] || {};
            if (tSched[day] && tSched[day][lesson]) {
                const existing = tSched[day][lesson];
                if (existing.group && existing.group !== groupName) return; // busy with other group
            }

            list.push(t.name);
        });
        return list;
    }

    const filtered = [];
    for (const s of groupSubjects) {
        const hoursReq = parseInt(s.hours_per_week || 0) || 0;
        const placed = placedCounts[s.name] || 0;
        const remaining = hoursReq - placed;

        const isCurrent = lessonData && lessonData.subject === s.name;

        // Determine assigned teachers for this subject (matching group or any)
        const assignedTeachers = teachers.filter(t => (t.subjects || []).some(ss => ss.name === s.name && ((ss.group || '') === groupName || !(ss.group)))).map(t => t.name);

        let availTeachers = [];
        if (assignedTeachers.length > 1) {
            // subgroup case: require ALL assigned teachers to be available
            let allAvailable = true;
            for (const tn of assignedTeachers) {
                const tObj = teachers.find(tt => tt.name === tn);
                if (!tObj) { allAvailable = false; break; }
                if (tObj.available_slots && Object.keys(tObj.available_slots).length > 0) {
                    const daySlots = tObj.available_slots[day] || [];
                    if (!daySlots.includes(lesson)) { allAvailable = false; break; }
                }
                const tSched = allTeacherSchedules[tn] || {};
                if (tSched[day] && tSched[day][lesson]) {
                    const existing = tSched[day][lesson];
                    if (existing.group && existing.group !== groupName) { allAvailable = false; break; }
                }
            }
            if (allAvailable) {
                // present as a combined entry (subgroup)
                availTeachers = [assignedTeachers.join(';')];
            } else {
                availTeachers = [];
            }
        } else {
            // single-teacher or unassigned: list individual available teachers
            availTeachers = availableTeachersForSubject(s.name);
        }

        if ((remaining > 0 && availTeachers.length > 0) || isCurrent) {
            const color = await getColor(s.name || '');
            filtered.push({ subj: s, availTeachers: availTeachers, remaining: remaining, color });
        }
    }

    return filtered;
}

async function saveLesson() {
    const form = $('#lessonForm');
    const day = form.find('input[name="day"]').val();
    const lesson = parseInt(form.find('input[name="lesson"]').val());
    const subject = form.find('select[name="subject"]').val();
    const teacher = form.find('select[name="teacher"]').val();

    // If aggressive flag set, prefer aggressive subject for saving (do not change UI selects)
    let subjectToSave = subject;
    try {
        const agg = form.find('input[name="aggressive_assigned"]').val();
        const aggSub = form.find('input[name="aggressive_subject"]').val() || '';
        if (agg === '1' && aggSub) subjectToSave = aggSub;
    } catch (e) {}

    // Prefer server color; fallback to local computeColor
    let color = { bg: '#E0E0E0', fg: '#000000' };
    try {
        color = subjectToSave ? await getColor(subjectToSave) : color;
    } catch (e) {}

    const lessonData = {
        subject: subjectToSave,
        teacher: teacher,
        group: currentGroupName,
        color_bg: color.bg,
        color_fg: color.fg
    };
    // include aggressive flag if applied via dblclick
    try {
        const agg = form.find('input[name="aggressive_assigned"]').val();
        if (agg === '1') {
            lessonData.aggressive_assigned = true;
            try { lessonData.aggressive_subject = form.find('input[name="aggressive_subject"]').val() || ''; } catch(e) {}
        }
    } catch (e) {}
    
    try {
        await API.post(`/api/schedules/group/${currentGroupName}/lesson`, {
            day: day,
            lesson: lesson,
            lesson_data: lessonData
        });
        bootstrap.Modal.getInstance(document.getElementById('lessonModal')).hide();
        loadGroupSchedule();
    } catch (error) {
        alert(_('Failed to save lesson: ') + error.message);
    }
}

async function deleteLesson() {
    const form = $('#lessonForm');
    const day = form.find('input[name="day"]').val();
    const lesson = parseInt(form.find('input[name="lesson"]').val());
    
    try {
        await API.delete(`/api/schedules/group/${currentGroupName}/lesson`, {
            day: day,
            lesson: lesson
        });
        bootstrap.Modal.getInstance(document.getElementById('lessonModal')).hide();
        loadGroupSchedule();
    } catch (error) {
        alert(_('Failed to delete lesson: ') + error.message);
    }
}

// Toolbar functions
// refreshData removed per project requirements

function importExcel() {
    alert(_('Import from Excel - to be implemented'));
}

async function exportExcel() {
    try {
        const res = await API.get('/api/admin/export');
        if (res && res.filename) {
            window.location = `/api/download/${res.filename}`;
        } else {
            alert(_('Export failed'));
        }
    } catch (e) {
        alert(_('Export failed: ') + e.message);
    }
}

// Export but open the download in a new tab so script execution can continue
async function exportExcelNoNavigate() {
    try {
        const res = await API.get('/api/admin/export');
        if (res && res.filename) {
            try { window.open(`/api/download/${res.filename}`, '_blank'); } catch (e) { window.location = `/api/download/${res.filename}`; }
            return { success: true };
        } else {
            return { success: false, error: _('Export failed') };
        }
    } catch (e) {
        return { success: false, error: e.message };
    }
}

async function saveToFavorites() {
    try {
        const defaultName = `Favorite ${new Date().toLocaleString()}`;
        const name = prompt(_('Enter favorite name:'), defaultName);
        if (!name) {
            // user cancelled prompt — ensure no stray backdrops remain
            try { _cleanupBackdropsIfNoVisibleModals(); } catch(e){}
            return;
        }
        const res = await API.post('/api/favorites/save', { name: name });
        if (res && res.success) {
            // Success: notify user but do NOT open the Load modal every time
            alert(_('Saved to Favorites'));
            // ensure no stray/backdrop remains after save
            try { _cleanupBackdropsIfNoVisibleModals(); } catch(e) {}
            // If you want to refresh an open favorites modal, we could signal it,
            // but avoid auto-opening the modal here to prevent UX churn.
        } else if (res && res.error === 'max_favorites_reached') {
            // Inform user about the limit and open the modal so they can remove items
            const msg = _('Maximum 10 favorites reached. Open "Load from Favorites", remove one or more entries, then try saving again. Opening the list now.');
            alert(msg);
            try { showFavoritesModal(); } catch(e) { console.warn('Failed to open favorites modal after max limit', e); }
        } else {
            alert(_('Failed to save favorite') + (res && res.error ? (': ' + res.error) : ''));
            try { _cleanupBackdropsIfNoVisibleModals(); } catch(e) {}
        }
    } catch (e) {
        alert(_('Failed to save favorite') + ': ' + e.message);
        try { _cleanupBackdropsIfNoVisibleModals(); } catch(e) {}
    }
}

// Show modal with favorites list
async function showFavoritesModal() {
    // Show modal immediately so UI appears responsive; populate contents asynchronously
    const favModalEl = document.getElementById('favoritesModal');
    if (!favModalEl) {
        alert(_('Favorites modal element not found'));
        return;
    }

    try {
        // cleanup any stray backdrops and reset body state before showing
        try {
            document.querySelectorAll('.modal-backdrop').forEach(e => e.remove());
            document.body.classList.remove('modal-open');
            document.body.style.paddingRight = '';
        } catch (err) { console.warn('Failed to cleanup existing modal backdrops', err); }

        // show modal now (data will be loaded into it)
        const modalInstance = bootstrap.Modal.getOrCreateInstance(favModalEl);
        modalInstance.show();

        // After showing, verify modal is actually visible; if not, attempt a forced fallback show
        setTimeout(() => {
            try {
                const rect = favModalEl.getBoundingClientRect();
                const visible = (rect.width > 0 && rect.height > 0 && window.getComputedStyle(favModalEl).display !== 'none');
                const backdrops = document.querySelectorAll('.modal-backdrop');
                console.debug('favoritesModal visibility check', { visible: visible, rect: rect, backdrops: backdrops.length });
                if (!visible) {
                    console.warn('favoritesModal not visible after show; performing fallback forceShow');
                    // remove extra backdrops
                    document.querySelectorAll('.modal-backdrop').forEach(e => e.remove());

                    // ensure modal is direct child of body (Bootstrap expects this)
                    try { document.body.appendChild(favModalEl); } catch (e) { /* ignore */ }

                    // force styles/classes
                    favModalEl.style.display = 'block';
                    favModalEl.classList.add('show');
                    favModalEl.removeAttribute('aria-hidden');
                    favModalEl.setAttribute('aria-modal', 'true');
                    favModalEl.setAttribute('role', 'dialog');

                    // add single backdrop element
                    const bd = document.createElement('div');
                    bd.className = 'modal-backdrop fade show';
                    document.body.appendChild(bd);

                    // ensure body state
                    document.body.classList.add('modal-open');
                    document.body.style.paddingRight = '';

                    // raise z-index for modal to ensure it's above backdrop
                    favModalEl.style.zIndex = 2000;
                    bd.style.zIndex = 1040;
                }
            } catch (e) { console.error('fallback visibility check failed', e); }
        }, 200);

        // find or create container
        let container = document.getElementById('favoritesList');
        if (!container) {
            const body = favModalEl.querySelector('.modal-body');
            if (body) {
                container = document.createElement('div');
                container.id = 'favoritesList';
                container.style.maxHeight = '400px';
                container.style.overflow = 'auto';
                body.appendChild(container);
            }
        }
        if (!container) {
            console.warn('showFavoritesModal: could not find/create container');
            return;
        }

        // If already loading, avoid re-fetching
        if (_favoritesLoading) {
            console.debug('showFavoritesModal: already loading — skipping fetch');
            return;
        }

        _favoritesLoading = true;
        console.debug('showFavoritesModal: fetching list (async)');
        console.trace('showFavoritesModal called');

        try {
            const res = await API.get('/api/favorites/list');
            console.debug('showFavoritesModal: got', res);
            const list = (res && res.success) ? (res.favorites || []) : [];

            container.innerHTML = '';
            if (!res || !res.success) {
                const errDiv = document.createElement('div');
                errDiv.className = 'alert alert-danger';
                errDiv.textContent = _('Failed to load favorites');
                container.appendChild(errDiv);
                return;
            }

            if (list.length === 0) {
                const empty = document.createElement('div');
                empty.className = 'alert alert-secondary';
                empty.textContent = _('No favorites saved');
                container.appendChild(empty);
            } else {
                list.forEach(f => {
                    try {
                        const row = document.createElement('div');
                        row.className = 'd-flex align-items-center justify-content-between border-bottom py-2';

                        const left = document.createElement('div');
                        const title = document.createElement('div');
                        title.innerHTML = `<strong>${escapeHtml(f.name)}</strong>`;
                        const meta = document.createElement('div');
                        meta.className = 'text-muted small';
                        meta.textContent = new Date(f.created_at).toLocaleString();
                        left.appendChild(title);
                        left.appendChild(meta);

                        const actions = document.createElement('div');

                        const loadBtn = document.createElement('button');
                        loadBtn.className = 'btn btn-sm btn-primary me-2';
                        loadBtn.textContent = _('Load');
                        loadBtn.addEventListener('click', () => loadFavorite(f.id));

                        const delBtn = document.createElement('button');
                        delBtn.className = 'btn btn-sm btn-danger me-2';
                        delBtn.textContent = _('Delete');
                        delBtn.addEventListener('click', () => deleteFavorite(f.id));

                        const renBtn = document.createElement('button');
                        renBtn.className = 'btn btn-sm btn-secondary';
                        renBtn.textContent = _('Rename');
                        renBtn.addEventListener('click', () => promptRenameFavorite(f.id, f.name));

                        actions.appendChild(loadBtn);
                        actions.appendChild(delBtn);
                        actions.appendChild(renBtn);

                        row.appendChild(left);
                        row.appendChild(actions);
                        container.appendChild(row);
                    } catch (innerE) {
                        console.error('Failed to render favorite row', innerE, f);
                    }
                });
            }
        } catch (e) {
            console.error('showFavoritesModal fetch error', e);
            container.innerHTML = '<div class="alert alert-danger">' + _('Failed to load favorites') + '</div>';
        } finally {
            _favoritesLoading = false;
        }
    } catch (e) {
        console.error('showFavoritesModal error outer', e);
        alert(_('Failed to open favorites modal') + ': ' + (e && e.message ? e.message : String(e)));
    }
}

async function loadFavorite(id) {
    try {
        // use hidden iframe to trigger download (avoids popup blockers)
        try {
            const iframe = document.createElement('iframe');
            iframe.style.display = 'none';
            iframe.src = `/api/favorites/download/${id}`;
            document.body.appendChild(iframe);
            setTimeout(() => { try { iframe.remove(); } catch (e) {} }, 30000);
        } catch (e) {
            // fallback to navigation
            try { window.location = `/api/favorites/download/${id}`; } catch (err) { console.error('download fallback failed', err); }
        }
        // hide modal after initiating download
        try { bootstrap.Modal.getOrCreateInstance(document.getElementById('favoritesModal')).hide(); } catch(e) { console.warn('hide modal failed', e); }
    } catch (e) {
        alert(_('Failed to load favorite') + ': ' + e.message);
    }
}

async function deleteFavorite(id) {
    try {
        if (!confirm(_('Delete this favorite?'))) return;
        const res = await API.post('/api/favorites/delete', { id: id });
        if (res && res.success) {
            showFavoritesModal();
        } else {
            alert(_('Failed to delete favorite') + (res && res.error ? (': ' + res.error) : ''));
        }
    } catch (e) {
        alert(_('Failed to delete favorite') + ': ' + e.message);
    }
}

function promptRenameFavorite(id, currentName) {
    const newName = prompt(_('Enter new name:'), currentName || '');
    if (!newName) return;
    renameFavorite(id, newName);
}

async function renameFavorite(id, name) {
    try {
        const res = await API.post('/api/favorites/rename', { id: id, name: name });
        if (res && res.success) {
            showFavoritesModal();
        } else {
            alert(_('Failed to rename favorite') + (res && res.error ? (': ' + res.error) : ''));
        }
    } catch (e) {
        alert(_('Failed to rename favorite') + ': ' + e.message);
    }
}

function escapeHtml(s) {
    if (!s) return '';
    return String(s).replace(/[&<>"']/g, function (m) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"}[m]; });
}

function escapeAttr(s) {
    return escapeHtml(s).replace(/"/g, '&quot;');
}

// backupData and showRestoreModal removed per project requirements

async function clearAllData() {
    // Use app-style confirmation modal (Confirmations.show) so it matches UI.
    Confirmations.show(
        _('Confirm'),
        _('Delete all data files (teachers/groups/subjects/schedules)?'),
        async (confirmed) => {
            if (!confirmed) return;

            try {
                const expRes = await exportExcelNoNavigate();
                if (!expRes || !expRes.success) {
                    alert(_('Export failed: ') + (expRes && expRes.error ? expRes.error : ''));
                    return;
                }

                const res = await API.post('/api/admin/clear-all', {});
                if (res.success) {
                    alert(_('All data cleared'));
                    location.reload();
                } else {
                    alert(_('Clear failed: ') + (res.error || _('unknown')));
                }
            } catch (e) {
                alert(_('Clear failed: ') + e.message);
            }
        }
    );
}

// Ensure favorites modal cleanup handlers are attached once DOM is ready
window.addEventListener('DOMContentLoaded', () => {
    try {
        const favModalEl = document.getElementById('favoritesModal');
        if (!favModalEl) return;

        // When modal is fully hidden, ensure no stray backdrops remain
        favModalEl.addEventListener('hidden.bs.modal', () => {
            try { _cleanupBackdropsIfNoVisibleModals(); } catch (e) { console.warn('favorites hidden handler failed', e); }
        });

        // If user clicks any dismiss buttons inside the modal, run cleanup shortly after
        const dismissBtns = favModalEl.querySelectorAll('[data-bs-dismiss="modal"]');
        dismissBtns.forEach(btn => btn.addEventListener('click', () => setTimeout(() => { try { _cleanupBackdropsIfNoVisibleModals(); } catch(e){} }, 50)));
    } catch (e) { console.warn('favorites modal init failed', e); }
});

// Clear all data without showing a confirmation (used when caller already confirmed)
async function clearAllDataNoConfirm() {
    try {
        const res = await API.post('/api/admin/clear-all', {});
        if (res.success) {
            // do not reload here; caller will handle flow
            return { success: true };
        } else {
            return { success: false, error: res.error };
        }
    } catch (e) {
        return { success: false, error: e.message };
    }
}

async function rebuildAll() {
    // If this is the first invocation from the button, save a flag and reload
    // so the page is refreshed (like Ctrl+R/F5). After reload the function
    // will run again and proceed with the rebuild flow.
    if (!sessionStorage.getItem('rebuild_requested')) {
        sessionStorage.setItem('rebuild_requested', '1');
        location.reload();
        return;
    }
    sessionStorage.removeItem('rebuild_requested');

    // open rebuild modal
    const modalEl = document.getElementById('rebuildModal');
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    // reset steps (guard elements may be missing)
    const el_step_export = document.getElementById('rebuild-step-export'); if (el_step_export) el_step_export.style.display = '';
    const el_step_prio = document.getElementById('rebuild-step-priorities'); if (el_step_prio) el_step_prio.style.display = 'none';
    const el_progress = document.getElementById('rebuild-progress'); if (el_progress) el_progress.style.display = 'none';
    const el_run = document.getElementById('rebuild-run'); if (el_run) el_run.style.display = 'none';
    modal.show();

    // handlers
    const btn_export_now = document.getElementById('rebuild-export-now');
    if (btn_export_now) btn_export_now.onclick = async () => {
        await exportExcel();
        // after export, show priorities
        showRebuildPriorities();
    };
    const btn_continue = document.getElementById('rebuild-continue');
    if (btn_continue) btn_continue.onclick = () => { showRebuildPriorities(); };

    const btn_run = document.getElementById('rebuild-run');
    if (!btn_run) return; // nothing to run
    btn_run.onclick = async () => {
        // hide Run to prevent duplicate long-running requests; it will
        // be shown again only when `rebuildAll()` is started anew.
        try { btn_run.style.display = 'none'; } catch (e) { /* ignore */ }
        // gather priorities
        const gather = (id) => Array.from(document.querySelectorAll(`#${id} .list-group-item`)).map(el=>el.dataset.value);
        const priorities = {
            groups: gather('prio-groups'),
            subjects: gather('prio-subjects'),
            teachers: gather('prio-teachers'),
            days: gather('prio-days')
        };

        const el_prio = document.getElementById('rebuild-step-priorities'); if (el_prio) el_prio.style.display = 'none';
        const el_prog = document.getElementById('rebuild-progress'); if (el_prog) el_prog.style.display = '';
        const el_prog_text = document.getElementById('rebuild-progress-text'); if (el_prog_text) el_prog_text.textContent = _('Running...');

        try {
            const res = await API.post('/api/admin/rebuild-all', { priorities });
            // Show detailed results
            const container = document.getElementById('rebuild-progress');
            let html = '';
            if (res && res.log && Array.isArray(res.log)) {
                html += `<div class="mb-2"><strong>${_('Rebuild results')}</strong></div>`;
                html += '<div class="list-group">';
                let anyFailures = false;
                res.log.forEach(item => {
                    const grp = item.group || '';
                    const ok = !!item.success;
                    const attempts = item.attempts || 0;
                    const info = item.info || {};
                    const incomplete = info.incomplete || [];
                    const errors = info.errors || [];
                    if (!ok || (incomplete && incomplete.length>0) ) anyFailures = true;

                    const displayAttempts = (ok && attempts === 0) ? 1 : attempts;
                    html += `<div class="list-group-item">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <strong>${grp}</strong>
                                <div class="small text-muted">${ok? _('Success') : _('Failed')} — ${_('Attempts')}: ${displayAttempts}</div>
                            </div>
                            <div>
                                `;

                    // if there are incomplete placements, offer an Open Teacher control
                    const teachersList = (incomplete && incomplete.length>0 && incomplete[0].teachers) ? incomplete[0].teachers : [];
                    if (teachersList && teachersList.length > 0) {
                        if (teachersList.length === 1) {
                            const firstProblemTeacher = teachersList[0];
                            const href = `${window.location.origin}${window.location.pathname}?tab=teacher-scheduler&editTeacher=${encodeURIComponent(firstProblemTeacher)}`;
                            html += `<a class="btn btn-sm btn-primary" target="_blank" href="${href}">${_('Open Teacher')}</a>`;
                        } else {
                            // multiple teachers -> render a combo box + Open button
                            // create a safe id based on group and index
                            const selId = 'open-teacher-select-' + (grp ? grp.replace(/[^a-zA-Z0-9_-]/g, '_') : 'grp') + '-' + Math.floor(Math.random()*10000);
                            html += `<select id="${selId}" class="form-select form-select-sm d-inline-block me-2" style="min-width:160px">`;
                            teachersList.forEach(t => {
                                const esc = String(t).replace(/"/g, '&quot;');
                                html += `<option value="${esc}">${esc}</option>`;
                            });
                            html += `</select>`;
                            // inline onclick opens selected teacher in new tab
                            html += `<button class="btn btn-sm btn-primary" onclick="(function(){const s=document.getElementById('${selId}'); if(s && s.value) { window.open(window.location.origin+window.location.pathname+'?tab=teacher-scheduler&editTeacher='+encodeURIComponent(s.value),'_blank'); } })()">${_('Open Teacher')}</button>`;
                        }
                    }

                    html += `</div></div><div class="mt-2">`;

                    if (incomplete && incomplete.length>0) {
                        html += `<div><strong>${_('Incomplete placements')}:</strong></div><ul>`;
                        incomplete.forEach(it=>{
                            const teachers = (it.teachers||[]).join(', ');
                            html += `<li>${it.subject}: ${it.placed}/${it.required} (${_('Teachers')}: ${teachers})</li>`;
                        });
                        html += '</ul>';
                    }

                    if (errors && errors.length>0) {
                        html += `<div><strong>${_('Errors')}:</strong><pre class="small text-danger">${errors.join('\n')}</pre></div>`;
                    }

                    html += '</div></div>';
                });
                html += '</div>';

                if (container) container.innerHTML = html;

                // Open Teacher now opens in a new tab via deep-link; no in-page handler required.

                if (!anyFailures) {
                    if (el_prog_text) el_prog_text.textContent = _('Rebuild completed');
                    setTimeout(()=>location.reload(), 1200);
                } else {
                    if (el_prog_text) el_prog_text.textContent = _('Rebuild completed with issues — see details below');
                }
            } else if (res && res.success) {
                if (el_prog_text) el_prog_text.textContent = _('Rebuild completed');
                setTimeout(()=>location.reload(), 1200);
            } else {
                if (el_prog_text) el_prog_text.textContent = _('Rebuild failed: ') + (res.error||'');
            }
        } catch (e) {
            if (el_prog_text) el_prog_text.textContent = _('Rebuild failed: ') + e.message;
        }
    };

    // helper to show priorities UI and populate lists
    async function showRebuildPriorities() {
        document.getElementById('rebuild-step-export').style.display = 'none';
        document.getElementById('rebuild-step-priorities').style.display = '';
        document.getElementById('rebuild-run').style.display = '';
        // fetch data
        try {
            const data = await API.get('/api/admin/priorities-data');
            const fillList = (id, items)=>{
                const container = document.getElementById(id);
                container.innerHTML='';
                (items||[]).forEach(it=>{
                    const li = document.createElement('div');
                    li.className='list-group-item d-flex justify-content-between align-items-center';
                    li.dataset.value = it;
                    li.innerHTML = `<span>${it}</span><span class=\"btn-group\" role=\"group\"><button class=\"btn btn-sm btn-light prio-up\">▲</button><button class=\"btn btn-sm btn-light prio-down\">▼</button></span>`;
                    container.appendChild(li);
                });
                // attach handlers
                container.querySelectorAll('.prio-up').forEach(btn=>btn.onclick = (ev)=>{
                    const li = ev.target.closest('.list-group-item');
                    if (!li) return;
                    const prev = li.previousElementSibling;
                    if (prev) li.parentNode.insertBefore(li, prev);
                });
                container.querySelectorAll('.prio-down').forEach(btn=>btn.onclick = (ev)=>{
                    const li = ev.target.closest('.list-group-item');
                    if (!li) return;
                    const next = li.nextElementSibling;
                    if (next) li.parentNode.insertBefore(next, li);
                });
            };

            fillList('prio-groups', data.groups.map(g=> typeof g==='string'?g:(g.name||'')) );
            fillList('prio-subjects', data.subjects.map(s=> s.name || s));
            fillList('prio-teachers', data.teachers.map(t=> t.name || t));
            fillList('prio-days', data.weekdays || []);
        } catch (e) {
            alert(_('Failed to load priorities data: ') + e.message);
        }
    }
}

// If a rebuild was requested before reload, auto-run the rebuild flow now.
if (sessionStorage.getItem('rebuild_requested')) {
    window.addEventListener('DOMContentLoaded', () => {
        try {
            rebuildAll();
        } catch (e) {
            // ignore any error to avoid breaking page load
            console.error('Auto rebuild failed', e);
        }
    });
}

// Weekday presets helper: populate preset select and wire editing UI
function getWeekdayPresets() {
    return {
        'en-ltr': ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],
        'en-rtl': ['Saturday','Friday','Thursday','Wednesday','Tuesday','Monday'],
        'he-ltr': ['יום ראשון','יום שני','יום שלישי','יום רביעי','יום חמישי','יום שישי'],
        'he-rtl': ['יום שישי','יום חמישי','יום רביעי','יום שלישי','יום שני','יום ראשון'],
        'ru-ltr': ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота'],
        'ru-rtl': ['Суббота','Пятница','Четверг','Среда','Вторник','Понедельник']
    };
}

// Initialize weekday preset UI after DOM ready
window.addEventListener('DOMContentLoaded', () => {
    const presetSelect = document.getElementById('weekdayPresetSelect');
    const weekdaysInput = document.getElementById('weekdaysInput');
    if (!presetSelect || !weekdaysInput) return;

    const presets = getWeekdayPresets();
    
    // Store original value to detect changes
    let originalWeekdays = weekdaysInput.value;
    
    // Fix: Force initial update after short delay to ensure proper initialization
    setTimeout(() => {
        const currentVal = weekdaysInput.value && weekdaysInput.value.trim();
        if (currentVal) {
            const normalized = currentVal.split(',').map(s=>s.trim()).join(',');
            Object.keys(presets).forEach(key => {
                if (presets[key].join(',') === normalized) {
                    presetSelect.value = key;
                }
            });
        }
    }, 100);

    presetSelect.addEventListener('click', (ev) => {
        // Wait for selection to complete
        setTimeout(() => {
            const val = presetSelect.value;
            if (presets[val]) {
                const newWeekdays = presets[val].join(',');
                
                // Show warning if weekdays will change
                if (originalWeekdays !== newWeekdays) {
                    const confirmed = confirm(
                        _('Warning: Changing weekday names will significantly affect the schedule!') + '\n\n' +
                        _('Teacher working days will need to be redone.') + '\n\n' +
                        _('Are you sure you want to continue?')
                    );
                    
                    if (!confirmed) {
                        return;
                    }
                    originalWeekdays = newWeekdays;
                }
                
                weekdaysInput.value = newWeekdays;
            }
        }, 50);
    });

    // Handle manual editing of weekdays input
    weekdaysInput.addEventListener('blur', (ev) => {
        const newValue = weekdaysInput.value.trim();
        const normalizedNew = newValue.split(',').map(s=>s.trim()).join(',');
        const normalizedOriginal = originalWeekdays.split(',').map(s=>s.trim()).join(',');
        
        if (normalizedNew !== normalizedOriginal && normalizedNew !== '') {
            const confirmed = confirm(
                _('Warning: Changing weekday names will significantly affect the schedule!') + '\n\n' +
                _('Teacher working days will need to be redone.') + '\n\n' +
                _('Are you sure you want to continue?')
            );
            
            if (!confirmed) {
                // Revert to original
                weekdaysInput.value = originalWeekdays;
            } else {
                // Update original to new value
                originalWeekdays = newValue;
            }
        }
    });
});

function clearAllSchedules() {
    Confirmations.clearSchedules(async (confirmed) => {
        if (confirmed) {
            try {
                await API.post('/api/schedules/clear');
                alert(_('All schedules cleared'));
                loadGroupSchedule();
                loadTeacherSchedule();
            } catch (error) {
                alert(_('Failed to clear schedules: ') + error.message);
            }
        }
    });
}

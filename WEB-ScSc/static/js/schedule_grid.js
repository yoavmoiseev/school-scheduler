// Schedule Grid Renderer

const ScheduleGrid = {
    currentSchedule: {},
    currentConfig: {},
    
    async render(selector, schedule, options = {}) {
        const container = $(selector);
        container.empty();
        
        this.currentSchedule = schedule;
        
        // Get config
        if (!this.currentConfig.WEEKDAYS) {
            this.currentConfig = await API.get('/api/config');
        }
        
        const weekdays = this.currentConfig.WEEKDAYS.split(',');
        const lessonsCount = parseInt(this.currentConfig.lessons || 8);
        const lessons = Array.from({length: lessonsCount}, (_, i) => i + 1);
        
        // DEBUG
        console.log('=== ScheduleGrid Debug ===');
        console.log('Config weekdays:', weekdays);
        console.log('Schedule keys:', Object.keys(schedule));
        console.log('Full schedule:', schedule);
        
        // Create table
        const table = $('<table>').addClass('schedule-table table table-bordered');
        
        // Header row
        const headerRow = $('<tr>');
        headerRow.append($('<th>').addClass('lesson-header').text(_('Lesson')));
        weekdays.forEach(day => {
            headerRow.append($('<th>').addClass('day-header').text(day.trim()));
        });
        const thead = $('<thead>').append(headerRow);
        table.append(thead);
        
        // Data rows
        const tbody = $('<tbody>');
        lessons.forEach(lesson => {
            const row = $('<tr>');
            // show lesson number and time slot (if available)
            const slots = window.timeSlots || {};
            const timeStr = slots[lesson] || '';
            const lessonCell = $('<td>').addClass('lesson-number');
            const lessonHtml = $('<div>').css('line-height','1').append($('<div>').text(lesson));
            const ts = $('<div>').addClass('time-slot small text-muted').text(timeStr);
            lessonCell.append(lessonHtml).append(ts);
            row.append(lessonCell);
            
            weekdays.forEach(day => {
                const dayTrimmed = day.trim();
                const cell = $('<td>').addClass('schedule-cell');
                const lessonData = schedule[dayTrimmed] && schedule[dayTrimmed][lesson];
                
                if (lessonData) {
                    cell.addClass('filled')
                        .css('background-color', lessonData.color_bg)
                        .css('color', lessonData.color_fg);
                    
                    const content = $('<div>').addClass('cell-content');
                    content.append($('<div>').addClass('subject').text(lessonData.subject));
                    content.append($('<div>').addClass('teacher').text(lessonData.teacher));
                    if (lessonData.group) {
                        content.append($('<div>').addClass('group').text(lessonData.group));
                    }
                    cell.append(content);
                }
                
                // If teacher availability was provided, gray-out unavailable slots
                if (options.teacherAvailableSlots && Object.keys(options.teacherAvailableSlots).length > 0) {
                    const avail = options.teacherAvailableSlots[dayTrimmed] || [];
                    const isAvailable = avail.includes ? avail.includes(lesson) : (avail.indexOf && avail.indexOf(lesson) !== -1);
                    if (!isAvailable && !lessonData) {
                        cell.addClass('unavailable').css('background', 'linear-gradient(180deg, #f3f3f3 0%, #bfbfbf 50%, #8f8f8f 100%)').css('color', '#000000');
                    }
                }

                if (options.editable) {
                    cell.css('cursor', 'pointer');
                    cell.click(() => {
                        if (options.onCellClick) {
                            options.onCellClick(dayTrimmed, lesson, lessonData);
                        }
                    });
                }
                
                row.append(cell);
            });
            
            tbody.append(row);
        });
        table.append(tbody);
        
        container.append(table);
    }
};

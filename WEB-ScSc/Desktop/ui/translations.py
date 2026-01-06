# translations.py
# Все тексты, видимые пользователю, из ui_build.py
# В порядке появления. Индексы (# 1, # 2, ...) используются в ui_build.py как GUI_TEXT[i].

from school_scheduler.data.consts import *

ENGLISH = [
    
    "Add Teacher",            # 1
    "Add Group",              # 2
    "Add Subject",            # 3
    "Save All",               # 4
    "ReBuild All",            # 5

    "Teachers",               # 6
    "Groups",                 # 7
    "Subjects",               # 8
    "Day view",               # 9
    "Group Scheduler",        # 10
    "Teacher Scheduler",      # 11

    "Name",                   # 12
    "Subjects",               # 13
    "TotalHours",             # 14
    "Name",                   # 15
    "Name",                   # 15
    "Subjects (name : hours : group;)",  # 16
    "Total Hours",            # 17

    "Edit Selected",          # 18
    "Delete Selected",        # 19

    "Name",                   # 20
    "Size",                   # 21
    "Name",                   # 22
    "Size",                   # 23

    "Edit Selected",          # 24
    "Delete Selected",        # 25

    "Name",                   # 26
    "Hours",                  # 27
    "Group",                  # 28
    "Name",                   # 29
    "Hours/week",             # 30
    "Group",                  # 31

    "Edit Selected",          # 32
    "Delete Selected",        # 33

    "Select day:",            # 34
    "Print to PDF",           # 35

    "Select group:",          # 36
    "Clear",                  # 37
    "Auto-fill for group",    # 38
    "Save Group Schedule",    # 39
    "Print to PDF",           # 40

    "Select teacher:",        # 41
    "Print to PDF",           # 42
    "Please select a group!",  # 43
    "Info: No subjects defined for this group",       # 44 messagebox.showinfo when group has no subjects
    "Warning: Some subjects could not be fully scheduled", # 45 warning for incomplete autofill
    "Error: Could not fully schedule after max attempts", # 46 error after MAX_ATTEMPTS
    "Info: Autofill attempt successful",             # 47 optional info after successful fill
    "Placeholder for future messages",               # 48 reserved for future localization
    # buttons_functions.py STARTS HERE
    "Saving data snapshot...",                      # 49 (was: before copying DATA_DIR)
    "Error: DATA_DIR folder not found:",             # 50 (was: "❌ Папка DATA_DIR не найдена")
    "Backup created successfully at:",               # 51 (was: "✅ Папка data сохранена как")
    "Error while saving data:",                      # 52 (was: "❌ Ошибка при сохранении")
    "Rebuild the schedule",                          # 53 (was: "Rebuild the schedule" - window title)
    "Delete and rebuild last schedule?",              # 54 (was: "Delete and rebuild last schedule?")
    "Info: Schedule rebuilt successfully.",           # 55 (was: "Расписание пересоздано.")
    "Error: No active window to capture.",            # 56 (was: "Ошибка: Нет активного окна для скриншота.")
    "PDF saved (Landscape):",                         # 57 (was: "✅ PDF сохранён (Landscape)")
    # START OF popups.py file
        "Add Teacher",                             # 58
    "Name",                                    # 59
    "Available subjects",                      # 60
    "Hours/week",                              # 61
    "Group (optional)",                        # 62
    "Add >>",                                  # 63
    "<< Remove",                               # 64
    "Selected subjects (name:hours:group)",    # 65
    "Add",                                     # 66
    "Error",                                   # 67
    "Select a subject to add",                 # 68
    "Hours must be integer",                   # 69
    "Info",                                    # 70
    "Subject already added",                   # 71
    "Name required",                           # 72
    "Add Group",                               # 73
    "Size (int)",                              # 74
    "Size must be integer",                    # 75
    "Add Subject",                             # 76
    "Hours per week (int)",                    # 77
    "Group (required)",                        # 78
    "Group required for subject",              # 79
    "End of popups.py code file",              # 80
    # START of ui_handlers.py
        "Edit Teacher",                    # 81
    "Select a teacher to edit",        # 82
    "Teacher not found",               # 83
    "Name",                            # 84
    "Available subjects",              # 85
    "Hours/week",                      # 86
    "Subject already added",           # 87
    "Selected subjects (name:hours:group)",  # 88
    "Availability (day:start-end)",    # 89
    "Start/End must be integers",      # 90
    "Choose a day",                    # 91
    "Add Interval",                    # 92
    "Remove Interval",                 # 93
    "Save",                             # 94
    "Error",                            # 95
    "Info",                             # 96
    "Confirm",                          # 97
    "Delete teacher '{name}'?",         # 98
    "Select a teacher to delete",       # 99
    "Add >>",                           # 100
    "<< Remove",                        # 101
    "General Configuration",           # 102
    # General Configuration tab texts (additional)
    "Application title:",          # 103
    "Window size (WxH):",         # 104
    "GUI language:",              # 105
    "Autofill direction:",        # 106
    "Max autofill retries:",      # 107
    "Number of lessons:",         # 108
    "Time slots:",                # 109
    "Lesson",                     # 110
    "Time range",                 # 111
    "L:",                         # 112
    "T:",                         # 113
    "Edit weekdays:",             # 114
    "If you edit weekdays — all data must be manually reentered! Use keyboard for editing, one day per line.", # 115
    "Max sequence lessons:",      # 116
    "Max lessons per day:",       # 117
    "Save",                       # 118
    "Reload last saved",          # 119
    "Reset to defaults",          # 120
    'Load',                     # 121
    'Save As',                    # 122
    "Changes will take effect only after fully restarting the application." , # 123
    "The selected folder is missing required files:", # 124
    "Are you sure you want to reload the last saved configuration? The application will restart and all unsaved changes will be lost.",  # 125
    "Error during loading",        # 126
    "Move Up ↑",                   # 127
    "Move Down ↓",                 # 128
    "Availability Lessons: (start : end)", # 129
    "DAY",                         # 130
    "AVAILABILITY HOURS",          # 131
    "TEACHER WEEKLY HOURS",        # 132
    "Start time (HH:MM)",          # 133
    "End time (HH:MM)",            # 134
    "Add Lesson",                  # 135
    "Add Lessons/Time Slots",      # 136
    "Add Day Hours",               # 137
    "Save Changes",                # 138
    "LESSONS",                     # 139
    "TIME SLOTS",                  # 140
    "Clear Schedulers",            # 141
    "Delete All",                  # 142
    "Delete all schedules? This will remove all generated schedules but keep Teachers, Groups, and Subjects.", # 143
    "Delete ALL data? This will remove Teachers, Groups, Subjects, and Schedules. Everything will be cleared!", # 144
    "Schedules cleared successfully.", # 145
    "All data cleared successfully.", # 146
    "Export to Excel",             # 147
    "Load from Excel",             # 148
    "Edit Subject",                # 149
    "Hours per week (int)",        # 150
    "Group (required)",            # 151
    "Select a subject to delete",  # 152
    "Confirm",                     # 153
    "Delete subject",              # 154
    "Warning! This subject is already assigned to:",  # 155
    "This is only acceptable if the subject is divided into subgroups.",  # 156
    "Warning",                     # 157
    "Assigned/Available",          # 158
    "Reporting Time / Dismissal Time",  # 159
    "Total Hours Per Group",      # 160
    # New translations for previously hardcoded messages
    "Select a group to save",     # 161
    "Saved",                       # 162
    "Group schedule for {group_name} saved",  # 163
    "Select a teacher to save",   # 164
    "Teacher schedule for {teacher_name} saved",  # 165
    "Select a group to edit",     # 166
    "Group not found",             # 167
    "Select a group to delete",   # 168
    "Delete group '{name}'?",     # 169
    "Select a subject to edit",   # 170
    "Subject not found",           # 171
    "Select a teacher to move",   # 172
    "Select a group to move",     # 173
    "Select a subject to move",   # 174
    "Please select start and end times",  # 175
    "Start time must be before end time",  # 176
    "Invalid time format",        # 177
    "Please enter check in/out times",  # 178
    "No lessons found in this time range. Check your times.",  # 179
    "openpyxl library is not installed. Please install it:\npip install openpyxl",  # 180
    "Success",                     # 181
    "Schedules exported successfully to:\n{file_path}",  # 182
    "Failed to export to Excel:\n{error}",  # 183
    "Imported from Excel:\n{items}",  # 184
    "No data found in Excel file",  # 185
    "Failed to load from Excel:\n{error}",  # 186
    "Config",                      # 187
    "The configuration successfully saved.",  # 188
    "Failed to save consts.py (see console).",  # 189
    "Reloaded from consts.py",    # 190
    "Reset to source_consts.py defaults.",  # 191
    "source_consts.py not found.", # 192
    "Neither consts.py nor source_consts.py found.",  # 193
    "Error deleting schedules.json: {error}",  # 194
    "Error deleting {filename}: {error}",  # 195
    "Comment",                    # 196
    "Excel files",                # 197
    "All files",                  # 198
    "Are you sure you want to save the configuration? This will apply the changes.",  # 199
    "Are you sure you want to reset to defaults? All current changes will be lost!",  # 200
]




HEBREW = [

    "הוסף מורה",              # 1
    "הוסף קבוצה",             # 2
    "הוסף מקצוע",             # 3
    "שמור הכל",               # 4
    "בנה מחדש הכל",           # 5

    "מורים",                  # 6
    "קבוצות",                 # 7
    "מקצועות",                # 8
    "תצוגת יום",             # 9
    "תזמן קבוצות",           # 10
    "תזמן מורים",            # 11

    "שם",                     # 12
    "מקצועות",                # 13
    "סה\"כ שעות",            # 14
    "שם",                     # 15
    "שם",                     # 15
    "מקצועות (שם : שעות : קבוצה;)",  # 16
    "סה\"כ שעות",            # 17

    "ערוך נבחר",              # 18
    "מחק נבחר",               # 19

    "שם",                     # 20
    "גודל",                   # 21
    "שם",                     # 22
    "גודל",                   # 23

    "ערוך נבחר",              # 24
    "מחק נבחר",               # 25

    "שם",                     # 26
    "שעות",                   # 27
    "קבוצה",                  # 28
    "שם",                     # 29
    "שעות/שבוע",              # 30
    "קבוצה",                  # 31

    "ערוך נבחר",              # 32
    "מחק נבחר",               # 33

    "בחר יום:",               # 34
    "הדפס ל-PDF",             # 35

    "בחר קבוצה:",             # 36
    "נקה",                     # 37
    "מילוי אוטומטי לקבוצה",   # 38
    "שמור תזמון קבוצה",       # 39
    "הדפס ל-PDF",             # 40

    "בחר מורה:",              # 41
    "הדפס ל-PDF",             # 42
"בבקשה לבחור קבוצה",         # 43
"מידע: לא הוגדרו מקצועות עבור הקבוצה הזו",       # 44 messagebox.showinfo כאשר לקבוצה אין מקצועות
"אזהרה: חלק מהמקצועות לא יכלו להיות מתוזמנים במלואם", # 45 אזהרה עבור מילוי אוטומטי לא שלם
"שגיאה: לא ניתן היה לתזמן במלואו לאחר מספר הנסיונות המרבי", # 46 שגיאה לאחר MAX_ATTEMPTS
"מידע: ניסיון מילוי אוטומטי הצליח",             # 47 מידע אופציונלי לאחר מילוי מוצלח
"מקום שמור עבור הודעות בעתיד",               # 48 שמור עבור לוקליזציה עתידית
# buttons_functions.py STARTS HERE
    "שומר עותק נתונים...",                               # 49
    "שגיאה: תיקיית DATA_DIR לא נמצאה:",                  # 50
    "גיבוי נשמר בהצלחה בתיקייה:",                         # 51
    "שגיאה במהלך השמירה:",                                # 52
    "בנה מחדש את מערכת השעות",                           # 53
    "למחוק ולבנות מחדש את מערכת השעות האחרונה?",         # 54
    "מערכת השעות נבנתה מחדש בהצלחה.",                    # 55
    "שגיאה: אין חלון פעיל לצילום מסך.",                   # 56
    "PDF נשמר (מצב רוחבי):",                              # 57
    # START OF popups.py file
    "הוסף מורה",                              # 58
    "שם",                                     # 59
    "מקצועות זמינים",                         # 60
    "שעות לשבוע",                             # 61
    "קבוצה (לא חובה)",                        # 62
    "הוסף >>",                                # 63
    "<< הסר",                                 # 64
    "מקצועות שנבחרו (שם:שעות:קבוצה)",         # 65
    "הוסף",                                   # 66
    "שגיאה",                                  # 67
    "בחר מקצוע להוספה",                       # 68
    "השעות חייבות להיות מספר שלם",            # 69
    "מידע",                                   # 70
    "המקצוע כבר נוסף",                        # 71
    "נדרש שם",                                # 72
    "הוסף קבוצה",                             # 73
    "גודל (מספר שלם)",                        # 74
    "הגודל חייב להיות מספר שלם",              # 75
    "הוסף מקצוע",                             # 76
    "שעות לשבוע (מספר שלם)",                  # 77
    "קבוצה (נדרש)",                           # 78
    "נדרשת קבוצה למקצוע",                     # 79
    "סוף קובץ popups.py",                     # 80
    # START of ui_handlers.py
    "ערוך מורה",                        # 81
    "בחר מורה לעריכה",                  # 82
    "המורה לא נמצא",                    # 83
    "שם",                               # 84
    "מקצועות זמינים",                   # 85
    "שעות לשבוע",                        # 86
    "המקצוע כבר נוסף",                  # 87
    "מקצועות שנבחרו (שם:שעות:קבוצה)",   # 88
    "זמינות (יום:התחלה-סיום)",         # 89
    "השעות חייבות להיות מספר שלם",      # 90
    "בחר יום",                           # 91
    "הוסף פרק זמן",                     # 92
    "הסר פרק זמן",                      # 93
    "שמור",                             # 94
    "שגיאה",                             # 95
    "מידע",                              # 96
    "אישור",                             # 97
    "האם למחוק את המורה '{name}'?",     # 98
    "בחר מורה למחיקה",                  # 99
    "הוסף >>",                           # 100
    "<< הסר" ,                           # 101
    "הגדרות כלליות",                   # 102
    # General Config Tab 
    "כותרת היישום:",                # 103
    "גודל חלון (WxH):",             # 104
    "שפת ממשק:",                    # 105
    "כיוון מילוי אוטומטי:",         # 106
    "מקס מספר ניסיונות מילוי:",     # 107
    "מספר שיעורים:",                # 108
    "חלונות זמן:",                  # 109
    "שיעור",                        # 110
    "טווח זמן",                     # 111
    "ש:",                            # 112
    "ז:",                            # 113
    "ערוך ימות השבוע:",             # 114
    "אם תערוך את ימות השבוע — כל הנתונים יצטרכו להיות מוזנים מחדש! השתמש במקלדת, שורה לכל יום.", # 115
    "מקס שיעורים ברצף:",            # 116
    "מקס שיעורים ליום:",             # 117
    "שמור",                          # 118
    "טען שמור אחרון",               # 119
    "איפוס להגדרות ברירת מחדל",                 # 120
    'טען',                          # 121
    'שמור בשם' ,                     # 122
    " השינויים ייכנסו לתוקף רק לאחר הפעלה מחדש מלאה של היישום.", # 123
    " התיקייה שנבחרה חסרה קבצים נדרשים:" ,   # 124
    "האם אתה בטוח שברצונך לטעון את התצורה השמורה האחרונה? היישום יופעל מחדש וכל השינויים שלא נשמרו יאבדו.",     # 125
    "שגיאה במהלך הטעינה",         # 126
    "הזז למעלה ↑",                 # 127
    "הזז למטה ↓",                  # 128
    "שיעורים זמינים: (התחלה : סוף)",      # 129
    "יום",                         # 130
    "שעות זמינות",                 # 131
    "שעות שבועיות של מורה",        # 132
    "שעת התחלה (HH:MM)",           # 133
    "שעת סיום (HH:MM)",            # 134
    "הוסף שיעור",                  # 135
    "הוסף שיעורים/משבצות זמן",             # 136
    "הוסף שעות יום",              # 137
    "שמור שינויים",                # 138
    "שיעורים",                     # 139
    "משבצות זמן",                  # 140
    "נקה לוחות זמנים",            # 141
    "מחק הכל",                     # 142
    "למחוק את כל לוחות הזמנים? פעולה זו תסיר את כל לוחות הזמנים שנוצרו אך תשמור על מורים, קבוצות ומקצועות.", # 143
    "למחוק את כל הנתונים? פעולה זו תסיר מורים, קבוצות, מקצועות ולוחות זמנים. הכל יימחק!", # 144
    "לוחות הזמנים נוקו בהצלחה.",  # 145
    "כל הנתונים נוקו בהצלחה.",    # 146
    "ייצא לאקסל",                 # 147
    "טען מאקסל",                  # 148
    "ערוך מקצוע",                 # 149
    "שעות בשבוע (מספר שלם)",      # 150
    "קבוצה (נדרש)",               # 151
    "בחר מקצוע למחיקה",           # 152
    "אישור",                      # 153
    "מחק מקצוע",                  # 154
    "אזהרה! מקצוע זה כבר מוקצה ל:",  # 155
    "זה מקובל רק אם המקצוע מחולק לתת-קבוצות.",  # 156
    "אזהרה",                      # 157
    "זמין/מוקצה",                 # 158
    "שעת הגעה / שעת שחרור",          # 159
    "סה\"כ שעות לקבוצה",         # 160
    # New translations for previously hardcoded messages
    "בחר קבוצה לשמירה",           # 161
    "נשמר",                       # 162
    "לוח זמנים של קבוצה {group_name} נשמר",  # 163
    "בחר מורה לשמירה",            # 164
    "לוח זמנים של מורה {teacher_name} נשמר",  # 165
    "בחר קבוצה לעריכה",           # 166
    "קבוצה לא נמצאה",             # 167
    "בחר קבוצה למחיקה",           # 168
    "למחוק קבוצה '{name}'?",     # 169
    "בחר מקצוע לעריכה",           # 170
    "מקצוע לא נמצא",              # 171
    "בחר מורה להזזה",             # 172
    "בחר קבוצה להזזה",            # 173
    "בחר מקצוע להזזה",            # 174
    "אנא בחר שעות התחלה וסיום",   # 175
    "שעת ההתחלה חייבת להיות לפני שעת הסיום",  # 176
    "פורמט זמן לא תקין",          # 177
    "אנא הזן שעות כניסה/יציאה",    # 178
    "לא נמצאו שיעורים בטווח זמן זה. בדוק את הזמנים.",  # 179
    "ספריית openpyxl לא מותקנת. אנא התקן אותה:\npip install openpyxl",  # 180
    "הצלחה",                      # 181
    "לוחות זמנים יוצאו בהצלחה אל:\n{file_path}",  # 182
    "כשל בייצוא ל-Excel:\n{error}",  # 183
    "יובא מ-Excel:\n{items}",     # 184
    "לא נמצאו נתונים בקובץ Excel",  # 185
    "כשל בטעינה מ-Excel:\n{error}",  # 186
    "תצורה",                      # 187
    "התצורה נשמרה בהצלחה.",       # 188
    "כשל בשמירת consts.py (ראה קונסול).",  # 189
    "נטען מחדש מ-consts.py",      # 190
    "אופס לברירות מחדל של source_consts.py.",  # 191
    "source_consts.py לא נמצא.",  # 192
    "לא נמצאו consts.py ו-source_consts.py.",  # 193
    "שגיאה במחיקת schedules.json: {error}",  # 194
    "שגיאה במחיקת {filename}: {error}",  # 195
    "הערה",                      # 196
    "קבצי Excel",                 # 197
    "כל הקבצים",                  # 198
    "האם אתה בטוח שברצונך לשמור את התצורה? זה יחיל את השינויים.",  # 199
    "האם אתה בטוח שברצונך לאפס לברירות מחדל? כל השינויים הנוכחיים יאבדו!",  # 200
]


RUSSIAN = [
    "Добавить преподавателя",   # 1
    "Добавить группу",          # 2             
    "Добавить предмет",         # 3             
    "Сохранить все",            # 4 
    "Перестроить все",          # 5
    "Преподаватели",            # 6
    "Группы",                   # 7 
    "Предметы",                 # 8
    "Просмотр дня",             # 9
    "Расписание группы",        # 10
    "Расписание преподавателя", # 11    
    "Имя",                      # 12
    "Предметы",                 # 13
    "Всего часов",              # 14
    "Имя",                      # 15
    "Имя",                      # 15
    "Предметы (имя : часы : группа;)", # 16 
    "Всего часов",              # 17
    "Редактировать выбранное",  # 18
    "Удалить выбранное",        # 19
    "Имя",                      # 20
    "Размер",                   # 21
    "Имя",                      # 22
    "Размер",                   # 23
    "Редактировать выбранное",  # 24
    "Удалить выбранное",        # 25
    "Имя",                      # 26
    "Часы",                     # 27
    "Группа",                   # 28
    "Имя",                      # 29
    "Часов/нед",                # 30
    "Группа",                   # 31
    "Редактировать выбранное",  # 32
    "Удалить выбранное",        # 33
    "Выберите день:",           # 34
    "Печать в PDF",             # 35
    "Выберите группу:",         # 36
    "Очистить",                 # 37    
    "Автозаполнение для группы", # 38
    "Сохранить расписание группы", # 39
    "Печать в PDF",             # 40
    "Выберите преподавателя:",  # 41
    "Печать в PDF",             # 42
    "Please select a group!",  # 43  BUG
    "Инфо: Для этой группы не определены предметы",       # 44 messagebox.showinfo when group has no subjects
    "Предупреждение: Некоторые предметы не могут быть полностью запланированы", # 45 warning for incomplete autofill
    "Ошибка: Не удалось полностью запланировать после максимального количества попыток", # 46 error after MAX_ATTEMPTS
    "Инфо: Попытка автозаполнения успешна",             #       47 optional info after successful fill
    "Заполнитель для будущих сообщений",               # 48 reserved for future localization
    
    # buttons_functions.py STARTS HERE
    "Создание резервной копии данных...",                # 49
    "Ошибка: Папка DATA_DIR не найдена:",                # 50
    "Резервная копия успешно создана в:",                # 51
    "Ошибка при сохранении данных:",                     # 52
    "Пересоздать расписание",                            # 53
    "Удалить и пересоздать последнее расписание?",        # 54
    "Расписание успешно пересоздано.",                   # 55
    "Ошибка: Нет активного окна для скриншота.",          # 56
    "PDF сохранён (альбомная ориентация):",               # 57
    # START OF popups.py file
     "Добавить преподавателя",                  # 58
    "Имя",                                    # 59
    "Доступные предметы",                      # 60
    "Часы в неделю",                           # 61
    "Группа (необязательно)",                  # 62
    "Добавить >>",                             # 63
    "<< Удалить",                              # 64
    "Выбранные предметы (название:часы:группа)", # 65
    "Добавить",                                # 66
    "Ошибка",                                  # 67
    "Выберите предмет для добавления",          # 68
    "Количество часов должно быть целым числом",# 69
    "Информация",                              # 70
    "Предмет уже добавлен",                    # 71
    "Требуется имя",                           # 72
    "Добавить группу",                         # 73
    "Размер (целое число)",                    # 74
    "Размер должен быть целым числом",         # 75
    "Добавить предмет",                        # 76
    "Часы в неделю (целое число)",             # 77
    "Группа (обязательно)",                    # 78
    "Для предмета требуется группа",           # 79
    "Конец файла popups.py",                   # 80
    # START of ui_handlers.py
    "Редактировать преподавателя",       # 81
    "Выберите преподавателя для редактирования",  # 82
    "Преподаватель не найден",           # 83
    "Имя",                               # 84
    "Доступные предметы",                # 85
    "Часы в неделю",                      # 86
    "Предмет уже добавлен",              # 87
    "Выбранные предметы (название:часы:группа)", # 88
    "Доступность (день:начало-конец)",   # 89
    "Начало/Конец должны быть числами",  # 90
    "Выберите день",                      # 91
    "Добавить интервал",                  # 92
    "Удалить интервал",                   # 93
    "Сохранить",                          # 94
    "Ошибка",                             # 95
    "Информация",                         # 96
    "Подтвердить",                        # 97
    "Удалить преподавателя '{name}'?",    # 98
    "Выберите преподавателя для удаления", # 99
    "Добавить >>",                         # 100
    "<< Удалить" ,                         # 101
    "Общая конфигурация",                # 102 BUG
    # General Configuration tab texts (additional)
    "Заголовок приложения:",         # 103
    "Размер окна (ШxВ):",           # 104
    "Язык интерфейса:",             # 105
    "Направление автозаполнения:",  # 106
    "Макс. попыток автозаполнения:",# 107
    "Количество уроков:",           # 108
    "Временные слоты:",             # 109
    "Урок",                         # 110
    "Временной интервал",           # 111
    "L:",                            # 112
    "T:",                            # 113
    "Редактировать дни недели:",    # 114
    "Если вы редактируете дни недели — все данные придется ввести заново! Используйте клавиатуру, по одному дню на строку.", # 115
    "Макс подряд уроков:",          # 116
    "Макс уроков в день:",          # 117
    "Сохранить",                    # 118
    "Загрузить последнее сохранение",# 119
    "Сбросить к значениям по умолчанию", # 120
    'Загрузить',                     # 121
    'Сохранить как',                  # 122
    "Изменения вступят в силу только после полного перезапуска приложения.", # 123
    "Выбранная папка не содержит необходимых файлов:",   # 124
    "Вы уверены, что хотите загрузить последнюю сохраненную конфигурацию? Приложение перезапустится и все несохраненные изменения будут потеряны.",   # 125 
    "Ошибка во время загрузки",        # 126
    "Переместить вверх ↑",             # 127
    "Переместить вниз ↓",              # 128
    "Доступные уроки: (начало : конец)", # 129
    "ДЕНЬ",                        # 130
    "ЧАСЫ ДОСТУПНОСТИ",            # 131
    "НЕДЕЛЬНЫЕ ЧАСЫ УЧИТЕЛЯ",      # 132
    "Время начала (HH:MM)",        # 133
    "Время окончания (HH:MM)",     # 134
    "Добавить урок",               # 135
    "Добавить уроки/слоты времени",      # 136
    "Добавить дневные часы",       # 137
    "Сохранить изменения",         # 138
    "УРОКИ",                       # 139
    "СЛОТЫ ВРЕМЕНИ",               # 140
    "Очистить расписания",         # 141
    "Удалить всё",                 # 142
    "Удалить все расписания? Это удалит все созданные расписания, но сохранит Учителей, Группы и Предметы.", # 143
    "Удалить ВСЕ данные? Это удалит Учителей, Группы, Предметы и Расписания. Всё будет очищено!", # 144
    "Расписания успешно очищены.", # 145
    "Все данные успешно очищены.", # 146
    "Экспорт в Excel",             # 147
    "Загрузить из Excel",          # 148
    "Редактировать предмет",       # 149
    "Часов в неделю (число)",      # 150
    "Группа (обязательно)",        # 151
    "Выберите предмет для удаления", # 152
    "Подтверждение",               # 153
    "Удалить предмет",             # 154
    "Внимание! Этот предмет уже назначен:",  # 155
    "Это допустимо только если предмет разделен на подгруппы.",  # 156
    "Внимание",                    # 157
    "Назначено/Доступно",          # 158
    "Время прихода / Время ухода",    # 159
    "Всего часов на группу",     # 160
    # New translations for previously hardcoded messages
    "Выберите группу для сохранения", # 161
    "Сохранено",                   # 162
    "Расписание группы {group_name} сохранено",  # 163
    "Выберите учителя для сохранения", # 164
    "Расписание учителя {teacher_name} сохранено",  # 165
    "Выберите группу для редактирования", # 166
    "Группа не найдена",           # 167
    "Выберите группу для удаления", # 168
    "Удалить группу '{name}'?",   # 169
    "Выберите предмет для редактирования", # 170
    "Предмет не найден",           # 171
    "Выберите учителя для перемещения", # 172
    "Выберите группу для перемещения", # 173
    "Выберите предмет для перемещения", # 174
    "Пожалуйста, выберите время начала и окончания", # 175
    "Время начала должно быть раньше времени окончания", # 176
    "Неверный формат времени",     # 177
    "Пожалуйста, введите время прихода/ухода", # 178
    "Уроки не найдены в этом диапазоне времени. Проверьте время.", # 179
    "Библиотека openpyxl не установлена. Пожалуйста, установите:\npip install openpyxl", # 180
    "Успех",                       # 181
    "Расписания успешно экспортированы в:\n{file_path}", # 182
    "Не удалось экспортировать в Excel:\n{error}", # 183
    "Импортировано из Excel:\n{items}", # 184
    "Данные не найдены в файле Excel", # 185
    "Не удалось загрузить из Excel:\n{error}", # 186
    "Конфигурация",                # 187
    "Конфигурация успешно сохранена.", # 188
    "Не удалось сохранить consts.py (см. консоль).", # 189
    "Перезагружено из consts.py",  # 190
    "Сброс к настройкам по умолчанию source_consts.py.", # 191
    "source_consts.py не найден.", # 192
    "Не найдены ни consts.py, ни source_consts.py.", # 193
    "Ошибка удаления schedules.json: {error}", # 194
    "Ошибка удаления {filename}: {error}", # 195
    "Комментарий",                # 196
    "Файлы Excel",                # 197
    "Все файлы",                  # 198
    "Вы уверены, что хотите сохранить конфигурацию? Это применит изменения.",  # 199
    "Вы уверены, что хотите сбросить к настройкам по умолчанию? Все текущие изменения будут потеряны!",  # 200
]









LANGUAGES_DIC = {"English":ENGLISH, "Hebrew":HEBREW, "Russian":RUSSIAN}
GUI_TEXT = LANGUAGES_DIC[GUI_LANGUAGE]
# Multilingual support for School Scheduler
# Index-based translation system

# English translations (indices 0-199+)
GUI_TEXT = [
    "Add Teacher",                      # 0
    "Add Group",                        # 1


# Favorites & Weekdays / Time-slot related GUI texts (English base + placeholders)
    "Add Subject",                      # 2
    "Teachers",                         # 3
    "Groups",                           # 4
    "Subjects",                         # 5
    "Day View",                         # 6
    "Group Scheduler",                  # 7
    "Teacher Scheduler",                # 8
    "General Configuration",            # 9
    "Name",                             # 10
    "Subject",                          # 11

# Placeholder Hebrew translations for the added texts
    "Hours",                            # 12
    "Group",                            # 13
    "Teachers Weekly Hours",            # 14
    "Availability",                     # 15
    "Edit Selected",                    # 16
    "Delete Selected",                  # 17
    "Move Up ↑",                        # 18
    "Move Down ↓",                      # 19
    "Select a teacher to edit",         # 20
    "Select a group to edit",           # 21

# Placeholder Russian translations for the added texts
    "Select a subject to edit",         # 22
    "Are you sure you want to delete?", # 23
    "Confirm",                          # 24
    "Cancel",                           # 25
    "Save",                             # 26
    "Close",                            # 27
    "Teacher Name",                     # 28
    "Group Name",                       # 29
    "Subject Name",                     # 30
    "Hours Per Week",                   # 31
    "Select group:",                    # 32
    "Select teacher:",                  # 33
    "Autofill",                         # 34
    "Clear",                            # 35
    "Print to PDF",                     # 36
    "Monday",                           # 37
    "Tuesday",                          # 38
    "Wednesday",                        # 39
    "Thursday",                         # 40
    "Friday",                           # 41
    "Saturday",                         # 42
    "Sunday",                           # 43
    "Lesson",                           # 44
    "Time Range",                       # 45
    "Schedule created successfully",    # 46
    "Errors occurred:",                 # 47
    "Rebuild the schedule? This will delete the current schedule and create a new one.", # 48
    "Delete all schedules? This will remove all generated schedules but keep Teachers, Groups, and Subjects.", # 49
    "Are you sure you want to save the configuration? This will apply the changes.", # 50
    "Configuration saved successfully", # 51
    "GUI Language",                     # 52
    "Application Name",                 # 53
    "Application Size",                 # 54
    "Autofill Direction",               # 55
    "Max Autofill Retries",             # 56
    "Max Sequence Lessons",             # 57
    "Max Per Day",                      # 58
    "Number of Lessons",                # 59
    "Weekdays",                         # 60
    "English",                          # 61
    "Hebrew",                           # 62
    "Russian",                          # 63
    "Forward",                          # 64
    "Backward",                         # 65
    "Random",                           # 66
    "Import from Excel",                # 67
    "Export to Excel",                  # 68
    "Export to PDF",                    # 69
    "Clear All Schedules",              # 70
    "Refresh",                          # 71
    "Help",                             # 72
    "About",                            # 73
    "Settings",                         # 74
        "New Entry",                       # 12
    "Exit",                             # 75
    "File",                             # 76
    "Edit",                             # 77
    "View",                             # 78
    "Tools",                            # 79
    "Language",                         # 80
    "Theme",                            # 81
    "Light",                            # 82
    "Dark",                             # 83
    "Auto",                             # 84
    "Search",                           # 85
    "Filter",                           # 86
    "Sort",                             # 87
    "Ascending",                        # 88
    "Descending",                       # 89
    "Add",                              # 90
    "Remove",                           # 91
    "Update",                           # 92
    "Duplicate",                        # 93
    "Copy",                             # 94
    "Paste",                            # 95
    "Cut",                              # 96
    "Undo",                             # 97
    "Redo",                             # 98
    "Select All",                       # 99
    "Deselect All",                     # 100
    "Assigned/Available",               # 101
    "No teacher found for",             # 102
    "Could not place all hours for",    # 103
    "placed",                           # 104
    "Check In",                         # 105
    "Check Out",                        # 106
    "Apply",                            # 107
    "Reset",                            # 108
    "Default",                          # 109
    "Custom",                           # 110
    "Yes",                              # 111
    "No",                               # 112
    "OK",                               # 113
    "Error",                            # 114
    "Warning",                          # 115
    "Info",                             # 116
    "Success",                          # 117
    "Loading...",                       # 118
    "Please wait...",                   # 119
    "Processing...",                    # 120
    "Completed",                        # 121
    "Failed",                           # 122
    "Pending",                          # 123
    "Active",                           # 124
    "Inactive",                         # 125
    "Enabled",                          # 126
    "Disabled",                         # 127
    "Required field",                   # 128
    "Invalid input",                    # 129
    "Value too large",                  # 130
    "Value too small",                  # 131
    "Invalid format",                   # 132
    "Already exists",                   # 133
    "Not found",                        # 134
    "Access denied",                    # 135
    "Operation cancelled",              # 136
    "Operation completed",              # 137
    "Saving...",                        # 138
    "Saved",                            # 139
    "Not saved",                        # 140
    "Changes detected",                 # 141
    "No changes",                       # 142
    "Discard changes?",                 # 143
    "Export completed",                 # 144
    "Import completed",                 # 145
    "Export failed",                    # 146
    "Import failed",                    # 147
    "Select file",                      # 148
    "Upload",                           # 149
    "Download",                         # 150
    "Preview",                          # 151
    "Print",                            # 152
    "Page",                             # 153
    "of",                               # 154
    "First",                            # 155
    "Last",                             # 156
    "Next",                             # 157
    "Previous",                         # 158
    "Show",                             # 159
    "Hide",                             # 160
    "Expand",                           # 161
    "Collapse",                         # 162
    "Open",                             # 163
    "Close All",                        # 164
    "Refresh All",                      # 165
    "Clear All",                        # 166
    "Delete All",                       # 167
    "Export All",                       # 168
    "Import All",                       # 169
    "Select Date",                      # 170
    "Today",                            # 171
    "Yesterday",                        # 172
    "Tomorrow",                         # 173
    "This Week",                        # 174
    "Last Week",                        # 175
    "Next Week",                        # 176
    "This Month",                       # 177
    "Last Month",                       # 178
    "Next Month",                       # 179
    "This Year",                        # 180
    "Last Year",                        # 181
    "Next Year",                        # 182
    "Custom Range",                     # 183
    "Start Date",                       # 184
    "End Date",                         # 185
    "Start Time",                       # 186
    "End Time",                         # 187
    "Duration",                         # 188
    "Total",                            # 189
    "Average",                          # 190
    "Minimum",                          # 191
    "Maximum",                          # 192
    "Count",                            # 193
    "Sum",                              # 194
    "Percentage",                       # 195
    "Status",                           # 196
    "Type",                             # 197
    "Category",                         # 198
    "Priority",                         # 199
    "Description",                      # 200
]

# Additional UI messages added for signup/login/file dialogs
GUI_TEXT.extend([
    "Passwords do not match",
    "Account created successfully! Redirecting to login...",
    "Signup failed",
    "An error occurred. Please try again.",
    "Login failed",
    "Please select a file",
    "Logout failed",
    "Please select a subject from available subjects",
    "This subject is already added",
    "Teacher name is required",
    "Choose day, start and end",
    "All existing data will be erased. An Export to Excel will run first. Continue?",
    "Start must be before end",
    "Choose day and enter check in/out",
    "Times do not match any lessons",
    "Select a teacher to delete",
    "Select a teacher to move",
    "Select a group to edit"
])

# General / Time-slot additions (appended to avoid changing existing indices)
GUI_TEXT.extend([
    "General Configurations",
    "Add New Time Slot",
    "Lesson Number"
])

# Hebrew translations (עברית)
GUI_TEXT_HE = [
    "הוסף מורה",                        # 0
    "הוסף קבוצה",                       # 1
    "הוסף מקצוע",                       # 2
    "מורים",                            # 3
    "קבוצות",                           # 4
    "מקצועות",                          # 5
    "תצוגת יום",                        # 6
    "מתזמן קבוצות",                     # 7
    "מתזמן מורים",                      # 8
    "הגדרות כלליות",                    # 9
    "שם",                               # 10
    "מקצוע",                            # 11
    "שעות",                             # 12
    "קבוצה",                            # 13
    "שעות שבועיות של מורים",            # 14
    "זמינות",                           # 15
    "ערוך נבחר",                        # 16
    "מחק נבחר",                         # 17
    "העבר למעלה ↑",                     # 18
    "העבר למטה ↓",                      # 19
    "בחר מורה לעריכה",                  # 20
    "בחר קבוצה לעריכה",                 # 21
    "בחר מקצוע לעריכה",                 # 22
    "האם אתה בטוח שברצונך למחוק?",      # 23
    "אישור",                            # 24
    "ביטול",                            # 25
    "שמור",                             # 26
    "סגור",                             # 27
    "שם מורה",                          # 28
    "שם קבוצה",                         # 29
    "שם מקצוע",                         # 30
    "שעות בשבוע",                       # 31
    "בחר קבוצה:",                       # 32
    "בחר מורה:",                        # 33
    "מילוי אוטומטי",                    # 34
    "נקה",                              # 35
    "הדפס ל-PDF",                       # 36
    "יום שני",                          # 37
    "יום שלישי",                        # 38
    "יום רביעי",                        # 39
    "יום חמישי",                        # 40
    "יום שישי",                         # 41
    "יום שבת",                          # 42
    "יום ראשון",                        # 43
    "שיעור",                            # 44
    "טווח זמן",                         # 45
    "מערכת שעות נוצרה בהצלחה",          # 46
    "אירעו שגיאות:",                    # 47
    "לבנות מחדש את המערכת? פעולה זו תמחק את המערכת הנוכחית ותיצור חדשה.", # 48
    "למחוק את כל המערכות? פעולה זו תסיר את כל המערכות שנוצרו אך תשאיר מורים, קבוצות ומקצועות.", # 49
    "האם אתה בטוח שברצונך לשמור את ההגדרות? פעולה זו תחיל את השינויים.", # 50
    "ההגדרות נשמרו בהצלחה",            # 51
    "שפת ממשק",                         # 52
    "שם יישום",                         # 53
    "גודל יישום",                       # 54
    "כיוון מילוי אוטומטי",              # 55
    "מקסימום נסיונות מילוי",            # 56
    "מקסימום שיעורים רצופים",           # 57
    "מקסימום ליום",                     # 58
    "מספר שיעורים",                     # 59
    "ימי שבוע",                         # 60
    "אנגלית",                           # 61
    "עברית",                            # 62
    "רוסית",                            # 63
    "קדימה",                            # 64
    "אחורה",                            # 65
    "אקראי",                            # 66
    "ייבא מאקסל",                       # 67
    "ייצא לאקסל",                       # 68
    "ייצא ל-PDF",                       # 69
    "נקה את כל המערכות",                # 70
    "רענן",                             # 71
    "עזרה",                             # 72
    "אודות",                            # 73
    "הגדרות",                           # 74
    "יציאה",                            # 75
    "קובץ",                             # 76
    "עריכה",                            # 77
    "תצוגה",                            # 78
    "כלים",                             # 79
    "שפה",                              # 80
    "ערכת נושא",                        # 81
    "בהיר",                             # 82
    "כהה",                              # 83
    "אוטומטי",                          # 84
    "חיפוש",                            # 85
    "סינון",                            # 86
    "מיון",                             # 87
    "עולה",                             # 88
    "יורד",                             # 89
    "הוסף",                             # 90
    "הסר",                              # 91
    "עדכן",                             # 92
    "שכפל",                             # 93
    "העתק",                             # 94
    "הדבק",                             # 95
    "גזור",                             # 96
    "בטל",                              # 97
    "בצע שוב",                          # 98
    "בחר הכל",                          # 99
    "בטל בחירה",                        # 100
    "משוייך/זמין",                      # 101
    "לא נמצא מורה עבור",                # 102
    "לא ניתן למקם את כל השעות עבור",     # 103
    "ממוקם",                            # 104
    "כניסה",                            # 105
    "יציאה",                            # 106
    "החל",                              # 107
    "אפס",                              # 108
    "ברירת מחדל",                       # 109
    "מותאם אישית",                      # 110
    "כן",                               # 111
    "לא",                               # 112
    "אישור",                            # 113
    "שגיאה",                            # 114
    "אזהרה",                            # 115
    "מידע",                             # 116
    "הצלחה",                            # 117
    "טוען...",                          # 118
    "אנא המתן...",                      # 119
    "מעבד...",                          # 120
    "הושלם",                            # 121
    "נכשל",                             # 122
    "ממתין",                            # 123
    "פעיל",                             # 124
    "לא פעיל",                          # 125
    "מופעל",                            # 126
    "מושבת",                            # 127
    "שדה חובה",                         # 128
    "קלט לא חוקי",                      # 129
    "ערך גדול מדי",                     # 130
    "ערך קטן מדי",                      # 131
    "פורמט לא חוקי",                    # 132
    "כבר קיים",                         # 133
    "לא נמצא",                          # 134
    "גישה נדחתה",                       # 135
    "הפעולה בוטלה",                     # 136
    "הפעולה הושלמה",                    # 137
    "שומר...",                          # 138
    "נשמר",                             # 139
    "לא נשמר",                          # 140
    "זוהו שינויים",                     # 141
    "אין שינויים",                      # 142
    "להתעלם משינויים?",                 # 143
    "הייצוא הושלם",                     # 144
    "הייבוא הושלם",                     # 145
    "הייצוא נכשל",                      # 146
    "הייבוא נכשל",                      # 147
    "בחר קובץ",                         # 148
    "העלה",                             # 149
    "הורד",                             # 150
    "תצוגה מקדימה",                     # 151
    "הדפס",                             # 152
    "עמוד",                             # 153
    "מתוך",                             # 154
    "ראשון",                            # 155
    "אחרון",                            # 156
    "הבא",                              # 157
    "הקודם",                            # 158
    "הצג",                              # 159
    "הסתר",                             # 160
]

# Hebrew translations for additional messages
GUI_TEXT_HE.extend([
    "הסיסמאות אינן תואמות",
    "החשבון נוצר בהצלחה! נעבור לדף ההתחברות...",
    "ההרשמה נכשלה",
    "אירעה שגיאה. נסה שוב.",
    "ההתחברות נכשלה",
    "אנא בחר קובץ",
    "יציאה נכשלה",
    "אנא בחר מקצוע מהרשימה הזמינה",
    "מקצוע זה נוסף כבר",
    "שם המורה נדרש",
    "בחר יום, התחלה וסיום",
    "ההתחלה חייבת להיות לפני הסיום",
    "בחר יום והזן שעות כניסה/יציאה",
    "הזמנים אינם תואמים לשיעורים כלשהם",
    "בחר מורה למחיקה",
    "בחר מורה להעברה",
    "All existing data will be erased. An Export to Excel will run first. Continue?",
    "בחר קבוצה לעריכה"
])

# Russian translations (Русский)
GUI_TEXT_RU = [
    "Добавить учителя",                 # 0
    "Добавить группу",                  # 1
    "Добавить предмет",                 # 2
    "Учителя",                          # 3
    "Группы",                           # 4
    "Предметы",                         # 5
    "Просмотр дня",                     # 6
    "Расписание групп",                 # 7
    "Расписание учителей",              # 8
    "Общие настройки",                  # 9
    "Имя",                              # 10
    "Предмет",                          # 11
    "Часы",                             # 12
    "Группа",                           # 13
    "Недельные часы учителей",          # 14
    "Доступность",                      # 15
    "Редактировать выбранное",          # 16
    "Удалить выбранное",                # 17
    "Переместить вверх ↑",              # 18
    "Переместить вниз ↓",               # 19
    "Выберите учителя для редактирования", # 20
    "Выберите группу для редактирования", # 21
    "Выберите предмет для редактирования", # 22
    "Вы уверены, что хотите удалить?",  # 23
    "Подтвердить",                      # 24
    "Отмена",                           # 25
    "Сохранить",                        # 26
    "Закрыть",                          # 27
    "Имя учителя",                      # 28
    "Название группы",                  # 29
    "Название предмета",                # 30
    "Часов в неделю",                   # 31
    "Выберите группу:",                 # 32
    "Выберите учителя:",                # 33
    "Автозаполнение",                   # 34
    "Очистить",                         # 35
    "Печать в PDF",                     # 36
    "Понедельник",                      # 37
    "Вторник",                          # 38
    "Среда",                            # 39
    "Четверг",                          # 40
    "Пятница",                          # 41
    "Суббота",                          # 42
    "Воскресенье",                      # 43
    "Урок",                             # 44
    "Временной диапазон",               # 45
    "Расписание успешно создано",       # 46
    "Произошли ошибки:",                # 47
    "Перестроить расписание? Это удалит текущее расписание и создаст новое.", # 48
    "Удалить все расписания? Это удалит все созданные расписания, но сохранит учителей, группы и предметы.", # 49
    "Вы уверены, что хотите сохранить конфигурацию? Это применит изменения.", # 50
    "Конфигурация успешно сохранена",   # 51
    "Язык интерфейса",                  # 52
    "Название приложения",              # 53
    "Размер приложения",                # 54
    "Направление автозаполнения",       # 55
    "Максимум попыток автозаполнения",  # 56
    "Максимум уроков подряд",           # 57
    "Максимум в день",                  # 58
    "Количество уроков",                # 59
    "Дни недели",                       # 60
    "Английский",                       # 61
    "Иврит",                            # 62
    "Русский",                          # 63
    "Вперёд",                           # 64
    "Назад",                            # 65
    "Случайно",                         # 66
    "Импорт из Excel",                  # 67
    "Экспорт в Excel",                  # 68
    "Экспорт в PDF",                    # 69
    "Очистить все расписания",          # 70
    "Обновить",                         # 71
    "Помощь",                           # 72
    "О программе",                      # 73
    "Настройки",                        # 74
    "Выход",                            # 75
    "Файл",                             # 76
    "Редактировать",                    # 77
    "Вид",                              # 78
    "Инструменты",                      # 79
    "Язык",                             # 80
    "Тема",                             # 81
    "Светлая",                          # 82
    "Тёмная",                           # 83
    "Авто",                             # 84
    "Поиск",                            # 85
    "Фильтр",                           # 86
    "Сортировка",                       # 87
    "По возрастанию",                   # 88
    "По убыванию",                      # 89
    "Добавить",                         # 90
    "Удалить",                          # 91
    "Обновить",                         # 92
    "Дублировать",                      # 93
    "Копировать",                       # 94
    "Вставить",                         # 95
    "Вырезать",                         # 96
    "Отменить",                         # 97
    "Повторить",                        # 98
    "Выбрать всё",                      # 99
    "Отменить выбор",                   # 100
    "Назначено/Доступно",               # 101
    "Не найден учитель для",            # 102
    "Не удалось разместить все часы для", # 103
    "размещено",                        # 104
    "Время прихода",                    # 105
    "Время ухода",                      # 106
    "Применить",                        # 107
    "Сбросить",                         # 108
    "По умолчанию",                     # 109
    "Пользовательский",                 # 110
    "Да",                               # 111
    "Нет",                              # 112
    "ОК",                               # 113
    "Ошибка",                           # 114
    "Предупреждение",                   # 115
    "Информация",                       # 116
    "Успех",                            # 117
    "Загрузка...",                      # 118
    "Пожалуйста, подождите...",         # 119
    "Обработка...",                     # 120
    "Завершено",                        # 121
    "Не удалось",                       # 122
    "В ожидании",                       # 123
    "Активный",                         # 124
    "Неактивный",                       # 125
    "Включено",                         # 126
    "Отключено",                        # 127
    "Обязательное поле",                # 128
    "Неверный ввод",                    # 129
    "Значение слишком большое",         # 130
    "Значение слишком маленькое",       # 131
    "Неверный формат",                  # 132
    "Уже существует",                   # 133
    "Не найдено",                       # 134
    "Доступ запрещён",                  # 135
    "Операция отменена",                # 136
    "Операция завершена",               # 137
    "Сохранение...",                    # 138
    "Сохранено",                        # 139
    "Не сохранено",                     # 140
    "Обнаружены изменения",             # 141
    "Нет изменений",                    # 142
    "Отменить изменения?",              # 143
    "Экспорт завершён",                 # 144
    "Импорт завершён",                  # 145
    "Экспорт не удался",                # 146
    "Импорт не удался",                 # 147
    "Выберите файл",                    # 148
    "Загрузить",                        # 149
    "Скачать",                          # 150
    "Предпросмотр",                     # 151
    "Печать",                           # 152
    "Страница",                         # 153
    "из",                               # 154
    "Первая",                           # 155
    "Последняя",                        # 156
    "Следующая",                        # 157
    "Предыдущая",                       # 158
    "Показать",                         # 159
    "Скрыть",                           # 160
]

# Russian translations for additional messages
GUI_TEXT_RU.extend([
    "Пароли не совпадают",
    "Аккаунт успешно создан! Перенаправление на страницу входа...",
    "Ошибка регистрации",
    "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
    "Ошибка входа",
    "Пожалуйста, выберите файл",
    "Выход не удался",
    "Пожалуйста, выберите предмет из доступных",
    "Этот предмет уже добавлен",
    "Требуется имя учителя",
    "Выберите день, начало и конец",
    "Начало должно быть раньше конца",
    "Выберите день и укажите время прихода/ухода",
    "Время не соответствует ни одному уроку",
    "Выберите учителя для удаления",
    "Выберите учителя для перемещения",
    "Выберите группу для редактирования"
])

# More UI strings used in auth pages and headers
GUI_TEXT.extend([
    "Create your account",
    "Login to your account",
    "First Name",
    "Last Name",
    "Email (optional)",
    "Username",
    "Password",
    "Confirm Password",
    "Sign Up",
    "Login",
    "Already have an account? Login",
    "Don't have an account? Sign Up",
    "Show Alert Close"
    ,
    "Clear All Data",
    "Rebuild All",
    "Logout",
    "Day Scheduler",
    "Select Weekday"
])

GUI_TEXT_HE.extend([
    "צור את החשבון שלך",
    "התחברות לחשבון",
    "שם פרטי",
    "שם משפחה",
    "אימייל (אופציונלי)",
    "שם משתמש",
    "סיסמה",
    "אשר סיסמה",
    "הירשם",
    "התחבר",
    "כבר יש חשבון? התחבר",
    "אין חשבון? הירשם",
    "סגור הודעה"
    ,
    "נקה כל הנתונים",
    "בנה מערכות מחדש",
    "התנתק",
    "מתזמן יום",
    "בחר יום בשבוע"
])

GUI_TEXT_RU.extend([
    "Создайте аккаунт",
    "Войдите в свой аккаунт",
    "Имя",
    "Фамилия",
    "Email (необязательно)",
    "Имя пользователя",
    "Пароль",
    "Подтвердите пароль",
    "Регистрация",
    "Вход",
    "Уже есть аккаунт? Войти",
    "Нет аккаунта? Зарегистрироваться",
    "Закрыть сообщение"
    ,
    "Очистить все данные",
    "Пересобрать всё",
    "Выйти",
    "Просмотр дня",
    "Выберите день недели"
])

# Additional UI keys used in Edit Teacher modal and availability editor
GUI_TEXT.extend([
    "Available Subjects",
    "Selected Subjects (name:hours:group)",
    "Interactive Availability Editor",
    "Add Time Slots",
    "Check-in",
    "Check-out",
    "Add Real Hours",
    "Day",
    "Lessons",
    "Time Slots",
    "Real Hours",
    "Priority Order:",
    "Teacher's Weekly Hours",
    "Time Slots (SECONDARY)",
    "Lessons (TERTIARY)",
    "Loading..."
])

GUI_TEXT_HE.extend([
    "מקצועות זמינים",
    "מקצועות נבחרים (שם:שעות:קבוצה)",
    "עורך זמינות אינטראקטיבי",
    "הוסף טווחי זמן",
    "כניסה",
    "יציאה",
    "הוסף שעות אמיתיות",
    "יום",
    "שיעורים",
    "טווחי זמן",
    "שעות אמיתיות",
    "סדר עדיפויות:",
    "שעות שבועיות של המורה",
    "טווחי זמן (משני)",
    "שיעורים (שלישוני)",
    "טוען..."
])

GUI_TEXT_RU.extend([
    "Доступные предметы",
    "Выбранные предметы (имя:часы:группа)",
    "Интерактивный редактор доступности",
    "Добавить временные слоты",
    "Время входа",
    "Время выхода",
    "Добавить реальные часы",
    "День",
    "Уроки",
    "Временные слоты",
    "Реальные часы",
    "Порядок приоритетов:",
    "Недельные часы преподавателя",
    "Временные слоты (ВТОРИЧНЫЕ)",
    "Уроки (ТЕРЦИЧНЫЕ)",
    "Загрузка..."
])

GUI_TEXT.extend(["Edit Teacher"])
GUI_TEXT_HE.extend(["ערוך מורה"])
GUI_TEXT_RU.extend(["Редактировать учителя"])

# Additional small UI keys used in JS
GUI_TEXT.extend([
    "Click to set time",
    "Click to edit",
    "Delete slot"
])

GUI_TEXT_HE.extend([
    "לחץ כדי להגדיר זמן",
    "לחץ כדי לערוך",
    "מחק משבצת"
])

GUI_TEXT_RU.extend([
    "Нажмите, чтобы установить время",
    "Нажмите, чтобы редактировать",
    "Удалить слот"
])

GUI_TEXT.extend([
    "All",
    "Edit Group",
    "Edit Subject",
    "Delete"
])

GUI_TEXT_HE.extend([
    "הכל",
    "ערוך קבוצה",
    "ערוך מקצוע",
    "מחק"
])

GUI_TEXT_RU.extend([
    "Все",
    "Редактировать группу",
    "Редактировать предмет",
    "Удалить"
])

# Signup / auth small messages
GUI_TEXT.extend([
    "Sign Up",
    "School Scheduler",
    "Username must be at least 3 characters and contain only letters, numbers, and underscores",
    "Password must be at least 6 characters"
])

GUI_TEXT_HE.extend([
    "הצטרף",
    "מתזמן בית ספר",
    "שם המשתמש חייב להכיל לפחות 3 תווים ולכלול אותיות, ספרות וקו תחתון בלבד",
    "הסיסמה חייבת להכיל לפחות 6 תווים"
])

GUI_TEXT_RU.extend([
    "Зарегистрироваться",
    "School Scheduler",
    "Имя пользователя должно содержать не менее 3 символов и содержать только буквы, цифры и подчёркивания",
    "Пароль должен содержать не менее 6 символов"
])
# Final sanity fixes (run after all extends) to correct any remaining index shifts.
_final_fixes = {
        217: ("בחר מורה להעברה", "Выберите учителя для перемещения"),
        222: ("שם משפחה", "Фамилия"),
        261: ("הירשם", "Зарегистрироваться"),
        264: ("הסיסמה חייבת להכיל לפחות 6 תווים", "Пароль должен содержать не менее 6 символов"),
        268: ("בנה מחדש הכול (מילוי אוטומטי)", "Перестроить всё (Автозаполнение)"),
        269: ("Reached max 10 favorites. Open 'Load from Favorites', remove entries, then retry.",
              "Достигнуто максимум 10 избранных. Откройте 'Загрузить из избранного', удалите записи, затем попробуйте ещё раз."),
        270: ("Maximum 10 favorites reached. Delete one before saving.", "Достигнуто максимум 10 избранных. Удалите один перед сохранением."),
        273: ("שמור למועדפים", "Сохранить в избранное"),
        281: ("שעות שבועיות של המורה", "Недельные часы преподавателя"),
        287: ("לחץ על כל טווח זמן בטבלה כדי לערוך אותו במקום", "Кликните по любому временному интервалу в таблице, чтобы отредактировать его на месте"),
        288: ("פורמט זמן: H:MM-H:MM או HH:MM-HH:MM (למשל, 9:15-10:00 או 09:15-10:00)",
              "Формат времени: H:MM-H:MM или HH:MM-HH:MM (например, 9:15-10:00 или 09:15-10:00)"),
        289: ("הקש Enter לשמירה, Escape לביטול העריכה במקום", "Нажмите Enter для сохранения, Escape для отмены редактирования на месте"),
        290: ("מספר הטווחים יסונכרן אוטומטית עם ההגדרה \"מספר שיעורים\"", "Количество слотов будет автоматически синхронизировано с настройкой \"Number of lessons\"")
    }

for idx, (he_val, ru_val) in _final_fixes.items():
    if 0 <= idx < len(GUI_TEXT_HE):
        GUI_TEXT_HE[idx] = he_val
    if 0 <= idx < len(GUI_TEXT_RU):
        GUI_TEXT_RU[idx] = ru_val


# Additional texts used in Rebuild modal
GUI_TEXT.extend([
    "Before rebuilding, please export your current data to Excel as a backup.",
    "I already exported",
    "Export now"
])

# Hebrew translations for the added texts
GUI_TEXT_HE.extend([
    "לפני ביצוע שחזור, נא לייצא את הנתונים הנוכחיים לאקסל כגיבוי.",
    "כבר ייצאתי",
    "ייצא עכשיו"
])

# Russian translations for the added texts
GUI_TEXT_RU.extend([
    "Перед перестроением, пожалуйста, экспортируйте текущие данные в Excel в качестве резервной копии.",
    "Я уже экспортировал",
    "Экспортировать сейчас"
])

# Add 'Rebuild All (Autofill)' to translations
GUI_TEXT.extend([
    "Rebuild All (Autofill)"
])

GUI_TEXT_HE.extend([
    "בנה מחדש הכול (מילוי אוטומטי)"
])

GUI_TEXT_RU.extend([
    "Перестроить всё (Автозаполнение)"
])


# Messages related to the Favorites feature (added so new UI/server texts have i18n entries)
GUI_TEXT.extend([
    "Maximum 10 favorites reached. Open \"Load from Favorites\", remove one or more entries, then try saving again. Opening the list now.",
    "Maximum 10 favorites reached. Delete one before saving."
])

# Placeholder Hebrew translations for the added Favorites texts
GUI_TEXT_HE.extend([
    "Maximum 10 favorites reached. Open \"Load from Favorites\", remove one or more entries, then try saving again. Opening the list now.",
    "Maximum 10 favorites reached. Delete one before saving."
])

# Placeholder Russian translations for the added Favorites texts
GUI_TEXT_RU.extend([
    "Maximum 10 favorites reached. Open \"Load from Favorites\", remove one or more entries, then try saving again. Opening the list now.",
    "Maximum 10 favorites reached. Delete one before saving."
])

# Favorites button labels
GUI_TEXT.extend([
    "Save to Favorites",
    "Load from Favorites"
])

# Add 'Saved to Favorites' and button labels
GUI_TEXT.extend([
    "Save to Favorites",
    "Load from Favorites",
    "Saved to Favorites"
])

# Hebrew translations for favorites labels
GUI_TEXT_HE.extend([
    "שמור למועדפים",
    "טען מהמועדפים",
    "נשמר במועדפים"
])

# Russian translations for favorites labels
GUI_TEXT_RU.extend([
    "Сохранить в избранное",
    "Загрузить из избранного",
    "Сохранено в избранное"
])

# Additional Favorites / Slot UI strings
GUI_TEXT.extend([
    "Rename",
    "Enter favorite name:",
    "OK",
    "Cancel",
    "Add Slot",
    "Choose a preset, then edit the comma-separated weekdays if needed"
])

# Rebuild priorities UI strings
GUI_TEXT.extend([
    "Set priorities for rebuild. Use Up/Down to change order. Press Run when ready.",
    "Groups Priority",
    "Subjects Priority",
    "Teachers Priority",
    "Days Priority",
    "Run"
])

# General / Time-slot UI strings
GUI_TEXT.extend([
    "General Configurations",
    "Add New Time Slot",
    "Lesson Number"
])

GUI_TEXT_HE.extend([
    "שנה שם",
    "הזן שם למועדף:",
    "אישור",
    "ביטול",
    "הוסף טווח",
    "בחר תבנית, ולאחר מכן ערוך את ימי השבוע המופרדים בפסיקים במידת הצורך"
])

GUI_TEXT_RU.extend([
    "Переименовать",
    "Введите имя избранного:",
    "ОК",
    "Отмена",
    "Добавить интервал",
    "Выберите пресет, затем при необходимости отредактируйте дни недели, разделённые запятыми"
])

# Add confirmation translation placeholder for Russian
GUI_TEXT_RU.extend([
    "All existing data will be erased. An Export to Excel will run first. Continue?"
])


# Time slots / lessons explanatory texts
GUI_TEXT.extend([
    "If provided, Time Slots and Lessons are calculated from this",
    "Used only if Weekly Hours is empty. Converted to lesson numbers"
])

GUI_TEXT_HE.extend([
    "אם הוזן, טווחי הזמן ומספר השיעורים יחושבו על פיו",
    "משמש רק אם שדה 'שעות שבועיות' ריק. יומר למספר שיעורים"
])

GUI_TEXT_RU.extend([
    "Если указано, временные слоты и количество уроков рассчитываются на его основе",
    "Используется только если поле 'Недельные часы' пусто. Преобразуется в номера уроков"
])

GUI_TEXT.extend([
    "Used only if both above are empty"
])

GUI_TEXT_HE.extend([
    "משמש רק אם שני השדות שלעיל ריקים"
])

GUI_TEXT_RU.extend([
    "Используется только если оба вышеуказанных поля пусты"
])

# Table column labels
GUI_TEXT.extend([
    "Total Required / Assigned",
    "Comments"
])

GUI_TEXT_HE.extend([
    "סה\"כ נדרש / מוקצה",
    "הערות"
])

GUI_TEXT_RU.extend([
    "Всего требуется / Назначено",
    "Комментарии"
])

# Priority labels (exact keys used in templates)
GUI_TEXT.extend([
    "Teacher's Weekly Hours",
    "Time Slots (SECONDARY)",
    "Lessons (TERTIARY)"
])

GUI_TEXT_HE.extend([
    "שעות שבועיות של המורה (PRIMARY)",
    "טווחי זמן (משני)",
    "שיעורים (שלישוני)"
])

GUI_TEXT_RU.extend([
    "Недельные часы преподавателя (PRIMARY)",
    "Временные интервалы (SECONDARY)",
    "Уроки (TERТИЧНЫЕ)"
])
# English translations (indices 0-199+)
GUI_TEXT = [
    "Add Teacher",                      # 0
    "Add Group",                        # 1


# Favorites & Weekdays / Time-slot related GUI texts (English base + placeholders)
    "Add Subject",                      # 2
    "Teachers",                         # 3
    "Groups",                           # 4
    "Subjects",                         # 5
    "Day View",                         # 6
    "Group Scheduler",                  # 7
    "Teacher Scheduler",                # 8
    "General Configuration",            # 9
    "Name",                             # 10
    "Subject",                          # 11

# Placeholder Hebrew translations for the added texts
    "Hours",                            # 12
    "Group",                            # 13
    "Teachers Weekly Hours",            # 14
    "Availability",                     # 15
    "Edit Selected",                    # 16
    "Delete Selected",                  # 17
    "Move Up ↑",                        # 18
    "Move Down ↓",                      # 19
    "Select a teacher to edit",         # 20
    "Select a group to edit",           # 21

# Placeholder Russian translations for the added texts
    "Select a subject to edit",         # 22
    "Are you sure you want to delete?", # 23
    "Confirm",                          # 24
    "Cancel",                           # 25
    "Save",                             # 26
    "Close",                            # 27
    "Teacher Name",                     # 28
    "Group Name",                       # 29
    "Subject Name",                     # 30
    "Hours Per Week",                   # 31
    "Select group:",                    # 32
    "Select teacher:",                  # 33
    "Autofill",                         # 34
    "Clear",                            # 35
    "Print to PDF",                     # 36
    "Monday",                           # 37
    "Tuesday",                          # 38
    "Wednesday",                        # 39
    "Thursday",                         # 40
    "Friday",                           # 41
    "Saturday",                         # 42
    "Sunday",                           # 43
    "Lesson",                           # 44
    "Time Range",                       # 45
    "Schedule created successfully",    # 46
    "Errors occurred:",                 # 47
    "Rebuild the schedule? This will delete the current schedule and create a new one.", # 48
    "Delete all schedules? This will remove all generated schedules but keep Teachers, Groups, and Subjects.", # 49
    "Are you sure you want to save the configuration? This will apply the changes.", # 50
    "Configuration saved successfully", # 51
    "GUI Language",                     # 52
    "Application Name",                 # 53
    "Application Size",                 # 54
    "Autofill Direction",               # 55
    "Max Autofill Retries",             # 56
    "Max Sequence Lessons",             # 57
    "Max Per Day",                      # 58
    "Number of Lessons",                # 59
    "Weekdays",                         # 60
    "English",                          # 61
    "Hebrew",                           # 62
    "Russian",                          # 63
    "Forward",                          # 64
    "Backward",                         # 65
    "Random",                           # 66
    "Import from Excel",                # 67
    "Export to Excel",                  # 68
    "Export to PDF",                    # 69
    "Clear All Schedules",              # 70
    "Refresh",                          # 71
    "Help",                             # 72
    "About",                            # 73
    "Settings",                         # 74
    "Exit",                             # 75
    "File",                             # 76
    "Edit",                             # 77
    "View",                             # 78
    "Tools",                            # 79
    "Language",                         # 80
    "Theme",                            # 81
    "Light",                            # 82
    "Dark",                             # 83
    "Auto",                             # 84
    "Search",                           # 85
    "Filter",                           # 86
    "Sort",                             # 87
    "Ascending",                        # 88
    "Descending",                       # 89
    "Add",                              # 90
    "Remove",                           # 91
    "Update",                           # 92
    "Duplicate",                        # 93
    "Copy",                             # 94
    "Paste",                            # 95
    "Cut",                              # 96
    "Undo",                             # 97
    "Redo",                             # 98
    "Select All",                       # 99
    "Deselect All",                     # 100
    "Assigned/Available",               # 101
    "No teacher found for",             # 102
    "Could not place all hours for",    # 103
    "placed",                           # 104
    "Check In",                         # 105
    "Check Out",                        # 106
    "Apply",                            # 107
    "Reset",                            # 108
    "Default",                          # 109
    "Custom",                           # 110
    "Yes",                              # 111
    "No",                               # 112
    "OK",                               # 113
    "Error",                            # 114
    "Warning",                          # 115
    "Info",                             # 116
    "Success",                          # 117
    "Loading...",                       # 118
    "Please wait...",                   # 119
    "Processing...",                    # 120
    "Completed",                        # 121
    "Failed",                           # 122
    "Pending",                          # 123
    "Active",                           # 124
    "Inactive",                         # 125
    "Enabled",                          # 126
    "Disabled",                         # 127
    "Required field",                   # 128
    "Invalid input",                    # 129
    "Value too large",                  # 130
    "Value too small",                  # 131
    "Invalid format",                   # 132
    "Already exists",                   # 133
    "Not found",                        # 134
    "Access denied",                    # 135
    "Operation cancelled",              # 136
    "Operation completed",              # 137
    "Saving...",                        # 138
    "Saved",                            # 139
    "Not saved",                        # 140
    "Changes detected",                 # 141
    "No changes",                       # 142
    "Discard changes?",                 # 143
    "Export completed",                 # 144
    "Import completed",                 # 145
    "Export failed",                    # 146
    "Import failed",                    # 147
    "Select file",                      # 148
    "Upload",                           # 149
    "Download",                         # 150
    "Preview",                          # 151
    "Print",                            # 152
    "Page",                             # 153
    "of",                               # 154
    "First",                            # 155
    "Last",                             # 156
    "Next",                             # 157
    "Previous",                         # 158
    "Show",                             # 159
    "Hide",                             # 160
    "Expand",                           # 161
    "Collapse",                         # 162
    "Open",                             # 163
    "Close All",                        # 164
    "Refresh All",                      # 165
    "Clear All",                        # 166
    "Delete All",                       # 167
    "Export All",                       # 168
    "Import All",                       # 169
    "Select Date",                      # 170
    "Today",                            # 171
    "Yesterday",                        # 172
    "Tomorrow",                         # 173
    "This Week",                        # 174
    "Last Week",                        # 175
    "Next Week",                        # 176
    "This Month",                       # 177
    "Last Month",                       # 178
    "Next Month",                       # 179
    "This Year",                        # 180
    "Last Year",                        # 181
    "Next Year",                        # 182
    "Custom Range",                     # 183
    "Start Date",                       # 184
    "End Date",                         # 185
    "Start Time",                       # 186
    "End Time",                         # 187
    "Duration",                         # 188
    "Total",                            # 189
    "Average",                          # 190
    "Minimum",                          # 191
    "Maximum",                          # 192
    "Count",                            # 193
    "Sum",                              # 194
    "Percentage",                       # 195
    "Status",                           # 196
    "Type",                             # 197
    "Category",                         # 198
    "Priority",                         # 199
    "Description",                      # 200
]

# Additional UI messages added for signup/login/file dialogs
GUI_TEXT.extend([
    "Passwords do not match",
    "Account created successfully! Redirecting to login...",
    "Signup failed",
    "An error occurred. Please try again.",
    "Login failed",
    "Please select a file",
    "Logout failed",
    "Please select a subject from available subjects",
    "This subject is already added",
    "Teacher name is required",
    "Choose day, start and end",
    "All existing data will be erased. An Export to Excel will run first. Continue?",
    "Start must be before end",
    "Choose day and enter check in/out",
    "Times do not match any lessons",
    "Select a teacher to delete",
    "Select a teacher to move",
    "Select a group to edit"
])

# Russian translations (Русский)
GUI_TEXT_RU.extend([
    "Пароли не совпадают",
    "Аккаунт успешно создан! Перенаправление на страницу входа...",
    "Ошибка регистрации",
    "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
    "Ошибка входа",
    "Пожалуйста, выберите файл",
    "Выход не удался",
    "Пожалуйста, выберите предмет из доступных",
    "Этот предмет уже добавлен",
    "Требуется имя учителя",
    "Выберите день, начало и конец",
    "Начало должно быть раньше конца",
    "Выберите день и укажите время прихода/ухода",
    "Время не соответствует ни одному уроку",
    "Выберите учителя для удаления",
    "Выберите учителя для перемещения",
    "Выберите группу для редактирования"
])

# Ensure Hebrew and Russian arrays are at least as long as the English base.
# This pads missing entries with empty placeholders so index-based lookups
# do not raise index errors and can be repaired iteratively.
if len(GUI_TEXT_HE) < len(GUI_TEXT):
    GUI_TEXT_HE.extend([''] * (len(GUI_TEXT) - len(GUI_TEXT_HE)))
if len(GUI_TEXT_RU) < len(GUI_TEXT):
    GUI_TEXT_RU.extend([''] * (len(GUI_TEXT) - len(GUI_TEXT_RU)))

# Optional: load external translation JSONs if provided by translators.
# Place files at services/i18n_he.json and services/i18n_ru.json as arrays
# of strings matching the English indices. This lets translators deliver
# professional translations without editing this file directly.
try:
    import json, os
    _base = os.path.dirname(__file__)
    _he_file = os.path.join(_base, 'i18n_he.json')
    _ru_file = os.path.join(_base, 'i18n_ru.json')
    if os.path.exists(_he_file):
        with open(_he_file, 'r', encoding='utf-8') as _f:
            _data = json.load(_f)
            if isinstance(_data, list):
                GUI_TEXT_HE = _data
    if os.path.exists(_ru_file):
        with open(_ru_file, 'r', encoding='utf-8') as _f:
            _data = json.load(_f)
            if isinstance(_data, list):
                GUI_TEXT_RU = _data
except Exception:
    # Fail silently: keep embedded translations if external load fails
    pass

# Manual fixes for misaligned entries discovered during validation.
# These set the correct Hebrew/Russian strings at the English indices
# where translations were shifted or missing.
_fixes = {
    217: ("בחר מורה להעברה", "Выберите учителя для перемещения"),
    222: ("שם משפחה", "Фамилия"),
    261: ("הירשם", "Зарегистрироваться"),
    264: ("הסיסמה חייבת להכיל לפחות 6 תווים", "Пароль должен содержать не менее 6 символов"),
    268: ("בנה מחדש הכול (מילוי אוטומטי)", "Перестроить всё (Автозаполнение)"),
    269: ("Maximum 10 favorites reached. Open \"Load from Favorites\", remove one or more entries, then try saving again. Opening the list now.",
          "Достигнуто максимум 10 избранных. Откройте \"Загрузить из избранного\", удалите одну или несколько записей, затем попробуйте сохранить снова. Открываю список."),
    270: ("Maximum 10 favorites reached. Delete one before saving.", "Достигнуто максимум 10 избранных. Удалите один перед сохранением."),
    273: ("שמור למועדפים", "Сохранить в избранное"),
    281: ("שעות שבועיות של המורה", "Недельные часы преподавателя"),
    287: ("לחץ על כל טווח זמן בטבלה כדי לערוך אותו במקום", "Кликните по любому временному интервалу в таблице, чтобы отредактировать его на месте"),
    288: ("פורמט זמן: H:MM-H:MM או HH:MM-HH:MM (למשל, 9:15-10:00 או 09:15-10:00)",
          "Формат времени: H:MM-H:MM или HH:MM-HH:MM (например, 9:15-10:00 или 09:15-10:00)"),
    289: ("הקש Enter לשמירה, Escape לביטול העריכה במקום", "Нажмите Enter для сохранения, Escape для отмены редактирования на месте"),
    290: ("מספר הטווחים יסונכרן אוטומטית עם ההגדרה \"מספר שיעורים\"", "Количество слотов будет автоматически синхронизировано с настройкой \"Number of lessons\"")
}

for idx, (he_val, ru_val) in _fixes.items():
    if 0 <= idx < len(GUI_TEXT_HE):
        GUI_TEXT_HE[idx] = he_val
    if 0 <= idx < len(GUI_TEXT_RU):
        GUI_TEXT_RU[idx] = ru_val


# Hebrew translations (עברית)
GUI_TEXT_HE = [
    "הוסף מורה",
    "הוסף קבוצה",
    "הוסף מקצוע",
    "מורים",
    "קבוצות",
    "מקצועות",
    "תצוגת יום",
    "מתזמן קבוצה",
    "מתזמן מורה",
    "הגדרות כלליות",
    "שם",
    "מקצוע",
    "שעות",
    "קבוצה",
    "שעות שבועיות של המורים",
    "זמינות",
    "ערוך נבחר",
    "מחק נבחר",
    "העבר למעלה ↑",
    "העבר למטה ↓",
    "בחר מורה לעריכה",
    "בחר קבוצה לעריכה",
    "בחר מקצוע לעריכה",
    "האם אתה בטוח שברצונך למחוק?",
    "אישור",
    "ביטול",
    "שמור",
    "סגור",
    "שם המורה",
    "שם הקבוצה",
    "שם המקצוע",
    "שעות בשבוע",
    "בחר קבוצה:",
    "בחר מורה:",
    "מילוי אוטומטי",
    "נקה",
    "הדפס ל-PDF",
    "יום שני",
    "יום שלישי",
    "יום רביעי",
    "יום חמישי",
    "יום שישי",
    "יום שבת",
    "יום ראשון",
    "שיעור",
    "טווח זמן",
    "הלוח נוצר בהצלחה",
    "התרחשו שגיאות:",
    "לבנות מחדש את הלוח? פעולה זו תמחק את הלוח הנוכחי ותיצור חדש.",
    "למחוק את כל הלוחות? פעולה זו תסיר את כל הלוחות שנוצרו אך תשאיר מורים, קבוצות ומקצועות.",
    "האם אתה בטוח שברצונך לשמור את התצורה? זה יחל על השינויים.",
    "התצורה נשמרה בהצלחה",
    "שפת הממשק",
    "שם האפליקציה",
    "גודל האפליקציה",
    "כיוון מילוי אוטומטי",
    "מקסימום ניסיונות מילוי אוטומטי",
    "מקסימום שיעורים רצופים",
    "מקסימום ליום",
    "מספר שיעורים",
    "ימי השבוע",
    "אנגלית",
    "עברית",
    "רוסית",
    "קדימה",
    "אחורה",
    "אקראי",
    "ייבוא מ-Excel",
    "ייצוא ל-Excel",
    "ייצוא ל-PDF",
    "נקה את כל הלוחות",
    "רענן",
    "עזרה",
    "אודות",
    "הגדרות",
    "יציאה",
    "קובץ",
    "עריכה",
    "תצוגה",
    "כלים",
    "שפה",
    "ערכת נושא",
    "בהיר",
    "כהה",
    "אוטו",
    "חפש",
    "מסנן",
    "מיין",
    "בסדר עולה",
    "בסדר יורד",
    "הוסף",
    "הסר",
    "עדכן",
    "שכפל",
    "העתק",
    "הדבק",
    "חתוך",
    "בטל",
    "בצע שוב",
    "בחר הכל",
    "בטל בחירה",
    "הוקצה/זמין",
    "לא נמצא מורה עבור",
    "לא ניתן למקם את כל השעות עבור",
    "מוקם",
    "סימון כניסה",
    "סימון יציאה",
    "החל",
    "איפוס",
    "ברירת מחדל",
    "מותאם",
    "כן",
    "לא",
    "אישור",
    "שגיאה",
    "אזהרה",
    "מידע",
    "הצלחה",
    "טוען...",
    "אנא המתן...",
    "מעבד...",
    "הושלם",
    "נכשל",
    "בהמתנה",
    "פעיל",
    "לא פעיל",
    "מופעל",
    "מושבת",
    "שדה חובה",
    "קלט לא חוקי",
    "הערך גדול מדי",
    "הערך קטן מדי",
    "פורמט לא חוקי",
    "כבר קיים",
    "לא נמצא",
    "גישה נדחתה",
    "הפעולה בוטלה",
    "הפעולה הושלמה",
    "שומר...",
    "נשמר",
    "לא נשמר",
    "שינויים זוהו",
    "אין שינויים",
    "בטל שינויים?",
    "ייצוא הושלם",
    "ייבוא הושלם",
    "ייצוא נכשל",
    "ייבוא נכשל",
    "בחר קובץ",
    "העלה",
    "הורד",
    "תצוגה מקדימה",
    "הדפס",
    "דף",
    "מתוך",
    "ראשון",
    "אחרון",
    "הבא",
    "הקודם",
    "הצג",
    "הסתר",
    "הרחב",
    "כיווץ",
    "פתח",
    "סגור הכל",
    "רענן הכל",
    "נקה הכל",
    "מחק הכל",
    "ייצא הכל",
    "ייבא הכל",
    "בחירת תאריך",
    "היום",
    "אתמול",
    "מחר",
    "השבוע הזה",
    "השבוע שעבר",
    "השבוע הבא",
    "החודש הזה",
    "החודש שעבר",
    "החודש הבא",
    "השנה הזו",
    "השנה שעברה",
    "השנה הבאה",
    "טווח מותאם",
    "תאריך התחלה",
    "תאריך סיום",
    "שעת התחלה",
    "שעת סיום",
    "משך זמן",
    "סה\"כ",
    "ממוצע",
    "מינימום",
    "מקסימום",
    "ספירה",
    "סכום",
    "אחוז",
    "סטטוס",
    "סוג",
    "קטגוריה",
    "עדיפות",
    "תיאור",
    "הסיסמאות אינן תואמות",
    "החשבון נוצר בהצלחה! מעביר לדף ההתחברות...",
    "ההרשמה נכשלה",
    "אירעה שגיאה. אנא נסה שוב.",
    "התחברות נכשלה",
    "אנא בחר קובץ",
    "יציאה נכשלה",
    "אנא בחר מקצוע מהרשימה הזמינה",
    "מקצוע זה כבר נוסף",
    "נדרש שם המורה",
    "בחר יום, התחלה וסיום",
    "כל הנתונים הקיימים ימחקו. יבוצע ייצוא ל-Excel כגיבוי. להמשיך?",
    "ההתחלה חייבת להיות לפני הסיום",
    "בחר יום והזן זמן הגעה/עזיבה",
    "הזמנים אינם תואמים לאף שיעור",
    "בחר מורה למחיקה",
    "בחר מורה להעברה",
    "בחר קבוצה לעריכה",
    "צור את החשבון שלך",
    "התחבר לחשבונך",
    "שם פרטי",
    "שם משפחה",
    "דוא\"ל (אופציונלי)",
    "שם משתמש",
    "סיסמה",
    "אשר סיסמה",
    "הירשם",
    "התחבר",
    "כבר יש לך חשבון? התחבר",
    "אין לך חשבון? הירשם",
    "הצג התראה סגור",
    "נקה את כל הנתונים",
    "בנה מחדש הכל",
    "התנתק",
    "מתזמן יומי",
    "בחר יום בשבוע",
    "מקצועות זמינים",
    "מקצועות שנבחרו (שם:שעות:קבוצה)",
    "עורך זמינות אינטראקטיבי",
    "הוסף טווחי זמן",
    "סימון כניסה",
    "סימון יציאה",
    "הוסף שעות אמת",
    "יום",
    "שיעורים",
    "טווחי זמן",
    "שעות אמת",
    "סדר עדיפויות:",
    "שעות שבועיות של המורה",
    "טווחי זמן (משני)",
    "שיעורים (שלישוני)",
    "טוען...",
    "ערוך מורה",
    "לחץ כדי לקבוע זמן",
    "לחץ כדי לערוך",
    "מחק טווח",
    "הכל",
    "ערוך קבוצה",
    "ערוך מקצוע",
    "מחק",
    "הירשם",
    "מתזמן בית ספר",
    "שם המשתמש חייב להכיל לפחות 3 תווים ולהכיל רק אותיות, ספרות וקו תחתון",
    "הסיסמה חייבת להכיל לפחות 6 תווים",
    "לפני הבנייה מחדש, נא ייצא את הנתונים הנוכחיים ל-Excel כגיבוי.",
    "כבר ייצאתי",
    "ייצא עכשיו",
    "בנה מחדש הכל (מילוי אוטומטי)",
    "Maximum 10 favorites reached. Open \"Load from Favorites\", remove one or more entries, then try saving again. Opening the list now.",
    "Maximum 10 favorites reached. Delete one before saving.",
    "Save to Favorites",
    "Load from Favorites",
    "Save to Favorites",
    "Load from Favorites",
    "Saved to Favorites",
    "If provided, Time Slots and Lessons are calculated from this",
    "Used only if Weekly Hours is empty. Converted to lesson numbers",
    "Used only if both above are empty",
    "Total Required / Assigned",
    "Comments",
    "שעות שבועיות של המורה",
    "טווחי זמן (משני)",
    "שיעורים (שלישוני)",
    "Teacher's Weekly Hours (PRIMARY)",
    "⚠️ Priority Order:<br>Teacher's Weekly Hours (PRIMARY) - If provided, Time Slots and Lessons are calculated from this<br>Time Slots (SECONDARY) - Used only if Weekly Hours is empty. Converted to lesson numbers<br>Lessons (TERTIARY) - Used only if both above are empty",
    "💡 Tips:",
    "Click on any time range in the table to edit it inline",
    "Time format: H:MM-H:MM or HH:MM-HH:MM (e.g., 9:15-10:00 or 09:15-10:00)",
    "Press Enter to save, Escape to cancel inline editing",
    "Number of slots will auto-sync with \"Number of lessons\" setting"
]



# Hebrew translations for additional messages
GUI_TEXT_HE.extend([
    "הסיסמאות אינן תואמות",
    "החשבון נוצר בהצלחה! נעבור לדף ההתחברות...",
    "ההרשמה נכשלה",
    "אירעה שגיאה. נסה שוב.",
    "ההתחברות נכשלה",
    "אנא בחר קובץ",
    "יציאה נכשלה",
    "אנא בחר מקצוע מהרשימה הזמינה",
    "מקצוע זה נוסף כבר",
    "שם המורה נדרש",
    "בחר יום, התחלה וסיום",
    "ההתחלה חייבת להיות לפני הסיום",
    "בחר יום והזן שעות כניסה/יציאה",
    "הזמנים אינם תואמים לשיעורים כלשהם",
    "בחר מורה למחיקה",
    "בחר מורה להעברה",
    "All existing data will be erased. An Export to Excel will run first. Continue?",
    "בחר קבוצה לעריכה"
])

# Russian translations (Русский)
GUI_TEXT_RU = [
    "Добавить преподавателя",
    "Добавить группу",
    "Добавить предмет",
    "Преподаватели",
    "Группы",
    "Предметы",
    "Просмотр дня",
    "Планировщик группы",
    "Планировщик преподавателя",
    "Общие настройки",
    "Имя",
    "Предмет",
    "Часы",
    "Группа",
    "Недельные часы преподавателей",
    "Доступность",
    "Редактировать выделенное",
    "Удалить выделенное",
    "Переместить вверх ↑",
    "Переместить вниз ↓",
    "Выберите преподавателя для редактирования",
    "Выберите группу для редактирования",
    "Выберите предмет для редактирования",
    "Вы уверены, что хотите удалить?",
    "Подтвердить",
    "Отмена",
    "Сохранить",
    "Закрыть",
    "Имя преподавателя",
    "Название группы",
    "Название предмета",
    "Часов в неделю",
    "Выберите группу:",
    "Выберите преподавателя:",
    "Автозаполнение",
    "Очистить",
    "Печать в PDF",
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье",
    "Урок",
    "Временной интервал",
    "Расписание успешно создано",
    "Произошли ошибки:",
    "Перестроить расписание? Это удалит текущее расписание и создаст новое.",
    "Удалить все расписания? Это удалит все сгенерированные расписания, но сохранит преподавателей, группы и предметы.",
    "Вы уверены, что хотите сохранить настройки? Это применит изменения.",
    "Настройки успешно сохранены",
    "Язык интерфейса",
    "Название приложения",
    "Размер приложения",
    "Направление автозаполнения",
    "Макс. попыток автозаполнения",
    "Макс. последовательных уроков",
    "Макс. в день",
    "Количество уроков",
    "Дни недели",
    "Английский",
    "Иврит",
    "Русский",
    "Вперед",
    "Назад",
    "Случайный",
    "Импорт из Excel",
    "Экспорт в Excel",
    "Экспорт в PDF",
    "Очистить все расписания",
    "Обновить",
    "Помощь",
    "О программе",
    "Настройки",
    "Выход",
    "Файл",
    "Правка",
    "Вид",
    "Инструменты",
    "Язык",
    "Тема",
    "Светлая",
    "Тёмная",
    "Авто",
    "Поиск",
    "Фильтр",
    "Сортировка",
    "По возрастанию",
    "По убыванию",
    "Добавить",
    "Удалить",
    "Обновить",
    "Дублировать",
    "Копировать",
    "Вставить",
    "Вырезать",
    "Отменить",
    "Повторить",
    "Выбрать всё",
    "Снять выделение",
    "Назначено/Доступно",
    "Преподаватель не найден для",
    "Не удалось разместить все часы для",
    "размещено",
    "Регистрация прихода",
    "Регистрация ухода",
    "Применить",
    "Сбросить",
    "По умолчанию",
    "Пользовательский",
    "Да",
    "Нет",
    "ОК",
    "Ошибка",
    "Предупреждение",
    "Информация",
    "Успех",
    "Загрузка...",
    "Пожалуйста, подождите...",
    "Обработка...",
    "Завершено",
    "Не удалось",
    "В ожидании",
    "Активно",
    "Неактивно",
    "Включено",
    "Отключено",
    "Обязательное поле",
    "Неверный ввод",
    "Значение слишком велико",
    "Значение слишком мало",
    "Неверный формат",
    "Уже существует",
    "Не найдено",
    "Доступ запрещён",
    "Операция отменена",
    "Операция выполнена",
    "Сохранение...",
    "Сохранено",
    "Не сохранено",
    "Обнаружены изменения",
    "Нет изменений",
    "Отменить изменения?",
    "Экспорт завершён",
    "Импорт завершён",
    "Экспорт не удался",
    "Импорт не удался",
    "Выберите файл",
    "Загрузить",
    "Скачать",
    "Предпросмотр",
    "Печать",
    "Страница",
    "из",
    "Первая",
    "Последняя",
    "Далее",
    "Назад",
    "Показать",
    "Скрыть",
    "Развернуть",
    "Свернуть",
    "Открыть",
    "Закрыть всё",
    "Обновить всё",
    "Очистить всё",
    "Удалить всё",
    "Экспортировать всё",
    "Импортировать всё",
    "Выбрать дату",
    "Сегодня",
    "Вчера",
    "Завтра",
    "Эта неделя",
    "Прошлая неделя",
    "Следующая неделя",
    "Этот месяц",
    "Прошлый месяц",
    "Следующий месяц",
    "Этот год",
    "Прошлый год",
    "Следующий год",
    "Произвольный диапазон",
    "Дата начала",
    "Дата окончания",
    "Время начала",
    "Время окончания",
    "Длительность",
    "Итого",
    "Среднее",
    "Минимум",
    "Максимум",
    "Количество",
    "Сумма",
    "Процент",
    "Статус",
    "Тип",
    "Категория",
    "Приоритет",
    "Описание",
    "Пароли не совпадают",
    "Аккаунт успешно создан! Перенаправление на страницу входа...",
    "Регистрация не удалась",
    "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
    "Не удалось войти",
    "Пожалуйста, выберите файл",
    "Не удалось выйти",
    "Пожалуйста, выберите предмет из доступных",
    "Этот предмет уже добавлен",
    "Требуется имя преподавателя",
    "Выберите день, начало и конец",
    "Все существующие данные будут удалены. Сначала будет выполнен экспорт в Excel. Продолжить?",
    "Начало должно быть раньше конца",
    "Выберите день и укажите время прихода/ухода",
    "Время не соответствует ни одному уроку",
    "Выберите преподавателя для удаления",
    "Выберите преподавателя для перемещения",
    "Выберите группу для редактирования",
    "Создайте вашу учётную запись",
    "Войдите в ваш аккаунт",
    "Имя",
    "Фамилия",
    "Электронная почта (необязательно)",
    "Имя пользователя",
    "Пароль",
    "Подтвердите пароль",
    "Зарегистрироваться",
    "Войти",
    "Уже есть аккаунт? Войдите",
    "Нет аккаунта? Зарегистрируйтесь",
    "Показать уведомление Закрыть",
    "Очистить все данные",
    "Перестроить всё",
    "Выйти",
    "Планировщик дня",
    "Выберите день недели",
    "Доступные предметы",
    "Выбранные предметы (название:часов:группа)",
    "Интерактивный редактор доступности",
    "Добавить временные интервалы",
    "Регистрация прихода",
    "Регистрация ухода",
    "Добавить реальные часы",
    "День",
    "Уроки",
    "Временные интервалы",
    "Реальные часы",
    "Порядок приоритета:",
    "Недельные часы преподавателя",
    "Временные интервалы (ВТОРИЧНО)",
    "Уроки (ТЕРЦИАРНО)",
    "Загрузка...",
    "Редактировать преподавателя",
    "Нажмите, чтобы установить время",
    "Нажмите, чтобы отредактировать",
    "Удалить интервал",
    "Все",
    "Редактировать группу",
    "Редактировать предмет",
    "Удалить",
    "Зарегистрироваться",
    "School Scheduler",
    "Имя пользователя должно содержать не менее 3 символов и состоять только из букв, цифр и подчёркиваний",
    "Пароль должен содержать не менее 6 символов",
    "Перед перестроением, пожалуйста, экспортируйте текущие данные в Excel в качестве резервной копии.",
    "Я уже экспортировал",
    "Экспортировать сейчас",
    "Перестроить всё (Автозаполнение)",
    "Достигнуто максимум 10 избранных. Откройте \"Загрузить из избранного\", удалите одну или несколько записей, затем попытайтесь сохранить снова. Открываю список.",
    "Достигнуто максимум 10 избранных. Удалите один перед сохранением.",
    "Сохранить в избранное",
    "Загрузить из избранного",
    "Сохранить в избранное",
    "Загрузить из избранного",
    "Сохранено в избранное",
    "Если указано, временные интервалы и уроки вычисляются на его основе",
    "Используется только если поле 'Недельные часы' пусто. Преобразуется в номера уроков",
    "Используется только если оба вышеуказанных поля пусты",
    "Всего требуемо / Назначено",
    "Комментарии",
    "Недельные часы преподавателя",
    "Временные интервалы (ВТОРИЧНО)",
    "Уроки (ТЕРЦИАРНО)",
    "Недельные часы преподавателя (ПЕРВИЧНО)",
    "⚠️ Порядок приоритета:<br>Недельные часы преподавателя (ПЕРВИЧНО) - Если указано, временные интервалы и уроки вычисляются на его основе<br>Временные интервалы (ВТОРИЧНО) - Используется только если Недельные часы пусты. Преобразуется в номера уроков<br>Уроки (ТЕРЦИАРНО) - Используется только если оба вышеуказанных поля пусты",
    "💡 Подсказки:",
    "Нажмите на любой временной интервал в таблице, чтобы отредактировать его на месте",
    "Формат времени: H:MM-H:MM или HH:MM-HH:MM (например, 9:15-10:00 или 09:15-10:00)",
    "Нажмите Enter, чтобы сохранить, Escape — чтобы отменить редактирование на месте",
    "Количество слотов будет автоматически синхронизировано с настройкой 'Number of lessons'"
]



# Russian translations for additional messages
GUI_TEXT_RU.extend([
    "Пароли не совпадают",
    "Аккаунт успешно создан! Перенаправление на страницу входа...",
    "Ошибка регистрации",
    "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
    "Ошибка входа",
    "Пожалуйста, выберите файл",
    "Выход не удался",
    "Пожалуйста, выберите предмет из доступных",
    "Этот предмет уже добавлен",
    "Требуется имя учителя",
    "Выберите день, начало и конец",
    "Начало должно быть раньше конца",
    "Выберите день и укажите время прихода/ухода",
    "Время не соответствует ни одному уроку",
    "Выберите учителя для удаления",
    "Выберите учителя для перемещения",
    "Выберите группу для редактирования"
])

# More UI strings used in auth pages and headers
GUI_TEXT.extend([
    "Create your account",
    "Login to your account",
    "First Name",
    "Last Name",
    "Email (optional)",
    "Username",
    "Password",
    "Confirm Password",
    "Sign Up",
    "Login",
    "Already have an account? Login",
    "Don't have an account? Sign Up",
    "Show Alert Close"
    ,
    "Clear All Data",
    "Rebuild All",
    "Logout",
    "Day Scheduler",
    "Select Weekday"
])

GUI_TEXT_HE.extend([
    "צור את החשבון שלך",
    "התחברות לחשבון",
    "שם פרטי",
    "שם משפחה",
    "אימייל (אופציונלי)",
    "שם משתמש",
    "סיסמה",
    "אשר סיסמה",
    "הירשם",
    "התחבר",
    "כבר יש חשבון? התחבר",
    "אין חשבון? הירשם",
    "סגור הודעה"
    ,
    "נקה כל הנתונים",
    "בנה מערכות מחדש",
    "התנתק",
    "מתזמן יום",
    "בחר יום בשבוע"
])

GUI_TEXT_RU.extend([
    "Создайте аккаунт",
    "Войдите в свой аккаунт",
    "Имя",
    "Фамилия",
    "Email (необязательно)",
    "Имя пользователя",
    "Пароль",
    "Подтвердите пароль",
    "Регистрация",
    "Вход",
    "Уже есть аккаунт? Войти",
    "Нет аккаунта? Зарегистрироваться",
    "Закрыть сообщение"
    ,
    "Очистить все данные",
    "Пересобрать всё",
    "Выйти",
    "Просмотр дня",
    "Выберите день недели"
])

# Additional UI keys used in Edit Teacher modal and availability editor
GUI_TEXT.extend([
    "Available Subjects",
    "Selected Subjects (name:hours:group)",
    "Interactive Availability Editor",
    "Add Time Slots",
    "Check-in",
    "Check-out",
    "Add Real Hours",
    "Day",
    "Lessons",
    "Time Slots",
    "Real Hours",
    "Priority Order:",
    "Teacher's Weekly Hours",
    "Time Slots (SECONDARY)",
    "Lessons (TERTIARY)",
    "Loading..."
])

GUI_TEXT_HE.extend([
    "מקצועות זמינים",
    "מקצועות נבחרים (שם:שעות:קבוצה)",
    "עורך זמינות אינטראקטיבי",
    "הוסף טווחי זמן",
    "כניסה",
    "יציאה",
    "הוסף שעות אמיתיות",
    "יום",
    "שיעורים",
    "טווחי זמן",
    "שעות אמיתיות",
    "סדר עדיפויות:",
    "שעות שבועיות של המורה",
    "טווחי זמן (משני)",
    "שיעורים (שלישוני)",
    "טוען..."
])

GUI_TEXT_RU.extend([
    "Доступные предметы",
    "Выбранные предметы (имя:часы:группа)",
    "Интерактивный редактор доступности",
    "Добавить временные слоты",
    "Время входа",
    "Время выхода",
    "Добавить реальные часы",
    "День",
    "Уроки",
    "Временные слоты",
    "Реальные часы",
    "Порядок приоритетов:",
    "Недельные часы преподавателя",
    "Временные слоты (ВТОРИЧНЫЕ)",
    "Уроки (ТЕРЦИЧНЫЕ)",
    "Загрузка..."
])

GUI_TEXT.extend(["Edit Teacher"])
GUI_TEXT_HE.extend(["ערוך מורה"])
GUI_TEXT_RU.extend(["Редактировать учителя"])

# Additional small UI keys used in JS
GUI_TEXT.extend([
    "Click to set time",
    "Click to edit",
    "Delete slot"
])

GUI_TEXT_HE.extend([
    "לחץ כדי להגדיר זמן",
    "לחץ כדי לערוך",
    "מחק משבצת"
])

GUI_TEXT_RU.extend([
    "Нажмите, чтобы установить время",
    "Нажмите, чтобы редактировать",
    "Удалить слот"
])

GUI_TEXT.extend([
    "All",
    "Edit Group",
    "Edit Subject",
    "Delete"
])

GUI_TEXT_HE.extend([
    "הכל",
    "ערוך קבוצה",
    "ערוך מקצוע",
    "מחק"
])

GUI_TEXT_RU.extend([
    "Все",
    "Редактировать группу",
    "Редактировать предмет",
    "Удалить"
])

# Signup / auth small messages
GUI_TEXT.extend([
    "Sign Up",
    "School Scheduler",
    "Username must be at least 3 characters and contain only letters, numbers, and underscores",
    "Password must be at least 6 characters"
])

GUI_TEXT_HE.extend([
    "הצטרף",
    "מתזמן בית ספר",
    "שם המשתמש חייב להכיל לפחות 3 תווים ולכלול אותיות, ספרות וקו תחתון בלבד",
    "הסיסמה חייבת להכיל לפחות 6 תווים"
])

GUI_TEXT_RU.extend([
    "Зарегистрироваться",
    "School Scheduler",
    "Имя пользователя должно содержать не менее 3 символов и содержать только буквы, цифры и подчёркивания",
    "Пароль должен содержать не менее 6 символов"
])

# Additional texts used in Rebuild modal
GUI_TEXT.extend([
    "Before rebuilding, please export your current data to Excel as a backup.",
    "I already exported",
    "Export now"
])

# Hebrew translations for the added texts
GUI_TEXT_HE.extend([
    "לפני ביצוע שחזור, נא לייצא את הנתונים הנוכחיים לאקסל כגיבוי.",
    "כבר ייצאתי",
    "ייצא עכשיו"
])

# Russian translations for the added texts
GUI_TEXT_RU.extend([
    "Перед перестроением, пожалуйста, экспортируйте текущие данные в Excel в качестве резервной копии.",
    "Я уже экспортировал",
    "Экспортировать сейчас"
])

# Add 'Rebuild All (Autofill)' to translations
GUI_TEXT.extend([
    "Rebuild All (Autofill)"
])

GUI_TEXT_HE.extend([
    "בנה מחדש הכול (מילוי אוטומטי)"
])

GUI_TEXT_RU.extend([
    "Перестроить всё (Автозаполнение)"
])


# Messages related to the Favorites feature (added so new UI/server texts have i18n entries)
GUI_TEXT.extend([
    "Maximum 10 favorites reached. Open \"Load from Favorites\", remove one or more entries, then try saving again. Opening the list now.",
    "Maximum 10 favorites reached. Delete one before saving."
])

# Placeholder Hebrew translations for the added Favorites texts
GUI_TEXT_HE.extend([
    "Maximum 10 favorites reached. Open \"Load from Favorites\", remove one or more entries, then try saving again. Opening the list now.",
    "Maximum 10 favorites reached. Delete one before saving."
])

# Placeholder Russian translations for the added Favorites texts
GUI_TEXT_RU.extend([
    "Maximum 10 favorites reached. Open \"Load from Favorites\", remove one or more entries, then try saving again. Opening the list now.",
    "Maximum 10 favorites reached. Delete one before saving."
])

# Favorites button labels
GUI_TEXT.extend([
    "Save to Favorites",
    "Load from Favorites"
])

# Add 'Saved to Favorites' and button labels
GUI_TEXT.extend([
    "Save to Favorites",
    "Load from Favorites",
    "Saved to Favorites"
])

# Hebrew translations for favorites labels
GUI_TEXT_HE.extend([
    "שמור למועדפים",
    "טען מהמועדפים",
    "נשמר במועדפים"
])

# Russian translations for favorites labels
GUI_TEXT_RU.extend([
    "Сохранить в избранное",
    "Загрузить из избранного",
    "Сохранено в избранное"
])

# Add confirmation translation placeholder for Russian
GUI_TEXT_RU.extend([
    "All existing data will be erased. An Export to Excel will run first. Continue?"
])


# Time slots / lessons explanatory texts
GUI_TEXT.extend([
    "If provided, Time Slots and Lessons are calculated from this",
    "Used only if Weekly Hours is empty. Converted to lesson numbers"
])

GUI_TEXT_HE.extend([
    "אם הוזן, טווחי הזמן ומספר השיעורים יחושבו על פיו",
    "משמש רק אם שדה 'שעות שבועיות' ריק. יומר למספר שיעורים"
])

GUI_TEXT_RU.extend([
    "Если указано, временные слоты и количество уроков рассчитываются на его основе",
    "Используется только если поле 'Недельные часы' пусто. Преобразуется в номера уроков"
])

GUI_TEXT.extend([
    "Used only if both above are empty"
])

GUI_TEXT_HE.extend([
    "משמש רק אם שני השדות שלעיל ריקים"
])

GUI_TEXT_RU.extend([
    "Используется только если оба вышеуказанных поля пусты"
])

# Table column labels
GUI_TEXT.extend([
    "Total Required / Assigned",
    "Comments"
])

GUI_TEXT_HE.extend([
    "סה\"כ נדרש / מוקצה",
    "הערות"
])

GUI_TEXT_RU.extend([
    "Всего требуется / Назначено",
    "Комментарии"
])

# Priority labels (exact keys used in templates)
GUI_TEXT.extend([
    "Teacher's Weekly Hours",
    "Time Slots (SECONDARY)",
    "Lessons (TERTIARY)"
])

GUI_TEXT_HE.extend([
    "שעות שבועיות של המורה (PRIMARY)",
    "טווחי זמן (משני)",
    "שיעורים (שלישוני)"
])

GUI_TEXT_RU.extend([
    "Недельные часы преподавателя (PRIMARY)",
    "Временные интервалы (SECONDARY)",
    "Уроки (TERTIARY)"
])

# Full label including parenthetical for Priority Order (PRIMARY)
GUI_TEXT.extend([
    "Teacher's Weekly Hours (PRIMARY)"
])

GUI_TEXT_HE.extend([
    "שעות שבועיות של המורה (ראשוני)"
])

GUI_TEXT_RU.extend([
    "Недельные часы преподавателя (ПЕРВИЧНО)"
])

# Full localized block for the Priority Order confirmation (single-key to avoid mixed fragments)
GUI_TEXT.extend([
    "⚠️ Priority Order:<br>Teacher's Weekly Hours (PRIMARY) - If provided, Time Slots and Lessons are calculated from this<br>Time Slots (SECONDARY) - Used only if Weekly Hours is empty. Converted to lesson numbers<br>Lessons (TERTIARY) - Used only if both above are empty"
])

GUI_TEXT_HE.extend([
    "⚠️ סדר עדיפויות:<br>שעות שבועיות של המורה (ראשוני) - אם הוזנו, טווחי הזמן ומספר השיעורים יחושבו על פיהם<br>טווחי זמן (משני) - ישמשו רק אם שדה 'שעות שבועיות' ריק. יומרו למספרי שיעור<br>שיעורים (שלישוני) - ישמשו רק אם שני השדות שלעיל ריקים"
])

GUI_TEXT_RU.extend([
    "⚠️ Порядок приоритетов:<br>Недельные часы преподавателя (ПЕРВИЧНЫЕ) - Если заданы, по ним рассчитываются временные слоты и уроки<br>Временные интервалы (ВТОРИЧНЫЕ) - Используются только если поле 'Недельные часы' пусто. Преобразуются в номера уроков<br>Уроки (ТЕРЦИЧНЫЕ) - Используются только если оба вышеуказанных поля пусты"
])

# Ensure specific critical keys have correct Hebrew/Russian translations
_corrections = {
    "Priority Order:": { 'he': "סדר עדיפויות:", 'ru': "Порядок приоритетов:" },
    "Teacher's Weekly Hours": { 'he': "שעות שבועיות של המורה (PRIMARY)", 'ru': "Недельные часы преподавателя (PRIMARY)" },
    "Time Slots (SECONDARY)": { 'he': "טווחי זמן (משני)", 'ru': "Временные интервалы (SECONDARY)" },
    "Lessons (TERTIARY)": { 'he': "שיעורים (שלישוני)", 'ru': "Уроки (TERTIARY)" },
    "Total Required / Assigned": { 'he': "סה\"כ נדרש / מוקצה", 'ru': "Всего требуется / Назначено" },
    "Comments": { 'he': "הערות", 'ru': "Комментарии" }
}

for key, vals in _corrections.items():
    try:
        idx = GUI_TEXT.index(key)
        if 'he' in vals and 0 <= idx < len(GUI_TEXT_HE):
            GUI_TEXT_HE[idx] = vals['he']
        if 'ru' in vals and 0 <= idx < len(GUI_TEXT_RU):
            GUI_TEXT_RU[idx] = vals['ru']
    except ValueError:
        # key not found in English list - ignore
        pass

# Inline editing tips shown in Time Slots section
GUI_TEXT.extend([
    "💡 Tips:",
    "Click on any time range in the table to edit it inline",
    "Time format: H:MM-H:MM or HH:MM-HH:MM (e.g., 9:15-10:00 or 09:15-10:00)",
    "Press Enter to save, Escape to cancel inline editing",
    "Number of slots will auto-sync with \"Number of lessons\" setting"
])

GUI_TEXT_HE.extend([
    "💡 טיפים:",
    "לחץ על כל טווח זמן בטבלה כדי לערוך אותו במקום",
    "פורמט זמן: H:MM-H:MM או HH:MM-HH:MM (למשל, 9:15-10:00 או 09:15-10:00)",
    "הקש Enter לשמירה, Escape לביטול העריכה במקום",
    "מספר הטווחים יסונכרן אוטומטית עם ההגדרה \"מספר שיעורים\""
])

GUI_TEXT_RU.extend([
    "💡 Советы:",
    "Кликните по любому временному интервалу в таблице, чтобы отредактировать его на месте",
    "Формат времени: H:MM-H:MM или HH:MM-HH:MM (например, 9:15-10:00 или 09:15-10:00)",
    "Нажмите Enter для сохранения, Escape для отмены редактирования на месте",
    "Количество слотов будет автоматически синхронизировано с настройкой \"Number of lessons\""
])


# Final overrides to correct remaining mismatches (applied after all translations defined)
_final_overrides = {
    269: ("הגעת למקסימום של 10 פריטים במועדפים. פתח \"טען מהמועדפים\", מחק פריט/ים, ונסה לשמור שוב. פותח את הרשימה כעת.",
          "Достигнуто максимум 10 избранных. Откройте \"Загрузить из избранного\", удалите одну или несколько записей, затем попробуйте сохранить снова. Открываю список."),
    270: ("הגעת למקסימום של 10 מועדפים. מחק אחד לפני השמירה.", "Достигнуто максимум 10 избранных. Удалите один перед сохранением."),
    275: ("נשמר במועדפים", "Сохранено в избранное"),
    289: ("הקש Enter לשמירה, Escape לביטול העריכה במקום", "Нажмите Enter для сохранения, Escape для отмены редактирования на месте"),
    290: ("מספר הטווחים יסונכרן אוטומטית עם ההגדרה \"מספר שיעורים\"", "Количество слотов будет автоматически синхронизировано с настройкой \"Number of lessons\"")
}

# Ensure HE/RU arrays have the same length as GUI_TEXT before applying overrides
if len(GUI_TEXT_HE) < len(GUI_TEXT):
    GUI_TEXT_HE.extend([''] * (len(GUI_TEXT) - len(GUI_TEXT_HE)))
if len(GUI_TEXT_RU) < len(GUI_TEXT):
    GUI_TEXT_RU.extend([''] * (len(GUI_TEXT) - len(GUI_TEXT_RU)))

for idx, (he_val, ru_val) in _final_overrides.items():
    if 0 <= idx < len(GUI_TEXT_HE):
        GUI_TEXT_HE[idx] = he_val
    if 0 <= idx < len(GUI_TEXT_RU):
        GUI_TEXT_RU[idx] = ru_val

# Ensure specific General/Time-slot keys exist in the English master
# (some were previously appended before the large GUI_TEXT literal and
# thus got overwritten). Add them now so translations align by index.
GUI_TEXT.extend([
    "Add New Time Slot",
    "Lesson Number",
    "Add Slot",
    "Choose a preset, then edit the comma-separated weekdays if needed",
    "Time Range (click to edit)",
    "Enter favorite name:",
    "OK",
    "Cancel"
    ,"Favorites",
    "Rename",
    "Load"
])

# Final: if translator JSONs or user "New" JSONs exist, prefer them
# This ensures any remaining English placeholders from incremental
# `extend` calls can be replaced by translator-supplied complete arrays
# or by partial/override JSONs created by the team (i18n_*_new.json).
try:
    import json, os
    _base = os.path.dirname(__file__)

    def _load_json(path):
        try:
            with open(path, 'r', encoding='utf-8') as _f:
                return json.load(_f)
        except Exception:
            return None

    # original translator files (full-list expected)
    _he_file = os.path.join(_base, 'i18n_he.json')
    _ru_file = os.path.join(_base, 'i18n_ru.json')

    if os.path.exists(_he_file):
        _data = _load_json(_he_file)
        if isinstance(_data, list) and len(_data) == len(GUI_TEXT):
            GUI_TEXT_HE = _data
    if os.path.exists(_ru_file):
        _data = _load_json(_ru_file)
        if isinstance(_data, list) and len(_data) == len(GUI_TEXT):
            GUI_TEXT_RU = _data

    # New override files (can be full lists or partial dicts)
    _text_new = os.path.join(_base, 'i18n_text_new.json')
    _he_new = os.path.join(_base, 'i18n_he_new.json')
    _ru_new = os.path.join(_base, 'i18n_ru_new.json')

    # store string-keyed overrides for lookup when GUI_TEXT doesn't contain the key
    _NEW_TEXT_OVERRIDES = {}
    _NEW_HE_OVERRIDES = {}
    _NEW_RU_OVERRIDES = {}

    def _apply_override(data, target_list, name):
        # data can be a list (full replace) or dict (partial overrides)
        if data is None:
            return target_list
        if isinstance(data, list):
            if len(data) == len(GUI_TEXT):
                return data
            # if lengths mismatch - ignore full replace but log in debug
            return target_list
        if isinstance(data, dict):
            # dict keys: either numeric indices (as str/int) or English key strings
            for k, v in data.items():
                try:
                    idx = int(k)
                    if 0 <= idx < len(target_list):
                        target_list[idx] = v
                        continue
                except Exception:
                    pass
                # otherwise treat k as English string key and apply to all matches
                try:
                    matches = [i for i, t in enumerate(GUI_TEXT) if t == k]
                    if matches:
                        for i in matches:
                            if 0 <= i < len(target_list):
                                target_list[i] = v
                    else:
                        # store as string-keyed override for later lookup
                        if name == 'he_new':
                            _NEW_HE_OVERRIDES[k] = v
                        elif name == 'ru_new':
                            _NEW_RU_OVERRIDES[k] = v
                        elif name == 'text_new':
                            _NEW_TEXT_OVERRIDES[k] = v
                except Exception:
                    continue
            return target_list
        return target_list

    # load and apply new files if present
    if os.path.exists(_text_new):
        _data = _load_json(_text_new)
        # English master (GUI_TEXT) should not be fully replaced here by default;
        # if a full list is provided and length matches, replace GUI_TEXT too.
        if isinstance(_data, list) and len(_data) == len(GUI_TEXT):
            GUI_TEXT = _data
        elif isinstance(_data, dict):
            GUI_TEXT = _apply_override(_data, GUI_TEXT, 'text_new')

    if os.path.exists(_he_new):
        _data = _load_json(_he_new)
        GUI_TEXT_HE = _apply_override(_data, GUI_TEXT_HE, 'he_new')

    if os.path.exists(_ru_new):
        _data = _load_json(_ru_new)
        GUI_TEXT_RU = _apply_override(_data, GUI_TEXT_RU, 'ru_new')

except Exception:
    pass

# Re-apply critical final overrides in case translator arrays need them
for idx, (he_val, ru_val) in _final_overrides.items():
    if 0 <= idx < len(GUI_TEXT_HE):
        GUI_TEXT_HE[idx] = he_val
    if 0 <= idx < len(GUI_TEXT_RU):
        GUI_TEXT_RU[idx] = ru_val


def get_text(index, lang='English'):
    """Get translated text by index or by English-key string.

    If `index` is a string, attempt to find its index in the English
    `GUI_TEXT` list and return the translation at that index for the
    requested `lang`. If not found, return the original string as a
    sensible fallback.
    """
    # Allow lookups by English key string
    if isinstance(index, str):
        try:
            idx = GUI_TEXT.index(index)
        except ValueError:
            # Not found in GUI_TEXT: check new-file string-keyed overrides
            try:
                if lang == 'עברית' or lang == 'Hebrew':
                    if index in _NEW_HE_OVERRIDES:
                        return _NEW_HE_OVERRIDES[index]
                elif lang == 'Русский' or lang == 'Russian':
                    if index in _NEW_RU_OVERRIDES:
                        return _NEW_RU_OVERRIDES[index]
                else:
                    if index in _NEW_TEXT_OVERRIDES:
                        return _NEW_TEXT_OVERRIDES[index]
            except Exception:
                pass
            # Not found anywhere: return the string itself
            return index
    else:
        idx = index

    if lang == 'עברית' or lang == 'Hebrew':
        if 0 <= idx < len(GUI_TEXT_HE):
            return GUI_TEXT_HE[idx]
    elif lang == 'Русский' or lang == 'Russian':
        if 0 <= idx < len(GUI_TEXT_RU):
            return GUI_TEXT_RU[idx]

    # Default to English
    if 0 <= idx < len(GUI_TEXT):
        return GUI_TEXT[idx]

    return f"[Missing: {index}]"


def get_all_texts(lang='English'):
    """Get all texts for client-side use"""
    # Return both the texts list and any string-keyed overrides so the
    # client can apply translations for hardcoded strings that are not
    # present in the `GUI_TEXT` list.
    if lang == 'עברית' or lang == 'Hebrew':
        payload = {'texts': GUI_TEXT_HE}
        try:
            payload['overrides'] = _NEW_HE_OVERRIDES
        except NameError:
            payload['overrides'] = {}
        return payload
    elif lang == 'Русский' or lang == 'Russian':
        payload = {'texts': GUI_TEXT_RU}
        try:
            payload['overrides'] = _NEW_RU_OVERRIDES
        except NameError:
            payload['overrides'] = {}
        return payload
    else:
        payload = {'texts': GUI_TEXT}
        try:
            payload['overrides'] = _NEW_TEXT_OVERRIDES
        except NameError:
            payload['overrides'] = {}
        return payload


def get_language_code(lang):
    """Get ISO language code"""
    lang_map = {
        'English': 'en',
        'עברית': 'he',
        'Hebrew': 'he',
        'Русский': 'ru',
        'Russian': 'ru'
    }
    return lang_map.get(lang, 'en')


def is_rtl(lang):
    """Check if language is RTL"""
    return lang in ['עברית', 'Hebrew']

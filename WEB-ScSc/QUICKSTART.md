# School Scheduler - Quick Start Guide

## Installation

### Windows

1. **Make sure Python 3.10+ is installed**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Double-click `start.bat`**
   - This will automatically:
     - Activate the virtual environment
     - Start the Flask server
   - The application will open at: http://localhost:5000

3. **Alternative: Manual start**
   ```cmd
   .venv\Scripts\activate
   python app.py
   ```

## First Time Setup

### Step 1: Configure Settings
1. Click on **General Configuration** tab
2. Set your preferences:
   - **GUI Language**: Choose English, עברית, or Русский
   - **Number of Lessons**: 8 (default)
   - **Max Sequence Lessons**: 2 (prevents 3+ consecutive lessons)
   - **Max Per Day**: 3 (max lessons of same subject per day)
3. Click **Save**

### Step 2: Add Teachers
1. Go to **Teachers** tab
2. Click **Add Teacher**
3. Fill in the form:

   **Example Teacher:**
   - **Name**: John Smith
   - **Subjects**: 
     - Subject: Math, Hours: 5, Group: Group A
     - Subject: Physics, Hours: 3, Group: Group A
   - **Teachers Weekly Hours** (IMPORTANT!):
     ```
     Monday:08:00-12:00; Monday:13:00-17:00; Tuesday:08:00-15:00; Wednesday:08:00-15:00
     ```
   - **Availability** (optional, only used if Weekly Hours is empty):
     ```
     Monday:1-5; Tuesday:1-5; Wednesday:1-5
     ```

4. Click **Save**
5. Repeat for all teachers

**Important Notes:**
- **Teachers Weekly Hours** takes PRIORITY over Availability
- Format: `Day:HH:MM-HH:MM; Day:HH:MM-HH:MM`
- The system automatically converts time ranges to lesson numbers
- You can have multiple time ranges per day (e.g., morning and afternoon)

### Step 3: Add Groups
1. Go to **Groups** tab
2. Click **Add Group**
3. Enter group name: "Group A"
4. Click **Save**
5. Repeat for all groups (e.g., "Group B", "Group C")

### Step 4: Add Subjects
1. Go to **Subjects** tab
2. Click **Add Subject**
3. Fill in:

   **Example Subject:**
   - **Name**: Math
   - **Group**: Group A
   - **Hours Per Week**: 5

4. Click **Save**
5. Repeat for all subjects

**Tip**: Make sure each subject has a teacher assigned (the teacher must have this subject in their subjects list from Step 2)

### Step 5: Generate Schedule
1. Go to **Group Scheduler** tab
2. Select "Group A" from dropdown
3. Click **Autofill**
4. Confirm: "Rebuild the schedule? This will delete the current schedule and create a new one."
5. Click **Yes**
6. Wait a moment...
7. Success! The schedule appears in the grid!

**If autofill fails:**
- Check that all subjects have teachers assigned
- Check that teachers have availability defined
- Verify teacher availability covers enough time slots
- Try increasing "Max Autofill Retries" in configuration

### Step 6: View Teacher Schedules
1. Go to **Teacher Scheduler** tab
2. Select a teacher from dropdown
3. View their complete schedule (automatically generated from group schedules)

### Step 7: Export to PDF
1. In **Group Scheduler** or **Teacher Scheduler**
2. Click **Print to PDF**
3. PDF file will download automatically
4. Open and print or share!

## Common Tasks

### Edit a Lesson Manually
1. Go to **Group Scheduler**
2. Select the group
3. **Click on any cell** in the schedule grid
4. A modal appears:
   - Change subject
   - Change teacher
5. Click **Save**
6. Or click **Remove** to delete the lesson

### Move Teachers Up/Down in List
1. Go to **Teachers** tab
2. Click on a teacher row to select it
3. Click **Move Up ↑** or **Move Down ↓**
4. Teacher position changes

### Delete Items
1. Select the item (teacher/group/subject) by clicking the row
2. Click **Delete Selected**
3. Confirm deletion

### Clear All Schedules
1. Click **Clear All Schedules** in top toolbar
2. Confirm
3. All group and teacher schedules are deleted
4. Teachers, Groups, and Subjects remain intact

### Change Language
1. Go to **General Configuration**
2. Change **GUI Language** to עברית or Русский
3. Click **Save**
4. Page will reload with new language
5. For Hebrew, layout switches to RTL (right-to-left)

## Understanding the Excel File

All data is stored in `data/SchoolScheduler.xlsx` with 8 sheets:

### Sheet 1: Configuration
Settings like language, autofill direction, constraints

### Sheet 2: Weekdays
List of weekdays (Monday-Friday by default)

### Sheet 3: Time Slots
Lesson numbers and time ranges (1: 08:00-09:00, etc.)

### Sheet 4: Teachers
**Most Important Sheet!**

| Name | Subject | Hours | Group | Teachers Weekly Hours | Availability |
|------|---------|-------|-------|----------------------|--------------|
| John Smith | Math | 5 | Group A | Monday:08:00-12:00 | Monday:1-5 |

**Priority**: Teachers Weekly Hours > Availability

### Sheet 5: Groups
Group names and their subjects

### Sheet 6: Subjects
Subject names, groups, hours per week, assigned teachers

### Sheet 7: Group Schedules
Generated schedules for each group

### Sheet 8: Teacher Schedules
Auto-generated from group schedules

**Tip**: You can edit the Excel file directly and refresh the web app!

## Troubleshooting

### Problem: "No teacher found for Math"
**Solution**: Add a teacher who teaches Math for the correct group in the Teachers tab

### Problem: "Could not place all hours for Math (placed 3/5)"
**Solutions**:
- Increase teacher availability
- Increase "Max Per Day" constraint
- Increase "Max Autofill Retries"
- Reduce hours per week for the subject

### Problem: Schedule looks wrong after autofill
**Solution**: 
- Click **Clear** to remove the schedule
- Check teacher availability
- Check constraints (max sequence, max per day)
- Try **Autofill** again

### Problem: Teacher shows up at two places at same time
**Solution**: This should not happen! The conflict checker prevents this. If you see this:
1. Click **Clear All Schedules**
2. Re-run **Autofill** for all groups
3. Teacher schedules will rebuild correctly

### Problem: Application won't start
**Solutions**:
- Check Python is installed: `python --version`
- Reinstall packages: `.venv\Scripts\activate` then `pip install -r requirements.txt`
- Check if port 5000 is in use by another program
- Try a different port: Edit app.py, change `port=5000` to `port=8080`

### Problem: PDF export doesn't work
**Solution**: 
- WeasyPrint requires additional system libraries on Linux
- On Windows, it should work after `pip install WeasyPrint`
- If fails, check error message for missing dependencies

## Tips and Best Practices

1. **Start Small**: Begin with 1-2 teachers, 1 group, 2-3 subjects to test
2. **Weekly Hours Format**: Always use `Day:HH:MM-HH:MM` format
3. **Multiple Shifts**: Use semicolons: `Monday:08:00-12:00; Monday:13:00-17:00`
4. **Subject Names**: Use consistent names (case-sensitive!)
5. **Save Often**: Click Save after each change
6. **Backup Excel**: Copy `data/SchoolScheduler.xlsx` before major changes
7. **Test Autofill**: After adding teachers, test autofill with one group first
8. **Check Conflicts**: Review teacher schedules to ensure no conflicts

## Advanced Usage

### Custom Colors
Colors are auto-generated based on subject name. Same subject = same color.

### Import/Export Excel
- **Export**: All data is already in `data/SchoolScheduler.xlsx`
- **Import**: Replace the Excel file and refresh the app
- **Backup**: Copy the Excel file regularly

### Multiple Locations
If you need separate schedules for different buildings:
1. Create separate groups: "Building A - Grade 1", "Building B - Grade 1"
2. Or run multiple instances on different ports

### API Integration
The app exposes REST APIs at:
- `/api/teachers` - Teacher CRUD
- `/api/groups` - Group CRUD
- `/api/subjects` - Subject CRUD
- `/api/schedules/autofill` - Generate schedule
- `/api/schedules/group/<name>` - Get group schedule
- `/api/schedules/teacher/<name>` - Get teacher schedule

## Support

If you encounter issues not covered here:
1. Check the main README.md file
2. Review the AUTO_GENERATION_PROMPT.md for technical details
3. Check the Excel file format in `data/SchoolScheduler.xlsx`
4. Verify Python packages are installed: `pip list`

## License

MIT License - Free to use and modify!

---

**Happy Scheduling! 📅✨**

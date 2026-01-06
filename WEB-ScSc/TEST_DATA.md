# Test Data Guide

This file contains sample data you can use to quickly test the School Scheduler application.

## Quick Test Scenario

### Teachers
1. **John Smith**
   - Subjects: Math (5h, Group A), Physics (3h, Group A)
   - Weekly Hours: `Monday:08:00-15:00; Tuesday:08:00-15:00; Wednesday:08:00-15:00`

2. **Sarah Johnson**
   - Subjects: English (4h, Group A), History (3h, Group A)
   - Weekly Hours: `Monday:09:00-16:00; Tuesday:09:00-16:00; Thursday:09:00-16:00`

3. **Michael Brown**
   - Subjects: Science (4h, Group A), Biology (2h, Group A)
   - Weekly Hours: `Tuesday:08:00-14:00; Wednesday:08:00-14:00; Thursday:08:00-14:00`

### Groups
- Group A
- Group B (optional)

### Subjects for Group A
1. Math - 5 hours/week
2. Physics - 3 hours/week
3. English - 4 hours/week
4. History - 3 hours/week
5. Science - 4 hours/week
6. Biology - 2 hours/week

**Total**: 21 hours/week across 3 teachers

### Expected Result
After clicking **Autofill** for Group A:
- Should generate a complete schedule
- No conflicts (each teacher appears only once per time slot)
- Maximum 2 consecutive lessons of the same subject
- Maximum 3 lessons of the same subject per day

## Testing Steps

1. Start the application
2. Add the 3 teachers above
3. Add Group A
4. Add the 6 subjects above
5. Go to Group Scheduler
6. Select Group A
7. Click Autofill
8. Verify schedule is generated successfully
9. Go to Teacher Scheduler
10. Check each teacher's schedule for conflicts

## Advanced Test: Multiple Groups

### Add Group B with different schedule needs:
- Math - 4 hours/week (Teacher: John Smith)
- English - 3 hours/week (Teacher: Sarah Johnson)
- Science - 3 hours/week (Teacher: Michael Brown)

### Expected Behavior:
- Group A and Group B schedules should not conflict
- Teachers appear in both group schedules appropriately
- No teacher is double-booked

## Testing Constraints

### Test 1: Max Sequence Lessons = 2
1. Set configuration: Max Sequence Lessons = 2
2. Autofill Group A
3. Check schedule: No subject should appear 3+ times consecutively

### Test 2: Max Per Day = 3
1. Set configuration: Max Per Day = 3
2. Autofill Group A
3. Check schedule: No day should have more than 3 lessons of the same subject

### Test 3: Teacher Availability
1. Edit John Smith
2. Change Weekly Hours to: `Monday:08:00-10:00` (only 2 lessons)
3. Try to autofill Group A with Math (5 hours)
4. Should fail or place Math on other days with different teachers

## PDF Export Test

1. Generate schedule for Group A
2. Click "Print to PDF"
3. Verify PDF contains:
   - Title with group name
   - Complete schedule grid
   - Colored cells for lessons
   - Readable teacher names and subjects

## Multi-Language Test

1. Go to Configuration
2. Change GUI Language to עברית
3. Click Save
4. Verify:
   - Interface switches to Hebrew
   - Layout switches to RTL (right-to-left)
   - All buttons and labels are in Hebrew

5. Change to Русский
6. Verify Russian translation

## Performance Test

### Large Dataset:
- 10 teachers
- 5 groups
- 30 subjects
- Average 5 hours per subject = 150 total hours

**Expected**: Autofill should complete within 10-30 seconds depending on complexity.

## Common Test Failures

### "No teacher found for Math"
- **Cause**: Teacher doesn't have Math in their subjects list
- **Fix**: Edit teacher, add Math subject with Group A

### "Could not place all hours"
- **Cause**: Not enough teacher availability
- **Fix**: Increase teacher weekly hours or availability

### Schedule has gaps
- **Normal**: Autofill places lessons where possible, gaps are expected
- **Solution**: Manually fill gaps by clicking cells and adding lessons

## Automated Test Script (Future)

```python
# tests/test_autofill.py
def test_basic_autofill():
    # Setup: 3 teachers, 1 group, 6 subjects
    # Run: autofill
    # Assert: schedule has 21 lessons placed
    # Assert: no conflicts
    pass
```

## Success Criteria

✅ Application starts without errors
✅ Can add teachers, groups, subjects
✅ Autofill generates complete schedule
✅ No teacher conflicts in teacher scheduler
✅ PDF export works
✅ Language switching works
✅ Excel file saves and loads correctly
✅ Manual lesson editing works
✅ Schedule clear function works

---

**Note**: After testing, you can click "Clear All Schedules" to reset and test again, or delete all data and start fresh.

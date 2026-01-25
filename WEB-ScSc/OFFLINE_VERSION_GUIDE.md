# School Scheduler - Offline Version Guide

## 🎯 Overview

This is a complete offline version of School Scheduler that works **without internet connection** on Windows computers (7, 8, 10, 11). No Python installation required!

---

## 📦 For Developers: Building the Offline Version

### Prerequisites
- Python 3.7 or higher installed
- Internet connection (only for building, not for running)

### Build Steps

1. **Navigate to the project folder**
   ```
   cd WEB-ScSc
   ```

2. **Run the build script**
   
   Simply double-click: `BUILD_OFFLINE.bat`
   
   OR run from command line:
   ```
   BUILD_OFFLINE.bat
   ```

3. **Wait for the build to complete** (3-5 minutes)
   - Downloads offline dependencies (Bootstrap, jQuery)
   - Installs PyInstaller
   - Packages the application into a standalone executable

4. **Find the result**
   - Location: `dist\SchoolScheduler\`
   - This folder contains everything needed

5. **Distribute**
   - Zip the `dist\SchoolScheduler` folder
   - Share the ZIP file with users
   - That's it!

---

## 👥 For End Users: Using the Offline Version

### Installation (First Time)

1. **Download and extract**
   - Download the `SchoolScheduler.zip` file
   - Extract it to any folder (e.g., Desktop, Documents)
   - Example: `C:\Users\YourName\Desktop\SchoolScheduler\`

2. **That's all!** No installation required.

### Running the Application

1. **Start the application**
   - Open the extracted folder
   - Double-click: `START_HERE.bat`
   
2. **What happens next**
   - A command window opens (keep it open!)
   - Your default browser opens automatically
   - You see the School Scheduler login page

3. **Access the application**
   - Default URL: `http://127.0.0.1:5000`
   - If browser doesn't open automatically, open it and type the URL above

### Stopping the Application

**Method 1:** Close the command window (black window)
**Method 2:** Press `Ctrl+C` in the command window

---

## 💾 Your Data

### Where is it stored?
- All data is in: `data\users\[your-username]\schedule_data.xlsx`
- This is a regular Excel file you can backup

### Backing up your data
1. Copy the entire `SchoolScheduler` folder to a safe location
2. OR just copy the `data` folder

### Restoring data
1. Extract the application to a new location
2. Copy your backed up `data` folder
3. Overwrite the existing `data` folder

---

## 🔧 Troubleshooting

### Problem: Application doesn't start

**Possible causes:**
1. Port 5000 is already in use
2. Antivirus blocking the .exe file
3. Insufficient permissions

**Solutions:**
- Close other applications that might use port 5000
- Add the application to antivirus exceptions
- Right-click `START_HERE.bat` and select "Run as Administrator"

### Problem: Browser doesn't open automatically

**Solution:**
- Manually open your browser (Chrome, Edge, Firefox)
- Go to: `http://127.0.0.1:5000`

### Problem: "Port already in use" error

**Solution:**
- Close any other instance of the application
- Check Task Manager for `SchoolScheduler.exe` processes
- End those processes and try again

### Problem: Can't save data

**Solution:**
- Make sure you have write permissions in the folder
- Don't run from a read-only location (like some USB drives)
- Run as Administrator

---

## 📋 System Requirements

### Minimum Requirements
- **OS:** Windows 7, 8, 10, or 11
- **RAM:** 512 MB
- **Disk Space:** 100 MB
- **Internet:** NOT required (fully offline)

### Recommended
- **OS:** Windows 10 or 11
- **RAM:** 1 GB or more
- **Disk Space:** 200 MB (for data growth)

---

## 🌐 Multi-Language Support

The application supports:
- English
- Hebrew (עברית) - with RTL support
- Russian (Русский)

Language can be changed in the application settings.

---

## ⚡ Features

All features from the online version are available offline:

- ✅ Teacher management
- ✅ Group management
- ✅ Subject management
- ✅ Automatic schedule generation
- ✅ Manual schedule editing
- ✅ Conflict detection
- ✅ Excel import/export
- ✅ PDF export
- ✅ Multi-language interface
- ✅ User authentication
- ✅ Data persistence

---

## 🔒 Security & Privacy

- All data stays on your computer
- No internet connection used
- No data sent anywhere
- No tracking or analytics
- Complete privacy

---

## 📞 Support

### For technical issues:
- GitHub: https://github.com/yoavmoiseev/school-scheduler
- Report issues in the GitHub repository

### For questions:
- Check this README first
- Review the troubleshooting section
- Open an issue on GitHub

---

## 📄 License & Credits

Built with:
- Python & Flask (Backend)
- Bootstrap 5 (UI)
- jQuery (Frontend)
- PyInstaller (Packaging)

Compatible with Windows 7/8/10/11

---

## 🔄 Updating

When a new version is released:

1. Download the new ZIP file
2. Extract to a NEW folder
3. Copy your `data` folder from the old version
4. Paste it into the new version folder
5. Run `START_HERE.bat` from the new version

---

**Happy Scheduling! 📅**

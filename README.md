# 🎓 School Auto-Scheduler

**Intelligent school timetable generator with automatic conflict detection and optimization.**

A powerful web-based system for creating school schedules, managing teachers, classes, and constraints — with support for automatic, manual, and hybrid scheduling.

---

## 🚀 Live Demo

🌐 [https://sc.yamsoft.org](https://sc.yamsoft.org)

---

## ✨ Key Features

### 🤖 Smart Scheduling Modes

* **Automatic (Autofill)** – generate full schedules in one click
* **Manual (Guided)** – choose only valid options (no conflicts)
* **Hybrid** – fix important lessons first, auto-fill the rest

### 👨‍🏫 Teacher Management

* Assign subjects and weekly hours
* Define availability using time ranges or lesson slots
* Prevent double-booking automatically

### 🔍 Conflict Detection

* Real-time validation
* Prevents invalid assignments
* Clear error messages

### 👥 Groups & Subgroups

* Manage classes and student groups
* Split classes into subgroups (levels)
* Parallel teaching with multiple teachers

### 🔗 United Groups (Advanced)

* Merge multiple classes into one lesson
* Automatically synchronize schedules across groups

### 🏫 Rooms & Locations

* Assign classrooms, labs, halls
* Track room occupancy in real time

### ⚙️ Flexible Constraints

* Max consecutive lessons
* Max lessons per day
* Teacher workload limits

### 📊 Multiple Views

* Schedule by **class (group)**
* Schedule by **teacher**
* Interactive grid editing

### 🌍 Multilingual

* English
* Hebrew (RTL)
* Russian

### 📄 Export Options

* PDF
* Excel
* Print-ready

---

## 💻 Tech Stack

* **Backend:** Flask, Flask-SocketIO
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Realtime:** WebSocket
* **Algorithm:** Constraint-based scheduling with backtracking

---

## 🧠 How It Works

The scheduler uses a constraint-based algorithm:

1. Collect teachers, subjects, and groups
2. Build availability map
3. Assign lessons to time slots
4. Validate constraints
5. Retry with different combinations if needed

**Priorities:**

1. No conflicts
2. Complete schedule
3. Respect constraints
4. Balanced distribution

---

## ⚡ Quick Start

### 1. Open the system

👉 [https://sc.yamsoft.org](https://sc.yamsoft.org)

### 2. Create account

* Username + password
* Optional email

### 3. Configure system

* Lessons per day
* Constraints

### 4. Add data

* Teachers
* Groups
* Subjects

### 5. Generate schedule

Click **Autofill** 🚀

---

## 📁 Project Structure

```
project/
├── server.py
├── scheduler_engine.py
├── templates/
├── static/
├── data/
└── exports/
```

---

## 📊 Example Use Case

**Grade 10-A schedule:**

* Math – 5 hours
* English – 4 hours
* Physics – 3 hours

Teachers:

* John → Math, Physics
* Sarah → English
* David → Chemistry

➡️ Click **Autofill** → system generates full schedule automatically.

---

## ⚙️ Constraints

### Hard Constraints (must be satisfied)

* No teacher double-booking
* Teacher availability respected
* Correct subject-teacher mapping
* Required weekly hours

### Soft Constraints

* Even distribution
* Teacher preferences
* Subject placement

---

## 📦 Offline Version

This project also supports **offline deployment**:

### Advantages

* 🔒 Full data privacy
* 🌐 No internet required
* ⚡ Faster performance
* 🏫 Ideal for schools

### Best for:

* Religious / Haredi schools
* Remote locations
* Strict data environments

---

## 📤 Export

* 📄 PDF schedules
* 📊 Excel (full data + schedules)
* 🖨️ Print-ready layout

---

## 🧩 Advanced Features

### 🔗 United Groups

Combine multiple classes into one lesson automatically.

### 👥 Subgroups

Split a class into multiple levels taught simultaneously.

### 🏫 Rooms

Assign and track classroom usage in real time.

---

## 🛠️ Troubleshooting

**Autofill fails?**

* Check teacher availability
* Ensure every subject has a teacher
* Reduce constraints

**Slow performance?**

* Reduce retries
* Relax constraints
* Add more availability

---

## 💡 Best Practices

* Start with **simple data**
* Use **example datasets**
* Ensure:

  ```
  total required hours ≤ total available teacher hours
  ```
* Iterate and refine

---

## 👤 Author

**Yoav Moiseev**
YamSoft – Educational Software Solutions

🌐 [https://www.yamsoft.org](https://www.yamsoft.org)

---

## 📄 License

MIT License – free for educational use.

---

## 🤝 Support

* Website: [https://www.yamsoft.org](https://www.yamsoft.org)
* Email: [support@yamsoft.org](mailto:support@yamsoft.org)

---

## ⭐ Final Note

This project is designed to **replace hours (or days) of manual scheduling work** with a fast, intelligent, and flexible system.



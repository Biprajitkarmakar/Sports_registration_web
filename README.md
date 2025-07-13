# 🏫 Student Sports Registration Website – Kaliganj Anchal

This is a freelance project built for Kaliganj Anchal Government Primary Schools, West Bengal, to simplify the **student registration process** for upcoming school sports events. The web application allows schools to register students under different sports categories, grouped by gender and age groups, with admin features for efficient data management.

---

## 🔧 Features

- 📝 Student Registration Form with:
  - School name, group, gender, and sport selection
  - Student image upload
  - Validation and confirmation screen
- 📦 Session-based data storage before final submission
- 🧾 PDF Generation after confirmation (Downloadable on Thank You Page)
- 🖥️ Admin Panel with:
  - Search, Edit, Delete student entries
  - Add chest number
  - Filter by school, sport, gender, or group
  - Download all student data as PDF
  - Export data to Excel
  - Student count analytics by group/sport/school
- 🔒 Duplicate registration prevention
- 🌐 Responsive and simple UI using Bootstrap

---

## 🧰 Tools & Technologies

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, Bootstrap 4
- **Database**: SQLite (Default with Django)
- **Image Handling**: `MEDIA_ROOT` with temp and permanent folders
- **PDF Generation**: `xhtml2pdf` and custom HTML template
- **Excel Export**: `pandas`, `openpyxl`
- **Version Control**: Git & GitHub

---

## 📁 Folder Structure (Main Parts)

sports_registration/
├── students/
│ ├── migrations/
│ ├── templates/
│ │ └── students/
│ ├── static/
│ ├── views.py
│ ├── models.py
│ ├── urls.py
│ └── forms.py
├── media/
│ ├── temp/
│ ├── students/
│ └── pdfs/
├── sports_registration/
│ ├── settings.py
│ ├── urls.py
├── manage.py
└── README.md

📄 PDF Example
A downloadable registration PDF is generated after successful student confirmation. It includes all details with official formatting and image.

🙏 Acknowledgment
Grateful to Kaliganj Anchal All Govt Primary Schools for trusting me with this project. This is my first freelance project and I'm proud to contribute to student sports management digitally.

🧑‍💻 Developed By
Biprajit Karmakar
Email: karmakarbiprojit@gmail.com
GitHub: github.com/Biprajitkarmakar

📌 License
This project is created for educational and internal administrative use. Please contact the author before reuse.

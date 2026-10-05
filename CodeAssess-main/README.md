# 🚀 CodeAssess - AI-Powered Coding Assessment Platform

CodeAssess is an intelligent online coding assessment platform designed to evaluate programming solutions beyond correctness. It combines automated code execution with AI-powered analysis to provide detailed feedback on code quality, performance, and best practices.

Built as a full-stack application, CodeAssess helps students, developers, and recruiters assess coding skills through real-time evaluation and comprehensive AI-generated reports.

---

## ✨ Features

### 🧑‍💻 Secure User Authentication
- Email & Password Authentication using Firebase
- User Registration & Login
- Password Reset
- Protected Dashboard

### 📚 Coding Problems
- Browse coding problems by difficulty
- View detailed problem descriptions
- Sample test cases and constraints
- Hidden test cases for fair evaluation

### 💻 Interactive Coding Workspace
- Monaco Code Editor (VS Code-like experience)
- Multiple Programming Language Support
- Custom Input Execution
- Real-time Code Editing

### ⚡ Automated Code Execution
- Judge0 Integration
- Compile & Run Programs
- Runtime & Memory Usage
- Compilation Error Handling
- Runtime Error Detection

### 🤖 AI Code Review
Powered by Google Gemini AI

- Code Quality Analysis
- Readability Evaluation
- Coding Standards Assessment
- Best Practice Suggestions
- Maintainability Review
- Naming Convention Analysis
- Optimization Suggestions

### 📈 Performance Analysis
- Time Complexity Estimation
- Space Complexity Estimation
- Execution Statistics
- Performance Insights

### 📖 Code Explanation
- AI-generated explanation of solution logic
- Beginner-friendly walkthrough
- Step-by-step understanding

### 🔄 Professional Code Improvement
- AI-generated optimized solution
- Cleaner implementation
- Industry-standard coding practices
- Improvement explanations

### 📊 Dashboard
- Submission History
- Performance Tracking
- Solved Problems
- Overall Progress

### 🔐 Admin Panel
- Problem Management
- Submission Monitoring
- Analytics Dashboard

---

# 🏗️ System Architecture

```
React Frontend
        │
        ▼
Flask REST API
        │
        ├────────► Firebase Authentication
        │
        ├────────► Firestore Database
        │
        ├────────► Judge0 API
        │
        └────────► Google Gemini AI
```

---

# 🛠️ Tech Stack

## Frontend

- React.js
- Vite
- Tailwind CSS
- Monaco Editor
- React Router
- Firebase Authentication

## Backend

- Python
- Flask
- Flask-CORS

## Database

- Firebase Firestore

## AI

- Google Gemini 1.5 Flash

## Code Execution

- Judge0 API

## Tools

- Git
- GitHub
- VS Code

---

# 📂 Project Structure

```
CodeAssess/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── routes/
│   ├── services/
│   ├── middleware/
│   ├── app.py
│   └── requirements.txt
│
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/sheikjeenath/code-assess.git
```

---

## Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Backend

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt

python app.py
```

---

# 🔑 Environment Variables

### Frontend

```
VITE_FIREBASE_API_KEY=
VITE_FIREBASE_AUTH_DOMAIN=
VITE_FIREBASE_PROJECT_ID=
VITE_FIREBASE_STORAGE_BUCKET=
VITE_FIREBASE_MESSAGING_SENDER_ID=
VITE_FIREBASE_APP_ID=
```

### Backend

```
PORT=5000

FIREBASE_SERVICE_ACCOUNT_PATH=

JUDGE0_API_URL=

JUDGE0_API_KEY=

GEMINI_API_KEY=
```

---

# 📸 Screenshots

> Add screenshots here after deployment.

- Landing Page
- Login
- Dashboard
- Problem List
- Coding Workspace
- AI Report

---

# 🚀 Future Enhancements

- AI Interview Feedback
- Flowchart Visualization
- Code Similarity Detection
- Plagiarism Detection
- Leaderboard
- Contest Mode
- Company-specific Coding Assessments
- Resume-based Personalized Coding Recommendations

---

# 🎯 Learning Outcomes

This project strengthened my knowledge of:

- Full Stack Development
- REST API Design
- Firebase Authentication
- Firestore Database
- AI Integration using Gemini
- Judge0 API Integration
- React Application Development
- Flask Backend Development
- Git & GitHub
- Software Architecture

---

# 👨‍💻 Author

**Sheik Jeenath Unnisa Begum**

GitHub:
https://github.com/sheikjeenath


## ⭐ If you found this project interesting, consider giving it a star!

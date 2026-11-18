# 🎯 Interview Prep Assistant

An AI-powered Interview Preparation Assistant.

The application generates role-specific mock interview questions, evaluates candidate answers using AI, provides detailed feedback with scores, and displays an overall interview summary.

---

## 🚀 Features

- Generate interview questions based on:
  - Target Role
  - Tech Stack
  - Resume Summary (Optional)
- Adaptive questions that change difficulty after each answer
- Explainable answer evaluation with correctness, depth, communication and relevance rubrics
- Personalized feedback
- Ideal answer points
- Interview summary with average score
- Skill-gap analysis and a personalised practice plan
- Account-based interview history
- PDF résumé text extraction for personalised questions
- Human-review dashboard to compare AI and reviewer scores
- Responsive React frontend
- FastAPI backend
- SQLite database

---

## 🛠 Tech Stack

### Frontend
- React
- Vite
- JavaScript
- CSS

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite

### AI Model
- Groq API
- Model: `openai/gpt-oss-120b`

---

## 📂 Project Structure

```
Interview-Prep-Assistant
│
├── backend
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── interview_service.py
│   ├── grok_service.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend
│   ├── src
│   │   ├── components
│   │   ├── api
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
│
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/SSv3611u/LLM-POWERED-INTELLIGENT-INTERVIEW-PREPARATION-ASSISTANT.git
cd interview-prep-assistant
```

---

## 2. Backend Setup

```bash
cd backend

python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file inside the **backend** folder.

```env
GROQ_API_KEY=your_api_key
GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions
GROQ_MODEL=openai/gpt-oss-120b
AUTH_SECRET=replace-with-a-long-random-secret-before-deployment
```

### Start Backend

```bash
uvicorn main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

## 3. Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

# 📡 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/sessions` | Create a new interview session |
| GET | `/api/sessions/{id}/questions` | Retrieve interview questions |
| POST | `/api/sessions/{id}/questions/{questionId}/answers` | Submit an answer for evaluation |
| GET | `/api/sessions/{id}/summary` | Retrieve interview summary |
| POST | `/api/auth/register` | Create an account |
| POST | `/api/auth/login` | Sign in |
| POST | `/api/resume/extract` | Extract text from a PDF résumé |
| GET | `/api/sessions` | Retrieve the signed-in user's history |
| POST | `/api/evaluations` | Save a human score for an answer |
| GET | `/api/evaluations/dashboard` | Retrieve AI versus human score metrics |

---

# 🗄 Database

The project uses **SQLite**.

A database file is automatically created when the backend starts.

```
interview_prep.db
```

Delete this file anytime if you want to reset all interview sessions.

---

# 🎯 Future Enhancements

- Resume PDF Upload
- Voice-based Interviews
- Speech-to-Text Integration
- Authentication System
- Performance Analytics Dashboard
- Interview History
- Dark Mode

---

# 👨‍💻 Developed By

**Vinjam Balakrishna**
**Sugali Chaitanya**
**Chenna Sai Saketh Vardhan**


Computer Science & Engineering

CVR College of Engineering

Major Project (2026–27)

# 🎓 Mentora — AI-Powered Course Recommendation Web App

> **Find your way into AI.**  
> Mentora is a modern, editorial AI course recommendation web app indexing 250+ curated courses from DeepLearning.AI, Stanford University, MIT, Google Cloud, fast.ai, Coursera, Udacity, and edX.

---

## ✨ Features

### 🟢 Phase 1: MVP Core
- **Curated Database**: 250+ pre-seeded AI courses with detailed metadata (title, platform, instructor, link, price, level, duration, topic, language, summary, what you'll learn, prerequisites, ratings, freshness score).
- **Multi-Criteria Search & Filtering**: Instant filter pills by:
  - **Topic**: LLMs, Generative AI, Computer Vision, MLOps, NLP, Prompt Engineering, Machine Learning.
  - **Level**: Beginner, Intermediate, Advanced.
  - **Price**: Free vs. Paid.
  - **Platform**: Coursera, DeepLearning.AI, Udacity, fast.ai, Google, Stanford, MIT, Hugging Face, Microsoft.
  - **Duration**: Short (<5h), Medium (5-20h), Comprehensive (>20h).
- **Course Detail View (`/course/<id>`)**: In-depth breakdown with prerequisites, syllabus bullet points, and direct official platform links.
- **Personal Saved Bookmarks (`/bookmarks`)**: One-click real-time AJAX bookmark toggling.
- **User Authentication (`/login`, `/register`, `/logout`)**: Password hashing and Google OAuth sign-in interface.

### 🤖 Phase 2: AI Features
- **AI Course Advisor Chatbot (`/ai-advisor`)**: Interactive career counselor powered by **Google Gemini API** (`google-generativeai`) to match user background, weekly time budget, and budget constraints with courses.
- **Learning Path Generator (`/learning-path`)**: Multi-step sequential roadmap generator for goals like *"Become an ML Engineer"* or *"Build LLM Chatbots"*.
- **Free Alternative Finder**: Automatically highlights 100% free alternative courses whenever a user views a paid course detail page.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12, Flask, Flask-SQLAlchemy, Flask-Login
- **Frontend**: HTML5, Tailwind CSS (CDN), Jinja2 Templates, Vanilla JS (AJAX)
- **Database**: SQLite (default) / PostgreSQL compatible
- **AI Integration**: Google Gemini API (`google-generativeai`)
- **Styling & Fonts**: Custom warm cream palette (`#FBF9F4`), deep forest green accents (`#1B3A2B`), Playfair Display & Plus Jakarta Sans typography.

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Mentora.git
cd Mentora
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Launch Mentora (Single Command)
```bash
python run.py
```
> **Note**: `run.py` automatically initializes the database, populates 250 AI courses on first launch, and opens your default browser directly to `http://127.0.0.1:5000`!

---

## 🔑 Environment Variables (Optional Gemini API)

To enable live AI responses in the Advisor Chatbot and Learning Path Generator, set your Google Gemini API key:

```env
# .env
SECRET_KEY=mentora-secret-key-2026-ai-recommendations
DATABASE_URL=sqlite:///mentora.db
GEMINI_API_KEY=your_google_gemini_api_key_here
```

On Windows PowerShell:
```powershell
$env:GEMINI_API_KEY="your_actual_gemini_api_key"
python run.py
```

---

## 📂 Project Structure

```
Mentora/
├── app.py                  # Main Flask application entry point & routes
├── run.py                  # Master launcher script (Auto-seeds DB & opens browser)
├── start_mentora.bat       # Windows double-clickable launcher
├── config.py               # Database and Gemini configuration
├── models.py               # SQLAlchemy Database Models (Course, User, Bookmark)
├── ai_advisor.py           # Gemini API Advisor Chat & Learning Path engine
├── seed_courses.py         # 250 Curated AI Course Dataset populator
├── init_db.py              # Manual Database trigger script
├── requirements.txt        # Python package dependencies
├── .gitignore              # Ignored files for git
├── static/
│   └── css/ style.css      # Custom styles
└── templates/
    ├── base.html           # Base layout template with header & footer
    ├── index.html          # Main course catalog & pill filter bar
    ├── course_detail.html  # Course detail page & Free Alternative Finder
    ├── ai_advisor.html     # Interactive AI Advisor Chat UI
    ├── learning_path.html  # Career Roadmap Generator UI
    ├── bookmarks.html      # Saved courses list
    ├── login.html          # Login page
    └── register.html       # User registration page
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

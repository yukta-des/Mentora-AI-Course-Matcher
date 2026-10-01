# 🎓 Mentora — AI-Powered Course Recommendation Web App

> **Find your way into AI.**  
> Mentora is a modern, editorial AI course recommendation web app indexing 250+ curated courses from DeepLearning.AI, Stanford University, MIT, Google Cloud, fast.ai, Coursera, Udacity, and edX.

---

## ✨ Features

### 🟢 Phase 1: MVP Core
- **Curated Database**: 250+ pre-seeded AI courses with detailed metadata 
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

- **Backend**: Python, Flask
- **Frontend**: HTML5, Tailwind CSS, Jinja2 Templates, Vanilla JS
- **Database**: SQLite (default) / PostgreSQL compatible
- **AI Integration**: Google Gemini API (`google-generativeai`)
- **Styling & Fonts**: Custom warm cream palette (`#FBF9F4`), deep forest green accents (`#1B3A2B`), Playfair Display & Plus Jakarta Sans typography.

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


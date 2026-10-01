import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Course, Bookmark
from ai_advisor import chat_with_advisor, generate_learning_path_roadmap

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Helper Functions ---
def get_user_bookmark_ids():
    if current_user.is_authenticated:
        return set(b.course_id for b in Bookmark.query.filter_by(user_id=current_user.id).all())
    return set()

# --- Phase 1 Routes ---

@app.route('/')
def index():
    search_query = request.args.get('q', '').strip()
    topic = request.args.get('topic', '')
    level = request.args.get('level', '')
    price = request.args.get('price', '')
    platform = request.args.get('platform', '')
    duration = request.args.get('duration', '')

    query = Course.query

    if search_query:
        query = query.filter(
            (Course.title.ilike(f'%{search_query}%')) |
            (Course.summary.ilike(f'%{search_query}%')) |
            (Course.topic.ilike(f'%{search_query}%')) |
            (Course.platform.ilike(f'%{search_query}%'))
        )

    if topic:
        query = query.filter(Course.topic == topic)

    if level:
        query = query.filter(Course.level == level)

    if price == 'free':
        query = query.filter(Course.is_free == True)
    elif price == 'paid':
        query = query.filter(Course.is_free == False)

    if platform:
        query = query.filter(Course.platform == platform)

    if duration == 'short':
        query = query.filter(Course.duration_hours <= 5)
    elif duration == 'medium':
        query = query.filter(Course.duration_hours > 5, Course.duration_hours <= 20)
    elif duration == 'long':
        query = query.filter(Course.duration_hours > 20)

    courses = query.order_by(Course.freshness_score.desc(), Course.rating.desc()).all()
    user_bookmark_ids = get_user_bookmark_ids()

    all_topics = db.session.query(Course.topic).distinct().all()
    topics_list = sorted([t[0] for t in all_topics if t[0]])
    
    all_platforms = db.session.query(Course.platform).distinct().all()
    platforms_list = sorted([p[0] for p in all_platforms if p[0]])

    return render_template(
        'index.html',
        courses=courses,
        user_bookmark_ids=user_bookmark_ids,
        topics=topics_list,
        platforms=platforms_list,
        current_topic=topic,
        current_level=level,
        current_price=price,
        current_platform=platform,
        current_duration=duration,
        search_query=search_query
    )


@app.route('/course/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    user_bookmark_ids = get_user_bookmark_ids()
    is_bookmarked = course_id in user_bookmark_ids

    # Find free alternatives if this course is paid
    free_alternatives = []
    if not course.is_free:
        free_alternatives = Course.query.filter(
            Course.topic == course.topic,
            Course.is_free == True,
            Course.id != course.id
        ).limit(3).all()

    # Related courses in same topic
    related_courses = Course.query.filter(
        Course.topic == course.topic,
        Course.id != course.id
    ).limit(3).all()

    return render_template(
        'course_detail.html',
        course=course,
        is_bookmarked=is_bookmarked,
        related_courses=related_courses,
        free_alternatives=free_alternatives,
        user_bookmark_ids=user_bookmark_ids
    )


@app.route('/api/courses')
def api_courses():
    search_query = request.args.get('q', '').strip()
    topic = request.args.get('topic', '')
    level = request.args.get('level', '')
    price = request.args.get('price', '')
    platform = request.args.get('platform', '')
    duration = request.args.get('duration', '')

    query = Course.query

    if search_query:
        query = query.filter(
            (Course.title.ilike(f'%{search_query}%')) |
            (Course.summary.ilike(f'%{search_query}%')) |
            (Course.topic.ilike(f'%{search_query}%')) |
            (Course.platform.ilike(f'%{search_query}%'))
        )

    if topic:
        query = query.filter(Course.topic == topic)

    if level:
        query = query.filter(Course.level == level)

    if price == 'free':
        query = query.filter(Course.is_free == True)
    elif price == 'paid':
        query = query.filter(Course.is_free == False)

    if platform:
        query = query.filter(Course.platform == platform)

    if duration == 'short':
        query = query.filter(Course.duration_hours <= 5)
    elif duration == 'medium':
        query = query.filter(Course.duration_hours > 5, Course.duration_hours <= 20)
    elif duration == 'long':
        query = query.filter(Course.duration_hours > 20)

    courses = query.order_by(Course.freshness_score.desc()).all()
    user_bookmark_ids = get_user_bookmark_ids()

    return jsonify({
        'status': 'success',
        'count': len(courses),
        'courses': [c.to_dict(user_bookmarked=(c.id in user_bookmark_ids)) for c in courses]
    })


@app.route('/bookmarks')
def bookmarks():
    if not current_user.is_authenticated:
        flash('Please sign in to view your saved bookmarks.', 'info')
        return redirect(url_for('login'))

    user_bookmarks = Bookmark.query.filter_by(user_id=current_user.id).order_by(Bookmark.created_at.desc()).all()
    bookmarked_courses = [b.course for b in user_bookmarks]
    user_bookmark_ids = set(c.id for c in bookmarked_courses)

    return render_template(
        'bookmarks.html',
        courses=bookmarked_courses,
        user_bookmark_ids=user_bookmark_ids
    )


@app.route('/api/bookmark/toggle', methods=['POST'])
def toggle_bookmark():
    if not current_user.is_authenticated:
        return jsonify({'status': 'error', 'message': 'Authentication required', 'redirect': url_for('login')}), 401

    data = request.get_json() or {}
    course_id = data.get('course_id')

    if not course_id:
        return jsonify({'status': 'error', 'message': 'Course ID required'}), 400

    course = Course.query.get(course_id)
    if not course:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404

    existing = Bookmark.query.filter_by(user_id=current_user.id, course_id=course.id).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({'status': 'success', 'bookmarked': False, 'message': 'Removed from saved courses'})
    else:
        new_bookmark = Bookmark(user_id=current_user.id, course_id=course.id)
        db.session.add(new_bookmark)
        db.session.commit()
        return jsonify({'status': 'success', 'bookmarked': True, 'message': 'Saved to personal list'})


# --- Phase 2 AI Features Routes ---

@app.route('/ai-advisor', methods=['GET', 'POST'])
def ai_advisor():
    if request.method == 'POST':
        data = request.get_json() or {}
        user_message = data.get('message', '').strip()
        history = data.get('history', [])

        if not user_message:
            return jsonify({'status': 'error', 'reply': 'Please type a question or goal.'}), 400

        all_courses = Course.query.all()
        response = chat_with_advisor(user_message, history, all_courses)
        return jsonify(response)

    return render_template('ai_advisor.html')


@app.route('/learning-path', methods=['GET', 'POST'])
def learning_path():
    goal = request.args.get('goal', 'Become an ML Engineer').strip()
    
    if request.method == 'POST':
        data = request.get_json() or {}
        goal = data.get('goal', goal).strip()

    all_courses = Course.query.all()
    roadmap_data = generate_learning_path_roadmap(goal, all_courses)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        return jsonify(roadmap_data)

    user_bookmark_ids = get_user_bookmark_ids()
    return render_template(
        'learning_path.html',
        roadmap=roadmap_data,
        goal=goal,
        user_bookmark_ids=user_bookmark_ids
    )


# --- Auth Routes ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Welcome back to Mentora!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not name or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('register.html')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email already exists.', 'error')
            return render_template('register.html')

        hashed_pw = generate_password_hash(password, method='scrypt')
        new_user = User(name=name, email=email, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('Account created successfully! Welcome to Mentora.', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)

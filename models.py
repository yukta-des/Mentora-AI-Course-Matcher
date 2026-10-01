from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookmarks = db.relationship('Bookmark', backref='user', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name
        }


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    platform = db.Column(db.String(100), nullable=False) # e.g. Coursera, DeepLearning.AI, Udacity, edX, fast.ai, Google
    instructor = db.Column(db.String(100), nullable=True) # e.g. Andrew Ng, Stanford University
    link = db.Column(db.Text, nullable=False)
    price_usd = db.Column(db.Float, default=0.0)
    is_free = db.Column(db.Boolean, default=True)
    level = db.Column(db.String(50), nullable=False) # Beginner, Intermediate, Advanced
    duration_hours = db.Column(db.Integer, default=10) # Estimated hours
    topic = db.Column(db.String(100), nullable=False) # Generative AI, LLMs, Computer Vision, MLOps, NLP, Prompt Engineering
    language = db.Column(db.String(50), default='English')
    summary = db.Column(db.Text, nullable=False)
    what_you_will_learn_json = db.Column(db.Text, nullable=True) # Stored as JSON string
    prerequisites_json = db.Column(db.Text, nullable=True) # Stored as JSON string
    rating = db.Column(db.Float, default=4.8)
    freshness_score = db.Column(db.Float, default=0.95) # 0.0 to 1.0 (Freshness)
    image_url = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookmarks = db.relationship('Bookmark', backref='course', lazy=True, cascade="all, delete-orphan")

    @property
    def what_you_will_learn(self):
        if self.what_you_will_learn_json:
            try:
                return json.loads(self.what_you_will_learn_json)
            except Exception:
                return []
        return []

    @what_you_will_learn.setter
    def what_you_will_learn(self, value):
        self.what_you_will_learn_json = json.dumps(value)

    @property
    def prerequisites(self):
        if self.prerequisites_json:
            try:
                return json.loads(self.prerequisites_json)
            except Exception:
                return []
        return []

    @prerequisites.setter
    def prerequisites(self, value):
        self.prerequisites_json = json.dumps(value)

    def to_dict(self, user_bookmarked=False):
        return {
            'id': self.id,
            'title': self.title,
            'platform': self.platform,
            'instructor': self.instructor or self.platform,
            'link': self.link,
            'price_usd': self.price_usd,
            'is_free': self.is_free,
            'level': self.level,
            'duration_hours': self.duration_hours,
            'topic': self.topic,
            'language': self.language,
            'summary': self.summary,
            'what_you_will_learn': self.what_you_will_learn,
            'prerequisites': self.prerequisites,
            'rating': self.rating,
            'freshness_score': self.freshness_score,
            'image_url': self.image_url,
            'is_bookmarked': user_bookmarked
        }


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'course_id', name='_user_course_uc'),)

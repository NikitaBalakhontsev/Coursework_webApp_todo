import sqlalchemy as sa
import sqlalchemy.orm as so


from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash


from app import db


class User(db.Model):
    __tablename__ = 'users'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    categories: so.Mapped[list['Category']] = so.relationship('Category', back_populates='user', lazy='dynamic')
    tags: so.Mapped[list['Tag']] = so.relationship('Tag', back_populates='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def encrypt_password(self, password):
        """Encrypt password"""
        return generate_password_hash(password)

    def set_password(self, password):
        """Set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create(cls, username, email, password):
        """Create a new user"""
        existing_user = cls.query.filter_by(email=email).first()
        if existing_user:
            return None, 'Email already registered'

        new_user = cls(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return new_user, None

    @classmethod
    def login(cls, email, password):
        user = cls.get_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None

    @classmethod
    def get_all(cls):
        """Get all users"""
        return cls.query.all()

    @classmethod
    def get_by_id(cls, user_id):
        """Get a user by ID"""
        return cls.query.get(user_id)

    @classmethod
    def get_by_email(cls, email):
        """Get a user by email"""
        return cls.query.filter_by(email=email).first()

    @classmethod
    def delete(cls, user_id):
        """Delete a user by user_id"""
        user = cls.query.get(user_id)
        if not user:
            return None, "User not found"

        try:
            db.session.delete(user)
            db.session.commit()
            return user, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            }

    @classmethod
    def update(cls, user_id, data):
        """Update user information"""
        user = cls.query.get(user_id)
        if not user:
            return None, "User not found"

        for key, value in data.items():
            if hasattr(user, key):
                if key == 'password':
                    user.set_password(value)
                else:
                    setattr(user, key, value)

        try:
            db.session.commit()
            return user, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
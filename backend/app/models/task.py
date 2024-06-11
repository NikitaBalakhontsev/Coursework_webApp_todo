import sqlalchemy as sa
import sqlalchemy.orm as so

from typing import Optional
from datetime import datetime, timezone

from app import db
from .tag import Tag


class Task(db.Model):
    __tablename__ = 'tasks'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(120), nullable=False)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    due_date: so.Mapped[Optional[datetime.date]] = so.mapped_column(sa.Date)
    category_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('categories.id'), nullable=False)
    category: so.Mapped['Category'] = so.relationship('Category', back_populates='tasks')
    tags: so.Mapped[list['Tag']] = so.relationship('Tag', secondary='task_tag', back_populates='tasks')

    def __repr__(self):
        return f'<Task {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'timestamp': self.timestamp.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'category_id': self.category_id,
            'tags': [tag.to_dict() for tag in self.tags]
        }

    @staticmethod
    def create(title, description, due_date, category_id):
        if isinstance(due_date, str):
            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
        new_task = Task(title=title, description=description, due_date=due_date, category_id=category_id)
        db.session.add(new_task)
        db.session.commit()
        return new_task

    @staticmethod
    def get_all(category_id):
        tasks = Task.query.filter_by(category_id=category_id).all()
        return [task.to_dict() for task in tasks]

    @staticmethod
    def get_by_id(task_id, category_id):
        return Task.query.filter_by(id=task_id, category_id=category_id).first()

    @staticmethod
    def update(task_id, category_id, title, description, due_date):
        task = Task.get_by_id(task_id, category_id)
        if not task:
            return None, "Task not found"

        if isinstance(due_date, str):
            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()

        task.title = title
        task.description = description
        task.due_date = due_date
        db.session.commit()
        return task, None

    @staticmethod
    def delete(task_id, category_id):
        task = Task.get_by_id(task_id, category_id)
        if not task:
            return None, "Task not found"

        try:
            db.session.delete(task)
            db.session.commit()
            return task, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @classmethod
    def add_tag(cls, task_id, tag_id):
        task = cls.query.get(task_id)
        if not task:
            return None, "Task not found"

        tag = Tag.query.get(tag_id)
        if not tag:
            return None, "Tag not found"

        if tag not in task.tags:
            task.tags.append(tag)
            try:
                db.session.commit()
                return task, None
            except Exception as e:
                db.session.rollback()
                return None, str(e)
        return task, None

    @classmethod
    def remove_tag(cls, task_id, tag_id):
        task = cls.query.get(task_id)
        if not task:
            return None, "Task not found"

        tag = Tag.query.get(tag_id)
        if not tag:
            return None, "Tag not found"

        if tag in task.tags:
            task.tags.remove(tag)
            try:
                db.session.commit()
                return task, None
            except Exception as e:
                db.session.rollback()
                return None, str(e)
        return task, None
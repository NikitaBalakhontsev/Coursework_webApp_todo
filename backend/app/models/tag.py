import sqlalchemy as sa
import sqlalchemy.orm as so

from typing import Optional

from app import db

class Tag(db.Model):
    __tablename__ = 'tags'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=True)
    color: so.Mapped[str] = so.mapped_column(sa.String(7), nullable=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    user: so.Mapped['User'] = so.relationship('User', back_populates='tags')
    tasks: so.Mapped[list['Task']] = so.relationship('Task', secondary='task_tag', back_populates='tags')

    def __repr__(self):
        return f'<Tag {self.description}>'

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "color": self.color,
            "user_id": self.user_id
        }

    @staticmethod
    def create(cls, description: Optional[str], color: Optional[str], user_id: int):
        if not description and not color:
            return None, "Either description or color must be provided"
        new_tag = cls(description=description, color=color, user_id=user_id)
        db.session.add(new_tag)
        db.session.commit()
        return new_tag, None

    @staticmethod
    def get_all():
        tags = Tag.query.all()
        return [tag.to_dict() for tag in tags]

    @staticmethod
    def get_by_id(tag_id):
        return Tag.query.get(tag_id)

    @staticmethod
    def update(tag_id, description, color):
        tag = Tag.get_by_id(tag_id)
        if not tag:
            return None, "Tag not found"

        tag.description = description
        tag.color = color
        db.session.commit()
        return tag, None

    @staticmethod
    def delete(tag_id):
        tag = Tag.get_by_id(tag_id)
        if not tag:
            return None, "Tag not found"

        try:
            db.session.delete(tag)
            db.session.commit()
            return tag, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

task_tag = db.Table(
    'task_tag',
    db.Column('task_id', sa.Integer, sa.ForeignKey('tasks.id', name='fk_task_tag_task_id'), primary_key=True),
    db.Column('tag_id', sa.Integer, sa.ForeignKey('tags.id', name='fk_task_tag_tag_id'), primary_key=True)
)
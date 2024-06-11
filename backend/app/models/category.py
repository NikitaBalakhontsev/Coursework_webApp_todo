import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db


class Category(db.Model):
    __tablename__ = 'categories'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(80), nullable=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    user: so.Mapped['User'] = so.relationship('User', back_populates='categories')
    tasks: so.Mapped[list['Task']] = so.relationship('Task', back_populates='category', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Category {self.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id
        }
    @staticmethod
    def create(name, user_id):
        new_category = Category(name=name, user_id=user_id)
        db.session.add(new_category)
        db.session.commit()
        return new_category

    @staticmethod
    def get_all(user_id):
        categories = Category.query.filter_by(user_id=user_id).all()
        return [category.to_dict() for category in categories]

    @staticmethod
    def get_by_id(category_id, user_id):
        return Category.query.filter_by(id=category_id, user_id=user_id).first()

    @staticmethod
    def update(category_id, user_id, name):
        category = Category.get_by_id(category_id, user_id)
        if not category:
            return None, "Category not found"

        category.name = name
        db.session.commit()
        return category, None

    @staticmethod
    def delete(category_id, user_id):
        category = Category.get_by_id(category_id, user_id)
        if not category:
            return None, "Category not found"

        try:
            db.session.delete(category)
            db.session.commit()
            return category, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
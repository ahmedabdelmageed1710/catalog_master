from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    items = relationship('Item')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        if self.items:
            items = [r.serialize for r in self.items]
            return {
                'name': self.name,
                'id': self.id,
                'item': items,
            }
        else:
            return {
                'name': self.name,
                'id': self.id,
            }


class Item(Base):
    __tablename__ = 'item'

    title = Column(String(80), nullable=False, unique=True)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'title': self.title,
            'description': self.description,
            'id': self.id,
            'cat_id': self.category_id,
        }


engine = create_engine('sqlite:///itemcatalog.db')


Base.metadata.create_all(engine)

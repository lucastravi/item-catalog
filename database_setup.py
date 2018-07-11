#===================
# Handle the DB tables by creating classes
#===================

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine


Base = declarative_base()

# Creates the user table
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    email = Column(String(250), nullable = False)
    picture = Column(String(250))

# Creates the category table where the Pokemon types will be stored
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key = True)
    name = Column(String(255), nullable = False)
    # Relates the user logged in when the category was created with it
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="category")

    # Serealize the category table items into JSON
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name'          : self.name,
            'id'            : self.id
        }

# Creates a table items where the Pokemon will be stored
class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    date = Column(DateTime, nullable=False)
    description = Column(String(250))
    picture = Column(String(250))
    # Relate the items table with the category table by storing category.category.id as items.category_id
    category_id = Column(Integer, ForeignKey('category.id'))
    # If a category (type) is deleated, all the items (Pokemon) related to this category also are deleted
    category = relationship(Category, backref=backref('items', cascade='all, delete'))
    # Relates the user logged in when the item was created with it
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="items")

    # Serealize the items table items into JSON
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name'          : self.name,
            'id'            : self.id,
            'description'   : self.description,
            'picture'       : self.picture,
            'category'      : self.category.name
        }


engine = create_engine('sqlite:///itemcatalog.db')

Base.metadata.create_all(engine)

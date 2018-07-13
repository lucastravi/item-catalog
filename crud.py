# ===================
# CRUD helper functions
# ===================

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import *

# ===================
# Database handling
# ===================

# Connect to database
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

# Create session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# User-login Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except BaseException:
        return None

# ===================
# Pokedex CRUD handling
# ===================

# Find all categories


def findAllCategories():
    return session.query(Category).order_by(asc(Category.name))

# Find the 3 last items for the catalog page


def findAllLastItems():
    return session.query(Items).order_by(desc(Items.date)).limit(3)

# Find Items to a certain category


def findCategoryItems(category):
    return session.query(Items).filter_by(
        category=category).order_by(asc(Items.name)).all()

# Find a specific category


def findCategory(name):
    return session.query(Category).filter_by(name=name).one()

# Count the category items


def countItems(category):
    return session.query(Items).filter_by(category=category).count()

# Find an specific item


def findItem(name):
    return session.query(Items).filter_by(name=name).one()

# Add a new category


def newCategory(name):
    new_category = Category(name=name)
    session.add(new_category)
    session.commit()

# Edit an existing category


def editingCategory(name):
    edited_category = findCategory(name)
    session.add(edited_category)
    session.commit()

# Edit an existing category


def deletingCategory(name):
    deleted_category = findCategory(name)
    session.delete(deleted_category)
    session.commit()

# Add a new item


def newItem(name, date, description, picture, category, user_id):
    new_item = Items(name=name,
                     date=date,
                     description=description,
                     picture=picture,
                     category=findCategory(category),
                     user_id=user_id
                     )
    session.add(new_item)
    session.commit()

# Edit an existing item


def editingItem(name, date, description, picture, category):
    item = findItem(name)
    edited_item = findItem(name)
    edited_item = Items(name=name,
                        date=date,
                        description=description,
                        picture=picture,
                        category=findCategory(category)
                        )
    session.delete(item)
    session.add(edited_item)
    session.commit()

# Delete an existing item


def deletingItem(name):
    deleted_item = findItem(name)
    session.delete(deleted_item)
    session.commit()


# Find Categories sorted by ID


def sortCategoriesByID():
    return session.query(Category).order_by(asc(Category.id))
# Find Items to a certain category by id


def findCategoryItemsById(category_id):
    return session.query(Items).filter_by(
        category_id=category_id).all()

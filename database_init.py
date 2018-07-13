# ===================
# Populates the Application with some trainers, types and Pokemon
# ===================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from database_setup import *

engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Delete Categories if exisitng.
session.query(Category).delete()
# Delete Items if exisitng.
session.query(Items).delete()
# Delete Users if exisitng.
session.query(User).delete()

# Create Pokemon Trainers
User1 = User(
    name="Ash Ketchum",
    email="ashketchum@gmail.com.com",
    picture='https://vignette.wikia.nocookie.net/nintendo/images/0/0f/Ash_Ketchum.png/revision/latest?cb=20111019135611&path-prefix=en')
session.add(User1)
session.commit()

User2 = User(
    name="Brock",
    email="brock@gmail.com.com",
    picture='https://vignette.wikia.nocookie.net/pokemon/images/0/0a/Brock_OS_anime.png/revision/latest?cb=20150915072500')
session.add(User2)
session.commit()

User3 = User(
    name="Misty",
    email="misty@gmail.com.com",
    picture='https://vignette.wikia.nocookie.net/fantendo/images/4/4f/Misty_OS_2.png/revision/latest?cb=20151116233633')
session.add(User3)
session.commit()


# Create Pokemon Types
Category1 = Category(name="Eletric",
                     user_id=1)
session.add(Category1)
session.commit()

Category2 = Category(name="Fire",
                     user_id=1)
session.add(Category2)
session.commit()

Category3 = Category(name="Water",
                     user_id=3)
session.add(Category3)
session.commit()

Category4 = Category(name="Grass",
                     user_id=1)
session.add(Category4)
session.commit()

Category5 = Category(name="Rock",
                     user_id=2)
session.add(Category5)
session.commit()

Category6 = Category(name="Normal",
                     user_id=1)
session.add(Category6)
session.commit()

Category7 = Category(name="Fairy",
                     user_id=3)
session.add(Category7)
session.commit()

Category8 = Category(name="Flying",
                     user_id=1)
session.add(Category8)
session.commit()

# Populate the Pokedex DB with some Pokemon
Item1 = Items(
    name="Pikachu",
    date=datetime.datetime.now(),
    description="It evolves from Pichu when leveled up with high friendship and evolves into Raichu when exposed to a Thunder Stone.",
    picture="https://cdn.bulbagarden.net/upload/thumb/1/17/025Pikachu-Original.png/600px-025Pikachu-Original.png",
    category_id=1,
    user_id=1)
session.add(Item1)
session.commit()

Item2 = Items(
    name="Charmander",
    date=datetime.datetime.now(),
    description="It evolves into Charmeleon starting at level 16, which evolves into Charizard starting at level 36. Along with Bulbasaur and Squirtle, Charmander is one of three starter Pokemon of Kanto.",
    picture="https://cdn.bulbagarden.net/upload/thumb/7/73/004Charmander.png/600px-004Charmander.png",
    category_id=2,
    user_id=1)
session.add(Item2)
session.commit()

Item3 = Items(
    name="Bulbasaur",
    date=datetime.datetime.now(),
    description="It evolves into Ivysaur starting at level 16, which evolves into Venusaur starting at level 32. Along with Charmander and Squirtle, Bulbasaur is one of three starter Pokemon of Kanto.",
    picture="https://cdn.bulbagarden.net/upload/thumb/2/21/001Bulbasaur.png/600px-001Bulbasaur.png",
    category_id=4,
    user_id=1)
session.add(Item3)
session.commit()

Item4 = Items(
    name="Snorlax",
    date=datetime.datetime.now(),
    description="It evolves from Munchlax when leveled up with high friendship.",
    picture="https://cdn.bulbagarden.net/upload/thumb/f/fb/143Snorlax.png/600px-143Snorlax.png",
    category_id=6,
    user_id=1)
session.add(Item4)
session.commit()

Item5 = Items(
    name="Pigeot",
    date=datetime.datetime.now(),
    description="It evolves from Pidgeotto starting at level 36. It is the final form of Pidgey. It can Mega Evolve into Mega Pidgeot using the Pidgeotite.",
    picture="https://cdn.bulbagarden.net/upload/thumb/5/57/018Pidgeot.png/600px-018Pidgeot.png",
    category_id=8,
    user_id=1)
session.add(Item5)
session.commit()

Item6 = Items(
    name="Onyx",
    date=datetime.datetime.now(),
    description="It evolves into Steelix when traded holding a Metal Coat.",
    picture="https://cdn.bulbagarden.net/upload/thumb/9/9a/095Onix.png/600px-095Onix.png",
    category_id=5,
    user_id=2)
session.add(Item6)
session.commit()

Item7 = Items(
    name="Geodude",
    date=datetime.datetime.now(),
    description="It evolves into Graveler starting at level 25, which evolves into Golem when traded.",
    picture="https://cdn.bulbagarden.net/upload/9/98/074Geodude.png",
    category_id=5,
    user_id=2)
session.add(Item7)
session.commit()

Item8 = Items(
    name="Togepi",
    date=datetime.datetime.now(),
    description="It evolves into Togetic when leveled up with high friendship, which evolves into Togekiss when exposed to a Shiny Stone.",
    picture="https://cdn.bulbagarden.net/upload/6/6b/175Togepi.png",
    category_id=7,
    user_id=3)
session.add(Item8)
session.commit()

Item9 = Items(
    name="Starmie",
    date=datetime.datetime.now(),
    description="It evolves from Staryu when exposed to a Water Stone.",
    picture="https://cdn.bulbagarden.net/upload/c/cd/121Starmie.png",
    category_id=3,
    user_id=3)
session.add(Item9)
session.commit()

Item10 = Items(
    name="Gyrados",
    date=datetime.datetime.now(),
    description="It evolves from Magikarp starting at level 20. It can Mega Evolve into Mega Gyarados using the Gyaradosite.",
    picture="https://cdn.bulbagarden.net/upload/4/41/130Gyarados.png",
    category_id=3,
    user_id=3)
session.add(Item10)
session.commit()

Item11 = Items(
    name="Squirtle",
    date=datetime.datetime.now(),
    description="It evolves into Wartortle starting at level 16, which evolves into Blastoise starting at level 36.",
    picture="https://cdn.bulbagarden.net/upload/thumb/3/39/007Squirtle.png/600px-007Squirtle.png",
    category_id=3,
    user_id=1)
session.add(Item11)
session.commit()

print "Your Pokedex has been populated with some cool Pokemon, enjoy it!"

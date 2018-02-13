from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


User1 = User(username="King of All Cosmos",
             email="tight_pants_king420@gmail.com", password="password123")
session.add(User1)
session.commit()

category1 = Category(user_id=1, name='Vegetables')
session.add(category1)
session.commit()

item1 = Item(name='Cabbage', size='74cm2mm',
             description='Very hard to make smaller just by peeling.  The center doesn\'t taste so good.', category_id=1, user_id=1)
session.add(item1)
session.commit()

item2 = Item(name='Daikon Radish', size='76cm9mm',
             description='It\'s very white.  You shouldn\'t tell a lady she has legs this color.', category_id=1, user_id=1)
session.add(item2)
session.commit()

item3 = Item(name='Carrot', size='57cm',
             description='Horses get excited and run faster if you put this in front of them.', category_id=1, user_id=1)
session.add(item3)
session.commit()

item4 = Item(name='Eggplant', size='17cm8mm',
             description='A purple vegetable.  Superstition says you shouldn\'t give this to your daughter-in-law in autumn.', category_id=1, user_id=1)
session.add(item4)
session.commit()

item5 = Item(name='Tomato', size='16cm5mm',
             description='Some people say it\'s fruit.  Some say vegetable.  Who cares!  It\'s food!', category_id=1, user_id=1)
session.add(item5)
session.commit()

category2 = Category(user_id=1, name='Animals')
session.add(category2)
session.commit()

item6 = Item(name='Spider', size='20cm3mm',
             description='Spins webs to catch bugs.  Most people hate them...', category_id=2, user_id=1)
session.add(item6)
session.commit()

item7 = Item(name='Mouse', size='11cm1mm',
             description='Lives in the house, but doesn\'t think it is really part of the family.', category_id=2, user_id=1)
session.add(item7)
session.commit()

item8 = Item(name='Yellow Swallowtail', size='10cm4mm',
             description='Tries to look scary with its bright yellow color, but most people think it is cute.', category_id=2, user_id=1)
session.add(item8)
session.commit()

item9 = Item(name='Giraffe', size='6m61cm1mm',
             description='An animal with a really long neck.  It doesn\'t expand or contract like rubber.', category_id=2, user_id=1)
session.add(item9)
session.commit()

item10 = Item(name='Big Dung Beetle', size='22cm',
              description='The dung seems to be the only big thing here.', category_id=2, user_id=1)
session.add(item10)
session.commit()

category3 = Category(user_id=1, name='Japanese Food')
session.add(category3)
session.commit()

item11 = Item(name='Onigiri (Rice Ball)', size='17cm5mm',
              description='A rice ball wrapped with seaweed.  Delicious and healthy.  Tastes better than it sounds.', category_id=3, user_id=1)
session.add(item11)
session.commit()

item12 = Item(name='Kagami-mochi', size='35cm2mm',
              description='ice cake for the New Year.  People usually just leave it lying around.', category_id=3, user_id=1)
session.add(item12)
session.commit()

item13 = Item(name='Shrimp Sushi', size='9cm4mm',
              description='Shrimp on rice.  It\'s a bit sour, but not rotten.  Don\'t worry.', category_id=3, user_id=1)
session.add(item13)
session.commit()

item14 = Item(name='Takoyaki', size='9cm3mm',
              description='A takoyaki with a toothpick.  This is much easier to eat.', category_id=3, user_id=1)
session.add(item14)
session.commit()

item15 = Item(name='Pickle Tub', size='1m8cm9mm',
              description='Put veggies inside and leave it for a while to make some pickles.', category_id=3, user_id=1)
session.add(item15)
session.commit()

category4 = Category(user_id=1, name='Adults')
session.add(category4)
session.commit()

item16 = Item(name='Relaxing Dude', size='1m66cm',
              description='This guy lounges around on boats, walls, benches, and basically anywhere he can.', category_id=4, user_id=1)
session.add(item16)
session.commit()

item17 = Item(name='Great Grandpa', size='1m80cm',
              description='A very healthy old man.  His back is still straight.', category_id=4, user_id=1)
session.add(item17)
session.commit()

item18 = Item(name='Shy Guy', size='1m88cm5mm',
              description='He\'s shy, and doesn\'t like heights or ghosts.', category_id=4, user_id=1)
session.add(item18)
session.commit()

item19 = Item(name='Great x2 Grandpa', size='1m57cm1mm',
              description='Once he starts telling a story about "the good old days", it never ends.', category_id=4, user_id=1)
session.add(item19)
session.commit()

item20 = Item(name='Snoozing Momma', size='1m33cm3mm',
              description='She always gets sleepy in the afternoon after finishing the housework.', category_id=4, user_id=1)
session.add(item20)
session.commit()

category5 = Category(user_id=1, name='Sports')
session.add(category5)
session.commit()

item21 = Item(name='Stadium', size='271m64cm3mm',
              description='A place where people throw and hit a ball.  Some people just sit around and shout.', category_id=5, user_id=1)
session.add(item21)
session.commit()

item22 = Item(name='Football', size='49cm4mm',
              description='Seems like an odd shape for a ball, but it appears to be shaped like this for a reason.', category_id=5, user_id=1)
session.add(item22)
session.commit()

item23 = Item(name='Soccer Goal', size='8m55cm6mm',
              description='People try to put a ball in here to get points.  A very popular Earth sport.', category_id=5, user_id=1)
session.add(item23)
session.commit()

item24 = Item(name='Baseball', size='19cm9mm',
              description='Hit this with a stick and get some points.', category_id=5, user_id=1)
session.add(item24)
session.commit()

item25 = Item(name='Surfboard', size='1m38cm5mm',
              description='A board used to ride on waves.  It looks a lot cooler when you stand up.', category_id=5, user_id=1)
session.add(item25)
session.commit()


print "Added stuff."

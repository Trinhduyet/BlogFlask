from flaskblog import create_app
from flask_script import Manager

from flaskblog.models import User, Post
from flaskblog import db

from datetime import datetime

from flask_bcrypt import Bcrypt

app = create_app()
manager = Manager(app)
bcrypt = Bcrypt()

@manager.command
def init():
    dropdb()
    initdb()
    filldb()

@manager.command
def initdb():
    db.create_all()

@manager.command
def dropdb():
    db.drop_all()

@manager.command
def filldb():
    admin = User(
        id = 1,
        username = "admin",
        email = "admin@gmail.com",
        password = "123456"
        # password =   bcrypt.generate_password_hash("123456");
    )
    db.session.add(admin)
    db.session.commit()

    user = User(
        id = 2,
        username = "trinhduyet95",
        email = "trinhduyet95@gmail.com",
        password = "123456"
    )
    db.session.add(user)
    db.session.commit()

    post = Post(
        id = 1,
        title = "Hello World",
        date_posted = datetime(2019, 2, 28),
        content = POST_1,
        user_id = 1
    )
    db.session.add(post)
    db.session.commit()

    post = Post(
        id=2,
        title="Getting started",
        date_posted=datetime(2019, 1, 19),
        content=POST_2,
        user_id=1
    )

    post = Post(
        id=3,
        title="Welcome",
        date_posted=datetime(2020, 6, 19),
        content=POST_3,
        user_id=1
    )
    db.session.add(post)
    db.session.commit()

POST_1 = u"""
First blog post.

Nam quis urna est. Duis vel tincidunt quam. Vivamus odio tortor, suscipit vel
pretium quis, imperdiet quis dolor. Integer molestie enim nec risus malesuada
imperdiet. Donec pellentesque justo id sem tempor varius. Etiam ut tincidunt
lorem. Nullam a tellus sem.
Vestibulum a neque sed quam pharetra interdum. Quisque euismod dictum ipsum.
Vivamus tincidunt mi at tellus pharetra placerat. Sed sed sem nisi, sit amet
ultrices neque. Quisque eget turpis et sapien luctus auctor in ac magna.
"""

POST_2 = u"""
Test blog.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean vel ipsum
lectus. Pellentesque tempus enim sed leo imperdiet non lobortis nulla
sollicitudin. Maecenas arcu orci, interdum eu rhoncus ut, blandit id felis.
Mauris consectetur dui at felis ultricies tempus. Quisque molestie convallis
lectus vitae viverra. Duis lobortis ultrices turpis, nec eleifend est
venenatis nec. Sed sed lorem quis metus eleifend ullamcorper. Ut semper
nulla a arcu ornare **condimentum**.

Aliquam neque metus, posuere vitae condimentum ut, fermentum quis diam.
*Nulla facilisi*. Proin sapien felis, tristique eu venenatis at,
**accumsan** non dui. Vestibulum ante ipsum primis in faucibus orci luctus et
ultrices posuere cubilia.
"""

POST_3 = u"""
First blog post.

Nam quis urna est. Duis vel tincidunt quam. Vivamus odio tortor, suscipit vel
pretium quis, imperdiet quis dolor. Integer molestie enim nec risus malesuada
imperdiet. Donec pellentesque justo id sem tempor varius. Etiam ut tincidunt
lorem. Nullam a tellus sem.
Vestibulum a neque sed quam pharetra interdum. Quisque euismod dictum ipsum.
Vivamus tincidunt mi at tellus pharetra placerat. Sed sed sem nisi, sit amet
ultrices neque. Quisque eget turpis et sapien luctus auctor in ac magna.
"""

if __name__ == "__main__":
    manager.run()

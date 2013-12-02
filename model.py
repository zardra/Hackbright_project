import config
import bcrypt
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

from flask.ext.login import UserMixin

engine = create_engine(config.DB_URI, echo=False) 
session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))

Base = declarative_base()
Base.query = session.query_property()


class User(Base, UserMixin):
    __tablename__ = "users" 
    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    salt = Column(String(64), nullable=False)

    def set_password(self, password):
        self.salt = bcrypt.gensalt()
        password = password.encode("utf-8")
        self.password = bcrypt.hashpw(password, self.salt)

    def authenticate(self, password):
        password = password.encode("utf-8")
        return bcrypt.hashpw(password, self.salt.encode("utf-8")) == self.password

class Image(Base):
    __tablename__="images"
    id = Column(Integer, primary_key=True)
    title = Column(String(150))
    ws_rows = Column(String(15))
    directions = Column(String())
    user_id = Column(Integer, ForeignKey("users.id"))

    def filename(self):
        filename = str(self.id) + ".png"
        return filename

def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    u = User(email="test@test.com", username="zardra")
    u.set_password("unicorn")
    session.add(u)
    session.commit()

if __name__ == "__main__":
    create_tables()

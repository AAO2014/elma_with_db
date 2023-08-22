import os
import random

from flask import Flask, jsonify
from sqlalchemy import Column, Integer, create_engine, Sequence, Boolean, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
application = app

DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_NAME = os.environ.get('DATABASE_NAME')
DATABASE_URI = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:5432/{DATABASE_NAME}'

engine = create_engine(DATABASE_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['DEBUG'] = True


class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer,  Sequence('id_seq'), primary_key=True)
    email = Column(Text, nullable=False)
    verified = Column(Boolean, default=False)

    def __init__(self, email, verified):
        self.email = email
        self.verified = verified

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'verified': self.verified,
        }


def create_test_records():
    records = []

    for i in range(10):
        record_data = {
            'email': f'mail{i}@mail.abc',
            'verified': bool(random.randint(0, 1)),
        }
        records.append(Test(**record_data))

    return records


# @app.before_request
# def before_request_func():
#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)
#     session.bulk_save_objects(create_test_records())
#     session.commit()


def is_email_verified(email):
    return session.query(Test).filter(Test.email == email).filter(Test.verified == True).all()


@application.route('/')
def foo():
    return jsonify([i.to_json() for i in session.query(Test).all()])


@application.route('/check_email/<path:email>')
def check_email(email):
    result = is_email_verified(email)
    return jsonify({'user_find': bool(result)})

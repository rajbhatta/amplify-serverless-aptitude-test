
from modal.sensor import Sensor
import awsgi
import json
import logging
import os

from flask_cors import CORS
from flask import Flask, app, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_ROUTE ="/sensors"

app = Flask(__name__)
CORS(app)

@app.route(BASE_ROUTE, methods=['POST'])
def create_customer():
    request_json = request.get_json()
    db_session = provide_database_session()
    create(db_session,Sensor(sensor_name='test',model='test',temperature='19', operating_location ='langley'))
    return jsonify(message='POST is sucessful')

@app.route(BASE_ROUTE, methods=['GET'])
def list_customer():
    return jsonify(message='GET is successful')


def handler(event, context):
  print('received event:')
  print(event)
  
  return awsgi.response(app,event,context)

def provide_database_session():
    
    dbusername = 'postgres'
    dbpassword = 'admin123$'
    dbhost = 'equipmentdb.cmqdxui4uot8.us-west-2.rds.amazonaws.com'
    dbname = 'postgres'

    postgres_engine = create_engine(f'postgresql://{dbusername}:{dbpassword}@{dbhost}:5432/{dbname}')
    session = sessionmaker(bind=postgres_engine)()
    return session;

def create(session, sensor):
        session.add(sensor)
        session.commit()
        session.flush()
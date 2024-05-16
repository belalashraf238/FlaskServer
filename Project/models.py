from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):
    User_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Status(db.Model):
    status_id = db.Column(db.Integer, primary_key=True)
    signal_strength = db.Column(db.Integer)
    signal_level_description = db.Column(db.String(50))
    units = db.Column(db.String(10))
    reachable_status = db.Column(db.Boolean)
    roaming_status = db.Column(db.Boolean)
    mcc = db.Column(db.String(10))
    mnc = db.Column(db.String(10))
    network_operator_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    network_country_iso = db.Column(db.String(2))
    charging = db.Column(db.Boolean)
    battery_level = db.Column(db.String(10))
    access_wifi_state = db.Column(db.Boolean)
    access_location = db.Column(db.Boolean)
    access_phone_state = db.Column(db.Boolean)
    access_phone_numbers = db.Column(db.Boolean)
    access_phone_calls = db.Column(db.Boolean)
    access_contacts = db.Column(db.Boolean)
    access_sms = db.Column(db.Boolean)
    access_call_interception = db.Column(db.Boolean)
    app_running_since = db.Column(db.DateTime)
    calls_received = db.Column(db.Integer)
    last_call_received = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.User_id'), nullable=False)
    user = relationship('User', backref='statuses')


class SMS(db.Model):
    sms_id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20))
    sender_id = db.Column(db.String(100))
    sms_content = db.Column(db.Text)
    time_received = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.User_id'), nullable=False)
    user = relationship('User', backref='sms')


class Calls(db.Model):
    calls_id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20))
    caller_id = db.Column(db.String(100))
    time_received = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.User_id'), nullable=False)
    user = relationship('User', backref='calls')

# Define your database models here
# Define the models for your tables

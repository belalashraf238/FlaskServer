from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Relationships
    wifis = db.relationship('WiFi', backref='user', cascade="all, delete-orphan", uselist=False)
    gsms = db.relationship('GSM', backref='user', cascade="all, delete-orphan", uselist=False)
    devices = db.relationship('Device', backref='user', cascade="all, delete-orphan", uselist=False)
    ris = db.relationship('RI', backref='user', cascade="all, delete-orphan", uselist=False)
    sms = db.relationship('SMS', backref='user', cascade="all, delete-orphan", uselist=False)
    calls = db.relationship('Call', backref='user', cascade="all, delete-orphan", uselist=False)

class WiFi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    signal_strength = db.Column(db.Integer, nullable=False, default=0)
    signal_level_description = db.Column(db.String(50), nullable=False, default='No Signal')
    units = db.Column(db.String(10), nullable=False, default='dBm')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class GSM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    signal_strength = db.Column(db.Integer, nullable=False, default=0)
    signal_level_description = db.Column(db.String(50), nullable=False, default='No Signal')
    units = db.Column(db.String(10), nullable=False, default='dBm')
    reachable_status = db.Column(db.Boolean, nullable=False, default=False)
    roaming_status = db.Column(db.Boolean, nullable=False, default=False)
    mcc = db.Column(db.String(10), nullable=False, default='000')
    mnc = db.Column(db.String(10), nullable=False, default='000')
    network_operator_name = db.Column(db.String(100), nullable=False, default='Unknown')
    phone_number = db.Column(db.String(20), nullable=False, default='0000000000')
    network_country_iso = db.Column(db.String(10), nullable=False, default='US')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    charging = db.Column(db.Boolean, nullable=False, default=False)
    battery_level = db.Column(db.String(10), nullable=False, default='0%')
    access_wifi_state = db.Column(db.Boolean, nullable=False, default=False)
    access_location = db.Column(db.Boolean, nullable=False, default=False)
    access_phone_state = db.Column(db.Boolean, nullable=False, default=False)
    access_phone_numbers = db.Column(db.Boolean, nullable=False, default=False)
    access_phone_calls = db.Column(db.Boolean, nullable=False, default=False)
    access_contacts = db.Column(db.Boolean, nullable=False, default=False)
    access_sms = db.Column(db.Boolean, nullable=False, default=False)
    access_call_interception = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class RI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_running_since = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    calls_received = db.Column(db.Integer, nullable=False, default=0)
    last_call_received = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class SMS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), default='0000000000')
    sender_id = db.Column(db.String(100), default='0000000000')
    sms_content = db.Column(db.Text, default='No content')
    time_received = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), default='0000000000')
    caller_id = db.Column(db.String(100), default='0000000000')
    time_received = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# Define your database models here
# Define the models for your tables

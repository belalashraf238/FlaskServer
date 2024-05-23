from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from datetime import datetime
from flask import Flask, jsonify, request
from models import db, Device, RI, WiFi, GSM, SMS, Call, User
from flask_httpauth import HTTPBasicAuth
import random
import string

engine = create_engine('mysql+pymysql://root:@localhost/MockDataBase1')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = engine.url
db.init_app(app)
auth = HTTPBasicAuth()

app.config['SECRET_KEY'] = 'secret-key'

if database_exists(engine.url):
    print("Database already exists")
else:
    if not create_database(engine.url):
        print('Database "mobile" created successfully.')
        app.config['SQLALCHEMY_DATABASE_URI'] = engine.url
    with app.app_context():
        db.create_all()


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return user


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if 'username' not in data :
        return jsonify({'message': 'Username is required'}), 400

    username = data['username']
    # Generate a random password
    password_length = 8
    password_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(password_characters) for _ in range(password_length))

    # Create a new user
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    new_wifi = WiFi(user_id=new_user.id)
    db.session.add(new_wifi)

    new_gsm = GSM(user_id=new_user.id)
    db.session.add(new_gsm)

    new_device = Device(user_id=new_user.id)
    db.session.add(new_device)

    new_ri = RI(user_id=new_user.id)
    db.session.add(new_ri)

    new_sms = SMS(user_id=new_user.id)
    db.session.add(new_sms)
    new_call = Call(user_id=new_user.id)
    db.session.add(new_call)
    db.session.commit()


    return jsonify({"data":{
        "username": username,
        "password": password,
    }}), 201


@app.route('/login', methods=['POST'])
@auth.login_required
def login():
    
    
   
    return jsonify({"message": f"Hello, {auth.current_user().username}!"}), 200


@app.route('/sms', methods=['PUT'])
@auth.login_required
def put_sms():
    data = request.json.get('data', [])
    current_user = auth.current_user()
    if not data:
        return jsonify(message="No SMS data provided"), 400

    for sms_data in data:
        phone_number = sms_data.get('phone_number')
        sender_id = sms_data.get('sender_id')
        sms_content = sms_data.get('sms_content')
        time_received_str = sms_data.get('time_received')

        try:
            time_received = datetime.strptime(time_received_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return jsonify(message="Invalid time format"), 400

        # Assuming you have a current_user variable representing the authenticated user

        # Check if an SMS with the same user ID and phone number exists
        existing_sms = SMS.query.filter_by(user_id=current_user.id).first()

        if existing_sms:
            # Update existing SMS
            existing_sms.sender_id = sender_id
            existing_sms.sms_content = sms_content
            existing_sms.time_received = time_received
            existing_sms.phone_number = phone_number
        else:
            # Create a new SMS entry
            new_sms = SMS(
                phone_number=phone_number,
                sender_id=sender_id,
                sms_content=sms_content,
                time_received=time_received,
                user_id=current_user.id
            )
            db.session.add(new_sms)

    db.session.commit()

    return jsonify(message="SMS data processed successfully"), 200


@app.route('/call', methods=['PUT'])
@auth.login_required
def put_call():
    data = request.json.get('data', [])
    current_user = auth.current_user()
    if not data:
        return jsonify(message="No call data provided"), 400

    for call_data in data:
        phone_number = call_data.get('phone_number')
        caller_id = call_data.get('caller_id')
        time_received_str = call_data.get('time_received')

        try:
            time_received = datetime.strptime(time_received_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return jsonify(message="Invalid time format"), 400

        # Assuming you have a current_user variable representing the authenticated user
        existing_call = Call.query.filter_by(user_id=current_user.id).first()

        if existing_call:
            # Update existing SMS
            existing_call.phone_number = phone_number
            existing_call.caller_id = caller_id
            existing_call.time_received_str = time_received

        # Create a new Call entry
        new_call = Call(
            phone_number=phone_number,
            caller_id=caller_id,
            time_received=time_received,
            user_id=current_user.id
        )
        db.session.add(new_call)

    db.session.commit()

    return jsonify(message="Call data processed successfully"), 200


@app.route('/status', methods=['PUT'])
@auth.login_required
def put_data():
    current_user = auth.current_user()  # Extract user from authentication
    data = request.json.get('data', {})

    # Update WiFi model
    wifi_data = data.get('WiFi', {})
    update_wifi(current_user.id, wifi_data)

    # Update GSM model
    gsm_data = data.get('GSM', {})
    update_gsm(current_user.id, gsm_data)

    # Update Device model
    device_data = data.get('Device', {})
    update_device(current_user.id, device_data)

    # Update RI model
    ri_data = data.get('RI', {})
    update_ri(current_user.id, ri_data)

    db.session.commit()

    return jsonify(message="Data updated successfully"), 200


def update_wifi(user_id, wifi_data):
    wifi = WiFi.query.filter_by(user_id=user_id).first()
    if wifi:
        wifi.signal_strength = wifi_data.get('signalStrength', wifi.signal_strength)
        wifi.signal_level_description = wifi_data.get('signalLevelDescription', wifi.signal_level_description)
        wifi.units = wifi_data.get('units', wifi.units)


def update_gsm(user_id, gsm_data):
    gsm = GSM.query.filter_by(user_id=user_id).first()
    if gsm:
        gsm.signal_strength = gsm_data.get('signalStrength', gsm.signal_strength)
        gsm.signal_level_description = gsm_data.get('signalLevelDescription', gsm.signal_level_description)
        gsm.units = gsm_data.get('units', gsm.units)
        gsm.reachable_status = gsm_data.get('reachableStatus', gsm.reachable_status)
        gsm.roaming_status = gsm_data.get('roamingStatus', gsm.roaming_status)
        gsm.mcc = gsm_data.get('MCC', gsm.mcc)
        gsm.mnc = gsm_data.get('MNC', gsm.mnc)
        gsm.network_operator_name = gsm_data.get('networkOperatorName', gsm.network_operator_name)
        gsm.phone_number = gsm_data.get('phoneNumber', gsm.phone_number)
        gsm.network_country_iso = gsm_data.get('networkCountryISO', gsm.network_country_iso)


def update_device(user_id, device_data):
    device = Device.query.filter_by(user_id=user_id).first()
    if device:
        device.charging = device_data.get('charging', device.charging)
        device.battery_level = device_data.get('batteryLevel', device.battery_level)
        device.access_wifi_state = device_data.get('access_wifi_state', device.access_wifi_state)
        device.access_location = device_data.get('access_location', device.access_location)
        device.access_phone_state = device_data.get('access_phone_state', device.access_phone_state)
        device.access_phone_numbers = device_data.get('access_phone_numbers', device.access_phone_numbers)
        device.access_phone_calls = device_data.get('access_phone_calls', device.access_phone_calls)
        device.access_contacts = device_data.get('access_contacts', device.access_contacts)
        device.access_sms = device_data.get('access_sms', device.access_sms)
        device.access_call_interception = device_data.get('access_call_interception', device.access_call_interception)


def update_ri(user_id, ri_data):
    ri = RI.query.filter_by(user_id=user_id).first()
    if ri:
        ri.app_running_since = datetime.strptime(ri_data.get('appRunningSince', ri.app_running_since),
                                                 "%Y-%m-%d %H:%M:%S")
        ri.calls_received = ri_data.get('callsReceived', ri.calls_received)
        ri.last_call_received = datetime.strptime(ri_data.get('lastCallReceived', ri.last_call_received),
                                                  "%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    app.run(debug=True)

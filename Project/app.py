from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import Flask, jsonify, request
from models import db, Status, SMS, Calls, User

engine = create_engine('mysql+pymysql://belal:17242524@localhost/MobileTestData')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = engine.url
db.init_app(app)
api = Api(app)
jwt = JWTManager(app)
app.config['SECRET_KEY'] = 'zeyad'
app.config['JWT_SECRET_KEY'] = 'zeyad'
if database_exists(engine.url):
    print("Database already exists")
else:
    if not create_database(engine.url):
        print('Database "mobile" created successfully.')
    app.config['SQLALCHEMY_DATABASE_URI'] = engine.url
    with app.app_context():
        db.create_all()


def authenticate(username, password):
    user = User.query.filter_by(username=username, password=password).first()
    return user


# User API Endpoints
class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        user = User(username=args['username'], password=args['password'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 201


class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        user = authenticate(args['username'], args['password'])
        if not user:
            return {'message': 'Invalid credentials'}, 401

        access_token = create_access_token(identity=user.User_id)
        return {'access_token': access_token}, 200


class UserData(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.get(current_user)
        return {'username': user.username
            , 'User_id': user.User_id}, 200

    @jwt_required()
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        current_user = get_jwt_identity()
        user = User.query.get(current_user)

        if args['username']:
            user.username = args['username']
        if args['password']:
            user.password = args['password']

        db.session.commit()
        return {'message': 'User data updated successfully'}, 200


status_parser = reqparse.RequestParser()
status_parser.add_argument('signal_strength', type=int)
status_parser.add_argument('signal_level_description', type=str)
status_parser.add_argument('units', type=str)
status_parser.add_argument('reachable_status', type=bool)
status_parser.add_argument('roaming_status', type=bool)
status_parser.add_argument('mcc', type=str)
status_parser.add_argument('mnc', type=str)
status_parser.add_argument('network_operator_name', type=str)
status_parser.add_argument('phone_number', type=str)
status_parser.add_argument('network_country_iso', type=str)
status_parser.add_argument('charging', type=bool)
status_parser.add_argument('battery_level', type=str)
status_parser.add_argument('access_wifi_state', type=bool)
status_parser.add_argument('access_location', type=bool)
status_parser.add_argument('access_phone_state', type=bool)
status_parser.add_argument('access_phone_numbers', type=bool)
status_parser.add_argument('access_phone_calls', type=bool)
status_parser.add_argument('access_contacts', type=bool)
status_parser.add_argument('access_sms', type=bool)
status_parser.add_argument('access_call_interception', type=bool)
status_parser.add_argument('app_running_since', type=str)
status_parser.add_argument('calls_received', type=int)
status_parser.add_argument('last_call_received', type=str)
status_parser.add_argument('user_id', type=int)

sms_parser = reqparse.RequestParser()
sms_parser.add_argument('phone_number', type=str)
sms_parser.add_argument('sender_id', type=str)
sms_parser.add_argument('sms_content', type=str)
sms_parser.add_argument('time_received', type=str)
sms_parser.add_argument('user_id', type=int)

calls_parser = reqparse.RequestParser()
calls_parser.add_argument('phone_number', type=str)
calls_parser.add_argument('caller_id', type=str)
calls_parser.add_argument('time_received', type=str)
calls_parser.add_argument('user_id', type=int)


class StatusListResource(Resource):
    def get(self, user_id):
        statuses = Status.query.filter_by(user_id=user_id).all()
        return [{'status_id': status.status_id, 'signal_strength': status.signal_strength} for status in statuses]

    def post(self, user_id):

        args = status_parser.parse_args()
        args['user_id'] = user_id
        new_status = Status(**args)
        db.session.add(new_status)
        db.session.commit()
        return {'message': 'Status added successfully'}, 201


class StatusResource(Resource):
    def get(self, user_id, status_id):
        status = Status.query.filter_by(user_id=user_id, status_id=status_id).first_or_404()
        return {'status_id': status.status_id, 'signal_strength': status.signal_strength}

    def delete(self, user_id, status_id):
        status = Status.query.filter_by(user_id=user_id, status_id=status_id).first_or_404()
        db.session.delete(status)
        db.session.commit()
        return {'message': 'Status deleted successfully'}, 200

    def put(self, user_id, status_id):
        status = Status.query.filter_by(user_id=user_id, status_id=status_id).first_or_404()
        args = status_parser.parse_args()
        for key, value in args.items():
            if value is not None:
                setattr(status, key, value)
        db.session.commit()
        return {'message': 'Status updated successfully'}, 200


class SMSListResource(Resource):
    def get(self, user_id):
        sms_list = SMS.query.filter_by(user_id=user_id).all()
        return [{'sms_id': sms.sms_id, 'phone_number': sms.phone_number, 'sender_id': sms.sender_id,
                 'sms_content': sms.sms_content, 'time_received': sms.time_received} for sms in sms_list]

    def post(self, user_id):
        args = sms_parser.parse_args()
        args['user_id'] = user_id
        new_sms = SMS(**args)
        db.session.add(new_sms)
        db.session.commit()
        return {'message': 'SMS added successfully'}, 201


class SMSResource(Resource):
    def get(self, user_id, sms_id):
        sms = SMS.query.filter_by(user_id=user_id, sms_id=sms_id).first_or_404()
        return {'sms_id': sms.sms_id, 'phone_number': sms.phone_number, 'sender_id': sms.sender_id,
                'sms_content': sms.sms_content, 'time_received': sms.time_received}

    def delete(self, user_id, sms_id):
        sms = SMS.query.filter_by(user_id=user_id, sms_id=sms_id).first_or_404()
        db.session.delete(sms)
        db.session.commit()
        return {'message': 'SMS deleted successfully'}, 200

    def put(self, user_id, sms_id):
        sms = SMS.query.filter_by(user_id=user_id, sms_id=sms_id).first_or_404()
        args = sms_parser.parse_args()
        for key, value in args.items():
            if value is not None:
                setattr(sms, key, value)
        db.session.commit()
        return {'message': 'SMS updated successfully'}, 200


class CallsListResource(Resource):
    def get(self, user_id):
        calls_list = Calls.query.filter_by(user_id=user_id).all()
        return [{'calls_id': call.calls_id, 'phone_number': call.phone_number, 'caller_id': call.caller_id,
                 'time_received': call.time_received} for call in calls_list]

    def post(self, user_id):
        args = calls_parser.parse_args()
        args['user_id'] = user_id
        new_call = Calls(**args)
        db.session.add(new_call)
        db.session.commit()
        return {'message': 'Call added successfully'}, 201


class CallsResource(Resource):
    def get(self, user_id, call_id):
        call = Calls.query.filter_by(user_id=user_id, calls_id=call_id).first_or_404()
        return {'calls_id': call.calls_id, 'phone_number': call.phone_number, 'caller_id': call.caller_id,
                'time_received': call.time_received}

    def delete(self, user_id, call_id):
        call = Calls.query.filter_by(user_id=user_id, calls_id=call_id).first_or_404()
        db.session.delete(call)
        db.session.commit()
        return {'message': 'Call deleted successfully'}, 200

    def put(self, user_id, call_id):
        call = Calls.query.filter_by(user_id=user_id, calls_id=call_id).first_or_404()
        args = calls_parser.parse_args()
        for key, value in args.items():
            if value is not None:
                setattr(call, key, value)
        db.session.commit()
        return {'message': 'Call updated successfully'}, 200


api.add_resource(StatusListResource, '/users/<int:user_id>/statuses')
api.add_resource(StatusResource, '/users/<int:user_id>/statuses/<int:status_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserData, '/user')
api.add_resource(SMSListResource, '/users/<int:user_id>/sms')
api.add_resource(SMSResource, '/users/<int:user_id>/sms/<int:sms_id>')
api.add_resource(CallsListResource, '/users/<int:user_id>/calls')
api.add_resource(CallsResource, '/users/<int:user_id>/calls/<int:call_id>')

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)

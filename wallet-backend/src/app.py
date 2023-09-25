import json
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import redis

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'utfkvhbkljgyfvgvWFSGEhgvjky'
jwt = JWTManager(app)

# Configure SQLAlchemy connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://juliusbright:juliusbright@localhost/wallet'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configure Redis connection
app.config['REDIS_HOST'] = 'localhost'
app.config['REDIS_PORT'] = 6379
app.config['REDIS_DB'] = 0

# Create a Redis connection
redis_conn = redis.StrictRedis(
    host=app.config['REDIS_HOST'],
    port=app.config['REDIS_PORT'],
    db=app.config['REDIS_DB'],
    decode_responses=True,
)

# Define the User model for SQLAlchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    balance = db.Column(db.Float, default=0.0)

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='transactions')
    type = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())


bcrypt = Bcrypt(app)

@app.route('/', methods=['GET'])
def list_endpoints():
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            route = {
                "endpoint": rule.endpoint,
                "methods": ','.join(rule.methods),
                "path": str(rule),
            }
            routes.append(route)
    return jsonify({"routes": routes})

@app.route('/create_account', methods=['POST'])
def create_account():
    try:
        data = request.json
        if 'username' in data and 'password' in data and 'initial_balance' in data:
            username = data['username']
            password = data['password']
            initial_balance = data['initial_balance']

            # Check if the username already exists
            if User.query.filter_by(username=username).first():
                return jsonify({"error": "Username already exists"}), 400

            # Hash the password before storing it
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            # Store the user data in the database
            user = User(username=username, password=hashed_password, balance=initial_balance)
            db.session.add(user)
            db.session.commit()

            cache_key = f"user:{username}"
            user_data = {
                "id": user.id,
                "username": user.username,
                "balance": user.balance,
            }
            redis_conn.setex(cache_key, 3600, json.dumps(user_data))  # Cache for 1 hour

            return jsonify({"message": "Account created successfully"}), 201
        else:
            return jsonify({"error": "Invalid data format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        if 'username' in data and 'password' in data:
            username = data['username']
            password = data['password']

            user = User.query.filter_by(username=username).first()

            # Check if the username exists and the password is correct
            if user and bcrypt.check_password_hash(user.password, password):
                # Generate a JWT token upon successful authentication
                access_token = create_access_token(identity=user.id)
                return jsonify({"access_token": access_token}), 200
            else:
                return jsonify({"error": "Invalid credentials"}), 401
        else:
            return jsonify({"error": "Invalid data format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/balance/<username>', methods=['GET'])
@jwt_required()
def get_balance(username):
    try:
        cached_balance = redis_conn.get(username)

        if cached_balance is not None:
            return jsonify({"balance": float(cached_balance)}), 200
        else:
            # If not found in cache, query the database
            user = User.query.filter_by(username=username).first()
            if user:
                # Store the retrieved balance in the cache with an expiration time (e.g., 3600 seconds)
                redis_conn.setex(username, 3600, user.balance)
                return jsonify({"balance": user.balance}), 200
            else:
                return jsonify({"error": "Username not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_and_cache_transaction_history(username):
    try:
        user = User.query.filter_by(username=username).first()
        if user:
            user_transactions = user.transactions

            transaction_history = []
            for transaction in user_transactions:
                transaction_history.append({
                    "type": transaction.type,
                    "amount": transaction.amount,
                    "timestamp": transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                })

            return {"transaction_history": transaction_history}
        else:
            return {"error": "Username not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500


@app.route('/transaction_history/<username>', methods=['GET'])
@jwt_required()
def get_transaction_history(username):
    cache_key = f"transaction_history:{username}"

    try:
        cached_data = redis_conn.get(cache_key)

        if cached_data:
            return jsonify(json.loads(cached_data.decode('utf-8'))), 200
        else:
            data_to_cache = get_and_cache_transaction_history(username)
            redis_conn.setex(cache_key, 3600, json.dumps(data_to_cache))  # Cache for 1 hour
            return jsonify(data_to_cache), 200
    except Exception as e:
        print(f"Redis error: {str(e)}")
        data_from_db = get_and_cache_transaction_history(username)
        return jsonify(data_from_db), 200

@app.route('/credit/<username>', methods=['POST'])
@jwt_required()
def credit_account(username):
    try:
        data = request.json
        if 'amount' in data:
            amount = data['amount']
            if username in User:
                User[username]["balance"] += amount
                Transactions.append({"username": username, "type": "credit", "amount": amount})
                return jsonify({"message": "Account credited successfully"}), 200
            else:
                return jsonify({"error": "Username not found"}), 404
        else:
            return jsonify({"error": "Invalid data format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/debit/<username>', methods=['POST'])
@jwt_required()
def debit_account(username):
    try:
        data = request.json
        if 'amount' in data:
            amount = data['amount']
            if username in User:
                if User[username]["balance"] >= amount:
                    User[username]["balance"] -= amount
                    Transactions.append({"username": username, "type": "debit", "amount": amount})
                    return jsonify({"message": "Account debited successfully"}), 200
                else:
                    return jsonify({"error": "Insufficient balance"}), 400
            else:
                return jsonify({"error": "Username not found"}), 404
        else:
            return jsonify({"error": "Invalid data format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = 5000
    app.run(debug=True, port=port)

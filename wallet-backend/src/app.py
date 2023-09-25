from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import redis

app = Flask(__name__)

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

# Placeholder for storing user accounts and transactions 
accounts = {}
class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
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
    data = request.json
    if 'username' in data and 'password' in data and 'initial_balance' in data:
        username = data['username']
        password = data['password']
        initial_balance = data['initial_balance']

        # Check if the username already exists
        if username in accounts:
            return jsonify({"error": "Username already exists"}), 400

        # Hash the password before storing it
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

       # Store the user data in the database
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        accounts[username] = {
            "password": hashed_password,
            "balance": initial_balance
        }

        return jsonify({"message": "Account created successfully"}), 201
    else:
        return jsonify({"error": "Invalid data format"}), 400

@app.route('/login', methods=['POST'])
def login():
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

@app.route('/balance/<username>', methods=['GET'])
@jwt_required()
def get_balance(username):
    if username in accounts:
        return jsonify({"balance": accounts[username]["balance"]}), 200
    else:
        return jsonify({"error": "Username not found"}), 404

@app.route('/transaction_history/<username>', methods=['GET'])
@jwt_required()
def get_transaction_history(username):
    user_transactions = Transactions.query.filter_by(username=username).all()

    transaction_history = []
    for transaction in user_transactions:
        transaction_history.append({
            "type": transaction.type,
            "amount": transaction.amount,
            "credit": transaction.credit,
            "debit": transaction.debit,
            "timestamp": transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify({"transaction_history": transaction_history}), 200
    
@app.route('/credit/<username>', methods=['POST'])
@jwt_required()
def credit_account(username):
    data = request.json
    if 'amount' in data:
        amount = data['amount']
        if username in accounts:
            accounts[username]["balance"] += amount
            Transactions.append({"username": username, "type": "credit", "amount": amount})
            return jsonify({"message": "Account credited successfully"}), 200
        else:
            return jsonify({"error": "Username not found"}), 404
    else:
        return jsonify({"error": "Invalid data format"}), 400

@app.route('/debit/<username>', methods=['POST'])
@jwt_required()
def debit_account(username):
    data = request.json
    if 'amount' in data:
        amount = data['amount']
        if username in accounts:
            if accounts[username]["balance"] >= amount:
                accounts[username]["balance"] -= amount
                Transactions.append({"username": username, "type": "debit", "amount": amount})
                return jsonify({"message": "Account debited successfully"}), 200
            else:
                return jsonify({"error": "Insufficient balance"}), 400
        else:
            return jsonify({"error": "Username not found"}), 404
    else:
        return jsonify({"error": "Invalid data format"}), 400
if __name__ == '__main__':
    port = 5000
    app.run(debug=True, port=port)

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import redis

app = Flask(__name__)

# Configure Flask-JWT-Extended
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key
jwt = JWTManager(app)

# Configure SQLAlchemy for PostgreSQL
#TODO:: 
# Configure the SQLAlchemy database URI to connect to your PostgreSQL database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://juliusbright:juliusbright@localhost/wallet'

# Initialize the SQLAlchemy extension with your Flask app.
db = SQLAlchemy(app)

# Configure Redis connection
app.config['REDIS_HOST'] = 'localhost'  
app.config['REDIS_PORT'] = 6379  
app.config['REDIS_DB'] = 0 

# Create a Redis connection
redis_conn = redis.StrictRedis(
    host=app.config['REDIS_HOST'],
    port=app.config['REDIS_PORT'],
    db=app.config['REDIS_DB'],
    decode_responses=True,  # Automatically decode responses to strings
)

# Define the User model for SQLAlchemy
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)
#     balance = db.Column(db.Float, default=0.0)

# Placeholder for storing user accounts and transactions (for demonstration purposes).
accounts = {}
transactions = []

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

       # Store the user data in the database (replace with your database logic)
        # user = User(username=username, password=hashed_password)
        # db.session.add(user)
        # db.session.commit()

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

        # Query the user data from the database (replace with your database logic)
        user = User.query.filter_by(username=username).first()

        # Check if the username exists and the password is correct
        # if user and bcrypt.check_password_hash(user.password, password):
        #     # Generate a JWT token upon successful authentication
        #     access_token = create_access_token(identity=user.id)
        #     return jsonify({"access_token": access_token}), 200
        # else:
        #     return jsonify({"error": "Invalid credentials"}), 401

        # For demonstration purposes, we'll return a token without actual database queries
        # Replace this with your database logic
        if username in accounts and bcrypt.check_password_hash(accounts[username]["password"], password):
            access_token = create_access_token(identity=username)
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
    # Implement logic to retrieve and return transaction history for the user.
    # You would typically query a database for this information.
    # For simplicity, we'll return an empty list for now.
    return jsonify({"transaction_history": []}), 200

@app.route('/credit/<username>', methods=['POST'])
@jwt_required()
def credit_account(username):
    data = request.json
    if 'amount' in data:
        amount = data['amount']
        if username in accounts:
            accounts[username]["balance"] += amount
            transactions.append({"username": username, "type": "credit", "amount": amount})
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
                transactions.append({"username": username, "type": "debit", "amount": amount})
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

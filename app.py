from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database (saves to 'app.db' in your project folder)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- DATABASE MODEL ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name}

# Create database tables automatically when app starts
with app.app_context():
    db.create_all()

# --- ROUTES ---

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the API!"}), 200


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "App is up and running!"}), 200


# GET all users from database
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


# GET single user by ID from database
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Not Found", "message": "User not found"}), 404
    return jsonify(user.to_dict()), 200


# POST create user and save to database
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Bad Request", "message": "Please provide a 'name'"}), 400
        
    new_user = User(name=data['name'])
    db.session.add(new_user)
    db.session.commit()  # Saves permanently to app.db
    
    return jsonify({"message": "User created!", "user": new_user.to_dict()}), 201


# --- ERROR HANDLERS ---

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found", "message": "The requested URL was not found."}), 404


# --- SERVER RUNNER ---

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
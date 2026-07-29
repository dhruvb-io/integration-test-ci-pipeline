import os
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database (saves to 'instance/app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- DATABASE MODEL ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name}


# Create instance directory & database tables automatically on launch
with app.app_context():
    os.makedirs(app.instance_path, exist_ok=True)
    db.create_all()


# ----------------------------
# ROUTES
# ----------------------------

# NEW - HTML Home Page
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# NEW - Form submission for Selenium/UI
@app.route("/create-user", methods=["POST"])
def create_user_form():
    name = request.form.get("name")

    if not name:
        return "Name is required", 400

    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("get_users"))


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "App is up and running!"
    }), 200


# GET all users from database
@app.route('/users', methods=['GET'])
def get_users():
    users = db.session.scalars(db.select(User)).all()
    return jsonify([user.to_dict() for user in users]), 200


# GET single user by ID from database
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({
            "error": "Not Found",
            "message": "User not found"
        }), 404

    return jsonify(user.to_dict()), 200


# API endpoint (used by Postman/Newman)
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({
            "error": "Bad Request",
            "message": "Please provide a 'name'"
        }), 400

    new_user = User(name=data['name'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User created!",
        "user": new_user.to_dict()
    }), 201


# ----------------------------
# ERROR HANDLERS
# ----------------------------

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        "error": "Not Found",
        "message": "The requested URL was not found."
    }), 404


# ----------------------------
# SERVER RUNNER
# ----------------------------

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
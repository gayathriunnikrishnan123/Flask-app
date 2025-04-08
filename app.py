from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy  12345......
db = SQLAlchemy()
#11111111
# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    fuel = db.Column(db.String(80), nullable=False)
    seat_nu = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Car {self.name}>"

def create_app():
    app = Flask(__name__)
    
    # Configure the SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize SQLAlchemy with the app
    db.init_app(app)
    
    # Create database tables when the app starts
    with app.app_context():
        db.create_all()
    
    # Define a route for the root URL.............
    @app.route('/')
    def home():
        return "Welcome to the Flask App!"
    
    @app.route('/add_car', methods=['POST'])
    def add_car():
        data = request.json
        new_car = Car(name=data['name'], fuel=data['fuel'], seat_nu=data['seat_nu'], price=data['price'])
        db.session.add(new_car)
        db.session.commit()
        return jsonify({"message": "Car added successfully!"})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

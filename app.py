from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy  12345......
db = SQLAlchemy()


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
    
    
    @app.route('/add_car', methods=['POST'])
    def items():
        print(request)
        print(request.json)
        data = request.json

        if not "price" in data:
            return jsonify({"message": "price not given"})
        if not "name" in data:
            return jsonify({"message": "name not given"})
        if not "fuel" in data:
            return jsonify({"message": "fuel not given"})
        if not "seat_nu" in data:
            return jsonify({"message": "seat number not given"})
        
        if not isinstance(data['seat_nu'],int):
             return jsonify({"message": "seat number not integer"})
        if not isinstance(data['price'],int):
             return jsonify({"message": "price not integer"})
        if not isinstance(data['fuel'],str):
             return jsonify({"message": "fuel not string"})
        if not isinstance(data['name'],str):
             return jsonify({"message": "name not string"})
        
        if Car.query.filter_by(name=data['name']):
            return jsonify({"message": "car whith this name already existing"})
        

        new_car = Car(name=data['name'], fuel=data['fuel'], seat_nu=data['seat_nu'], price=data['price'])
        db.session.add(new_car)
        db.session.commit()
        return jsonify({"message": "Car added successfully!"})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

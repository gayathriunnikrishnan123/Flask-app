from app import db
from datetime import datetime

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    fuel = db.Column(db.String(80), nullable=False)
    seat_nu = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}


class Employer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    salary = db.Column(db.Float, nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    address = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {"id": self.id, "email": self.email, "salary": self.salary}


class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    sqrft = db.Column(db.Integer, nullable=False)
    layout = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "sqrft": self.sqrft, "layout": self.layout}

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_restx import Resource, Api, fields

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
    
    def to_dict(self):
        d={"id":self.id,"name":self.name,"price":self.price}
        return d


class Employer(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False)  
    email = db.Column(db.String(100), unique=True, nullable=False) 
    age = db.Column(db.Integer, nullable=True) 
    salary = db.Column(db.Float, nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True) 
    address = db.Column(db.Text, nullable=True) 
    
    def __repr__(self):
        return f"<Employer {self.name}>"
    
    def to_dict1(self):
        d1={"id":self.id,"email":self.email,"salary":self.salary}
        return d1



class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    sqrft = db.Column(db.Integer, nullable=False)
    layout = db.Column(db.String(20), nullable=False)


    def __repr__(self):
        return f"<House{self.name}>"
    
    def to_dict2(self):
        d2={"id":self.id,"name":self.name,"sqrft":self.sqrft,"layout":self.layout}
        return d2





def create_app():
    app = Flask(__name__)
    api=Api(app)
    
    # Configure the SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize SQLAlchemy with the app
    db.init_app(app)
    
    
    # Create database tables when the app starts
    with app.app_context():
        db.create_all()
    
    
    house_model = api.model('House', {
        'name': fields.String(required=True, max_length=20, description='Name of the house'),
        'sqrft': fields.Integer(required=True, description='Square feet'),
        'layout': fields.String(required=True, max_length=20, description='Layout description')
    })

    delete_model = api.model('DeleteHouse', {
    'id': fields.Integer(required=True, description='ID of the house to delete')
    })


    @api.route('/add_house')
    class AddHome(Resource):
        @api.expect(house_model, validate=True)
        def post(self):
            data = request.json
            print(data)
            new_house = House(name=data['name'],sqrft=data['sqrft'],layout=data['layout'])
            db.session.add(new_house)
            db.session.commit()
            return {"message":"House added successfully!"}
        

    #api.add_resource(Home, '/add_house')
    
    
    
    @api.route('/drop_house')
    class DropHome(Resource):
        @api.expect(delete_model, validate=True)
        def delete(self):
            data = request.json
            id=data.get('id')
            home_to_delete = House.query.filter_by(id=id).first()

            if not home_to_delete:
                return {"message": f"No house found with id {id}"}

            db.session.delete(home_to_delete)
            db.session.commit()

            return {"message": "House deleted successfully!"}
        

    
    @api.route('/get_house')
    class GetHome(Resource):
        def get(self):
            home_to_list = House.query.all()
            result = [home.to_dict2() for home in home_to_list]
            return {"houses": result}
    
    @api.route('/change_house')
    class PutHome(Resource):
        @api.expect(house_model, validate=True)
        def put(self):
            data = request.json
            id = data.get("id")
            home_to_update = House.query.filter_by(id=id).first()
            if home_to_update:
                home_to_update.name = data['name']
                home_to_update.sqrft = data['sqrft']
                home_to_update.layout = data['layout']
                db.session.commit()
                return {"message": "House updated successfully!"}
            else:
                return {"message": "There is no house existing with this id"}




    @app.route('/add_car', methods=['POST'])
    def items():
        print(request)
        print(request.json)
        data = request.json
        print(Car.query.filter_by().all())
        print(Car.query.filter_by().first())
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
        
        if Car.query.filter_by(name=data['name']).all():
            
            return jsonify({"message": "car whith this name already existing"})
        

        new_car = Car(name=data['name'], fuel=data['fuel'], seat_nu=data['seat_nu'], price=data['price'])
        db.session.add(new_car)
        db.session.commit()
        return jsonify({"message": "Car added successfully!"})
    
    
    @app.route('/drop_car', methods=['DELETE'])
    def drop_item():
        data = request.json
        name_in_request=data['name']
        car_to_delete = Car.query.filter_by(name=name_in_request).first()
        db.session.delete(car_to_delete)
        db.session.commit()
        return jsonify({"message": "Car deleted successfully!"})
    

    @app.route('/get_car', methods=['GET'])
    def get_item():
        car_to_list = Car.query.all()
        print(car_to_list)
        new_dict=[]
        for car in car_to_list:
            car.to_dict()
            new_dict.append(car.to_dict())
        return jsonify({"message": new_dict})
    


    @app.route('/change_car', methods=['PUT'])
    def update_item():
        data = request.json
        name_in_request=data['id']
        car_to_update = Car.query.filter_by(id=name_in_request).first()
        if car_to_update:
            car_to_update.name=data['name']
            car_to_update.price=data['price']
            db.session.commit()
            return jsonify({"message": "Car updated successfully!"})
        
        else:
           return jsonify({"message": "There is no car existing in this id"})






    @app.route('/employer', methods=['POST'])
    def people():
        data = request.json
        hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d').date()
        print(data)
        new_employer = Employer(name=data['name'],email=data['email'],age=data['age'],salary=data['salary'],hire_date=hire_date,address=data['address'])
        db.session.add(new_employer)
        db.session.commit()
        return jsonify({"message": "Employer added successfully!"})


    @app.route('/drop_employer',methods=['DELETE'])
    def drop_people():
        data = request.json
        id=data['id']
        employer_to_delete = Employer.query.filter_by(id=id).first()
        db.session.delete(employer_to_delete)
        db.session.commit()
        return jsonify({"message":"employer deleted successfully"})
    
    @app.route('/get_employer',methods=['GET'])
    def get_people():
        employer_list=Employer.query.all()
        new_dict1=[]
        for employer in employer_list:
            employer.to_dict1()
            new_dict1.append(employer.to_dict1())
        return jsonify({"message": new_dict1})
    

    @app.route('/change_employer',methods=['PUT'])
    def change_people():
        data = request.json
        id=data['id']
        employer_to_update = Employer.query.filter_by(id=id).first()
        if employer_to_update:
            employer_to_update.email=data['email']
            employer_to_update.salary=data['salary']
            db.session.commit()
            return jsonify({"message": "Employer updated successfully!"})
        
        else:
           return jsonify({"message": "There is no employer existing in this id"})



    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

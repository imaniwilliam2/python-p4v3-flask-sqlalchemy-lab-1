# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()

    if earthquake:
        body = earthquake.to_dict()
        status = 200
    else:
        body = {'message': f'Earthquake {id} not found.'}
        status = 404

    return make_response(body, status)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_min_mag(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()


    if earthquakes:
      earthquake_dicts = [earthquake.to_dict() for earthquake in earthquakes]
      body = {'count': len(earthquakes),
              'earthquakes': earthquake_dicts
              }
      status = 200
        
    else:
        body = {'count': len(earthquakes),
                'quakes': [],
                'message': f'Earthquake with {magnitude} magnitude not found.'}
        status = 200

    return make_response(body, status)


if __name__ == '__main__':
    app.run(port=5555, debug=True)

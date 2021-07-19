"""Flask app for Cupcakes"""


from flask import Flask, request
from flask.json import jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/api/cupcakes')
def get_all_cupcakes():
    '''Returns JSON with data on all cupcakes
       {cupcakes : [{id, flavor, size, rating, image}, ...]}
    '''
    
    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    '''Returns JSON with data on specific cupcake
       {cupcake : {id, flavor, size, rating, image}}
    '''

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    '''Returns JSON with data on created cupcake and code 201
       {cupcake : {id, flavor, size, rating, image}}
    '''

    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image'] or None

    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    
    db.session.add(cupcake)
    db.session.commit()

    serialized = cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)


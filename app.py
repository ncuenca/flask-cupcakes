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

    # question: should we change request.json['image']? Which format is better?
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image'] if 'image' in request.json.keys() else None
    # image = request.json['image'] or None


    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    
    db.session.add(cupcake)
    db.session.commit()

    serialized = cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Returns JSON with data updated on a specific cupcake
        {cupcake : {id, flavor, size, rating, image}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    # for key in ['flavor', 'size', 'rating', 'image']:
    #     request.json.get(key, cupcake.key)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor) # this is the best way: straightforward
    # setattr(cupcake, key, request.json[key]) # option 2 (review in further study)

    # didn't work: because request.json['rating'] throws an error unless rating is in JSON data
    # cupcake.flavor = request.json['flavor'] or cupcake.flavor
    # cupcake.size = request.json['size'] or cupcake.size
    # cupcake.rating = request.json['rating'] or cupcake.rating
    # cupcake.image = request.json['image'] or cupcake.image

    # didn't work: why?
    # for key in request.json.keys():
    #     print(key)
    #     print(request.json[f'{key}'])
    #     cupcake.key = request.json[f'{key}']

    # this worked
    cupcake.flavor = request.json['flavor'] if 'flavor' in request.json.keys() else cupcake.flavor
    cupcake.size = request.json['size'] if 'size' in request.json.keys() else cupcake.size
    cupcake.rating = request.json['rating'] if 'rating' in request.json.keys() else cupcake.rating
    cupcake.image = request.json['image'] if 'image' in request.json.keys() else cupcake.image  

    db.session.commit()

    serialized = cupcake.serialize()
    
    return jsonify(cupcake=serialized) 

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Handles the deletion of the data for an existing cupcake. 
       Returns JSON: {message: "Deleted"} """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit() 

    return (jsonify(message='Deleted'))     
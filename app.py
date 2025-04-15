from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta
from models import db, Heroes, Powers, Hero_powers

app = Flask(__name__)

# Database and JWT Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hero.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Prevents a warning
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)
app.config['JWT_SECRET_KEY'] = 'cnjshsbvhsbhjavbjvidjijfvdk'

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

@app.route('/')
def home():
    return 'Hello Flask App'

# Get all heroes
@app.route('/heroes', methods=['GET'])
def heroes():
    heroes_list = []
    for hero in Heroes.query.all(): 
        hero_dict = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        }
        heroes_list.append(hero_dict)

    return jsonify(heroes_list)

# Get hero by ID
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Heroes.query.get(id)  
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404

    hero_dict = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': []
    }

    for power in hero.powers:
        hero_dict['powers'].append({
            'id': power.id,
            'name': power.name,
            'description': power.description
        })

    return jsonify(hero_dict)

# Get all powers
@app.route('/powers', methods=['GET'])
def powers():
    powers_list = []
    for power in Powers.query.all():  
        powers_list.append({
            'id': power.id,
            'name': power.name,
            'description': power.description
        })

    return jsonify(powers_list)

# Get power by ID
@app.route('/powers/<int:id>', methods=['GET'])
def fetch_power(id):
    power = Powers.query.get(id)  
    if not power:
        return jsonify({'error': 'Power not found'}), 404

    return jsonify({
        'id': power.id,
        'name': power.name,
        'description': power.description
    })

# Update hero details
@app.route('/heroes/<int:id>', methods=['PATCH'])
def update_hero(id):
    data = request.get_json()
    hero = Heroes.query.get(id)  

    if not hero:
        return jsonify({'error': 'Hero not found'}), 404

    if 'name' in data:
        hero.name = data['name']
    if 'super_name' in data:
        hero.super_name = data['super_name']

    db.session.commit()

    return jsonify({'message': 'Hero updated successfully'}), 200

# Update power details
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Powers.query.get(id)  

    if not power:
        return jsonify({'error': 'Power not found'}), 404

    data = request.get_json()
    if "description" not in data:
        return jsonify({'error': 'Description field is required'}), 400

    power.description = data["description"]
    db.session.commit()

    return jsonify({
        'id': power.id,
        'name': power.name,
        'description': power.description
    })

# Assign a power to a hero
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    # Validate the required fields
    if "strength" not in data or "power_id" not in data or "hero_id" not in data:
        return jsonify({"errors": ["strength, power_id, and hero_id fields are required"]}), 400

    hero = Heroes.query.get(data["hero_id"])  
    power = Powers.query.get(data["power_id"]) 

    if not hero or not power:
        return jsonify({"errors": ["Power or Hero not found"]}), 404

    # Create the Hero_powers relationship
    hero_power = Hero_powers(strength=data["strength"], hero=hero, power=power)

    try:
        db.session.add(hero_power)
        db.session.commit()
        return jsonify({
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)

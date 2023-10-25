#!/usr/bin/env python3

from flask import Flask, request, jsonify,make_response
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
#db.init_app(app)


@app.route('/')
def home():
    return ''


@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_data = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(hero_data)


@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if hero:
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
        }
        return jsonify(hero_data)
    else:
        return jsonify({"error": "Hero not found"}), 404


@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_data = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(power_data)


@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power(power_id):
    power = Power.query.get(power_id)
    if power:
        power_data = {'id': power.id, 'name': power.name, 'description': power.description}
        return jsonify(power_data)
    else:
        return jsonify({"error": "Power not found"}), 404


@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)
    if power:
        data = request.get_json()
        if 'description' in data:
            power.description = data['description']
            db.session.commit()
            return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
        else:
            return jsonify({'errors': ['No description provided']}), 400
    else:
        return jsonify({"error": "Power not found"}), 404


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if hero and power:
        if strength in ['Strong', 'Weak', 'Average']:
            hero_power = HeroPower(hero=hero, power=power, strength=strength)
            db.session.add(hero_power)
            db.session.commit()
            return jsonify({
                'id': hero.id,
                'name': hero.name,
                'super_name': hero.super_name,
                'powers': [{'id': p.id, 'name': p.name, 'description': p.description} for p in hero.powers]
            }), 201
        else:
            return jsonify({'errors': ['Invalid strength value']}), 400
    else:
        return jsonify({'errors': ['Hero or Power not found']}), 400

if __name__ == '__main__':
    app.run(port=5555)




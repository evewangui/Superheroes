from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy ()

class Heroes (db.Model):
    id = db.Column (db.Integer, primary_key = True)
    name = db.Column (db.String (64), nullable = False)
    super_name = db.Column (db.String (64), nullable = False)
    hero = db.relationship ('Hero_powers', backref = 'hero', lazy = True)

class Hero_powers (db.Model):
    id = db.Column (db.Integer, primary_key = True)
    strength = db.Column (db.String (64), nullable = False)
    hero_id = db.Column (db.Integer, db.ForeignKey ('heroes.id'), nullable = False)
    power_id = db.Column (db.Integer, db.ForeignKey ('powers.id'), nullable = False)

    #validates(strength)
    def validate_strength(self, key, value):
        allowed_values = ['Strong', 'Weak', 'Average']
        if value not in allowed_values:
            raise ValueError(f"Strength must be one of {allowed_values}")
        return value

class Powers (db.Model):
    id = db.Column (db.Integer, primary_key = True)
    name = db.Column (db.String (64), nullable = False)
    description = db.Column (db.String (64), nullable = False)
    hero = db.relationship ('Hero_powers', backref = 'power', lazy = True)

    #validates(description)
    def validate_description(self, key, value):
        if not value:
            raise ValueError("Description cannot be empty.")
        if len(value) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return value
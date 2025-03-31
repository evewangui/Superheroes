from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = "heroes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "super_name": self.super_name
        }


class Power(db.Model):
    __tablename__ = "powers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    hero_powers = db.relationship('HeroPower', back_populates='power', cascade="all, delete")

    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return description

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class HeroPower(db.Model):
    __tablename__ = "hero_powers"

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey("heroes.id"), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey("powers.id"), nullable=False)
    strength = db.Column(db.String, nullable=False)

    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ["Strong", "Weak", "Average"]
        if strength not in valid_strengths:
            raise ValueError(f"Strength must be one of {valid_strengths}")
        return strength

    def to_dict(self):
        return {
            "id": self.id,
            "hero_id": self.hero_id,
            "power_id": self.power_id,
            "strength": self.strength,
            "hero": self.hero.to_dict(),
            "power": self.power.to_dict()
        }


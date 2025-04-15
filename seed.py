from random import choice as rc

from app import app
from models import db, Heroes, Powers, Hero_powers

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        Powers.query.delete()
        Heroes.query.delete()
        Hero_powers.query.delete()

        print("Seeding powers...")
        powers = [
           Powers(name="super strength", description="gives the wielder super-human strengths"),
           Powers(name="flight", description="gives the wielder the ability to fly through the skies at supersonic speed"),
           Powers(name="super human senses", description="allows the wielder to use her senses at a super-human level"),
           Powers(name="elasticity", description="can stretch the human body to extreme lengths"),
        ]

        db.session.add_all(powers)

        print("Seeding heroes...")
        heroes = [
            Heroes(name="Kamala Khan", super_name="Ms. Marvel"),
            Heroes(name="Doreen Green", super_name="Squirrel Girl"),
            Heroes(name="Gwen Stacy", super_name="Spider-Gwen"),
            Heroes(name="Janet Van Dyne", super_name="The Wasp"),
            Heroes(name="Wanda Maximoff", super_name="Scarlet Witch"),
            Heroes(name="Carol Danvers", super_name="Captain Marvel"),
            Heroes(name="Jean Grey", super_name="Dark Phoenix"),
            Heroes(name="Ororo Munroe", super_name="Storm"),
            Heroes(name="Kitty Pryde", super_name="Shadowcat"),
            Heroes(name="Elektra Natchios", super_name="Elektra"),
        ]

        db.session.add_all(heroes)

        print("Adding powers to heroes...")
        strengths = ["Strong", "Weak", "Average"]
        hero_powers = []
        for hero in heroes:
            power = rc(powers)
            hero_powers.append(
                Hero_powers(hero=hero, power=power, strength=rc(strengths))
            )
        db.session.add_all(hero_powers)
        db.session.commit()

        print("Done seeding!")
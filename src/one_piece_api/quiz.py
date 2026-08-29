from sqlalchemy import func 
from .models import CharacterDB
import random 

def create_crew_question(db, character):
    correct_answer = character.crew 

    other_crews = db.query(CharacterDB.crew).filter(
        CharacterDB.crew != correct_answer,
        CharacterDB.crew.isnot(None)
    ).distinct().order_by(
        func.random()
    ).limit(3).all()

    possible_answers = [correct_answer]

    for crew in other_crews:
        possible_answers.append(crew[0])

    random.shuffle(possible_answers)

    return {
        "question":f"What crew does {character.name} belong to?",
        "answers":possible_answers
    }

def create_affiliation_question(db, character):
    correct_answer = character.affiliation 

    other_affiliations = db.query(CharacterDB.affiliation).filter(
        CharacterDB.affiliation != correct_answer,
        CharacterDB.affiliation.isnot(None)
    ).distinct().order_by(
        func.random()
    ).limit(3).all()

    possible_answers = [correct_answer]

    for affiliation in other_affiliations:
        possible_answers.append(affiliation[0])

    random.shuffle(possible_answers)

    return {
        "question":f"What affiliation does {character.name} belong to?",
        "answers":possible_answers
    }

def create_devil_fruit_question(db, character):
    correct_answer = character.devil_fruit 

    other_fruits = db.query(CharacterDB.devil_fruit).filter(
        CharacterDB.devil_fruit != correct_answer,
        CharacterDB.devil_fruit.isnot(None)
    ).distinct().order_by(
        func.random()
    ).limit(3).all()

    possible_answers = [correct_answer]

    for fruit in other_fruits:
        possible_answers.append(fruit[0])

    random.shuffle(possible_answers)

    return {
        "question":f"What Devil Fruit does {character.name} have?",
        "answers":possible_answers
    }

def create_bounty_question(db, character):
    correct_answer = character.bounty 
    other_bounties = db.query(CharacterDB.bounty).filter(
        CharacterDB.bounty != correct_answer,
        CharacterDB.bounty.isnot(None)
    ).distinct().order_by(
        func.random()
    ).limit(3).all()

    possible_answers = [correct_answer]

    for bounty in other_bounties:
        possible_answers.append(bounty[0])

    random.shuffle(possible_answers)

    return {
        "question": f"What is {character.name}'s bounty?",
        "answers": possible_answers
    }


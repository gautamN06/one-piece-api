from fastapi import FastAPI, HTTPException 
from sqlalchemy import func 
import random 

from .database import SessionLocal, engine, Base 
from .models import CharacterDB
from .schemas import Character 

from .quiz import (
    create_crew_question,
    create_affiliation_question,
    create_devil_fruit_question,
    create_bounty_question
)

Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/character")
def get_characters(
    crew: str | None = None,
    affiliation: str |None = None
):
    db = SessionLocal()

    query = db.query(CharacterDB)

    if crew:
        query=query.filter(
            CharacterDB.crew.ilike(f"%{crew}%")
        )

    if affiliation:
        query=query.filter(
            CharacterDB.affiliation.ilike(f"%{affiliation}%")
        )

    characters = query.all()

    db.close()
    if not characters: 
        raise HTTPException(
            status_code=404,
            detail="No characters found! :("
        )
    
    return characters 

@app.get("/quiz/random")
def random_quiz():
    db = SessionLocal()

    question_type = random.choice([
        "crew",
        "affiliation",
        "devil_fruit",
        "bounty"
    ])

    if question_type == "crew":
        character = db.query(CharacterDB).filter(
            CharacterDB.crew.isnot(None)
        ).order_by(
            func.random()
        ).first()

        question = create_crew_question(db, character)

    elif question_type == "affiliation":
        character = db.query(CharacterDB).filter(
            CharacterDB.affiliation.isnot(None)
        ).order_by(
            func.random()
        ).first()

        question = create_affiliation_question(db, character)

    elif question_type == "devil_fruit":
        character = db.query(CharacterDB).filter(
            CharacterDB.devil_fruit.isnot(None)
        ).order_by(
            func.random()
        ).first()

        question = create_devil_fruit_question(db, character)
    
    elif question_type == "bounty":
        character = db.query(CharacterDB).filter(
            CharacterDB.bounty.isnot(None)
        ).order_by(
            func.random()
        ).first()

        question = create_bounty_question(db, character)


    db.close()

    return question 

  

@app.get("/characteres/random")
def search_random():
    db = SessionLocal()

    character = db.query(CharacterDB).order_by(
        func.random()
    ).first()

    db.close()

    if character is None:
        raise HTTPException(
            status_code=404,
            detail="No Characters in database! :("
        )

    return character 

@app.get("/characters/search/{affiliation}")
def search_affiliation(affiliation: str):
    db = SessionLocal()
    characters = db.query(CharacterDB).filter(
        CharacterDB.affiliation.ilike(f"%{affiliation}%")
    ).all()
    db.close() 
    
    if not characters:
        raise HTTPException(
            status_code=404,
            detail="Members of this affiliation not found! :("
        )
    return characters 

@app.get("/characters/{character_id}")
def get_character(character_id: int):
    db = SessionLocal()
    character = db.query(CharacterDB).filter(
        CharacterDB.id == character_id
    ).first()
    db.close()

    if character is None:
        raise HTTPException(
            status_code=404,
            detail="Character not found!:("
        )

    return character 

@app.get("/characters/search/{name}")
def search_character(name: str):
    db = SessionLocal()
    characters = db.query(CharacterDB).filter(
        CharacterDB.name.ilike(f"%{name}%")  #%{name}% - anything can come before and after name 
        ).all()
    db.close()

    if characters is None:
        raise HTTPException(
            status_code=404,
            detail="No characters not found! :("
        )
    return characters

@app.post("/characters/search/{crew}")
def search_crew(crew: str):
    db = SessionLocal()
    characters = db.query(CharacterDB).filter(
        CharacterDB.crew.ilike(f"%{crew}%")
    ).all()
    db.close()

    if characters is None:
        raise HTTPException(
            status_code=404,
            detail="Not able to find crew! :("
        )
    return characters 

@app.post("/characters")
def create_character(character: Character):
    db = SessionLocal()
    new_character = CharacterDB(
        name=character.name,
        age=character.age,
        affiliation=character.affiliation,
        crew=character.crew,
        devil_fruit=character.devil_fruit,
        devil_fruit_type=character.devil_fruit_type, 
        bounty=character.bounty, 
        status=character.status 
    )
    db.add(new_character)
    db.commit()
    db.refresh(new_character)
    db.close()

    return new_character 

@app.put("/characters/{character_id}")
def update_character(character_id: int, character: Character):
    db = SessionLocal()

    db_character = db.query(CharacterDB).filter(
        CharacterDB.id == character_id
    ).first()

    if db_character is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Character not found :("
        )

    db_character.name = character.name
    db_character.age = character.age 
    db_character.affiliation = character.affiliation
    db_character.crew = character.crew
    db_character.devil_fruit = character.devil_fruit 
    db_character.devil_fruit_type = character.devil_fruit_type
    db_character.bounty = character.bounty 
    db_character.status = character.status 

    db.commit()
    db.refresh(db_character)
    db.close() 

    return db_character 

@app.delete("/characters/{character_id}")
def delete_character(character_id: int):
    db = SessionLocal()
    db_character = db.query(CharacterDB).filter(
        CharacterDB.id == character_id 
    ).first()

    if db_character is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Character not found :("
        )

    db.delete(db_character)
    db.commit()
    db.close()

    return{
        "message":f"{db_character.name} was deleted!"
    }
    


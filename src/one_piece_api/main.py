from fastapi import FastAPI, HTTPException 
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func 
import random 

from .database import SessionLocal, engine, Base 
from .models import CharacterDB, QuizSession
from .schemas import Character, QuizAnswer, QuizSubmission


from .quiz import (
    create_crew_question,
    create_affiliation_question,
    create_devil_fruit_question,
    create_bounty_question
)

Base.metadata.create_all(engine)
print(Base.metadata.tables.keys())

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/quiz")
def create_quiz():
    db = SessionLocal()

    questions = []
    used_questions = set()

    while len(questions) < 10:
        question_type = random.choice([
            "crew",
            "affiliation",
            "devil_fruit",
            "bounty"
        ])

        if question_type=="crew":
            character = db.query(CharacterDB).filter(
                CharacterDB.crew.isnot(None)
            ).order_by(
                func.random()
            ).first() 

          

        elif question_type == "affiliation":
            character = db.query(CharacterDB).filter(
                CharacterDB.affiliation.isnot(None)
            ).order_by(
                func.random()
            ).first()

            

        elif question_type == "devil_fruit":
            character = db.query(CharacterDB).filter(
                CharacterDB.devil_fruit.isnot(None)
            ).order_by(
                func.random()
            ).first()

            

        elif question_type == "bounty":
            character = db.query(CharacterDB).filter(
                CharacterDB.bounty.isnot(None)
            ).order_by(
                func.random()
            ).first()

        question_key = (character.id, question_type)

        if question_key in used_questions:
            continue 

        used_questions.add(question_key)

        if question_type == "crew":
            question = create_crew_question(db, character)
        elif question_type == "affiliation":
            question = create_affiliation_question(db, character)
        elif question_type == "devil_fruit":
            question = create_devil_fruit_question(db, character)
        elif question_type == "bounty":
            question = create_bounty_question(db, character)

        questions.append(question)

    db.close()
    

    return {
        "total_questions": len(questions),
        "questions" : questions 
    }

@app.post("/quiz/answer")
def check_answer(quiz_answer: QuizAnswer):
    db = SessionLocal()

    character = db.query(CharacterDB).filter(
        CharacterDB.id == quiz_answer.character_id
    ).first()

    db.close() 

    if character is None: 
        raise HTTPException(
            status_code=404,
            detail="Character not found!"
        )

    if quiz_answer.question_type == "crew":
        correct_answer = character.crew 
    elif quiz_answer.question_type == "affiliation":
        correct_answer = character.affiliation
    elif quiz_answer.question_type == "devil_fruit":
        correct_answer = character.devil_fruit 
    elif quiz_answer.question_type == "bounty":
        correct_answer = character.bounty 

    else:
        raise HTTPException(
            status_code=404,
            detail="Invalid question type!"
        )

    if str(correct_answer).lower() == quiz_answer.answer.lower():
        return{
            "correct":True,
            "message":"Correct!"
        }

    return {
        "correct": False, 
        "message" : "Incorrect!",
        "correct_answer": correct_answer
    }

@app.get("/characters")
def get_characters(
    crew: str | None = None,
    affiliation: str | None = None
):
    db = SessionLocal()

    query = db.query(CharacterDB)

    if crew:
        query = query.filter(
            CharacterDB.crew.ilike(f"%{crew}%")
        )

    if affiliation:
        query = query.filter(
            CharacterDB.affiliation.ilike(f"%{affiliation}%")
        )

    characters = query.all()

    db.close()

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
        status=character.status,
        image_url = character.image_url
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
    db_character.image_url = character.image_url

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
    


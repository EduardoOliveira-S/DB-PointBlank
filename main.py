from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Account

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE
@app.post("/accounts")
def create_account(login: str, password: str, db: Session = Depends(get_db)):
    new_acc = Account(login=login, password=password)
    db.add(new_acc)
    db.commit()
    db.refresh(new_acc)
    return new_acc


# READ ALL
@app.get("/ken10")
def read_accounts():
    return {"message": "Criada por K10"}


# READ ALL
@app.get("/accounts")
def read_accounts(db: Session = Depends(get_db)):
    return db.query(Account).all()


# READ ONE
@app.get("/accounts/{player_id}")
def read_account(player_id: int, db: Session = Depends(get_db)):
    acc = db.query(Account).filter(Account.player_id == player_id).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Account não encontrada")
    return acc


# UPDATE
@app.put("/accounts/{player_id}")
def update_account(
    player_id: int, login: str = None, password: str = None, rank: int = None, db: Session = Depends(get_db)
):
    acc = db.query(Account).filter(Account.player_id == player_id).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Account não encontrada")

    if login is not None:
        acc.login = login
    if password is not None:
        acc.password = password
    if rank is not None:
        acc.rank = rank

    db.commit()
    db.refresh(acc)
    return acc


# DELETE
@app.delete("/accounts/{player_id}")
def delete_account(player_id: int, db: Session = Depends(get_db)):
    acc = db.query(Account).filter(Account.player_id == player_id).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Account não encontrada")

    db.delete(acc)
    db.commit()
    return {"message": "Account deletada com sucesso"}


from fastapi.responses import RedirectResponse


@app.get("/")
def root():
    return RedirectResponse(url="/docs")

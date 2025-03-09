from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"

DATABASE_URL = "mssql+pyodbc://@ANBU-PC\SQLEXPRESS/books?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserDB(Base):
    __tablename__ = "user_details"
    userid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(20), unique=True, index=True)
    password = Column(String(256))

class BookDB(Base):
    __tablename__ = "user_books"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(20), index=True)
    author = Column(String(20), index=True)

Base.metadata.create_all(bind=engine)

class Book(BaseModel):
    title: str
    author: str
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    print("Hashed Password:", hashed_password)  # Debugging line
    db_user = UserDB(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = db.query(UserDB).filter(UserDB.username == username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@app.post("/books/")
def create_book(book: Book, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    db_book = BookDB(title=book.title, author=book.author)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return {"book": db_book}

@app.get("/books/")
def get_books(db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    books = db.query(BookDB).all()
    return {"books": books}

@app.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"book": book}

@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = updated_book.title
    book.author = updated_book.author
    db.commit()
    db.refresh(book)
    return {"book": book}

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}

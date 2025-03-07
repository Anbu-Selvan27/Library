from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pyodbc

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    publication_year: int
    id: int = None  

server = r'ANBU-PC\SQLEXPRESS'  
database = 'book' 
driver= '{ODBC Driver 17 for SQL Server}' 

def get_db_connection():
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    return pyodbc.connect(conn_str)

@app.post("/books/", response_model=Book)
def create_book(book: Book):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Book1 (title, author, publication_year) VALUES (?, ?, ?); SELECT SCOPE_IDENTITY()",
                   book.title, book.author, book.publication_year)
    book_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return Book(id=book_id, **book.dict()) 

@app.get("/books/", response_model=List[Book])
def read_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, publication_year FROM Book1") 
    rows = cursor.fetchall()
    conn.close()
    return [Book(id=row.id, title=row.title, author=row.author, publication_year=row.publication_year) for row in rows] 

@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, publication_year FROM Book1 WHERE id = ?", book_id) 
    row = cursor.fetchone()
    conn.close()
    if row:
        return Book(id=row.id, title=row.title, author=row.author, publication_year=row.publication_year) 
    else:
        raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Book1 SET title = ?, author = ?, publication_year = ? WHERE id = ?", 
                   updated_book.title, updated_book.author, updated_book.publication_year, book_id)
    conn.commit()
    conn.close()
    return Book(id=book_id, **updated_book.dict()) 

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Book1 WHERE id = ?", book_id) 
    conn.commit()
    conn.close()
    return {"message": "Book deleted"}
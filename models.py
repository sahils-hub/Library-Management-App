from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# -----------------------------
# Database Connection
# -----------------------------
# Replace YOUR_PASSWORD with your MySQL root password
engine = create_engine("mysql+pymysql://root:password1@localhost/library_db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# -----------------------------
# Book Model
# -----------------------------
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    author = Column(String(50))
    publisher = Column(String(50))
    category = Column(String(30))
    copies = Column(Integer)

# -----------------------------
# Student Model
# -----------------------------
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    roll_no = Column(String(20))
    department = Column(String(30))

# -----------------------------
# Transaction Model
# -----------------------------
class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    student_id = Column(Integer, ForeignKey('students.id'))
    issue_date = Column(Date)
    due_date = Column(Date)
    return_date = Column(Date, nullable=True)
    status = Column(String(20))

    book = relationship("Book")
    student = relationship("Student")

# -----------------------------
# Create tables if they don't exist
# -----------------------------
Base.metadata.create_all(engine)

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date, timedelta
from models import Book, Student, Transaction, session


# -----------------------------
# MySQL Database Connection
# -----------------------------
engine = create_engine("mysql+pymysql://root:password1@localhost/library_db")  # <- change password
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# -----------------------------
# SQLAlchemy Models
# -----------------------------
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    author = Column(String(50))
    publisher = Column(String(50))
    category = Column(String(30))
    copies = Column(Integer)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    roll_no = Column(String(20))
    department = Column(String(30))

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

# Create tables
Base.metadata.create_all(engine)

# -----------------------------
# Streamlit App UI
# -----------------------------
st.title("📚 Library Management System")

menu = ["Home", "Books", "Students", "Issue/Return", "Reports"]
choice = st.sidebar.selectbox("Menu", menu)

# -----------------------------
# Home
# -----------------------------
if choice == "Home":
    st.subheader("Welcome to the Library Management System")
    st.write("Use the menu to navigate: manage books, students, issue/return books, and view reports.")

# -----------------------------
# Books
# -----------------------------
elif choice == "Books":
    st.subheader("Manage Books")

    # Add new book
    st.markdown("### Add / Edit Book")
    book_id = st.text_input("Book ID (leave blank to add new)")
    title = st.text_input("Title")
    author = st.text_input("Author")
    publisher = st.text_input("Publisher")
    category = st.text_input("Category")
    copies = st.number_input("Copies", min_value=1, value=1)

    if st.button("Save Book"):
        if book_id:
            # Update existing
            book = session.query(Book).filter_by(id=int(book_id)).first()
            if book:
                book.title = title
                book.author = author
                book.publisher = publisher
                book.category = category
                book.copies = copies
                session.commit()
                st.success("Book updated successfully!")
        else:
            # Add new
            new_book = Book(title=title, author=author, publisher=publisher, category=category, copies=copies)
            session.add(new_book)
            session.commit()
            st.success("Book added successfully!")

    # List all books
    st.markdown("### Book List")
    books = pd.read_sql(session.query(Book).statement, session.bind)
    st.dataframe(books)

    # Delete book
    del_id = st.text_input("Enter Book ID to Delete")
    if st.button("Delete Book"):
        book = session.query(Book).filter_by(id=int(del_id)).first()
        if book:
            session.delete(book)
            session.commit()
            st.success("Book deleted successfully!")

# -----------------------------
# Students
# -----------------------------
elif choice == "Students":
    st.subheader("Manage Students")

    student_id = st.text_input("Student ID (leave blank to add new)")
    name = st.text_input("Name")
    roll_no = st.text_input("Roll Number")
    dept = st.text_input("Department")

    if st.button("Save Student"):
        if student_id:
            student = session.query(Student).filter_by(id=int(student_id)).first()
            if student:
                student.name = name
                student.roll_no = roll_no
                student.department = dept
                session.commit()
                st.success("Student updated successfully!")
        else:
            new_student = Student(name=name, roll_no=roll_no, department=dept)
            session.add(new_student)
            session.commit()
            st.success("Student added successfully!")

    # List all students
    st.markdown("### Student List")
    students = pd.read_sql(session.query(Student).statement, session.bind)
    st.dataframe(students)

    # Delete student
    del_id = st.text_input("Enter Student ID to Delete")
    if st.button("Delete Student"):
        student = session.query(Student).filter_by(id=int(del_id)).first()
        if student:
            session.delete(student)
            session.commit()
            st.success("Student deleted successfully!")

# -----------------------------
# Issue / Return
# -----------------------------
elif choice == "Issue/Return":
    st.subheader("Issue / Return Books")

    trans_menu = ["Issue Book", "Return Book"]
    trans_choice = st.selectbox("Action", trans_menu)

    if trans_choice == "Issue Book":
        student_id = st.number_input("Student ID", min_value=1)
        book_id = st.number_input("Book ID", min_value=1)
        issue_date = st.date_input("Issue Date", value=date.today())
        due_date = issue_date + timedelta(days=14)

        if st.button("Issue Book"):
            book = session.query(Book).filter_by(id=book_id).first()
            if book and book.copies > 0:
                book.copies -= 1
                new_trans = Transaction(book_id=book_id, student_id=student_id,
                                        issue_date=issue_date, due_date=due_date, status="Issued")
                session.add(new_trans)
                session.commit()
                st.success(f"Book issued! Due date: {due_date}")
            else:
                st.error("Book not available")

    elif trans_choice == "Return Book":
        trans_id = st.number_input("Transaction ID", min_value=1)
        if st.button("Return Book"):
            trans = session.query(Transaction).filter_by(id=trans_id, status="Issued").first()
            if trans:
                trans.status = "Returned"
                trans.return_date = date.today()
                book = session.query(Book).filter_by(id=trans.book_id).first()
                book.copies += 1
                session.commit()
                st.success("Book returned successfully!")
            else:
                st.error("Transaction not found or already returned")

# -----------------------------
# Reports
# -----------------------------
elif choice == "Reports":
    st.subheader("Reports")
    report_menu = ["Issued Books", "Overdue Books", "Student History"]
    report_choice = st.selectbox("Report Type", report_menu)

    if report_choice == "Issued Books":
        df = pd.read_sql(session.query(Transaction).filter_by(status="Issued").statement, session.bind)
        st.dataframe(df)

    elif report_choice == "Overdue Books":
        today = date.today()
        df = pd.read_sql(session.query(Transaction).filter(Transaction.status=="Issued", Transaction.due_date<today).statement, session.bind)
        st.dataframe(df)

    elif report_choice == "Student History":
        student_id = st.number_input("Enter Student ID", min_value=1)
        df = pd.read_sql(session.query(Transaction).filter_by(student_id=student_id).statement, session.bind)
        st.dataframe(df)

    if st.button("Export Report as CSV"):
        if report_choice == "Issued Books":
            df.to_csv("issued_books_report.csv", index=False)
        elif report_choice == "Overdue Books":
            df.to_csv("overdue_books_report.csv", index=False)
        elif report_choice == "Student History":
            df.to_csv(f"student_{student_id}_history.csv", index=False)
        st.success("CSV Exported successfully!")

from models import Book, Student, session

# -----------------------------
# Sample Books
# -----------------------------
books = [
    {"title": "The Alchemist", "author": "Paulo Coelho", "publisher": "HarperOne", "category": "Fiction", "copies": 5},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "publisher": "J.B. Lippincott & Co.", "category": "Classic", "copies": 4},
    {"title": "1984", "author": "George Orwell", "publisher": "Secker & Warburg", "category": "Dystopian", "copies": 6},
    {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "publisher": "Bloomsbury", "category": "Fantasy", "copies": 8},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "publisher": "T. Egerton", "category": "Classic", "copies": 3},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "publisher": "Charles Scribner's Sons", "category": "Classic", "copies": 4},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "publisher": "George Allen & Unwin", "category": "Fantasy", "copies": 5},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "publisher": "Little, Brown and Company", "category": "Fiction", "copies": 4},
    {"title": "The Da Vinci Code", "author": "Dan Brown", "publisher": "Doubleday", "category": "Thriller", "copies": 6},
    {"title": "The Hunger Games", "author": "Suzanne Collins", "publisher": "Scholastic Press", "category": "Dystopian", "copies": 5},
]

for b in books:
    book = Book(**b)
    session.add(book)

# -----------------------------
# Sample Students
# -----------------------------
students = [
    {"name": "Aarav Sharma", "roll_no": "CS101", "department": "Computer Science"},
    {"name": "Priya Singh", "roll_no": "CS102", "department": "Computer Science"},
    {"name": "Rahul Mehta", "roll_no": "EE201", "department": "Electrical Engineering"},
    {"name": "Sneha Patil", "roll_no": "EE202", "department": "Electrical Engineering"},
    {"name": "Ananya Kapoor", "roll_no": "ME301", "department": "Mechanical Engineering"},
    {"name": "Rohan Deshmukh", "roll_no": "ME302", "department": "Mechanical Engineering"},
    {"name": "Karan Verma", "roll_no": "CE401", "department": "Civil Engineering"},
    {"name": "Nisha Rao", "roll_no": "CE402", "department": "Civil Engineering"},
    {"name": "Ishita Gupta", "roll_no": "IT501", "department": "Information Technology"},
    {"name": "Arjun Joshi", "roll_no": "IT502", "department": "Information Technology"},
]

for s in students:
    student = Student(**s)
    session.add(student)

# Commit all changes
session.commit()
print("Sample books and students inserted successfully!")

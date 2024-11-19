from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Add a new book (POST)
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(
        book_name=data['book_name'],
        author=data['author'],
        publisher=data['publisher']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added successfully!"}), 201

# Retrieve all books (GET)
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    books_list = [{"id": b.id, "book_name": b.book_name, "author": b.author, "publisher": b.publisher} for b in books]
    return jsonify(books_list)

# Update a specific book (PUT)
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    book.book_name = data.get('book_name', book.book_name)
    book.author = data.get('author', book.author)
    book.publisher = data.get('publisher', book.publisher)
    db.session.commit()
    return jsonify({"message": "Book updated successfully!"})

# Delete a specific book (DELETE)
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully!"})

# Home route (optional)
@app.route('/')
def home():
    return "Welcome to the Book API!"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

import sqlite3
import requests
from flask import Flask, request, jsonify


app = Flask(__name__)


conn = sqlite3.connect('books.db')
conn.execute('CREATE TABLE books (id INTEGER PRIMARY KEY AUTOINCREMENT, '
             'name TEXT, isbn INTEGER, authors TEXT, '
             'number_of_pages INTEGER, publisher TEXT, '
             'Country TEXT, release_date TEXT)')
conn.close()


@app.route("/api/external-books/<book_name>", methods=['GET'])
def get_book(book_name):
    resp_value = requests.get('https://www.anapioficeandfire.com/api/books')
    resp_value = resp_value.json()
    for item in resp_value:
        if item['name'] == book_name:
            keys = item.keys()
            resp_data = {}
            for key in keys:
                if key not in ['povCharacters', 'characters', 'mediaType']:
                    resp_data[key] = item.get(key)
            resp_val = {"status_code": 200, "status": "success", "data": [resp_data]}
            return jsonify(resp_val), 200
    else:
        data = {"status_code": 200, "status": "success", "data": []}
        return jsonify(data), 200


@app.route("/api/v1/books/", methods=['POST'])
def post_database_book():
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    name = request.args.get('name')
    isbn = request.args.get('isbn')
    authors = request.args.get('authors')
    number_of_pages = request.args.get('number_of_pages')
    publisher = request.args.get('publisher')
    country = request.args.get('country')
    release_date = request.args.get('release_date')
    cur.execute("INSERT into books (name, isbn, authors, number_of_pages, "
                "publisher, country, release_date) "
                "values (?,?,?,?,?,?,?)", (name, isbn, authors,
                                           number_of_pages, publisher, country,
                                           release_date))
    conn.commit()
    response = {
        "status_code": 201,
        "status": "success",
        "data": [
            {
                "book":
                    {
                        "name": name,
                        "isbn": isbn,
                        "authors": [authors],
                        "number_of_pages": number_of_pages,
                        "publisher": publisher,
                        "country": country,
                        "release_date": release_date
                    }
            }
        ]
    }
    return jsonify(response), 201


@app.route('/api/v1/books', methods=['GET'])
def get_database_books():
    data = []
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    if request.args:
        request_param = dict(request.args)
        for k, v in request_param.items():
            column, colval = k, v
        cur.execute("SELECT * FROM books where " + str(column) + "=""'"+str(colval[0])+"'")
    else:
        cur.execute("SELECT * FROM books")
    rows = cur.fetchall()
    for row in rows:
        data.append(dict(row))
    resp_data = {
        "status_code": 200,
        "status": "success",
        "data": data[0]
    }
    return jsonify(resp_data), 200


@app.route('/api/v1/books/<int:id>/update', methods=['PATCH'])
def update_database_books(id):
    request_param = dict(request.args)
    for k, v in request_param.items():
        column, colval = k, v
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    query = "UPDATE books SET "+ str(column) + " = " + "'"+str(colval[0])+\
            "'" + " WHERE id = " + "'"+str(id)+"'"+";"
    cur.execute(query)
    conn.commit()
    cur.execute("SELECT * FROM books where " + str(column) + " = ""'"+str(colval[0])+"'")
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(dict(row))
    data[0].pop('id')
    resp_data = {
        "status_code": 201,
        "status": "success",
        "data": data[0]
    }
    return jsonify(resp_data), 201


@app.route('/api/v1/books/<int:id>/delete', methods=['DELETE'])
def delete_books_database(id):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    select_book = "SELECT name from books where id = "+"'" + str(id) + "'" + ";"
    cur.execute(select_book)
    result = cur.fetchall()
    query = "DELETE FROM books WHERE id = " + "'" + str(id) + "'" + ";"
    cur.execute(query)
    conn.commit()
    resp_data = {
        "status_code": 201,
        "status": "success",
        "message": "The book {bookname} was deleted successfully".format(bookname=result[0][0]),
        "data": []
    }
    return jsonify(resp_data), 201


@app.route('/api/v1/books/<int:id>', methods=['GET'])
def show_database_books(id):
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * from books where id = " + "'" + str(id) + "'" + ";")
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(dict(row))
    data[0].pop('id')
    resp_data = {
        "status_code": 201,
        "status": "success",
        "data": data[0]
    }
    return jsonify(resp_data), 201


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)

import my_api
from my_api import app

def test_get_book():
        with app.app_context():
                response = my_api.get_book(book_name='A Game of Thrones')
                assert response[1] == 200

def test_post_database_book():
        with app.test_request_context():
                response = my_api.post_database_book()
                assert response[1] == 201

def test_get_database_books():
        with app.test_request_context():
                response = my_api.get_database_books()
                assert response[1] == 200

def test_update_database_books():
        with app.test_request_context():
                response = my_api.update_database_books(1)
                assert response[1] == 201

def test_delete_books_database():
        with app.test_request_context():
                response = my_api.delete_books_database(1)
                assert response[1] == 201

def test_show_database_books():
        with app.test_request_context():
                response = my_api.show_database_books(1)
                assert response[1] == 201
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
import sqlite3
import db

class TestDB(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['DATABASE'] = ':memory:'
        self.app.app_context().push()

    @patch('db.g')
    @patch('db.current_app')
    @patch('sqlite3.connect')
    def test_get_db(self, mock_connect, mock_current_app, mock_g):
        mock_current_app.config = {'DATABASE': ':memory:'}
        mock_g._database = None
        mock_db = MagicMock()
        mock_connect.return_value = mock_db

        result = db.get_db()

        mock_connect.assert_called_once_with(':memory:')
        self.assertEqual(result, mock_db)
        self.assertEqual(mock_g._database, mock_db)
        self.assertEqual(mock_db.row_factory, sqlite3.Row)

    @patch('db.g')
    def test_get_db_existing_connection(self, mock_g):
        mock_db = MagicMock()
        mock_g._database = mock_db

        result = db.get_db()

        self.assertEqual(result, mock_db)

        class TestDB(unittest.TestCase):

            def setUp(self):
                self.app = Flask(__name__)
                self.app.config['DATABASE'] = ':memory:'
                self.app.app_context().push()

            @patch('db.g')
            @patch('db.current_app')
            @patch('sqlite3.connect')
            def test_get_db(self, mock_connect, mock_current_app, mock_g):
                mock_current_app.config = {'DATABASE': ':memory:'}
                mock_g._database = None
                mock_db = MagicMock()
                mock_connect.return_value = mock_db

                result = db.get_db()

                mock_connect.assert_called_once_with(':memory:')
                self.assertEqual(result, mock_db)
                self.assertEqual(mock_g._database, mock_db)
                self.assertEqual(mock_db.row_factory, sqlite3.Row)

            @patch('db.g')
            def test_get_db_existing_connection(self, mock_g):
                mock_db = MagicMock()
                mock_g._database = mock_db

                result = db.get_db()

                self.assertEqual(result, mock_db)

            @patch('db.g')
            def test_close_connection(self, mock_g):
                mock_db = MagicMock()
                mock_g._database = mock_db

                db.close_connection(None)

                mock_db.close.assert_called_once()

            @patch('db.g')
            def test_close_connection_no_db(self, mock_g):
                mock_g._database = None

                db.close_connection(None)

                mock_g._database = None

            @patch('db.get_db')
            def test_query_db_select(self, mock_get_db):
                mock_db = MagicMock()
                mock_cursor = MagicMock()
                mock_cursor.fetchall.return_value = [{'id': 1}]
                mock_db.execute.return_value = mock_cursor
                mock_get_db.return_value = mock_db

                result = db.query_db('SELECT * FROM test')

                mock_db.execute.assert_called_once_with('SELECT * FROM test', ())
                mock_cursor.fetchall.assert_called_once()
                mock_cursor.close.assert_called_once()
                self.assertEqual(result, [{'id': 1}])

            @patch('db.get_db')
            def test_query_db_insert(self, mock_get_db):
                mock_db = MagicMock()
                mock_cursor = MagicMock()
                mock_cursor.lastrowid = 1
                mock_db.execute.return_value = mock_cursor
                mock_get_db.return_value = mock_db

                result = db.query_db('INSERT INTO test (name) VALUES (?)', ('test',))

                mock_db.execute.assert_called_once_with('INSERT INTO test (name) VALUES (?)', ('test',))
                mock_cursor.close.assert_called_once()
                self.assertEqual(result, 1)

            @patch('db.get_db')
            def test_query_db_update(self, mock_get_db):
                mock_db = MagicMock()
                mock_cursor = MagicMock()
                mock_cursor.rowcount = 1
                mock_db.execute.return_value = mock_cursor
                mock_get_db.return_value = mock_db

                result = db.query_db('UPDATE test SET name = ? WHERE id = ?', ('test', 1))

                mock_db.execute.assert_called_once_with('UPDATE test SET name = ? WHERE id = ?', ('test', 1))
                mock_cursor.close.assert_called_once()
                self.assertEqual(result, 1)

            @patch('db.get_db')
            def test_query_db_delete(self, mock_get_db):
                mock_db = MagicMock()
                mock_cursor = MagicMock()
                mock_cursor.rowcount = 1
                mock_db.execute.return_value = mock_cursor
                mock_get_db.return_value = mock_db

                result = db.query_db('DELETE FROM test WHERE id = ?', (1,))

                mock_db.execute.assert_called_once_with('DELETE FROM test WHERE id = ?', (1,))
                mock_cursor.close.assert_called_once()
                self.assertEqual(result, 1)

            @patch('db.get_db')
            @patch('db.current_app')
            def test_init_db(self, mock_current_app, mock_get_db):
                mock_db = MagicMock()
                mock_get_db.return_value = mock_db
                mock_open_resource = MagicMock()
                mock_open_resource.return_value.__enter__.return_value.read.return_value = 'CREATE TABLE test (id INTEGER);'
                mock_current_app.open_resource = mock_open_resource

                db.init_db()

                mock_get_db.assert_called_once()
                mock_open_resource.assert_called_once_with('schema.sql', mode='r')
                mock_db.cursor().executescript.assert_called_once_with('CREATE TABLE test (id INTEGER);')
                mock_db.commit.assert_called_once()

        if __name__ == '__main__':
            unittest.main()

if __name__ == '__main__':
    unittest.main()
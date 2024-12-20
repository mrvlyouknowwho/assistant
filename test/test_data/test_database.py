import unittest
import os
import json
from ..data.database import Database, DatabaseLoadError, DatabaseSaveError
from ..config import DATABASE_PATH


class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file for testing
        self.test_db_path = "test_database.json"
        self.db = Database(self.test_db_path)

    def tearDown(self):
       if os.path.exists(self.test_db_path):
         os.remove(self.test_db_path)



    def test_load_database_not_exists(self):
        # Test that a new database is created if it doesn't exist
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        db = Database(self.test_db_path)
        self.assertEqual(db.data, {"history": [], "context": {}, "user_info": {}, "search_cache":{}})

    def test_load_database_exists(self):
        # Test that database loads correctly if file exists
         test_data = {"history": ["test_query"], "context": {"last_query": "test"}, "user_info":{"name":"test"}, "search_cache":{"test_query": ["link1", "link2"]}}
         with open (self.test_db_path, "w") as f:
           json.dump(test_data, f)
         db = Database(self.test_db_path)
         self.assertEqual(db.data, test_data)

    def test_load_database_bad_json(self):
        # Test loading with bad JSON data
        with open(self.test_db_path, "w") as f:
            f.write("{bad json}")
        with self.assertRaises(DatabaseLoadError):
            Database(self.test_db_path)

    def test_save_database(self):
          test_data = {"history": ["test_query"], "context": {"last_query": "test"}, "user_info":{"name":"test"}, "search_cache":{"test_query": ["link1", "link2"]}}
          self.db.data = test_data
          self.db.save()
          with open (self.test_db_path, "r") as f:
              data = json.load(f)
          self.assertEqual(data,test_data)

    def test_clear_database(self):
        # Test that the database can be cleared
        test_data = {"history": ["test_query"], "context": {"last_query": "test"}, "user_info":{"name":"test"}, "search_cache":{"test_query": ["link1", "link2"]}}
        self.db.data = test_data
        self.db.clear()
        self.assertEqual(self.db.data, {"history": [], "context": {}, "user_info": {}, "search_cache":{}})


if __name__ == '__main__':
    unittest.main()
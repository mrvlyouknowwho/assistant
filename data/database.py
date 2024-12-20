""" Загрузка, сохранение, очистка данных """
import json
import os

class DatabaseError(Exception):
  """Base class for database errors."""
  pass


class DatabaseLoadError(DatabaseError):
   """Error loading database."""
   pass


class DatabaseSaveError(DatabaseError):
   """Error saving database."""
   pass

class Database:
   def __init__(self, db_path):
        self.db_path = db_path
        self.data = self._load()


   def _load(self):
        """Loads the database from file."""
        if not os.path.exists(self.db_path):
           return {"history": [], "context": {}, "user_info": {}, "search_cache":{}}
        try:
            with open(self.db_path, "r") as f:
                data = json.load(f)
                print(f"Дебаг: База данных загружена: {data}")
                if "user_info" not in data:
                    data["user_info"] = {}
                if "search_cache" not in data:
                     data["search_cache"] = {}
                return data
        except FileNotFoundError:
             raise DatabaseLoadError("Database file not found")
        except json.JSONDecodeError as e:
             raise DatabaseLoadError(f"Error parsing JSON: {e}")
        except Exception as e:
             raise DatabaseLoadError(f"Unknown error when loading the database: {e}")

   def save(self):
         """Saves the database to file."""
         try:
              with open(self.db_path, "w") as f:
                json.dump(self.data, f, indent=4)
              print("Дебаг: База данных сохранена.")
         except Exception as e:
               raise DatabaseSaveError(f"Error saving database: {e}")

   def clear(self):
         """Clears the database."""
         self.data = {"history": [], "context": {}, "user_info": {}, "search_cache":{}}
         self.save()
         print("Дебаг: База данных очищена.")
""" Отвечает за управление потоком действий ассистента """
import time
import random
from .exceptions import DispatcherError 
from processing.nlp.analyzer import analyze_query
from processing.search import search_google, filter_links
from .utils import fix_errors, add_function
from skills.basic import BasicSkills
from skills.search import SearchSkills

class Dispatcher:
  def __init__(self, db):
    self.db = db
    self.basic_skills = BasicSkills(db)
    self.search_skills = SearchSkills(db)

  def process_query(self):
        if self.db.data["user_info"].get("как_меня_называть"):
            name = random.choice(self.db.data["user_info"]["как_меня_называть"])
        else:
           name = "друг"
        query = input(f"Ассистент: {name}, введи запрос: ")
        print(f"Дебаг: Получен запрос от пользователя: {query}")

        action = analyze_query(query, self.db.data)

        if action == "exit":
            print("Ассистент: Завершение работы")
            raise DispatcherError("Завершение работы")
        if action == "name_changed":
            print("Ассистент: Отлично, буду знать как тебя называть!")
            return
        if action =="bad_name":
            print("Ассистент: Не понял какое имя запомнить.")
            return
        if action == "format_changed":
            print("Ассистент: Отлично, запомнил твой предпочтительный формат!")
            return
        if action == "bad_format":
            print("Ассистент: Не понял какой формат запомнить.")
            return
        if action == "themes_changed":
             print ("Ассистент: Отлично, запомнил твои любимые темы!")
             return
        if action == "bad_themes":
            print("Ассистент: Не понял какие темы запомнить.")
            return
        if action == "clear_database":
            self.db.clear()
            print("Ассистент: База данных очищена!")
            return
        if action == "fix":
             fix_errors()
             return
        elif action == "add_function":
             add_function()
             return
        elif action == "related":
             print("Ассистент: Я помню твой прошлый запрос.")
             self.search_skills.search_and_display(query)
        else:
             self.search_skills.search_and_display(query)


        self.db.data["history"].append({"query": query})
        self.db.data["context"] = {"last_query": query}
        self.db.save()
        time.sleep(random.randint(2,5)) # рандомная задержка
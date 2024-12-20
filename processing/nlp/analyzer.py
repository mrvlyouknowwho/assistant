""" Анализ запроса """
import re

def analyze_query(query, data):
    print(f"Дебаг: Анализ запроса: {query}. Контекст: {data.get('context')}")

    if not query:
        return None

    if query.lower() in ["exit", "выход", "q", "quit"]:
        return "exit"

    if "как меня называть" in query.lower():
        name = re.search(r'как меня называть (.+)', query.lower())
        if name:
          data["user_info"]["как_меня_называть"] = name.group(1).split()
          print (f"Дебаг: Запомнил как тебя называть - {name.group(1)}")
          return "name_changed"
        else:
          print ("Дебаг: Не понял какое имя запомнить")
          return "bad_name"

    if "формат" in query.lower():
        format_ = re.search(r'формат (.+)', query.lower())
        if format_:
          data["user_info"]["предпочтения_формат"] = format_.group(1).split()
          print(f"Дебаг: Запомнил формат - {format_.group(1)}")
          return "format_changed"
        else:
          print ("Дебаг: Не понял какой формат запомнить")
          return "bad_format"

    if "темы" in query.lower():
        themes = re.search(r'темы (.+)', query.lower())
        if themes:
            data["user_info"]["предпочтения_темы"] = themes.group(1).split()
            print(f"Дебаг: Запомнил темы - {themes.group(1)}")
            return "themes_changed"
        else:
          print ("Дебаг: Не понял какие темы запомнить")
          return "bad_themes"

    if query.lower() == "ошибка":
        print("Дебаг: Запрос классифицирован как 'ошибка'")
        return "fix"
    if query.lower() == "новая функция":
        print("Дебаг: Запрос классифицирован как 'новая функция'")
        return "add_function"
    if query.lower() == "очистить базу":
        print("Дебаг: Запрос классифицирован как 'очистить базу'")
        return "clear_database"
    if data.get("context") and "last_query" in data["context"]:
      last_query = data["context"]["last_query"]
      if any(word in query.lower() for word in last_query.lower().split()):
          print("Дебаг: Запрос связан с предыдущим запросом.")
          return "related"

    print("Дебаг: Запрос не классифицирован")
    return None
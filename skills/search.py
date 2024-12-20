""" Навыки для работы с поиском """
import random

from processing.search import search_google, filter_links


class SearchSkills:
  def __init__(self, db):
    self.db = db

  def search_and_display(self, query):
    links = search_google(query, self.db.data)
    if links:
        print("Ассистент: Вот что я нашел:")
        filtered_links = filter_links(links, query)
        for index, link in enumerate(filtered_links):
            print(f"{index + 1}. {link}")
    else:
         print("Ассистент: Ничего не нашел")
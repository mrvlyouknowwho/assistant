""" Поиск в Google, фильтрация """
import requests
from bs4 import BeautifulSoup
import re
import random

def search_google(query, data):
    print(f"Дебаг: Запрос: {query}")
    if query in data.get("search_cache", {}):
        print("Дебаг: Результаты найдены в кеше.")
        return data["search_cache"][query]

    url = f"https://www.google.com/search?q={query}"
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ]
    headers = {
        "User-Agent": random.choice(user_agents)
    }
    print(f"Дебаг: URL: {url}")
    print(f"Дебаг: Headers: {headers}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        print(f"Дебаг: Статус ответа: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Дебаг: Ошибка запроса: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    print(f"Дебаг: Получен HTML")
    links = []
    for div in soup.find_all('div', class_='yuRUbf'):
        a_tag = div.find('a', href=True)
        if a_tag:
           try:
               href = a_tag['href']
               match = re.search(r'/url\?q=(.+?)&', href)
               if match:
                   href = match.group(1)
                   if href.startswith("http"):
                       links.append(href)
           except Exception as e:
              print(f"Дебаг: Ошибка при парсинге ссылки: {href}. Ошибка: {e}")
              continue
    if not links:
      for a_tag in soup.find_all('a', href=True):
        try:
             href = a_tag['href']
             if href.startswith("http"):
                 links.append(href)
        except Exception as e:
             print(f"Дебаг: Ошибка при парсинге ссылки: {href}. Ошибка: {e}")
             continue
    print(f"Дебаг: Найденные ссылки: {links}")

    data["search_cache"][query] = links  # Сохраняем в кеш
    return links

def filter_links(links, query):
    print(f"Дебаг: Фильтрация ссылок: {links} по запросу: {query}")
    filtered_links = []
    query_words = query.lower().split()
    for link in links:
        try:
            score = 0
            if "youtube.com" in link:
                score -= 10  # понижаем рейтинг youtube
            if any(keyword in link.lower() for keyword in ["разработка", "обучение", "машинное обучение", "алгоритмы", "память", "ии"]):  # повышаем рейтинг если есть ключевые слова
                score += 5
            if any(keyword in link.lower() for keyword in query_words):  # повышаем рейтинг если есть слова из запроса
                score += 10
            if any(keyword in link.lower() for keyword in ["pdf", "doc"]):  # понижаем рейтинг pdf и doc
                score -= 5

            if score > 0:
                filtered_links.append((link, score))
            else:
                if random.random() > 0.7:
                    filtered_links.append((link, score))

        except Exception as e:
            print(f"Дебаг: Ошибка при фильтрации ссылки: {link}. Ошибка: {e}")
            continue
    filtered_links.sort(key=lambda item: item[1], reverse=True)
    print(f"Дебаг: Отфильтрованные ссылки: {[link for link, score in filtered_links]}")
    return [link for link, score in filtered_links]
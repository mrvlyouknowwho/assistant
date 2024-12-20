import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

knowledge_base = {
    "нейронные сети": "Нейронные сети — это вычислительные системы, вдохновленные строением и функционированием биологических нейронных сетей. Они используются для решения задач классификации, регрессии и др.",
    "машинное обучение": "Машинное обучение — это раздел искусственного интеллекта, изучающий методы построения алгоритмов, способных обучаться на данных без явного программирования.",
    "алгоритмы": "Алгоритм — это набор инструкций, описывающих порядок действий для достижения некоторой цели. Алгоритмы являются основой программирования.",
    "глубокое обучение": "Глубокое обучение (Deep Learning) — это подраздел машинного обучения, основанный на использовании нейронных сетей с большим количеством слоев (глубоких).",
    "что такое ии": "Искусственный интеллект (ИИ) — это область компьютерных наук, занимающаяся разработкой интеллектуальных систем, способных выполнять задачи, которые обычно требуют человеческого интеллекта."
}


def get_answer_from_knowledge_base(user_input):
    """Анализирует ввод пользователя и возвращает ответ из базы знаний."""
    user_input = user_input.lower()
    logging.info(f"Пользователь: {user_input}")

    for keyword, answer in knowledge_base.items():
        if keyword in user_input:
            logging.info(f"Ассистент нашел ответ: {answer}")
            return answer
    
    # Если нет совпадений, даем общий ответ
    default_answer = "Извини, я пока не знаю ответа на этот вопрос. Я еще учусь. Можешь попробовать перефразировать или задать другой вопрос."
    logging.info(f"Ассистент: {default_answer}")
    return default_answer


def add_to_knowledge_base(new_knowledge):
    try:
        data = json.loads(new_knowledge)
        for key, value in data.items():
            knowledge_base[key] = value
            logging.info(f"Добавлено в базу знаний: {key}: {value}")
        return "Новые знания успешно добавлены в базу."
    except json.JSONDecodeError:
        logging.warning(f"Неверный формат JSON. Не удалось добавить новые знания: {new_knowledge}")
        return "Не удалось добавить новые знания. Пожалуйста, предоставьте данные в формате JSON."
    except Exception as e:
        logging.error(f"Ошибка при добавлении в базу знаний: {e}")
        return "Произошла ошибка при добавлении знаний."


def update_knowledge_base(user_input, answer):
    """Запрашивает у пользователя, хочет ли он обновить знания"""
    logging.info("Запрос на обновление базы знаний")
    
    if "добавь в знания" in user_input.lower() or "обнови знания" in user_input.lower() or "добавь новые знания" in user_input.lower():
        
        new_knowledge = input("Пожалуйста, предоставьте новые знания в формате JSON (например, {\"ключевое слово\": \"ответ\"}): ")
        result = add_to_knowledge_base(new_knowledge)
        return result

    if "запомни" in user_input.lower():
        new_knowledge = input("Введите ключевое слово для запоминания: ")
        knowledge_base[new_knowledge] = answer
        return f"Ключевое слово {new_knowledge} с ответом добавлено в базу знаний"
    
    return None
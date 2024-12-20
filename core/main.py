import logging

from utils import get_answer_from_knowledge_base, update_knowledge_base
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

messages = []

def main():
    while True:
        try:
            user_input = input("Вы: ")
            if user_input.lower() == 'выход':
                break
            
            messages.append({"role": "user", "content": user_input})

            # Сначала проверяем базу знаний
            answer = get_answer_from_knowledge_base(user_input)
            
            # Запрашиваем у пользователя обновление базы знаний
            update_result = update_knowledge_base(user_input, answer)

            if update_result:
                print("Ассистент:", update_result)
            else:
                print("Ассистент:", answer)

            messages.append({"role": "assistant", "content": answer})


        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
import os
import telegram
from dotenv import load_dotenv
import asyncio

load_dotenv()
bot_token = os.getenv('TOKEN')
group_id = int(os.getenv('GROUP_ID'))
usernames = [username.replace('"', '').replace("'", '').replace('[', '').replace(']', '').replace(',', '').strip() for
             username in os.getenv('USERS').split(',')]
starting_user_index = 0

bot = telegram.Bot(token=bot_token)


def save_indexes(start_index):  # Сохраняем индексы
    with open('indexes.txt', 'w') as f:
        f.write(f"START_INDEX={start_index}")


def load_indexes():  # Загружаем индексы
    with open('indexes.txt', 'r') as f:
        lines = f.readlines()

    for line in lines:
        key, value = line.strip().split('=')
        if key == 'START_INDEX':
            return int(value)


async def main():  # Используем асинхронность в функции main()
    global starting_user_index

    starting_user_index = load_indexes()

    next_duty_index = (starting_user_index + 1) % len(usernames)
    next_duty = usernames[next_duty_index]

    message_text = f'Всем доброго времени суток!\nСегодня дежурный: {next_duty}'
    await bot.send_message(chat_id=group_id, text=message_text)  # Добавляем await

    starting_user_index = next_duty_index
    save_indexes(starting_user_index)


if __name__ == '__main__':

    asyncio.run(main())  # Запускаем асинхронную функцию с помощью asyncio.run()

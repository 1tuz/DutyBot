import os
from dotenv import load_dotenv
import telegram
import asyncio

# загружаем переменные из файла .env
load_dotenv()
bot_token = os.getenv('TOKEN')
group_chat_id = os.getenv('GROUP_ID')
usernames = os.getenv('USERS').split()

# создаем объект бота
bot = telegram.Bot(token=bot_token)
duty_file_path = 'duty.txt'

usernames = [username.replace('"', '').replace("'", '').replace('[', '').replace(']', '').replace(',', '') for username in usernames]

async def main():
    with open(duty_file_path, 'r') as duty_file:
        current_duty_index = int(duty_file.read().strip()) if os.path.exists(duty_file_path) else -1

    next_duty_index = (current_duty_index + 1) % len(usernames)
    next_duty = usernames[next_duty_index]

    message_text = f'Сегодня дежурный: {next_duty}'
    await bot.send_message(chat_id=group_chat_id, text=message_text)

    with open(duty_file_path, 'w') as duty_file:
        duty_file.write(str(next_duty_index))


if __name__ == '__main__':
    asyncio.run(main())

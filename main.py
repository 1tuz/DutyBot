import os
from dotenv import load_dotenv
import telegram
import asyncio

load_dotenv()

bot_token = os.getenv('TOKEN')
group_id = int(os.getenv('GROUP_ID'))
usernames = [username.replace('"', '').replace("'", '').replace('[', '').replace(']', '').replace(',', '').strip() for username in os.getenv('USERS').split(',')]
starting_user_index = int(os.getenv('START_INDEX'))

bot = telegram.Bot(token=bot_token)

async def main():
    global starting_user_index

    next_duty_index = (starting_user_index + 1) % len(usernames)
    next_duty = usernames[next_duty_index]

    message_text = f'Сегодня дежурный: {next_duty}'
    await bot.send_message(chat_id=group_id, text=message_text)

    starting_user_index = next_duty_index
    os.environ['START_INDEX'] = str(starting_user_index)
    with open('.env', 'w') as f:
        f.write(f"TOKEN={bot_token}\n")
        f.write(f"USERS={','.join(usernames)}\n")
        f.write(f"GROUP_ID={group_id}\n")
        f.write(f"START_INDEX={starting_user_index}\n")

if __name__ == '__main__':
    asyncio.run(main())

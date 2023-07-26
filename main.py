import os
import requests
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta
import time
import datetime

load_dotenv()
bot_token = os.getenv('TOKEN')  
group_id = int(os.getenv('GROUP_ID'))
usernames = [username.replace('"', '').replace("'", '').replace('[', '').replace(']', '').replace(',', '').strip() for
             username in os.getenv('USERS').split(',')]
starting_user_index = 0

# Set up logging
logging.basicConfig(filename='duty_bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Log start time
start_time = datetime.datetime.now()
print(f"Bot started at {start_time}")
logging.info(f"Bot started at {start_time}")

def save_indexes(start_index, counter):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'indexes.txt')
    with open(file_path, 'w') as f:
        f.write(f"START_INDEX={start_index}\n")
        f.write(f"COUNTER={counter}")
        
def load_indexes():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'indexes.txt')

    if not os.path.isfile(file_path):
        return None, None

    with open(file_path, 'r') as f:
        lines = f.readlines()

    start_index = None
    counter = None
    for line in lines:
        key, value = line.strip().split('=')
        if key == 'START_INDEX':
            start_index = int(value)
        elif key == 'COUNTER':
            counter = int(value)

    return start_index, counter

def send_duty_message():
    starting_user_index, counter = load_indexes()

    if starting_user_index is None or counter is None:
        starting_user_index = 0
        counter = 0

    next_duty_index = (starting_user_index + counter) % len(usernames)
    next_duty = usernames[next_duty_index]

    message_text = f'Всем доброго времени суток!\nНапоминаю, что сегодня дежурный {next_duty}'

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {
        'chat_id': group_id,
        'text': message_text
    }

    response = requests.post(url, data=data)
    if response.ok:
        logging.info('Duty message sent.')
    else:
        logging.error('Failed to send duty message.')

    counter += 1
    if counter == 2:
        counter = 0
        starting_user_index = (starting_user_index + 1) % len(usernames)

    save_indexes(starting_user_index, counter)


def run_duty_bot():
    while True:
        # Current time
        now = datetime.now()

        # Test timeouts
        if now.hour in [7, 8, 9, 10, 16, 22, 23]:
            send_duty_message()

        # Sleep for 1 hour before checking again
        time.sleep(3600)

if __name__ == '__main__':

    try:
        run_duty_bot()
    except KeyboardInterrupt:
        pass
        
# Log end time
end_time = datetime.datetime.now()
print(f"Bot finished at {end_time}")
logging.info(f"Bot finished at {end_time}")

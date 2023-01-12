import os
import telegram
import json
from dotenv import load_dotenv 
from loguru import logger
from datetime import datetime, timedelta
from pathlib import Path

path_to_project = Path(__file__)  # Get present working directory
log_file = Path(__file__).parent / 'log.log'  # Put log.log in code directory

logger.remove()  # Remove default sysout log
logger.add(log_file, retention="1 month", level='DEBUG')  # Create physical log file

# Load environment variables
assert load_dotenv()  # If the .env file is missing, this will raise an error
TELEGRAM_TOKEN=os.environ.get('TELEGRAM_TOKEN')  # Token for the telegram bot
USER_ID=os.environ.get('USER_ID')  # ID of the user

# Load JSON file with notification dates
with open(path_to_project.parent / 'dates.json') as f:
    DATES=json.load(f)

# birthdays = DATES['birthday']
# anniversaries = DATES['anniversary']
# holidays=DATES['holiday']
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Get the current day
TODAY = datetime.now()

# Check intervals
check_intervals = [14, 7, 1, 0]  # The days to be notified from.  The date itself is 0, day before is 1, etc.

@logger.catch
def send_telegram_message(message):
    """Sends the message to the Telegram API

    Args:
        message (str): The message that will be displayed by the Telegram Bot
    """    
    bot.send_message(text=message, chat_id=USER_ID)  # Pulled from .env file

def convert_to_datetime(stringdate):
    """Take in a string and convert it to a datetime object

    Args:
        stringdate (str): String from dates.json of the form 'yyyy-mm-dd' or 'mm-dd'

    Returns:
        date_obj (datetime-obj): A datetime object

    """    
    logger.debug(f"Sringdate: {stringdate}")
    date_list = [int(i) for i in stringdate.split('-')]  # Convert values to integer
    day = date_list[-1]  # Date is always last
    month= date_list[-2]  # Month always second to last
    if len(date_list) == 3:  # year, month, and day
        year = date_list[0]  # If year is present, it's the first value
    else:
        year = datetime.now().year 
    date_obj = datetime(year, month, day)  # Create a datetime object

    return(date_obj)


def check_today(the_occasion, person, target_date_string, time_until):
    """Checks if a given event is available to be notified on

    Args:
        the_occation (str): Event type, like Birthday, Holiday
        person (str):  Person or subject, like Bill, or Christmas
        target_date_string (str):  String representation of the date yyyy-mm-dd or mm-dd
        time_until (int):  X Days until event

    Returns:
        None 

    """        
    logger.debug(f"Occasion: {the_occasion}\nThe Subject: {person}\nTime Until: {time_until}")
    target_date = convert_to_datetime(target_date_string)
    delta = timedelta(time_until)
    check_date = target_date-delta
    if check_date.month == TODAY.month and check_date.day == TODAY.day:
        message = f"It's {person}'s {the_occasion} "
        if delta.days == 0:
            message_suffix = 'TODAY!'
        else:
            message_suffix = f'in {time_until} days'
        message+=message_suffix
        logger.info(f"{message}")
        send_telegram_message(message)


def check_all():
    """ Function which iterates through all items in dates.json

    Args:
        None

    Returns:
        None

    """    
    occasions = list(DATES.keys())
    for occasion in occasions:  # Iterate through all occasions, like birthdays, events, etc
        subjects = list(DATES[occasion].keys())  # The objects of the occasions
        for subject in subjects:  # Iterate through dates
            the_date = DATES[occasion][subject]
            for interval in check_intervals:
                check_today(occasion, subject, the_date, interval)


if __name__ == '__main__':
    logger.info(f"Checking on {datetime.now().isoformat()}")
    check_all()

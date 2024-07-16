import os
from dotenv import load_dotenv, find_dotenv


success = load_dotenv(find_dotenv('.env'))

PARSING_PATH = os.getenv('PARSING_PATH', "hh.ru")
CHROME_PATH = os.getenv('CHROME_PATH')
DRIVER_PATH = os.getenv('DRIVER_PATH')
USER_DATA_DIR = os.getenv('USER_DATA_DIR')
PROFILE_DIR = os.getenv('PROFILE_DIR')
TXT_FILE = os.getenv("TXT_FILE")
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH'),
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
FILE_PATH='~/Documents/BaburinCV_Backend.pdf'
KEYWORD = 'Python Backend'
message_text = """Добрый день!\n\nПрочитал описание Вашей вакансии, отдельное спасибо составлителю за чёткое и понятное изложение.\n
Понравились Ваши цели и достижения, мне было бы интересно у Вас работать. Обладаю 2х летним опытом в Питоне и окружении вокруг него(Django, FastAPI, ORMs, SQL/NoSQL, Docker, Celery и тд, так что уверен, что и с Вами найдем общий язык)\n\nБуду рад продолжить общение,\nСпасибо)"""



print(success)

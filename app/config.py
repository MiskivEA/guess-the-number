from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
ADMINISTRATORS = [ADMIN_ID]

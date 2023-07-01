import motor.motor_asyncio
from src.settings import DATABASE_URL, DATABASE_NAME


client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL, uuidRepresentation="standard")
db = client[DATABASE_NAME]

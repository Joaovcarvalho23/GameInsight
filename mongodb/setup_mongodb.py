from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv("MONGO_URI")

client = MongoClient(connection_string)

db = client["gameinsight"]
collection = db["games"]

file_path = os.path.join("data", "vgsales.csv")

data = pd.read_csv(file_path)
data_dict = data.to_dict("records")

collection.insert_many(data_dict)

print("Dados importados com sucesso!")
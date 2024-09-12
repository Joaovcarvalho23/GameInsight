from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASSWORD")

connection_string = f"mongodb+srv://{username}:{password}@cluster-gameinsight.suh1e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-GameInsight"


client = MongoClient(connection_string)

db = client["gameinsight"]
collection = db["games"]

file_path = os.path.join("data", "vgsales.csv")

data = pd.read_csv(file_path)

data_dict = data.to_dict("records")

collection.insert_many(data_dict)

print("Dados importados com sucesso!")

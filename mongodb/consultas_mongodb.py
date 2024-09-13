from pymongo import MongoClient
from pprint import pprint
import os
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv("MONGO_URI")
client = MongoClient(connection_string)

db = client["gameinsight"]
collection = db["games"]

# Definicao dos metodos de busca
def buscar_jogos_por_ano(year):
    consulta = {"Year": year}
    resultadoBusca = collection.find(consulta).limit(3)
    for jogo in resultadoBusca:
        pprint(jogo)
        print("\n")  


def buscar_jogos_por_plataforma(platform):
    consulta = {"Platform": platform}
    resultadoBusca = collection.find(consulta).limit(3)
    for jogo in resultadoBusca:
        pprint(jogo)
        print("\n")  


def buscar_jogos_mais_vendidos(limit=10):
    resultadoBusca = collection.find().sort("Global_Sales", -1).limit(limit)
    for jogo in resultadoBusca:
        pprint(jogo)
        print("\n")  
        
        
def buscar_publisher_com_mais_jogos_ano(year):
    pipeline = [
        {"$match": {"Year": year}},
        {"$group": {"_id": "$Publisher", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ]
    resultadoBusca = list(collection.aggregate(pipeline))
    if resultadoBusca:
        publisher = resultadoBusca[0]["_id"]
        total_jogos = resultadoBusca[0]["count"]
        print(f"O publisher com mais lançamentos em {year} foi {publisher} com {total_jogos} jogos.")
    else:
        print(f"Nenhum publisher encontrado para o ano {year}.")
        

def buscar_jogos_mais_vendidos_continente(continente, limit=3):
    if continente not in ["EU_Sales", "JP_Sales", "NA_Sales"]:
        print(f"Continente inválido: {continente}. Use 'EU_Sales', 'JP_Sales', ou 'NA_Sales'.")
        return

    resultadoBusca = collection.find().sort(continente, -1).limit(limit)
    
    for jogo in resultadoBusca:
        pprint(jogo)
        print("\n")
        
         
         
def buscar_jogos_action_publisher(publisher, limit=5):
    consulta = {"Publisher": publisher, "Genre": "Action"}
    resultadoBusca = collection.find(consulta).sort("Global_Sales", -1).limit(limit)
    
    for jogo in resultadoBusca:
        pprint(jogo)
        print("\n")
        
        
# Main
if __name__ == "__main__":
    print(" ------------ Jogos na plataforma NES ------------ ")
    buscar_jogos_por_plataforma("NES")
    
    print(" ------------ Jogos lançados em 2013 ------------ ")
    buscar_jogos_por_ano(2013)
    
    print("\n ------------ Top 10 jogos mais vendidos ------------ ")
    buscar_jogos_mais_vendidos()
    
    print("\n ------------ Publisher com mais lançamentos em 2016 ------------ ")
    buscar_publisher_com_mais_jogos_ano(2016)
    
    print("\n ------------ Top 3 jogos mais vendidos no Japão (JP_Sales) ------------ ")
    buscar_jogos_mais_vendidos_continente("JP_Sales")
    
    print("\n ------------ Jogos de Action mais vendidos da Activision ------------ ")
    buscar_jogos_action_publisher("Activision")
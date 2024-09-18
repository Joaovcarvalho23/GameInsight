from pymongo import MongoClient
from neo4j import GraphDatabase
from prettytable import PrettyTable
import os
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client["gameinsight"]
mongo_collection = mongo_db["games"]

neo4j_uri = os.getenv("NEO4J_URI")
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")
neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))

def print_table(title, headers, rows):
    table = PrettyTable()
    table.field_names = headers
    for row in rows:
        table.add_row(row)
    print(f"\n{title}")
    print(table)

def consultar_jogos_por_publisher_plataforma(publisher, platform):
    with neo4j_driver.session() as session:
        query = """
        MATCH (p:Publisher {name: $publisher})-[:PUBLISHED]->(g:Game)-[:AVAILABLE_ON]->(pl:Platform {name: $platform})
        RETURN g.title AS title
        """
        result = session.run(query, publisher=publisher, platform=platform)
        jogos = [record["title"] for record in result]

    detalhes_jogos = mongo_collection.find({"Name": {"$in": jogos}}, {"_id": 0, "Name": 1, "Year": 1, "Global_Sales": 1})
    
    rows = [(jogo['Name'], int(jogo['Year']), jogo['Global_Sales']) for jogo in detalhes_jogos]
    print_table(f"Jogos por Publisher ({publisher}) e Plataforma ({platform})", ["Nome", "Ano", "Vendas Globais"], rows)

def consultar_jogos_por_genero_ano(genre, year):
    with neo4j_driver.session() as session:
        query = """
        MATCH (g:Game)-[:CATEGORIZED_AS]->(:Genre {name: $genre}), (g)-[:RELEASED_IN]->(:Year {year: $year})
        RETURN g.title AS title
        """
        result = session.run(query, genre=genre, year=year)
        jogos = [record["title"] for record in result]

    detalhes_jogos = mongo_collection.find({"Name": {"$in": jogos}}, {"_id": 0, "Name": 1, "Platform": 1, "Publisher": 1})
    
    rows = [(jogo['Name'], jogo['Platform'], jogo['Publisher']) for jogo in detalhes_jogos]
    print_table(f"Jogos por Gênero ({genre}) e Ano ({year})", ["Nome", "Plataforma", "Publisher"], rows)

if __name__ == "__main__":
    consultar_jogos_por_publisher_plataforma("Nintendo", "Wii")
    
    consultar_jogos_por_genero_ano("Sports", 2013)

mongo_client.close()
neo4j_driver.close()
from pymongo import MongoClient
from neo4j import GraphDatabase
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
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))

def create_game_node(game):
    with driver.session() as session:
        query = """
        MERGE (g:Game {title: $title, platform: $platform, year: $year, genre: $genre, publisher: $publisher, global_sales: $global_sales})
        RETURN g
        """
        session.run(query, title=game['Name'], platform=game['Platform'], year=game['Year'], genre=game['Genre'],
                    publisher=game['Publisher'], global_sales=game['Global_Sales'])

def create_publisher_node(publisher):
    with driver.session() as session:
        query = """
        MERGE (p:Publisher {name: $name})
        RETURN p
        """
        session.run(query, name=publisher)

def create_relationship(game):
    with driver.session() as session:
        query = """
        MATCH (g:Game {title: $title}), (p:Publisher {name: $publisher})
        MERGE (p)-[:PUBLISHED]->(g)
        """
        session.run(query, title=game['Name'], publisher=game['Publisher'])

def import_games_to_neo4j():
    games = mongo_collection.find()
    
    for game in games:
        create_game_node(game)
        create_publisher_node(game['Publisher'])
        create_relationship(game)

if __name__ == "__main__":
    print("Iniciando importação de dados para o Neo4j...")
    import_games_to_neo4j()
    print("Importação concluída com sucesso!")
    driver.close()

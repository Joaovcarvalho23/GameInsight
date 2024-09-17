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
        MERGE (g:Game {title: $title, global_sales: $global_sales})
        RETURN g
        """
        session.run(query, title=game['Name'], global_sales=game['Global_Sales'])

def create_publisher_node(publisher):
    with driver.session() as session:
        query = """
        MERGE (p:Publisher {name: $name})
        RETURN p
        """
        session.run(query, name=publisher)

def create_platform_node(platform):
    with driver.session() as session:
        query = """
        MERGE (pl:Platform {name: $name})
        RETURN pl
        """
        session.run(query, name=platform)

def create_genre_node(genre):
    with driver.session() as session:
        query = """
        MERGE (g:Genre {name: $name})
        RETURN g
        """
        session.run(query, name=genre)

def create_year_node(year):
    with driver.session() as session:
        query = """
        MERGE (y:Year {year: $year})
        RETURN y
        """
        session.run(query, year=year)

def create_relationships(game):
    with driver.session() as session:
        query_publisher_game = """
        MATCH (g:Game {title: $title}), (p:Publisher {name: $publisher})
        MERGE (p)-[:PUBLISHED]->(g)
        """
        session.run(query_publisher_game, title=game['Name'], publisher=game['Publisher'])
        
        query_platform_game = """
        MATCH (g:Game {title: $title}), (pl:Platform {name: $platform})
        MERGE (g)-[:AVAILABLE_ON]->(pl)
        """
        session.run(query_platform_game, title=game['Name'], platform=game['Platform'])
        
        query_genre_game = """
        MATCH (g:Game {title: $title}), (gen:Genre {name: $genre})
        MERGE (g)-[:CATEGORIZED_AS]->(gen)
        """
        session.run(query_genre_game, title=game['Name'], genre=game['Genre'])
        
        query_year_game = """
        MATCH (g:Game {title: $title}), (y:Year {year: $year})
        MERGE (g)-[:RELEASED_IN]->(y)
        """
        session.run(query_year_game, title=game['Name'], year=game['Year'])

def import_games_to_neo4j(limit=1500):
    games = mongo_collection.find().limit(limit)
    
    for game in games:
        create_game_node(game)
        create_publisher_node(game['Publisher'])
        create_platform_node(game['Platform'])
        create_genre_node(game['Genre'])
        create_year_node(game['Year'])
        create_relationships(game)

if __name__ == "__main__":
    print("Iniciando importação de dados para o Neo4j com limite...")
    import_games_to_neo4j(limit=1500)
    print("Importação concluída com sucesso!")
    driver.close()
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

neo4j_uri = os.getenv("NEO4J_URI")
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))

def buscar_jogos_mais_vendidos(limit=10):
    with driver.session() as session:
        query = """
        MATCH (g:Game)
        RETURN g.title, g.global_sales
        ORDER BY g.global_sales DESC
        LIMIT $limit
        """
        result = session.run(query, limit=limit)
        for record in result:
            print(f"Jogo: {record['g.title']}, Vendas Globais: {record['g.global_sales']}")

def buscar_jogos_por_plataforma(platform):
    with driver.session() as session:
        query = """
        MATCH (g:Game {platform: $platform})
        RETURN g.title, g.global_sales, g.year
        ORDER BY g.global_sales DESC
        LIMIT 10
        """
        result = session.run(query, platform=platform)
        for record in result:
            print(f"Jogo: {record['g.title']}, Vendas: {record['g.global_sales']}, Ano: {record['g.year']}")


def buscar_publisher_com_mais_jogos_ano(year):
    with driver.session() as session:
        query = """
        MATCH (p:Publisher)-[:PUBLISHED]->(g:Game {year: $year})
        RETURN p.name, COUNT(g) AS num_jogos
        ORDER BY num_jogos DESC
        LIMIT 1
        """
        result = session.run(query, year=year)
        for record in result:
            print(f"Publisher: {record['p.name']}, Jogos: {record['num_jogos']}")

def buscar_jogos_por_genero_publisher(publisher, genre):
    with driver.session() as session:
        query = """
        MATCH (p:Publisher {name: $publisher})-[:PUBLISHED]->(g:Game {genre: $genre})
        RETURN g.title, g.global_sales
        ORDER BY g.global_sales DESC
        LIMIT 10
        """
        result = session.run(query, publisher=publisher, genre=genre)
        for record in result:
            print(f"Jogo: {record['g.title']}, Vendas: {record['g.global_sales']}")

def close_neo4j():
    driver.close()

if __name__ == "__main__":
    print("Consultando jogos mais vendidos no Neo4j:")
    buscar_jogos_mais_vendidos()

    print("\nConsultando jogos na plataforma NES:")
    buscar_jogos_por_plataforma("NES")

    print("\nPublisher com mais lançamentos em 2016:")
    buscar_publisher_com_mais_jogos_ano(2016)

    print("\nJogos de Action da Activision:")
    buscar_jogos_por_genero_publisher("Activision", "Action")

    close_neo4j()

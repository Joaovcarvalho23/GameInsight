from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

neo4j_uri = os.getenv("NEO4J_URI")
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))

def jogos_lancados_ano_plataforma(year, platform):
    with driver.session() as session:
        query = """
        MATCH (g:Game)-[:RELEASED_IN]->(y:Year {year: $year}), (g)-[:AVAILABLE_ON]->(p:Platform {name: $platform})
        RETURN g.title, g.global_sales
        ORDER BY g.global_sales DESC
        """
        result = session.run(query, year=year, platform=platform)
        for record in result:
            print(f"Jogo: {record['g.title']}, Vendas Globais: {record['g.global_sales']}")

def jogos_lancados_ano(year):
    with driver.session() as session:
        query = """
        MATCH (g:Game)-[:RELEASED_IN]->(y:Year {year: $year})
        RETURN g.title, g.global_sales
        ORDER BY g.global_sales DESC
        """
        result = session.run(query, year=year)
        for record in result:
            print(f"Jogo: {record['g.title']}, Vendas Globais: {record['g.global_sales']}")

def jogos_por_genero(genre):
    with driver.session() as session:
        query = """
        MATCH (g:Game)-[:CATEGORIZED_AS]->(gen:Genre {name: $genre})
        RETURN g.title, g.global_sales
        ORDER BY g.global_sales DESC
        """
        result = session.run(query, genre=genre)
        for record in result:
            print(f"Jogo: {record['g.title']}, Vendas Globais: {record['g.global_sales']}")

def jogos_publisher_genero(publisher, genre):
    with driver.session() as session:
        query = """
        MATCH (p:Publisher {name: $publisher})-[:PUBLISHED]->(g:Game)-[:CATEGORIZED_AS]->(gen:Genre {name: $genre})
        RETURN g.title, g.global_sales
        ORDER BY g.global_sales DESC
        """
        result = session.run(query, publisher=publisher, genre=genre)
        for record in result:
            print(f"Jogo: {record['g.title']}, Vendas Globais: {record['g.global_sales']}")

def jogos_plataforma(platform):
    with driver.session() as session:
        query = """
        MATCH (g:Game)-[:AVAILABLE_ON]->(p:Platform {name: $platform})
        RETURN g.title, g.global_sales
        ORDER BY g.global_sales DESC
        LIMIT 10
        """
        result = session.run(query, platform=platform)
        for record in result:
            print(f"Jogo: {record['g.title']}, Vendas Globais: {record['g.global_sales']}")

def top_10_jogos():
    with driver.session() as session:
        query = """
        MATCH (g:Game)
        RETURN g.title, g.global_sales
        ORDER BY g.global_sales DESC
        LIMIT 10
        """
        result = session.run(query)
        for record in result:
            print(f"Jogo: {record['g.title']}, Vendas Globais: {record['g.global_sales']}")

def jogos_por_publisher(publisher):
    with driver.session() as session:
        query = """
        MATCH (p:Publisher {name: $publisher})-[:PUBLISHED]->(g:Game)
        RETURN g.title, g.global_sales
        ORDER BY g.global_sales DESC
        """
        result = session.run(query, publisher=publisher)
        for record in result:
            print(f"Jogo: {record['g.title']}, Vendas Globais: {record['g.global_sales']}")

def contar_jogos_por_publisher():
    with driver.session() as session:
        query = """
        MATCH (p:Publisher)-[:PUBLISHED]->(g:Game)
        RETURN p.name, COUNT(g) AS num_jogos
        ORDER BY num_jogos DESC
        """
        result = session.run(query)
        for record in result:
            print(f"Publisher: {record['p.name']}, Número de Jogos: {record['num_jogos']}")

def plataformas_mais_jogos():
    with driver.session() as session:
        query = """
        MATCH (p:Platform)-[:AVAILABLE_ON]->(g:Game)
        RETURN p.name, COUNT(g) AS num_jogos
        ORDER BY num_jogos DESC
        """
        result = session.run(query)
        for record in result:
            print(f"Plataforma: {record['p.name']}, Número de Jogos: {record['num_jogos']}")

def close_neo4j():
    driver.close()

if __name__ == "__main__":
    print("\n------------------------- Jogos lançados em 2012 na plataforma X360 -------------------------")
    jogos_lancados_ano_plataforma(2012, "X360")

    print("\n------------------------- Jogos lançados em 2012 -------------------------")
    jogos_lancados_ano(2012)

    print("\n------------------------- Jogos de gênero 'Action' -------------------------")
    jogos_por_genero("Action")

    print("\n------------------------- Jogos de 'Electronic Arts' no gênero 'Sports' -------------------------")
    jogos_publisher_genero("Electronic Arts", "Sports")

    print("\n------------------------- Top 10 jogos mais vendidos na plataforma PS4 -------------------------")
    jogos_plataforma("PS4")

    print("\n------------------------- Top 10 jogos mais vendidos -------------------------")
    top_10_jogos()

    print("\n------------------------- Jogos publicados pela Activision -------------------------")
    jogos_por_publisher("Activision")

    print("\n------------------------- Número de jogos publicados por cada publisher -------------------------")
    contar_jogos_por_publisher()

    print("\n------------------------- Plataformas com mais jogos disponíveis -------------------------")
    plataformas_mais_jogos()
    close_neo4j()
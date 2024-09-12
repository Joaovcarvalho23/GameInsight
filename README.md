# GameInsight

**GameInsight** é uma plataforma de análise e recomendação de Video Games baseada em dados históricos de vendas. O projeto utiliza **MongoDB** para armazenar os dados de vendas e **Neo4j** para criar relações entre jogos, publicadoras, plataformas e jogadores.

**GameInsight** é uma plataforma de análise e recomendação de Video Games baseada em dados históricos de vendas, destinada a jogadores, desenvolvedores, publicadoras e pesquisadores do mercado de jogos, que serão as nossas entidades. O modelo de negócio se baseia em oferecer insights valiosos a partir dos dados de vendas de jogos em diferentes plataformas e continentes, utilizando análises avançadas e visualizações interativas.
Optamos por usar o **MongoDB** para armazenar os dados de vendas, e o **Neo4j** para criar relações entre jogos, publicadoras, plataformas e jogadores. O Mongo possui uma facilidade e flexibilidade na modelagem dos nossos dados. O Neo4j que, por ser um banco de dados baseado em grafos, os dados são armazenados como nós e relacionamentos. Isso nos permite criar uma representação mais eficiente dos diversos relacionamentos que a gente pode fazer com os nossos dados.

## Instalação

### MongoDB

1. Execute `setup_mongodb.py` para importar os dados para o MongoDB.
2. Use `queries_mongodb.py` para executar consultas.

### Neo4j

1. Execute `setup_neo4j.py` para importar dados do MongoDB para o Neo4j.
2. Execute as consultas no arquivo `queries_neo4j.cypher` no Neo4j.

### Notebooks

- Use `analysis.ipynb` para análise no MongoDB.
- Use `graph_analysis.ipynb` para explorar grafos no Neo4j.

## Dependências

Na raiz do projeto, instale as dependências com o comando abaixo:

pip install -r requirements.txt
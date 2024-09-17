// Jogos lançados em um ano específico e em uma plataforma
MATCH (g:Game)-[:RELEASED_IN]->(y:Year {year: 2012}), (g)-[:AVAILABLE_ON]->(p:Platform {name: "X360"})
RETURN g.title, g.global_sales
ORDER BY g.global_sales DESC;

// Jogos lançados em um determinado ano
MATCH (g:Game)-[:RELEASED_IN]->(y:Year {year: 2013})
RETURN g.title, g.global_sales
ORDER BY g.global_sales DESC;

// Jogos de um determinado gênero
MATCH (g:Game)-[:CATEGORIZED_AS]->(gen:Genre {name: "Action"})
RETURN g.title, g.global_sales
ORDER BY g.global_sales DESC;

// Jogos de um publisher específico em um gênero
MATCH (p:Publisher {name: "Electronic Arts"})-[:PUBLISHED]->(g:Game)-[:CATEGORIZED_AS]->(gen:Genre {name: "Sports"})
RETURN g.title, g.global_sales
ORDER BY g.global_sales DESC;

// Jogos mais vendidos em uma plataforma específica
MATCH (g:Game)-[:AVAILABLE_ON]->(p:Platform {name: "PS4"})
RETURN g.title, g.global_sales
ORDER BY g.global_sales DESC
LIMIT 10;

// Jogos disponíveis em uma determinada plataforma
MATCH (g:Game)-[:AVAILABLE_ON]->(p:Platform {name: "N64"})
RETURN g.title, g.global_sales
ORDER BY g.global_sales DESC;

// Top 10 jogos mais vendidos
MATCH (g:Game)
RETURN g.title, g.global_sales
ORDER BY g.global_sales DESC
LIMIT 10;

// Listar os jogos publicados por uma determinada publisher
MATCH (p:Publisher {name: "Activision"})-[:PUBLISHED]->(g:Game)
RETURN g.title, g.global_sales
ORDER BY g.global_sales DESC;

// Contar quantos jogos foram publicados por cada publisher
MATCH (p:Publisher)-[:PUBLISHED]->(g:Game)
RETURN p.name, COUNT(g) AS num_jogos
ORDER BY num_jogos DESC;

// Plataformas que têm mais jogos disponíveis
MATCH (p:Platform)-[:AVAILABLE_ON]->(g:Game)
RETURN p.name, COUNT(g) AS num_jogos
ORDER BY num_jogos DESC;

//Consultas com grafos
//Retornar os primeiros 25 relacionamentos existentes
MATCH p=()-[:PUBLISHED]->() RETURN p LIMIT 25;

//Jogos Lançados em um Ano Específico e Disponíveis em uma Plataforma
MATCH (g:Game)-[rel1:AVAILABLE_ON]->(p:Platform {name: "PS3"}), (g)-[rel2:RELEASED_IN]->(y:Year {year: 2010})
RETURN g, rel1, rel2, p, y
LIMIT 80;

//Jogos e Seus Gêneros
MATCH (g:Game)-[rel:CATEGORIZED_AS]->(gen:Genre)
RETURN g, rel, gen
LIMIT 500;

//Jogos Disponíveis em uma Plataforma Específica
MATCH (g:Game)-[rel:AVAILABLE_ON]->(p:Platform {name: "PS4"})
RETURN g, rel, p
LIMIT 75;

//Jogos Disponíveis em Múltiplas Plataformas
MATCH (g:Game)-[rel:AVAILABLE_ON]->(p:Platform)
WITH g, COUNT(p) AS num_plataformas, collect(p) AS platforms, collect(rel) AS rels
WHERE num_plataformas > 1
UNWIND platforms AS platform
UNWIND rels AS rel
RETURN g, rel, platform
LIMIT 150;

//Plataformas e Vendas Globais dos Jogos
MATCH (g:Game)-[rel:AVAILABLE_ON]->(p:Platform)
RETURN g, rel, p
ORDER BY g.global_sales DESC
LIMIT 75;

//Retornar todos os relacionamentos existentes
MATCH p=()-[]->() RETURN p;//DEIXAR PARA O FINAL!!!!
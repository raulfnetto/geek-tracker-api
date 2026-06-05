#Tabela de criação de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL
);

#Tabela de criação de obras associadas aos usuários
CREATE TABLE IF NOT EXISTS obras (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    titulo VARCHAR(255) NOT NULL,
    categoria VARCHAR(50) NOT NULL, -- Ex: Filme, Jogo (tipo LoL), Anime, Série
    status VARCHAR(50) NOT NULL,    -- Ex: Concluído, Jogando, Quero Assistir
    nota INTEGER,                   -- Ex: de 1 a 10
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

#A tabela de integração e unificação das duas obviamente foi oculta
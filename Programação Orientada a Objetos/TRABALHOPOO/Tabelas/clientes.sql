CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Chave primária única
    nome VARCHAR(100) NOT NULL,       -- Nome do cliente
    cnpj VARCHAR(100) NOT NULL UNIQUE,    -- CNPJ (com 14 caracteres, sem pontos ou traços)
    telefone VARCHAR(20),             -- Telefone do cliente
    email VARCHAR(100) UNIQUE,        -- E-mail do cliente (único)
    endereco VARCHAR(100),                    -- Endereço do cliente
    data_cadastro VARCHAR(100) -- Data de cadastro com valor padrão
);
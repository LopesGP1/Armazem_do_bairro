create database armazem_bd;
USE armazem_bd;


CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome_completo VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo_usuario ENUM('cliente','gerente','funcionario','admin') NOT NULL 
);

CREATE TABLE carteira (
    id_carteira INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    saldo DECIMAL(10,2) DEFAULT 0,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);
CREATE TABLE transacao_carteira (
    id_transacao INT AUTO_INCREMENT PRIMARY KEY,
    id_carteira INT NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    tipo ENUM('entrada','saida') NOT NULL,
    descricao VARCHAR(255),
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_carteira) REFERENCES carteira(id_carteira)
);

-- ==========================================
-- Criação da tabela de categorias
-- ==========================================
CREATE TABLE IF NOT EXISTS categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT
);

-- ==========================================
-- Criação da tabela de produtos
-- ==========================================
CREATE TABLE IF NOT EXISTS produto (
    id_produto INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE, -- agora o nome é único
    id_categoria INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    unidade_medida ENUM('UN', 'KG') NOT NULL,
    estoque DECIMAL(10,2) NOT NULL,
    descricao TEXT,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE,
    imagem VARCHAR(255),
    FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria)
);

CREATE TABLE carrinho (
    id_carrinho INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('aberto','finalizado','cancelado') DEFAULT 'aberto',
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE item_carrinho (
    id_item INT AUTO_INCREMENT PRIMARY KEY,
    id_carrinho INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_carrinho) REFERENCES carrinho(id_carrinho),
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
);

CREATE TABLE pedido (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor_total DECIMAL(10,2) NOT NULL,
    status ENUM('pendente','pago','enviado','cancelado') DEFAULT 'pendente',
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE item_pedido (
    id_item INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade DECIMAL(10,2) NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
);

-- ==========================================
-- Inserção de categorias
-- ==========================================
INSERT INTO categoria (nome, descricao) VALUES
('Frutas', 'Frutas frescas e naturais'),
('Verduras e Legumes', 'Produtos hortifrúti'),
('Laticínios', 'Leite, queijos e derivados'),
('Bebidas', 'Sucos, refrigerantes e água'),
('Padaria', 'Pães, bolos e doces'),
('Higiene', 'Produtos de higiene pessoal'),
('Limpeza', 'Produtos de limpeza doméstica');

-- ==========================================
-- Inserção de produtos
-- ==========================================
INSERT INTO produto (nome, id_categoria, preco_unitario, unidade_medida, estoque, descricao, imagem) VALUES
('Maçã', 1, 5.50, 'KG', 20, 'Maçã vermelha fresca', 'static/img/produtos/maca.jpg'),
('Banana', 1, 3.20, 'KG', 30, 'Banana nanica', 'static/img/produtos/banana.jpg'),
('Alface', 2, 2.50, 'UN', 50, 'Alface americana', 'static/img/produtos/alface.jpg'),
('Tomate', 2, 4.00, 'KG', 25, 'Tomate italiano', 'static/img/produtos/tomate.jpg'),
('Leite Integral', 3, 4.50, 'UN', 40, 'Leite integral 1L', 'static/img/produtos/leite.jpg'),
('Queijo Mussarela', 3, 25.00, 'KG', 10, 'Queijo mussarela fresco', 'static/img/produtos/queijo.jpg'),
('Refrigerante Coca-Cola', 4, 7.50, 'UN', 60, 'Refrigerante 2L', 'static/img/produtos/coca.jpg'),
('Suco de Laranja', 4, 6.00, 'UN', 30, 'Suco natural 1L', 'static/img/produtos/suco.jpg'),
('Pão Francês', 5, 0.50, 'UN', 100, 'Pãozinho fresco', 'static/img/produtos/pao.jpg'),
('Bolo de Chocolate', 5, 15.00, 'UN', 20, 'Bolo de chocolate caseiro', 'static/img/produtos/bolo.jpg'),
('Sabonete Dove', 6, 3.50, 'UN', 50, 'Sabonete hidratante', 'static/img/produtos/sabonete.jpg'),
('Shampoo Pantene', 6, 12.00, 'UN', 40, 'Shampoo nutritivo', 'static/img/produtos/shampoo.jpg'),
('Detergente Ypê', 7, 2.50, 'UN', 60, 'Detergente líquido 500ml', 'static/img/produtos/detergente.jpg'),
('Água Mineral', 4, 3.00, 'UN', 100, 'Água mineral 1,5L', 'static/img/produtos/agua.jpg'),
('Cenoura', 2, 3.00, 'KG', 35, 'Cenoura fresca', 'static/img/produtos/cenoura.jpg');

-- ==========================================
-- Consulta para visualizar produtos com categorias
-- ==========================================
SELECT 
    p.id_produto,
    p.nome AS nome_produto,
    c.nome AS nome_categoria,
    p.preco_unitario,
    p.unidade_medida,
    p.estoque,
    p.descricao,
    p.imagem,
    p.data_cadastro,
    p.ativo
FROM 
    produto p
JOIN 
    categoria c ON p.id_categoria = c.id_categoria;

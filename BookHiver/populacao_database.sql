CREATE DATABASE bookhiver;

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL,
    senha VARCHAR(50) NOT NULL
);

CREATE TABLE livros(
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(50) NOT NULL,
    autor VARCHAR(50) NOT NULL,
    editora VARCHAR(50) NOT NULL,
    ano_publicacao INTEGER NOT NULL,
    isbn VARCHAR(14) NOT NULL,
    genero VARCHAR(50) NOT NULL,
    idioma VARCHAR(50) NOT NULL,
    qtde_paginas INTEGER
);

CREATE TABLE leitores(
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cpf VARCHAR(11) NOT NULL,
    email VARCHAR(50) NOT NULL,
    telefone VARCHAR(20) NOT NULL
);

CREATE TABLE emprestimos(
    id SERIAL PRIMARY KEY NOT NULL,
    leitor VARCHAR(50) NOT NULL,
    dataemprestimo DATE NOT NULL,
    isbn VARCHAR(13) NOT NULL,
    situacao VARCHAR(20) NOT NULL,
    data_devolucao_prevista DATE GENERATED ALWAYS AS (dataemprestimo + '7 days'::interval) STORED,
    data_devolucao_real DATE
);
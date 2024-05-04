CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS pictures (picture text PRIMARY KEY, embedding vector(768));
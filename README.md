CREATE DATABASE RAG;

CREATE TABLE documents(
	id INT PRIMARY KEY AUTO_INCREMENT,
	text TEXT,
	embedding VECTOR(1024)
);

USE RAG;
SELECT * FROM documents;
SELECT * FROM documents WHERE id=1;

python -m venv .env
pip list
pip install --upgrade pip
pip install pandas
pip install sentence-transformers
pip install mysql-connector-python
pip install ollama

pip install -r requirements.txt

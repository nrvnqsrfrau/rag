import json
import pandas as pd
import mysql.connector

from sentence_transformers import SentenceTransformer

# Create Instance for Embedding
embedding = SentenceTransformer('BAAI/bge-m3')


# db = mysql.connector.connect(
#   host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
#   port = 4000,
#   user = "2h2urJdiLhXdEiK.root",
#   password = "p3C51VnKymF1IYnV",
#   database = "RAG",
#   ssl_ca = "cert.pem",
#   ssl_verify_cert = True,
#   ssl_verify_identity = True
# )

curr = db.cursor()

df = pd.read_csv("data_knowledge.csv")
# print(df)

for index, row in df.iterrows():
    text = str(row['question']) + " " + str(row['answer'])
    # print(text)
    try:
      embedding_list = embedding.encode(text).tolist()
      #print(embedding_list)
      embedding_str = json.dumps(embedding_list)

      sql_query = """
                  INSERT into documents (text,embedding) VALUES (%s,%s)
      
      """

      curr.execute(sql_query, (text, embedding_str))
      print(f"Data Index-{index} Berhasil ditambah")
    except Exception as e: 
      print("Data Index-{index} Error: {e}")
      print(f"Data Index-{index} Gagal ditambah")

db.commit()
curr.close()
print("Data berhasil di tambahkan")
import mysql.connector
import json
import ollama

from sentence_transformers import SentenceTransformer

OLLAMA_HOST = "http://127.0.0.1:11434"
OLLAMA_MODEL = "deepseek"

llm_agent = ollama.Client(host=OLLAMA_HOST)
embedding = SentenceTransformer("BAAI/bge-m3")

db = mysql.connector.connect(
  host = "[ENDPOINT]",
  port = 4000,
  user = "[USER]",
  password = "[PASS]",
  database = "RAG",
  ssl_ca = "cert.pem",
  ssl_verify_cert = True,
  ssl_verify_identity = True
)



def search_document(database, query, top_k=5):
    results = []
    query_embedding_list = embedding.encode(query).tolist()
    query_embedding_str = json.dumps(query_embedding_list)

    curr = database.cursor()

    sql_query = f"""
                SELECT text, vec_cosine_distance(embedding,%s) AS distance
                FROM documents
                ORDER BY distance ASC
                LIMIT {top_k}
        """

    curr.execute(sql_query,(query_embedding_str,))
    search_results = curr.fetchall()
    database.commit()
    curr.close()
    # print(search_results)
    for result in search_results:
        text, distance = result
        results.append({
            'text': text,
            'distance': distance
        })
    return results

def response_query(database, query):
    retrieved_doc = search_document(database, query)
    # print(retrieved_doc)
    context = "\n".join([doc['text'] for doc in retrieved_doc])
    prompt = f"Answer the following question on provided context {context}\n\nquestion:{query}" 
    response = llm_agent.chat(model=OLLAMA_MODEL, messages=[
        {
            'role':'user',
            'content': prompt
        }
    ])

    return response['message']['content']

if __name__ == "__main__":
    print("AI Agent Start :")
    while True:
        query_text = input("Prompt : ")

        if query_text.lower() in ['exit','quit','q']:
            print("Closing AI Agent ...")
            break

        response = response_query(database=db, query=query_text)
        print("AI Agent : ", response)

print("AI Agent End")

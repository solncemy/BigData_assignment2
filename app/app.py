#!/usr/bin/env python3
from cassandra.cluster import Cluster
import numpy as np
from pyspark import SparkContext
from pyspark.sql import SparkSession
import math

def create_vector_space():
    cluster = Cluster(['cassandra-server'])
    session = cluster.connect('search_engine')
    
    session.execute("""
        CREATE TABLE IF NOT EXISTS document_vectors (
            doc_id text PRIMARY KEY,
            vector vector<float, 1000>
        )
    """)
    
    vocab_size = session.execute("SELECT COUNT(*) FROM vocabulary").one()[0]
    
    terms = [row.term for row in session.execute("SELECT term FROM vocabulary")]
    
    documents = session.execute("SELECT doc_id, title FROM documents")
    
    spark = SparkSession.builder \
        .appName("Vector Space Creation") \
        .getOrCreate()
    
    for doc in documents:
        doc_id = doc.doc_id
        vector = np.zeros(vocab_size)
        
        for i, term in enumerate(terms):
            result = session.execute("SELECT docs FROM vocabulary WHERE term = %s", (term,)).one()
            if result:
                for doc_info in result.docs.split(','):
                    if doc_info.startswith(doc_id):
                        tf = int(doc_info.split(':')[1])
                        df = len(result.docs.split(','))
                        N = session.execute("SELECT COUNT(*) FROM documents").one()[0]
                        idf = math.log(N / df)
                        vector[i] = tf * idf
        
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        session.execute(
            "INSERT INTO document_vectors (doc_id, vector) VALUES (%s, %s)",
            (doc_id, vector.tolist())
        )
    
    spark.stop()

def vector_search(query):
    cluster = Cluster(['cassandra-server'])
    session = cluster.connect('search_engine')
    
    terms = query.lower().split()
    
    vocab_size = session.execute("SELECT COUNT(*) FROM vocabulary").one()[0]
    query_vector = np.zeros(vocab_size)
    
    terms_list = [row.term for row in session.execute("SELECT term FROM vocabulary")]
    
    for term in terms:
        if term in terms_list:
            idx = terms_list.index(term)
            result = session.execute("SELECT docs FROM vocabulary WHERE term = %s", (term,)).one()
            if result:
                df = len(result.docs.split(','))
                N = session.execute("SELECT COUNT(*) FROM documents").one()[0]
                idf = math.log(N / df)
                query_vector[idx] = idf
    
    norm = np.linalg.norm(query_vector)
    if norm > 0:
        query_vector = query_vector / norm
    
    results = session.execute("""
        SELECT doc_id, vector, cosine_similarity(vector, %s) as similarity 
        FROM document_vectors 
        ORDER BY similarity DESC 
        LIMIT 10
    """, (query_vector.tolist(),))
    
    for result in results:
        doc_id = result.doc_id
        title = session.execute("SELECT title FROM documents WHERE doc_id = %s", (doc_id,)).one().title
        print(f"Document ID: {doc_id}, Title: {title}, Similarity: {result.similarity}")

if __name__ == "__main__":
    create_vector_space()
    
    query = "example search query"
    vector_search(query)
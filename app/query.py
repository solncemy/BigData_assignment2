#!/usr/bin/env python3
import sys
from pyspark import SparkContext
from cassandra.cluster import Cluster
import math
import re

def tokenize(text):
    return re.findall(r'\w+', text.lower())

def calculate_bm25(term, doc_info, N, avg_dl, k1=1.2, b=0.75):
    doc_id, tf, dl = doc_info.split(':')
    tf = int(tf)
    dl = int(dl)
    
    df = len(doc_info.split(','))
    idf = math.log((N - df + 0.5) / (df + 0.5) + 1)
    
    numerator = tf * (k1 + 1)
    denominator = tf + k1 * (1 - b + b * (dl / avg_dl))
    return (doc_id, idf * (numerator / denominator))

def main():
    if len(sys.argv) != 2:
        print("Usage: query.py <query>")
        sys.exit(1)
        
    query = sys.argv[1]
    terms = tokenize(query)
    
    cluster = Cluster(['cassandra-server'])
    session = cluster.connect('search_engine')
    
    N = session.execute("SELECT COUNT(*) FROM documents").one()[0]
    avg_dl = session.execute("SELECT AVG(avg_length) FROM documents").one()[0]
    
    sc = SparkContext(appName="BM25 Search")
    
    term_docs = {}
    for term in terms:
        result = session.execute("SELECT docs FROM vocabulary WHERE term = %s", (term,)).one()
        if result:
            term_docs[term] = result.docs
    
    scores = {}
    for term, docs in term_docs.items():
        for doc_info in docs.split(','):
            doc_id, score = calculate_bm25(term, doc_info, N, avg_dl)
            scores[doc_id] = scores.get(doc_id, 0) + score
    
    top_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
    
    for doc_id, score in top_docs:
        result = session.execute("SELECT title FROM documents WHERE doc_id = %s", (doc_id,)).one()
        if result:
            print(f"Document ID: {doc_id}, Title: {result.title}, Score: {score}")
    
    sc.stop()

if __name__ == "__main__":
    main()
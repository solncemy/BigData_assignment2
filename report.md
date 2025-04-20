## Methodology

### Comments of work and how it is implemented

1. **Data Preparation**
   - PySpark to read and process file
   - Standartize the name of files
   - Processing files to HDFS

2. **Indexing Pipeline**
   - MapReduce pipeline for document indexing
   - Mapper tokenizes documents and emits term-document pairs with frequencies
   - Reducer calculates document frequencies and prepares data for Cassandra
   - Cassandra to store:
     - Vocabulary table: terms, document frequencies, and document lists
     - Documents table: document IDs, titles, and average lengths
     - Document vectors table: TF-IDF vectors for vector search

3. **BM25 Ranking**
   - BM25 scoring in PySpark
   - Cassandra for storing and sattistics of documents
   - IDF using document frequencies
   - Length normalization and term frequency saturation
   - k1=1.2 and b=0.75 as standard parameters

4. **Vector Search (Extra Credit)**
   - TF-IDF vectors
   - Stored vectors in Cassandra using vector type
   - Cosine similarity search
   - Normalized vectors for better similarity comparison

## Demonstration (Sorry, I do not have ability to attached the photoes because of I'm not in Innopolis)

### Running

1. **Start Services**
   ```bash
   docker-compose up
   ```
  Services and run the indexing process.

2. **Index Documents**
   ```bash
   ./app/index.sh /index/data
   ```
  Index the documents in the specified path.

3. **Search Documents**
   ```bash
   ./app/search.sh "your search query"
   ```
  Top 10 most relevant documents.

4. **Vector Search**
   ```bash
   python3 app.py
   ``` 
   Vector space and perform vector similarity search.




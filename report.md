## Methodology

### Design Choices and Implementation Details

1. **Data Preparation**
   - Used PySpark to read and process the parquet file
   - Created text documents with standardized naming format
   - Stored documents in HDFS for distributed processing

2. **Indexing Pipeline**
   - Implemented a MapReduce pipeline for document indexing
   - Mapper tokenizes documents and emits term-document pairs with frequencies
   - Reducer calculates document frequencies and prepares data for Cassandra
   - Used Cassandra to store:
     - Vocabulary table: terms, document frequencies, and document lists
     - Documents table: document IDs, titles, and average lengths
     - Document vectors table: TF-IDF vectors for vector search

3. **BM25 Ranking**
   - Implemented BM25 scoring in PySpark
   - Used Cassandra to store and retrieve document statistics
   - Calculated IDF using document frequencies
   - Applied length normalization and term frequency saturation
   - Used k1=1.2 and b=0.75 as standard BM25 parameters

4. **Vector Search (Extra Credit)**
   - Created TF-IDF vectors for all documents
   - Stored vectors in Cassandra using vector type
   - Implemented cosine similarity search
   - Used normalized vectors for better similarity comparison

### Components

1. **MapReduce Pipeline**
   - `mapper1.py`: Tokenizes documents and emits term-document pairs
   - `reducer1.py`: Calculates document frequencies and prepares data for Cassandra

2. **Indexing Script**
   - `index.sh`: Runs MapReduce job and stores results in Cassandra
   - Creates necessary Cassandra tables and keyspaces

3. **Search Implementation**
   - `query.py`: Implements BM25 ranking using PySpark
   - `search.sh`: Runs the search engine with proper environment setup

4. **Vector Search**
   - `app.py`: Implements vector space creation and similarity search
   - Uses Cassandra's vector capabilities for efficient similarity search

## Demonstration (Sorry, I do not have ability to attached the photoes because of I'm not in Innopolis)

### Running the Search Engine

1. **Start Services**
   ```bash
   docker-compose up
   ```
   This will start all required services and run the indexing process.

2. **Index Documents**
   ```bash
   ./app/index.sh /index/data
   ```
   This will index the documents in the specified path.

3. **Search Documents**
   ```bash
   ./app/search.sh "your search query"
   ```
   This will return the top 10 most relevant documents.

4. **Vector Search**
   ```bash
   python3 app.py
   ```
   This will create the vector space and perform vector similarity search.




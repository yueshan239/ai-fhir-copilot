import os
import json

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from config import settings

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge", "fhir_docs")
VECTORSTORE_DIR = os.path.join(os.path.dirname(__file__), "..", "vectorstore")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# IRIS vector store table name
IRIS_VECTOR_TABLE = "fhir_knowledge"
EMBEDDING_DIMENSIONS = 384  # MiniLM-L6-v2 outputs 384 dimensions


def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def load_documents():
    """Load and split documents from knowledge directory."""
    loader = DirectoryLoader(
        KNOWLEDGE_DIR,
        glob="**/*.md",
        loader_cls=TextLoader,
    )
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    return splitter.split_documents(docs)


def get_iris_connection():
    """Get IRIS database connection."""
    try:
        import intersystems_iris
    except ImportError:
        raise ImportError("intersystems-iris package not installed. Run: uv pip install intersystems-iris")

    # Extract host from IRIS_HOST (remove http://)
    host = settings.IRIS_HOST.replace("http://", "").replace("https://", "").split(":")[0]
    port = settings.IRIS_SQL_PORT
    namespace = settings.IRIS_NAMESPACE
    username = settings.IRIS_USERNAME
    password = settings.IRIS_PASSWORD

    return intersystems_iris.connect(host, port, namespace, username, password)


def init_iris_vector_table():
    """Create vector table in IRIS if not exists."""
    conn = get_iris_connection()
    cursor = conn.cursor()

    try:
        # Create table with native VECTOR type for embeddings
        # VECTOR(DOUBLE, 384) for MiniLM-L6-v2 embeddings
        cursor.execute(f"""
            CREATE TABLE {IRIS_VECTOR_TABLE} (
                ID INT IDENTITY,
                Content LONGVARCHAR,
                Metadata LONGVARCHAR,
                Embedding VECTOR(DOUBLE, {EMBEDDING_DIMENSIONS}),
                CONSTRAINT PK_{IRIS_VECTOR_TABLE} PRIMARY KEY (ID)
            )
        """)
        conn.commit()
    except Exception as e:
        # Table might already exist, which is fine
        if "already exists" not in str(e).lower():
            raise e
    finally:
        cursor.close()
        conn.close()


def build_vectorstore_iris():
    """Build vector store in IRIS."""
    chunks = load_documents()
    embeddings = get_embeddings()

    # Initialize table
    init_iris_vector_table()

    # Get embeddings for all chunks
    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]
    vectors = embeddings.embed_documents(texts)

    # Store in IRIS
    conn = get_iris_connection()
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute(f"DELETE FROM {IRIS_VECTOR_TABLE}")

    # Insert new data with native VECTOR type
    for i, (text, metadata, vector) in enumerate(zip(texts, metadatas, vectors)):
        # Convert vector to string format for TO_VECTOR function
        vector_str = ",".join(str(v) for v in vector)
        cursor.execute(
            f"INSERT INTO {IRIS_VECTOR_TABLE} (Content, Metadata, Embedding) VALUES (?, ?, TO_VECTOR(?, DOUBLE, {EMBEDDING_DIMENSIONS}))",
            (text, json.dumps(metadata), vector_str)
        )

    conn.commit()
    cursor.close()
    conn.close()

    return {"status": "ok", "count": len(chunks)}


def search_iris(query: str, k: int = 3):
    """Search IRIS vector store using native vector similarity."""
    embeddings = get_embeddings()
    query_vector = embeddings.embed_query(query)

    conn = get_iris_connection()
    cursor = conn.cursor()

    # Convert query vector to string for TO_VECTOR
    query_vector_str = ",".join(str(v) for v in query_vector)

    # Use IRIS native VECTOR_DOT_PRODUCT for similarity search
    # Higher dot product = more similar (for normalized vectors)
    cursor.execute(f"""
        SELECT TOP {k} Content, Metadata,
               VECTOR_DOT_PRODUCT(Embedding, TO_VECTOR(?, DOUBLE, {EMBEDDING_DIMENSIONS})) AS Score
        FROM {IRIS_VECTOR_TABLE}
        ORDER BY Score DESC
    """, (query_vector_str,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [row[0] for row in rows]


def build_vectorstore_faiss():
    """Build FAISS vector store."""
    chunks = load_documents()
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTORSTORE_DIR)
    return vectorstore


def get_vectorstore_faiss():
    """Get FAISS vector store instance."""
    embeddings = get_embeddings()
    if os.path.exists(VECTORSTORE_DIR) and os.listdir(VECTORSTORE_DIR):
        return FAISS.load_local(
            VECTORSTORE_DIR,
            embeddings,
            allow_dangerous_deserialization=True,
        )
    return build_vectorstore_faiss()


def build_vectorstore():
    """Build vector store based on configured type."""
    if settings.VECTOR_STORE_TYPE == "iris":
        return build_vectorstore_iris()
    return build_vectorstore_faiss()


def search(query: str, k: int = 3):
    """Search for similar documents."""
    if settings.VECTOR_STORE_TYPE == "iris":
        try:
            return search_iris(query, k)
        except Exception as e:
            print(f"IRIS vector search failed, falling back to FAISS: {e}")
            # Fallback to FAISS
            vectorstore = get_vectorstore_faiss()
            results = vectorstore.similarity_search(query, k=k)
            return [doc.page_content for doc in results]

    # FAISS search
    vectorstore = get_vectorstore_faiss()
    results = vectorstore.similarity_search(query, k=k)
    return [doc.page_content for doc in results]

import os
import sys
import uvicorn


def ensure_vectorstore():
    """Build vectorstore on first startup if it doesn't exist."""
    from config import reload_settings
    from services.rag_service import build_vectorstore

    # Reload settings from settings.json (if exists)
    reload_settings()

    # Always check FAISS
    vectorstore_dir = os.path.join(os.path.dirname(__file__), "vectorstore")
    if not os.path.exists(vectorstore_dir) or not os.listdir(vectorstore_dir):
        print("Building FAISS vectorstore...", flush=True)
        build_vectorstore()
        print("FAISS vectorstore built.", flush=True)

    # Also ensure IRIS table exists (for easy switching)
    try:
        from services.rag_service import get_iris_connection, IRIS_VECTOR_TABLE
        conn = get_iris_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {IRIS_VECTOR_TABLE}")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        print(f"IRIS vector table ready ({count} records).", flush=True)
    except Exception:
        try:
            from services.rag_service import build_vectorstore_iris
            build_vectorstore_iris()
            print("IRIS vector table built.", flush=True)
        except Exception as e:
            print(f"IRIS build skipped: {e}", flush=True)


def main():
    ensure_vectorstore()
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()

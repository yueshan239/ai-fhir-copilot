#!/usr/bin/env python3
"""Build the FAISS vectorstore from FHIR knowledge documents."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.rag_service import build_vectorstore


def main():
    print("Building FAISS vectorstore from FHIR knowledge documents...")
    print("Loading documents from knowledge/fhir_docs/")
    print()

    vectorstore = build_vectorstore()

    doc_count = vectorstore.index.ntotal
    print(f"Successfully built vectorstore with {doc_count} vectors")
    print(f"Saved to vectorstore/")
    print()
    print("Done! Restart the server to use the new vectorstore.")


if __name__ == "__main__":
    main()

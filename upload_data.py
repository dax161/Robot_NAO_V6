import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma


from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

def cargar_documentos(ruta_archivo: str):
    """
    Carga un PDF y realiza chunking semántico usando SemanticChunker.
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo {ruta_archivo} no existe.")

    loader = PyMuPDFLoader(ruta_archivo)
    documentos = loader.load()

    embed_model = FastEmbedEmbeddings(
        model_name="BAAI/bge-small-en"
    )

    text_splitter = SemanticChunker(
        embeddings=embed_model,
        breakpoint_threshold_type="percentile",       # Método de ruptura
        breakpoint_threshold_amount=95.0,             # Umbral en percentil (opcional)
        min_chunk_size=500,                           # Tamaño mínimo del chunk
        buffer_size=1                                 # Buffer alrededor de cambios
    )

    docs_semantic = text_splitter.split_documents(documentos)
    return docs_semantic

def crear_vectorstore(docs):
    """
    Crea un vectorstore persistente en ChromaDB usando FastEmbedEmbeddings.
    Aquí es donde se puede aprovechar el chunking semántico al indexar
    con embeddings para búsquedas semánticas.
    """
    embed_model = FastEmbedEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embed_model,
        persist_directory="chroma_db_dir",
        collection_name="upc_data"
    )
    return vectorstore
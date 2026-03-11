from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from upload_data import cargar_documentos, crear_vectorstore
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
import subprocess
import json
from transcribir_audio import transcribir_audio  # Función que creamos

# Códigos de escape ANSI para colores
AZUL = "\033[94m"
VERDE = "\033[92m"
RESET = "\033[0m"

# Función para enviar texto a NAO
def enviar_a_nao(texto):
    """
    Envía texto al NAO usando Python 2.7 y el script nao_speak.py
    """
    proceso = subprocess.run(
        ["C:/Python27/python.exe", "nao_speak.py"],
        input=json.dumps({"texto": texto}),
        text=True,
        capture_output=True
    )
    print("Salida NAO:", proceso.stdout)

def iniciar_chat(ruta_archivo: str):
    # LLM local con Ollama
    llm = Ollama(model="llama3.2:3b")

    # Embeddings locales
    embed_model = FastEmbedEmbeddings(model_name="BAAI/bge-small-en")

    # Conectar o crear vectorstore
    vectorstore = Chroma(
        embedding_function=embed_model,
        persist_directory="chroma_db_dir",
        collection_name="upc_data"
    )

    if len(vectorstore.get()['ids']) == 0:
        docs = cargar_documentos(ruta_archivo)
        vectorstore = crear_vectorstore(docs)

    retriever = vectorstore.as_retriever(search_kwargs={'k': 4})

    prompt_template = """
    You are Nao, a humanoid robot assistant that answers questions 
    about the Universidad Peruana de Ciencias Aplicadas (UPC), 
    its Mechatronics Engineering program, its Fab Lab, 
    and the Laureate network.

    Users may mispronounce words or the speech-to-text may contain mistakes. 
    Infer the intended meaning of their question even if some words are unclear. 
    Focus on context and the most common questions people usually ask:

    1. Who is the Chairman of the Board of Laureate?
    2. Who are the 2 ladies members of the board of Laureate?
    3. What is the Mission of UPC?
    4. What is Mechatronics Engineering?
    5. What equipment is in the FABLAB?
    6. What activities are carried out in the FABLAB?
    7. When was UPC founded?

    Guidelines for answers:
    - Speak in English.
    - Give answers that are clear, natural, and engaging. 
    - Keep them short enough to be understood when spoken aloud, 
    but not so short that they sound robotic or boring. 
    A good length is 2 to 4 sentences.
    - If you don’t know the answer, say: 
    "I’m sorry, I don’t know the answer to that."

    Context: {context}
    Question: {question}

    Answer:
    """

    prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    print("¡Bienvenido al chat por audio! Ctrl+C para salir.")

    while True:
        # 1️⃣ Llamar al script que graba el audio del NAO
        subprocess.run(["C:/Python27/python.exe", "audio_nao.py"])

        # 2️⃣ Transcribir el audio a texto
        pregunta = transcribir_audio("audio/grabacion.wav")
        print(f"Pregunta transcrita: {pregunta}")

        # 3️⃣ Enviar la pregunta al RAG
        respuesta = qa.invoke({"query": pregunta})
        texto_respuesta = respuesta["result"]

        # 4️⃣ Mostrar respuesta y enviarla al NAO
        print(f"{VERDE}Asistente:{RESET} {texto_respuesta}")
        enviar_a_nao(texto_respuesta)

if __name__ == "__main__":
    ruta_archivo = "src/upc_data.pdf"
    iniciar_chat(ruta_archivo)





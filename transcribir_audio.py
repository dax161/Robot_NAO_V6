from faster_whisper import WhisperModel

def transcribir_audio(audio_path: str, modelo: str = "small", device: str = "cpu") -> str:
    """
    Transcribe un archivo de audio usando Faster-Whisper y devuelve todo el texto concatenado.

    Args:
        audio_path (str): Ruta del archivo de audio (.wav, .mp3, etc.).
        modelo (str): Tamaño del modelo Whisper ("tiny", "base", "small", "medium", "large").
        device (str): Dispositivo para la inferencia ("cpu" o "cuda").

    Returns:
        str: Texto transcrito del audio.
    """
    # Cargar el modelo (CPU por defecto)
    model = WhisperModel(modelo, device=device)

    # Transcribir el audio
    segments, info = model.transcribe(audio_path)

    # Concatenar todos los segmentos en un solo texto
    texto_completo = " ".join(segment.text for segment in segments)

    return texto_completo

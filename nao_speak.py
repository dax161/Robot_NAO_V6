# -*- coding: utf-8 -*-
from naoqi import ALProxy
import sys
import json

# Configuración de NAO
NAO_IP = "192.168.137.216"
NAO_PORT = 9559

# Configuración para que hable con gestos
cfg = {"bodyLanguageMode": "contextual"} 

def decir_nao(texto):
    try:
        # Forzar conversión a UTF-8 solo si estás en Python 2
        if isinstance(texto, unicode):  
            texto = texto.encode("utf-8")

        # Usar ALAnimatedSpeech en lugar de ALTextToSpeech
        anim = ALProxy("ALAnimatedSpeech", NAO_IP, NAO_PORT)
        anim.say(texto, cfg)

    except Exception as e:
        print("Error al conectar con NAO:", e)

if __name__ == "__main__":
    try:
        entrada = sys.stdin.read()
        datos = json.loads(entrada)
        texto_a_decir = datos.get("texto", "")

        if texto_a_decir:
            decir_nao(texto_a_decir)
            print("Texto enviado al NAO:", texto_a_decir)
        else:
            print("No se recibió texto válido.")
    except Exception as e:
        print("Error al procesar entrada:", e)

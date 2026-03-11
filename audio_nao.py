# -*- coding: utf-8 -*-
import time
import os
from naoqi import ALProxy
import paramiko  # Para descargar el archivo

# Configuración de la conexión al NAO
NAO_IP = "192.168.137.216"  # Cambia esta IP por la de tu robot
PORT = 9559 

cfg = {"bodyLanguageMode": "contextual"} 
anim = ALProxy("ALAnimatedSpeech", NAO_IP, PORT)

# Proxies para los módulos necesarios
tts = ALProxy("ALTextToSpeech", NAO_IP, PORT)
audio_recorder = ALProxy("ALAudioRecorder", NAO_IP, PORT)
audio_player = ALProxy("ALAudioPlayer", NAO_IP, PORT)
memory = ALProxy("ALMemory", NAO_IP, PORT)

# Archivo de salida en NAO
output_file = "/home/nao/recording.wav"

anim.say("Hello, my name is Nao, I am your personal assistant, touch my head to start", cfg)

try:
    anim.say("I'm ready to hear your questions", cfg)

    # --------------------------
    # 1️⃣ Esperar toque en la cabeza
    # --------------------------
    while True:
        head_touch = memory.getData("FrontTactilTouched")
        if head_touch == 1.0:  # 1.0 significa tocado
            break
        time.sleep(0.1)

    # --------------------------
    # 2️⃣ Preparar la grabación limpia
    # --------------------------
    try:
        audio_recorder.stopMicrophonesRecording()
    except:
        pass

    # Limpieza de archivos previos
    if os.path.exists(output_file):
        os.remove(output_file)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_folder = os.path.join(script_dir, "audio")
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)
    local_file = os.path.join(local_folder, "grabacion.wav")
    if os.path.exists(local_file):
        os.remove(local_file)

    # --------------------------
    # 3️⃣ Avisar antes de grabar (NAO aún no graba)
    # --------------------------
    anim.say("Touch my right hand when you finish speaking", cfg)

    # --------------------------
    # 4️⃣ Iniciar grabación (sin hablar durante grabación)
    # --------------------------
    channels = [1, 0, 0, 0]  # Solo canal frontal
    audio_recorder.startMicrophonesRecording(output_file, "wav", 16000, channels)

    # --------------------------
    # 5️⃣ Esperar toque en la mano para detener
    # --------------------------
    while True:
        hand_touch = memory.getData("HandRightBackTouched")
        if hand_touch == 1.0:
            break
        time.sleep(0.1)

    # --------------------------
    # 6️⃣ Detener grabación
    # --------------------------
    audio_recorder.stopMicrophonesRecording()
    anim.say("I got it", cfg)

    # --------------------------
    # 7️⃣ Descargar el archivo al PC (credenciales desde variables de entorno)
    # --------------------------
    USERNAME = os.getenv("NAO_USERNAME", "nao")
    PASSWORD = os.getenv("NAO_PASSWORD")
    SSH_PORT = int(os.getenv("NAO_SSH_PORT", "22"))

    if not PASSWORD:
        raise RuntimeError(
            "NAO_PASSWORD no está definida. Define la variable de entorno NAO_PASSWORD antes de ejecutar el script."
        )

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(NAO_IP, SSH_PORT, USERNAME, PASSWORD)

    sftp = ssh.open_sftp()
    sftp.get(output_file, local_file)
    sftp.close()
    ssh.close()

    print("Archivo descargado en:", os.path.abspath(local_file))

except Exception as e:
    anim.say("Sorry, I did not hear well, can you repeat again?", cfg)
    print("Error:", e)


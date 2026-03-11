# nao-agente

Proyecto para interactuar con un robot NAO y un RAG local (Chroma + Ollama). Contiene scripts para grabar audio en NAO, descargar la grabación y procesarla con herramientas locales.

Prerequisitos
- Python 3.11 o 3.12
- Instalar dependencias con `poetry install` o `pip install -r requirements.txt`

Variables de entorno importantes
- `NAO_IP`: IP del robot NAO (por defecto en el código: 192.168.137.216)
- `NAO_PASSWORD`: contraseña SSH del usuario `nao` en el robot (obligatorio para `audio_nao.py`)
- `NAO_USERNAME` (opcional, por defecto `nao`)
- `NAO_SSH_PORT` (opcional, por defecto `22`)

Uso rápido

1. Exporta las variables de entorno (ejemplo Windows PowerShell):

```powershell
$Env:NAO_PASSWORD = "tu_contraseña"
$Env:NAO_IP = "192.168.137.216"
```

2. Ejecuta el script de audio:

```powershell
python audio_nao.py
```

Subir a GitHub

1. Inicializa repo local (si no está inicializado):

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/dax161/Robot_NAO_V6.git
git branch -M main
git push -u origin main
```

Notas de seguridad
- No subas credenciales (archivos `.env`) al repositorio. Se ha eliminado la contraseña embebida en `audio_nao.py`; usa `NAO_PASSWORD`.

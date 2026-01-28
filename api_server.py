{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "5137fb75-188a-4b25-bda6-e7a09192a7bc",
   "metadata": {},
   "outputs": [
    {
     "ename": "ImportError",
     "evalue": "cannot import name 'AntiCheatDetector' from 'model_core' (C:\\Users\\eliut\\Downloads\\Data Science stuff\\model_core.py)",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mImportError\u001b[0m                               Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[4], line 5\u001b[0m\n\u001b[0;32m      3\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mpydantic\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mimport\u001b[39;00m BaseModel\n\u001b[0;32m      4\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mos\u001b[39;00m\n\u001b[1;32m----> 5\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mmodel_core\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mimport\u001b[39;00m AntiCheatDetector, generar_datos_jugadores \u001b[38;5;66;03m# Importamos nuestro cerebro\u001b[39;00m\n\u001b[0;32m      7\u001b[0m \u001b[38;5;66;03m# Inicializar App\u001b[39;00m\n\u001b[0;32m      8\u001b[0m app \u001b[38;5;241m=\u001b[39m FastAPI(\n\u001b[0;32m      9\u001b[0m     title\u001b[38;5;241m=\u001b[39m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mEmbark Anti-Cheat Oracle\u001b[39m\u001b[38;5;124m\"\u001b[39m,\n\u001b[0;32m     10\u001b[0m     description\u001b[38;5;241m=\u001b[39m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mMicroservicio de detección de anomalías en FPS\u001b[39m\u001b[38;5;124m\"\u001b[39m,\n\u001b[0;32m     11\u001b[0m     version\u001b[38;5;241m=\u001b[39m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124m1.0\u001b[39m\u001b[38;5;124m\"\u001b[39m\n\u001b[0;32m     12\u001b[0m )\n",
      "\u001b[1;31mImportError\u001b[0m: cannot import name 'AntiCheatDetector' from 'model_core' (C:\\Users\\eliut\\Downloads\\Data Science stuff\\model_core.py)"
     ]
    }
   ],
   "source": [
    "# api_server.py\n",
    "from fastapi import FastAPI, HTTPException\n",
    "from pydantic import BaseModel\n",
    "import os\n",
    "from model_core import AntiCheatDetector, generar_datos_jugadores # Importamos nuestro cerebro\n",
    "\n",
    "# Inicializar App\n",
    "app = FastAPI(\n",
    "    title=\"Embark Anti-Cheat Oracle\",\n",
    "    description=\"Microservicio de detección de anomalías en FPS\",\n",
    "    version=\"1.0\"\n",
    ")\n",
    "\n",
    "# Definir el contrato de datos (Schema)\n",
    "class PlayerTelemetry(BaseModel):\n",
    "    player_id: str\n",
    "    time_to_damage_ms: float\n",
    "    aim_path_deviation: float\n",
    "    headshot_rate: float\n",
    "\n",
    "# Instanciar el detector global\n",
    "detector = AntiCheatDetector()\n",
    "MODEL_PATH = \"embark_model.pkl\"\n",
    "\n",
    "# Evento de inicio: Cargar modelo o entrenar uno nuevo si no existe\n",
    "@app.on_event(\"startup\")\n",
    "def load_or_train_model():\n",
    "    if os.path.exists(MODEL_PATH):\n",
    "        detector.load(MODEL_PATH)\n",
    "        print(\"✅ Modelo pre-entrenado cargado exitosamente.\")\n",
    "    else:\n",
    "        print(\"⚠️ No se encontró modelo. Entrenando uno nuevo (Cold Start)...\")\n",
    "        df = generar_datos_jugadores(1000)\n",
    "        detector.train(df, 'is_cheater', ['time_to_damage_ms', 'aim_path_deviation', 'headshot_rate'])\n",
    "        print(\"✅ Modelo entrenado al vuelo.\")\n",
    "\n",
    "@app.get(\"/\")\n",
    "def home():\n",
    "    return {\"message\": \"Anti-Cheat System Online. Use /docs for interface.\"}\n",
    "\n",
    "@app.post(\"/analyze_player\")\n",
    "def analyze_player(telemetry: PlayerTelemetry):\n",
    "    \"\"\"Recibe datos de un jugador y retorna veredicto.\"\"\"\n",
    "    try:\n",
    "        # Mapear datos\n",
    "        input_data = {\n",
    "            'time_to_damage_ms': telemetry.time_to_damage_ms,\n",
    "            'aim_path_deviation': telemetry.aim_path_deviation,\n",
    "            'headshot_rate': telemetry.headshot_rate\n",
    "        }\n",
    "        \n",
    "        result = detector.predict_player(input_data)\n",
    "        \n",
    "        # Respuesta enriquecida\n",
    "        return {\n",
    "            \"player_id\": telemetry.player_id,\n",
    "            \"verdict\": result,\n",
    "            \"timestamp\": pd.Timestamp.now().isoformat()\n",
    "        }\n",
    "        \n",
    "    except Exception as e:\n",
    "        raise HTTPException(status_code=500, detail=f\"Error interno: {str(e)}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b5d0af3a-fdd9-4d48-8888-c6ca9b404dbd",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

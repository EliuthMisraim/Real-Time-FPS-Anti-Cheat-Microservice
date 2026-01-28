# 🛡️ Real-Time FPS Anti-Cheat Microservice (API)

## 📋 Descripción del Proyecto
Este proyecto consiste en un microservicio de alto rendimiento diseñado para la detección de anomalías en videojuegos de disparos en primera persona (FPS). Utiliza un enfoque de **Machine Learning** para analizar la telemetría de los jugadores en tiempo real y emitir veredictos sobre comportamientos sospechosos (trampas/cheating).

El sistema está diseñado siguiendo una arquitectura modular que separa la lógica del modelo de la capa de entrega de servicios, permitiendo escalabilidad y mantenibilidad en entornos de producción.

## 🚀 Funcionalidades Técnicas
* **API de Baja Latencia:** Construida con **FastAPI** y optimizada con **Uvicorn** para procesar datos de telemetría de manera instantánea.
* **Modelo Predictivo:** Implementación de un clasificador **Random Forest** que evalúa variables críticas de juego:
    * `time_to_damage_ms`: Tiempo de reacción al causar daño.
    * `aim_path_deviation`: Desviación en la trayectoria del apuntado.
    * `headshot_rate`: Proporción de disparos a la cabeza.
* **Serialización Eficiente:** Uso de **Joblib** para la persistencia del modelo, asegurando una integración fluida.
* **Sistema Cold Start:** Capacidad de auto-entrenamiento si no se detecta un modelo pre-existente al iniciar el servicio.

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python (Pandas, Scikit-learn, Joblib).
* **Framework:** FastAPI / Uvicorn.
* **Modelo:** Random Forest Classifier.
* **Metodología:** CRISP-DM.



## 🔧 Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone [https://github.com/EliuthMisraim/fps-anticheat-api.git](https://github.com/EliuthMisraim/fps-anticheat-api.git)
cd fps-anticheat-api

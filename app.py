import time
import redis
from flask import Flask, jsonify
import os
import logging
import json
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from datetime import datetime

load_dotenv()

app = Flask("app")

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "name": record.name,
            "time": self.formatTime(record),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

# Configuración del logger
logger = logging.getLogger("jsonLogger")

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Configuración de la caché de Redis
cache = redis.Redis(host='redis', port=6379)

# Configuración de Elasticsearch
ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'elasticsearch')
es = Elasticsearch(f"http://{ELASTICSEARCH_HOST}:9200")

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    logger.info("Request recibido")

    # Crear el mensaje de log
    log_message = {
        "redis_host": REDIS_HOST,
        "redis_port": REDIS_PORT,
        "message": "Request recibido",
        "hits": count,
        "timestamp": datetime.now().isoformat()
    }

    # Indexar datos en Elasticsearch
    try:
        es.index(index="flask-logs", document=log_message)
        logger.info(f"Datos almacenados en Elasticsearch: {log_message}")
    except Exception as e:
        logger.error(f"Error al almacenar en Elasticsearch: {e}")
        return jsonify({"error": str(e)}), 500


    return 'Redis host: {}, Redis port: {} . Hello World! I have been seen {} times.\n'.format(REDIS_HOST, REDIS_PORT, count)

@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Recupera los datos almacenados en Elasticsearch.
    """
    index_name = "flask-logs"
    try:
        response = es.search(index=index_name, query={"match_all": {}})
        hits = response.get("hits", {}).get("hits", [])
        logs = [hit["_source"] for hit in hits]
        logger.info("Datos recuperados desde Elasticsearch")
        return jsonify(logs), 200
    except Exception as e:
        logger.error(f"Error al recuperar datos desde Elasticsearch: {e}")
        return jsonify({"error": str(e)}), 500
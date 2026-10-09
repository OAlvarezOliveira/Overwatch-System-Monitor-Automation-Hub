import psutil
import json


def leer_metricas():
    cpu = psutil.cpu_percent(interval=0.5)
    memoria = psutil.virtual_memory().percent
    disco = psutil.disk_usage("/").percent

    return {"cpu":cpu,"memoria":memoria,"disco":disco}


if __name__ == "__main__":
    while(True):
        metricas = leer_metricas()
        print(json.dumps(metricas)) 
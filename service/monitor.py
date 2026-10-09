import psutil

def leer_metricas():
    cpu = psutil.cpu_percent(interval=0.5)
    memoria = psutil.virtual_memory().percent
    disco = psutil.disk_usage("/").percent

    return cpu,memoria,disco


if __name__ == "__main__":
    while(True):
        print(leer_metricas())    
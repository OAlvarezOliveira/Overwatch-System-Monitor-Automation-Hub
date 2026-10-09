# -*- coding: utf-8 -*-

import os ,psutil



while (True):
    cpu = psutil.cpu_percent(interval=0.5)
    memoria = psutil.virtual_memory().percent
    disco = psutil.disk_usage("/").percent

    print(f"cpu:{cpu}")
    print(f"Porcentaje de memoria :{memoria}")
    print(f"Porcentaje de disco:{disco}")
from monitor import leer_metricas        

def test_leer_metricas():                  
    metricas = leer_metricas()                             
    assert set(metricas)== {"cpu", "memoria", "disco"}
                               
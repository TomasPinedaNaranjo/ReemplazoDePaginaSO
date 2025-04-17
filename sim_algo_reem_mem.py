#!/usr/bin/env python

marcos_libres = [0x0,0x1,0x2]
reqs = [ 0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A ]
segmentos =[ ('.text', 0x00, 0x1A),
              ('.data', 0x40, 0x28),
              ('.heap', 0x80, 0x1F),
              ('.stack', 0xC0, 0x22),
             ]

def procesar(segmentos, reqs, marcos_libres):
    resultados = []
    tabla_paginas = {}
    cola_fifo = []  

    for tiempo, req in enumerate(reqs):

        
        direccion_valida = False
        for nombre, base, limite in segmentos:
            if base <= req <= base + limite - 1:
                direccion_valida = True
                break

        if not direccion_valida:
            resultados.append((req, 0x1FF, "Segmentation Fault"))
            continue

        pagina = req >> 4
        offset = req & 0xF

        
        if pagina in tabla_paginas:
            marco = tabla_paginas[pagina]
            direccion_fisica = (marco << 4) | offset
            resultados.append((req, direccion_fisica, "Marco ya estaba asignado"))
            continue

        
        if marcos_libres:
            marco = marcos_libres.pop(0)
            tabla_paginas[pagina] = marco
            cola_fifo.append(pagina)
            direccion_fisica = (marco << 4) | offset
            resultados.append((req, direccion_fisica, "Marco libre asignado"))
            continue

        
        pagina_vieja = cola_fifo.pop(0)
        marco = tabla_paginas[pagina_vieja]
        del tabla_paginas[pagina_vieja]

        tabla_paginas[pagina] = marco
        cola_fifo.append(pagina)
        direccion_fisica = (marco << 4) | offset
        resultados.append((req, direccion_fisica, "Marco asignado"))

    return resultados

    
def print_results(results):
    for result in results:
        print(f"Req: {result[0]:#0{4}x} Direccion Fisica: {result[1]:#0{4}x} Acción: {result[2]}")

if __name__ == '__main__':
    results = procesar(segmentos, reqs, marcos_libres)
    print_results(results)


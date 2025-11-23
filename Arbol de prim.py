import heapq
import networkx as nx
import matplotlib.pyplot as plt

def algoritmo_prim_visual(grafo_dict, inicio):
    # --- 1. INICIALIZACIÓN ---
    mst_aristas = []     # Aquí guardaremos las conexiones ganadoras
    visitados = set()    # Nodos que ya conectamos a la red
    costo_total = 0
    
    # Cola de prioridad: (peso, nodo_origen, nodo_destino)
    # Empezamos simulando que llegamos al nodo inicio con costo 0
    min_heap = [(0, inicio, inicio)]
    
    print(f"\n--- ⚡ INICIANDO ALGORITMO DE PRIM (Infraestructura) ---")
    
    # --- 2. LÓGICA DEL ALGORITMO ---
    while min_heap:
        peso, u, v = heapq.heappop(min_heap)
        
        # Si el nodo destino 'v' ya está conectado, lo ignoramos para no crear ciclos
        if v in visitados:
            continue
            
        # ¡Conectamos el nodo!
        visitados.add(v)
        costo_total += peso
        
        # Si no es el nodo inicial, guardamos la arista para graficarla
        if u != v:
            mst_aristas.append((u, v))
            print(f"🔧 Conectando: {u} <--> {v} | Costo de cable: ${peso}")
        else:
            print(f"📍 Comenzando instalación desde: {v}")

        # Explorar vecinos del nodo recién conectado
        for vecino, costo in grafo_dict[v].items():
            if vecino not in visitados:
                heapq.heappush(min_heap, (costo, v, vecino))
                
    return mst_aristas, costo_total

def graficar_prim(grafo_dict, aristas_mst, costo_total):
    G = nx.Graph()
    
    # Añadir todas las conexiones posibles (Contexto)
    for u, vecinos in grafo_dict.items():
        for v, peso in vecinos.items():
            G.add_edge(u, v, weight=peso)
            
    pos = nx.spring_layout(G, seed=10) # Seed fija para que no se mueva
    
    plt.figure(figsize=(10, 7))
    
    # 1. Dibujar TODO el grafo en gris (Opciones descartadas)
    nx.draw_networkx_nodes(G, pos, node_size=1200, node_color='#D3D3D3')
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.3, edge_color='gray', style='dashed')
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold")
    
    # Etiquetas de pesos (costos)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    # 2. RESALTAR EL ÁRBOL DE EXPANSIÓN MÍNIMA (MST)
    # Dibujar nodos conectados en azul
    nodos_conectados = set()
    for u, v in aristas_mst:
        nodos_conectados.add(u)
        nodos_conectados.add(v)
        
    nx.draw_networkx_nodes(G, pos, nodelist=list(nodos_conectados), node_size=1200, node_color='#87CEEB') # Azul cielo
    
    # Dibujar las aristas del MST más gruesas y sólidas
    nx.draw_networkx_edges(G, pos, edgelist=aristas_mst, width=4, edge_color='#1E90FF') # Azul fuerte
    
    plt.title(f"Árbol de Expansión Mínima (Prim)\nCosto Total de Infraestructura: ${costo_total}", fontsize=14)
    plt.axis('off')
    
    plt.savefig("resultado_prim.png")
    print(f"\n💾 Gráfica guardada como 'resultado_prim.png'")
    plt.show()

# --- DATOS DE EJEMPLO: COSTOS DE CABLEADO ENTRE SERVIDORES ---
topologia = {
    'Servidor_A': {'Servidor_B': 4, 'Servidor_H': 8},
    'Servidor_B': {'Servidor_A': 4, 'Servidor_C': 8, 'Servidor_H': 11},
    'Servidor_C': {'Servidor_B': 8, 'Servidor_D': 7, 'Servidor_F': 4, 'Servidor_I': 2},
    'Servidor_D': {'Servidor_C': 7, 'Servidor_E': 9, 'Servidor_F': 14},
    'Servidor_E': {'Servidor_D': 9, 'Servidor_F': 10},
    'Servidor_F': {'Servidor_C': 4, 'Servidor_D': 14, 'Servidor_E': 10, 'Servidor_G': 2},
    'Servidor_G': {'Servidor_F': 2, 'Servidor_H': 1, 'Servidor_I': 6},
    'Servidor_H': {'Servidor_A': 8, 'Servidor_B': 11, 'Servidor_G': 1, 'Servidor_I': 7},
    'Servidor_I': {'Servidor_C': 2, 'Servidor_G': 6, 'Servidor_H': 7}
}

# --- EJECUCIÓN ---
mst, costo = algoritmo_prim_visual(topologia, 'Servidor_A')

print(f"\nRESULTADO:")
print(f"Conexiones óptimas realizadas: {len(mst)}")
print(f"Presupuesto Total Utilizado: ${costo}")

graficar_prim(topologia, mst, costo)
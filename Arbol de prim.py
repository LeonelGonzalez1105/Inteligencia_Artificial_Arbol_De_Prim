import heapq
import networkx as nx
import matplotlib.pyplot as plt

# --- DATOS: TOPOLOGÍA DE RED (Global para usar en ambas gráficas) ---
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

def graficar_estado_inicial(grafo_dict):
    print("\n📊 Generando gráfica del estado inicial (ANTES)...")
    print("⚠️ IMPORTANTE: Cierra la ventana de la gráfica para continuar con el algoritmo.")
    
    G = nx.Graph()
    for u, vecinos in grafo_dict.items():
        for v, peso in vecinos.items():
            G.add_edge(u, v, weight=peso)
            
    pos = nx.spring_layout(G, seed=10)
    
    plt.figure(figsize=(10, 7))
    
    # Dibujar todo en gris para mostrar el problema a resolver
    nx.draw_networkx_nodes(G, pos, node_size=1200, node_color='#D3D3D3')
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.5, edge_color='black', style='dashed')
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold")
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title("Estado Inicial: Todas las conexiones posibles (Costo desconocido)", fontsize=14)
    plt.axis('off')
    plt.show() # <--- EL PROGRAMA SE PAUSA AQUÍ HASTA QUE CIERRES LA VENTANA

def algoritmo_prim_logica(grafo_dict, inicio):
    mst_aristas = []
    visitados = set()
    costo_total = 0
    min_heap = [(0, inicio, inicio)]
    
    print(f"\n--- ⚡ EJECUTANDO ALGORITMO DE PRIM ---")
    
    while min_heap:
        peso, u, v = heapq.heappop(min_heap)
        
        if v in visitados:
            continue
            
        visitados.add(v)
        costo_total += peso
        
        if u != v:
            mst_aristas.append((u, v))
            print(f"🔧 Conectando: {u} <--> {v} | Costo: ${peso}")

        for vecino, costo in grafo_dict[v].items():
            if vecino not in visitados:
                heapq.heappush(min_heap, (costo, v, vecino))
                
    return mst_aristas, costo_total

def graficar_resultado_final(grafo_dict, aristas_mst, costo_total):
    print("\n📊 Generando gráfica del resultado (DESPUÉS)...")
    G = nx.Graph()
    for u, vecinos in grafo_dict.items():
        for v, peso in vecinos.items():
            G.add_edge(u, v, weight=peso)
            
    pos = nx.spring_layout(G, seed=10) # Misma seed = mismas posiciones
    
    plt.figure(figsize=(10, 7))
    
    # Fondo (Contexto)
    nx.draw_networkx_nodes(G, pos, node_size=1200, node_color='#D3D3D3')
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.2, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold")
    
    # Solución (MST)
    nodos_conectados = set()
    for u, v in aristas_mst:
        nodos_conectados.add(u)
        nodos_conectados.add(v)
        
    nx.draw_networkx_nodes(G, pos, nodelist=list(nodos_conectados), node_size=1200, node_color='#87CEEB')
    nx.draw_networkx_edges(G, pos, edgelist=aristas_mst, width=4, edge_color='#1E90FF')
    
    # Etiquetas de peso solo en la solución para limpiar visualmente
    edge_labels = nx.get_edge_attributes(G, 'weight')
    # Filtramos para mostrar solo etiquetas de la ruta ganadora (opcional, pero se ve mejor)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title(f"Solución Óptima (Prim)\nCosto Mínimo Total: ${costo_total}", fontsize=14)
    plt.axis('off')
    plt.savefig("resultado_prim.png")
    plt.show()

# --- BLOQUE PRINCIPAL DE EJECUCIÓN ---
if __name__ == "__main__":
    # 1. Mostrar el problema
    graficar_estado_inicial(topologia)
    
    # 2. Calcular la solución (Solo corre cuando cierras la ventana anterior)
    mst, costo = algoritmo_prim_logica(topologia, 'Servidor_A')
    
    print(f"\n✅ RESULTADO FINAL: Presupuesto Total ${costo}")
    
    # 3. Mostrar la solución
    graficar_resultado_final(topologia, mst, costo)
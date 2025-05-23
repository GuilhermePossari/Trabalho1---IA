import networkx as nx
import matplotlib.pyplot as plt
import json
from collections import deque

input_path_file = "grafo.json"

with open(input_path_file, "r") as input_file:
    graph_from_json = json.load(input_file)

graph = nx.Graph(graph_from_json)

# --- Início do código BFS para encontrar caminho ---
def bfs_path(graph, start_node, end_node):
    """
    Realiza uma busca em largura (BFS) para encontrar o caminho mais curto
    entre start_node e end_node.

    Args:
        graph: O grafo (objeto networkx.Graph).
        start_node: O nó inicial para a busca.
        end_node: O nó de destino da busca.

    Returns:
        Uma lista contendo o caminho do start_node ao end_node,
        ou None se não houver caminho.
    """
    if start_node not in graph:
        print(f"Erro: O nó inicial '{start_node}' não existe no grafo.")
        return None
    if end_node not in graph:
        print(f"Erro: O nó de destino '{end_node}' não existe no grafo.")
        return None
    if start_node == end_node:
        return [start_node]

    visited = {start_node}  # Usar um conjunto para nós visitados
    # A fila agora armazena tuplas (nó, caminho_até_o_nó)
    queue = deque([(start_node, [start_node])])

    while queue:
        current_node, path = queue.popleft()

        for neighbor in graph.neighbors(current_node):
            if neighbor == end_node:
                return path + [neighbor]  # Caminho encontrado
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None  # Caminho não encontrado
# --- Fim do código BFS para encontrar caminho ---

# Casos de teste
test_cases = [
    ("Londrina", "Maringá"),
    ("Primeiro de Maio", "Apucarana"),
    ("Londrina", "Paranavaí"),
    ("Londrina", "Foz do Iguaçu"),
    ("Primeiro de Maio", "Curitiba")
]

print("--- Testando buscas BFS para caminhos específicos ---")
for i, (inicio, fim) in enumerate(test_cases):
    print(f"\nTeste {i+1}: Buscando caminho de '{inicio}' para '{fim}'")
    caminho = bfs_path(graph, inicio, fim)
    if caminho:
        print(f"Caminho encontrado: {' -> '.join(caminho)}")
        print(f"Número de 'saltos' (arestas): {len(caminho) - 1}")
    else:
        print(f"Não foi encontrado caminho entre '{inicio}' e '{fim}'.")

# --- Opcional: Plotar o grafo com um caminho específico destacado ---
def plot_graph_with_path(graph_obj, path_to_highlight, start_node_path, end_node_path):
    if not path_to_highlight:
        print(f"Não há caminho para destacar entre {start_node_path} e {end_node_path}.")
        return

    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(graph_obj, k=0.15, iterations=20, seed=42) # k ajusta o espaçamento

    # Desenha todos os nós e arestas
    nx.draw_networkx_nodes(graph_obj, pos, node_size=200, node_color='lightblue', alpha=0.9)
    nx.draw_networkx_edges(graph_obj, pos, width=1, alpha=0.3, edge_color='gray')
    nx.draw_networkx_labels(graph_obj, pos, font_size=7)

    # Destaca os nós do caminho
    nx.draw_networkx_nodes(graph_obj, pos, nodelist=path_to_highlight, node_color='red', node_size=300)

    # Destaca as arestas do caminho
    path_edges = list(zip(path_to_highlight[:-1], path_to_highlight[1:]))
    nx.draw_networkx_edges(graph_obj, pos, edgelist=path_edges, width=2, alpha=0.8, edge_color='red')

    # Destaca nós de início e fim de forma diferente
    nx.draw_networkx_nodes(graph_obj, pos, nodelist=[start_node_path], node_color='green', node_size=400, label="Início")
    nx.draw_networkx_nodes(graph_obj, pos, nodelist=[end_node_path], node_color='purple', node_size=400, label="Fim")


    plt.title(f"Caminho BFS de {start_node_path} para {end_node_path}")
    plt.legend()
    plt.axis('off')
    plt.show()

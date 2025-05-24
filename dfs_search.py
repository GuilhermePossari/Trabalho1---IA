import json
import copy # Importe a biblioteca copy para fazer uma cópia profunda
import matplotlib.pyplot as plt # Para plotagem
import networkx as nx # Para manipulação e plotagem de grafos

try:
    with open("grafo.json", "r") as f:
        graph_from_json = json.load(f) # Renomeado para clareza
except FileNotFoundError:
    print("Erro: O arquivo 'grafo.json' não foi encontrado.")
    exit(1)
except json.JSONDecodeError:
    print("Erro: O arquivo 'grafo.json' está mal formatado.")
    exit(1)

# --- Início da Modificação: Criar uma representação não direcionada do grafo ---
# Este 'graph_dict' será usado pela função DFS.
graph_dict = copy.deepcopy(graph_from_json)

for node, neighbors in graph_from_json.items():
    for neighbor, distance in neighbors.items():
        if neighbor not in graph_dict:
            graph_dict[neighbor] = {}
        graph_dict[neighbor][node] = distance
# --- Fim da Modificação ---

# --- Início da função de plotagem (adaptada do seu bfs_search.py) ---
def plot_graph_with_path(graph_to_plot, path_to_highlight, start_node_path, end_node_path, filename_prefix, algorithm_name):
    """
    Plota o grafo e destaca um caminho específico.

    Args:
        graph_to_plot: O grafo (objeto networkx.Graph).
        path_to_highlight: Lista de nós no caminho a ser destacado.
        start_node_path: Nó inicial do caminho.
        end_node_path: Nó final do caminho.
        filename_prefix: Prefixo para o nome do arquivo de imagem.
        algorithm_name: Nome do algoritmo (ex: "DFS") para o título.
    """
    if not path_to_highlight:
        print(f"Não há caminho para destacar entre {start_node_path} e {end_node_path}.")
        return

    plt.figure(figsize=(14, 12)) # Aumentado para melhor visualização de grafos maiores
    # Usar um layout que tente espalhar melhor os nós
    try:
        pos = nx.kamada_kawai_layout(graph_to_plot)
    except nx.NetworkXError: # Fallback para spring_layout se kamada_kawai falhar (ex: grafo desconexo)
        print("Alerta: kamada_kawai_layout falhou, usando spring_layout como fallback.")
        pos = nx.spring_layout(graph_to_plot, k=0.2, iterations=30, seed=42)


    # Desenha todos os nós e arestas
    nx.draw_networkx_nodes(graph_to_plot, pos, node_size=250, node_color='lightblue', alpha=0.9)
    nx.draw_networkx_edges(graph_to_plot, pos, width=1, alpha=0.3, edge_color='gray')
    nx.draw_networkx_labels(graph_to_plot, pos, font_size=8) # Ajuste o tamanho da fonte se necessário

    # Destaca os nós do caminho
    nx.draw_networkx_nodes(graph_to_plot, pos, nodelist=path_to_highlight, node_color='tomato', node_size=350)

    # Destaca as arestas do caminho
    path_edges = list(zip(path_to_highlight[:-1], path_to_highlight[1:]))
    nx.draw_networkx_edges(graph_to_plot, pos, edgelist=path_edges, width=2.5, alpha=0.8, edge_color='orangered')

    # Destaca nós de início e fim de forma diferente
    nx.draw_networkx_nodes(graph_to_plot, pos, nodelist=[start_node_path], node_color='lime', node_size=450, label="Início")
    nx.draw_networkx_nodes(graph_to_plot, pos, nodelist=[end_node_path], node_color='darkviolet', node_size=450, label="Fim")

    plt.title(f"Caminho {algorithm_name} de {start_node_path} para {end_node_path} (Saltos: {len(path_to_highlight)-1})", fontsize=14)
    plt.legend(scatterpoints=1, loc='upper right')
    plt.axis('off')

    filename = f"{filename_prefix}{start_node_path}_para{end_node_path}.png".replace(" ", "_").lower()
    plt.savefig(filename, dpi=150) # Aumentar DPI para melhor qualidade
    print(f"Imagem salva em: {filename}")
    plt.close()
# --- Fim da função de plotagem ---

def dfs(current_graph, start, target):
    if start == target:
        return [start]
    visited = set()
    stack = [start]
    visited.add(start)
    predecessors = {start: None}

    while stack:
        current_node_dfs = stack.pop()
        if current_node_dfs == target:
            path = []
            temp_current = current_node_dfs
            while temp_current is not None:
                path.append(temp_current)
                temp_current = predecessors[temp_current]
            return path[::-1]

        if current_node_dfs in current_graph: # Garante que o nó exista antes de acessar vizinhos
            # Iterar em ordem reversa pode, às vezes, dar caminhos mais "intuitivos" para DFS em grafos desenhados
            # mas a ordem padrão (da forma como o dicionário retorna) também é válida.
            # neighbors_to_explore = list(current_graph[current_node_dfs].keys())
            # for neighbor_dfs in reversed(neighbors_to_explore):
            for neighbor_dfs in current_graph[current_node_dfs]:
                if neighbor_dfs not in visited:
                    stack.append(neighbor_dfs)
                    visited.add(neighbor_dfs)
                    predecessors[neighbor_dfs] = current_node_dfs
    return None

casos_teste = [
    ("Londrina", "Maringá"),
    ("Primeiro de Maio", "Apucarana"),
    ("Londrina", "Paranavaí"),
    ("Londrina", "Foz do Iguaçu"),
    ("Primeiro de Maio", "Curitiba")
]

# Criar o objeto de grafo NetworkX uma vez para plotagem
# Ele será não direcionado por padrão se graph_dict for simétrico,
# ou podemos forçá-lo a ser não direcionado como no seu BFS.
# Usando graph_dict que já foi tornado simétrico (não direcionado na prática para DFS).
nx_graph_for_plotting = nx.Graph(graph_dict)

# Executa os casos de teste
for i, (origem, destino) in enumerate(casos_teste):
    print(f"\n--- Teste DFS {i+1}: Buscando caminho de '{origem}' para '{destino}' ---")
    if origem not in graph_dict: # Verifica no dicionário usado pelo DFS
        print(f"Erro: A origem '{origem}' não está no grafo.")
        continue
    if destino not in graph_dict: # Verifica no dicionário usado pelo DFS
        print(f"Erro: O destino '{destino}' não está no grafo.")
        continue

    route = dfs(graph_dict, origem, destino)

    if route:
        print(f"Caminho DFS encontrado: {' -> '.join(route)}")
        print(f"Número de 'saltos' (arestas): {len(route) - 1}")
        # Chamar a função de plotagem
        plot_graph_with_path(nx_graph_for_plotting, route, origem, destino, f"grafo_dfs_{i+1}", "DFS")
    else:
        print(f"Não foi encontrado caminho DFS entre '{origem}' e '{fim}'.")
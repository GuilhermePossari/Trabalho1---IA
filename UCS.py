import json
import heapq

with open("grafo.json", "r", encoding="utf-8") as file:
    grafo = json.load(file)

def busca_custo_uniforme(grafo, inicio, objetivo):
    fila = []
    heapq.heappush(fila, (0, inicio, [inicio]))  # (custo, cidade atual, caminho)

    visitados = set()

    while fila:
        custo, atual, caminho = heapq.heappop(fila)

        if atual == objetivo:
            return caminho, custo

        if atual in visitados:
            continue
        visitados.add(atual)

        for vizinho, custo_vizinho in grafo.get(atual, {}).items():
            if vizinho not in visitados:
                heapq.heappush(fila, (custo + custo_vizinho, vizinho, caminho + [vizinho]))

    return None, float("inf")

casos_teste = [
    ("Londrina", "Maringá"),
    ("Primeiro de Maio", "Apucarana"),
    ("Londrina", "Paranavaí"),
    ("Londrina", "Foz do Iguaçu"),
    ("Primeiro de Maio", "Curitiba")
]

if __name__ == "__main__":
    for origem, destino in casos_teste:
        caminho, custo = busca_custo_uniforme(grafo, origem, destino)
        print(f"\nDe {origem} para {destino}:")
        if caminho:
            print(" -> ".join(caminho))
            print(f"Custo total: {custo:.2f}")
        else:
            print("Caminho não encontrado.")


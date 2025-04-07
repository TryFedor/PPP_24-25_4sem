from fastapi import APIRouter, HTTPException
from itertools import permutations
from app.schemas.tsp import Graph, PathResult

router = APIRouter(tags=["TSP"])


@router.post("/shortest-path/", response_model=PathResult)
def find_shortest_path(graph: Graph):
    # Преобразуем узлы в индексы
    node_to_index = {node: idx for idx, node in enumerate(graph.nodes)}
    n = len(graph.nodes)

    # Создаём матрицу расстояний (по умолчанию ∞)
    distance_matrix = [[float('inf')] * n for _ in range(n)]

    # Заполняем матрицу для всех рёбер (граф НЕориентированный)
    for a, b in graph.edges:
        i = node_to_index[a]
        j = node_to_index[b]
        distance_matrix[i][j] = 1  # прямое направление
        distance_matrix[j][i] = 1  # обратное направление

    # Поиск кратчайшего гамильтонова цикла
    min_distance = float('inf')
    best_route = None

    for perm in permutations(range(n)):
        current_distance = 0
        valid = True

        for i in range(len(perm)):
            u = perm[i]
            v = perm[(i + 1) % len(perm)]  # замыкаем цикл

            if distance_matrix[u][v] == float('inf'):
                valid = False
                break
            current_distance += distance_matrix[u][v]

        if valid and current_distance < min_distance:
            min_distance = current_distance
            best_route = perm

    if best_route is None:
        raise HTTPException(
            status_code=400,
            detail="No valid Hamiltonian cycle found"
        )

    # Преобразуем индексы обратно в исходные узлы
    original_nodes = [graph.nodes[i] for i in best_route]

    return PathResult(
        path=original_nodes,
        total_distance=min_distance
    )

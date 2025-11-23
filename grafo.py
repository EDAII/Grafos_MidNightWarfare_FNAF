import pygame
import random
from config import POSICOES, COR_LINHA, COR_SALA, COR_OFFICE, COR_PORTA_FECHADA, COR_PORTA_ABERTA

# definicao das adjacencias entre as salas
GRAFO = {
    "Palco": ["Jantar"],
    "Jantar": ["Palco", "Backstage", "West Hall", "East Hall", "Cozinha", "Banheiros"],
    "Backstage": ["Jantar"],
    "Pirate Cove": ["West Hall"],
    "Banheiros": ["Jantar", "East Hall"],
    "Cozinha": ["Jantar", "East Hall"],
    "West Hall": ["Jantar", "Pirate Cove", "Despensa", "West Hall Corner"],
    "Despensa": ["West Hall"],
    "West Hall Corner": ["West Hall", "Office"],
    "East Hall": ["Jantar", "Banheiros", "Cozinha", "East Hall Corner"],
    "East Hall Corner": ["East Hall", "Office"],
    "Office": []
}

# algoritmo de busca em largura para encontrar o caminho mais curto
def obter_proximo_passo_bfs(inicio, objetivo):
    if inicio == objetivo: return inicio
    fila = [[inicio]]
    visitados = {inicio}
    while fila:
        caminho = fila.pop(0)
        node = caminho[-1]
        if node == objetivo:
            return caminho[1] if len(caminho) > 1 else objetivo
        for vizinho in GRAFO.get(node, []):
            if vizinho not in visitados:
                visitados.add(vizinho)
                novo_caminho = list(caminho)
                novo_caminho.append(vizinho)
                fila.append(novo_caminho)
    return inicio

# algoritmo de busca em profundidade com memoria e filtro de salas validas
def obter_proximo_passo_dfs(inicio, memoria_visitados, vizinhos_validos=None):
    todos_vizinhos = GRAFO.get(inicio, [])
    
    # utiliza apenas os vizinhos permitidos se fornecidos
    if vizinhos_validos:
        vizinhos = [v for v in todos_vizinhos if v in vizinhos_validos]
    else:
        vizinhos = todos_vizinhos
        
    # prioriza salas nao visitadas recentemente
    candidatos = [v for v in vizinhos if v not in memoria_visitados]
    if candidatos:
        return random.choice(candidatos)
    else:
        return random.choice(vizinhos) if vizinhos else inicio

# renderizacao do mapa tatico na tela principal quando a camera esta desligada
def desenhar_mapa(tela, portas):
    w, h = tela.get_size() 
    
    def to_pixel(pos_ratio):
        return (int(pos_ratio[0] * w), int(pos_ratio[1] * h))

    # desenha as conexoes (arestas)
    for node, vizinhos in GRAFO.items():
        p1 = to_pixel(POSICOES[node])
        for vizinho in vizinhos:
            if vizinho in POSICOES:
                p2 = to_pixel(POSICOES[vizinho])
                cor = COR_LINHA
                largura = 2
                # destaca conexoes com o escritorio baseadas no estado das portas
                if vizinho == "Office":
                    largura = 6
                    if node == "West Hall Corner":
                        cor = COR_PORTA_FECHADA if portas[0] else COR_PORTA_ABERTA
                    elif node == "East Hall Corner":
                        cor = COR_PORTA_FECHADA if portas[1] else COR_PORTA_ABERTA
                pygame.draw.line(tela, cor, p1, p2, largura)

    # desenha os nos (salas)
    for nome, pos_ratio in POSICOES.items():
        pos_pixel = to_pixel(pos_ratio)
        cor = COR_OFFICE if nome == "Office" else COR_SALA
        
        raio = max(6, int(h * 0.015))
        pygame.draw.circle(tela, cor, pos_pixel, raio)
        pygame.draw.circle(tela, cor, pos_pixel, int(raio * 1.5), 1) 
        
        font = pygame.font.SysFont("consolas", 12)
        text = font.render(nome, True, (100, 150, 150))
        tela.blit(text, (pos_pixel[0] - text.get_width()//2, pos_pixel[1] + raio + 5))
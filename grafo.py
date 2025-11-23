import pygame
import random
from config import POSICOES, COR_LINHA, COR_SALA, COR_OFFICE, COR_PORTA_FECHADA, COR_PORTA_ABERTA

GRAFO = {
    "Palco": ["Jantar"],
    "Jantar": ["Palco", "Backstage", "Pirate Cove", "West Hall", "East Hall", "Cozinha", "Banheiros"],
    "Backstage": ["Jantar"],
    "Pirate Cove": ["Jantar", "West Hall"],
    "Banheiros": ["Jantar"],
    "Cozinha": ["Jantar", "East Hall"],
    "West Hall": ["Jantar", "Despensa", "West Hall Corner"],
    "Despensa": ["West Hall"],
    "West Hall Corner": ["West Hall", "Office"],
    "East Hall": ["Jantar", "East Hall Corner"],
    "East Hall Corner": ["East Hall", "Office"],
    "Office": []
}

# Algoritmo BFS: 
# garante menor caminho para chegar ao escritório
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

# Algoritmo DFS: 
# prioriza nós não visitados recentemente para simular animatronic vagando pelo mapa
def obter_proximo_passo_dfs(inicio, memoria_visitados):
    vizinhos = GRAFO.get(inicio, [])
    # Tenta ir para um nó ainda não explorado na memória recente
    candidatos = [v for v in vizinhos if v not in memoria_visitados]
    
    if candidatos:
        return random.choice(candidatos)
    else:
        # Backtracking implícito: se todos vizinhos foram visitados, retorna a um aleatório
        return random.choice(vizinhos) if vizinhos else inicio

def desenhar_mapa(tela, portas):
    for node, vizinhos in GRAFO.items():
        p1 = POSICOES[node]
        for vizinho in vizinhos:
            if vizinho in POSICOES:
                p2 = POSICOES[vizinho]
                cor = COR_LINHA
                largura = 2
                if vizinho == "Office":
                    largura = 6
                    idx = 0 if node == "West Hall Corner" else 1
                    if node == "West Hall Corner":
                        cor = COR_PORTA_FECHADA if portas[0] else COR_PORTA_ABERTA
                    elif node == "East Hall Corner":
                        cor = COR_PORTA_FECHADA if portas[1] else COR_PORTA_ABERTA
                pygame.draw.line(tela, cor, p1, p2, largura)

    for nome, pos in POSICOES.items():
        cor = COR_OFFICE if nome == "Office" else COR_SALA
        pygame.draw.circle(tela, cor, pos, 8)
        pygame.draw.circle(tela, cor, pos, 12, 1) 
        font = pygame.font.SysFont("consolas", 12)
        text = font.render(nome, True, (100, 150, 150))
        tela.blit(text, (pos[0] - text.get_width()//2, pos[1] + 15))
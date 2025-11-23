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

def obter_proximo_passo_dfs(inicio, memoria_visitados):
    vizinhos = GRAFO.get(inicio, [])
    candidatos = [v for v in vizinhos if v not in memoria_visitados]
    if candidatos:
        return random.choice(candidatos)
    else:
        return random.choice(vizinhos) if vizinhos else inicio

def desenhar_mapa(tela, portas):
    w, h = tela.get_size() # pega tamanho atual da janela
    
    # Função que converte ratio (0.0-1.0) em pixel
    def to_pixel(pos_ratio):
        return (int(pos_ratio[0] * w), int(pos_ratio[1] * h))

    for node, vizinhos in GRAFO.items():
        p1 = to_pixel(POSICOES[node])
        for vizinho in vizinhos:
            if vizinho in POSICOES:
                p2 = to_pixel(POSICOES[vizinho])
                cor = COR_LINHA
                largura = 2
                if vizinho == "Office":
                    largura = 6
                    if node == "West Hall Corner":
                        cor = COR_PORTA_FECHADA if portas[0] else COR_PORTA_ABERTA
                    elif node == "East Hall Corner":
                        cor = COR_PORTA_FECHADA if portas[1] else COR_PORTA_ABERTA
                pygame.draw.line(tela, cor, p1, p2, largura)

    for nome, pos_ratio in POSICOES.items():
        pos_pixel = to_pixel(pos_ratio)
        cor = COR_OFFICE if nome == "Office" else COR_SALA
        
        # tamanho dos nós escala levemente
        raio = max(6, int(h * 0.015))
        pygame.draw.circle(tela, cor, pos_pixel, raio)
        pygame.draw.circle(tela, cor, pos_pixel, int(raio * 1.5), 1) 
        
        font = pygame.font.SysFont("consolas", 12)
        text = font.render(nome, True, (100, 150, 150))
        tela.blit(text, (pos_pixel[0] - text.get_width()//2, pos_pixel[1] + raio + 5))
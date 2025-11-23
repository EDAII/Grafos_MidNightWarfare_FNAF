import pygame
from config import POSICOES, COR_LINHA, COR_SALA, COR_OFFICE, COR_PORTA_FECHADA, COR_PORTA_ABERTA


# Estrutura do grafo (lista de adjacência)
GRAFO = {
    "Palco": ["Jantar", "Backstage"],
    "Jantar": ["Palco", "Backstage", "Pirate Cove", "West Hall", "East Hall", "Cozinha", "Banheiros"],
    "Backstage": ["Jantar"],
    "Pirate Cove": ["Jantar", "West Hall"], # atalho do Foxy
    "Banheiros": ["Jantar"],
    "Cozinha": ["Jantar", "East Hall"],
    "West Hall": ["Jantar", "Despensa", "West Hall Corner"],
    "Despensa": ["West Hall"],
    "West Hall Corner": ["West Hall", "Office"], # porta Esquerda
    "East Hall": ["Jantar", "East Hall Corner"],
    "East Hall Corner": ["East Hall", "Office"], # porta Direita
    "Office": [] # Jogador
} 

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
                    if node == "West Hall Corner":
                        cor = COR_PORTA_FECHADA if portas[0] else COR_PORTA_ABERTA
                    elif node == "East Hall Corner":
                        cor = COR_PORTA_FECHADA if portas[1] else COR_PORTA_ABERTA
                pygame.draw.line(tela, cor, p1, p2, largura)

    # desenha as salas (nós)
    for nome, pos in POSICOES.items():
        cor = COR_OFFICE if nome == "Office" else COR_SALA
        pygame.draw.circle(tela, cor, pos, 8)
        pygame.draw.circle(tela, cor, pos, 12, 1) 
        font = pygame.font.SysFont("consolas", 12)
        text = font.render(nome, True, (100, 150, 150))
        tela.blit(text, (pos[0] - text.get_width()//2, pos[1] + 15))

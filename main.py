import pygame
import random
import time
import math

# Configurações Visuais 
LARGURA, ALTURA = 1024, 768
COR_FUNDO = (10, 15, 20)  # azul muito escuro
COR_LINHA = (40, 60, 80)  # azul escuro para conexões inativas
COR_SALA = (0, 255, 200)  # ciano neon para salas
COR_PORTA_FECHADA = (255, 50, 50) # vermelho
COR_PORTA_ABERTA = (50, 255, 50)  # verde
COR_OFFICE = (200, 200, 200)

# Estrutura do grafo
# implementação da lista de adjacência 
# usa um dicionário onde:
#   Chave = Nó (u)
#   Valor = Adj[u] 
# Essa estrutura é escolhida pois o grafo é esparso (m << n^2), economizando memória
# comparado a uma Matriz de Adjacência
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

# Posições na tela 
POSICOES = {
    "Palco": (512, 150),
    "Jantar": (512, 300),
    "Backstage": (350, 200),
    "Pirate Cove": (250, 350),
    "Banheiros": (750, 250),
    "Cozinha": (750, 400),
    "West Hall": (350, 450),
    "Despensa": (200, 450),
    "West Hall Corner": (350, 600),
    "East Hall": (674, 450),
    "East Hall Corner": (674, 600),
    "Office": (512, 700)
}

class Animatronic:
    def __init__(self, nome, cor, start_node, agressividade):
        self.nome = nome
        self.cor = cor
        self.node_atual = start_node
        self.agressividade = agressividade # tempo entre movimentos
        self.ultimo_movimento = time.time()
        self.pos_x, self.pos_y = POSICOES[start_node]
        self.target_x, self.target_y = POSICOES[start_node]

    def atualizar(self, portas_fechadas):
        # interpolação visual
        self.pos_x += (self.target_x - self.pos_x) * 0.1
        self.pos_y += (self.target_y - self.pos_y) * 0.1

        # Lógica de IA baseada em travessia de grafo (mais especificamente uma bfs)
        if time.time() - self.ultimo_movimento > self.agressividade:
            vizinhos = GRAFO[self.node_atual]
            
            # Acessa Adj[u] (lista de adjacência) para descobrir para onde é possível mover
            if vizinhos:
                # verificação de Adjacência Direta
                # o animatronic verifica se o nó destino é adjacente ao atual.
                if "Office" in vizinhos:
                    # Checar portas
                    lado = "Esq" if self.node_atual == "West Hall Corner" else "Dir"
                    if (lado == "Esq" and portas_fechadas[0]) or (lado == "Dir" and portas_fechadas[1]):
                        # Porta fechada, bate e volta ou fica parado
                        print(f"{self.nome} bloqueado pela porta!")
                        self.ultimo_movimento = time.time()
                        return
                    else:
                        proximo = "Office" #marca o fim do caminho
                else:
                    # o animatronic escolhe uma aresta (u, v) aleatória em E para atravessar
                    proximo = random.choice(vizinhos)
                
                self.node_atual = proximo
                self.target_x, self.target_y = POSICOES[proximo]
                self.ultimo_movimento = time.time()

    def desenhar(self, superficie):
        # efeitos visuais
        s = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.cor, 50), (30, 30), 25) 
        pygame.draw.circle(s, (*self.cor, 150), (30, 30), 15) 
        superficie.blit(s, (self.pos_x - 30, self.pos_y - 30))

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

        #nomenclatura da sala
        font = pygame.font.SysFont("consolas", 12)
        text = font.render(nome, True, (100, 150, 150))
        tela.blit(text, (pos[0] - text.get_width()//2, pos[1] + 15))

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Jogo")
    clock = pygame.time.Clock()
    
    # Começa o jogo com as portas abertas e energia no 100%
    portas = [False, False] 
    energia = 100.0
    
    # Lista de objetos pra animatronics
    animatronics = [
        Animatronic("Bonnie", (180, 50, 255), "Palco", 3.0),
        Animatronic("Chica", (255, 255, 50), "Palco", 3.5),
        Animatronic("Foxy", (255, 50, 50), "Pirate Cove", 5.0)
    ]

    rodando = True
    game_over = False

    while rodando:
        tela.fill(COR_FUNDO)
        dt = clock.tick(60) / 1000 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_a: # porta Esquerda
                    portas[0] = not portas[0]
                if event.key == pygame.K_d: # porta Direita
                    portas[1] = not portas[1]
                if event.key == pygame.K_r: 
                    pass 

        if not game_over:
            # gerenciamento da energia, onde energia <= 0 resulta em abertura de ambas as portas
            uso = 0.05 + (0.1 if portas[0] else 0) + (0.1 if portas[1] else 0)
            energia -= uso * dt
            if energia <= 0:
                energia = 0
                portas = [False, False] 
            for anim in animatronics:
                anim.atualizar(portas)
                if anim.node_atual == "Office":
                    game_over = True
                    

        desenhar_mapa(tela, portas)
        
        for anim in animatronics:
            anim.desenhar(tela)

        font_hud = pygame.font.SysFont("consolas", 24)
        texto_energia = font_hud.render(f"POWER: {int(energia)}%", True, (255, 255, 255))
        texto_portas = font_hud.render(f"[A] Esq: {'FECHADA' if portas[0] else 'ABERTA'} | [D] Dir: {'FECHADA' if portas[1] else 'ABERTA'}", True, (200, 200, 200))
        
        tela.blit(texto_energia, (20, 700))
        tela.blit(texto_portas, (20, 730))

        if game_over:
            texto_fim = pygame.font.SysFont("consolas", 60).render("GAME OVER", True, (255, 0, 0))
            tela.blit(texto_fim, (LARGURA//2 - texto_fim.get_width()//2, ALTURA//2))

        for i in range(0, ALTURA, 4):
            pygame.draw.line(tela, (0, 0, 0, 50), (0, i), (LARGURA, i))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
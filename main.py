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
        self.start_node = start_node   # nó de spawn / retorno
        self.node_atual = start_node
        self.agressividade = agressividade # tempo entre movimentos em segundos
        self.ultimo_movimento = time.time()
        self.pos_x, self.pos_y = POSICOES[start_node]
        self.target_x, self.target_y = POSICOES[start_node]
        # small timer to make Foxy wait in pirate cove if desired
        self.paciência = 0.0

    def atualizar(self, portas_fechadas):
        # interpolação visual (suaviza movimento)
        self.pos_x += (self.target_x - self.pos_x) * 0.12
        self.pos_y += (self.target_y - self.pos_y) * 0.12

        # controla frequência de movimento baseada em agressividade
        if time.time() - self.ultimo_movimento <= self.agressividade:
            return

        vizinhos = GRAFO.get(self.node_atual, [])
        # se não tiver vizinhos (Office), para
        if not vizinhos:
            self.ultimo_movimento = time.time()
            return

        # Se estiver imediatamente adjacente ao Office, trata portas
        if "Office" in vizinhos:
            lado = "Esq" if self.node_atual == "West Hall Corner" else "Dir" if self.node_atual == "East Hall Corner" else None
            if lado == "Esq":
                if portas_fechadas[0]:
                    # porta fechada -> bate e volta (fica no nó atual por enquanto)
                    self.ultimo_movimento = time.time()
                    return
                else:
                    proximo = "Office"
            elif lado == "Dir":
                if portas_fechadas[1]:
                    self.ultimo_movimento = time.time()
                    return
                else:
                    proximo = "Office"
            else:
                # se "Office" está listado mas não é via corner (caso raro)
                proximo = "Office"
            # aplica movimento final
            self.node_atual = proximo
            self.target_x, self.target_y = POSICOES[proximo]
            self.ultimo_movimento = time.time()
            return

        # Comportamento especial para Foxy e Freddy: tendem a voltar ao spawn
        if self.nome.lower() == "foxy" or self.nome.lower() == "freddy":
            # se já está no spawn, comportamento normal (ronda leve)
            if self.node_atual == self.start_node:
                # pequena chance de sair do spawn (Foxy pode sair da Pirate Cove menos frequentemente)
                if random.random() < 0.5:
                    proximo = random.choice(vizinhos)
                else:
                    # espera um pouco (fica no spawn)
                    self.ultimo_movimento = time.time()
                    return
            else:
                # Escolher vizinho que aproxima mais do spawn (heurística euclidiana)
                spawn_x, spawn_y = POSICOES[self.start_node]
                # filtra vizinhos válidos para pathing mínimo pela posição
                def distancia_para_spawn(v):
                    vx, vy = POSICOES.get(v, (0,0))
                    return math.dist((vx, vy), (spawn_x, spawn_y))
                proximo = min(vizinhos, key=distancia_para_spawn)
        else:
            # Bonnie/Chica: movimento randômico entre vizinhos
            proximo = random.choice(vizinhos)

        # Aplica movimento
        self.node_atual = proximo
        self.target_x, self.target_y = POSICOES[proximo]
        self.ultimo_movimento = time.time()

    def desenhar(self, superficie):
        # efeitos visuais
        s = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.cor, 60), (30, 30), 26) 
        pygame.draw.circle(s, (*self.cor, 180), (30, 30), 14) 
        superficie.blit(s, (self.pos_x - 30, self.pos_y - 30))
        # nome
        font = pygame.font.SysFont("consolas", 12)
        texto = font.render(self.nome, True, (230,230,230))
        superficie.blit(texto, (self.pos_x - texto.get_width()//2, self.pos_y - 40))


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


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("FNAF-like - Demo")
    clock = pygame.time.Clock()
    
    # Começa o jogo com as portas abertas e energia no 100%
    portas = [False, False]  # [esquerda, direita] False = aberta
    energia = 100.0
    
    # Lista de animatronics: adicione Freddy e Foxy (com seus spawns)
    animatronics = [
        Animatronic("Freddy", (255, 200, 0), "Palco", 30.0),
        Animatronic("Bonnie", (180, 50, 255), "Palco", 11.0),
        Animatronic("Chica", (255, 255, 50), "Palco", 12.0),
        Animatronic("Foxy", (255, 50, 50), "Pirate Cove", 15.0),
    ]

    rodando = True
    game_over = False
    energia_acabou = False

    while rodando:
        tela.fill(COR_FUNDO)
        dt = clock.tick(60) / 1.0  # dt em ms; vamos tratar dt como ms para decrementar energia de modo perceptível

        if energia <= 0 and not energia_acabou:
                portas[0] = False
                portas[1] = False
                energia_acabou = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            
            if event.type == pygame.KEYDOWN and not game_over:
                if not energia_acabou:
                    if event.key == pygame.K_a: # porta Esquerda (toggle)
                        portas[0] = not portas[0]
                    if event.key == pygame.K_d: # porta Direita (toggle)
                        portas[1] = not portas[1]
                if event.key == pygame.K_r:
                    # reset básico
                    energia = 100.0
                    portas = [False, False]
                    for anim in animatronics:
                        anim.node_atual = anim.start_node
                        anim.pos_x, anim.pos_y = POSICOES[anim.start_node]
                        anim.target_x, anim.target_y = POSICOES[anim.start_node]
                    game_over = False

        if not game_over:
            # gerenciamento da energia:
            # consumo base por segundo (convertendo dt em segundos)
            segundos = dt / 1000.0
            consumo_base_por_segundo = 0.05  # ajuste para ritmo do jogo
            consumo = consumo_base_por_segundo

            # cada porta fechada adiciona consumo significativo
            if portas[0]:
                consumo += 1
            if portas[1]:
                consumo += 1


            # consumo por segundo -> consumo * segundos
            energia -= consumo * segundos * 10  # multiplicador para ficar perceptível
            energia = max(0.0, energia)

            # atualizar animatronics
            for anim in animatronics:
                anim.atualizar(portas)
                if anim.node_atual == "Office":
                    game_over = True

        desenhar_mapa(tela, portas)
        
        for anim in animatronics:
            anim.desenhar(tela)

        # HUD
        font_hud = pygame.font.SysFont("consolas", 24)
        texto_energia = font_hud.render(f"POWER: {int(energia)}%", True, (255, 255, 255))
        texto_portas = font_hud.render(f"[A] Esq: {'FECHADA' if portas[0] else 'ABERTA'} | [D] Dir: {'FECHADA' if portas[1] else 'ABERTA'}", True, (200, 200, 200))
        
        tela.blit(texto_energia, (20, 700))
        tela.blit(texto_portas, (20, 730))

        if game_over:
            texto_fim = pygame.font.SysFont("consolas", 60).render("GAME OVER", True, (255, 0, 0))
            tela.blit(texto_fim, (LARGURA//2 - texto_fim.get_width()//2, ALTURA//2))

        # grade estética
        for i in range(0, ALTURA, 4):
            pygame.draw.line(tela, (0, 0, 0, 50), (0, i), (LARGURA, i))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

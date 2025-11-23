import random
import time
import pygame
from config import POSICOES, LARGURA, ALTURA
from grafo import GRAFO, obter_proximo_passo_bfs, obter_proximo_passo_dfs

class Animatronic:
    def __init__(self, nome, cor, start_node, agressividade, tipo_ia="random"):
        self.nome = nome
        self.cor = cor
        self.start_node = start_node
        self.node_atual = start_node
        self.agressividade = agressividade
        self.tipo_ia = tipo_ia  # 'bfs', 'dfs', 'foxy'
        self.ultimo_movimento = time.time()
        self.pos_x, self.pos_y = POSICOES[start_node]
        self.target_x, self.target_y = POSICOES[start_node]
        # Memória para DFS (evita ciclos imediatos)
        self.memoria_dfs = []

    def atualizar(self, portas_fechadas):
        # Movimento visual suave
        self.pos_x += (self.target_x - self.pos_x) * 0.12
        self.pos_y += (self.target_y - self.pos_y) * 0.12

        if time.time() - self.ultimo_movimento <= self.agressividade:
            return

        vizinhos = GRAFO[self.node_atual]
        proximo = self.node_atual

        # Lógica de bloqueio de portas (adjacência ao Office)
        if "Office" in vizinhos:
            lado = 0 if self.node_atual == "West Hall Corner" else 1 if self.node_atual == "East Hall Corner" else None
            if lado is not None:
                if portas_fechadas[lado]:
                    # Foxy reseta ao pirate cove bater na porta 
                    if self.tipo_ia == "foxy":
                        self.node_atual = self.start_node
                        self.target_x, self.target_y = POSICOES[self.start_node]
                    self.ultimo_movimento = time.time()
                    return
                else:
                    proximo = "Office"
        
        # Decisão de movimento baseada em algoritmo se não estiver atacando
        if proximo != "Office":
            if self.tipo_ia == "bfs":
                # Freddy: Caminho mais curto determinístico 
                proximo = obter_proximo_passo_bfs(self.node_atual, "Office")
            
            elif self.tipo_ia == "dfs":
                # Bonnie/Chica: Exploração com dfs
                self.memoria_dfs.append(self.node_atual)
                if len(self.memoria_dfs) > 3: self.memoria_dfs.pop(0)
                proximo = obter_proximo_passo_dfs(self.node_atual, self.memoria_dfs)
            
            elif self.tipo_ia == "foxy":
                # Foxy: Avanço linear por estágios através de conectividade direta
                if self.node_atual == "Pirate Cove":
                    if random.random() < 0.4: proximo = "West Hall"
                elif self.node_atual == "West Hall":
                    proximo = "West Hall Corner"
                # Se já estiver no Corner, espera o próximo tick para tentar entrar

        self.node_atual = proximo
        self.target_x, self.target_y = POSICOES[proximo]
        self.ultimo_movimento = time.time()

    def desenhar(self, tela):
        pass 

    def desenhar_camera_view(self, tela):
        tamanho = 120
        cx = LARGURA // 2
        cy = ALTURA // 2
        pygame.draw.circle(tela, self.cor, (cx, cy), tamanho)
        font = pygame.font.SysFont("consolas", 32)
        texto = font.render(self.nome, True, (255,255,255))
        tela.blit(texto, (cx - texto.get_width()//2, cy + tamanho + 20))
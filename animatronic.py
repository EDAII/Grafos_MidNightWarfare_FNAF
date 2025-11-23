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
        self.tipo_ia = tipo_ia 
        self.ultimo_movimento = time.time()
        self.pos_x, self.pos_y = POSICOES[start_node]
        self.target_x, self.target_y = POSICOES[start_node]
        self.memoria_dfs = []

    def atualizar(self, portas_fechadas):
        self.pos_x += (self.target_x - self.pos_x) * 0.12
        self.pos_y += (self.target_y - self.pos_y) * 0.12

        if time.time() - self.ultimo_movimento <= self.agressividade:
            return

        vizinhos = GRAFO[self.node_atual]
        proximo = self.node_atual

        if "Office" in vizinhos:
            lado = 0 if self.node_atual == "West Hall Corner" else 1 if self.node_atual == "East Hall Corner" else None
            if lado is not None:
                if portas_fechadas[lado]:
                    if self.tipo_ia == "foxy":
                        self.node_atual = self.start_node
                        self.target_x, self.target_y = POSICOES[self.start_node]
                    self.ultimo_movimento = time.time()
                    return
                else:
                    proximo = "Office"
        
        if proximo != "Office":
            if self.tipo_ia == "bfs":
                proximo = obter_proximo_passo_bfs(self.node_atual, "Office")
            elif self.tipo_ia == "dfs":
                self.memoria_dfs.append(self.node_atual)
                if len(self.memoria_dfs) > 3: self.memoria_dfs.pop(0)
                proximo = obter_proximo_passo_dfs(self.node_atual, self.memoria_dfs)
            elif self.tipo_ia == "foxy":
                if self.node_atual == "Pirate Cove":
                    if random.random() < 0.4: proximo = "West Hall"
                elif self.node_atual == "West Hall":
                    proximo = "West Hall Corner"

        self.node_atual = proximo
        self.target_x, self.target_y = POSICOES[proximo]
        self.ultimo_movimento = time.time()

    def desenhar(self, tela):
        w, h = tela.get_size()
        px = int(self.pos_x * w)
        py = int(self.pos_y * h)
        pygame.draw.circle(tela, (*self.cor, 150), (px, py), 20)
        
        font = pygame.font.SysFont("arial", 12, bold=True)
        texto = font.render(self.nome[0], True, (255,255,255))
        tela.blit(texto, (px - texto.get_width()//2, py - texto.get_height()//2))

    def desenhar_camera_view(self, tela):
        w, h = tela.get_size()
        tamanho = int(h * 0.25)
        cx = w // 2
        cy = h // 2
        pygame.draw.circle(tela, self.cor, (cx, cy), tamanho)
        font = pygame.font.SysFont("consolas", 32)
        texto = font.render(self.nome, True, (255,255,255))
        tela.blit(texto, (cx - texto.get_width()//2, cy + tamanho + 20))
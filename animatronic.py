import random
import time
import math
import pygame

from config import POSICOES, LARGURA, ALTURA
from grafo import GRAFO

class Animatronic:
    def __init__(self, nome, cor, start_node, agressividade):
        self.nome = nome
        self.cor = cor
        self.start_node = start_node
        self.node_atual = start_node
        self.agressividade = agressividade
        self.ultimo_movimento = time.time()
        self.pos_x, self.pos_y = POSICOES[start_node]
        self.target_x, self.target_y = POSICOES[start_node]

    def atualizar(self, portas_fechadas):
        self.pos_x += (self.target_x - self.pos_x) * 0.12
        self.pos_y += (self.target_y - self.pos_y) * 0.12

        if time.time() - self.ultimo_movimento <= self.agressividade:
            return

        vizinhos = GRAFO[self.node_atual]

        if "Office" in vizinhos:
            if self.node_atual == "West Hall Corner":
                if portas_fechadas[0]: return
            if self.node_atual == "East Hall Corner":
                if portas_fechadas[1]: return
            proximo = "Office"
        else:
            proximo = random.choice(vizinhos)

        self.node_atual = proximo
        self.target_x, self.target_y = POSICOES[proximo]
        self.ultimo_movimento = time.time()

    def desenhar(self, tela):
        pass  # NÃO DESENHA NO MAPA!!!

    def desenhar_camera_view(self, tela):
        tamanho = 120
        cx = LARGURA // 2
        cy = ALTURA // 2

        pygame.draw.circle(tela, self.cor, (cx, cy), tamanho)

        font = pygame.font.SysFont("consolas", 32)
        texto = font.render(self.nome, True, (255,255,255))
        tela.blit(texto, (cx - texto.get_width()//2, cy + tamanho + 20))

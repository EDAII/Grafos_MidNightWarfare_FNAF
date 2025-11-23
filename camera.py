import pygame
from config import *
from grafo import GRAFO


def desenhar_interface_camera(tela, sala_atual, animatronics):
    fonte = pygame.font.SysFont("consolas", 30)

    # fundo escuro da câmera
    tela.fill((10, 10, 10))

    texto = fonte.render(f"Câmera: {sala_atual}", True, (0, 200, 255))
    tela.blit(texto, (20, 20))

    # desenha retângulo da sala
    pygame.draw.rect(tela, (80, 80, 80), (100, 120, 600, 400))

    # verifica animatronics na sala
    for anim in animatronics:
        if anim.node_atual == sala_atual:
            pygame.draw.circle(tela, anim.cor, (400, 320), 40)
            nome = fonte.render(anim.nome, True, anim.cor)
            tela.blit(nome, (360, 370))

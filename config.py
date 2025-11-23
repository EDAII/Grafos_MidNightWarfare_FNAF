import pygame

# Configurações Visuais 
LARGURA, ALTURA = 1024, 768
COR_FUNDO = (10, 15, 20)  # azul muito escuro
COR_LINHA = (40, 60, 80)  # azul escuro para conexões inativas
COR_SALA = (0, 255, 200)  # ciano neon para salas
COR_PORTA_FECHADA = (255, 50, 50) # vermelho
COR_PORTA_ABERTA = (50, 255, 50)  # verde
COR_OFFICE = (200, 200, 200)

    

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


def desenhar_hud(tela, portas, energia):
    #fonte
    font_hud = pygame.font.SysFont("consolas", 24)
    texto_energia = font_hud.render(f"POWER: {int(energia)}%", True, (255, 255, 255))
    texto_portas = font_hud.render(f"[A] Esq: {'FECHADA' if portas[0] else 'ABERTA'} | [D] Dir: {'FECHADA' if portas[1] else 'ABERTA'}", True, (200, 200, 200))
    tela.blit(texto_energia, (20, 700))
    tela.blit(texto_portas, (20, 730))
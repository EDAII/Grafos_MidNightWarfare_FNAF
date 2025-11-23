import pygame

# configuracoes visuais gerais
LARGURA, ALTURA = 800, 600 
COR_FUNDO = (10, 15, 20)
COR_LINHA = (40, 60, 80)
COR_SALA = (0, 255, 200)
COR_PORTA_FECHADA = (255, 50, 50)
COR_PORTA_ABERTA = (50, 255, 50)
COR_OFFICE = (200, 200, 200)


POSICOES = {
    "Palco": (0.5, 0.15),
    "Jantar": (0.5, 0.35),
    "Backstage": (0.22, 0.32),
    "Pirate Cove": (0.12, 0.45),
    "Banheiros": (0.78, 0.35),
    "Cozinha": (0.82, 0.58),
    "West Hall": (0.32, 0.58),
    "Despensa": (0.15, 0.65),
    "West Hall Corner": (0.32, 0.82),
    "East Hall": (0.68, 0.58),
    "East Hall Corner": (0.68, 0.82),
    "Office": (0.5, 0.92)
}

# funcao auxiliar para desenhar o heads up display com energia e estado das portas
def desenhar_hud(tela, portas, energia):
    w, h = tela.get_size()
    tamanho_fonte = max(20, int(h * 0.04))
    font_hud = pygame.font.SysFont("consolas", tamanho_fonte)
    
    texto_energia = font_hud.render(f"POWER: {int(energia)}%", True, (255, 255, 255))
    texto_portas = font_hud.render(f"[A] Esq: {'FECHADA' if portas[0] else 'ABERTA'} | [D] Dir: {'FECHADA' if portas[1] else 'ABERTA'}", True, (200, 200, 200))
    
    tela.blit(texto_energia, (20, h - tamanho_fonte * 2.5))
    tela.blit(texto_portas, (20, h - tamanho_fonte * 1.2))
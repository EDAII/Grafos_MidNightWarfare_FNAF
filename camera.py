import pygame
from config import *
from grafo import GRAFO

# offsets e dimensoes para o minimapa no canto inferior direito
MAPA_OFFSET_X = 520
MAPA_OFFSET_Y = 320
MAPA_LARGURA = 260 
MAPA_ALTURA = 260

# funcao principal de desenho da interface da camera
def desenhar_interface_camera(tela, sala_atual, animatronics):
    fonte = pygame.font.SysFont("consolas", 30)

    # fundo com cor solida simulando o monitor
    tela.fill((20, 20, 20))

    texto = fonte.render(f"CAM: {sala_atual}", True, (255, 255, 255))
    tela.blit(texto, (50, 50))

    # desenha o viewport da camera
    pygame.draw.rect(tela, (255, 255, 255), (45, 95, 410, 310), 2)
    pygame.draw.rect(tela, (10, 10, 10), (50, 100, 400, 300))

    # identifica animatronics presentes na sala visualizada
    anims_na_sala = [a for a in animatronics if a.node_atual == sala_atual]
    qtd = len(anims_na_sala)
    
    # logica de posicionamento para evitar sobreposicao visual
    if qtd > 0:
        centro_x, centro_y = 250, 250
        deslocamentos = []
        
        # define vetores de deslocamento baseados na quantidade de personagens
        if qtd == 1:
            deslocamentos = [(0, 0)]
        elif qtd == 2:
            # aumento do deslocamento para garantir separacao
            deslocamentos = [(-80, 0), (80, 0)]
        elif qtd == 3:
            deslocamentos = [(0, -60), (-70, 60), (70, 60)]
        else:
            deslocamentos = [(-70, -60), (70, -60), (-70, 60), (70, 60)]
            
        for i, anim in enumerate(anims_na_sala):
            # aplica o deslocamento se houver slot disponivel
            dx, dy = deslocamentos[i] if i < len(deslocamentos) else (0,0)
            px = centro_x + dx
            py = centro_y + dy
            
            # desenha o indicador do animatronic
            pygame.draw.circle(tela, anim.cor, (px, py), 35)
            nome = fonte.render(anim.nome, True, anim.cor)
            tela.blit(nome, (px - nome.get_width()//2, py + 45))
    else:
        # indicador de sala vazia
        txt_vazio = fonte.render("...", True, (50, 50, 50))
        tela.blit(txt_vazio, (230, 230))

    desenhar_minimapa(tela, sala_atual)

# renderiza os botões do minimapa interativo
def desenhar_minimapa(tela, sala_atual):
    for nome_sala, pos_ratio in POSICOES.items():
        if nome_sala == "Office": continue 

        # conversao de coordenada proporcional para tela do minimapa
        mx = MAPA_OFFSET_X + int(pos_ratio[0] * MAPA_LARGURA)
        my = MAPA_OFFSET_Y + int(pos_ratio[1] * MAPA_ALTURA)
        
        # destaque para a sala selecionada
        cor_btn = (0, 255, 0) if nome_sala == sala_atual else (100, 100, 100)
        tamanho_btn = (30, 20)
        
        rect_sala = pygame.Rect(mx - tamanho_btn[0]//2, my - tamanho_btn[1]//2, tamanho_btn[0], tamanho_btn[1])
        pygame.draw.rect(tela, cor_btn, rect_sala)
        pygame.draw.rect(tela, (255, 255, 255), rect_sala, 1) 

# detecta cliques do mouse nos botoes do minimapa
def verificar_clique_mapa(pos_mouse):
    x_mouse, y_mouse = pos_mouse
    
    for nome_sala, pos_ratio in POSICOES.items():
        if nome_sala == "Office": continue

        mx = MAPA_OFFSET_X + int(pos_ratio[0] * MAPA_LARGURA)
        my = MAPA_OFFSET_Y + int(pos_ratio[1] * MAPA_ALTURA)
        
        if (mx - 15 <= x_mouse <= mx + 15) and (my - 10 <= y_mouse <= my + 10):
            return nome_sala
            
    return None
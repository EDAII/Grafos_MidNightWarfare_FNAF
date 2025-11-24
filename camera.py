import pygame
import math
import time
from config import *
from grafo import GRAFO

MAPA_OFFSET_X = 520
MAPA_OFFSET_Y = 320
MAPA_LARGURA = 260 
MAPA_ALTURA = 260

def desenhar_interface_camera(tela, sala_atual, animatronics):
    fonte = pygame.font.SysFont("consolas", 30)

    tela.fill((20, 20, 20))

    texto = fonte.render(f"CAM: {sala_atual}", True, (255, 255, 255))
    tela.blit(texto, (50, 50))

    pygame.draw.rect(tela, (255, 255, 255), (45, 95, 410, 310), 2)
    pygame.draw.rect(tela, (10, 10, 10), (50, 100, 400, 300))

    anims_na_sala = [a for a in animatronics if a.node_atual == sala_atual and a.tipo_ia != "golden"]
    qtd = len(anims_na_sala)
    
    if sala_atual == "Pirate Cove":
        foxy = next((a for a in animatronics if a.nome == "Foxy"), None)
        if foxy and foxy.node_atual == "Pirate Cove":
            msgs = ["(Cortinas Fechadas)", "(Espiando)", "(Saindo...)", "(VAZIO!)"]
            estado = foxy.foxy_estagio if foxy.foxy_estagio < 4 else 3
            cor_foxy = foxy.cor if estado > 0 else (100, 100, 100)
            
            pygame.draw.rect(tela, (50, 0, 0), (150, 150, 200, 200)) 
            if estado > 0 and estado < 3:
                pygame.draw.circle(tela, cor_foxy, (250, 250), 40 + (estado * 20))
            
            txt_estagio = fonte.render(msgs[estado], True, (255, 0, 0))
            tela.blit(txt_estagio, (150, 350))
            desenhar_minimapa(tela, sala_atual)
            return

    if qtd > 0:
        centro_x, centro_y = 250, 250
        deslocamentos = []
        
        if qtd == 1:
            deslocamentos = [(0, 0)]
        elif qtd == 2:
            deslocamentos = [(-80, 0), (80, 0)]
        elif qtd == 3:
            deslocamentos = [(0, -60), (-70, 60), (70, 60)]
        else:
            deslocamentos = [(-70, -60), (70, -60), (-70, 60), (70, 60)]
            
        for i, anim in enumerate(anims_na_sala):
            dx, dy = deslocamentos[i] if i < len(deslocamentos) else (0,0)
            px = centro_x + dx
            py = centro_y + dy
            
            if anim.nome == "Foxy" and sala_atual == "West Hall":
                ticks = pygame.time.get_ticks()
                offset_corrida = (ticks % 500) / 500.0 
                pos_x_corrida = 100 + (offset_corrida * 300) 
                
                s = pygame.Surface((400, 300), pygame.SRCALPHA)
                
                for j in range(3):
                    alpha = 100 - (j * 30)
                    lag = j * 30
                    x_ghost = 100 + (((ticks - lag) % 500) / 500.0 * 300)
                    pygame.draw.circle(s, (*anim.cor, alpha), (int(x_ghost) - 50, 150), 30)
                
                pygame.draw.circle(s, anim.cor, (int(pos_x_corrida) - 50, 150), 35)
                
                tela.blit(s, (50, 100))
                
                if ticks % 200 < 100:
                    txt_run = fonte.render("RUNNING!", True, (255, 0, 0))
                    tela.blit(txt_run, (180, 350))
                
                continue 

            pygame.draw.circle(tela, anim.cor, (px, py), 35)
            nome = fonte.render(anim.nome, True, anim.cor)
            tela.blit(nome, (px - nome.get_width()//2, py + 45))
    else:
        txt_vazio = fonte.render("...", True, (50, 50, 50))
        tela.blit(txt_vazio, (230, 230))

    desenhar_minimapa(tela, sala_atual)

def desenhar_minimapa(tela, sala_atual):
    for nome_sala, pos_ratio in POSICOES.items():
        if nome_sala == "Office": continue 

        mx = MAPA_OFFSET_X + int(pos_ratio[0] * MAPA_LARGURA)
        my = MAPA_OFFSET_Y + int(pos_ratio[1] * MAPA_ALTURA)
        
        cor_btn = (0, 255, 0) if nome_sala == sala_atual else (100, 100, 100)
        tamanho_btn = (30, 20)
        
        rect_sala = pygame.Rect(mx - tamanho_btn[0]//2, my - tamanho_btn[1]//2, tamanho_btn[0], tamanho_btn[1])
        pygame.draw.rect(tela, cor_btn, rect_sala)
        pygame.draw.rect(tela, (255, 255, 255), rect_sala, 1) 

def verificar_clique_mapa(pos_mouse):
    x_mouse, y_mouse = pos_mouse
    
    for nome_sala, pos_ratio in POSICOES.items():
        if nome_sala == "Office": continue

        mx = MAPA_OFFSET_X + int(pos_ratio[0] * MAPA_LARGURA)
        my = MAPA_OFFSET_Y + int(pos_ratio[1] * MAPA_ALTURA)
        
        if (mx - 15 <= x_mouse <= mx + 15) and (my - 10 <= y_mouse <= my + 10):
            return nome_sala
            
    return None
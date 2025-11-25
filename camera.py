import pygame
import random
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
            
            if anim.nome == "Foxy":
                if sala_atual == "West Hall":
                    if anim.foxy_chegada_westhall == 0:
                        anim.foxy_chegada_westhall = pygame.time.get_ticks()

                    duracao_corrida = 1800 
                    tempo_passado = pygame.time.get_ticks() - anim.foxy_chegada_westhall
                    progresso = min(tempo_passado / duracao_corrida, 1.0)

                    if progresso < 1.0:
                        start_x, start_y = 350, 180
                        end_x, end_y = 80, 350
                        
                        start_radius = 20
                        end_radius = 80

                        current_x = start_x + (end_x - start_x) * progresso
                        current_y = start_y + (end_y - start_y) * progresso
                        current_radius = start_radius + (end_radius - start_radius) * progresso
                        
                        ghost_surface = pygame.Surface((500, 500), pygame.SRCALPHA)
                        
                        for j in range(4):
                            if j == 0:
                                cx, cy, cr, alpha = current_x, current_y, current_radius, 255
                            else:
                                lag_prog = max(0, progresso - (j * 0.02))
                                cx = start_x + (end_x - start_x) * lag_prog
                                cy = start_y + (end_y - start_y) * lag_prog
                                cr = start_radius + (end_radius - start_radius) * lag_prog
                                alpha = 100 - (j * 25)
                            
                            cor_base = (*anim.cor, alpha)
                            
                            ear_h = cr * 1.2
                            pygame.draw.polygon(ghost_surface, cor_base, [
                                (cx - cr*0.7, cy - cr*0.3), 
                                (cx - cr*0.9, cy - cr*0.3 - ear_h), 
                                (cx - cr*0.2, cy - cr*0.8)
                            ])
                            pygame.draw.polygon(ghost_surface, cor_base, [
                                (cx + cr*0.7, cy - cr*0.3), 
                                (cx + cr*0.9, cy - cr*0.3 - ear_h), 
                                (cx + cr*0.2, cy - cr*0.8)
                            ])
                            
                            pygame.draw.circle(ghost_surface, cor_base, (int(cx), int(cy)), int(cr))

                        tela.blit(ghost_surface, (0, 0))
                        
                    else:
                        anim.foxy_animacao_concluida = True
                        txt_vazio = fonte.render("...", True, (50, 50, 50))
                        tela.blit(txt_vazio, (230, 230))
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
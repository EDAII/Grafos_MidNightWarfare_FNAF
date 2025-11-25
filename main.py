import pygame
import sys
import random
import time
from config import *
from grafo import desenhar_mapa, GRAFO
from animatronic import Animatronic
from camera import desenhar_interface_camera, verificar_clique_mapa

def desenhar_scanlines(surface, largura, altura):
    for i in range(0, altura, 4):
        pygame.draw.line(surface, (0, 0, 0, 150), (0, i), (largura, i), 2)

def desenhar_estatica(tela, largura, altura):
    for _ in range(400):
        rx = random.randint(0, largura)
        ry = random.randint(0, altura)
        c = random.randint(20, 100) 
        pygame.draw.rect(tela, (c, c, c), (rx, ry, 2, 2))

def menu_inicial(tela, clock):
    largura, altura = tela.get_size()
    
    fonte_titulo = pygame.font.SysFont("consolas", int(altura * 0.08), bold=True)
    fonte_subtitulo = pygame.font.SysFont("consolas", int(altura * 0.04))
    
    scanline_surf = pygame.Surface((largura, altura), pygame.SRCALPHA)
    desenhar_scanlines(scanline_surf, largura, altura)

    rodando_menu = True
    while rodando_menu:
        tela.fill((5, 5, 10)) 

        desenhar_estatica(tela, largura, altura)

        offset_x = random.randint(-2, 3) if random.random() > 0.7 else 0
        offset_y = random.randint(-2, 3) if random.random() > 0.7 else 0

        cor_titulo = (220, 220, 220)
        if random.random() > 0.98:
             cor_titulo = (200, 50, 50)

        titulo_txt = "MIDNIGHT"
        titulo_txt2 = "WARFARE"
        
        t1 = fonte_titulo.render(titulo_txt, True, cor_titulo)
        t1_sombra = fonte_titulo.render(titulo_txt, True, (50, 0, 0))
        
        pos_x1 = largura//2 - t1.get_width()//2
        pos_y1 = altura//3.5
        
        tela.blit(t1_sombra, (pos_x1 + 3, pos_y1 + 3))
        tela.blit(t1, (pos_x1 + offset_x, pos_y1 + offset_y))
        
        t2 = fonte_titulo.render(titulo_txt2, True, cor_titulo)
        t2_sombra = fonte_titulo.render(titulo_txt2, True, (50, 0, 0))
        
        pos_x2 = largura//2 - t2.get_width()//2
        pos_y2 = pos_y1 + t1.get_height() + 10
        
        tela.blit(t2_sombra, (pos_x2 + 3, pos_y2 + 3))
        tela.blit(t2, (pos_x2 + offset_x, pos_y2 + offset_y))

        if pygame.time.get_ticks() % 1000 < 600:
            subtitulo = fonte_subtitulo.render("> PRESS ENTER <", True, (150, 150, 150))
            tela.blit(subtitulo, (largura//2 - subtitulo.get_width()//2, altura//2 + 100))

        tela.blit(scanline_surf, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    rodando_menu = False

        pygame.display.flip()
        clock.tick(30)

def executar_jumpscare(tela, anim_nome, cor_animatronic):
    largura, altura = tela.get_size()
    centro_x, centro_y = largura // 2, altura // 2
    
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 1500: 
        tela.fill((0, 0, 0))
        
        shake_x = random.randint(-20, 20)
        shake_y = random.randint(-20, 20)
        cx = centro_x + shake_x
        cy = centro_y + shake_y
        
        if "Bonnie" in anim_nome:
            pygame.draw.ellipse(tela, cor_animatronic, (cx - 120, cy - 400, 80, 250))
            pygame.draw.ellipse(tela, cor_animatronic, (cx + 40, cy - 400, 80, 250))
        elif "Foxy" in anim_nome:
            pygame.draw.polygon(tela, cor_animatronic, [(cx - 150, cy - 100), (cx - 50, cy - 350), (cx, cy - 150)])
            pygame.draw.polygon(tela, cor_animatronic, [(cx + 150, cy - 100), (cx + 50, cy - 350), (cx, cy - 150)])
        elif "Freddy" in anim_nome or "Golden" in anim_nome:
            pygame.draw.circle(tela, cor_animatronic, (cx - 180, cy - 180), 70)
            pygame.draw.circle(tela, cor_animatronic, (cx + 180, cy - 180), 70)
        elif "Chica" in anim_nome:
            pygame.draw.ellipse(tela, cor_animatronic, (cx - 50, cy - 320, 100, 150))

        pygame.draw.circle(tela, cor_animatronic, (cx, cy), 280)
        
        pygame.draw.circle(tela, (0, 0, 0), (cx - 80, cy - 50), 70)
        pygame.draw.circle(tela, (0, 0, 0), (cx + 80, cy - 50), 70)
        
        pygame.draw.circle(tela, (255, 255, 255), (cx - 80, cy - 50), 15)
        pygame.draw.circle(tela, (255, 255, 255), (cx + 80, cy - 50), 15)
        
        rect_boca = pygame.Rect(cx - 100, cy + 80, 200, 120)
        pygame.draw.rect(tela, (0, 0, 0), rect_boca)
        
        pygame.display.flip()
        pygame.time.delay(30)

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA)) 
    pygame.display.set_caption("Midnight Warfare Fnaf")
    clock = pygame.time.Clock()

    menu_inicial(tela, clock)

    portas = [False, False]
    energia = 100.0
    hora_atual = 0
    acumulador_tempo = 0.0
    
    animatronics = [
        Animatronic("Freddy", (100, 50, 0), "Palco", 30.0, tipo_ia="bfs"),
        Animatronic("Bonnie", (100, 100, 200), "Palco", 11.0, tipo_ia="dfs"),
        Animatronic("Chica", (255, 255, 0), "Palco", 12.0, tipo_ia="dfs"),
        Animatronic("Foxy", (200, 50, 50), "Pirate Cove", 6.0, tipo_ia="foxy"),
        Animatronic("G.Freddy", COR_GOLDEN, "Palco", 0.0, tipo_ia="golden"), 
    ]

    rodando = True
    game_over = False
    vitoria = False
    energia_acabou = False
    camera_ligada = False
    
    sala_atual_camera = "Palco" 
    quem_matou = None
    
    confetes = []
    for _ in range(150):
        confetes.append({
            "x": random.randint(0, LARGURA),
            "y": random.randint(-600, 0),
            "vel": random.randint(2, 7),
            "cor": (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
            "tam": random.randint(5, 10)
        })
    tempo_vitoria_inicio = 0

    while rodando:
        tela.fill(COR_FUNDO)
        dt = clock.tick(60) / 1.0 
        segundos = dt / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            
            if not game_over and not vitoria:
                if event.type == pygame.MOUSEBUTTONDOWN and camera_ligada:
                    nova_sala = verificar_clique_mapa(pygame.mouse.get_pos())
                    if nova_sala:
                        sala_atual_camera = nova_sala

                if event.type == pygame.KEYDOWN:
                    if not energia_acabou:
                        if not camera_ligada:
                            if event.key == pygame.K_a: portas[0] = not portas[0]
                            if event.key == pygame.K_d: portas[1] = not portas[1]
                        if event.key == pygame.K_c: camera_ligada = not camera_ligada
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                menu_inicial(tela, clock) 
                
                energia = 100.0
                portas = [False, False]
                camera_ligada = False
                sala_atual_camera = "Palco"
                hora_atual = 0
                acumulador_tempo = 0.0
                energia_acabou = False
                game_over = False
                vitoria = False
                quem_matou = None
                tempo_vitoria_inicio = 0
                for c in confetes:
                    c["y"] = random.randint(-600, 0)
                
                for anim in animatronics:
                    if anim.tipo_ia != "golden":
                        anim.node_atual = anim.start_node
                        anim.pos_x, anim.pos_y = POSICOES[anim.start_node]
                        anim.target_x, anim.target_y = POSICOES[anim.start_node]
                        anim.memoria_dfs = []
                        anim.foxy_estagio = 0
                        anim.foxy_cooldown = 30.0
                        anim.foxy_chegada_westhall = 0
                        anim.foxy_animacao_concluida = False
                        anim.ultimo_movimento = time.time()
                    else:
                        anim.node_atual = "Palco" 

        if not game_over and not vitoria:
            acumulador_tempo += segundos
            if acumulador_tempo >= DURACAO_HORA:
                acumulador_tempo = 0
                hora_atual += 1
                if hora_atual == 6:
                    vitoria = True

            if energia <= 0 and not energia_acabou:
                portas[0] = False
                portas[1] = False
                energia_acabou = True
                camera_ligada = False

            nivel_uso = 1 
            if portas[0]: nivel_uso += 1
            if portas[1]: nivel_uso += 1
            if camera_ligada: nivel_uso += 1
            
            drenagem = nivel_uso * 0.244
            energia -= drenagem * segundos
            energia = max(0.0, energia)
            
            for anim in animatronics:
                anim.atualizar(portas, camera_ligada, sala_atual_camera)
                if anim.node_atual == "Office":
                    executar_jumpscare(tela, anim.nome, anim.cor)
                    if anim.nome == "G.Freddy":
                        pygame.quit()
                        sys.exit()
                    else:
                        game_over = True
                        quem_matou = anim.nome

            if camera_ligada and not energia_acabou:
                desenhar_interface_camera(tela, sala_atual_camera, animatronics)
            else:
                desenhar_mapa(tela, portas)
                
            desenhar_hud(tela, portas, energia, hora_atual)
            
            scanline_surf = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            desenhar_scanlines(scanline_surf, LARGURA, ALTURA)
            tela.blit(scanline_surf, (0,0))

        elif game_over:
            tela.fill((0, 0, 0))
            desenhar_estatica(tela, LARGURA, ALTURA) 
            
            fonte_go = pygame.font.SysFont("consolas", 80, bold=True)
            fonte_sub = pygame.font.SysFont("consolas", 30)
            
            off_x = random.randint(-2, 2)
            txt_go = fonte_go.render("GAME OVER", True, (200, 0, 0))
            txt_reset = fonte_sub.render("Pressione R para reiniciar", True, (150, 150, 150))
            
            tela.blit(txt_go, (LARGURA//2 - txt_go.get_width()//2 + off_x, ALTURA//2 - 50))
            tela.blit(txt_reset, (LARGURA//2 - txt_reset.get_width()//2, ALTURA//2 + 50))
            
            scanline_surf = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            desenhar_scanlines(scanline_surf, LARGURA, ALTURA)
            tela.blit(scanline_surf, (0,0))

        elif vitoria:
            tela.fill((0, 0, 0))
            
            if tempo_vitoria_inicio == 0:
                tempo_vitoria_inicio = pygame.time.get_ticks()
            
            tempo_decorrido = pygame.time.get_ticks() - tempo_vitoria_inicio
            
            fonte_grande = pygame.font.SysFont("consolas", 120, bold=True)
            fonte_peq = pygame.font.SysFont("consolas", 30)
            
            if tempo_decorrido < 2000:
                txt_hora = fonte_grande.render("5 AM", True, (100, 100, 100))
                tela.blit(txt_hora, (LARGURA//2 - txt_hora.get_width()//2, ALTURA//2 - 60))
            else:
                for c in confetes:
                    pygame.draw.rect(tela, c["cor"], (c["x"], c["y"], c["tam"], c["tam"]))
                    c["y"] += c["vel"]
                    if c["y"] > ALTURA:
                        c["y"] = random.randint(-100, -10)
                        c["x"] = random.randint(0, LARGURA)

                txt_hora = fonte_grande.render("6 AM", True, COR_VITORIA)
                txt_msg = fonte_peq.render("SOBREVIVEU A NOITE", True, (255, 255, 255))
                
                tela.blit(txt_hora, (LARGURA//2 - txt_hora.get_width()//2, ALTURA//2 - 80))
                tela.blit(txt_msg, (LARGURA//2 - txt_msg.get_width()//2, ALTURA//2 + 40))
                
                if tempo_decorrido > 4000:
                    txt_reset = fonte_peq.render("Pressione R para reiniciar", True, (150, 150, 150))
                    tela.blit(txt_reset, (LARGURA//2 - txt_reset.get_width()//2, ALTURA//2 + 100))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
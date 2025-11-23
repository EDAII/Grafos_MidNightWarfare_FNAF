import pygame
from config import *
from grafo import desenhar_mapa, GRAFO
from animatronic import Animatronic
from camera import desenhar_interface_camera, verificar_clique_mapa

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
    pygame.display.set_caption("FNAF")
    clock = pygame.time.Clock()

    # inicializacao de variaveis de estado
    portas = [False, False]
    energia = 100.0
    hora_atual = 0
    acumulador_tempo = 0.0
    
    animatronics = [
        Animatronic("Freddy", (255, 200, 0), "Palco", 30.0, tipo_ia="bfs"),
        Animatronic("Bonnie", (180, 50, 255), "Palco", 11.0, tipo_ia="dfs"),
        Animatronic("Chica", (255, 255, 50), "Palco", 12.0, tipo_ia="dfs"),
        Animatronic("Foxy", (255, 50, 50), "Pirate Cove", 6.0, tipo_ia="foxy"),
    ]

    rodando = True
    game_over = False
    vitoria = False
    energia_acabou = False
    camera_ligada = False
    
    sala_atual_camera = "Palco" 

    while rodando:
        # limpa a tela sempre no comeco do frame
        tela.fill(COR_FUNDO)
        dt = clock.tick(60) / 1.0 
        segundos = dt / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            
            # input so funciona se o jogo nao acabou
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
            
            # reset funciona mesmo na tela de game over
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                energia = 100.0
                portas = [False, False]
                camera_ligada = False
                sala_atual_camera = "Palco"
                hora_atual = 0
                acumulador_tempo = 0.0
                energia_acabou = False
                game_over = False
                vitoria = False
                for anim in animatronics:
                    anim.node_atual = anim.start_node
                    anim.pos_x, anim.pos_y = POSICOES[anim.start_node]
                    anim.target_x, anim.target_y = POSICOES[anim.start_node]
                    anim.memoria_dfs = []

        # logica do jogo roda apenas se nao acabou
        if not game_over and not vitoria:
            # sistema de tempo
            acumulador_tempo += segundos
            if acumulador_tempo >= DURACAO_HORA:
                acumulador_tempo = 0
                hora_atual += 1
                if hora_atual == 6:
                    vitoria = True

            # sistema de energia
            if energia <= 0 and not energia_acabou:
                portas[0] = False
                portas[1] = False
                energia_acabou = True
                camera_ligada = False

            nivel_uso = 1 
            if portas[0]: nivel_uso += 1
            if portas[1]: nivel_uso += 1
            if camera_ligada: nivel_uso += 1
            
            drenagem = nivel_uso * 0.104
            energia -= drenagem * segundos
            energia = max(0.0, energia)
            for anim in animatronics:
                anim.atualizar(portas)
                if anim.node_atual == "Office":
                    game_over = True

            # renderizacao do jogo normal
            if camera_ligada and not energia_acabou:
                desenhar_interface_camera(tela, sala_atual_camera, animatronics)
            else:
                desenhar_mapa(tela, portas)

            desenhar_hud(tela, portas, energia, hora_atual)

        # renderizacao das telas de fim de jogo
        elif game_over:
            tela.fill((0, 0, 0))
            fonte_go = pygame.font.SysFont("consolas", 80)
            fonte_sub = pygame.font.SysFont("consolas", 30)
            
            txt_go = fonte_go.render("GAME OVER", True, (200, 0, 0))
            txt_reset = fonte_sub.render("Pressione R para reiniciar", True, (150, 150, 150))
            
            tela.blit(txt_go, (LARGURA//2 - txt_go.get_width()//2, ALTURA//2 - 50))
            tela.blit(txt_reset, (LARGURA//2 - txt_reset.get_width()//2, ALTURA//2 + 50))

        elif vitoria:
            tela.fill((0, 0, 0))
            fonte_win = pygame.font.SysFont("consolas", 80)
            fonte_sub = pygame.font.SysFont("consolas", 30)
            
            txt_win = fonte_win.render("6 AM", True, COR_VITORIA)
            txt_msg = fonte_sub.render("Sobreviveu a noite!", True, (255, 255, 255))
            txt_reset = fonte_sub.render("Pressione R para jogar novamente", True, (150, 150, 150))
            
            tela.blit(txt_win, (LARGURA//2 - txt_win.get_width()//2, ALTURA//2 - 60))
            tela.blit(txt_msg, (LARGURA//2 - txt_msg.get_width()//2, ALTURA//2 + 20))
            tela.blit(txt_reset, (LARGURA//2 - txt_reset.get_width()//2, ALTURA//2 + 80))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
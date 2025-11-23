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

    portas = [False, False]
    energia = 100.0
    
    # inicializacao dos animatronics com suas ias e niveis de agressividade
    animatronics = [
        Animatronic("Freddy", (255, 200, 0), "Palco", 30.0, tipo_ia="bfs"),
        Animatronic("Bonnie", (180, 50, 255), "Palco", 11.0, tipo_ia="dfs"),
        Animatronic("Chica", (255, 255, 50), "Palco", 12.0, tipo_ia="dfs"),
        Animatronic("Foxy", (255, 50, 50), "Pirate Cove", 6.0, tipo_ia="foxy"),
    ]

    rodando = True
    game_over = False
    energia_acabou = False
    camera_ligada = False
    
    sala_atual_camera = "Palco" 

    while rodando:
        tela.fill(COR_FUNDO)
        dt = clock.tick(60) / 1.0 

        # verifica fim da energia
        if energia <= 0 and not energia_acabou:
                portas[0] = False
                portas[1] = False
                energia_acabou = True
                camera_ligada = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            
            # processamento de clique no minimapa apenas se a camera estiver ativa
            if event.type == pygame.MOUSEBUTTONDOWN and camera_ligada:
                nova_sala = verificar_clique_mapa(pygame.mouse.get_pos())
                if nova_sala:
                    sala_atual_camera = nova_sala

            if event.type == pygame.KEYDOWN and not game_over:
                if not energia_acabou:
                    # controle de portas bloqueado se o monitor estiver levantado
                    if not camera_ligada:
                        if event.key == pygame.K_a: portas[0] = not portas[0]
                        if event.key == pygame.K_d: portas[1] = not portas[1]
                    
                    # alternar estado do monitor
                    if event.key == pygame.K_c: camera_ligada = not camera_ligada
                
                # reset de debug
                if event.key == pygame.K_r:
                    energia = 100.0
                    portas = [False, False]
                    camera_ligada = False
                    sala_atual_camera = "Palco"
                    for anim in animatronics:
                        anim.node_atual = anim.start_node
                        anim.pos_x, anim.pos_y = POSICOES[anim.start_node]
                        anim.target_x, anim.target_y = POSICOES[anim.start_node]
                        anim.memoria_dfs = []
                    game_over = False

        if not game_over:
            segundos = dt / 1000.0
            
            # calculo de drenagem de energia baseado em niveis de uso
            nivel_uso = 1 # ventilador base
            if portas[0]: nivel_uso += 1
            if portas[1]: nivel_uso += 1
            if camera_ligada: nivel_uso += 1
            drenagem = nivel_uso * 0.104
            energia -= drenagem * segundos
            energia = max(0.0, energia)

            # ativa o game over se qualquer animatronic chegar no escritório
            for anim in animatronics:
                anim.atualizar(portas)
                if anim.node_atual == "Office":
                    game_over = True

        # renderizacao condicional baseada no estado do monitor
        if camera_ligada and not energia_acabou:
            desenhar_interface_camera(tela, sala_atual_camera, animatronics)
        else:
            # desenha apenas o mapa tatico sem os animatronics
            desenhar_mapa(tela, portas)

        desenhar_hud(tela, portas, energia)

        if game_over:
            texto_fim = pygame.font.SysFont("consolas", 60).render("GAME OVER", True, (255, 0, 0))
            tela.blit(texto_fim, (tela.get_width()//2 - texto_fim.get_width()//2, tela.get_height()//2))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
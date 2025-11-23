import pygame
from config import *
from grafo import desenhar_mapa, GRAFO
from animatronic import Animatronic
from camera import desenhar_interface_camera 

def main():
    pygame.init()
    # RESIZABLE permite redimensionar a janela livremente
    tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
    pygame.display.set_caption("FNAF-like - Demo Graph Theory")
    clock = pygame.time.Clock()

    portas = [False, False]
    energia = 100.0
    
    animatronics = [
        Animatronic("Freddy", (255, 200, 0), "Palco", 30.0, tipo_ia="bfs"),
        Animatronic("Bonnie", (180, 50, 255), "Palco", 11.0, tipo_ia="dfs"),
        Animatronic("Chica", (255, 255, 50), "Palco", 12.0, tipo_ia="dfs"),
        Animatronic("Foxy", (255, 50, 50), "Pirate Cove", 15.0, tipo_ia="foxy"),
    ]

    rodando = True
    game_over = False
    energia_acabou = False
    camera_ligada = False
    salas_camera = list(GRAFO.keys())
    indice_camera = 0 

    while rodando:
        tela.fill(COR_FUNDO)
        dt = clock.tick(60) / 1.0 

        if energia <= 0 and not energia_acabou:
                portas[0] = False
                portas[1] = False
                energia_acabou = True
                camera_ligada = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            
            if event.type == pygame.KEYDOWN and not game_over:
                if not energia_acabou:
                    if event.key == pygame.K_a: portas[0] = not portas[0]
                    if event.key == pygame.K_d: portas[1] = not portas[1]
                    if event.key == pygame.K_c: camera_ligada = not camera_ligada
                    
                    if camera_ligada:
                        if event.key == pygame.K_RIGHT:
                            indice_camera = (indice_camera + 1) % len(salas_camera)
                        elif event.key == pygame.K_LEFT:
                            indice_camera = (indice_camera - 1) % len(salas_camera)

                if event.key == pygame.K_r:
                    energia = 100.0
                    portas = [False, False]
                    camera_ligada = False
                    for anim in animatronics:
                        anim.node_atual = anim.start_node
                        anim.pos_x, anim.pos_y = POSICOES[anim.start_node]
                        anim.target_x, anim.target_y = POSICOES[anim.start_node]
                        anim.memoria_dfs = []
                    game_over = False

        if not game_over:
            segundos = dt / 1000.0
            nivel_uso = 1 
            if portas[0]: nivel_uso += 1
            if portas[1]: nivel_uso += 1
            if camera_ligada: nivel_uso += 1
            
            # a taxa base é aproximadamente 0.104 por cento por segundo por nivel de uso
            drenagem = nivel_uso * 0.104
            
            energia -= drenagem * segundos
            energia = max(0.0, energia)

            for anim in animatronics:
                anim.atualizar(portas)
                if anim.node_atual == "Office":
                    game_over = True

        if camera_ligada and not energia_acabou:
            desenhar_interface_camera(tela, salas_camera[indice_camera], animatronics)
        else:
            desenhar_mapa(tela, portas)
            # Desenhar animatronics no mapa tático
            for anim in animatronics:
                anim.desenhar(tela)

        desenhar_hud(tela, portas, energia)

        if game_over:
            texto_fim = pygame.font.SysFont("consolas", 60).render("GAME OVER", True, (255, 0, 0))
            tela.blit(texto_fim, (tela.get_width()//2 - texto_fim.get_width()//2, tela.get_height()//2))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
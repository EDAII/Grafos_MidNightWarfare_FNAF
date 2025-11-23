import pygame
from config import *
from grafo import desenhar_mapa, GRAFO
from animatronic import Animatronic


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("FNAF-like - Demo")
    clock = pygame.time.Clock()

    # Começa o jogo com as portas abertas e energia no 100%
    portas = [False, False]  # [esquerda, direita] False = aberta
    energia = 100.0
    
    # Lista de animatronics: adicione Freddy e Foxy (com seus spawns)
    animatronics = [
        Animatronic("Freddy", (255, 200, 0), "Palco", 30.0),
        Animatronic("Bonnie", (180, 50, 255), "Palco", 11.0),
        Animatronic("Chica", (255, 255, 50), "Palco", 12.0),
        Animatronic("Foxy", (255, 50, 50), "Pirate Cove", 15.0),
    ]

    rodando = True
    game_over = False
    energia_acabou = False
    camera_ligada = False
    salas_camera = list(GRAFO.keys())  # lista de salas
    indice_camera = 0  # começa mostrando a primeira sala

    while rodando:
        tela.fill(COR_FUNDO)
        dt = clock.tick(60) / 1.0  # dt em ms; vamos tratar dt como ms para decrementar energia de modo perceptível

        if energia <= 0 and not energia_acabou:
                portas[0] = False
                portas[1] = False
                energia_acabou = True
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            
            if event.type == pygame.KEYDOWN and not game_over:
                if not energia_acabou:
                    if event.key == pygame.K_a: # porta Esquerda (toggle)
                        portas[0] = not portas[0]
                    if event.key == pygame.K_d: # porta Direita (toggle)
                        portas[1] = not portas[1]
                    if event.key == pygame.K_c:  # toggle da câmera
                        camera_ligada = not camera_ligada
                if event.key == pygame.K_r:
                    # reset básico
                    energia = 100.0
                    portas = [False, False]
                    for anim in animatronics:
                        anim.node_atual = anim.start_node
                        anim.pos_x, anim.pos_y = POSICOES[anim.start_node]
                        anim.target_x, anim.target_y = POSICOES[anim.start_node]
                    game_over = False

        if not game_over:
            # gerenciamento da energia:
            # consumo base por segundo (convertendo dt em segundos)
            segundos = dt / 1000.0
            consumo_base_por_segundo = 0.05  # ajuste para ritmo do jogo
            consumo = consumo_base_por_segundo

            # cada porta fechada adiciona consumo significativo
            if portas[0]:
                consumo += 1
            if portas[1]:
                consumo += 1
            if camera_ligada:
                consumo += 1


            # consumo por segundo -> consumo * segundos
            energia -= consumo * segundos * 10  # multiplicador para ficar perceptível
            energia = max(0.0, energia)

            # atualizar animatronics
            for anim in animatronics:
                anim.atualizar(portas)
                if anim.node_atual == "Office":
                    game_over = True

        desenhar_mapa(tela, portas)
        desenhar_hud(tela, portas, energia)
        
        for anim in animatronics:
            anim.desenhar(tela)

        if game_over:
            texto_fim = pygame.font.SysFont("consolas", 60).render("GAME OVER", True, (255, 0, 0))
            tela.blit(texto_fim, (LARGURA//2 - texto_fim.get_width()//2, ALTURA//2))

        # grade estética
        for i in range(0, ALTURA, 4):
            pygame.draw.line(tela, (0, 0, 0, 50), (0, i), (LARGURA, i))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

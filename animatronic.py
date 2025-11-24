import random
import time
import pygame
from config import POSICOES, LARGURA, ALTURA
from grafo import GRAFO, obter_proximo_passo_bfs, obter_proximo_passo_dfs

class Animatronic:
    def __init__(self, nome, cor, start_node, agressividade, tipo_ia="random"):
        self.nome = nome
        self.cor = cor
        self.start_node = start_node
        self.node_atual = start_node
        self.agressividade = agressividade
        self.tipo_ia = tipo_ia 
        self.ultimo_movimento = time.time()
        self.pos_x, self.pos_y = POSICOES[start_node]
        self.target_x, self.target_y = POSICOES[start_node]
        self.memoria_dfs = []
        
        self.foxy_estagio = 0 
        self.foxy_cooldown = 5.0 

        self.salas_proibidas = set()
        if nome == "Bonnie":
            self.salas_proibidas = {"East Hall", "East Hall Corner", "Cozinha", "Banheiros", "Pirate Cove"}
        elif nome == "Chica":
            self.salas_proibidas = {"West Hall", "West Hall Corner", "Despensa", "Backstage", "Pirate Cove"}

    def atualizar(self, portas_fechadas, camera_ligada=False, sala_observada=None):
        self.pos_x += (self.target_x - self.pos_x) * 0.12
        self.pos_y += (self.target_y - self.pos_y) * 0.12

        if self.tipo_ia == "golden":
            if random.randint(0, 10000) == 666:
                self.node_atual = "Office"
            return

        if self.tipo_ia == "foxy" and self.node_atual == "Pirate Cove":
            sendo_observado = camera_ligada and (sala_observada == "Pirate Cove")
            
            if not sendo_observado:
                self.foxy_cooldown -= 0.016 
            else:
                self.foxy_cooldown = min(self.foxy_cooldown + 0.1, 5.0)

            if self.foxy_cooldown <= 0:
                self.foxy_estagio += 1
                self.foxy_cooldown = 5.0 
                if self.foxy_estagio > 3:
                    self.node_atual = "West Hall" 
                    self.target_x, self.target_y = POSICOES["West Hall"]
                    self.foxy_estagio = 0
                    self.ultimo_movimento = time.time() 
            return 

        if time.time() - self.ultimo_movimento <= self.agressividade:
            return

        vizinhos = GRAFO[self.node_atual]
        proximo = self.node_atual

        if "Office" in vizinhos:
            lado = 0 if self.node_atual == "West Hall Corner" else 1 if self.node_atual == "East Hall Corner" else None
            if lado is not None:
                if portas_fechadas[lado]:
                    if self.tipo_ia == "foxy":
                        self.node_atual = self.start_node
                        self.target_x, self.target_y = POSICOES[self.start_node]
                        self.foxy_estagio = 0
                        self.foxy_cooldown = 5.0
                        self.ultimo_movimento = time.time()
                    else:
                        recuo = [v for v in vizinhos if v != "Office"]
                        if recuo:
                            self.node_atual = random.choice(recuo)
                            self.target_x, self.target_y = POSICOES[self.node_atual]
                            self.memoria_dfs = [] 
                            self.ultimo_movimento = time.time()
                    return
                else:
                    proximo = "Office"
        
        if proximo != "Office":
            if self.tipo_ia == "bfs":
                proximo = obter_proximo_passo_bfs(self.node_atual, "Office")
            elif self.tipo_ia == "dfs":
                todos_vizinhos = GRAFO.get(self.node_atual, [])
                vizinhos_validos = [v for v in todos_vizinhos if v not in self.salas_proibidas]
                
                self.memoria_dfs.append(self.node_atual)
                if len(self.memoria_dfs) > 3: self.memoria_dfs.pop(0)
                
                proximo = obter_proximo_passo_dfs(self.node_atual, self.memoria_dfs, vizinhos_validos)
                
            elif self.tipo_ia == "foxy":
                if self.node_atual == "West Hall":
                    if time.time() - self.ultimo_movimento > 2.5:
                        proximo = "West Hall Corner"
                    else:
                        proximo = "West Hall"
                elif self.node_atual == "West Hall Corner":
                    proximo = "Office"
        
        self.node_atual = proximo
        self.target_x, self.target_y = POSICOES[proximo]
        self.ultimo_movimento = time.time()

    def desenhar(self, tela):
        w, h = tela.get_size()
        px = int(self.pos_x * w)
        py = int(self.pos_y * h)
        if self.tipo_ia != "golden":
            pygame.draw.circle(tela, (*self.cor, 150), (px, py), 20)
            font = pygame.font.SysFont("arial", 12, bold=True)
            texto = font.render(self.nome[0], True, (255,255,255))
            tela.blit(texto, (px - texto.get_width()//2, py - texto.get_height()//2))
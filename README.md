# MidNight Warfare Fnaf

## Alunos

| Matrícula | Nome |
|-----------------------|---------------------|
| 23/1033737 | Artur Mendonça Arruda |
| 23/1035464 | Lucas Mendonça Arruda |

## Sobre o Projeto

Este projeto é inspirado no jogo Five Nights at Freddy's (FNAF) e utiliza conceitos, mecânicas e personagens da franquia. O projeto não é oficial nem está associado à Scott Cawthon ou à empresa responsável pela franquia.

O objetivo é criar um projeto acadêmico, com fins educacionais e de aprendizado em programação de jogos, utilizando o conceito de grafos para construir o universo do jogo.

## Sobre o Jogo

O jogador controlará a maioria das mecânicas do jogo original Five Nights at Freddy’s, incluindo energia, portas, câmeras, nomes dos locais das câmeras e a mecânica do turno da manhã.  

## Mecânicas

O jogo implementa diversas mecânicas inspiradas no original, adaptadas para fins educacionais:

- **Energia**:  
  - Começa em 100%.  
  - Fechar portas ou abrir câmeras aumenta o consumo de energia.  
  - Se a energia chegar a 0%, o jogador perde automaticamente.  

- **Câmeras**:  
  - Permitem localizar os animatronics.  
  - Auxiliam o jogador a planejar estratégias para economizar energia.  

- **Portas**:  
  - Protege o jogador, impedindo que animatronics alcancem a sala do guarda.   

- **Turno**:  
  - O objetivo é sobreviver do início da noite até 6:00 da manhã.   

- **Animatronics / IA**:  
  - Cada animatronic possui inteligência artificial que decide os movimentos por meio de uma travessia em grafo:  

- **Jumpscare**:  
  - Se um animatronic alcançar a sala do guarda com a porta aberta, ocorre um jumpscare, encerrando o turno com derrota.  

- **Interface HUD**:  
  - Mostra energia restante, estado das portas e indicadores das câmeras para auxiliar na tomada de decisões.


# Guia de instalação

### Dependências do projeto

  - **Sistema operacional:** Linux ou Windows
  - **Linguagem:** Python versão 3 ou superior
  - **Bibliotecas externas** Pygame 2.6.1



## Como executar o projeto

1.  Clone o repositório

<!-- end list -->

```bash
git clone https://github.com/EDAII/Grafos_MidNightWarfare_FNAF
```

1.  Abra o terminal na pasta do projeto com o comando: `cd Grafos_MidNightWarfare_FNAF`
2. (Opcional) Crie um ambiente virtual:
3.  Baixe as bibliotecas externas na sua máquina com o comando:

```bash
pip install -r requirements.txt 
```

4.  Execute o programa com:
    ```
    python3 main.py
    ```

## Grafos e travessias

O jogo usa três comportamentos principais para movimentação dos animatronics. Abaixo está o que cada um realmente faz:

### 1. BFS — Busca em Largura

Essa travessia é utilizada pelo Freddy, e funciona da seguinte maneira:

- Possui uma fila de caminhos e um conjunto de visitados.
- Expande caminhos em largura, marca vizinhos como visitados e monta novos caminhos até encontrar `Office`.
- Quando encontra o `Office` retorna apenas o próximo nó do caminho, porque o animatronic só se move uma sala por vez.
- A busca é recalculada do zero quando o animatronic decide mover-se.

---

### 2. DFS — Busca em Profundidade adaptada

Essa travessia é utilizada pelo Bonnie e Chica, e funciona da seguinte forma:

- Obtém todos_vizinhos do nó atual e filtra vizinhos_validos impedindo que bonnie siga o percurso da direita e chica o da esquerda
- Acrescenta o nó atual em uma memória, armazenando 3.
- retorna um vizinho que não esteja na memoria se possível; se não houver, escolhe aleatoriamente entre os vizinhos.
- Ela não explora até o fim igual uma DFS padrão.


### 3. Caminho scriptado


- Fica em `Pirate Cove` com um prazo que diminui quando não está sendo observado pela câmera.
- Ao preencher estágios, Foxy avança.
- Se a porta estiver fechada ao chegar no corredor, Foxy recua.


Fechar a porta significa cortar a ligação dos corredores com o escritório.

## Capturas de tela

### Algoritmos de travessia

#### BFS



#### DFS


### Jogo rodando

#### Tela de início


#### Tela do mapa


#### Tela das câmeras


####
## Conclusão

O uso de grafos permitiu replicar o jogo Five Nights at Fredy's num contexto acadêmico, utilizando grafos para aplicar a lógica de movimentação dos robôs entre as salas. O uso de diversos tipos de busca em grafos fez com que o jogo se torna-se mais imprevisível, tornando a experiência do jogo menos monótona. 

### Link do Vídeo de apresentação


## Referências

## Histórico de Versões

\<div align="center"\>

| Versão | Data | Descrição | Autor | Revisor | Revisão |
|-----------|---------|--------------|----------|------------|------------|
| `v1.0` | 22/11/2025 | Estruturação inicial da README | [Artur Mendonça](https://github.com/ArtyMend07) e [Lucas Mendonça](https://github.com/lucasarruda9)| | |
| `v1.1` | 22/11/2025 | adicionando seção de guia de instalação | [Artur Mendonça](https://github.com/ArtyMend07) e [Lucas Mendonça](https://github.com/lucasarruda9)| | |
| `v1.2` | 24/11/2025 | Adicionando explicação sobre o projeto [Lucas Mendonça](https://github.com/lucasarruda9) | [Artur Mendonça](https://github.com/ArtyMend07) | |

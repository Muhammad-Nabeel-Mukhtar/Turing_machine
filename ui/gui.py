import pygame
import sys
import os

# Ensure project modules are accessible
sys.path.insert(0, '.')

from parser import parser
from tm_engine.simulator import simulate_turing_machine
from visualizer.ast_cfg_visualizer import generate_tm_graph

# === Pygame Setup ===
pygame.init()
WIDTH, HEIGHT = 900, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
BLUE = (52, 152, 219)
GRAY = (200, 200, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Turing Machine Simulator")

font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

input_box = pygame.Rect(50, 50, 400, 40)
run_button = pygame.Rect(470, 50, 120, 40)

user_input = ''
output_tape = ''

# === Parse config and generate AST/CFG ===
parser.parse_tm_config("input/config.tm")
generate_tm_graph(parser.transitions)

# === Draw the GUI ===
def draw_interface():
    screen.fill(WHITE)

    # Input section
    screen.blit(big_font.render("Enter Binary Input:", True, BLACK), (50, 20))
    pygame.draw.rect(screen, GRAY, input_box)
    pygame.draw.rect(screen, GREEN, run_button)
    txt_surface = font.render(user_input, True, BLACK)
    screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))
    screen.blit(font.render("Run", True, BLACK), (run_button.x + 35, run_button.y + 10))

    # Output section
    screen.blit(big_font.render("Final Tape Output:", True, BLACK), (50, 120))
    screen.blit(font.render(output_tape, True, BLUE), (50, 160))

    # Graph Image (AST/CFG)
    graph_path = "output/tm_cfg_ast.png"
    if os.path.exists(graph_path):
        try:
            graph_img = pygame.image.load(graph_path)
            graph_img = pygame.transform.scale(graph_img, (350, 250))
            screen.blit(graph_img, (500, 200))
        except pygame.error:
            screen.blit(font.render("Graph image failed to load.", True, RED), (500, 200))

    pygame.display.flip()

# === Main Loop ===
running = True
while running:
    draw_interface()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            elif event.key == pygame.K_RETURN:
                pass
            else:
                user_input += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if run_button.collidepoint(event.pos):
                if all(c in '01' for c in user_input):
                    try:
                        output_tape = simulate_turing_machine(parser.transitions, user_input)
                    except Exception as e:
                        output_tape = f"[!] Runtime Error: {str(e)}"
                else:
                    output_tape = "[!] Invalid input: only binary digits allowed"

    clock.tick(30)

pygame.quit()

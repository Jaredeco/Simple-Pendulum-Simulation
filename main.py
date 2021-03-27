import pygame
from globals import SCREEN_WIDTH, SCREEN_HEIGHT, white, green, red, black, FONT
from ui.components import Pendulum
from pygame_widgets import Slider, Button
import matplotlib.pyplot as plt
from collections import deque

pygame.init()
FPS = 60
CLOCK = pygame.time.Clock()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pendulum-Simulation")
pendulum = Pendulum()
plt.style.use("seaborn")
fig, ax = plt.subplots()
MOVE = False
A = L = G = 0


def start():
    global MOVE, button_s
    MOVE = not MOVE


sliders = [Slider(win, 700, 50, 70, 20, min=1, max=L, step=0.1, initial=1),
           Slider(win, 700, 100, 70, 20, min=30, max=350, step=0.1, initial=30),
           Slider(win, 700, 150, 70, 20, min=1, max=5000, step=0.1, initial=9.81)]
button_s = Button(win, 10, 10, 100, 50, text='Start/Stop',
                  fontSize=30, margin=20,
                  inactiveColour=green,
                  pressedColour=red, radius=50,
                  onClick=start)


def redraw_win():
    win.fill(white)
    pendulum.draw(win)
    texts = [FONT.render(f"Amplitude {A}", True, black), FONT.render(f"Length {L}", True, black),
             FONT.render(f"Gravity {G}", True, black)]
    if not MOVE:
        y = 50
        for t in texts:
            win.blit(t, (450, y))
            y += 50
        for s in sliders:
            s.draw()
    if MOVE:
        img = pygame.image.load("graph.png")
        win.blit(img, (470, -10))
    button_s.draw()
    pygame.display.flip()


def plot(mem):
    vals = pendulum.graph()
    for i in range(len(vals)):
        mem[i].append(vals[i])
    ax.clear()
    ax.set_title("Pendulum Graph")
    ax.set_xlabel("Time(s)")
    dpi = 130
    fig.set_size_inches(550 / dpi, 400 / dpi)
    ax.plot(mem[0], mem[1], label="Displacement")
    ax.plot(mem[0], mem[2], label="Acceleration")
    ax.plot(mem[0], mem[3], label="Velocity")
    ax.legend(loc=1)
    fig.savefig("graph.png", dpi=dpi, bbox_inches="tight")


RUN = True
mem = [deque(maxlen=40) for _ in range(4)]
while RUN:
    CLOCK.tick(FPS)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            RUN = False
    button_s.listen(events)
    if MOVE:
        plot(mem)
        pendulum.move()
    else:
        ax.clear()
        mem = [deque(maxlen=40) for _ in range(4)]
        for s in sliders:
            s.listen(events)
        vals = [float(round(s.getValue(), 1)) for s in sliders]
        A, L, G = vals
        sliders[0].max = L
        pendulum.set_values(vals)
        pendulum.change_pos()
    redraw_win()
pygame.quit()

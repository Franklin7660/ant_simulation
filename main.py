import Simulation
import Interface
import Control
import pygame
pygame.init()

simulation = Simulation.Simulation()
interface = Interface.Interface()
control = Control.Control(simulation, interface)

while control.run:
    control.update()

pygame.display.quit()
pygame.quit()
quit()


import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
import glob, os
import numpy as np

class Control:

    def __init__(self, simulation, interface = None):
        self.sim = simulation
        self.inter = interface
        self.t = 0
        self.build_widgets()
        self.run = True
        self.show_widgets = True
        self.widget_background = pygame.Surface((250,700), pygame.SRCALPHA)
        self.widget_background.fill((0,0,0,200))
        
        self.capture = False
        
        folder_path = './renders'
        for file in glob.glob(os.path.join(folder_path, '*')):
            os.remove(file)
            
            
            
    def show_hide_color(self):
        self.inter.color = not self.inter.color


    def manage_events(self, events):
                 
        for event in events:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False
                elif event.key == pygame.K_SPACE:
                    self.show_widgets = not self.show_widgets
                elif event.key == pygame.K_f:
                    #self.capture = True
                    pass
                
            elif event.type == pygame.QUIT:
                self.run = False

    def update(self):          
        self.sim.update()
        events = pygame.event.get()
        self.manage_events(events)
        if self.inter != None:
            self.inter.update(self.sim)
                               
            if self.capture and self.t%10 == 0:
                pygame.image.save(self.inter.win, f"renders/{self.t//10}.png")
                pygame.draw.circle(self.inter.win, (255,0,0), (10,10), 5)

            if self.show_widgets:
                self.update_widgets()
                pygame_widgets.update(events)
        
        pygame.display.update()       
        self.t += 1

    def update_widgets(self):
        self.inter.win.blit(self.widget_background,(0,195))
        self.inter.win.blit(self.widget_background,(1670,195))
        
        self.sim.sensor_angle = self.update_slider(self.angle_slider, self.angle_output, 'sensor angle')
        self.sim.sensor_length = self.update_slider(self.length_slider, self.length_output, 'sensor length')
        self.sim.steering_angle = self.update_slider(self.steering_slider, self.steering_output, 'steering step')
        self.sim.madness = self.update_slider(self.madness_slider, self.madness_output, 'madness')
        
        self.sim.evaporation = self.update_slider(self.evaporation_slider, self.evaporation_output, 'evaporation')
        self.sim.max_pheromone = self.update_slider(self.maxphe_slider, self.maxphe_output, 'contrast')
           
        self.info.setText("  SPACE to hide interface         ECHAP to quit")
        
    def shuffle_settings(self):
        self.sim.shuffle_params()
        
        self.angle_slider.setValue(self.sim.sensor_angle)
        self.length_slider.setValue(self.sim.sensor_length)
        self.angle_slider.setValue(self.sim.steering_angle)
        self.steering_slider.setValue(self.sim.sensor_angle)
        
        self.evaporation_slider.setValue(self.sim.evaporation)
        self.maxphe_slider.setValue(self.sim.max_pheromone)
        
        
    def build_widgets(self):
        self.angle_slider, self.angle_output = self.build_slider(25, 225, 0, 3.14, 0.01, self.sim.sensor_angle)
        self.length_slider, self.length_output = self.build_slider(25, 425, 1, 40, 0.01, self.sim.sensor_length)
        self.steering_slider, self.steering_output = self.build_slider(25, 625, -3.14, 3.14, 0.01, self.sim.steering_angle)
        self.madness_slider, self.madness_output = self.build_slider(25, 825, 0, 1, 0.01, self.sim.madness)
        
        self.evaporation_slider, self.evaporation_output = self.build_slider(1690, 225, 0, 0.05, 0.001, self.sim.evaporation)
        self.maxphe_slider, self.maxphe_output = self.build_slider(1690, 425, 1, 10, 0.01, self.sim.max_pheromone)
        
        self.info = TextBox(
            self.inter.win,
            0,
            1050,
            340,
            25,
            fontSize=15,
            colour=(0,0,0),
            textColour=(255,255,255)
        )
        
        self.color_button = Button(self.inter.win,1690,625,200,40,onClick=lambda:self.show_hide_color(),radius=20,text='thermal (slower)')
        self.shuffle_button = Button(self.inter.win,1690,825,200,40,onClick=lambda:self.shuffle_settings(),radius=20,text='random settings')
        
    def build_slider(self, x, y, min, max, step, initial):
        slider = Slider(
            self.inter.win,
            x,
            y,
            200,
            10,
            min=min,
            max=max,
            step=step,
            colour=(100,100,100),
            handleColour=(255,255,255),
            initial = initial
        )
        box = TextBox(
            self.inter.win,
            x - 10,
            y + 50,
            0,
            0,
            fontSize=23,
            colour=(0,0,0),
            textColour=(255,255,255)
        )
        box.disable
        return slider, box
        
    def update_slider(self, slider, textbox, title):
        value = slider.getValue()
        textbox.setText(title + f" : {round(value,3)}")
        return value
        
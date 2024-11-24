import unittest
import sys
import os
import pygame

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configurar el controlador de video a 'dummy' para evitar abrir ventanas gráficas
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()
        pygame.font.init()

    @classmethod
    def tearDownClass(cls):
        pygame.font.quit()
        pygame.quit()

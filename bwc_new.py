#!/usr/bin/env python2

import pygame
from pygame.locals import *

import time
import res

from settings import *

__author__ = 'fonter'

FPS = 10


class CardDeck():
    SUITS = ['clubs', 'diamonds', 'hearts', 'spades']
    NAME = ['7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self):
        self.cards = [[Card(x * 4 + y) for x in range(7, -1, -1)] for y in range(1, 5)]
        self.size = Rect(0, 0, len(self.cards[0]), len(self.cards))

    def get_by_point(self, point):
        for _, row in enumerate(self.cards):
            for _, c in enumerate(row):
                if c.rect.collidepoint(point):
                    return c
        return None

    def smart_locate_on_rect(self, rect):
        self.scale_all(Rect(0, 0, rect.width / self.size.width, rect.height / self.size.height))

        #all cards equal, ok?
        card_size = self.cards[0][0].rect

        for y, row in enumerate(self.cards):
            for x, c in enumerate(row):
                c.rect.x = x * card_size.width + 6
                c.rect.x += rect.width / 2 - self.size.width * card_size.width / 2

                c.rect.y = y * card_size.height
                c.rect.y += rect.height / 2 - self.size.height * card_size.height / 2

    def scale_all(self, rect):
        for _, row in enumerate(self.cards):
            for _, c in enumerate(row):
                c.scale(rect)

    def all_set_states(self, state):
        for _, row in enumerate(self.cards):
            for _, c in enumerate(row):
                c.set_state(state)


class Card(pygame.sprite.Sprite):
    #STATE
    CLOSE = 0
    OPEN = 1

    def __init__(self, number):
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = res.load_image("{0}.png".format(number), CARDS_FOLDER)
        self.original_image, self.original_rect = self.image, self.rect
        self.scaled_image = self.original_image

        self.state = Card.OPEN

    def scale(self, rect):
        scale_n = min(float(rect.width) / self.original_rect.width, float(rect.height) / self.original_rect.height)
        scale_size = (int(self.original_rect.width * scale_n), int(self.original_rect.height * scale_n))

        self.scaled_image = pygame.transform.smoothscale(self.original_image, scale_size)
        self.rect = self.image.get_rect()

        self.set_state(self.state)

    def update_image(self):
        self.image = self.scaled_image.copy()
        if self.state == Card.CLOSE:
            self.image.fill((255, 255, 255, SHADOW_ALPHA), None, pygame.BLEND_RGBA_MULT)

    def set_state(self, state):
        self.state = state
        self.update_image()


def run():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE, RESIZABLE)

    card_deck = CardDeck()
    card_deck.smart_locate_on_rect(screen.get_rect())

    sprites = pygame.sprite.Group(card_deck.cards)

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_SPACE or event.type == MOUSEBUTTONDOWN and event.button == 2:
                card_deck.all_set_states(Card.OPEN)
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if event.button == 1 or event.button == 2:
                    c = card_deck.get_by_point(pos)
                    if c:
                        c.set_state([Card.OPEN, Card.CLOSE][c.state])
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, RESIZABLE)
                card_deck.smart_locate_on_rect(screen.get_rect())

        screen.fill(TABLE_COLOR)
        sprites.draw(screen)

        pygame.display.flip()

        time.sleep(1. / FPS)

if __name__ == "__main__":
    run()
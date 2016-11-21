#! /usr/bin/env python

"""
pygame gui for Synonym crawler game
written by David Goldstein on 11.20.2016
using http://www.pygame.org/project-Mek%27s+Sample+Code-2823-.html
"""

import os
import sys
import SynonymCrawler

import pygame as pg


CAPTION = "Synonym Crawler"
SCREEN_SIZE = (450, 600)


class Header(object):
    """
    Header at top of page displaying curr / targe word and definition
    """
    SIZE = (SCREEN_SIZE[0], SCREEN_SIZE[1] / 3)
    
    def __init__(self, crawler,pos):
        """
        The argument pos corresponds to the center of our rectangle.
        """
        self.rect = pg.Rect((0,0), Header.SIZE)
        self.rect.top = pos
        
        self.currWord = self.setup_font(crawler.currWord,True)
        self.currDef = self.setup_font(crawler.currDefinition,False)
        self.targetWord = self.setup_font(crawler.targetData[0],True)
        self.targetDef = self.setup_font(crawler.scrapeDefinition(crawler.targetData[0]),False)

        self.label_data = []
        self.label_data.append(self.currWord)
        self.label_data.append(self.currDef)
        self.label_data.append(self.targetWord)
        self.label_data.append(self.targetDef)


        self.click = False

    def setup_font(self,word,title):
        """
        If your text doesn't change it is best to render once, rather than
        re-render every time you want the text.  Rendering text every frame is
        a common source of bottlenecks in beginner programs.
        """
        font = None
    
        if title == True:
            font = pg.font.SysFont('timesnewroman', Header.SIZE[0] / 17)
            font.set_bold(True)
            word += ":"

        elif title == False:
            font = pg.font.SysFont('timesnewroman', Header.SIZE[0] / 25)
            font.set_italic(True)

        message = word
        label = font.render(message, True, pg.Color("white"))
        label_rect = label.get_rect()
        return label, label_rect

    def update(self, crawler, screen_rect):
        """
        If the square is currently clicked, update its position based on the
        relative mouse movement.  Clamp the rect to the screen.
        """
        pass

    def draw(self, surface):
        """
        Blit image and text to the target surface.
        """
        surface.fill(pg.Color("blue"), self.rect)

        yDispl = 15
        for label in self.label_data:
            label[1].center = (self.rect.centerx,self.rect.top + yDispl)            
            yDispl += int(Header.SIZE[1] / 4)
            surface.blit(label[0], label[1] )



class App(object):
    """
    A class to manage our event, game loop, and overall program flow.
    """
    def __init__(self):
        """
        Get a reference to the screen (created in main); define necessary
        attributes; and create our Header (draggable rect).
        """


        #init model
        self.crawler = SynonymCrawler.SynonymCrawler("test",leafWidth=3)
        
        #init display
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.done = False
        self.keys = pg.key.get_pressed()
        self.Header = Header(self.crawler,self.screen_rect.top)


    def event_loop(self):
        """
        This is the event loop for the whole program.
        Regardless of the complexity of a program, there should never be a need
        to have more than one event loop.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pass
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.Header.click = False
            elif event.type in (pg.KEYUP, pg.KEYDOWN):
                self.keys = pg.key.get_pressed()

    def render(self):
        """
        All drawing should be found here.
        This is the only place that pygame.display.update() should be found.
        """
        self.screen.fill(pg.Color("black"))
        self.Header.draw(self.screen)
        pg.display.update()

    def main_loop(self):
        """
        This is the game loop for the entire program.
        Like the event_loop, there should not be more than one game_loop.
        """
        while not self.done:
            self.event_loop()
            self.Header.update(self.crawler,self.screen_rect)
            self.render()
            self.clock.tick(self.fps)


def main():
    """
    Prepare our environment, create a display, and start the program.
    """
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    App().main_loop()
    pg.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()

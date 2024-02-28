import copy
from enum import Enum
import pygame as pg
import pygame_gui as gui
from chess_model import ChessModel, MoveValidity, UndoException
from move import Move
from player import Player

IMAGE_SIZE = 52  #small format - images 52 X 52


class SpriteType(Enum):
    King = 0
    Queen = 1
    Bishop = 2
    Knight = 3
    Rook = 4
    Pawn = 5

class SpriteColor(Enum):
    WHITE = 0
    BLACK = 1

class GUI:
    first = True
    def __init__(self) -> None:
        pg.init()
        self.__model = ChessModel()
        self._screen = pg.display.set_mode((800, 600))
        pg.display.set_caption("Laker Chess")
        self._ui_manager = gui.UIManager((800, 600))
        self._side_box = gui.elements.UITextBox('<b>Laker Chess</b><br /><br />White moves first.<br />',
                                                relative_rect=pg.Rect((500, 100), (400, 500)),
                                                manager=self._ui_manager)
        self._undo_button = gui.elements.UIButton(relative_rect = pg.Rect((700, 50), (100, 50)),
                                                  text='Undo',
                                                  manager=self._ui_manager)
        self._restart_button = gui.elements.UIButton(relative_rect = pg.Rect((600, 50), (100, 50)),
                                                     text='Reset',
                                                     manager=self._ui_manager)
        self._piece_selected = False
        self._first_selected = (0, 0)
        self._second_selected = (0, 0)
    
    @classmethod
    def load_images(cls):
        def load_image(color, ptype):
            SS = pg.image.load('./images/pieces.png')
            a = 105
            surf = pg.Surface((a,a), pg.SRCALPHA)
            surf.blit(SS, (0, 0), pg.rect.Rect(a*ptype.value, color.value*a, a, a))
            surf_scaled = pg.transform.scale(surf, (IMAGE_SIZE, IMAGE_SIZE))
            return surf_scaled
        cls.white_sprites = {}
        cls.black_sprites = {}
        for st in SpriteType:
            cls.white_sprites[st.name] = load_image(SpriteColor.WHITE, st)
            cls.black_sprites[st.name] = load_image(SpriteColor.BLACK, st)

    def run_game(self) -> None:
        running = True
        time_delta = 0
        clock = pg.time.Clock()
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    x, y = pg.mouse.get_pos()
                    y, x = self.__get_coords__(y, x)
                    piece = self.__model.piece_at(y, x)
                    if not self._piece_selected and piece:
                        if piece.player != self.__model.current_player:
                            msg = 'Not your turn!'
                            self._side_box.append_html_text(msg + '<br />')
                        else:
                            self._piece_selected = True
                            self._first_selected = y, x
                            self._piece_selected = piece
                    elif self._piece_selected:
                        mv = Move(self._first_selected[0], self._first_selected[1], y, x)
                        if self.__model.is_valid_move(mv):
                            target = self.__model.piece_at(y, x)
                            self.__model.move(mv)
                            if target is not None:
                                msg = f'Moved {self._piece_selected} and captured {target}'
                            else:
                                msg = f'Moved {self._piece_selected}'
                            self._side_box.append_html_text(msg + '<br />')
                        
                        else:
                            self._side_box.append_html_text(f'{self.__model.messageCode}<br />')
                        incheck = self.__model.in_check(self.__model.current_player)
                        complete = self.__model.is_complete()

                        if incheck:
                            player_color = self.__model.current_player.name
                            if complete:
                                self._side_box.append_html_text(f'{player_color} is in CHECKMATE!<br />GAME OVER!')
                            else:
                                self._side_box.append_html_text(f'{player_color} is in CHECK!<br />')
                        
                        self._piece_selected = False
                    else:
                        self._piece_selected = False
                if event.type == gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self._restart_button:
                        self.__model = ChessModel()
                        self._side_box.set_text("Restarting game...<br />")
                    if event.ui_element == self._undo_button:
                        try:
                            self.__model.undo()
                            self._side_box.append_html_text('Undoing move.<br />')
                        except UndoException as e:
                            self._side_box.append_html_text(f'{e}<br />')
            self._ui_manager.process_events(event)

            self._screen.fill((255, 255, 255))
            self.__draw_board__()
            self._ui_manager.draw_ui(self._screen)
            self._ui_manager.update(time_delta)

            pg.display.flip()
            time_delta = clock.tick(30) / 1000.0

    def __get_coords__(self, y, x):
        grid_x = x // IMAGE_SIZE
        grid_y = y // IMAGE_SIZE
        return grid_y, grid_x

    def __draw_board__(self) -> None:
        count = 0
        color = (255, 255, 255)
        for x in range(0, 8):
            for y in range(0, 8):
                if count % 2 == 0:
                    color = (255, 255, 255)
                else:
                    color = (127, 127, 127)
                count = count + 1
                pg.draw.rect(self._screen, color, pg.rect.Rect(x * IMAGE_SIZE, y * IMAGE_SIZE, IMAGE_SIZE, IMAGE_SIZE))
                if self._piece_selected and (y, x) == self._first_selected:
                    pg.draw.rect(self._screen, (255, 0, 0), pg.rect.Rect(x * IMAGE_SIZE, y * IMAGE_SIZE, IMAGE_SIZE, IMAGE_SIZE), 2)
                draw_piece = self.__model.piece_at(y, x)
                if draw_piece is not None:
                    if draw_piece.player == Player.BLACK:
                        d = GUI.black_sprites
                    else:
                        d = GUI.white_sprites
                    self._screen.blit(copy.deepcopy(d[draw_piece.type()]), (x * IMAGE_SIZE, y * IMAGE_SIZE))
            count = count + 1
        pg.draw.line(self._screen, (0, 0, 0), (0, 840), (840, 840))
        pg.draw.line(self._screen, (0, 0, 0), (840, 840), (840, 0))
        GUI.first = False


def main():
    GUI.load_images()
    g = GUI()
    g.run_game()


if __name__ == '__main__':
    main()

import pygame
import sys
from pieces import Piece, King, Queen, Bishop, Knight, Rook, Pawn
import something
import math

WIDTH = 640
HEIGHT = 640

DARK = (58, 32, 13)
LIGHT = (255, 233, 213)
MEDIUM = (228, 174, 126)
RED = (255, 157, 142)
WHITE = 1
BLACK = 0

BOARD_SIZE = 640
BOARD_POS = (0, 0)
SQUARES = 8

SQUARE_SIZE = int((BOARD_END[0] - BOARD_START[0]) / SQUARES)

def main():

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    rect = Rect(BOARD_POS, (BOARD_POS[0] + BOARD_SIZE, BOARD_POS[1] + BOARD_SIZE))
    board = screen.subsurface(rect)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Chess')
    font = pygame.font.SysFont('Comic Sans MS', 30)

    images = load_images()



    grid, pieces = initialise_game(images)
    draw_board(board, pieces)

    turn = WHITE
    current_piece = None

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = grid_pos(mouse_pos)
                game_over = move(board, x, y, turn, current_piece, coloured_squares)

        pygame.display.update
        clock.tick(60)


def move(board, x, y, turn, current_piece, coloured_squares):

    game_over = False

    old_x, old_y = current_piece.get_pos()

    # if no current piece, change current piece if piece of turn colour is pressed
    if current_piece == None:
        press_piece(board, grid, turn, current_piece)

    else:
        move = current_piece.move((x, y), pieces, turn, grid)

        if move == -1:
            king_x, king_y = pieces[turn][0].get_pos()
            flash_king(board, grid, king_x, king_y)

        # if move is successful, draw background over prev pos and draw new piece
        elif move == 1:

            if pawn_promoting(current_piece):
                promotion()

            capture = move()

            if capture and material_draw():
                draw_material_draw()
                game_over = True

            elif checkmate():
                draw_checkmate()
                game_over = True

            elif stalemate():
                draw_stalemate()
                game_over = True

            turn = 1 - turn

        revert_square(board, grid, old_x, old_y)


def load_images():
    images = {}
    ls = ['king', 'queen', 'bishop', 'pawn', 'rook', 'knight']
    colours = ['white', 'black']
    for colour in colours:
        for item in ls:
            piece = colour + "_" + piece
            path = 'chess_pieces/' + piece + '.png'
            image = pygame.transform.scale((pygame.image.load(path).convert_alpha()), (SQUARE_SIZE, SQUARE_SIZE))
            images[piece] = image
    return images

def initialise_game(images):

    pieces_dict = create_pieces(images)
    pieces_ls = pieces_ls(pieces_dict)
    grid = get_board(pieces_dict)

    for colour in pieces_ls:
        for piece in colour:
            piece.update_moves(grid)

    return grid, pieces_ls

def create_pieces():
    pieces = {}
    pieces["black_pieces"] =  [Rook((0, 0), BLACK, images['black_rook']),
                    Knight((1, 0), BLACK, images['black_knight']),
                    Bishop((2, 0), BLACK, images['black_bishop']),
                    Queen((3, 0), BLACK, images['black_queen']),
                    King((4, 0), BLACK, images['black_king']),
                    Bishop((5, 0), BLACK, images['black_bishop']),
                    Knight((6, 0), BLACK, images['black_knight']),
                    Rook((7, 0), BLACK, images['black_rook'])]

    pieces["white_pieces"] = [Rook((0, 7), WHITE, images['white_rook']),
                    Knight((1, 7), WHITE, images['white_knight']),
                    Bishop((2, 7), WHITE, images['white_bishop']),
                    Queen((3, 7), WHITE, images['white_queen']),
                    King((4, 7), WHITE, images['white_king']),
                    Bishop((5, 7), WHITE, images['white_bishop']),
                    Knight((6, 7), WHITE, images['white_knight']),
                    Rook((7, 7), WHITE, images['white_rook'])]

    # create pawns for each colour and add to board and list
    pieces["white_pawns"] = [Pawn((x, 1), WHITE, images['white_pawn']) for x in range(SQUARES)]
    pieces["black_pawns"] = [Pawn((x, 7), BLACK, images['black_pawn']) for x in range(SQUARES)]

    return pieces

def pieces_ls(pieces_ls):

    pieces_ls = [[], []]
    pieces_ls[WHITE] = pieces_dict["white_pieces"] + pieces_dict["white_pawns"]
    pieces_ls[BLACK] = pieces_dict["black_pieces"] + pieces_dict["black_pawns"]

    pieces_ls[WHITE].insert(0, pieces_ls[WHITE].pop(4))
    pieces_ls[BLACK].insert(0, pieces_ls[BLACK].pop(3))

    return pieces_ls

def get_board(pieces):

    grid = [[] for i in range(SQUARES)]
    grid[0] = pieces["white_pieces"]
    grid[1] = pieces["white_pawns"]
    for i in range(2, 7):
        grid[i] = [None for j in range(SQUARES)]
    grid[6] = pieces["black_pawns"]
    grid[7] = pieces["black_pieces"]

    return grid

def draw_board(board, pieces):

    for x in range(SQUARES):
        for y in range(SQUARES):
            draw_square(board, x, y)

    # draw pieces
    for colour in pieces:
        for piece in colour:
            draw_piece(board, piece)

def draw_piece(board, piece):
    x, y = piece.get_pos()
    board.blit(piece.get_image(), (x * SQUARE_SIZE, y * SQUARE_SIZE))

def draw_square(board, x, y, *args):

    if len(args):
        colour = args[0]
    elif (x + y) % 2 == 0:
        colour = LIGHT
    else:
        colour = DARK

    x *= SQUARE_SIZE
    y *= SQUARE_SIZE

    pygame.draw.rect(board, colour, (x, y, x + SQUARE_SIZE, y + SQUARE_SIZE))

def press_piece(board, grid, turn, current_piece):

    if x >= 0 and y >= 0 and x < SQUARE_SIZE and y < SQUARE_SIZE:
    pressed_square = grid[y][x]
    if pressed_square and pressed_square.get_colour() == turn:
        current_piece = pressed_square
        draw_square(board, x, y, MEDIUM)
        draw_piece(board, current_piece)

def revert_square(board, grid, x, y):
    draw_square(board, x, y)
    piece = grid[y][x]
    if piece:
        draw_piece(piece)

def flash_king(board, grid, x, y):
    draw_square(board, x, y, RED)
    draw_piece(king)
    pygame.display.update()
    clock.tick(60)
    draw_square(board, x, y)
    draw_piece(king)

def pawn_promoting(current_piece):
    if isinstance(current_piece, Pawn):
        y = current_piece.get_pos()[1]
        if y == 0 or y == 7:
            return True
    return False

def promotion():

    new_piece = promote()
    if new_piece:
        remove_pawn()
        new_piece(new_piece)

def move_mini():

    draw_square(piece_x, piece_y)
    draw_square(x, y)
    draw_piece(current_piece)

    if square: # if capture
        pieces[turn].remove(square)
        if material_draw(pieces):
            draw = True

    if isinstance(current_piece, Pawn) and y[1] == 7:
        PROMOTIOOON

        draw up 4 squares in middle of board,
        if whire and goes up,


def grid_pos(mouse_pos):
    new_x = math.floor((mouse_pos[0] - BOARD_POS[0]) / SQUARE_SIZE)
    new_y = math.floor((mouse_pos[1] - BOARD_POS[1]) / SQUARE_SIZE)
    return (new_x, new_y)


def draw_game_over():

    banner_size = (5, 3.5)

    x_start = BOARD_START[0] + ((SQUARES - banner_size[0]) * SQUARE_SIZE / 2)
    y_start = BOARD_START[1] + ((SQUARES - banner_size[1]) * SQUARE_SIZE / 2)
    x_end = x_start + banner_size[0] * SQUARE_SIZE
    y_end = y_start + board_size[1] * SQUARE_SIZE

    pygame.draw.rect(screen, WHITE, (x_start, y_start, x_end, y_end))

    textsurface = myfont.render('Some Text', False, (0, 0, 0))
    screen.blit(textsurface,(0,0))

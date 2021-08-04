class Piece:
    def __init__(self, pos, colour, image):
        self.pos = pos
        self.prev_pos = pos
        self.moves = []
        self.prev_moves = []
        self.colour = colour
        self.image = image

    def get_pos(self):
        return self.pos

    def get_colour(self):
        return self.colour

    def get_image(self):
        return self.image

    def get_moves(self):
        return self.moves

    def revert_moves(self):
        self.moves = self.prev_moves

    def move(self, pos, pieces, turn, board):
        # returns boolean of whether move is successful

        if pos not in self.moves: # check if it is a valid move
            return 0

        self.prev_pos = self.pos # update position attr of piece
        self.pos = pos

        for piece in own_pieces: # update moves of all pieces on own side
            piece.update_moves(board)

        king = own_pieces[0].get_pos()
        check = False # update enemy moves and see if own king is in check
        for piece in enemy_pieces:
            piece.update_moves(board)
            if king in piece.get_moves():
                check = True

        if check: # invalid move because King will be in check
            self.pos = self.prev_pos
            for piece in own_pieces:
                piece.revert_moves()
            for piece in enemy_pieces:
                piece.revert_moves()
            return -1

        return 1


class King(Piece):

    def image():
        pass
        # return image

    def update_moves(self, board): # updates possible moves based on current pos

        self.prev_moves = self.moves
        self.moves = []

        x = [self.pos[0]] # array of valid x positions to move
        y = [self.pos[1]] # array of valid y positions to move

        # add valid positions to arrays
        if self.pos[0] > 0:
            x.append(self.pos[0] - 1)
        if self.pos[0] < 7:
            x.append(self.pos[0] + 1)

        if self.pos[1] > 0:
            y.append(self.pos[1] - 1)
        if self.pos[1] < 7:
            y.append(self.pos[1] + 1)

        # add valid moves to self.moves
        for i in x:
            for j in y:
                check = False
                for piece in enemy_pieces:
                    if (i, j) in piece.get_moves():
                        check = True
                if not check and (i, j) != self.pos:
                    if board[j][i] == None or board[j][i].get_colour() != self.colour:
                        self.moves.append((i, j))

class Rook(Piece):

    def update_moves(self, board):

        self.prev_moves = self.moves
        self.moves = Rook.find_moves(self, board)

    @staticmethod
    def find_moves(piece, board):

        moves = []
        directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        for direction in directions:
            # add possible moves on the same row
            x = piece.get_pos()[0] + direction[0]
            y = piece.get_pos()[1] + direction[1]
            while x >= 0 and x <= 7 and y >= 0 and y <= 7:
                if board[y][x] != None:
                    if board[y][x].get_colour() != piece.get_colour():
                        moves.append((x, y))
                    break

                moves.append((x, y))
                x += direction[0]
                y += direction[1]

        return moves


class Bishop(Piece):

    def __init__(self, pos, colour, image):
        super().__init__(pos, colour, image)
        self.type = (pos[0] + pos[1]) % 2

    def get_type():
        return self.type

    def update_moves(self, board):
        self.prev_moves = self.moves
        self.moves = Bishop.find_moves(self, board)


    @staticmethod
    def find_moves(piece, board):

        moves = []
        directions = [-1, 1]

        for i in directions:
            for j in directions:
                x = piece.get_pos()[0] + i
                y = piece.get_pos()[1] + j

                while x >= 0 and x <= 7 and y >= 0 and y <= 7:
                    if board[j][i] != None:
                        if board[j][i].get_colour() != piece.get_colour():
                            moves.append((x, y))
                        break
                    moves.append((x, y))
                    x += i
                    x += j

        return moves


class Queen(Piece):

    def update_moves(self, board):

        self.prev_moves = self.moves
        self.moves = []
        self.moves.append(Bishop.find_moves(self, board))
        self.moves.append(Rook.find_moves(self, board))


class Pawn(Piece):

    def __init__(self, pos, colour, image, promotion_images):
        super().__init__(pos, colour, image)

    def move(self, pos, pieces, turn, board):

        move = super().move(pos, pieces, turn, board)
        if move == 1 and (pos[1] == 0 or pos[1] == 7):
            return 2
        else:
            return move

    def revert_pos():
        self.pos = self.prev_pos

    def update_moves(self, board):
        self.prev_moves = self.moves
        self.moves = []

        if self.colour == 1: # white
            i = 1
        else:
            i = -1

        x = self.pos[0]
        y = self.pos[1] + i
        if y >= 0 and y <= 7:
            if board[y][x] == None:
                self.moves.append((x, y))
            for j in [-1, 1]:
                if x + j >= 0 and x + j <= 7 and board[y][x + j] != None:
                    if board[y][x + j].get_colour() != self.colour:
                        self.moves.append((x + j, y))


class Knight(Piece):

    def update_moves(self, board):
        self.prev_moves = self.moves
        self.moves = []

        ls = [[-2, 2], [-1, 1]]

        x = self.pos[0]
        y = self.pos[1]

        for i in range(2):
            for j in ls[i]:
                new_x = x + j
                if new_x >= 0 and new_x <= 7:
                    for k in ls[1 - i]:
                        new_y = y + k
                        if new_y >= 0 and new_y <= 7:
                            if board[new_y][new_x] == None or board[new_y][new_x].get_colour() != self.colour:
                                self.moves.append((new_x, new_y))

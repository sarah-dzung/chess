def checkmate(own_pieces, enemy_pieces): # returns boolean

    king = own_pieces[0]

    # check if king in check
    checks = 0
    check_piece = None

    for piece in enemy_pieces:
        if king in piece.get_moves():
            checks += 1
            check_piece = piece
    if checks == 0:
        return False

    # only 1 checking piece
    if checks == 1:
        check_pos = check_piece.get_pos()

        # check if own pieces can capture or block check
        # block/ capture checks in the same file
        if check_pos[0] == king[0]:
            if check_pos[1] < king[1]:
                y_range = (check_pos[1], king[1])
            else:
                y_range = (king[1] + 1, check_pos[1])

            for piece in own_pieces:
                for i in range(y_range):
                    if (check_pos[0], i) in piece.get_moves():
                        return False

        # block/ capture checks in the same row
        elif check_pos[1] == king[1]:
            if check_pos[0] < king[0]:
                x_range = (check_pos[0], king[0])
            else:
                x_range = (king[0], check_pos[0])

            for piece in own_pieces:
                for i in range(x_range):
                    if (i, check_pos[1]) in piece.get_moves():
                        return False

        # capture knights
        elif isinstance(check_piece, Knight):
            for piece in own_pieces:
                if check_pos in piece.get_moves():
                    return False

        # block/ capture diagonal check
        else:
            if check_pos[0] < king[0]:
                x_range = range(check_pos[0], king[0])
            else:
                x_range = range(check_pos[0], king[0], -1)

            if check_pos[1] < king[1]:
                y_range = range(check_pos[1], king[1])
            else:
                y_range = range(check_pos[1], king[1], -1)

            for piece in own_pieces:
                for i in range(len(x_range)):
                    if (x_range[i], y_range[i]) in piece.get_moves():
                        return False

    # check if there are any other valid squares for king to move
    for move in king.get_moves():
        valid_move = True
        for piece in enemy_pieces:
            if move in piece.get_moves():
                valid_move = False
        if valid_move == True:
            return False

    return True

def material_draw(pieces):

    all_pieces = [pieces[0][1:] + pieces[1][1:]]

    if len(all_pieces) == 0:
        draw = True
    elif len(all_pieces == 1):
        if isinstance(all_pieces[0], Knight) or isinstance(all_pieces[0], Bishop):
            draw = True
        else:
            draw = False

    else:
        draw = True
        for piece in all_pieces:
            if not isinstance(piece, Bishop):
                draw = False
                break
            elif piece.get_type() != all_pieces[0].get_type():
                draw = False
                break
    return draw

def stalemate(pieces):
    for piece in pieces:
        if len(piece.get_moves()):
            return False
    return True

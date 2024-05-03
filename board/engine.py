import chess
from stockfish import Stockfish
from texts.texts import TEXTS_RU

#
def create_AI():
    stf = Stockfish(path=r"stockfish\stockfish-windows-x86-64-avx2.exe")
    board_tmp = chess.Board()
    fen_tmp = board_tmp.fen()
    stf.set_fen_position(fen_tmp)

    return stf

#
def set_level_AI(stf, level, skill_type='ELO'):
    if level == 'easy':
        level = 500
    elif level == 'med':
        level = 1500
    elif level == 'hard':
        level = 3000

    stf.set_elo_rating(level)

    return stf
    
#
def get_user_move(board: chess.Board, move: str) -> str | bool:
    try:
        move = chess.Move.from_uci(move)
    except chess.InvalidMoveError:
        return False    

    if move in board.legal_moves:
        return move
    else:
        return False
    
#
def get_move_AI(stf, board) -> str:
    stf.set_fen_position(board.fen())
    move = stf.get_best_move()
    move = chess.Move.from_uci(move)
    return move

#
def check_win(board) -> bool | None:
    if board.is_checkmate():
        return True
    return None

#
def check_draw(board) -> str | None:
    if board.is_stalemate():
        return 'stalemate'
    elif board.is_insufficient_material():
        return 'ins_material'
    else:
        return None

#
def check_check(board, side) -> str:
    if board.is_check():
        return TEXTS_RU[f'{side}_check']
    else:
        return ''

#

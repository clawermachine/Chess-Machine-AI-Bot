from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from texts.texts import BUTTONS_RU

# game keyboards
def create_kb_8_8(move, side, pressed=None):
    if side == 'white':
        letters = 'a b c d e f g h'.split()
        digits = '8 7 6 5 4 3 2 1'.split()
    elif side == 'black':
        letters = 'h g f e d c b a'.split()
        digits = '1 2 3 4 5 6 7 8'.split()
        
    move_buttons = []

    for digit in digits:
        for letter in letters:
            label = letter + digit
            if label == pressed:
                label = '--'
                callback = 'freeze'
            else:
                callback = 'move_' + label

            button = InlineKeyboardButton(text=label, callback_data=callback)
            move_buttons.append(button)
            
    cancel_button = InlineKeyboardButton(text=BUTTONS_RU['cancel_move'],
                                         callback_data='cancel_move')
    yield_button = InlineKeyboardButton(text=BUTTONS_RU['yield'],
                                         callback_data='yield')
    let_AI_move_button = InlineKeyboardButton(text=BUTTONS_RU['let_AI_move'],
                                         callback_data='let_AI_move')
    toggle_inline_mode_button = InlineKeyboardButton(text=BUTTONS_RU['inline_mode'],
                                         callback_data='inline_mode')
    toggle_console_mode_button = InlineKeyboardButton(text=BUTTONS_RU['console_mode'],
                                         callback_data='console_mode')
    if move == 'human':
        # kb for player's move w/ buttons
        move_inline_kb_builder = InlineKeyboardBuilder()
        move_inline_kb_builder.row(*move_buttons, width=8)
        move_inline_kb_builder.row(toggle_console_mode_button, cancel_button, yield_button, width=1)
        move_inline_kb: InlineKeyboardMarkup = move_inline_kb_builder.as_markup(resize_keyboard=True)
        return move_inline_kb
    elif move == 'AI':
        # kb for player's waiting for AI move w/ buttons
        wait_inline_kb_builder = InlineKeyboardBuilder()
        wait_inline_kb_builder.row(let_AI_move_button, width=1)
        wait_inline_kb_builder.row(*move_buttons, width=8)
        wait_inline_kb_builder.row(toggle_console_mode_button, cancel_button, yield_button, width=1)
        wait_inline_kb: InlineKeyboardMarkup = wait_inline_kb_builder.as_markup(resize_keyboard=True)
        return wait_inline_kb


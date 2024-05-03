from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from texts.texts import BUTTONS_RU

# game keyboards
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
digits = ['8', '7', '6', '5', '4', '3', '2', '1']
move_buttons = []

for digit in digits:
    for letter in letters:
        label = letter + digit
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
# kb for player's move w/ buttons
move_inline_kb_builder = InlineKeyboardBuilder()
move_inline_kb_builder.row(*move_buttons, width=8)
move_inline_kb_builder.row(toggle_console_mode_button, cancel_button, yield_button, width=1)
move_inline_kb: InlineKeyboardMarkup = move_inline_kb_builder.as_markup(resize_keyboard=True)

# kb for player's waiting for AI move w/ buttons
wait_inline_kb_builder = InlineKeyboardBuilder()
wait_inline_kb_builder.row(let_AI_move_button, width=1)
wait_inline_kb_builder.row(*move_buttons, width=8)
wait_inline_kb_builder.row(toggle_console_mode_button, cancel_button, yield_button, width=1)
wait_inline_kb: InlineKeyboardMarkup = wait_inline_kb_builder.as_markup(resize_keyboard=True)



# human/AI keyboard
human_button = InlineKeyboardButton(text=BUTTONS_RU['against_human'],
                                     callback_data='against_human')
AI_button = InlineKeyboardButton(text=BUTTONS_RU['against_AI'],
                                     callback_data='against_AI')
        

human_AI_kb_builder = InlineKeyboardBuilder()
human_AI_kb_builder.row(human_button, AI_button, width=2)
human_AI_kb: InlineKeyboardMarkup = human_AI_kb_builder.as_markup(resize_keyboard=True)


# AI level keyboard
easy_button = InlineKeyboardButton(text=BUTTONS_RU['easy'],
                                     callback_data='easy')
med_button = InlineKeyboardButton(text=BUTTONS_RU['med'],
                                     callback_data='med')
hard_button = InlineKeyboardButton(text=BUTTONS_RU['hard'],
                                     callback_data='hard')
        

AI_level_kb_builder = InlineKeyboardBuilder()
AI_level_kb_builder.row(easy_button, med_button, hard_button, width=1)
AI_level_kb: InlineKeyboardMarkup = AI_level_kb_builder.as_markup(resize_keyboard=True)



# start position w/b keyboard
white_button = InlineKeyboardButton(text=BUTTONS_RU['white'],
                                     callback_data='white')
black_button = InlineKeyboardButton(text=BUTTONS_RU['black'],
                                     callback_data='black')

        
start_position_kb_builder = InlineKeyboardBuilder()
start_position_kb_builder.row(white_button, black_button, width=1)
start_position_kb: InlineKeyboardMarkup = start_position_kb_builder.as_markup(resize_keyboard=True)


# double start (during active game) keyboard
yes_ds_button = InlineKeyboardButton(text=BUTTONS_RU['yes_ds'],
                                     callback_data='yes_ds')
no_ds_button = InlineKeyboardButton(text=BUTTONS_RU['no_ds'],
                                     callback_data='no_ds')

        
ds_kb_builder = InlineKeyboardBuilder()
ds_kb_builder.row(yes_ds_button, no_ds_button, width=1)
ds_kb: InlineKeyboardMarkup = ds_kb_builder.as_markup(resize_keyboard=True)



# yield keyboard
yes_yield_button = InlineKeyboardButton(text=BUTTONS_RU['yes_yield'],
                                     callback_data='yes_yield')
no_yield_button = InlineKeyboardButton(text=BUTTONS_RU['no_yield'],
                                     callback_data='no_yield')

        
yield_kb_builder = InlineKeyboardBuilder()
yield_kb_builder.row(yes_yield_button, no_yield_button, width=1)
yield_kb: InlineKeyboardMarkup = yield_kb_builder.as_markup(resize_keyboard=True)

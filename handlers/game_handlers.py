from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state

from keyboards.kb_8_8 import create_kb_8_8
from keyboards.keyboards import (human_AI_kb, AI_level_kb,
                                 start_position_kb, ds_kb,
                                 yield_kb)
from board.board_actions import get_board_pic
from texts.texts import TEXTS_RU, BUTTONS_RU

from loguru import logger
from time import sleep
import chess
from board.engine import (get_user_move, create_AI,
                          set_level_AI, get_move_AI,
                          check_check, check_win,
                          check_draw)


#
router = Router()

#
class FSMgame(StatesGroup):
    game_start = State()
    move_human_from = State()
    move_human_to = State()
    move_AI = State()
    yield_Q = State()
  
#
@router.message(Command(commands='start_game'), StateFilter(default_state))
async def process_start_game(message: Message, state: FSMContext):
    logger.info('Starting new game')
    await state.set_state(FSMgame.game_start)
    await message.answer(text=TEXTS_RU['human_AI'], reply_markup=human_AI_kb)

#
@router.message(Command(commands='start_game'), StateFilter(FSMgame.move_human_from,
                                                            FSMgame.move_human_to,
                                                            FSMgame.move_AI))
async def process_second_start_game(message: Message, state: FSMContext):
    await message.answer(text=TEXTS_RU['second_start'], reply_markup=ds_kb)

    prev_state = await state.get_state()
    await state.update_data(prev_state=prev_state)
    await state.set_state(FSMgame.yield_Q)

#
@router.callback_query(F.data=='yes_ds', StateFilter(FSMgame.yield_Q))
async def process_yes_db(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text=TEXTS_RU['lose'])
    logger.info('Game finished with human"s yield')
    await state.set_state(FSMgame.game_start)
    logger.info('Starting new game')
    await callback.message.answer(text=TEXTS_RU['human_AI'], reply_markup=human_AI_kb)

#
@router.callback_query(F.data=='yes_ds', ~StateFilter(FSMgame.yield_Q))
async def process_yes2_db(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    
#
@router.callback_query(F.data=='no_ds', StateFilter(FSMgame.yield_Q))
async def process_no_db(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    data = await state.get_data()
    prev_state = data['prev_state'].split(':')[1]
    if prev_state == 'move_human_from':
        await state.set_state(FSMgame.move_human_from)
    elif prev_state == 'move_human_to':
        await state.set_state(FSMgame.move_human_to)
    elif prev_state == 'move_AI':
        await state.set_state(FSMgame.move_AI)
        
    await state.update_data(prev_state='')

#
@router.callback_query(F.data=='no_ds', ~StateFilter(FSMgame.yield_Q))
async def process_no2_db(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
#
@router.message(Command(commands='start_game'), StateFilter(FSMgame.yield_Q))
async def process_start_game_yield(message: Message, state: FSMContext):
    pass

#
@router.message(Command(commands='start_game'), StateFilter(FSMgame.game_start))
async def process_another_start_game(message: Message, state: FSMContext):
    logger.info('Starting new game')
    await state.clear()
    await state.set_state(FSMgame.game_start)
    await message.answer(text=TEXTS_RU['human_AI'], reply_markup=human_AI_kb)

    
#
@router.callback_query(F.data=='against_human', StateFilter(FSMgame.game_start))
async def process_start_against_human(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=TEXTS_RU['not_ready'])

#
@router.callback_query(F.data=='against_human', ~StateFilter(FSMgame.game_start))
async def process_start2_against_human(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
#
@router.callback_query(F.data=='against_AI', StateFilter(FSMgame.game_start))
async def process_start_against_AI(callback: CallbackQuery, state: FSMContext):
    AI_engine = create_AI()
    await state.update_data(AI_engine=AI_engine)
    await callback.message.edit_text(text=TEXTS_RU['AI_level'],
                                     reply_markup=AI_level_kb)

#
@router.callback_query(F.data=='against_AI', ~StateFilter(FSMgame.game_start))
async def process_start2_against_AI(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    
#
@router.callback_query(F.data.in_({'easy', 'med', 'hard'}), StateFilter(FSMgame.game_start))
async def process_set_AI_level(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    AI_level = callback.data
    AI_engine = set_level_AI(data['AI_engine'], AI_level)
    await state.update_data(AI_engine=AI_engine)
    await state.update_data(AI_level=AI_level)
    
    await callback.message.edit_text(text=TEXTS_RU['start_position'],
                                     reply_markup=start_position_kb)

#
@router.callback_query(F.data.in_({'easy', 'med', 'hard'}), ~StateFilter(FSMgame.game_start))
async def process_set2_AI_level(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    
#
@router.callback_query(F.data.in_({'white', 'black'}), StateFilter(FSMgame.game_start))
async def process_set_start_position(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    AI_level = data['AI_level']
    
    board = chess.Board()
    await state.update_data(board=board)

    side = callback.data
    if side == 'white':
        side_AI = 'black'
        await state.update_data(side=side)
        await state.update_data(side_AI=side_AI)
        reply_markup = create_kb_8_8(move='human', side=side)    
        await state.set_state(FSMgame.move_human_from)
    elif side == 'black':
        side_AI = 'white'
        await state.update_data(side=side)
        await state.update_data(side_AI=side_AI)
        reply_markup = create_kb_8_8(move='AI', side=side)   
        await state.set_state(FSMgame.move_AI)

    label = TEXTS_RU['new_game'].format(TEXTS_RU[side], TEXTS_RU[side_AI], BUTTONS_RU[AI_level])
    await callback.message.edit_text(text=label)
    logger.info('New game started')
    
    sleep(3)
    
    board_pic = get_board_pic(board, side)
    board_pic = FSInputFile(board_pic)
    caption = TEXTS_RU['white_move']
    
    await callback.message.answer_photo(photo=board_pic,
                                        caption=caption,
                                        reply_markup=reply_markup)

#
@router.callback_query(F.data.in_({'white', 'black'}), ~StateFilter(FSMgame.game_start))
async def process_set2_start_position(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    
#
@router.callback_query(F.data=='console_mode')
async def process_toggle_console_mode_callback(callback: CallbackQuery):
    await callback.answer()


#
@router.callback_query(F.data=='cancel_move')
async def process_cancel_move_callback(callback: CallbackQuery):
    await callback.answer()


#
@router.callback_query(F.data=='yield', StateFilter(FSMgame.move_human_from,
                                                    FSMgame.move_human_to,
                                                    FSMgame.move_AI))
async def process_yield_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text=TEXTS_RU['yield_Q'], reply_markup=yield_kb)

    prev_state = await state.get_state()
    await state.update_data(prev_state=prev_state)
    await state.set_state(FSMgame.yield_Q)

#
@router.callback_query(F.data=='yield', ~StateFilter(FSMgame.move_human_from,
                                                    FSMgame.move_human_to,
                                                    FSMgame.move_AI))
async def process_yield2_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    

#
@router.callback_query(F.data=='yes_yield', StateFilter(FSMgame.yield_Q))
async def process_yield_yes_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    logger.info('Game finished with human"s yield')
    await callback.message.edit_text(text=TEXTS_RU['lose'])
    await state.clear()

#
@router.callback_query(F.data=='yes_yield', ~StateFilter(FSMgame.yield_Q))
async def process_yield2_yes_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    

#
@router.callback_query(F.data=='no_yield', StateFilter(FSMgame.yield_Q))
async def process_yield_no_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    data = await state.get_data()
    prev_state = data['prev_state'].split(':')[1]
    if prev_state == 'move_human_from':
        await state.set_state(FSMgame.move_human_from)
    elif prev_state == 'move_human_to':
        await state.set_state(FSMgame.move_human_to)
    elif prev_state == 'move_AI':
        await state.set_state(FSMgame.move_AI)
        
    await state.update_data(prev_state='')

#
@router.callback_query(F.data=='no_yield', ~StateFilter(FSMgame.yield_Q))
async def process_yield2_no_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
#
@router.callback_query(F.data.startswith('move'), StateFilter(FSMgame.move_human_from))
async def process_move_from_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    press = callback.data[-2:]
    data = await state.get_data()
    side = data['side']
    reply_markup = create_kb_8_8(move='human', side=side, pressed=press)
    await callback.message.edit_reply_markup(reply_markup=reply_markup)
    await state.update_data(move=press)
    await state.set_state(FSMgame.move_human_to)
        
#
@router.callback_query(F.data.startswith('move'), StateFilter(FSMgame.move_human_to))
async def process_move_to_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    data = await state.get_data()
    move = data['move'] + callback.data[-2:]
    board = data['board']
    side = data['side']
    side_AI = data['side_AI']
    res = get_user_move(board, move)

    if not res:
        await state.set_state(FSMgame.move_human_to)
    else:
        board.push(res)
        await state.update_data(board=board)
        await state.update_data(move='')
        await state.set_state(FSMgame.move_AI)
        
        board_pic = get_board_pic(board, side)
        board_pic = FSInputFile(board_pic)
        reply_markup = create_kb_8_8(move='AI', side=side)
        
        win_status = check_win(board)
        draw_status = check_draw(board)
        
        if win_status:
            text_win = TEXTS_RU['checkmate'] + '\n' + TEXTS_RU['win']
            logger.info('Game finished with human"s win')
            await callback.message.answer(text=text_win)
            await state.clear()
        elif draw_status:
            text_draw = TEXTS_RU[draw_status] + '\n' + TEXTS_RU['draw']
            logger.info('Game finished with draw')
            await callback.message.answer(text=text_draw)
            await state.clear()
        else:
            caption = TEXTS_RU['human_move'] + str(res) + '\n'
            
            check_status = check_check(board, side)
            caption += check_status + TEXTS_RU[f'{side_AI}_move']
                
            await callback.message.edit_media(InputMediaPhoto(
                                                        media=board_pic,
                                                        caption=caption),
                                              reply_markup=reply_markup)

#
@router.callback_query(F.data=='freeze', StateFilter(FSMgame.move_human_to))
async def process_pressed_button_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(move='')

    data = await state.get_data()
    side = data['side']
    
    reply_markup = create_kb_8_8(move='human', side=side)
    await callback.message.edit_reply_markup(reply_markup=reply_markup)
    
    await state.set_state(FSMgame.move_human_from)
    
#
@router.callback_query(F.data.startswith('move'), ~StateFilter(FSMgame.move_human_from, FSMgame.move_human_to))
async def process_move2_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()


#
@router.callback_query(F.data=='let_AI_move', StateFilter(FSMgame.move_AI))
async def process_move_AI_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    side = data['side']
    reply_markup = create_kb_8_8(move='AI', side=side)

    for i in range(1, 4):
        caption = TEXTS_RU['AI_move_label'] + '..' * i
        await callback.message.edit_caption(caption=caption,
                                            reply_markup=reply_markup)
        sleep(1)
    
    data = await state.get_data()
    AI_engine = data['AI_engine']
    board = data['board']
    side = data['side']
    side_AI = data['side_AI']
    
    AI_move = get_move_AI(AI_engine, board)
    board.push(AI_move)
    
    board_pic = get_board_pic(board, side)
    board_pic = FSInputFile(board_pic)
    reply_markup = create_kb_8_8(move='human', side=side)

    win_status = check_win(board)
    draw_status = check_draw(board)
        
    if win_status:
        text_lose = TEXTS_RU['checkmate'] + '\n' + TEXTS_RU['lose']
        logger.info('Game finished with AI"s win')
        await callback.message.answer(text=text_lose)
        await state.clear()
    elif draw_status:
        text_draw = TEXTS_RU[draw_status] + '\n' + TEXTS_RU['draw']
        logger.info('Game finished with draw')
        await callback.message.answer(text=text_draw)
        await state.clear()
    else:
        caption = TEXTS_RU['AI_move'] + str(AI_move) + '\n'
        
        check_status = check_check(board, side_AI)
        caption += check_status + TEXTS_RU[f'{side}_move']
    
        await state.update_data(board=board)
        await callback.message.edit_media(InputMediaPhoto(
                                                media=board_pic,
                                                caption=caption),
                                          reply_markup=reply_markup)
        await state.set_state(FSMgame.move_human_from)

#
@router.callback_query(F.data=='let_AI_move', ~StateFilter(FSMgame.move_AI))
async def process_move2_AI_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
# EOF

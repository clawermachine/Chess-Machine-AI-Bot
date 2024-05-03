import chess
import chess.svg
import os
import io
import cairosvg
import json
from PIL import Image

from board.positions import positions

#
def _search_pic(position: str, side: str) -> str | bool:
    key = position + '_' + side
    if key in positions.keys():
        return positions[key]
    else:
        return None
#
def _add_pic(position, side, filename_pic):
    file_path = 'board/positions.py'
    # Открываем файл для чтения и записи
    with open(file_path, 'r+') as file:
        dictionary = dict()

        heading = file.readline()
        for string in file:
            # считываем
            if string.rstrip() != '}':
                k, v = string.rstrip().split(':')
                dictionary[k.strip("'")] = v.strip(",'")
            else:
                break

        key = position + '_' + side
        # Обновляем словарь новым ключом и значением
        dictionary[key] = filename_pic

        # Устанавливаем указатель файла в начало
        file.seek(0)

        # Записываем обновленный словарь обратно в файл
        file.write(heading)
        count = 1
        for k, v in dictionary.items():
            if count != len(dictionary):
                file.write("'" + k + "':'" + v + "',\n")
            else:
                file.write("'" + k + "':'" + v + "'\n")
            count += 1
        file.write('}\n#EOF')
        
        # Обрезаем файл до размера, соответствующего записанному объекту
        file.truncate()

#
def _get_position_from_fen(fen: str) -> str:
    position = fen.split()[0].replace('/', '_')
    return position

#
def _board2svg(board: chess.Board, position: str, side: str) -> str:

    if side == 'white':
        side_svg = chess.WHITE
    elif side == 'black':
        side_svg = chess.BLACK

    boardsvg = chess.svg.board(board=board, orientation=side_svg)
        
    filename = 'board/pics/' + position + '_' + side + '.SVG'
    with open(filename, 'w') as f:
        f.write(boardsvg)


# converting svg to png or webp and saving as file
def _svg2image(position, side, new_width=1000, new_height=1000,
                 frmt='png', quality=100) -> str:
    filename_svg = 'board/pics/' + position + '_' + side + '.svg'
    filename_pic = 'board/pics/' + position + '_' + side + '.' + frmt
    
    with open(filename_svg, 'rb') as f:
        svg_data = f.read()

    # Render SVG to PNG in memory
    png_data = cairosvg.svg2png(bytestring=svg_data)

    # Convert PNG to Image
    with Image.open(io.BytesIO(png_data)) as img:
        # Resize the image
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save in the desired format
        if frmt == 'webp':
            img.save(filename_pic, 'WEBP', quality=quality)
        elif frmt == 'png':
            img.save(filename_pic, 'PNG', quality=quality)
        else:
            raise ValueError('Wrong format.')

    os.remove(filename_svg)
    _add_pic(position, side, filename_pic)


#
def get_board_pic(board: chess.Board, side: str) -> str:
    fen = board.fen()
    position = _get_position_from_fen(fen)
    search_result = _search_pic(position, side)
    
    if search_result:
        return search_result
    else:
        _board2svg(board, position, side)
        _svg2image(position, side)

        with open('board/positions.py', 'r') as file:
            data = file.read()
            # Извлекаем словарь из строки данных
            exec(data, globals())
    
    search_result = _search_pic(position, side)
    
    return search_result

        









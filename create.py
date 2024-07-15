import os
from pyshortcuts import make_shortcut
import sys

def create_desktop_shortcut():
    # Diretório onde o script create_shortcut.py está localizado
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # Caminho para o arquivo main.py
    main_file = os.path.join(current_dir, 'main.py')

    is_windows = sys.platform.startswith('win')
    if is_windows:
        executable = 'pythonw'
    else:
        executable = 'python3'

    # Criar atalho na área de trabalho
    make_shortcut(main_file, name='ytdlp-ui', description='Executa uma interface básica para usar yt-dlp', icon='ytdlp.ico', terminal=False, executable=executable, working_dir=current_dir)

    print('''--------------------------------------------------------------------------------------
    \n ------------------------ ytdlp-ui shortchut added to desktop ------------------------
    \n--------------------------------------------------------------------------------------
    \n ************************ If doesn't work, run python main.py ************************''')

if __name__ == '__main__':
    create_desktop_shortcut()

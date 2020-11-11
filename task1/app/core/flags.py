import os
import shutil

EASY_FLAG_NAME = os.environ.get('EASY_FLAG_NAME', 'catch_me')
EASY_FLAG_CONTENT = os.environ.get('EASY_FLAG_CONTENT', 'bit{easy_flag_content}')
HARD_FLAG_NAME = os.environ.get('HARD_FLAG_NAME', 'you cannot catch me')
HARD_FLAG_CONTENT = os.environ.get('HARD_FLAG_CONTENT', 'bit{medium_flag_content}')

def create_flags():
    if not os.path.isdir('./flags'):
        os.makedirs('./flags')

    if not os.path.exists(f'/tmp/{EASY_FLAG_NAME}'):
        with open(f'/tmp/{EASY_FLAG_NAME}', 'w+') as f:
            f.write(EASY_FLAG_CONTENT)
        shutil.move(f'/tmp/{EASY_FLAG_NAME}', f'flags/{EASY_FLAG_NAME}')

    if not os.path.exists(f'/tmp/{HARD_FLAG_NAME}'):
        with open(f'/tmp/{HARD_FLAG_NAME}', 'w+') as f:
            f.write(HARD_FLAG_CONTENT)
        shutil.move(f'/tmp/{HARD_FLAG_NAME}', f'flags/{HARD_FLAG_NAME}')
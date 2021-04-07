import socket, pickle
import time


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


s = socket.socket()
s.connect(('109.251.157.178', 5001))
print('connected')
sch = [0, 0]
print(f'the score {sch}')
with open('log.log', 'w') as f:
    f.write('START')
try:
    while 1:
        time.sleep(0.3)
        data = int_from_bytes(s.recv(1))
        with open('log.log', 'a') as f:
            f.write('\nPING 1\n')
            f.write(str(data))
        if data == 0:
            print('You lose turn')
            ch = int_from_bytes(s.recv(1))
            with open('log.log', 'a') as f:
                f.write('\nPING 2')
            if ch == 0:
                print('You wasn\'t chosen')
                sch[1] += 1
            else:
                print('You was chosen')
                sch[0] += 1
            print(f'the score {sch}')
            '''
            t = s.recv(128)
            s.sendall(t)
            t = pickle.loads(t)
            print(t)
            if (t[0] != sch[1]) or (t[1] != sch[0]):
                with open('log.log', 'a') as f:
                    f.write('\nERROR 1')'''
            with open('log.log', 'a') as f:
                f.write('\nPING 3')
        else:
            while 1:
                try:
                    inp = int(input('You won turn. Choose yourself(1) or your opponent(0)'))
                except Exception:
                    print('you can choose only 0/1')
                    continue
                if inp == 1:
                    sch[0] += 1
                    s.sendall(int_to_bytes(0))
                    with open('log.log', 'a') as f:
                        f.write('\nOK 1')
                    break
                elif inp == 0:
                    sch[1] += 1
                    s.sendall(int_to_bytes(1))
                    with open('log.log', 'a') as f:
                        f.write('\nOK 2')
                    break
                else:
                    print('you can choose only 0/1')
            # s.sendall(pickle.dumps(sch))
            with open('log.log', 'a') as f:
                f.write('\nOK 3')
            print(f'the score {sch}')
        superfun()
        print(f'Calculating...\nThe score {sch}')
        if sch[0] >= 25:
            print('You win')
            break
        if sch[1] >= 25:
            print('You lose')
            break
except KeyboardInterrupt:
    s.close()

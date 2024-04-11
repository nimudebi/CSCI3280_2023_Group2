import socket
import tqdm
import os

SEPARATOR=""

host="192.168.99.1"
port=7777

BUFFER_SIZE = 4096

filename=""

file_size=os.path.getsize(filename)

s=socket.socket()
s.connect((host,port))

s.send(f"{filename}{SEPARATOR}{file_size}".encode())
#进度条
progress = tqdm.tqdm(range(file_size),f"send {filename}",unit="B",unit_divisor=1024)
with open(filename,"rb") as f:
    for _ in progress:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        s.sendall(bytes_read)
        # 更新进度条
        progress.update(len(bytes_read))

s.close()
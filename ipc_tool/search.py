# coding: utf-8
import socket
import ctypes

multicast_group = '238.238.238.238'
port = 8888


class gsf_user_t(ctypes.Structure):
    _fields_ = [
        ("name", ctypes.c_char * 32),
        ("pwd", ctypes.c_char * 32),
        ("caps", ctypes.c_uint64),
    ]


class gsf_msg_t(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("ver", ctypes.c_short),
        ("id", ctypes.c_short),
        ("ch", ctypes.c_char),
        ("set", ctypes.c_char),
        ("sid", ctypes.c_char),
        ("nsave", ctypes.c_char),
        ("ts", ctypes.c_uint64),
        ("err", ctypes.c_int),
        ("size", ctypes.c_int),
        ("data", ctypes.c_char * 0),
    ]


class gsf_sadp_msg_t(ctypes.Structure):
    _fields_ = [
        ("ver", ctypes.c_short),
        ("modid", ctypes.c_short),
        ("devid", ctypes.c_int),
        ("user", gsf_user_t),
        ("msg", gsf_msg_t),
    ]


class gsf_base_t(ctypes.Structure):
    _fields_ = [
        ("name", ctypes.c_char * 32),
        ("language", ctypes.c_int),
        ("zone", ctypes.c_int),
        ("mcastdev", ctypes.c_char * 32),
    ]


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 设置套接字选项，允许发送组播消息
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)


msg = gsf_sadp_msg_t()
msg.ver = 1
msg.modid = 0
msg.devid = 0
msg.user.name = b"admin"
msg.user.pwd = b"admin"
msg.user.caps = 0xFFFFFFFFFFFFFFFF
msg.msg.ver = 1
msg.msg.id = 8
msg.msg.ch = 0
msg.msg.set = 0
msg.msg.sid = 0
msg.msg.nsave = 0
msg.msg.ts = 0
msg.msg.err = 0
msg.msg.size = 0
msg_bytes = ctypes.string_at(ctypes.byref(msg), ctypes.sizeof(msg))
sock.sendto(msg_bytes, (multicast_group, port))

sock.settimeout(2)
while True:
    try:
        # 设置超时时间为5秒
        data, address = sock.recvfrom(1024)
        msg_size = ctypes.sizeof(gsf_msg_t)
        out_msg = gsf_msg_t.from_buffer_copy(data[:msg_size])
        print(f'msg_size: {msg_size}')
        print(f"out_msg.ver: {out_msg.ver}")
        print(f'out_msg.size: {out_msg.size}')
        print(f'out_msg.err: {out_msg.err}')
        if out_msg.err == 0 and out_msg.size == ctypes.sizeof(gsf_base_t) and out_msg.size == len(data[msg_size:]):
            base = gsf_base_t.from_buffer_copy(data[msg_size:])
            print(f'base.name: {base.name}')
            print(f'base.language: {base.language}')
            print(f'base.zone: {base.zone}')
            print(f'base.mcastdev: {base.mcastdev}')
        print(f'Received message from {address}')
    except socket.timeout:
        print('receive complete')
        break

sock.close()

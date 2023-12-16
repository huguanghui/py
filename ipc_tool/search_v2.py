# coding: utf-8
import socket
import ctypes


def search_devices():
    multicast_group = "238.238.238.238"
    port = 8080

    class gsf_search_t(ctypes.Structure):
        _fields_ = [
            ("data", ctypes.c_uint8 * 2),
        ]

    class sadp_dev_info_t(ctypes.Structure):
        _fields_ = [
            ("type", ctypes.c_int),
            ("soft_ver", ctypes.c_char * 24),
            ("hard_ver", ctypes.c_char * 24),
            ("sn", ctypes.c_char * 64),
            ("mac", ctypes.c_char * 6),
        ]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    gsf_search = gsf_search_t()
    gsf_search.data[0] = 0xBE
    gsf_search.data[1] = 0xEF
    msg_bytes = ctypes.string_at(ctypes.byref(gsf_search), ctypes.sizeof(gsf_search))
    sock.sendto(msg_bytes, (multicast_group, port))
    sock.settimeout(3)
    devices = []
    while True:
        try:
            data, address = sock.recvfrom(1024)
            msg_size = ctypes.sizeof(sadp_dev_info_t)
            if len(data) >= msg_size:
                out_msg = sadp_dev_info_t.from_buffer_copy(data[:msg_size])
                device = {
                    "type": hex(out_msg.type),
                    "soft_ver": out_msg.soft_ver.decode(),
                    "hard_ver": out_msg.hard_ver.decode(),
                    "sn": out_msg.sn.decode(),
                    "mac": ":".join("{:02x}".format(byte) for byte in out_msg.mac),
                }
                devices.append(device)
            print(f"Received message from {address}")
        except socket.timeout:
            print("receive complete")
            break
    sock.close()
    return devices


if __name__ == "__main__":
    dev_lists = search_devices()
    print(dev_lists)

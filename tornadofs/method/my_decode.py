# coding=utf-8
from math import sqrt
from base64 import b64encode, b64decode

def func_x(x):
    return x**2 + x + 7


def get_x(x):
    a = 1
    b = 1
    c = 7 - x
    x1 = (-b + sqrt(b**2 - 4 * a * c)) / (2 * a)
    x2 = (-b - sqrt(b**2 - 4 * a * c)) / (2 * a)

    if x1 > 0:
        return x1
    else:
        return x2


def ord_encode(ori_str):
    result = ''
    for i in ori_str:
        temp = func_x(int(ord(i)))
        print(i, temp)
        result += "%0.5d" % temp
        result += chr(int(temp))
    return result


def ord_decode(encoded_str):
    result = ''
    for i in range(len(encoded_str) // 5):
        data = encoded_str[i * 5:(i+1) * 5]
        print("decode:", i, data)
        data = int("".join(data))
        ord_str = get_x(data)
        result += chr(int(ord_str))
    return result


def ord_encode_ch(ori_str):
    result = ''
    for i in ori_str:
        temp = func_x(int(ord(i)))
        print(i, temp, int(ord(i)))
        result += "%0.10d" % temp
    return result


def ord_decode_cn(encoded_str):
    result = ''
    for i in range(len(encoded_str) // 10):
        data = encoded_str[i * 10:(i+1) * 10]
        print("decode:", i, data)
        data = int("".join(data))
        ord_str = get_x(data)
        result += chr(int(ord_str))
    return result


def self_encode(ori_str):
    result = ''
    if isinstance(ori_str, bytes):
        ori_str = ori_str.decode()
    for i in ori_str:
        temp = func_x(int(ord(i)))
        # print(i, temp)
        result += chr(int(temp))
    # print(result)
    return b64encode(result.encode())


def self_decode(encoded_str):
    if isinstance(encoded_str, bytes):
        encoded_str = b64decode(encoded_str).decode()
    elif isinstance(encoded_str, str):
        bstr = encoded_str.encode()
        encoded_str = b64decode(bstr).decode()
    result = ''
    for i in encoded_str:

        data = int(ord(i))
        ord_str = get_x(data)
        result += chr(int(ord_str))
    return result


if __name__ == "__main__":
    # a = ord_encode("slkdf!@#$%^&*()_+=-`~")
    # print(a)
    # b = ord_decode(a)
    # print(b)
    #
    # a_ch = ord_encode_ch("中文 sdff+ _")
    # b_ch = ord_decode_cn(a_ch)
    # print(a_ch)
    # print(b_ch)

    # sn = ord_encode("123456789az_")
    # print(sn)
    s_a = self_encode("1234")
    print(s_a.decode('utf-8'))
    s_b = self_decode(s_a)

    print(s_b)


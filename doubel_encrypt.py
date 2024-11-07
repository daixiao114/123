import tkinter as tk
from tkinter import messagebox

# S-AES相关函数定义（保持不变）
# S-AES相关函数定义
S = [[9, 4, 10, 11],
     [13, 1, 8, 5],
     [6, 2, 0, 3],
     [12, 14, 15, 7]]

IS = [[10, 5, 9, 11],
      [1, 7, 8, 15],
      [6, 0, 2, 3],
      [12, 4, 13, 14]]

RCON1 = '10000000'
RCON2 = '00110000'


def XOR(bits1, bits2):
    return ''.join(str(int(b1) ^ int(b2)) for b1, b2 in zip(bits1, bits2))


def AddRoundKey(bits1, bits2):
    return XOR(bits1, bits2)


def SubNib(bits):
    new = ''
    for i in range(0, len(bits), 4):
        row = int(bits[i:i + 2], 2)
        col = int(bits[i + 2:i + 4], 2)
        new += f'{S[row][col]:04b}'
    return new


def InvSubNib(bits):
    new = ''
    for i in range(0, len(bits), 4):
        row = int(bits[i:i + 2], 2)
        col = int(bits[i + 2:i + 4], 2)
        new += f'{IS[row][col]:04b}'
    return new


def ShiftRows(bits):
    return bits[0:4] + bits[12:16] + bits[8:12] + bits[4:8]


def RotNib(bits):
    return bits[4:8] + bits[0:4]


def GF(a, b):
    mul_table = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        [0, 2, 4, 6, 8, 10, 12, 14, 3, 1, 7, 5, 11, 9, 15, 13],
        [0, 3, 6, 5, 12, 15, 10, 9, 11, 8, 13, 14, 7, 4, 1, 2],
        [0, 4, 8, 12, 3, 7, 11, 15, 6, 2, 14, 10, 5, 1, 13, 9],
        [0, 5, 10, 15, 7, 2, 13, 8, 14, 11, 4, 1, 9, 12, 3, 6],
        [0, 6, 12, 10, 11, 13, 7, 1, 5, 3, 9, 15, 14, 8, 2, 4],
        [0, 7, 14, 9, 15, 8, 1, 6, 13, 10, 3, 4, 2, 5, 12, 11],
        [0, 8, 3, 11, 6, 14, 5, 13, 12, 4, 15, 7, 10, 2, 9, 1],
        [0, 9, 1, 8, 2, 11, 3, 10, 4, 13, 5, 12, 6, 15, 7, 14],
        [0, 10, 7, 13, 14, 4, 9, 3, 15, 5, 8, 2, 1, 11, 6, 12],
        [0, 11, 5, 14, 10, 1, 15, 4, 7, 12, 2, 9, 13, 6, 8, 3],
        [0, 12, 11, 7, 5, 9, 14, 2, 10, 6, 1, 13, 15, 3, 4, 8],
        [0, 13, 9, 4, 1, 12, 8, 5, 2, 15, 11, 6, 3, 14, 10, 7],
        [0, 14, 15, 1, 13, 3, 2, 12, 9, 7, 6, 8, 4, 10, 11, 5],
        [0, 15, 13, 2, 9, 6, 4, 11, 1, 14, 12, 3, 8, 7, 5, 10]
    ]
    result_int = mul_table[int(a, 2)][int(b, 2)]
    return f'{result_int:04b}'


def MixColumns(bits):
    new = XOR(bits[0:4], GF('0100', bits[4:8])) + XOR(GF('0100', bits[0:4]), bits[4:8]) + \
          XOR(bits[8:12], GF('0100', bits[12:16])) + \
          XOR(GF('0100', bits[8:12]), bits[12:16])
    return new


def InvMixColumns(bits):
    new = XOR(GF('1001', bits[0:4]), GF('0010', bits[4:8])) + XOR(GF('0010', bits[0:4]), GF('1001', bits[4:8])) + XOR(
        GF('1001', bits[8:12]), GF('0010', bits[12:16])) + XOR(GF('0010', bits[8:12]), GF('1001', bits[12:16]))
    return new


def KeyExpansion(key):
    [w0, w1] = [key[0:8], key[8:16]]
    w2 = XOR(w0, XOR(RCON1, SubNib(RotNib(w1))))
    w3 = XOR(w2, w1)
    w4 = XOR(w2, XOR(RCON2, SubNib(RotNib(w3))))
    w5 = XOR(w4, w3)
    return [w0 + w1, w2 + w3, w4 + w5]


def Encrypt(plain_text, key):
    expanded_key = KeyExpansion(key)
    cipher_text = AddRoundKey(plain_text, expanded_key[0])
    cipher_text = SubNib(cipher_text)
    cipher_text = ShiftRows(cipher_text)
    cipher_text = MixColumns(cipher_text)
    cipher_text = AddRoundKey(cipher_text, expanded_key[1])
    cipher_text = SubNib(cipher_text)
    cipher_text = ShiftRows(cipher_text)
    cipher_text = AddRoundKey(cipher_text, expanded_key[2])
    return cipher_text


def Decrypt(cipher_text, key):
    expanded_key = KeyExpansion(key)
    plain_text = AddRoundKey(cipher_text, expanded_key[2])
    plain_text = ShiftRows(plain_text)
    plain_text = InvSubNib(plain_text)
    plain_text = AddRoundKey(plain_text, expanded_key[1])
    plain_text = InvMixColumns(plain_text)
    plain_text = ShiftRows(plain_text)
    plain_text = InvSubNib(plain_text)
    plain_text = AddRoundKey(plain_text, expanded_key[0])
    return plain_text


# 辅助函数
def ascii_to_binary(ascii_text):
    binary_text = ''
    for char in ascii_text:
        binary_char = bin(ord(char))[2:].zfill(8)
        binary_text += binary_char
    return binary_text


def binary_to_ascii(binary_text):
    ascii_text = ''
    for i in range(0, len(binary_text), 8):
        ascii_char = chr(int(binary_text[i:i + 8], 2))
        ascii_text += ascii_char
    return ascii_text


def ascii_encrypt(plain_text, key):
    encrypted_text = ''
    for i in range(0, len(plain_text), 2):
        # 获取两个字符
        block = plain_text[i:i + 2]
        # 如果块不足两个字符，则直接添加到结果中
        if len(block) < 2:
            encrypted_text += block
            break
        # 将块转换为16位二进制
        binary_block = ascii_to_binary(block)
        # 加密二进制块
        encrypted_block = Encrypt(binary_block, key)
        # 将加密后的二进制转换回ASCII字符
        encrypted_chars = binary_to_ascii(encrypted_block)
        encrypted_text += encrypted_chars
    return encrypted_text


def ascii_decrypt(cipher_text, key):
    decrypted_text = ''
    for i in range(0, len(cipher_text), 2):
        # 获取两个字符
        block = cipher_text[i:i + 2]
        # 如果块不足两个字符，则直接添加到结果中
        if len(block) < 2:
            decrypted_text += block
            break
        # 将块转换为16位二进制
        binary_block = ascii_to_binary(block)
        # 解密二进制块
        decrypted_block = Decrypt(binary_block, key)
        # 将解密后的二进制转换回ASCII字符
        decrypted_chars = binary_to_ascii(decrypted_block)
        decrypted_text += decrypted_chars
    return decrypted_text


# 双重加密函数
def DoubleEncrypt(plain_text, key):
    key1 = key[:16]
    key2 = key[16:]
    cipher_text = Encrypt(plain_text, key1)
    cipher_text = Encrypt(cipher_text, key2)
    return cipher_text


def DoubleDecrypt(cipher_text, key):
    key2 = key[16:]
    key1 = key[:16]
    plain_text = Decrypt(cipher_text, key2)
    plain_text = Decrypt(plain_text, key1)
    return plain_text


# 更新辅助函数以支持双重加密
def ascii_double_encrypt(plain_text, key):
    encrypted_text = ''
    for i in range(0, len(plain_text), 2):
        block = plain_text[i:i + 2]
        if len(block) < 2:
            encrypted_text += block
            break
        binary_block = ascii_to_binary(block)
        encrypted_block = DoubleEncrypt(binary_block, key)
        encrypted_chars = binary_to_ascii(encrypted_block)
        encrypted_text += encrypted_chars
    return encrypted_text


def ascii_double_decrypt(cipher_text, key):
    decrypted_text = ''
    for i in range(0, len(cipher_text), 2):
        block = cipher_text[i:i + 2]
        if len(block) < 2:
            decrypted_text += block
            break
        binary_block = ascii_to_binary(block)
        decrypted_block = DoubleDecrypt(binary_block, key)
        decrypted_chars = binary_to_ascii(decrypted_block)
        decrypted_text += decrypted_chars
    return decrypted_text


# 更新GUI部分
def validate_key(input_str, double_encryption=False):
    if double_encryption:
        return all(c in '01' for c in input_str) and len(input_str) == 32
    else:
        return all(c in '01' for c in input_str) and len(input_str) == 16


def show_encrypt_result():
    plaintext = plaintext_var.get()
    key = key_var.get()
    if double_encryption_var.get() == 1:
        if not validate_key(key, True):
            messagebox.showerror("Input Error", "Key must be a 32-bit binary string for double encryption.")
            return
        ciphertext = ascii_double_encrypt(plaintext, key)
    else:
        if not validate_key(key, False):
            messagebox.showerror("Input Error", "Key must be a 16-bit binary string for single encryption.")
            return
        ciphertext = ascii_encrypt(plaintext, key)
    ciphertext_var.set(ciphertext)


def show_decrypt_result():
    ciphertext = ciphertext_var.get()
    key = key_var.get()
    if double_encryption_var.get() == 1:
        if not validate_key(key, True):
            messagebox.showerror("Input Error", "Key must be a 32-bit binary string for double encryption.")
            return
        plaintext = ascii_double_decrypt(ciphertext, key)
    else:
        if not validate_key(key, False):
            messagebox.showerror("Input Error", "Key must be a 16-bit binary string for single encryption.")
            return
        plaintext = ascii_decrypt(ciphertext, key)
    plaintext_var.set(plaintext)


# 创建主窗口
root = tk.Tk()
root.title("S-AES Encryption/Decryption Tool with ASCII Support and Double Encryption")

# 设置变量
plaintext_var = tk.StringVar()
key_var = tk.StringVar()
ciphertext_var = tk.StringVar()
double_encryption_var = tk.IntVar()

# GUI组件
tk.Label(root, text="Plaintext (ASCII):").pack()
tk.Entry(root, textvariable=plaintext_var).pack()
tk.Label(root, text="Key (16 bits for single, 32 bits for double encryption):").pack()
tk.Entry(root, textvariable=key_var).pack()
tk.Checkbutton(root, text="Use Double Encryption", variable=double_encryption_var).pack()
tk.Button(root, text="Encrypt", command=show_encrypt_result).pack()
tk.Label(root, text="Ciphertext (ASCII):").pack()
tk.Entry(root, textvariable=ciphertext_var, state='readonly').pack()
tk.Button(root, text="Decrypt", command=show_decrypt_result).pack()

# 运行主循环
root.mainloop()

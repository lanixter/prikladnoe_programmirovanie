import sys


def decrypt(encrypted_text):
    result = []
    i = 0
    length = len(encrypted_text)

    while i < length:
        if encrypted_text[i] == '.' and i + 1 < length and encrypted_text[i + 1] == '.':
            if result:
                result.pop()
            i += 2
        elif encrypted_text[i] == '.':
            i += 1
        else:
            result.append(encrypted_text[i])
            i += 1

    return ''.join(result)


if __name__ == '__main__':
    data = sys.stdin.read().strip()
    decrypted = decrypt(data)
    print(decrypted)
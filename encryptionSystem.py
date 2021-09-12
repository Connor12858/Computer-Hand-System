from cryptography.fernet import Fernet


def generate_key():
    key = Fernet.generate_key()
    with open("data\\secret.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    return open("data\\secret.key", "rb").read()


def encrypt_message(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)

    return encrypted_message.decode()


def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    encrypted_message = encrypted_message.encode()
    decrypted_message = f.decrypt(encrypted_message)

    return decrypted_message.decode()

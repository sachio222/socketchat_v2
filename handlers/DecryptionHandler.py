from handlers.routers import DecryptionCmds

def message_router(data_dict: dict) -> tuple:
    sender = data_dict["sender"]
    cipher = data_dict["cipher"]
    cipher_text = data_dict["msg_pack"]["cipher_text"]

    func = DecryptionCmds.cipher_dict.get(cipher, DecryptionCmds.goober)
    try:
        plain_text = func(cipher_text).decode()
    except Exception as e:
        print(e)
        # In case of wrong key, return cipher text
        plain_text = cipher_text
    return sender, plain_text
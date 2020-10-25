from chatutils import utils
import config.filepaths as paths

configs = utils.JSONLoader()
users = utils.JSONLoader(paths.user_dict_path)


def get_keys(sender_nick: str) -> str:
    """Get's trusted user's key."""
    users.reload()
    pub_key_sender = None
    pub_key_recip = None
    ver_key_sender = None
    ver_key_recip = None

    for user in users.dict.keys():
        if user != sender_nick:
            pub_key_recip = users.dict[user]["public_key"]
            ver_key_recip = users.dict[user]["verify_key"]
        elif user == sender_nick:
            pub_key_sender = users.dict[user]["public_key"]
            ver_key_sender = users.dict[user]["verify_key"]

    return pub_key_sender, pub_key_recip, ver_key_sender, ver_key_recip

from chatutils import utils

class Router:
    def __init__(self):
        pass

    def about(self, *args, **kwargs):
        """Read from file in config folder."""
        print(args)
        path = 'config/about.txt'
        utils.print_from_file(path)

    def help(self, *args, **kwargs):
        """Read from file in config folder."""
        path = 'config/help.txt'
        utils.print_from_file(path)

    def sendfile(self, *args, **kwargs):
        """Initiates Send File (SF) sequence."""
        self.start_sendfile_process(sock)

    def sendkey(self, *args, **kwargs):
        pass

    def status(self, *args, **kwargs):
        """Ask SERVER to broadcast who is online.
        Join and strip. Send over full string.
        """
        msg = ' '.join(msg)
        msg = msg[1:]
        self.pack_n_send(sock, '/', msg)

    def mute(self, *args, **kwargs):
        cfg.muted = True
        self.print_message("@YO: Muted. Type /unmute to restore sound.")
    
    def trust(self, *args, **kwargs):
        self.trust(msg_parts)

    def unmute(self, *args, **kwargs):
        cfg.muted = False
        self.print_message("@YO: B00P! Type /mute to turn off sound.")
    
    cmd_dict = {
        '/about': about,
        '/help': help,
        '/h': help,
        '/sendfile': sendfile,
        '/sendkey': sendkey,
        '/status': status,
        '/mute': mute,
        '/trust': trust,
        '/unmute': unmute
    }
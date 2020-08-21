import os
import time
from . import utils
from .chatio import ChatIO


class FileXfer(ChatIO):
    """FileXfer 2.0 - For file transfer, sending and receiving.
    
    A utility class that facilitates file transfer between 2 clients. The send
    file process involves several steps of data being sent back and forth be-
    tween three end points, the sender, the server and the recipient.
    """

    def __init__(self):
        super(FileXfer, self).__init__()
        self.filesize = None

    def sender_prompt(self, path=''):
        """Sendfile 1 (SF1): Ask SENDER what file they would like to send.

        Prompt SENDER what file they want to send, and confirm that it exists
        in the location state. The default file location is the relative root.

        Args
            path - (str) The path of the file to send.

        Returns
            path - (str) Path of the confirmed file or None if nonexistant.
            filesize - (int) The size of the file in bytes.
        """
        while not path:

            # Get filepath and filesize.
            path, filename, filesize = self._get_file_info(path)

            if not path:
                break

            print(f'OK! Found: {filename} | {filesize}bytes')

        return path, filename, filesize

    def user_prompt(self, sock, mtype: str = 'U', user=''):

        while not user:
            user = self.get_username(sock, mtype, user='')

            if not user:
                break

        return user


    def recip_prompt(self, sock, path, filename=None, filesize=None, user=None):
        """Sends filename and filesize. Prompts user to accept file transfer.
        
        Args:
            filename: (str) The name of the incoming file.
            filesize: (int) Size of incoming file in bytes.
        """

        print('OK! Waiting for user to accept...')

        msg = f'User sending {filename} | {filesize} bytes\n-?- Do you want to accept this file? (Y/N)'
        # Send as A type so message is routed to recip.
        # TODO: Make so it routes only to Recip!
        self.pack_n_send(sock, 'F', msg)

    def _get_file_info(self, path=''):
        """Validate if selected file exists, and get filesize.

        Input:
            path: (string) a file location.

        Returns:
            path: (str or path??) a path to an existing file.
            filesize: (int) bytes of file at path
        """

        filesize = None

        print("-=- Send file to recipient (or type cancel).")
        while not os.path.exists(path):
            path = input("-=- Input filepath >> ")

            if self._user_did_cancel(path):
                path = None
                filename = None
                break

            elif not os.path.exists(path):
                print("x-x File or path doesn't exist. Check yer work, bud.")

            else:
                # remove absolute path if there is one
                try:
                    path = os.path.abspath(path)
                    print('path is:', path)
                    filename = os.path.basename(path)
                    print('filename is:', filename)
                    filesize = os.path.getsize(path)
                    # filesize = 748
                    print('filesize is: ', filesize)
                except:
                    print("-!- File should be in your project root.")
        return path, filename, filesize

    def get_username(self, sock, mtype: str = 'U', user=''):
        """ Returns valid recipient for file send."""

        while not user:
            user = input('-=- Send to >> @')

            if self._user_did_cancel(user):
                user = ''
                break
            
            self.pack_n_send(sock, mtype, user)

        return user

    def _user_did_cancel(self, inp_str):
        """Returns true if inp_str is cancelled, and shows message. """

        if inp_str.lower() == 'cancel':
            print('x-x Send file cancelled. Continue chatting.')
            return True

        else:
            return False

    def file_xfer(self, sock, path, filename, filesize, recip=''):

        file_info = f'{str(filesize)}::{filename}'

        try:
            with open(path, 'rb') as f:
                self.pack_n_send(sock, 'X', str(file_info))
                sock.sendfile(f, 0)
        except:
            print('Unknown exception. I dunno whut u did.')

    def new_path(self, path, download_folder='downloads/'):
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        if os.path.exists(download_folder + path):
            main, ext = utils.split_path_ext(path)
            path = f"{main}_copy.{ext}"
        path = download_folder + path
        return path

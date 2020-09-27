"""A complex process that communicates between SERVER and 2 CLIENTS

Steps to send a file with recipient and confirmation.

1. CLIENT1: Wishes to send file.
/sendfile -> sendfile_process...
2. LOCAL CHANNEL: Asks for file to send.
xfer.sender_prompt() -> bool
3. LOCAL CHANNEL: Asks for recipient.
xfer.user_prompt() -> xfer.get_username() -> sends U-type (user) message->
4. SERVER: Receives U-type message.
_serv_u_handler() -> lookup_user() -> sends bool as U-type reply to CLIENT1 ->
5. CLIENT1: Receives U-type message.
_u_handler() false ? -> U-type loop to SERVER | true ? xfer.recip_prompt(path, fn) -> CHANNEL
6. LOCAL CHANNEL: Prints User Found, Sends fileinfo and accept prompt to CLIENT 2
xfer.recip_prompt(path, fn) -> F-type (file) prompt - SERVER
7. SERVER: Receives F-type message.
_serv_f_handler() -> Prompt with file info as F-type msg -> CLIENT2
8. CLIENT2: Prompt if wish to accept?
_f_handler() -> Shows prompt, waits for answer as A-type (answer) -> 
9. SERVER: Receives A-type message.
_serv_a_handler() -> invalid? Loopback as F-type : valid? Routes A-type -> CLIENT1 as A-type msg ->
10. CLIENT1: receives A-type message. Tells if accepted or rejected.
_a_handler() -> 'n' ? break : 'y' ? xfer.file_xfer() -> Send as X-type (Xfer) -> SERVER
11. SERVER: Receives X-type message.
_serv_x_handler() -> transfers open buffer from CLIENT1 to CLIENT2
12. CLIENT2: receives X-type message. File downloads
x_handler() -> write file. -> print msg receipt as M-type (message). 
Done."""

#===========================================================#


def sender_logging(func):

    def logging_wrapper(*args, **kwargs):
        print(f'SND: <{func.__name__}> ', end="")
        result = func(*args, **kwargs)
        return result

    return logging_wrapper


def server_logging(func):

    def logging_wrapper(*args, **kwargs):
        print(f'SRV: <{func.__name__}> ', end="")
        result = func(*args, **kwargs)
        return result

    return logging_wrapper


def recip_logging(func):

    def logging_wrapper(*args, **kwargs):
        print(f'RCP: <{func.__name__}> ', end="")
        result = func(*args, **kwargs)
        return result

    return logging_wrapper


def local_logging(func):

    def logging_wrapper(*args, **kwargs):
        print(f'LCL: <{func.__name__}> ', end="")
        result = func(*args, **kwargs)
        return result

    return logging_wrapper


#===========================================================#


class SenderOperations():

    def __init__(self):
        """1. Show prompts. """
        # self.show_prompts()
        pass

    def show_prompts(self, sock):
        ### 0-------- Called by Sender
        fn, fs = self._what_is_filename()
        sn = self._what_is_username()
        user_accept = self.ask_server_if_user_exists(sn)
        if user_accept:
            ### -------> Outbound to Server
            print(sock)
            # SOCK.send()

            ServerOperations().ask_recip_to_accept(sn, fn, fs)

    @sender_logging
    def _what_is_filename(self):
        """2. Ask for filename. """
        found = False

        while not found:
            prompt = "-?- What file to send -> "
            fn = self._input(prompt)
            found = FileTools().does_file_exist(fn)
        fs = FileTools().what_is_filesize(fn)
        return fn, fs

    @sender_logging
    def _what_is_username(self):
        """4. Ask for username"""
        prompt = "-?- Send to: "
        sn = self._input(prompt)
        return sn

    @sender_logging
    def ask_server_if_user_exists(self, sn):
        """5. Send screenname (sn) to  SERVER"""

        ### <------ Called from show_prompts
        print("//asking server to look up user...")

        ### -------> Outbound to Server
        response = ServerOperations().is_user_here(sn)

        if response == True:
            print(f"-=- Waiting for {sn} to accept file. Press A to abort.")
            return True

        else:
            print(f"{sn} not found. Try again.")
            return False

    @sender_logging
    def recv_recip_accept_response(self, choice):
        print(choice)
        if choice.lower() == "y":
            payload = "This is the message being sent. "
            self.send_file_to_server(payload)
        if choice.lower() == "n":
            print("Transfer cancelled by user")

    @sender_logging
    def send_file_to_server(self, payload):
        print("Sending {fn} | {fs} bytes...")
        ### -------> Outbound to Server
        ServerOperations().deliver_payload(payload)

    def _did_cancel(self):
        pass

    @staticmethod
    def _input(prompt):
        input_txt = input(prompt)
        return input_txt

    dispatch = {'cancel': _did_cancel}


#===========================================================#


class RecipOperations():

    def __init__(self):
        pass

    @recip_logging
    def send_recip_accept_response(self, string):
        ### <-------- Inbound from Server

        print(string, end="")
        choice = input("(Y/N)? ")

        if choice.lower() == "y":
            print("Send accepted.")
        elif choice.lower() == "n":
            print("Send cancelled.")
        else:
            choice = input("Please enter a valid choice (Y or N): ")
            return

        ### -------> Outbound to Server
        ServerOperations().deliver_accept_or_not_response(choice)

    @recip_logging
    def receiving_payload(self, payload):
        print("Saving payload.")
        print(payload)


#===========================================================#


class ServerOperations():

    def __init__(self):
        pass

    @server_logging
    def is_user_here(self, sn):
        """6. Lookup User."""
        # receive sn from SENDER
        if sn == sn:
            return True
        else:
            return False

    @server_logging
    def ask_recip_to_accept(self, sn, fn, fs):

        print("//sending accept prompt to recip...")
        SENDER = "Sender"
        string = f"{SENDER} wants to send you {fn} ({fs}bytes). Do you wish to accept? "

        ### --------> Outbound to Recip.
        RecipOperations().send_recip_accept_response(string)
        return string

    @server_logging
    def deliver_accept_or_not_response(self, choice):
        print("//passing response to sender...")
        ### -------> Outbound to Server
        SenderOperations().recv_recip_accept_response(choice)

    @server_logging
    def deliver_payload(self, payload):
        print("//sending payload...")

        ### ---------> Outbound to Recip
        RecipOperations().receiving_payload(payload)


#===========================================================#


class FileTools():

    def __init__(self):
        pass

    @local_logging
    def does_file_exist(self, fn):
        """3. Look for file to send. """
        if True:
            print(f"-=- {fn} found.")
            return True
        else:
            print(f"-!- {fn} not found. Try again")
            return False

    @local_logging
    def what_is_filesize(self, fn):
        """"""
        fs = 5000
        print(f"-=- {fs} bytes")
        return fs


#===========================================================#

if __name__ == "__main__":

    while True:
        msg = input("prompt -> ")

        if msg == '/sendfile':

            SenderOperations().show_prompts()

        elif msg == "break":
            print("Connection closed.")
            break
        else:
            print(f">> {msg}")

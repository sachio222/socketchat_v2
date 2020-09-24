class SenderOperations():
    def __init__(self):
        """1. Show prompts. """
        # self.show_prompts()
        pass
    
    def show_prompts(self):
        ### 0-------- Called by Sender
        fn, fs = self._what_is_filename()
        sn = self._what_is_username()
        user_accept = self.ask_server_if_user_exists(sn)
        if user_accept:
            ### -------> Outbound to Server
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

    dispatch = {
        'cancel': _did_cancel
    }

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

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

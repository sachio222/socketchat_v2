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

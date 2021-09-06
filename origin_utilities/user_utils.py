import getpass

def get_current_user():
    username = getpass.getuser()
    return username
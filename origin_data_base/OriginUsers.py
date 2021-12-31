class OriginUsers(object):

    @staticmethod
    def get_curr_user():
        import getpass
        username = getpass.getuser()
        return username
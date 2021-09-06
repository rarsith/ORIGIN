from _datetime import datetime

class OriginDateTime(object):
    def __init__(self):
        self.time_now = datetime.now()

    def return_time(self):
        return self.time_now.strftime("%H:%M")

    def return_date(self):
        return self.time_now.strftime("%Y-%m-%d")


import datetime

class toolbox:

    @staticmethod
    def get_date(datestring):
        date_patterns = ["%d/%m/%Y","%Y/%m/%d","%m/%d/%Y","%Y/%d/%m"]
        return toolbox.get_datetime(datestring,date_patterns).date()

    @staticmethod
    def get_time(timestring):
        time_patterns = ["%I:%M %p","%H:%M","%I:%M:%S %p","%H:%M:%S"]
        return toolbox.get_datetime(timestring,time_patterns).time()

    @staticmethod
    def get_datetime(dtstring,patterns):
        for pattern in patterns:
            try:
                return datetime.datetime.strptime(dtstring,pattern)
            except:
                pass
        raise ValueError('Invalid datetime string.')

# coding=utf-8
from datetime import datetime, date, timedelta
from functools import wraps, reduce
import json


def running_time(fn):
    @wraps(fn)
    def process_fn(*args, **kwargs):
        t1 = datetime.now().timestamp()
        res = fn(*args, **kwargs)
        used_time = datetime.now().timestamp() - t1
        # process_fn(used_time)
        print(fn.__name__, "used(s):", used_time)
        return res
    return process_fn


def print_file_lineno():
    import inspect
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    return info.filename,  info.lineno  # , info.function, info.code_context


@running_time
def all_prem(num_list):
    """
    reduce to ger perm
    func_perm = lambda x, code=',': reduce(lambda x, y: ['%s%s' % (i, j) for i in x for j in y], x)
    :param num_list:
    :return:
    """
    lists = [num_list for i in range(len(num_list))]
    func_perm = lambda x: reduce(lambda x, y: ['%s%s' % (i, j) for i in x for j in y], x)
    lists = func_perm(lists)
    print(len(lists))
    return lists


@running_time
def recursion_perm(lists, k):
    """
    recursion to get perm
    lists: [1,2,3,4,5,]
    k: length
    """
    if k == 1:
        return lists
    all_perm = []
    result = recursion_perm(lists, k - 1)
    for item in result:
        for j in lists:
            all_perm += [str(j) + str(item)]
    return all_perm


class Singleton(type):
    """
    class SingleClass(metaclass=Singleton)  # python3
    __metaclass__ = Singleton  # python2
    """
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


class JsonSerialize(object):

    @staticmethod
    def str2json(str_msg):
        assert isinstance(str_msg, str)
        return json.loads(str_msg)

    @staticmethod
    def byte2json(byte_msg):
        assert isinstance(byte_msg, bytes)
        byte_msg = byte_msg.decode('utf-8')
        return json.loads(byte_msg)

    @staticmethod
    def json2str(json_msg):
        assert isinstance(json_msg, dict)
        return json.dumps(json_msg)

    @staticmethod
    def json2byte(json_msg):
        assert isinstance(json_msg, dict)
        return json.dumps(json_msg).encode('utf-8')

    @staticmethod
    def json2file(json_msg, filename):
        with open(filename, 'w+') as f:
            f.write(json.dumps(json_msg, indent=4))

    @staticmethod
    def file2json(filename):
        with open(filename, 'r') as f:
            json_data = json.load(f)
            return json_data

    @staticmethod
    def json_sort(json_msg, key=0):
        json_msg = sorted(json_msg, key=lambda d: d[key])
        return json_msg


class DatetimeManage(object):
    FMTDEFAULT = "%Y-%m-%d %H:%M:%S"
    FMTES = "%Y-%m-%dT%H:%M:%S"
    FDATE = "%Y-%m-%d"
    NDATEF = "%Y%m%d"

    def __init__(self):
        pass

    @staticmethod
    def datetime2str(dt, fmt=FMTDEFAULT):
        """
        :param dt:
        :param fmt: default="%Y-%m-%d %H:%M:%S"
        :return:
        """
        if isinstance(dt, datetime):
            return dt.strftime(fmt)
        else:
            return None

    @staticmethod
    @running_time
    def str2datetime(st, fmt=FMTDEFAULT):
        try:
            return datetime.strptime(st, fmt)
        except Exception as e:
            return None

    @staticmethod
    def get_current_week(weeks_ago=0, str_result=False):
        """
        get monday and sunday of current date
        :param weeks_ago: int
        :return:
        """
        monday, sunday = date.today() - timedelta(days=7*weeks_ago), date.today() - timedelta(days=7*weeks_ago)
        one_day = timedelta(days=1)
        while monday.weekday() != 0:
            monday -= one_day
        while sunday.weekday() != 6:
            sunday += one_day
        if str_result:
            return monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")
        return monday, sunday

    @staticmethod
    def get_days_ago(days):
        days_ago = date.today() - timedelta(days=days)
        return days_ago.strftime(DatetimeManage.NDATEF)

@running_time
def test():
    sum = 0
    for i in range(123000):
        sum += i**2 + 1
    return sum


if __name__ == "__main__":
    test()
    data = [i for i in range(1, 9)]
    data1 = all_prem(data)
    data2 = recursion_perm(data, 8)
    print(len(data2))

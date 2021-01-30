from psutil import disk_usage
import os

def get_disk_usage(path):
    if not path.startswith("/opt/data"):
        path = os.path.join("/opt/data", path)
    if not os.path.exists(path):
        return u"路径不存在"
    use_info = disk_usage(path)
    total = round(use_info.total / 1024 / 1024 / 1024, 2)
    used = round(use_info.used / 1024 / 1024 / 1024, 2)
    free = round(use_info.free / 1024 / 1024 / 1024, 2)
    output = u"已用{} %, 可用{} / 共{} G".format(use_info.percent, free, total)
    return output


if __name__ == "__main__":
    import sys
    # print(sys.argv)
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "/opt/data"
    print(get_disk_usage(path))

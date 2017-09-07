import json
import psutil


class Usage():
    def __init__(self, capture_time=1):
        self.capture_time = capture_time

    def bytes2human(self, n):
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.3f%s' % (value, s)
        return '%s%s' % (n, 'B')

    def cpu_header(self):
        number = psutil.cpu_count(logical=True)
        line = ''
        for n in range(number):
            line += 'CPU utilization {},'.format(n)
        return line[0:-1]

    def cpu_csv(self):
        values = psutil.cpu_percent(interval=self.capture_time, percpu=True)
        line = ''
        for value in values:
            line += str(value) + ','
        return line[0:-1]

    def disk_header(self):
        header = ['total', 'used', 'free', 'percent']
        line = ''
        for item in header:
            line += 'Disk {} /,'.format(item)
        return line[0:-1]

    def disk_csv(self):
        line = ''
        values = psutil.disk_usage('/')
        for value in values[0:-1]:
            line += self.bytes2human(value) + ','
        line += str(values[-1])
        return line

    def mem_ram_header(self):
        header = ['total', 'available', 'percent']
        line = ''
        for item in header:
            line += 'RAM {},'.format(item)
        return line[0:-1]

    def mem_ram_csv(self):
        values = psutil.virtual_memory()
        values = [values.total, values.available]
        line = ''
        for value in values:
            line += self.bytes2human(value) + ','
        line += '%.2f' % float((1 - values[1] / values[0]) * 100)
        return line

    def mem_swap_header(self):
        header = ['total', 'free', 'percent']
        line = ''
        for item in header:
            line += 'SWAP {},'.format(item)
        return line[0:-1]

    def mem_swap_csv(self):
        values = psutil.swap_memory()
        values = [values[0], values[2], values[3]]
        line = ''
        for value in values[0:-1]:
            line += self.bytes2human(value) + ','
        line += '%.2f' % values[-1]
        return line


if __name__ == '__main__':
    values = psutil.swap_memory()
    print(values)

    print('----')
    usage = Usage()
    print(usage.cpu_header())
    print(usage.cpu_csv())
    print(usage.disk_header())
    print(usage.disk_csv())
    print(usage.mem_ram_header())
    print(usage.mem_ram_csv())
    print(usage.mem_swap_header())
    print(usage.mem_swap_csv())

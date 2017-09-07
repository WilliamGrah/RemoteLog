from gpu import GPU
from usage import Usage
import os
import sys
import time


class Logger():
    def __init__(self, path, filename='log', delay=1):
        self.delay = delay;
        self.path= os.path.abspath(path)
        self.logfile = None
        self.header = None
        self.csv = None

        notGood = True
        name = filename
        count = 0
        while notGood:
            self.logfile = os.path.join(path, name + '.csv')
            print('Log in: ', self.logfile)
            if os.path.exists(self.logfile):
                print('File already exist..')
                name = filename +'_{:05d}'.format(count)
                count += 1
            else:
                notGood = False

    def append_csv(self, values, endl=True):
        with open(self.logfile, 'a') as f:
            line = ''
            for value in values:
                line += value() + ','
            line = line[0:-1]
            print(line)
            if endl:
                line += '\n'
            f.write(line)
            f.close()

    def set_header(self, header):
        self.header = header

    def set_csv(self, csv):
        self.csv = csv

    def run(self):
        self.append_csv(self.header)
        start_time = time.time()
        while True:
            try:
                delay = self.delay - (time.time() - start_time)
                print('Delay for: {:.2f}s'.format(delay))
                time.sleep(delay)
            except Exception as e:
                print(e)

            start_time = time.time()
            self.append_csv(self.csv)

if __name__ == '__main__':
    gpu = GPU()
    usage = Usage(3)

    headers = [usage.cpu_header, usage.disk_header, usage.mem_ram_header, usage.mem_swap_header, gpu.header]
    values = [usage.cpu_csv, usage.disk_csv, usage.mem_ram_csv, usage.mem_swap_csv, gpu.csv]

    path = os.path.dirname(os.path.realpath(__file__))
    logger = Logger(path, delay=5)
    logger.set_header(headers)
    logger.set_csv(values)
    logger.run();

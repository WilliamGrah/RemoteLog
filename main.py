from logger import Logger
from save import Saver
from gpu import GPU
from usage import Usage

import os
import threading


class Record():
    def __init__(self, path, repository, user):
        self.path = path
        self.gpu = GPU()
        self.usage = Usage(15)
        self.headers = [self.usage.cpu_header, self.usage.disk_header,
                        self.usage.mem_ram_header, self.usage.mem_swap_header, self.gpu.header]
        self.values = [self.usage.cpu_csv, self.usage.disk_csv,
                       self.usage.mem_ram_csv, self.usage.mem_swap_csv, self.gpu.csv]
        self.logger = Logger(os.path.join(self.path, repository), delay=0)
        self.logger.set_header(self.headers)
        self.logger.set_csv(self.values)

        self.saver = Saver()
        self.saver.get_repository(path, repository, user)

    def run_saver(self):
        self.saver.add()
        self.saver.commit()
        threading.Timer(30, self.run_saver).start()

    def run_logger(self):
        self.logger.run()

    def run(self):
        self.run_saver()
        self.run_logger()


def run_saver(saver):
    saver.add()
    saver.commit()
    threading.Timer(30, lambda: run_saver(saver)).start()


if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    record = Record(path,  'log', 'patrickelectric')
    record.run()

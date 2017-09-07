import gpustat
import json
import io
import sys


class GPU():
    def __init__(self, prefix='gpu'):
        try:
            self.gpu_stats = gpustat.GPUStatCollection.new_query()
            self.prefix = prefix
            self.ids = ['index', 'name', 'temperature.gpu',
                        'utilization.gpu', 'memory.used', 'memory.total', 'processes']
        except Exception as e:
            self.ids = ''
            self.prefix = ''
            print(e)

    def header(self):
        line = ''
        for id in self.ids:
            line += '{} {},'.format(self.prefix, id.split('.')[0])
        return line[0:-1]

    def csv(self):
        data = io.StringIO()
        try:
            self.gpu_stats.print_json(data)
            data = json.loads(data.getvalue())
            line = ''
            for gpu in data['gpus']:
                for id in self.ids:
                    line += str(gpu[id]) + ','
            return line[0:-1]
        except Exception as e:
            print(e)
            return ''


if __name__ == '__main__':
    gpu = GPU()
    print(gpu.header())
    print(gpu.csv())

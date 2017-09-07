import gpustat
import json
import io
import sys

class GPU():
    def __init__(self, prefix='gpu'):
        self.prefix = prefix
        self.ids = ['index', 'name', 'temperature.gpu', 'utilization.gpu', 'memory.used', 'memory.total', 'processes']

    def header(self):
        line = ''
        for id in self.ids:
            line += '{} {},'.format(self.prefix, id.split('.')[0])
        return line[0:-1]

    def csv(self):
        data = io.StringIO()
        try:
            gpu_stats = gpustat.GPUStatCollection.new_query()
            gpu_stats.print_json(data)
        except Exception as e:
            print(e)

        data = json.loads(data.getvalue())

        line = ''
        for gpu in data['gpus']:
            for id in self.ids:
                line += str(gpu[id]) + ','
        return line[0:-1]

if __name__ == '__main__':
    gpu = GPU()
    print(gpu.header())
    print(gpu.csv())

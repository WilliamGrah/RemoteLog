import os
import psycopg2
import time
from gpu import GPU
from usage import Usage
from datetime import datetime
from decouple import config

class Register():
    def __init__(self, delay=30):
        self.delay = delay

    def connect(self):
        return psycopg2.connect(host=config('host'), user=config('user'), password=config('password'), dbname=config('dbname'))

    def execute(self, query):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        cur.close()
        return cur

    def create_table(self):
        self.execute("""
            CREATE TABLE cpu_usage (
                id SERIAL,
                uname varchar(20),
                info text[],
                created_at timestamp)
        """)

    def get_data(self):
        gpu = GPU()
        usage = Usage(3)

        data = []
        data_list = [usage.cpu_csv(), usage.disk_csv(), usage.mem_ram_csv(), usage.mem_swap_csv(), gpu.csv()]
        for i in data_list:
            data += i.split(',')

        return data

    def save(self):
        name = os.uname()[1]
        data = self.get_data()

        query = """
            INSERT INTO cpu_usage
            (uname, info, created_at)
            VALUES
            (\'{}\', ARRAY{}, \'{}\')
            """.format(name, data, datetime.now()
        )

        reg.execute(query)

    def run(self):
        start_time = time.time()
        while True:
            try:
                delay = self.delay - (time.time() - start_time)
                if delay > 0:
                    print('Delay for: {:.2f}s'.format(delay))
                    time.sleep(delay)
            except Exception as e:
                print(e)

            start_time = time.time()
            self.save()


if __name__ == '__main__':
    reg = Register(45)
    reg.run()

from tripcamera.Worker import Worker
import time

while True:
    print('worker exec')
    worker = Worker(station='innertube',srcpath='/vanaramdisk/',uploadUrl='localhost:3030/upload')
    worker.exec()
    time.sleep(5)
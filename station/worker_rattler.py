from tripcamera.Worker import Worker
import time

while True:
    worker = Worker(station='rattler',srcpath='/vanaramdisk/',uploadUrl='192.168.111.19:3030/upload')
    worker.exec()
    time.sleep(5)
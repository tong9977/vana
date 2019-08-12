from tripcamera.Worker import Worker
from twisted.internet import task, reactor


worker = Worker(station='rattler',srcpath='/vanaramdisk/',uploadUrl='localhost:3030/upload')
def sendCustomerPhotosToServer():
    #print("sendCustomerPhotosToServer")
    worker.exec() 
    pass

task1 = task.LoopingCall(sendCustomerPhotosToServer)
task1.start(5.0) # call every 5 seconds


reactor.run()

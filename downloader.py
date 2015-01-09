import threading
import time
import urllib2
from java.io import Serializable
from java.util.concurrent import Callable
from com.hazelcast.core import HazelcastInstanceAware
from com.hazelcast.nio.serialization import DataSerializable

class Downloader(Callable, Serializable, HazelcastInstanceAware, DataSerializable):
    def __init__(self, url):
        self.url = url
        self.started = 0
        self.completed = 0
        self.result = ""
        self.exception = ""

    def __str__(self):
        if self.exception:
             return "[%s] %s download error %s in %.2fs" % \
                (self.hazelcastInstance, self.url, self.exception,
                 self.completed - self.started, ) #, self.result)
        elif self.completed:
            return "[%s] %s downloaded %dK in %.2fs" % \
                (self.hazelcastInstance, self.url, len(self.result)/1024,
                 self.completed - self.started, ) #, self.result)
        elif self.started:
            return "[%s] %s started at %s" % \
                (self.hazelcastInstance, self.url, self.started)
        else:
            return "[%s] %s not yet scheduled" % \
                (self.hazelcastInstance, self.url)

    # needed to implement the Callable interface;
    # any exceptions will be wrapped as either ExecutionException
    # or InterruptedException
    def call(self):
        self.thread_used = threading.currentThread().getName()
        self.started = time.time()
        try:
            self.result = urllib2.urlopen(self.url).read()
        except Exception, ex:
            self.exception = str(ex)
        self.completed = time.time()
        return self

    # implement HazelcastInstanceAware
    def setHazelcastInstance(self, instance):
        self.hazelcastInstance = instance;
        
    # implement DataSerializable
    def writeData(self, out):
        out.writeUTF(self.url)
        out.writeInt(self.started)
        out.writeInt(self.completed)
        out.writeUTF(self.result)
        out.writeUTF(self.exception)

    def readData(self, input):
        self.url = input.readUTF()
        self.started = input.readInt()
        self.completed = input.readInt()
        self.result = input.readUTF()
        self.exception = input.readUTF()

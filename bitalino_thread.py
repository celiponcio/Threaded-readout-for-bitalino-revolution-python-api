from bitalino import BITalino as _BITalino
import threading, datetime
import numpy as np

class btt(object):

    def __init__(self, macAddress):
        # defaults
        self.batteryThreshold = 30
        self.acqChannels = [0, 1, 2, 3, 4, 5]
        self.samplingRate = 1000 # SPS
        self.nSamples = 100 # samples per readout call. The average is a point in the buffer.
        self.timeout = 5 # seconds
        self.fifoDepth=10 # seconds
        self.duration = 1000000 # seconds
        #        self.readoutRate=10 # Hz, Not yet...

        self.macAddress = macAddress
        self.__fifo_size=0
        self.__btl = _BITalino(self.macAddress, self.timeout)
        print(self.__btl.version())
        self.__btl.battery(self.batteryThreshold)

    def start(self):
    # handle errors, etc later
        self.fifo_size=self.fifoDepth*self.samplingRate/self.nSamples
        self.btt_fifo=np.zeros((self.fifo_size, len(self.acqChannels)))
        self.__start_time=datetime.datetime.now()
        self.thread = threading.Thread(target=self.__aquire)
        self.thread.start()

    def __aquire(self):
        self.__btl.start(self.samplingRate, self.acqChannels)
        while (datetime.datetime.now() - self.__start_time).total_seconds()<self.duration:
            raw_btl = self.__btl.read(self.nSamples)
            # print(raw_btl[:, 5:].mean(0).T)
            self.btt_fifo = np.roll(self.btt_fifo, -1,0)
            self.btt_fifo[-1,:] = raw_btl[:, 5:].mean(0).T
            # print(self.btt_fifo.T)

    def running(self):
        try:
            return self.thread.is_alive()
        except:
            return False

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
        try:
            self.bitalino = _BITalino(self.macAddress, self.timeout)
        except Exception as ex:
            print str(ex)
            self.bitalino = None
            return
        print(self.bitalino.version())
        self.bitalino.battery(self.batteryThreshold)

    def __del__(self):
        if not self.bitalino:
            return
        self.bitalino.stop()
        self.bitalino.close()

    def start(self):
    # handle errors, etc later
        self.fifo_size=self.fifoDepth*self.samplingRate/self.nSamples
        self.btt_fifo=np.zeros((self.fifo_size, len(self.acqChannels)))
        self.__start_time=datetime.datetime.now()
        self.thread = threading.Thread(target=self.__aquire)
        self.thread.start()

    def __aquire(self):
        self.bitalino.start(self.samplingRate, self.acqChannels)
        while (datetime.datetime.now() - self.__start_time).total_seconds()<self.duration:
            raw_btl = self.bitalino.read(self.nSamples)
            # print(raw_btl[:, 5:].mean(0).T)
            self.btt_fifo = np.roll(self.btt_fifo, -1,0)
            self.btt_fifo[-1,:] = raw_btl[:, 5:].mean(0).T
            # print(self.btt_fifo.T)

    def running(self):
        try:
            return self.thread.is_alive()
        except:
            return False

# Threaded readout for bitalino (r)evolution python api
Usefull if several data sources are to be acquired simultaneouslly without mutually waiting for each other.

Requires installation of the bitalino python api: https://github.com/BITalinoWorld/revolution-python-api and numpy

Data appears in a fifo in the main application. See example in bitalino_thread_test.py.

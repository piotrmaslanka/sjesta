#!/usr/bin/python
from satella.unix import hang_until_sig
from satella.threads import BaseThread
from sjesta.master import SjestaThread
from sjesta.db import SQLDB

if __name__ == '__main__':
    SQLDB()     # Connect to SQL
        
    sjesta = SjestaThread().start()
    hang_until_sig()
    sjesta.terminate().join()
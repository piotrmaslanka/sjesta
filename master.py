from satella.threads import BaseThread, Monitor
import json, time
from sjesta.db import SQLDB
from sjesta.job_tracker import JobTrackerThread 
from sjesta.objects import Job

class SjestaThread(BaseThread, Monitor):
    def __init__(self):
        BaseThread.__init__(self)
        Monitor.__init__(self)
        
        self.active_jobs_counter = 0

        with open('config.txt', 'rb') as cfg:
            js = json.load(cfg)
    
        self.scan_interval = js['scan_interval']
        self.max_concurrent_jobs = js['max_concurrent_jobs']
    
    @Monitor.protect
    def get_job_counter(self):
        return self.active_jobs_counter
    
    @Monitor.protect
    def increase_job_counter(self):
        self.active_jobs_counter += 1
        
    @Monitor.protect
    def decrease_job_counter(self):
        self.active_jobs_counter -= 1    
    
    def schedule_a_job(self):
        """True if anything was scheduled, else False"""
        with SQLDB.i.transaction() as cur:
            cur.execute('''SELECT id
                           FROM jobs
                           WHERE started_at IS NULL
                           ORDER BY niceness ASC
                           LIMIT 1''')
            try:
                id, = cur.fetchone()
            except TypeError:
                return False

        j = Job(id)
        JobTrackerThread(j, self).start()
        return True
    
    def run(self):        
        while not self._terminating:            
            if self.get_job_counter() < self.max_concurrent_jobs:
                if self.schedule_a_job():
                    continue
                else:
                    time.sleep(self.scan_interval)
                        
        # Wait for jobs to terminate
        while self.get_job_counter() > 0:
            time.sleep(5)
            

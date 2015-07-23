from threading import Thread
from sjesta.objects import Job
import shlex
try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess

class JobTrackerThread(Thread):
    def __init__(self, job, master):
        Thread.__init__(self)
        self.job = job
        self.master = master
        job.enter_state(Job.RUNNING)
        
    def run(self):
        self.master.increase_job_counter()
        po = subprocess.Popen(shlex.split(self.job.program),
                              bufsize=-1,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

        stdout, stderr = po.communicate(self.job.get_stdin_data())

        if len(stdout) == 0: stdout = None
        if len(stderr) == 0: stderr = None
        
        self.job.enter_state(Job.COMPLETED, po.returncode, stdout, stderr)
        self.master.decrease_job_counter()
        
        
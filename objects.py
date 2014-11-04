import time
from sjesta.db import SQLDB

class Job(object):
    
    SCHEDULED = 0       # State just after creation
    RUNNING = 1         # Running
    COMPLETED = 2         # Completed / failed
    
    class DoesNotExist(Exception): pass
    
    def __init__(self, id):
        self.id = id
        with SQLDB.i.transaction() as cur:
            cur.execute('''SELECT scheduled_by, scheduled_at, completed_on,
                                  return_code, description, started_at,
                                  stdin, stdout, stderr, program, niceness
                           FROM jobs
                           WHERE id=%s''', (id, ))
            try:
                self.scheduled_by, self.scheduled_at, self.completed_on, \
                self.return_code, self.description, self.started_at, \
                self.stdin, self.stdout, self.stderr, \
                self.program, self.niceness = cur.fetchone()
            except TypeError:
                raise Job.DoesNotExist
                        
    def get_stdin_data(self):
        """Returns stdin data or None if no stdin"""
        try:
            stdin = Dataset(self.stdin)
        except Dataset.DoesNotExist:
            return None
        else:
            return stdin.data
                    
                        
    def enter_state(self, newstate, rc=None, stdout=None, stderr=None):
        with SQLDB.i.transaction() as cur:
            if newstate == Job.RUNNING:
                self.started_at = int(time.time())
                # Set "started_at"
                cur.execute('UPDATE jobs SET started_at=%s WHERE id=%s', 
                            (self.started_at, self.id))
            elif newstate == Job.COMPLETED:
                self.completed_on = int(time.time())
                self.return_code = rc
                # Allocate stdout and stderr if necessary
                if stdout != None:
                    cur.execute('INSERT INTO datasets (data) VALUES (%s) RETURNING id', 
                                                (stdout, ))
                    self.stdout, = cur.fetchone()
                if stderr != None:
                    cur.execute('INSERT INTO datasets (data) VALUES (%s) RETURNING id', 
                                                (stderr, ))
                    self.stderr, = cur.fetchone()

                cur.execute('''UPDATE jobs 
                               SET stdout=%s, stderr=%s, completed_on=%s, return_code=%s
                               WHERE id=%s''', 
                                    (self.stdout, self.stderr, self.completed_on,
                                     self.return_code, self.id))
            
                        
                        
class Dataset(object):
    class DoesNotExist(Exception): pass
    
    def __init__(self, id):
        self.id = id
        with SQLDB.i.transaction() as cur:
            cur.execute('SELECT data FROM datasets WHERE id=%s', (id, ))
            try:
                self.data, = cur.fetchone()
            except TypeError:
                raise Dataset.DoesNotExist
                        
    def delete(self):
        with SQLDB.i.transaction() as cur:
            cur.execute('DELETE FROM datasets WHERE id=%s', (self.id, ))
                        
                        
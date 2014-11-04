from satella.db.pool import DatabaseDefinition, ConnectionPool
import json
try:
    import psycopg2        # depends on psycopg2 PostgreSQL driver
except:
    import psycopg2ct as psycopg2
    from psycopg2ct import compat
    compat.register()
    
class SQLDB(object):
    """
    A class that can be used to get cursors to perform queries.
    Safeguards against multiple shit that comes from DB & network programming.
    Implements connection pooling
    """

    from psycopg2 import IntegrityError

    i = None        # Instance variable
    
    def __init__(self):
        """
        Initiates multiple connections

        @type dbconn_args: dictionary of arguments
        @param dbconn_args: dictionary to be passed to connect()

        @type pool: int
        @param pool: how many connections to pool
        """

        def acs(conn):
            conn.set_client_encoding('UTF8')

        def filter_excepts(e):
            """DatabaseError saying that "error with no message from the libpq"
            if only DatabaseError that needs reloading connection"""
            if isinstance(e, psycopg2.OperationalError): return True
            if not isinstance(e, psycopg2.DatabaseError): return False
            if 'no message from the libpq' in e.message: return True
            if 'server closed the connection unexpectedly' in e.message: return True
            return False

        with open('config.txt', 'rb') as cfg:
            js = json.load(cfg)
        
        dbconn_args = {
            'database': str(js['db_name']),
            'host': str(js['db_host']),
            'password': str(js['db_password']),
            'user': str(js['db_user']),
            'port': js['db_port']
        }
        
        dd = DatabaseDefinition(
                psycopg2.connect,
                (psycopg2.OperationalError, psycopg2.DatabaseError),
                (), dbconn_args, xwcb=filter_excepts,
                acs=acs)

        self.cp = ConnectionPool(dd, 1)

        SQLDB.i = cp

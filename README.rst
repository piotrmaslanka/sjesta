About SJESTA
------------

SJESTA is a batch job manager written in Python.

You enqueue jobs in it by writing rows into a Postgres table, and it reports them done
by writing values in the same table. It supports priorities.

It essentially runs programs, managing their arguments, return codes, stdin/stdout/stderr.

SJESTA requires `satella <https://github.com/piotrmaslanka/satella/>`_ to be installed.

About SJESTA
------------

SJESTA is a batch job manager written in Python.

You enqueue jobs in it by writing rows into a Postgres table, and it reports them done
by writing values in the same table. It supports priorities.

It essentially runs programs, managing their arguments, return codes, stdin/stdout/stderr.

SJESTA was built for `SMOK <http://www.smok-serwis.pl/>`_ by `Piotr Maślanka <https://github.com/piotrmaslanka/>`_.

Background
----------

We use SJESTA at `SMOK <http://www.smok-serwis.pl/>`_ for running multiple batch jobs needed to keep the system in a good shape and perform administrative tasks.
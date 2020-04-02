import os

class Config(object):
    ORACLE_USER = os.environ['ORACLE_USER'] or 'my-username'
    ORACLE_PASS = os.environ['ORACLE_PASS'] or 'my-password'
    ORACLE_HOST = 'oracle12c.scs.ryerson.ca'
    ORACLE_PORT = '1521'
    ORACLE_SID  = 'orcl12c'

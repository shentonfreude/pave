The settings.py file should put the SQLite DB file here.
It needs to use an absolute path so Apache mod_wsgi can also use it.
For Apache, change the ownership of the file and dir to be
the same as the userid that Apache runs as

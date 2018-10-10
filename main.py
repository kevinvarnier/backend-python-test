"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
  main.py migratedb
"""
from docopt import docopt
import subprocess
import os

from alayatodo import app
from resources import fixtures

def _run_sql(filename):
    try:
        subprocess.check_output(
            "sqlite3 %s < %s" % (app.config['DATABASE'], filename),
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError, ex:
        print ex.output
        os.exit(1)


if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        _run_sql('resources/database.sql')
        _run_sql('resources/fixtures.sql')
        fixtures.create_users()
        print "AlayaTodo: Database initialized."
    elif args['migratedb']:
        _run_sql('resources/migration.sql')
        print("AlayaTodo: Database correcly migrated")
    else:
        app.run(use_reloader=True)

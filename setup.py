import os
import sys

def bootstrap():
    if not os.path.exists('db/users.db'):
        print("The file db/users.db does not exist.", file=sys.stderr)
        print("Run db/setup.py before running the server.", file=sys.stderr)
        print("System exiting.", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists('db/users'):
        print("The folder db/users does not exist.", file=sys.stderr)
        print("Create the folder before running the server.", file=sys.stderr)
        print("System exiting.", file=sys.stderr)
        sys.exit(1)

# Python standard library modules
import sys
import yaml

# 3rd party modules
from fabric.api import run, sudo

# Try to open and parse the config.yaml file
try:
    config = yaml.load(open('config.yaml', 'r'))
except yaml.scanner.ScannerError:
    print 'Error: Could not parse config.yaml file.'
    sys.exit(1)
except IOError:
    print 'Error: Could not open config.yaml file.'
    sys.exit(1)


def deploy():
    for command_pair in config['commands']:
        privilege, command = command_pair.items()[0]
        if privilege == 'sudo':
            sudo(command)
        else:
            run(command)

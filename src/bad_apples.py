import os
import psutil
import time
import signal

import logging

SIGKILL = 9
INTERVAL = 10


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-c", dest='bad_apples', help="Bad apples file")
parser.add_argument("-d", dest='daemon', help="Start daemon", action="store_true")
args = parser.parse_args()

def get_logger():
    logger = logging.getLogger("bad_apples")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def get_bad_apples():
    bad_apples_file = "/etc/bad_apples/bad_apples.txt"
    if args.bad_apples:
       bad_apples_file = args.bad_apples 

    data = []
    try:
        with open(bad_apples_file, "r") as fp:
            data = fp.readlines()
    except FileNotFoundError:
        print("Bad apples file was not found")
        exit(1)

    data = [ x.strip() for x in data ]
    return data

def kill_bad_apple_process(logger):
    bad_apples = get_bad_apples()
    actors = []
    procs = {p.pid: p.info for p in psutil.process_iter(['name'])}

    for process, info in procs.items():
        if info["name"] in bad_apples:
            actors.append((process, info["name"]))

    for actor in actors:
        logger.info("killing {}".format(actor[1]))
        os.kill(actor[0], SIGKILL)

def handler(signum, frame):
    print('Exiting...')
    exit(0)


def setup_sigint():
    signal.signal(signal.SIGINT, handler)

def main():
    logger = get_logger()
    setup_sigint()
    if args.daemon:
        logger.info('Starting bad_apples daemon')
        while True:
            kill_bad_apple_process(logger)
            time.sleep(INTERVAL)
    else:
        kill_bad_apple_process(logger)

if __name__ == "__main__":
    main()

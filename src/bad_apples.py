import os
import psutil

import logging

SIGKILL = 9


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--bad_apples", help="Bad apples file")
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
    bad_apples_file = "bad_apples.txt"
    if args.bad_apples:
       bad_apples_file = args.bad_apples 

    data = []
    try:
        with open(bad_apples_file, "r") as fp:
            data = fp.readlines()
    except FileNotFoundError:
        logger.error("Bad apples file was not found")
        
    data = [ x.strip() for x in data ]
    return data


def main():
    logger = get_logger()
    bad_apples = get_bad_apples()
    actors = []
    procs = {p.pid: p.info for p in psutil.process_iter(['name'])}
    
    for process, info in procs.items():
        if info["name"] in bad_apples:
            actors.append((process, info["name"]))

    for actor in actors:
        logger.info("killing {}".format(actor[1]))
        os.kill(actor[0], SIGKILL)


if __name__ == "__main__":
    main()

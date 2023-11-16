#!/usr/bin/python3
##
## Author: Logu R<logu.rangasamy@suse.com>
## 

import argparse
from concurrent.futures import ThreadPoolExecutor
import subprocess
import os

def runssh_cmd(host, rcmd):
    try:
        sshcmd = f"ssh -l root {host} {rcmd}"
        result = subprocess.run(sshcmd, shell=True, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        # Capture error information
        result = e

    return result

def get_hosts_from_env():
    nodes_env = os.getenv("NODES")
    if not nodes_env:
        raise ValueError("Environment variable NODES is not set.")
    return nodes_env.split()

def main():
    parser = argparse.ArgumentParser(description='Run remote command in parallel on multiple hosts defined by NODES env variable.')
    parser.add_argument('rcmd', help='Remote command to run on each host')
    args = parser.parse_args()

    try:
        hosts = get_hosts_from_env()
    except ValueError as e:
        print(f"Error: {e}")
        return

    rcmd_result = {}

    with ThreadPoolExecutor(max_workers=128) as executor:
        ssh_ex = []
        for host in hosts:
            ssh_ex.append(executor.submit(runssh_cmd, host, args.rcmd))

        for host in hosts:
            rcmd_result.update({host: ssh_ex.pop(0).result()})

    for host, result in rcmd_result.items():
        code = str(result.returncode)
        out = result.stdout.strip()
        err = result.stderr.strip()

        print("%20s %5s ==> %s | %s" % (host, "[" + code + "]", out, err))
if __name__ == "__main__":
    main()


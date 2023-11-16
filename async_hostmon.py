#!/usr/bin/python3
##
## Author: Logu R<logu.rangasamy@suse.com>
## 

import os
import yaml
import json
import asyncio
from flask import Flask, render_template, jsonify, request
from flask_caching import Cache
from cachetools import cached, TTLCache

# Constants
CACHE_TIMEOUT = 60
CMD_CACHE_TIMEOUT = CACHE_TIMEOUT
REFHOST_YML = os.path.join(os.environ.get("HOME"), ".local/share/refdb/refhosts.yml")

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['SECRET_KEY'] = 'secret_key'  # Add a secret key for Flask

cache_config = {
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': '.cache1',
    'CACHE_THRESHOLD': 1000
}
cache = Cache(app, config=cache_config)

def load_refhost_data(yml_path):
    with open(yml_path) as f:
        return yaml.safe_load(f)

def get_host_inventory(data):
    refhost_inventory = {}
    counter = 0

    for loc, hosts in data.items():
        for host in hosts:
            counter += 1
            prod = host['product']
            prod_vers = prod['version']
            major = str(prod_vers['major'])
            minor = prod_vers.get('minor')
            version_num = major

            if minor is not None:
                version_num = major + "-" + minor

            refhost = {
                'sno': counter,
                'hostname': host['name'],
                'arch': host['arch'],
                'product': prod['name'],
                'version': version_num,
                'location': loc
            }

            refhost_inventory[host['name']] = refhost

    return refhost_inventory

def get_unique_list(data, key):
    unique_values = {host_info.get(key) for _, host_info in data.items() if host_info.get(key) is not None}
    return sorted(list(unique_values))

def get_specific_refhosts(data, location=None, arch=None, product=None, version=None):
    filtered_hosts = {}

    for hostname, host_info in data.items():
        if (
            (not location or host_info['location'] == location) and
            (not arch or host_info['arch'] == arch) and
            (not product or host_info['product'] == product) and
            (not version or host_info['version'] == version)
        ):
            filtered_hosts[hostname] = host_info

    return filtered_hosts

@cached(cache = TTLCache(maxsize = 1024, ttl = CMD_CACHE_TIMEOUT))


async def run_cmd(cmd):
    r = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await r.communicate()  # Capture stdout and stderr data
    print(f"{cmd} => {stderr.decode().strip()}")  # Print stderr data
    return r.returncode, stdout, stderr
    return r

def check_icmp(host):
    return run_cmd(f"ping -c 1 -w 2 {host}")

def check_ssh(host):
    return run_cmd(f"nc -vzw 2 {host} 22")

async def do_probe(probe, host_name):
    result = await probe(host_name)  # Use await here
    status = 'Up' if result[0] == 0 else 'Down'  # Access return code from the result tuple
    return status

## ===================

async def logic_issue_get_probe_data(data, probe_funcs):
    all_host_status = []

    tasks = []
    for probe_func in probe_funcs:
        tasks.extend([do_probe(probe_func, host) for host in data])

    results = await asyncio.gather(*tasks)

    for host, probe_func, result in zip(data, probe_funcs * len(data), results):
        host_status = {'hostname': host}
        host_status[f'{probe_func.__name__}_status'] = result
        all_host_status.append(host_status)

    print (all_host_status)
    return all_host_status

async def seq_get_probe_data(data, probe_funcs):
    all_host_status = []

    tasks = []
    for host in data:
        host_status = {'hostname': host}
        host_tasks = [do_probe(probe_func, host) for probe_func in probe_funcs]
        results = await asyncio.gather(*host_tasks)

        for probe_func, result in zip(probe_funcs, results):
            host_status[f'{probe_func.__name__}_status'] = result

        all_host_status.append(host_status)

    return all_host_status


async def get_probe_data(data, probe_funcs):
    all_host_status = []

    tasks = []
    for probe_func in probe_funcs:
        tasks.extend([do_probe(probe_func, host) for host in data])
        #tasks[probe_func.__name__] = [do_probe(probe_func, host) for host in data]

    results = await asyncio.gather(*tasks)

    print("####", results)

    for host in data:
        host_status = {'hostname': host}

        for probe_func, result in zip(probe_funcs, results):
            host_status[f'{probe_func.__name__}_status'] = result

        all_host_status.append(host_status)

    print (json.dumps(all_host_status, indent=2))
    return all_host_status

## ===================

def get_allprobe_data(data):
    probes = [check_icmp, check_ssh]
    return get_probe_data(data, probes)

def get_query_params():
    return {
        'location': request.args.get('location'),
        'arch': request.args.get('arch'),
        'product': request.args.get('product'),
        'version': request.args.get('version'),
    }

# Load data once at the start of the application

try:
    ymldata = load_refhost_data(REFHOST_YML)
    refhost_inventory = get_host_inventory(ymldata)
except FileNotFoundError as e:
    print(f"Error: {e}. Please make sure the YAML file {REFHOST_YML} exists.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
else:
    print("Data loaded successfully.")

# Get filters based on refhost_inventory
filters = {key: get_unique_list(refhost_inventory, key) for key in ['location', 'arch', 'product', 'version']}

@app.route('/')
def index():
    return render_template('hostmon.html', filters=filters)

@app.route('/status', methods=['GET'])
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=lambda: request.url)
def get_status():
    params = get_query_params()
    data = get_specific_refhosts(refhost_inventory, **params)

    # Run the asynchronous function synchronously using asyncio.run
    all_status = asyncio.run(get_allprobe_data(data))

    return jsonify(all_status)


@app.route('/hostinfo', methods=['GET'])
def get_hostinfo():
    params = get_query_params()
    data = get_specific_refhosts(refhost_inventory, **params)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)


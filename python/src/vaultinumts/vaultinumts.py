#!/usr/bin/env python3

import argparse
import hashlib
import os
import requests
import rfc3161ng

from datetime import datetime
from functools import partial

TS_SANDBOX = 'sandbox'
TS_PRODUCTION = 'production'
TS_ENVIRONMENTS = {
    'sandbox': 'https://ts-sandbox.vaultinum.com/v1/timestamp/request',
    'production': 'https://ts-eidas.vaultinum.com/v1/timestamp/request'
}


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog=f'python {os.path.basename(__file__)}',
        description='Send a timestamp request to the Vaultinum timestamping service.')
    environment_group = parser.add_mutually_exclusive_group()
    environment_group.add_argument('-environment',
                                   default='sandbox',
                                   choices={'sandbox', 'production'},
                                   help='Vaultinum environment to query')
    parser.add_argument('-filename',
                        required=True,
                        type=str,
                        help='file to timestamp')
    parser.add_argument('-apikey',
                        required=False,
                        type=str,
                        help='apikey to use to query the timestamping service')
    return parser.parse_args()


def hash_file(filename, hashtype, chunksize=2**15, bufsize=-1):
    """Create a hash object with specified hash algorithm from a filename on disk."""
    h = hashtype()
    with open(filename, 'rb', bufsize) as file:
        for chunk in iter(partial(file.read, chunksize), b''):
            h.update(chunk)
    return h


def timestamp(filename, environment, apikey):
    print(
        f'Timestamping file "{filename}" on {environment} environment')
    file_digest = hash_file(filename, hashlib.sha512)
    tsq = rfc3161ng.make_timestamp_request(
        digest=file_digest.digest(), hashname='sha512')
    encoded_tsq = rfc3161ng.encode_timestamp_request(tsq)

    # Save the timestamp request to disk
    exec_date_time = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    filenames_prefix = f'{exec_date_time}_{filename}'

    ts_req_filename = f'{filenames_prefix}.tsq'
    print(f'Creating timestamp request file: {ts_req_filename}')
    with open(ts_req_filename, mode="wb") as output_file:
        output_file.write(encoded_tsq)
        output_file.close()

    TS_URL = TS_ENVIRONMENTS[environment]
    print(f'Sending request to the timestamp service: {TS_URL}')
    TS_HEADERS = {
        'X-API-KEY': apikey,
        'Content-Type': 'application/timestamp-query'
    }
    r = requests.post(TS_URL, headers=TS_HEADERS, data=encoded_tsq)

    # Save the timestamp response to disk
    ts_res_filename = 'tmp_req_output_file'
    if r.status_code != 200:
        print(
            f'Error when sending timestamp request: {r.status_code}')
        ts_res_filename = f'{filenames_prefix}_{r.status_code}.txt'
    else:
        ts_res_filename = f'{filenames_prefix}.tsr'

    print(f'Saving response content to file: {ts_res_filename}')
    with open(ts_res_filename, mode="wb") as output_file:
        output_file.write(r.content)


def real_main():
    args = parse_arguments()
    timestamp(args.filename, args.environment, args.apikey)


if __name__ == '__main__':
    real_main()

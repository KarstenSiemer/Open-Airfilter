#!/usr/bin/env python3
"""
airfilter exporter for the Prometheus monitoring system.
"""

import sys
from argparse import ArgumentParser
from app.http import start_http_server

def main(args=None):
    """
    Main entry point.
    """

    parser = ArgumentParser()
    parser.add_argument('--port', dest='port', type=int, default=9600,
                        help='Port on which the exporter is listening (9600)')
    parser.add_argument('--address', dest='address', type=str, default='0.0.0.0',
                        help='Address to which the exporter will bind')

    params = parser.parse_args(args if args is None else sys.argv[1:])

    start_http_server(port=params.port, address=params.address)

if __name__ == "__main__":
    main()

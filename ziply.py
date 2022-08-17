################################################################################
"""
Ziply/Frontier Router Statistics Collector.

(c) Joe Stanley | Stanley Solutions | 2022
License: MIT
"""
################################################################################

import argparse
import requests

ZIPLY_ROUTER_URL = "http://{ip_addr}/cgi-bin/home.ha"


def add_arguments(parser_obj: argparse.ArgumentParser) -> None:
    """Attach the arguments to the parser."""
    parser_obj.add_argument("-ip", "--ip-address", default="192.168.254.254",
        help="the IP address of the router to be queried")


def get_router_stats_table(ip_addr: str) -> dict:
    """Get the Router's Statistics Table."""
    resp = requests.get(ZIPLY_ROUTER_URL.format(ip_addr=ip_addr))
    resp.raise_for_status()


def main(parser_obj: argparse.ArgumentParser) -> None:
    """Main Functional Body."""
    args = parser_obj.parse_args()
    statistics = get_router_stats_table(args.ip_address)
    print(statistics)


if __name__ == "__main__":
    main(parser_obj=parser)
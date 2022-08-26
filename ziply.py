################################################################################
"""
Ziply/Frontier Router Statistics Collector.

(c) Joe Stanley | Stanley Solutions | 2022
License: MIT

Parse the data from a Ziply (or Frontier) router and provide it as a dictionary
keyed by section, then by data description. Optionally serve as a simple API to
provide the data as needed.
"""
################################################################################

import argparse
import requests
from bs4 import BeautifulSoup

# Attempt Access for Serving
try:
    from fastapi import FastAPI
    import uvicorn
    __SERVE_FUNCTIONALITY__ = True
except ImportError:
    __SERVE_FUNCTIONALITY__ = False # Indicate Inability to Serve

__version__ = "0.0.1"

ZIPLY_ROUTER_URL = "http://{ip_addr}/cgi-bin/home.ha"

parser = argparse.ArgumentParser(
    description='Collect Ziply/Frontier Router Stats.'
)


def add_arguments(parser_obj: argparse.ArgumentParser) -> None:
    """Attach the arguments to the parser."""
    parser_obj.add_argument("-ip", "--ip-address", default="192.168.254.254",
        help="the IP address of the router to be queried")
    parser_obj.add_argument("-s", "--host-server", action="store_true",
        help="host a simple web-server for the information")
    parser_obj.add_argument("-p", "--port", help="http port to serve")


def get_router_stats_table(ip_addr: str) -> dict:
    """
    Get the Router's Statistics Tables.
    
    Use this function to load the statistics as a dictionary of dictionaries,
    keying the individual headings to their related tables.

    Examples
    --------
    >>> from ziply import get_router_stats_table
    >>> stats_dict = get_router_stats_table(ip_addr="192.168.254.254")
    >>> print(stats_dict)
    {"WAN Summary": {"WAN Link": "Up", "WAN Connection": "Connected",...}}
    """
    # Get Router HTML
    resp = requests.get(ZIPLY_ROUTER_URL.format(ip_addr=ip_addr))
    resp.raise_for_status()
    # Parse into Soup Object
    soup = BeautifulSoup(resp.content, features="html.parser")
    html_headings = [heading.text for heading in soup.find_all("h2")]
    html_tables = soup.find_all("table", attrs={"class": "tablewidthhome"})
    tables = {}
    # Iteratively Build Tables
    for heading, table_data in zip(html_headings, html_tables):
        table = {}
        # Parse the Columns from each Table
        col1 = table_data.find_all(attrs={"class": "col1"})
        col2 = table_data.find_all(attrs={"class": "col2"})
        for k, v in zip(col1, col2):
            table[k.text.replace(":", "")] = v.text.strip("\n\t ").replace(
                "\n", ""
            )
        tables[heading] = table
    return tables


def print_data_table(ip_address: str) -> None:
    """Print the data as a table for CLI interactions."""
    statistics = get_router_stats_table(ip_address)
    # Iteratively Print Table Data
    for i, (stat_group_name, stat_group) in enumerate(statistics.items()):
        if i > 0:
            print("\n")
        print(stat_group_name)
        print('-'*80)
        for stat, data in stat_group.items():
            stat += ":"
            print(f"    {stat.ljust(22)}{data}")


def main(parser_obj: argparse.ArgumentParser) -> None:
    """Main Functional Body."""
    args = parser_obj.parse_args()
    if args.host_server:
        if __SERVE_FUNCTIONALITY__:
            api = FastAPI()
            @api.get("/api/v1/stats")
            def get_stats():
                return get_router_stats_table(args.ip_address)
            uvicorn.run(api, port=args.port)
        else:
            # Serving isn't Supported
            print(
                "(!)  The required pacakges aren't installed to support web "
                "server functionality. Consider installing `fastapi` and "
                "`uvicorn`.\n"
                "Sorry about that..."
            )
    else:
        print_data_table(ip_address=args.ip_address)


if __name__ == "__main__":
    add_arguments(parser_obj=parser)
    main(parser_obj=parser)
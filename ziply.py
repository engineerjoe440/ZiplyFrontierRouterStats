################################################################################
"""
Ziply/Frontier Router Statistics Collector.

(c) Joe Stanley | Stanley Solutions | 2022
License: MIT
"""
################################################################################

import argparse
import requests
from bs4 import BeautifulSoup

ZIPLY_ROUTER_URL = "http://{ip_addr}/cgi-bin/home.ha"

parser = argparse.ArgumentParser(
    description='Collect Ziply/Frontier Router Stats.'
)


def add_arguments(parser_obj: argparse.ArgumentParser) -> None:
    """Attach the arguments to the parser."""
    parser_obj.add_argument("-ip", "--ip-address", default="192.168.254.254",
        help="the IP address of the router to be queried")


def get_router_stats_table(ip_addr: str) -> dict:
    """Get the Router's Statistics Tables."""
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


def main(parser_obj: argparse.ArgumentParser) -> None:
    """Main Functional Body."""
    args = parser_obj.parse_args()
    statistics = get_router_stats_table(args.ip_address)
    # Iteratively Print Table Data
    for i, (stat_group_name, stat_group) in enumerate(statistics.items()):
        if i > 0:
            print("\n")
        print(stat_group_name)
        print('-'*80)
        for stat, data in stat_group.items():
            stat += ":"
            print(f"    {stat.ljust(22)}{data}")


if __name__ == "__main__":
    add_arguments(parser_obj=parser)
    main(parser_obj=parser)
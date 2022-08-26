# ZiplyFrontier Router Statistics Collector
*Scrape Ziply/Frontier Routers for Generic Network Statistics*

This single-file Python utility can be used when trying to interact with Ziply
(formerly Frontier) router devices to gather network statistics. This can be for
generating data used by services like Home Assistant, for automation purposes
such as configuring dynamic-DNS, etc.

### Command-Line-Interface
This script will support being called from the command-line, directly.

```shell
$ python3 ziply.py
WAN Summary
--------------------------------------------------------------------------------
    WAN Link:             Up
    WAN Connection:       Connected
    Link Type:            ONT WAN
    Connection Type:      DHCP Client
    Link Speed:           1000/Full Mbps
...more...
```

### Functional API
The module may also be used directly in other scripts.

```python
# Import the Utility Function
from ziply import get_router_stats_table

stats_dict = get_router_stats_table(ip_addr="192.168.254.254")
print(stats_dict)
# Prints the following:
# {"WAN Summary": {"WAN Link": "Up", "WAN Connection": "Connected",...}}
```

Should you decide that you'd rather just use the printing functionality, that's
an option, too! You may use the printing function directly without any trouble:

```python
# Import the Printing Function
from ziply import print_data_table

print_data_table(ip_addr="192.168.254.254")
# Prints the following:
#WAN Summary
#--------------------------------------------------------------------------------
#    WAN Link:             Up
#    WAN Connection:       Connected
#    Link Type:            ONT WAN
#    Connection Type:      DHCP Client
#    Link Speed:           1000/Full Mbps
#...more...
```


### Installation
At this time, this script is a single Python file that should be downloaded, and
vendored into software manually. There is no Python packaging, and said
packaging may, or may not, be developed later.

To install, simply download the `ziply.py` file and store in a location that may
be accessed, either by calling the file directly, or by importing as shown above
for more pragmatic use.

#### Requirements
Some additional packages are required for the full functionality of this tool.
At a bare minimum, [`requests`](https://pypi.org/project/requests/) and
[`BeautifulSoup`](https://pypi.org/project/beautifulsoup4/) are required.

Additionally, this tool is built in such a way that it may serve a simple web
API that will provide the latest statistics upon request of the endpoint:

> `http://<hostname-or-ip>/api/v1/stats`

To support this functionality, the additional packages:
[`FastAPI`](https://fastapi.tiangolo.com/) and
[`Uvicorn`](http://www.uvicorn.org/) are required.
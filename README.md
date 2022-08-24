# ZiplyFrontierRouterStats
*Scrape Ziply/Frontier Routers for Generic Network Statistics*


### Command-Line-Interface
This script will support being called from the command-line, directly.

```shell
$> python3 ziply.py
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

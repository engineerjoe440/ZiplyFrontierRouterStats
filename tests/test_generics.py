################################################################################
"""
pytest orchestrated testing framework for ziply script.

NOTE: Must be run from a location with direct access to a Ziply router.
"""
################################################################################

import sys
from pathlib import Path

# Ensure the Ziply Script is in Path
root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))

ROUTER_IP = "192.168.254.254"

# Import Ziply Script Components
from ziply import get_router_stats_table


def test_data_collector():
    """Verify that the Ziply script can access the requisite data from router"""
    stats = get_router_stats_table(ip_addr=ROUTER_IP)
    assert isinstance(stats, dict)
    assert len(stats) > 3


# END

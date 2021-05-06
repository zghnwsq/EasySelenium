import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), ".")))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from Utils.RPC.tools import get_host_ip, update_node_off


if __name__ == "__main__":
    host_ip = get_host_ip()
    update_node_off(host_ip)



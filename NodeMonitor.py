import requests
import time
import os

# Enter RPC credentials here 
url = "http://username:password@IPADDRESS:PORT/"

def rpc(method, params=[]):
    
    #Send an HTTP POST request to the Bitcoin JSON-RPC API and return the result.
    response = requests.post(url, json={"method": method, "params": params})
    return response.json()["result"]

#Print a list of peers, left-aligning the IP addresses in a fixed width field and right-aligning the other values.
def print_peers(peers, inbound=True): 
    # Determine the maximum width of the IP address column
    max_ip_width = 22

    # Print the list of peers
    for ip, total_mb, ct, lat in peers:
        # Use ANSI escape codes to color the IP address and colons, and add padding to the IP address and data transferred columns
        if inbound:
            # Print the last 21 characters of the IP address
            print(f"\033[91m{ip[-21:]:<{max_ip_width}s}\033[0m\033[91m: \033[93m{total_mb:>7.2f} MB\033[0m \033[95m{ct:>5}mins\033[0m \033[92m{int(round(lat*1000)):>6}ms\033[0m")
        else:
            # Print the last 21 characters of the IP address
            print(f"\033[94m{ip[-21:]:<{max_ip_width}s}\033[0m\033[94m: \033[93m{total_mb:>7.2f} MB\033[0m \033[95m{ct:>5}mins\033[0m \033[92m{int(round(lat*1000)):>6}ms\033[0m")

#uncomment the sleep below if you want to run on startup, it will crash if the node has not finished synchronizing so 90 seconds is usually an adequate buffer.
#time.sleep(90)
while True:
    # Clear the terminal screen
    os.system("cls")
    # Get various Bitcoin network statistics
    mempool_txs = rpc("getrawmempool")
    mempool_size = rpc("getmempoolinfo")["bytes"] / 1000
    peers = rpc("getpeerinfo")
    blockchain_info = rpc("getblockchaininfo")
    block_height = blockchain_info["blocks"]
    latest_block_hash = blockchain_info["bestblockhash"]
    latest_block = rpc("getblock", [latest_block_hash])
    latest_block_time = latest_block["time"]
    block_age = int(time.time() - latest_block_time)
    block_age_minutes = block_age // 60
    block_age_seconds = block_age % 60
    inbound_peers = []
    outbound_peers = []
    #build the structure for how the peer data is printed
    for peer in peers:
        addr = peer["addr"]
        conn_time = int((time.time() - peer["conntime"]) / 60)
        latency = peer.get("pingtime")
        if latency is None:
            latency = 0
        total_kb_sent = peer["bytessent"] / 1000
        total_kb_received = peer["bytesrecv"] / 1000
        total_mb = (total_kb_sent + total_kb_received) / 1000
        if peer["inbound"]:
            inbound_peers.append((addr, total_mb, conn_time, latency))
        else:
            outbound_peers.append((addr, total_mb, conn_time, latency))
    net_totals = rpc("getnettotals")
    total_mb_received = net_totals["totalbytesrecv"] / 1000000
    total_mb_sent = net_totals["totalbytessent"] / 1000000

    # Print the network statistics
    print(f"Current Block Height: {block_height}")
    print(f"Block Age: {block_age_minutes} minutes, {block_age_seconds} seconds")
    print(f"Number of Transactions in Mempool: {len(mempool_txs)}")
    print(f"Size of Mempool: {mempool_size:.2f} KB")
    print(f"Total MB received: {total_mb_received:.2f}")
    print(f"Total MB sent: {total_mb_sent:.2f}")
    print("=====================================================")
    print(f"Inbound Peers ({len(inbound_peers)}):")
    print_peers(inbound_peers)
    print(f"Outbound Peers ({len(outbound_peers)}):")
    print_peers(outbound_peers, inbound=False)
    print("=====================================================")
    time.sleep(30)


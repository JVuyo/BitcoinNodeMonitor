# Bitcoin Node Monitor

![index](https://user-images.githubusercontent.com/106835161/209446171-b58dc8d1-0cfa-4811-82e2-c480b76baa40.png)

![Screenshot 2022-12-24 002058](https://user-images.githubusercontent.com/106835161/209446114-e8a2db6b-fc4c-47d1-b66a-55434b628f36.png)

This script is a tool for monitoring various statistics about a Bitcoin node. When run it displays information about the latest block and your peers, including their IP, the total data transferred between your nodes, how long they've been connected to your node and their latency. 
    
Onion Addresses are shortened for aesthetic purposes but can be returned to their original length by changing the "max_ip_width" to 67 and altering line 26/29 so that "-21" is 0.

To use it you need to enter your RPC credentials in the url variable at the top of the script. The format of the URL should be http://username:password@IPADDRESS:PORT/ and the credentials should match those set in your bitcoin.conf file. 

To run the script, simply execute it using Python or drag into your console and hit enter. 
The script will run indefinitely, updating in an interval designated by the last "sleep" command in the script. To stop the script, use the CTRL+C keyboard shortcut.

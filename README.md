# omci-wireshark-dissector
Exported from code.google.com/p/omci-wireshark-dissector

# Requirements

 - 64 bit Ubuntu 16.04 LTS Desktop
 - Wireshark 2.6.3 (with lua 5.4.2)

# Usage

- You must add the lua files "BinDecHex" and "omci" to proper Wireshark plugin directory:

```sh
cp BinDecHex.lua ~/.config/wireshark/plugins
cp omci.lua ~/.config/wireshark/plugins
```
- You must get the OMCI log that includes "omci ... capture:" lines. This process may vary due to ONT device type, brand and version. I use the following commands for my ONT:

```sh
> omci capture control --state on
-- send OMCI messages from OLT
> omci capture control --state off
> omci capture save --filename omci.msg
```
- You must run the omciToPcap.py file. It asks you the full path of the omci.msg file. Enter the proper full path of the file.
There is an example:

```sh
python omciToPcap.py
Please enter the file path of OMCI log file:/home/gamzeab/omci_lua/omci-wireshark-dissector/resources/omci.msg
```
If the python script runs successfully, you must see the following lines:

```sh
Input from: omciForPcap.txt
Output to: omci.pcap
Output format: PCAP
Wrote packet of 62 bytes.
...
Read 74 potential packets, wrote 74 packets (5796 bytes).
```
The output file (omci.pcap) will be generated in the directory where the script is run. Then, you can open this file using Wireshark.

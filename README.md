# preBootPi
Prepare a Raspberry Pi befor first Boot

## fundamentals
When I prepare a Raspberry Pi for a project, I like to use fix IP Addresses. Normally I user [Pi Imager](https://www.raspberrypi.com/software/) to flash an SD-Card or an SSD-Drive.

After that I have to login to setup the Fix IP. That is OK for a single Pi but if you setup a Kubernetes cluster it is hard work.
At that point is started to create preBootPi, for easy prepare the Pi before the first Boot.

[Pi Imager](https://www.raspberrypi.com/software/) make a great Job. With version 1.8 or higher it makes the work easier.
Depending on the operating system it writes files to the Boot Partition that’s prepare the Pi on its first boot. 

## Raspbian (Raspberry OS)

On **Raspbian (Raspberry OS)** it prepares the file “*firstrun.sh*”. 

## Ubuntu

On **Ubuntu** it's the files “*user-data*” and “*network-config*”. preBootPi will modify these files to add some more setting. And it will help to manage the nodes in your Cluster.

## Install

Clone this repository. Then copy or rename the file **sanples-nodes.json** in the nodes folder to nodes.json.

```bash
git clone https://github.com/Thro42/preBootPi.git
cd preBootPi
pip install -r requirements.txt
rename nodes\sanples-nodes.json nodes.json
```

## Using
To using the tool, open a comandline/terminal window, go to the preBootPi folder and start the main.py.

```bash
python main.py
```
on the first run you see a folowing Window, for selecting the **node.json** file.

![node Base](/images/nodebase.png)

open the nodes folder and select **node.json**. After select an press open you see the main Window with the samples nodes.

![main Window](/images/main-start.png)

### add a node

### edit a node

### Setup

for Raspian you need to select the Templates. open the Menu File->Setup->Raspberry OS

![Setup Rasbian](/images/menu-pisetup.png)



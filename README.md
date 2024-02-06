# preBootPi
Prepare a Raspberry Pi befor first Boot

## fundamentals
When I prepare a Raspberry Pi for a project, I like to use fix IP Addresses. Normally I user [Pi Imager](https://www.raspberrypi.com/software/) to flash an SD-Card or an SSD-Drive.

After that I have to login to setup the Fix IP. That is OK for a single Pi but if you setup a Kubernetes cluster it is hard work.
At that point is started to create preBootPi, for easy prepare the Pi before the first Boot.

[Pi Imager](https://www.raspberrypi.com/software/) make a great Job. With version 1.8 or higher it makes the work easier.
Depending on the operating system it writes files to the Boot Partition that’s prepare the Pi on its first boot. On **Raspbian (Raspberry OS)** it prepares the file “*firstrun.sh*” on **Ubuntu** it's the files “*user-data*” and “*network-config*”. preBootPi will modify these files to add some more setting. And it will help to manage the nodes in your Cluster.

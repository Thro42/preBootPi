#!/bin/bash

set +e

CURRENT_HOSTNAME=`cat /etc/hostname | tr -d " \t\n\r"`
if [ -f /usr/lib/raspberrypi-sys-mods/imager_custom ]; then
   /usr/lib/raspberrypi-sys-mods/imager_custom set_hostname [hostname]
else
   echo [hostname] >/etc/hostname
   sed -i "s/127.0.1.1.*$CURRENT_HOSTNAME/127.0.1.1\t[hostname]/g" /etc/hosts
fi
FIRSTUSER=`getent passwd 1000 | cut -d: -f1`
FIRSTUSERHOME=`getent passwd 1000 | cut -d: -f6`
if [ -f /usr/lib/raspberrypi-sys-mods/imager_custom ]; then
   /usr/lib/raspberrypi-sys-mods/imager_custom enable_ssh -k 'ssh-rsa [ssh-rsa]'
else
   install -o "$FIRSTUSER" -m 700 -d "$FIRSTUSERHOME/.ssh"
   install -o "$FIRSTUSER" -m 600 <(printf "ssh-rsa [ssh-rsa]") "$FIRSTUSERHOME/.ssh/authorized_keys"
   echo 'PasswordAuthentication no' >>/etc/ssh/sshd_config
   systemctl enable ssh
fi
if [ -f /usr/lib/userconf-pi/userconf ]; then
   /usr/lib/userconf-pi/userconf '[username]' '[passwd]'
else
   echo "$FIRSTUSER:"'[passwd]' | chpasswd -e
   if [ "$FIRSTUSER" != "[username]" ]; then
      usermod -l "[username]" "$FIRSTUSER"
      usermod -m -d "/home/[username]" "[username]"
      groupmod -n "[username]" "$FIRSTUSER"
      if grep -q "^autologin-user=" /etc/lightdm/lightdm.conf ; then
         sed /etc/lightdm/lightdm.conf -i -e "s/^autologin-user=.*/autologin-user=[username]/"
      fi
      if [ -f /etc/systemd/system/getty@tty1.service.d/autologin.conf ]; then
         sed /etc/systemd/system/getty@tty1.service.d/autologin.conf -i -e "s/$FIRSTUSER/[username]/"
      fi
      if [ -f /etc/sudoers.d/010_pi-nopasswd ]; then
         sed -i "s/^$FIRSTUSER /[username] /" /etc/sudoers.d/010_pi-nopasswd
      fi
   fi
fi
#WLAN
if [ "[wifi-state]" == "enable"]; then
if [ -f /usr/lib/raspberrypi-sys-mods/imager_custom ]; then
   /usr/lib/raspberrypi-sys-mods/imager_custom set_wlan '[ssid]' '[ssid_pwd]' '[wifi-contry]'
else
cat >/etc/wpa_supplicant/wpa_supplicant.conf <<'WPAEOF'
country=[wifi-contry]
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
ap_scan=1

update_config=1
network={
	ssid="[ssid]"
	psk=[ssid_pwd]
}

WPAEOF
   chmod 600 /etc/wpa_supplicant/wpa_supplicant.conf
   rfkill unblock wifi
   for filename in /var/lib/systemd/rfkill/*:wlan ; do
       echo 0 > $filename
   done
fi
fi
# Fix IP
if [ -f /boot/firmware/interfaces.net ]; then
   cp /boot/firmware/interfaces.net /etc/network/interfaces
fi
if [ -f /boot/dhcpcd.conf ]; then
   cp /boot/dhcpcd.conf /etc/dhcpcd.conf
fi
#
if [ -f /usr/lib/raspberrypi-sys-mods/imager_custom ]; then
   /usr/lib/raspberrypi-sys-mods/imager_custom set_keymap 'de'
   /usr/lib/raspberrypi-sys-mods/imager_custom set_timezone 'Europe/Berlin'
else
   rm -f /etc/localtime
   echo "Europe/Berlin" >/etc/timezone
   dpkg-reconfigure -f noninteractive tzdata
cat >/etc/default/keyboard <<'KBEOF'
XKBMODEL="pc105"
XKBLAYOUT="de"
XKBVARIANT=""
XKBOPTIONS=""

KBEOF
   dpkg-reconfigure -f noninteractive keyboard-configuration
fi
rm -f /boot/firstrun.sh
sed -i 's| systemd.run.*||g' /boot/cmdline.txt
exit 0
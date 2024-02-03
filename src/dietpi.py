import os.path
import configparser
from configobj import ConfigObj
from PySide6.QtWidgets import QMessageBox
from src.config import *

class DietPiSettings():
    def __init__(self, parent, settings, drive, node):
        self.parent = parent
        self.drive = drive
        self.node = node
        self.settings = settings
        #self.config = configparser.ConfigParser()

    def check_sd_os(self):
        user_file = self.drive + DIETPI_OUTPUT
        print('Check ' + user_file)
        return os.path.isfile(user_file)
    
    def save_dietpi_flat(self):
        config = {}
        # Settings
        config['AUTO_SETUP_ACCEPT_LICENSE'] = '1'
        # Local
        config['AUTO_SETUP_LOCALE'] = 'de_DE.UTF-8'
        config['AUTO_SETUP_KEYBOARD_LAYOUT'] = 'de'
        config['AUTO_SETUP_TIMEZONE'] = 'Europe/Berlin'
        # Statik IP
        config['AUTO_SETUP_NET_USESTATIC'] = '1'
        config['AUTO_SETUP_NET_STATIC_IP'] = self.node['ip']
        if self.settings['ip_mask'] == '16':
            config['AUTO_SETUP_NET_STATIC_MASK'] = '255.255.0.0'
        else:
            config['AUTO_SETUP_NET_STATIC_MASK'] = '255.255.255.0'
        config['AUTO_SETUP_NET_STATIC_GATEWAY'] = self.settings['gateway']
        sep = ' '
        nameservers = sep.join(self.settings['nameservers'])
        config['AUTO_SETUP_NET_STATIC_DNS'] = nameservers

    def save_dietpi(self):
        # Settings
        filename = self.drive + DIETPI_OUTPUT
        config = ConfigObj(filename)
        config['AUTO_SETUP_ACCEPT_LICENSE'] = '1'
        # Local
        config['AUTO_SETUP_LOCALE'] = 'de_DE.UTF-8'
        config['AUTO_SETUP_KEYBOARD_LAYOUT'] = 'de'
        config['AUTO_SETUP_TIMEZONE'] = 'Europe/Berlin'
        # eth OR wifi
        if self.node['network'] == 'eth':
            config['AUTO_SETUP_NET_ETHERNET_ENABLED'] = '1'
            config['AUTO_SETUP_NET_WIFI_ENABLED'] = '0'
        elif self.node['network'] == 'wifi':
            config['AUTO_SETUP_NET_ETHERNET_ENABLED'] = '0'
            config['AUTO_SETUP_NET_WIFI_ENABLED'] = '1'
        # Statik IP
        config['AUTO_SETUP_NET_USESTATIC'] = '1'
        config['AUTO_SETUP_NET_STATIC_IP'] = self.node['ip']
        if self.settings['ip_mask'] == '16':
            config['AUTO_SETUP_NET_STATIC_MASK'] = '255.255.0.0'
        else:
            config['AUTO_SETUP_NET_STATIC_MASK'] = '255.255.255.0'
        config['AUTO_SETUP_NET_STATIC_GATEWAY'] = self.settings['gateway']
        sep = ' '
        nameservers = sep.join(self.settings['nameservers'])
        config['AUTO_SETUP_NET_STATIC_DNS'] = nameservers
# Hostname
        config['AUTO_SETUP_NET_HOSTNAME'] = self.node['name']
# ssh
        config['AUTO_SETUP_SSH_PUBKEY'] = 'ssh-rsa ' + self.settings['ssh_rsa']
#AUTO_SETUP_AUTOSTART_TARGET_INDEX
        config['AUTO_SETUP_AUTOSTART_TARGET_INDEX'] = '7'
        #
        config.write()

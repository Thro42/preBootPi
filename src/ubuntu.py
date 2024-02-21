import yaml
import os.path
from src.config import *

class UbuntuSettings():
    def __init__(self, parent, drive, node):
        self.drive = drive
        self.node = node
        self.settings = parent.model.getSettings()
        self.appSetting = parent.appSetting
        self.net_config = {}
        self.net_config['version'] = 2
        #self.udata_file = self.appSetting.getOption()
        self.user_data = {}
#        with open(USER_DATA_TEMPLATE, 'r') as file:
#            self.user_data = yaml.safe_load(file)

    def check_sd_os(self):
        user_file = self.drive + NET_CONF_OUTPUT
        return os.path.isfile(user_file)
    
 #   def save_net_config(self):
 #       ip = self.node['ip']+'/'+self.settings['ip_mask']
 #       sep = ','
 #       nameservers = sep.join(self.settings['nameservers'])
 #       if self.node['network'] == 'eth':
 #           teplite_file = NET_CONF_TEMPLATE_ETH
 #       elif self.node['network'] == 'wifi':
 #           teplite_file = NET_CONF_TEMPLATE_WIFI
 #       if os.path.isfile(teplite_file):
 #           with open(teplite_file, 'r') as file:
 #               data = file.read()
 #               data = data.replace('[ip_address]', ip)
 #               data = data.replace('[local-domain]', self.settings['domain'])
 #               data = data.replace('[gateway]', self.settings['gateway'])
 #               data = data.replace('[nameservers]', nameservers)
 #               data = data.replace('[ssid]', self.settings['access_point'])
 #               data = data.replace('[ssid_pwd]', self.settings['access_passwd'])
 #               net_file = self.drive + NET_CONF_OUTPUT
 #               print(net_file)
 #               with open(net_file, 'w') as file:
 #                   file.write(data)

    def save_net_config(self):
        net_config = {}
        ips = []
        ips.append(self.node['ip']+'/'+self.settings['ip_mask'])
        search = []
        search.append(self.settings['domain'])
        addresses = self.settings['nameservers']
        nameservers = {'search':search, 'addresses':addresses}
        interface = {}
        interface['eth0'] = {'dhcp4': False, 'optional': True}
        eth = interface['eth0']
        eth['addresses'] = ips
        routes = []
        routes.append({'to':'default', 'via': self.settings['gateway']})
        eth['routes'] = routes
        eth['nameservers'] = nameservers
        self.net_config['ethernets'] = interface
        net_config['network'] = self.net_config
        net_file = self.drive + NET_CONF_OUTPUT
        print(net_file)
        with open(net_file, 'w', newline='\n') as yaml_file:
            yaml.dump(net_config, yaml_file)
            
    def save_net_config_alt(self):
        net_config = {}

        ips = []
        ips.append(self.node['ip']+'/'+self.settings['ip_mask'])
        #search = []
        #search.append(self.settings['domain'])
        search = '['+ self.settings['domain'] + ']'
        addresses = self.settings['nameservers']
        sep = ','
        #addresses = '[' + sep.join(self.settings['nameservers']) + ']'
        nameservers = {}
        #nameservers['nameservers'] = {'search':search, 'addresses':addresses}
        nameservers = {'search':search, 'addresses':addresses}
        if self.node['network'] == 'eth':
            neteth = {'eth0': {'dhcp4': False, 'addresses': ips, 'gateway4': self.settings['gateway'], 'nameservers':nameservers}}
            self.net_config['ethernets'] = neteth
        elif self.node['network'] == 'wifi':
            netwifi = {'wlan0': {'dhcp4': False, 'addresses': ips, 'gateway4': self.settings['gateway'], 'nameservers':nameservers}}
            self.net_config['wifis'] = netwifi
        net_file = self.drive + NET_CONF_OUTPUT
        print(net_file)
        net_config['network'] = self.net_config
        with open(net_file, 'w', newline='\n') as yaml_file:
            yaml.dump(net_config, yaml_file)
    
    def save_user_data_yaml(self):
        user_in_file = self.drive + USER_DATA_OUTPUT
        if os.path.isfile(user_in_file) != True:
            user_in_file = USER_DATA_TEMPLATE
        with open(user_in_file, 'r') as file:
            self.user_data = yaml.safe_load(file)
        file.close()
        self.user_data['hostname'] = self.node['name']
        self.user_data['users'][0]['name'] = self.settings['firstuser']
        self.user_data['users'][0]['passwd'] = self.settings['passwd']
        rsa = 'ssh-rsa ' + self.settings['ssh_rsa']
        self.user_data['users'][0]['ssh_authorized_keys'][0] = rsa
        timezone = self.appSetting.getDefaultOption('timezone')
        self.user_data['timezone'] = timezone
        localectl = 'localectl set-x11-keymap "' + self.appSetting.getDefaultOption('keyboard_layout') + '" pc105'
        self.user_data['runcmd'][0] = localectl
        user_file = self.drive + USER_DATA_OUTPUT
        print(user_file)
        with open(user_file, 'w', newline='\n') as yaml_file:
            yaml.dump(self.user_data, yaml_file)

    def save_user_data(self):
        with open(USER_DATA_TEMPLATE, 'r') as file:
            data = file.read()
            data = data.replace('[timezone]', self.appSetting.getDefaultOption('timezone'))
            data = data.replace('[keyboard_layout]', self.appSetting.getDefaultOption('keyboard_layout'))
            data = data.replace('[hostname]', self.node['name'])
            data = data.replace('[username]', self.settings['firstuser'])
            data = data.replace('[passwd]', self.settings['passwd'])
            rsa = 'ssh-rsa ' + self.settings['ssh_rsa']
            data = data.replace('[ssh-rsa]', self.settings['ssh_rsa'])
            user_file = self.drive + USER_DATA_OUTPUT
            print(user_file)
            with open(user_file, 'w', newline='\n') as file:
                file.write(data)

    def update_cmdline(self):
        user_file = self.drive + 'cmdline.txt'
        if os.path.isfile(user_file):
            print(user_file)
            with open(user_file, 'r') as file:
                data = file.read()
                #print(data)
                file.close()
                if data.endswith("splash\n"):
                    print('Append cgroup_enable')
                    # data = data + ' cgroup_enable=cpuset cgroup_enable=memory cgroup_memory=1'
                    ndata = data.replace("\n", " cgroup_enable=cpuset cgroup_enable=memory cgroup_memory=1\n")
                    with open(user_file, 'w', newline='\n') as file:
                        file.write(ndata)

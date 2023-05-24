import requests
import subprocess
import json
import os

def check_dns_resolution(hostname):
    command = ['dig', '+short', hostname]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        dns_output = result.stdout.strip()
        if dns_output:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False

def setupdns(hostname, ip4):
  data = { "hostname": hostname, "ip_address": ip4 }
  url = "https://dns.openknowit.com/dns"
  headers = {"Content-Type": "application/json"}
  response = requests.post(url, json=data, headers=headers)

  if response.status_code == 200:
    print("DNS entry added successfully.")
    return True
  else:
    print(f"Failed to add DNS entry. Status code: {response.status_code}")
    return False

def checkservice():
  hostname = 'inabox.openknowit.com'
  if check_dns_resolution(hostname):
    print(f"The DNS resolution for {hostname} is correct.")
  else:
     print(f"The DNS resolution for {hostname} is incorrect or unavailable.")
     setupdns('inabox', '88.99.58.240')
     os.sleep(5)
     if check_dns_resolution(hostname):
       print(f"The DNS resolution for {hostname} is correct.")
     else:
       print(f"The DNS resolution for {hostname} is incorrect or unavailable.")
       exit(1)
  return 0

def read_config():
  try:
    with open("./inabox.json", "r") as inabox_config:
      inabox_config = json.load(inabox_config)
      print(inabox_config)
  except:
    print("Failed to read config file")
    exit(1)
    try:
      iso_path = inabox_config['iso_path']
      preceed_path = inabox_config['preceed_path']
    except:
      print("Failed to read iso or preceed path")
      inabox_config['iso_path'] = "/tmp/debian10,iso"
      inabox_config['preceed_path'] = "preceed.cfg"
      try:
        size = inabox_config['vm_size']
        if size in ['small', 'medium', 'large']:
          print("We have a valid vm size")
        else:
          print("We dont have a valid vm size")
          inabox_config['vm_size'] = "small"
      except:
        inabox_config['vm_size'] = "small"
      
      try: 
        network = inabox_config['vm_network']
        if network in ['inabox', 'inabox2']:
          print("We have a valid network")  
        else:
          print("We dont have a valid network")
          inabox_config['vm_network'] = "inabox"
      except:
        inabox_config['vm_network'] = "inabox"


          
        network = inabox_config['vm_network']

      inabox_config['vm_network'] = "inabox"
      inabox_config['vm_name'] = "inabox"
      inabox_config['disk_size'] = "10G"
      inabox_config['ram_size'] = "1024"
      inabox_config['vm_ip'] = "" 
      inabox_config['vm_netmask'] = ""
      inabox_config['vm_gateway'] = ""
      inabox_config['vm_dns'] = ""
      inabox_config['vm_domain'] = ""
      inabox_config['vm_hostname'] = ""
      inabox_config['vm_user'] = ""
      inabox_config['vm_password'] = ""
      inabox_config['vm_root_password'] = ""
      inabox_config['vm_ssh_key'] = ""
      inabox_config['vm_ssh_user'] = ""
      inabox_config['vm_ssh_password'] = ""
      inabox_config['vm_ssh_port'] = ""
      inabox_config['vm_ssh_key'] = ""

  return inabox_config

def check_the_hosts(hosts):
   for group in hosts.keys():
      print("---------------")
      print(hosts[group]['group_size'])
      for memeber in hosts[group]['members']:
        print(memeber)
        if check_if_we_have_a_vm(memeber):
          print("We have a vm")
        else:
          print("We dont have a vm")
          create_virtual_server(vm_name)



      print("---------------")


def download_file(url, filename):
  r = requests.get(url, allow_redirects=True)
  try:
    open(filename, 'wb').write(r.content)
    return True
  except:
    return False
  
def print_status():
  print("Status:")
  print("-------")
  print("DNS: OK")
  print("VM: OK")
  print("SSH: OK")
  print("-------"
        )

  

def create_virtual_server(iso_path, preceed_path, vm_name, disk_size, ram_size):
    # check if we have a preceedfile 
    if os.path.exists(preceed_path):
      print("Found preceed.cfg")
    else:
      print("No preceed.cfg found")
      if download_file("https://artifacts.openknowit.com/files/inabox/debian10.preceed.cfg", "preceed.cfg"):
        print("Downloaded preceed.cfg")
      else:
        print("Failed to download preceed.cfg")
        exit(1)

    if os.path.exists(iso_path):
      print("Found iso")
    else:
      if download_file("https://artifacts.openknowit.com/files/inabox/debian10.iso"):
        print("Downloaded iso")
      else: 
        print("Failed to download iso")
        exit(1)
      
    # Construct the virt-install command with preseeding options
    command = [
        'virt-install',
        '--name', vm_name,
        '--memory', str(ram_size),
        '--disk', f'size={disk_size}',
        '--cdrom', iso_path,
        '--os-variant', 'debian10',
        '--network', 'bridge=virbr0',
        '--graphics', 'none',
        '--console', 'pty,target_type=serial',
        '--extra-args', f'auto=true priority=critical url=file:/preseed.cfg'
    ]

    # Execute the virt-install command
    process = subprocess.run(command)
    if process.returncode == 0:
        print(f"Virtual server {vm_name} created successfully.")
    else:
        print(f"Failed to create virtual server {vm_name}.")
        exit(1)




   
def main():
  print("Starting inabox")
  checkservice()
  myconf = read_config()
  print(myconf['domain'])
  hosts  = myconf['hosts']
  try:
    check_the_hosts(hosts)
  except:
    print("Failed to check the hosts")
    exit(1)


  
  return 0





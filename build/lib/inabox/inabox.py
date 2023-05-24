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
  return inabox_config

def check_the_hosts(hosts):
   for group in hosts.keys():
      print("---------------")
      print(hosts[group]['group_size'])
      for memeber in hosts[group]['members']:
        print(memeber)

      print("---------------")



import subprocess

def create_virtual_server(iso_path, vm_name, disk_size, ram_size):
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
    subprocess.run(command)

# Example usage
iso_path = '/path/to/debian.iso'
vm_name = 'my_virtual_server'
disk_size = '20'
ram_size = 2048

create_virtual_server(iso_path, vm_name, disk_size, ram_size)


   
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





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
  return inabox_config

def check_the_hosts(hosts, meta_data):
   for group in hosts.keys():
      mysize = hosts[group]['group_size']
      size = meta_data['group_sizes'][0][mysize]
      for memeber in hosts[group]['members']:
        vm_name = memeber['hostname']
        if check_if_we_have_a_vm(vm_name):
          print("We have a vm")
        else:
          print("We dont have a vm")
          size
          create_virtual_server(vm_name, size, meta_data)




      print("---------------")

def  check_if_we_have_a_vm(vm_name, ):
  command = ['virsh', 'list', '--all']
  try:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    virsh_output = result.stdout.strip()
    if vm_name in virsh_output:
      return True
    else:
      return False
  except subprocess.CalledProcessError:
    return False

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

def mb_to_bytes(mb):
  bytes = mb * 1024 * 1024
  return bytes 

def create_virtual_server(hostname, size, meta_data):
    # check if we have a preceedfile 
    if os.path.exists(meta_data['preceed_path']):
      print("Found preceed.cfg")
    else:
      print("No preceed.cfg found")
      if download_file("https://artifacts.openknowit.com/files/inabox/debian10.preceed.cfg", meta_data['preceed_path']):
        print("Downloaded preceed.cfg")
      else:
        print("Failed to download preceed.cfg")
        exit(1)

    if os.path.exists(meta_data['iso_path']):
      print("Found iso")
    else:
      if download_file("https://artifacts.openknowit.com/files/inabox/debian10.iso", meta_data['iso_path']):
        print("Downloaded iso")
      else: 
        print("Failed to download iso")
        exit(1)
      
    # Construct the virt-install command with preseeding options
    if size['disk_size'] == "auto":
      size['disk_size'] = mb_to_bytes(10000)
    if size['disk_size'].endswith("M"):
      size['disk_size'] = mb_to_bytes(int(size['disk_size'].replace("M", "")))
    if size['disk_size'].endswith("G"):
      size['disk_size'] = mb_to_bytes(int(size['disk_size'].replace("G", "")) * 1024)
    if size['disk_size'].endswith("T"):
      size['disk_size'] = mb_to_bytes(int(size['disk_size'].replace("T", "")) * 1024 * 1024)
      
    command = [
        'virt-install',
        '--name', hostname,
        '--memory', str(size["memory"]),
        '--disk', f'size={size["disk_size"]}',
        '--cdrom', meta_data['iso_path'],
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
  check_the_hosts(hosts, myconf)
  try:
    check_the_hosts(hosts, myconf)
  except:
    print("Failed to check the hosts")
    exit(1)


  
  return 0





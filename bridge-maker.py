#!/usr/bin/env python3
#############################
#  Automatic bridge maker   #
#############################
# Author: Marcos Dos Santos #
# Github: dotvectortech     #
#############################

# Imports.
import os
import re

# Is ip, nmcli and virsh installed?
print("Checking for 'ip', 'nmcli' and 'virsh'")
if os.system('which ip') == 0:
    found = 1
else:
    print()
    print("No command 'ip' found. Exiting")
    quit()

if os.system('which nmcli') == 0:
    found += 1
else:
    print()
    print("No command 'nmcli' found. Exiting")
    quit()

if os.system('which virsh') == 0:
    found += 1
else:
    print()
    print("No command 'virsh' found.")

# Main function
def y_n(question,answer,fail):
    choice = None
    while choice == None:
        print(question)
        choice = input('(y/N): ')
        if choice == 'y' or choice == 'Y' or choice == 'yes' or choice == 'Yes':
            print(answer)
        elif choice == '' or choice == 'n' or choice == 'N' or choice == 'no' or choice == 'No':
            print(fail)
            quit()
        else:
            print('Invalid option selected. Exiting')
            quit()

# Making sure the user is ok not installing Virt-Manager part of the script
if found != 3:
    y_n('Virt-Manager part of the script will not work, are you sure you want to continue?',
            'Ok, ommiting Virt-Manager script',
            'Canceling')
print()

# Generates a file with all the interfaces.
os.system('ip link > network.txt')
with open('./network.txt','r') as f:
    network_cards_raw = f.read()

# Parse the finds for later use.
network_cards = list()

if re.findall('[0-9]: [0-9,a-z]+:',network_cards_raw):
    interface = re.findall('[0-9]: ([0-9,a-z]+):',network_cards_raw)
    for item in interface:
        network_cards.append(item)

# Selecting the right interface to do the bridge.
choice = None
number = 0

print('This is the list of interfaces able:')

for n in network_cards:
    number += 1
    print(number,'-',n)

while choice == None:
    choice = input('Select the correct number of the interface you want to make bridge: ')
    try:
        choice = int(choice)
    except:
        print('Invalid character, only numbers. Exiting')
        quit()
       
choice = choice - 1

try:
    correct_interface = network_cards[choice]
except:
    print('Invalid number selected. Exiting')
    quit()
print()

# Making sure the interface is the correct one before going.
print('Interface selected:',correct_interface)
y_n('Are you sure thats the right interface?',
        'Ok, starting nmcli work',
        'Canceling')
print()

# Checking nmcli name.
cmd = 'nmcli con show --active | grep ' + correct_interface + ' > nm_name.txt'
os.system(cmd)
with open('./nm_name.txt','r') as f:
    nm_name_raw = f.read()
nm_name = nm_name_raw.split('  ')
nm_name = nm_name[0]

# Starts the nmcli work.
print()
cmd = 'sudo nmcli con add ifname br0 type bridge con-name br0'
os.system(cmd)
cmd = 'sudo nmcli con add type bridge-slave ifname ' + correct_interface + ' master br0'
os.system(cmd)
cmd = 'sudo nmcli con modify br0 bridge.stp no'
os.system(cmd)
cmd = 'sudo nmcli con down ' + '"' + nm_name + '"'
os.system(cmd)
cmd = 'sudo nmcli con up br0'
os.system(cmd)
print()

if found != 3:
    print('Script done!\nHave a nice day')
    quit()

# Ask about adding br0 to virsh
y_n('Do you want to add br0 to Virt-Manager network as default?',
        'Ok, adding br0 to Virt-Manager!',
        'Script done!\nHave a nice day')

# Virsh work
print()
cmd = 'virsh net-define ./br0.xml'
os.system(cmd)
cmd = 'virsh net-start br0'
os.system(cmd)
cmd = 'virsh net-autostart br0'
os.system(cmd)
print()
print('Script done!\nHave a nice day')
quit()

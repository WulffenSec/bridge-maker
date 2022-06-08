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


# Making sure the user is ok not installing Virt-Manager part of the script
choice = None
if found != 3:
    while choice == None:
        print('Virt-Manager part of the script will not work, are you sure you want to continue?')
        choice = input('(y/N): ')
        if choice == 'y' or choice == 'Y' or choice == 'yes' or choice == 'Yes':
            print('Ok, ommiting Virt-Manager script') 
        elif choice == '' or choice == 'n' or choice == 'N' or choice == 'no' or choice == 'No':
            print('Canceling')
            quit()
        else:
            print('Invalid option selected. Exiting')

print()

# Generates a file with all the interfaces.
os.system('ip link > network.txt')
network_cards_raw = open('./network.txt','r')

# Parse the finds for later use.
network_cards = list()

for card in network_cards_raw:
    if re.findall('[0-9]: [0-9,a-z]+:',card):
        interface = re.findall('[0-9]: ([0-9,a-z]+):',card)
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

# Making sure the interface is the correct one before going.
choice = None

while choice == None:
    print('Are you sure the right interface is',correct_interface,'?')
    choice = input('(y/N): ')

if choice == 'y' or choice == 'Y' or choice == 'yes' or choice == 'Yes':
    print('Ok, starting nmcli work')
elif choice == '' or choice == 'n' or choice == 'N' or choice == 'no' or choice == 'No':
    print('Canceling')
    quit()
else:
    print('Invalid option selected. Exiting')
    quit()

# Checking nmcli name.
cmd = 'nmcli con show --active | grep ' + correct_interface + ' > nm_name.txt'
os.system(cmd)
nm_name_raw = open('./nm_name.txt','r')
for n in nm_name_raw:
    n = n.split('  ')
    nm_name = n[0]

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
choice = None
while choice == None:
    print('Do you want to add br0 to Virt-Manager network as default?')
    choice = input('(y/N): ')

if choice == 'y' or choice == 'Y' or choice == 'yes' or choice == 'Yes':
    print('Ok, adding br0 to Virt-Manager!')
elif choice == '' or choice == 'n' or choice == 'N' or choice == 'no' or choice == 'No':
    print('Script done!\nHave a nice day')
    quit()
else:
    print('Invalid option selected. Exiting')

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

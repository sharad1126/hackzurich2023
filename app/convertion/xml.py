import xml.etree.ElementTree as ET
import re
from more_itertools import locate

root_node = ET.parse('/Users/sharadagarwal/Downloads/sample_set/within-resource.xml').getroot()

for k in range(len(root_node)):
	c = 0
	mail = False
	iban = False
	address = False
	phone = False
	for x in root_node[k]:
		tags = []
		values = []
		tags.append(x.tag)
		values.append(x.text) 
		for tag in tags:
			if re.search('name',tag):
				x = tags.index(tag)
				if values[x]:
					print('name: ' + values[x])
					c = c + 1
			if re.search('mail',tag):
				y=tags.index(tag)
				if values[y]:
					print('mail:' + values[y])
					mail = True
			if re.search('iban',tag) or re.search('IBAN',tag):
				z=tags.index(tag)
				if values[z]:
					print('iban: ' + values[z])
					iban = True
			if re.search('phone',tag):
				b=tags.index(tag)
				if values[b]:
					print('phone: ' + values[b])	
					phone = True
			if re.search('ddress',tag):
				a=tags.index(tag)
				if values[a]:
					print('address: ' + values[a])	
					address = True
	if (((c == 2) and (mail or iban or phone or address)) or (mail and (iban or address or phone))):	
		print('sensitive')	
		break




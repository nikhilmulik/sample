#!/usr/bin/env python
"""
This script provides encryption algorithm.
"""
__appId__ = ''
__version__ = '1'

class Encryption():
  def Encode(self,data):	
	pwd = ""
	pwdLength = len(pwd)
	key =list()
	counter = list()
	Zcrypt = ''
	for i in range(255):
		key.append(ord(pwd[(i % pwdLength):(i % pwdLength)+ 1]))
		counter.append(i)
	x = 0
	for i in range(255):
		x = (x + counter[i] + key[i]) % 255
		temp = counter[i]
		counter[i] = counter[x]
		counter[x] = temp
	a = 0
	j = 0
	for i in range(len(data)):
		a = (a + 1) % 255
		j = (j + counter[a]) % 255
		temp = counter[a]
		counter[a] = counter[j]
		counter[j] = temp
		k = counter[(counter[a] + counter[j]) % 255]
		Zcipher = ord(data[i:i+1]) ^ k			
		Zcrypt += chr(Zcipher)
	return Zcrypt
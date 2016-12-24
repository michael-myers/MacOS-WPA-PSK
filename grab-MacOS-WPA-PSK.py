#!/usr/bin/env python
"""
    Grab the wireless key from Macs' non-volatile RAM (NVRAM)
    
    License:	
    Public Domain

    About:
    grab-MacOS-WPA-PSK is a tool to retrieve and decode the current wireless network key.
    It is just a proof-of-concept to remind users that Apple treats this value as non-secret.
    You might have expected it to require root to obtain, and be protected in the Keychain. Nope.

    Why not recover the passphrase?:
    First, because it is unimportant, and not actually used to join a network.
    Second, you cannot efficiently work backwards to the wifi passphrase from the PSK.
    The PSK is generated from the passphrase using PBKDF2 with 4096 rounds of HMAC-SHA1 using the
    SSID as a nonce, making brute-force guessing expensive-ish, and most people use long-ish
    passphrases so it won't even be a matter of guessing all 10 or 12 character sequences, which
    itself would be too many.

    Usage:
        python grab-MacOS-WPA-PSK.py

    Alternately:
        chmod +x ./grab-MacOS-WPA-PSK.py
        ./grab-MacOS-WPA-PSK.py

    Changelog:
    1.0:    initial release. None of this 0.x crap. It works, so it's 1.0.
"""
from __future__ import print_function
import os
import binascii

# Get the current network's (encoded) PSK, available to anyone, with the nvram command:
p = os.popen('nvram 36C28AB5-6566-4C50-9EBD-CBB920F83843:current-network',"r")
nvRAMvariable = p.readline().split()

# The second field contains the SSID.
print ("Your SSID: ", end="")

# A while loop, where I manage my own integer iterator because Python makes it too hard to "next()" a string iterator
# inside a 'for' loop:
pos = 0
currSSID = nvRAMvariable[1]
while pos < len(currSSID):
    if currSSID[pos] == '%':
        #print(binascii.unhexlify(currSSID[pos+1:pos+3]), end="") # no, I don't want to output the actual zero...
        # Ignore the non-printable characters, really. Nothing useful about it.
        # This includes the arbitrarily long sequence of repeating %00 after the SSID, which seems like reserved space.
        # Potential bug: Unicode stuff in SSIDs like Japanese or emoji might be skipped.
        #hexifiedByte = currSSID[pos + 1: pos + 2]  # no, I don't really want to print a bunch of hex from this
        #print(hexifiedByte, end = " ")
        pos += 3
    else:
        print(currSSID[pos], end="") # Assuming it was not escaped hex, it must be printable text, so print it.
        pos += 1

print("")

# The third field contains the PSK. There's no readable string here so print it all as hex, i.e., its ASCII representation.
print ("Your PSK (hex representation): ", end="")
pos = 0
currPSK = nvRAMvariable[-1]
while pos < len(currPSK):
    if currPSK[pos] == '%':
        hexifiedByte = currPSK[pos + 1: pos + 3]
        print(hexifiedByte, end=" ")
        pos += 3
    else:
        print(binascii.hexlify(currPSK[pos]), end=" ")
        pos += 1

print("")

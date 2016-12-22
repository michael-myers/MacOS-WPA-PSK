# MacOS-WPA-PSK
PoC script showing that MacOS leaves the wireless key in NVRAM, in plaintext and accessible to anyone.

grab-MacOS-WPA-PSK.py is a tool to retrieve and decode the current wireless network key.
It is just a proof-of-concept to remind users that Apple treats this value as non-secret.
You might have expected it to require root to obtain, and be protected in the Keychain. Nope.

Usage:
        python grab-MacOS-WPA-PSK.py

Dependencies:
        Just python, which as a MacOS user you already have.

Tested with MacOS 10.12.2.

from client import Client
import os
import sys
import getopt


fs_url, current_firmware_version = ('', '')

try:
    argumentList = sys.argv[1:]
    opts, _ = getopt.getopt(argumentList, 'u:f:')
    opts = dict(opts)
    fs_url, current_firmware_version = opts['-u'], opts['-f']
except Exception as e:
    print(e)

if not fs_url:
    fs_url = 'http://127.0.0.1:80/'
if not current_firmware_version:
    current_firmware_version = '1.0.2'

clt = Client(file_server_url=fs_url)
new_firmware = clt.check_new_firmware_version(current_firmware_version, download=True)
if os.sep in new_firmware.lower():  # file downloaded
    print(f'New downloaded firmware path: {new_firmware}')
else:
    print(new_firmware)

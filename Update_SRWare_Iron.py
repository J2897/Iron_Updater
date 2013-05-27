# Released under the GNU General Public License version 3 by J2897.

def get_page(page):
	import urllib2
	source = urllib2.urlopen(page)
	return source.read()

def find_site_ver(page):
	T1 = page.find(target)
	if T1 == -1:
		return None
	T2 = page.find('>', T1)
	T3 = page.find('<', T2)
	return page[T2+1:T3]	# 27.0.1500.0

def stop():
	import sys
	sys.exit()

target = 'Version:'
url = 'https://www.srware.net/en/software_srware_iron_download.php'
page = get_page(url)

site_version = find_site_ver(page)
if site_version == None:
	stop()

import os
tmp = os.getenv('TEMP')
PF = os.getenv('PROGRAMFILES')

import win32api
try:
    info = win32api.GetFileVersionInfo(PF + '\\SRWare Iron\\iron.exe', "\\")
    ms = info['FileVersionMS']
    ls = info['FileVersionLS']
    file_version = "%d.%d.%d.%d" % (win32api.HIWORD(ms), win32api.LOWORD (ms),
									win32api.HIWORD (ls), win32api.LOWORD (ls))
except:
    file_version = '0.0.0.0' # some appropriate default here.

# Check if the site_version is the same as the file_version...
if file_version == site_version:
	# Yes:	Quit.
	stop()

# Check if Iron is running...
def find_proc(exe):
	import subprocess
	cmd = 'WMIC PROCESS get Caption'
	proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	for line in proc.stdout:
		if line.find(exe) != -1:
			return True

while find_proc('iron.exe'):
	user_input = win32api.MessageBox(0, 'There is a new version of Iron available. Please close Iron and press OK to continue.', 'SRWare Iron Updater', 1)
	if user_input == 1:
		pass
	elif user_input == 2:
		stop()

# Now download and install the new file...

import urllib
url = 'http://www.srware.net/downloads/srware_iron.exe'
DL = tmp + '\\' + 'srware_iron.exe'
urllib.urlretrieve(url, DL)

args = ' /SILENT /NORESTART'

def sub_proc(exe, args):
	import subprocess
	filepath = exe + args
	p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
	stdout, stderr = p.communicate()
	return p.returncode # is 0 if success

sub_proc(DL, args)

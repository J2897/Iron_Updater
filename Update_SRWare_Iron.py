# Released under the GNU General Public License version 3 by J2897.

title = 'SRWare Iron Updater'
print 'Running:	' + title

# Is SRWare Iron installed?
import os
DL = os.getenv('TEMP') + '\\' + 'srware_iron.exe'
PF = os.getenv('PROGRAMFILES')
iron_exe = PF + '\\SRWare Iron\\iron.exe'

if os.path.isfile(iron_exe):
	# Yes.
	first_time = False
else:
	# No.
	first_time = True

def DL_file():
	import urllib
	file_url = 'http://www.srware.net/downloads/srware_iron.exe'
	urllib.urlretrieve(file_url, DL)

def sub_proc(command):
	import subprocess
	p = subprocess.Popen(command, shell=True, stdout = subprocess.PIPE)
	stdout, stderr = p.communicate()
	return p.returncode # is 0 if success

def delay(sec):
	import time
	time.sleep(sec)

def stop():
	import sys
	sys.exit()

command = [DL, '/SILENT', '/NORESTART']	# More parameters: http://winscp.net/eng/docs/installation#automating_installation

if first_time == True:
	# Download and install SRWare Iron.
	print 'File not found:		' + iron_exe
	print 'Installing SRWare Iron for the first time...'
	DL_file()
	sub_proc(command)
	print 'Ending...'
	delay(5)
	stop()
	# End.

target = 'Version:'
url = 'https://www.srware.net/en/software_srware_iron_download.php'
print 'Target:		' + target
print 'URL:		' + url

import win32api

def msg_box(message, box_type):
	user_input = win32api.MessageBox(0, message, title, box_type)
	return user_input

# Get the web-page.
def get_page(page):
	import urllib2
	source = urllib2.urlopen(page)
	return source.read()

try:
	page = get_page(url)
except:
	msg_box('Could not download the page. You may not be connected to the internet.', 0)
	stop()
else:
	print 'Got page...'

# Get the current version information from the web-page.
def find_site_ver(page):
	T1 = page.find(target)
	if T1 == -1:
		return None
	T2 = page.find('>', T1)
	T3 = page.find('<', T2)
	return page[T2+1:T3] # 27.0.1500.0

try:
	site_version = find_site_ver(page)
except:
	msg_box('Could not search the page.', 0)
	stop()
else:
	print 'Site version:		' + site_version

if site_version == None:
	msg_box('The search target has not been found on the page. The formatting, or the text on the page, may have been changed.', 0)
	stop()

# Get the version information from the local file.
try:
	info = win32api.GetFileVersionInfo(iron_exe, "\\")
	ms = info['FileVersionMS']
	ls = info['FileVersionLS']
	file_version = "%d.%d.%d.%d" % (win32api.HIWORD(ms), win32api.LOWORD(ms),
									win32api.HIWORD(ls), win32api.LOWORD(ls)) # 27.0.1400.0
except:
	msg_box('Could not retrieve the local file version information.', 0)
	stop()
else:
	print 'Local version:		' + file_version
	# Is the local file version the same as the site version?
	if file_version == site_version:
		# Yes.
		print 'Match!'
		print 'Ending...'
		delay(5)
		stop()
	else:
		# No.
		print 'New version available!'
		print 'Updating...'

# Is Iron currently running?
def find_proc(exe):
	import subprocess
	cmd = 'WMIC PROCESS get Caption'
	proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	for line in proc.stdout:
		if line.find(exe) != -1:
			return True

while find_proc('iron.exe'):
	# Yes.
	print 'Iron is running. Close Iron now!'
	user_input = msg_box('There is a new version of Iron available. Please close Iron and press OK to continue.', 1)
	if user_input == 1:
		pass
	elif user_input == 2:
		stop()

# No.
# Download and install SRWare Iron.
DL_file()
sub_proc(command)
print 'Ending...'
delay(5)
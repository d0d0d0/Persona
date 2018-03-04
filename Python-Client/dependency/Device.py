# -*- coding: utf-8 -*-
"""
This file contains functions that are capable to access internal device
information and features.

	-SSHFS information
		-Username
		-Shared directory

	-File access

	-Capability
		-Linux and iOS
			-Bluetooth
			-Camera
			-Battery

	-Camera access
"""

from selenium import webdriver
from geopy.geocoders import Nominatim

from selenium.common.exceptions import NoSuchWindowException

import getpass
import os
import json
import requests
import sys
import facebook
import urllib
import threading, time
import threading

utf8_convert = {'ğ':'g', 'Ğ':'G', 'ç':'c', 'Ç':'C', 'ş':'s', 'Ş':'S', 'ı':'i', 'İ':'I', 'ö':'o', 'Ö':'O', 'Ü':'U', 'ü':'u'}
unidict = {k.decode('utf8'): v.decode('utf8') for k, v in utf8_convert.items()}


def convert(let):

	if let in unidict.keys():
		return unidict[let]
	else:
		return let


def string_normalizer(strr):
	return ''.join([convert(i) for i in strr])


def get_location():
	send_url = "http://ip-api.com/json"
	response = requests.get(send_url)
	data = json.loads(response.text)
	geolocator = Nominatim()
	location = geolocator.reverse(str(data["lat"]) + " , " + str(data["lon"]))
	return json.dumps({'location': location.address})


def get_sshfs_info(rootdir='/../shared'):
	"""
	Returns ssh-username and shared directory in json
	"""
	user_name = getpass.getuser()
	path = os.getcwd() + rootdir
	direc = {'username': user_name, 'path': path}
	return json.dumps(direc)


def get_directory_structure(dict=None, rootdir='../shared'):
	"""
	Return directory structure in format
	{
		"Dirname": directory_name,
		"SubDirs": [list_of_subfolder],
		"File":
			[
				{
					"filename": file_name
					"path: absolute_path
				},
				....
			]
	"""
	if not os.path.isfile(rootdir):
		try:
			dict["DirName"] = rootdir.split('/')[-1]
			n_dic = {"DirName": '', "SubDirs": [], "Files": []}
			for f in os.listdir(rootdir):
				if not os.path.isfile(os.path.join(rootdir, f)):
					subfolder = os.path.join(rootdir, f)
					n_dic = get_directory_structure(dict=n_dic, rootdir=subfolder)
					if os.path.isdir(subfolder):
						dict["SubDirs"].append(n_dic)
				else:
					# f_name = rootdir.split('/')[-1]
					f_name = f
					dict["Files"].append({"filename": f_name, "path": os.path.abspath(rootdir)})
		except Exception as e:
			print 'Error occurred: ', str(e)
	return dict


def create_virtual_filesystem(dict=None, path='./deneme'):
	"""
	Creating a meta directory structure from dictionary
	"""
	path = os.path.join(os.getcwd(), path)
	try:
		dir_name = dict['DirName']
		dir_path = os.path.join(path, dir_name)
		os.mkdir(dir_path)
		for f in dict['Files']:
			f_name = f['filename']
			f_path = os.path.join(dir_path, f_name)
			fdesc = open(f_path, 'wb')
			fdesc.close()
		for d in dict['SubDirs']:
			create_virtual_filesystem(dict=d, path=dir_path)
	except Exception as e:
		print 'Error occurred: ', str(e)


def get_file(path):
	"""
	Returns requested file descriptor
	"""
	try:
		requested_file = (open(path, "rb")).read()
		return requested_file
	except Exception as e:
		print e


def get_capability(platform='Darwin'):
	"""
	Returns platform specific capabilities in json
	"""


	def formatter(cap):
		if cap != '':
			return (cap[:-1]).split(': ')[-1]
		else:
			return 'NOT FOUND'
	try:
		if platform == 'Darwin':
			command_list = {
				'model_name': 'system_profiler SPHardwareDataType | grep "Model Identifier"',
				'camera': 'system_profiler SPCameraDataType | grep "Model ID"',
				'charge_remaining': 'system_profiler SPPowerDataType | grep "Charge Remaining"',
				'charge_full': 'system_profiler SPPowerDataType | grep "Full Charge Capacity"',
				'bluetooth_addr': 'system_profiler SPBluetoothDataType | grep "Address"',
				'bluetooth_le': 'system_profiler SPBluetoothDataType | grep "Bluetooth Low Energy Supported"',
			}

			model_name = formatter(os.popen(command_list['model_name']).read())
			camera = formatter(os.popen(command_list['camera']).read())
			charge_remaining = formatter(os.popen(command_list['charge_remaining']).read())
			charge_full = formatter(os.popen(command_list['charge_full']).read())
			bluetooth_addr = formatter(os.popen(command_list['bluetooth_addr']).read())
			bluetooth_le = formatter(os.popen(command_list['bluetooth_le']).read())
			charge = (int((int(charge_remaining)/float(charge_full))*100))

		elif platform == 'Linux':
			model_name_command = 'cat /sys/devices/virtual/dmi/id/product_name'
			model_name = os.popen(model_name_command).read()[:-1]
			battery_dir = os.popen('upower -e | grep BAT0').read()[:-1]
			charge_command = 'upower -i ' + battery_dir + ' | grep percentage'
			charge = os.popen(charge_command).read()[:-2].split(':          ')[-1]
			bluetooth_addr_command = 'hciconfig | grep BD'
			bluetooth_addr = os.popen(bluetooth_addr_command).read()[13:30]

			# Works with 1 camera. Command returns list of all cameras.
			camera_command = 'for I in /sys/class/video4linux/*; do cat $I/name; done'
			camera = os.popen(camera_command).read()[:-1]
			bluetooth_le = "NOT FOUND"

		elif platform == 'Windows':
			txt = open("WindowsDependencies/capabilities.txt")

			capabilitiesJson = txt.read()
			dictionary = json.loads(capabilitiesJson)

			model_name = dictionary["model_name"]
			charge = dictionary["charge"]
			bluetooth_addr = dictionary["bluetooth_addr"]
			camera = dictionary["camera"]
			bluetooth_le = dictionary["bluetooth_le"]

	except Exception as e:
		print e

	dict = {
		"model_name": model_name, "camera": camera, "charge": charge,
		"bluetooth_addr": bluetooth_addr, "bluetooth_le": bluetooth_le,
		"sensors": [], "type": "desktop"
	}

	return str(dict)


def get_camera_webrtc(browser='FIREFOX', room_id=''):
	"""
	Returns WebRTC roomd id for online webcam session
	For client, it only connects to room
	For server, it generates a room and connect to it
	"""
	if browser == 'FIREFOX':
		address = "http://apprtc.appspot.com/r/" + room_id
		# address = "http://app.rtc/r/" + room_id
		profile = webdriver.FirefoxProfile()
		profile.set_preference('media.navigator.permission.disabled', True)
		profile.update_preferences()
		driver = webdriver.Firefox(profile)
		driver.get(address)
		driver.find_element_by_id('confirm-join-button').click()


def facebook_login(app_key='OBFUSCATED', scope='user_friends'):

	auth_url = 'https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&response_type=token&scope=%s' \
				% (urllib.quote(app_key),
				'https://www.facebook.com/connect/login_success.html', urllib.quote(scope))
	try:
		profile = webdriver.FirefoxProfile()
		profile.set_preference('webdriver.load.strategy', 'unstable')
		driver = webdriver.Firefox(profile)
		driver.set_page_load_timeout(5)
		driver.get(auth_url)
		st = time.time()
		is_login = True

		if 'dialog' not in driver.current_url:
			is_login = False

		while 'dialog' in driver.current_url and is_login:

			if time.time() - st > 60:
				is_login = False
				break

		if is_login:
			raw_token = driver.current_url
			token = raw_token[raw_token.index('=') + 1:raw_token.index('&')]
			driver.close()

			graph = facebook.GraphAPI(access_token=token, version='2.2')
			return graph

		driver.close()
		return 'NOT SUCCESSFUL'

	except NoSuchWindowException:
		print 'Error occured during Facebook login: Browser is closed.'

	except Exception as e:
		print 'Error occured during Facebook login: ', str(e)

"""
TODO: Need thread otherwise it blocks main app

def facebook_login(scope='user_friends'):
	t = threading.Thread(target=facebook_login_body)
	t.start()
"""

# SimCity 4 Backup release setting file.
# Yungon Park (http://github.com/rubysoho07)

from distutils.core import setup
import py2exe

setup(
	# Make execute files option.
	console=[{
		"script": "simcity_backup.py", 
		"dest_base": "SC4Backup",
		}],

	# py2exe option
	options={"py2exe": {
	"bundle_files": 1,
	"dll_excludes": ["w9xpopen.exe", "MSVCP90.DLL"]}},
	
	zipfile=None)
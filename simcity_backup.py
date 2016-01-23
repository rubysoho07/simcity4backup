# simcity backup (using zipfile library) 
# Yungon Park
# https://github.com/rubysoho07/simcity4backup

import zipfile
import datetime
import os
import sys

is_there_plugins = False
is_there_regions = False

today_date = None

plugin_file_name = ""
region_file_name = ""

backup_path = ""

# 1. Check whether SimCity plugins & region folder. (If not, exit program. -- using sys.exit())
# os.path.exists (path) : you can check whether the file or directory exist.

plugins_path = "C:\\Users\\-----\\Documents\\SimCity 4\\Plugins\\"
regions_path = "C:\\Users\\-----\\Documents\\SimCity 4\\Regions\\"

def system_check():
    global is_there_regions
    global is_there_plugins
    global plugins_path
    global regions_path
    global today_date
    global plugin_file_name
    global region_file_name
    global backup_path

    if (os.path.exists(regions_path) == True):
        is_there_regions = True
        print "Regions directory exists."
    else:
        print "Regions directory doesn't exist.\n"
        sys.exit()   

    if (os.path.exists(plugins_path) == True):
        is_there_plugins = True
        print "Plugins directory exists."
    else:
        print "Plugins directory doesn't exist.\n"
        sys.exit()

    # 2. If those are true, make backup file at "D:\SCbackup\".
    #     Filename will be "SC_Plugin(or Region)_<date>.zip".

    today_date = datetime.date.today()
    backup_path = "G:\\SCbackup\\"

    # if you integer to string, use str(integer).
    # datetime.isoformat() : Get today's date like "yyyy-mm-dd" to string.
    plugin_file_name = "SC_Plugin_" + today_date.isoformat() + ".zip"
    region_file_name = "SC_Region_" + today_date.isoformat() + ".zip"

    # 2-1. Check whether backup path is present. (If not, make directory.)

    if (os.path.exists(backup_path) == True):
        print "Backup folder (" + backup_path + ") exists."
        if (os.path.exists(backup_path+plugin_file_name) == True):
            print "Already backuped today's plugins data."
            sys.exit()

        if (os.path.exists(backup_path+region_file_name) == True):
            print "Already backuped today's regions data."
            sys.exit()
    else:
        print "Backup folder doesn't exist. make directory " + backup_path
        os.mkdir(backup_path)
        print "Making directory at (" + backup_path + ")... Done."

# 2-2. Make file list of plugins and regions.

def backup_plugin():
    global plugin_file_name
    global backup_path

    plugins_list = []

    printed_already = False
    printed_point = 0

    os.chdir(plugins_path)

    for root, dirs, names in os.walk("."):
        for name in names:
            plugins_list.append(os.path.join(root, name))

    print "Make plugins file list ... Done. ", len(plugins_list), " files."
    sys.stdout.write("Making backup : ")

    # 2-3. Make zipfile with zipfile.ZIP_DEFLATED option (to compress files)
    plugins_zipfile = zipfile.ZipFile(plugin_file_name, "w", zipfile.ZIP_DEFLATED)

    for item in plugins_list:
        plugins_zipfile.write(item)
        percent = plugins_list.index(item) / float(len(plugins_list)) * 100
        if int(percent) % 10 == 0 and percent >= 10:
            if printed_already == False:
                sys.stdout.write('*')
                printed_already = True
                printed_point = int(percent)

            if printed_point != int(percent):
                printed_already = False
            else:
                printed_already = True

    sys.stdout.write('* \t\t [Done]\n')
    plugins_zipfile.close()
    os.rename(plugin_file_name, backup_path+plugin_file_name)

    print "Making plugins backup ... Done."

# for regions directory, also make list and make zipfile.

def backup_region():
    global region_file_name
    global backup_path

    regions_list = []

    printed_already = False
    printed_point = 0

    os.chdir(regions_path)

    for root, dirs, names in os.walk("."):
        for name in names:
            regions_list.append(os.path.join(root, name))

    print "Make regions file list ... Done. ", len(regions_list), " files."
    sys.stdout.write("Making backup : ")

    regions_zipfile = zipfile.ZipFile(region_file_name, "w", zipfile.ZIP_DEFLATED)

    for item in regions_list:
        regions_zipfile.write(item)
        percent = regions_list.index(item) / float(len(regions_list)) * 100
        if int(percent) % 10 == 0 and percent >= 10:
            if printed_already == False:
                sys.stdout.write('*')
                printed_already = True
                printed_point = int(percent)

            if printed_point != int(percent):
                printed_already = False
            else:
                printed_already = True

    sys.stdout.write('* \t\t [Done]\n')
    regions_zipfile.close()
    os.rename(region_file_name, backup_path+region_file_name)

    print "Making regions backup ... Done."

# Main routine.
if __name__ == "__main__":

    system_check()

    is_backup_plugin = raw_input("Will you backup plugins?(y/n)")

    if is_backup_plugin == "y":
        backup_plugin()
    elif is_backup_plugin == "n":
        print "OK. I'll go on."
    else:
        print "Invalid input! Input must be 'y' or 'n'. Execute this script again."
        sys.exit()

    is_backup_region = raw_input("Wall you backup regions?(y/n)")

    if is_backup_region == "y":
        backup_region()
    elif is_backup_region == "n":
        print "Ok. All done."
    else:
        print "Invalid input! Input must be 'y' or 'n'. Execute this script again."
        sys.exit()

    # 2-4. done.
    print "All Done. Check \"" + backup_path + "\" directory." 

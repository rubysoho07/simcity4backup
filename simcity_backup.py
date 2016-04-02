# simcity backup (using zipfile library) 
# Yungon Park
# https://github.com/rubysoho07/simcity4backup

import zipfile
import datetime
import os
import sys
import glob

is_there_plugins = False
is_there_regions = False

today_date = None

plugin_file_name = ""
region_file_name = ""

backup_path = ""

# 1. Check whether SimCity plugins & region folder. (If not, exit program. -- using sys.exit())
# os.path.exists (path) : you can check whether the file or directory exist.

plugins_path = ""
regions_path = ""

# Write default config (If you don't have scb.cfg file)
def write_default_config ():
    global plugins_path
    global regions_path
    global backup_path

    cfg_w = open("scb.cfg", 'w')

    tmp_src_path = ""
    tmp_dst_path = ""

    # Write source directory
    tmp_src_path = find_folder ()
    if tmp_src_path != "":
        plugins_path = tmp_src_path + "Plugins\\"
        regions_path = tmp_src_path + "Regions\\"
        print "Set default source:", tmp_src_path
    else:
        print "SimCity 4 may not be installed. Check whether SimCity 4 installed."
        cfg_w.close ()
        sys.exit ()

    cfg_w.write ("SRC_DIR" + "=" + tmp_src_path + "\n")

    # Write destination directory
    tmp_dst_path = os.getcwd() + "\\"
    print "Set default destination:", tmp_dst_path
    backup_path = tmp_dst_path

    cfg_w.write ("DEST_DIR" + "=" + tmp_dst_path + "\n")

    cfg_w.close ()

# Write config
def write_config (option, write_path):
    cfg_r = open("scb.cfg", 'r')
    cfg_w = open("scb.cfg_w", 'w')

    while True:
        # readline
        line = cfg_r.readline ()

        if not line:
            break;

        # split with "="
        line_split = line.split ('=')

        # if length is 2, just write.
        if len(line_split) == 2:
            if line_split[1] == "\n":
                # for example, "DEST_DIR=\n"
                continue
            cfg_w.write(line+"\n")

    cfg_w.write (option + "=" + write_path)

    cfg_r.close ()
    cfg_w.close ()

    os.remove ("scb.cfg")
    os.rename ("scb.cfg_w", "scb.cfg")


# Find SimCity 4 Region/Plugin folder & Write path to file.
def find_folder ():
    # find SimCity 4 Directory. It must have SimCity 4.cfg, Region and Plugins folder. 
    # Windows 7, 8, 10 Users Directory: C:\Users\
    user_list = []

    for item in glob.glob("C:\\Users\\*"):
        if os.path.isdir(item) and os.access(item + "\\Documents\\SimCity 4\\", os.F_OK):
            user_list.append(item)

    if len(user_list) == 1:
        return user_list[0] + "\\Documents\\SimCity 4\\"

    return ""

# Read config from file.
def read_config ():
    global plugins_path
    global regions_path
    global backup_path

    # Check source/destination path found
    is_src_found = False
    is_dest_found = False

    # Temporary source/destination path
    tmp_src_path = ""
    tmp_dst_path = ""

    conf_file = open("scb.cfg", 'r')

    line = conf_file.readline()
    while line:
        # If string has return(\n), remove it.
        if line[-1] == '\n':
            line_without_return = line[:-1]
        else:
            line_without_return = line

        # Read config.
        split_line = line_without_return.split('=')

        if split_line[0] == "SRC_DIR":
            # Find source directory.
            if split_line[1] == "":
                tmp_src_path = find_folder()
                if tmp_src_path != "":
                    plugins_path = tmp_src_path + "Plugins\\"
                    regions_path = tmp_src_path + "Regions\\"
                    print "Set default source:", tmp_src_path
                else:
                    print "SimCity 4 may not be installed. Check whether SimCity 4 installed."
                    sys.exit()
            else:
                plugins_path = split_line[1] + "Plugins\\"
                regions_path = split_line[1] + "Regions\\"

            print "SimCity 4 Region Directory:", regions_path
            print "SimCity 4 Plugin Directory:", plugins_path

        elif split_line[0] == "DEST_DIR":
            # Find destination directory.
            if split_line[1] == "":
                # Default backup path is CWD(Current Working Directory).
                tmp_dst_path = os.getcwd() + "\\"
                print "Set default destination:", tmp_dst_path
                backup_path = tmp_dst_path
            else:
                backup_path = split_line[1]
                print "Destination Directory:", backup_path
        else:
            # Exception case.
            print "Exception: Can't read config file. Check scb.cfg file."
            conf_file.close()
            sys.exit()

        line = conf_file.readline()

    conf_file.close()

    if tmp_src_path != "":
        write_config("SRC_DIR", tmp_src_path)
    
    if tmp_dst_path != "":
        write_config("DEST_DIR", tmp_dst_path)

# Check source and destination directory exists. 
# After that, Make archive file name.
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
        print "Regions directory (" + regions_path + ") doesn't exist.\n"
        sys.exit()   

    if (os.path.exists(plugins_path) == True):
        is_there_plugins = True
        print "Plugins directory exists."
    else:
        print "Plugins directory (" + plugins_path + ")doesn't exist.\n"
        sys.exit()

    # 2. If those are true, make backup file at "D:\SCbackup\".
    #     Filename will be "SC_Plugin(or Region)_<date>.zip".

    today_date = datetime.date.today()

    # if you integer to string, use str(integer).
    # datetime.isoformat() : Get today's date like "yyyy-mm-dd" to string.
    plugin_file_name = "SC_Plugin_" + today_date.isoformat() + ".zip"
    region_file_name = "SC_Region_" + today_date.isoformat() + ".zip"

    # 2-1. Check whether backup path is present. (If not, make directory.)

    if (os.path.exists(backup_path) == True):
        print "Backup folder (" + backup_path + ") exists."    
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

    # If backup file exists, exit this function.
    if (os.path.exists(backup_path+plugin_file_name) == True):
        print "Already backuped today's plugins data."
        return

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

    # Check today's region backup exists.
    if (os.path.exists(backup_path+region_file_name) == True):
        print "Already backuped today's regions data."
        return

    # Go to regions_path.
    os.chdir(regions_path)

    # Make files of regions directory list.
    for root, dirs, names in os.walk("."):
        for name in names:
            regions_list.append(os.path.join(root, name))

    print "Make regions file list ... Done. ", len(regions_list), " files."
    sys.stdout.write("Making backup : ")

    # Make zip file.
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

    # Read Config
    if os.access("scb.cfg", os.F_OK):
        read_config()
    else:
        print "Can't find config file(scb.cfg). Make default config."
        write_default_config()

    # System Check.
    system_check()

    # Backup Plugin.
    is_backup_plugin = raw_input("Will you backup plugins?(y/n)")

    if is_backup_plugin == "":
        print "No input detected. Plugin backup file will not be made."
    elif is_backup_plugin[0] == "y":
        backup_plugin()
    elif is_backup_plugin[0] == "n":
        print "OK. I'll go on."
    else:
        print "Invalid input! Input must be started with 'y' or 'n'. Execute this script again."
        sys.exit()

    # Backup Region.
    is_backup_region = raw_input("Will you backup regions?(y/n)")

    if is_backup_region == "":
        print "No input detected. Region backup file will not be made."
    elif is_backup_region[0] == "y":
        backup_region()
    elif is_backup_region[0] == "n":
        print "Ok. I'll go on."
    else:
        print "Invalid input! Input must be started with 'y' or 'n'. Execute this script again."
        sys.exit()

    # 2-4. done.
    print "All Done. Check \"" + backup_path + "\" directory." 

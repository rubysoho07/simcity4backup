"""
SimCity 4 backup (using zipfile library)

Make a backup data of SimCity 4 user.
By Yungon Park
https://github.com/rubysoho07/simcity4backup
"""

import zipfile
import datetime
import os
import sys
import glob
import argparse

is_there_plugins = False
is_there_regions = False
is_there_albums = False

today_date = None

plugin_file_name = ""
region_file_name = ""
album_file_name = ""

backup_path = ""

# Check whether SimCity plugins, region and album folder. (If not, exit.)

plugins_path = ""
regions_path = ""
albums_path = ""


def write_default_config():
    """ Write default config (If you don't have scb.cfg file) """
    global plugins_path
    global regions_path
    global albums_path
    global backup_path

    cfg_w = open("scb.cfg", 'w')

    tmp_src_path = ""
    tmp_dst_path = ""

    # Write source directory
    tmp_src_path = find_folder()
    if tmp_src_path != "":
        plugins_path = tmp_src_path + "Plugins\\"
        regions_path = tmp_src_path + "Regions\\"
        albums_path = tmp_src_path + "Albums\\"
        print "Set default source:", tmp_src_path
    else:
        print "SimCity 4 may not be installed."
        print "Check whether SimCity 4 installed."
        cfg_w.close()
        sys.exit()

    cfg_w.write("SRC_DIR" + "=" + tmp_src_path + "\n")

    # Write destination directory
    tmp_dst_path = os.getcwd() + "\\"
    print "Set default destination:", tmp_dst_path
    backup_path = tmp_dst_path

    cfg_w.write("DEST_DIR" + "=" + tmp_dst_path + "\n")

    cfg_w.close()


def write_config(option, write_path):
    """ Write config file. """
    cfg_r = open("scb.cfg", 'r')
    cfg_w = open("scb.cfg_w", 'w')

    while True:
        # readline
        line = cfg_r.readline()

        if not line:
            break

        # split with "="
        line_split = line.split('=')

        # if length is 2, just write.
        if len(line_split) == 2:
            if line_split[1] == "\n":
                # for example, "DEST_DIR=\n"
                continue
            cfg_w.write(line+"\n")

    cfg_w.write(option + "=" + write_path)

    cfg_r.close()
    cfg_w.close()

    os.remove("scb.cfg")
    os.rename("scb.cfg_w", "scb.cfg")


def find_folder():
    """ Find SimCity 4 Region/Plugin folder & Write path to file. """
    user_list = []

    for item in glob.glob("C:\\Users\\*"):
        if os.path.isdir(item) and os.access(item + "\\Documents\\SimCity 4\\",
                                             os.F_OK):
            user_list.append(item)

    if len(user_list) == 1:
        return user_list[0] + "\\Documents\\SimCity 4\\"

    return ""


def read_config():
    """ Read config from file. """
    global plugins_path
    global regions_path
    global albums_path
    global backup_path

    # Temporary source/destination path
    tmp_src_path = ""
    tmp_dst_path = ""

    conf_file = open("scb.cfg", 'r')

    line = conf_file.readline()
    while line:
        # If string has return(\n), remove it.
        line_without_return = line.strip('\n')

        # Read config.
        split_line = line_without_return.split('=')

        if split_line[0] == "SRC_DIR":
            # Find source directory.
            if split_line[1] == "":
                tmp_src_path = find_folder()
                if tmp_src_path != "":
                    plugins_path = tmp_src_path + "Plugins\\"
                    regions_path = tmp_src_path + "Regions\\"
                    albums_path = tmp_src_path + "Albums\\"
                    print "Set default source:", tmp_src_path
                else:
                    print "SimCity 4 may not be installed.",
                    print "Check whether SimCity 4 is installed."
                    sys.exit()
            else:
                plugins_path = split_line[1] + "Plugins\\"
                regions_path = split_line[1] + "Regions\\"
                albums_path = split_line[1] + "Albums\\"

            print "SimCity 4 Region Directory:", regions_path
            print "SimCity 4 Plugin Directory:", plugins_path
            print "SimCity 4 Screenshot(Album) Directory:", albums_path

        elif split_line[0] == "DEST_DIR":
            # Find destination directory.
            if split_line[1] == "" or not os.path.exists(split_line[1]):
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


def system_check():
    """ Check source and destination directory exists.
    After that, Make archive file name."""
    global is_there_regions
    global is_there_plugins
    global is_there_albums
    global plugins_path
    global regions_path
    global albums_path
    global today_date
    global plugin_file_name
    global region_file_name
    global album_file_name
    global backup_path

    if os.path.exists(regions_path) is True:
        is_there_regions = True
        print "Regions directory exists."
    else:
        print "Regions directory (" + regions_path + ") doesn't exist.\n"
        sys.exit()

    if os.path.exists(plugins_path) is True:
        is_there_plugins = True
        print "Plugins directory exists."
    else:
        print "Plugins directory (" + plugins_path + ")doesn't exist.\n"
        sys.exit()

    if os.path.exists(albums_path) is True:
        is_there_albums = True
        print "Screenshots directory exists."
    else:
        print "Screenshots directory (" + albums_path + ")doesn't exist.\n"
        sys.exit()

    # 2. If those are true, make backup file at "D:\SCbackup\".
    #     Filename will be "SC_Plugin(or Region)_<date>.zip".

    today_date = datetime.date.today()

    # if you integer to string, use str(integer).
    # datetime.isoformat() : Get today's date like "yyyy-mm-dd" to string.
    plugin_file_name = "SC_Plugin_" + today_date.isoformat() + ".zip"
    region_file_name = "SC_Region_" + today_date.isoformat() + ".zip"
    album_file_name = "SC_Screenshot_" + today_date.isoformat() + ".zip"

    # Check whether backup path is present. (If not, make directory.)

    if os.path.exists(backup_path) is True:
        print "Backup folder (" + backup_path + ") exists."
    else:
        print "Backup folder doesn't exist. make directory " + backup_path
        os.mkdir(backup_path)
        print "Making directory at (" + backup_path + ")... Done."


def print_star(num):
    """ Print star(*) x num. """
    for i in range(num):
        sys.stdout.write('*')


def make_backup_file(file_name, file_list):
    """ Make backup file with zipfile library. """
    printed_percent = 0
    backup_file = zipfile.ZipFile(file_name, "w", zipfile.ZIP_DEFLATED)

    for item in file_list:
        backup_file.write(item)
        percent = file_list.index(item) / float(len(file_list)) * 100
        if int(percent / 10) > int(printed_percent / 10):
            print_star(int(percent / 10) - int(printed_percent / 10))
            printed_percent = percent

    print_star(100/10 - int(printed_percent / 10))
    sys.stdout.write(' \t\t [Done]\n')
    backup_file.close()


def backup_plugin():
    """ Backup plugin files. (Buildings) """
    global plugin_file_name
    global backup_path

    plugins_list = []

    # If backup file exists, exit this function.
    if os.path.exists(backup_path+plugin_file_name) is True:
        print "Already backuped today's plugins data."
        return

    os.chdir(plugins_path)

    for root, _, names in os.walk("."):
        for name in names:
            plugins_list.append(os.path.join(root, name))

    print "Make plugins file list ... Done. ", len(plugins_list), " files."
    sys.stdout.write("Making backup : ")

    make_backup_file(plugin_file_name, plugins_list)
    os.rename(plugin_file_name, backup_path+plugin_file_name)

    print "Making plugins backup ... Done."


def backup_region():
    """ Backup region files. """
    global region_file_name
    global backup_path

    regions_list = []

    # Check today's region backup exists.
    if os.path.exists(backup_path+region_file_name) is True:
        print "Already backuped today's regions data."
        return

    # Go to regions_path.
    os.chdir(regions_path)

    # Make files of regions directory list.
    for root, _, names in os.walk("."):
        for name in names:
            regions_list.append(os.path.join(root, name))

    print "Make regions file list ... Done. ", len(regions_list), " files."
    sys.stdout.write("Making backup : ")

    # Make zip file.
    make_backup_file(region_file_name, regions_list)
    os.rename(region_file_name, backup_path+region_file_name)

    print "Making regions backup ... Done."


def backup_album():
    """ Backup screenshots. """
    global album_file_name
    global backup_path

    albums_list = []

    # Check today's region backup exists.
    if os.path.exists(backup_path+album_file_name) is True:
        print "Already backuped today's screenshots data."
        return

    # Go to regions_path.
    os.chdir(albums_path)

    # Make files of albums directory list.
    for root, _, names in os.walk("."):
        for name in names:
            albums_list.append(os.path.join(root, name))

    print "Make screenshots file list ... Done. ", len(albums_list), "files."
    sys.stdout.write("Making backup : ")

    # Make zip file.
    make_backup_file(album_file_name, albums_list)
    os.rename(album_file_name, backup_path+album_file_name)

    print "Making screenshots backup ... Done."


def do_backup(part, backup_function):
    """ Ask to back up some part of game data and execute backup function. """
    answer = raw_input("Will you backup " + part + "?(y/n)")

    if answer == "":
        print "No input detected. " + part + " backup file will not be made."
    elif answer[0] == "y":
        backup_function()
    elif answer[0] == "n":
        print "OK. I'll go on."
    else:
        print "Invalid input! Input must be started with 'y' or 'n'."
        sys.exit()


def print_version():
    """ Print version of this script. """
    print "SimCity 4 Backup Version "
    print "Released Date: "
    sys.exit()

# Main routine.
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version",
                        help="Show version of SC4Backup.",
                        action="store_true")
    parser.add_argument("-y", "--yes",
                        help="Backup all user data without asking you.",
                        action="store_true")

    args = parser.parse_args()

    if args.version:
        print_version()

    # Read Config
    if os.access("scb.cfg", os.F_OK):
        read_config()
    else:
        print "Can't find config file(scb.cfg). Make default config."
        write_default_config()

    # System Check.
    system_check()

    # Backup game data.
    if args.yes:
        backup_plugin()
        backup_album()
        backup_region()
    else:
        do_backup("plugins", backup_plugin)
        do_backup("screenshots", backup_album)
        do_backup("regions", backup_region)

    # 2-4. done.
    print "All Done. Check \"" + backup_path + "\" directory."

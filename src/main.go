package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
)

type backupConfig struct {
	isTherePlugins bool
	isThereRegions bool
	isThereAlbums  bool
	todayData      string
	pluginFileName string
	regionFileName string
	albumFileName  string
	backupPath     string
	pluginsPath    string
	regionsPath    string
	albumsPath     string
}

func makeBackupFile(fileName string, fileList []string) {

	fmt.Printf("Started to make backup file: %s\n", fileName)

	for i, listElement := range fileList {
		fmt.Println(i, listElement)
	}
}

func confirmBackup(ignoreAsking bool) bool {

	if ignoreAsking == true {
		return true
	}

	fmt.Print("Will you backup plugins (y/n)? ")
	var confirmed string
	fmt.Scan(&confirmed)

	if confirmed == "Y" || confirmed == "y" {
		return true
	}

	return false
}

func (c backupConfig) backupPlugin(ignoreAsking bool) {

	// If backup file exists, exit this function.
	if _, err := os.Stat(c.backupPath + c.pluginFileName); os.IsExist(err) {
		fmt.Println("Already backuped today's plugins data.")
		return
	}

	if confirmBackup(ignoreAsking) == true {
		os.Chdir(c.pluginsPath)

		var pluginFiles []string

		filepath.Walk(".", func(path string, info os.FileInfo, err error) error {
			if err != nil {
				fmt.Printf("Error on walking SimCity 4 Plugins Directory (%v)\n", err)
				return err
			}

			pluginFiles = append(pluginFiles, path)
			// fmt.Printf("Visited: %q\n", path)

			return nil
		})

		fmt.Printf("Make plugins file list ... Done. %d files.\n", len(pluginFiles))
		makeBackupFile(c.pluginFileName, pluginFiles)
		// os.Rename(c.pluginFileName, c.backupPath+c.pluginFileName)
	}
}

func main() {
	fmt.Println("===============SimCity 4 Backup=================")

	var printVersion = flag.Bool("version", false, "Show version of SC4Backup.")
	var setAllYes = flag.Bool("yes", false, "Backup all user data without asking you.")

	flag.Parse()

	if *printVersion == true {
		fmt.Println("SimCity 4 Backup Version v2.0.0")
		fmt.Println("Release Date: 2018-12-31")
		return
	}

	config := backupConfig{
		isThereAlbums:  true,
		isTherePlugins: true,
		isThereRegions: true,
		todayData:      "2018-08-25",
		pluginFileName: "SC_Plugin_2018-08-25.zip",
		regionFileName: "SC_Region_2018-08-25.zip",
		albumFileName:  "SC_Screenshot_2018-08-25.zip",
		backupPath:     "C:\\Users\\hahaf\\Documents\\",
		pluginsPath:    "C:\\Users\\hahaf\\Documents\\SimCity 4\\Plugins\\",
		regionsPath:    "C:\\Users\\hahaf\\Documents\\SimCity 4\\Regions\\",
		albumsPath:     "C:\\Users\\hahaf\\Documents\\SimCity 4\\Albums\\",
	}

	config.backupPlugin(*setAllYes)
}

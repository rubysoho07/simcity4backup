package main

import (
	"archive/zip"
	"flag"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"time"
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

func (c backupConfig) makePluginArchiveFile() error {
	zipfile, err := os.Create(c.backupPath + c.pluginFileName)
	if err != nil {
		return err
	}
	defer zipfile.Close()

	archive := zip.NewWriter(zipfile)
	defer archive.Close()

	info, err := os.Stat(c.pluginsPath)
	if err != nil {
		return nil
	}

	var baseDir string
	if info.IsDir() {
		baseDir = filepath.Base(c.pluginsPath)
	}

	filepath.Walk(c.pluginsPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			fmt.Printf("Error on walking SimCity 4 Plugins Directory (%v)\n", err)
			return err
		}

		header, err := zip.FileInfoHeader(info)
		if err != nil {
			return err
		}

		if baseDir != "" {
			header.Name = filepath.Join(baseDir, strings.TrimPrefix(path, c.pluginsPath))
		}

		if info.IsDir() {
			header.Name += "/"
		} else {
			header.Method = zip.Deflate
		}

		writer, err := archive.CreateHeader(header)
		if err != nil {
			return err
		}

		if info.IsDir() {
			return nil
		}

		file, err := os.Open(path)
		if err != nil {
			return err
		}
		defer file.Close()

		_, err = io.Copy(writer, file)
		return err
	})

	return nil
}

func (c backupConfig) backupPlugin(ignoreAsking bool) error {
	if _, err := os.Stat(c.backupPath + c.pluginFileName); !os.IsNotExist(err) {
		fmt.Println("Already made the backup of today's plugins data.")
		return err
	}

	if confirmBackup(ignoreAsking) == true {
		fmt.Printf("Making the backup of Plugins")
		err := c.makePluginArchiveFile()
		if err != nil {
			return err
		}
		fmt.Printf(" ... Done.\n")
	}

	return nil
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

	currentTime := time.Now().Local().Format("2006-01-02")

	config := backupConfig{
		isThereAlbums:  true,
		isTherePlugins: true,
		isThereRegions: true,
		todayData:      currentTime,
		pluginFileName: "SC_Plugin_" + currentTime + ".zip",
		regionFileName: "SC_Region_" + currentTime + ".zip",
		albumFileName:  "SC_Screenshot_" + currentTime + ".zip",
		backupPath:     "C:\\Users\\hahaf\\Documents\\",
		pluginsPath:    "C:\\Users\\hahaf\\Documents\\SimCity 4\\Plugins\\",
		regionsPath:    "C:\\Users\\hahaf\\Documents\\SimCity 4\\Regions\\",
		albumsPath:     "C:\\Users\\hahaf\\Documents\\SimCity 4\\Albums\\",
	}

	err := config.backupPlugin(*setAllYes)
	if err != nil {
		fmt.Println(err)
	}
}

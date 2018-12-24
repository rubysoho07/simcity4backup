package main

import (
	"archive/zip"
	"errors"
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

func confirmBackup(ignoreAsking bool, t string) bool {
	if ignoreAsking == true {
		return true
	}

	fmt.Print("Will you backup ", strings.ToLower(t), " (y/n)? ")
	var confirmed string
	fmt.Scan(&confirmed)

	if confirmed == "Y" || confirmed == "y" {
		return true
	}

	return false
}

func (c backupConfig) getBackupInfo(t string) (source string, target string) {
	switch t {
	case "PLUGIN":
		return c.pluginsPath, c.backupPath + c.pluginFileName
	case "REGION":
		return c.regionsPath, c.backupPath + c.regionFileName
	case "ALBUM":
		return c.albumsPath, c.backupPath + c.albumFileName
	default:
		return "ERROR_SOURCE", "ERROR_TARGET"
	}
}

func (c backupConfig) makeArchiveFile(source string, target string) error {
	zipfile, err := os.Create(target)
	if err != nil {
		return err
	}
	defer zipfile.Close()

	archive := zip.NewWriter(zipfile)
	defer archive.Close()

	info, err := os.Stat(source)
	if err != nil {
		return nil
	}

	var baseDir string
	if info.IsDir() {
		baseDir = filepath.Base(source)
	}

	filepath.Walk(source, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			fmt.Printf("Error on walking SimCity 4 Plugins Directory (%v)\n", err)
			return err
		}

		header, err := zip.FileInfoHeader(info)
		if err != nil {
			return err
		}

		if baseDir != "" {
			header.Name = filepath.Join(baseDir, strings.TrimPrefix(path, source))
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

func (c backupConfig) backup(ignoreAsking bool, t string) error {

	source, target := c.getBackupInfo(t)

	if source == "ERROR_SOURCE" || target == "ERROR_TARGET" {
		return errors.New("Invalid source or target")
	}

	if _, err := os.Stat(target); !os.IsNotExist(err) {
		fmt.Println("Already made the backup of today's ", strings.ToLower(t), "data:", target)
		return err
	}

	if confirmBackup(ignoreAsking, t) == true {
		fmt.Print("Making the backup of ", strings.ToLower(t), " ... ")
		err := c.makeArchiveFile(source, target)
		if err != nil {
			return err
		}
		fmt.Printf("Done.\n")
	}

	return nil
}

func main() {
	fmt.Println("===============SimCity 4 Backup=================")

	printVersion := flag.Bool("version", false, "Show version of SC4Backup.")
	setAllYes := flag.Bool("yes", false, "Backup all user data without asking you.")

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

	err := config.backup(*setAllYes, "PLUGIN")
	if err != nil {
		fmt.Println(err)
	}
	err = config.backup(*setAllYes, "REGION")
	if err != nil {
		fmt.Println(err)
	}
	err = config.backup(*setAllYes, "ALBUM")
	if err != nil {
		fmt.Println(err)
	}
}

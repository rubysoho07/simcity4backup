package main

import (
	"fmt"
	"os"
)

func backupPlugin() {

	if _, err := os.Stat("test.zip"); os.IsExist(err) {
		fmt.Println("File already exists")
		return
	}

	// TODO: Backup Plugin
}

func main() {
	fmt.Println("SimCity 4 Backup")

	backupPlugin()
}

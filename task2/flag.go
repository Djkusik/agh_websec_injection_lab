package main

import (
	"os"
	"github.com/joho/godotenv"
	"log"
)

func PrepareFlags() {
	err := godotenv.Load()
	if err != nil {
		log.Println("Error loading .env file")
	}

	flagFolder := getEnv("FLAG_FOLDER", "folder_with_a_flag_really")
	flagFile := getEnv("FLAG_FILE", "file_without_a_flag")
	flagContent := getEnv("FLAG_CONTENT", "bit{that_was_easy_yeah?}")

	_, err = os.Stat(flagFolder)
	if os.IsNotExist(err) {
		log.Println("Creating folder for flags")
		err := os.Mkdir(flagFolder, 0755)
		if err != nil {
			log.Fatal(err)
			os.Exit(1)
		}
	}

	_, err = os.Stat(flagFolder + "/" + flagFile)
	if os.IsNotExist(err) {
		log.Println("Creating flag file")
		f, err := os.Create(flagFolder + "/" + flagFile)
		if err != nil {
			log.Fatal(err)
		}
		_, err = f.WriteString(flagContent)
		if err != nil {
			f.Close()
			log.Fatal(err)
		}
		err = f.Close()
		if err != nil {
			log.Fatal(err)
		}
	}
}

func getEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return fallback
}
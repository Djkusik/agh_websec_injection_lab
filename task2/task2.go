package main

import (
	"fmt"
	"net/http"
	"log"
)

func handler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hi")
}

func main() {
	http.HandleFunc("/", handler)

	log.Println("Serving HTTP server on :5001")
	log.Fatal(http.ListenAndServe(":5001", nil))
}
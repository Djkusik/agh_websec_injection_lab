package main

import (
	"fmt"
	"net/http"
	"log"
	"os/exec"
	"time"
	"context"
	"html/template"
	"bytes"
)

type Page struct {
	Request string
	Response string
	ResponseError string
	UrlBase string
}

var urlBase string = "/"
var templates = template.Must(template.ParseFiles("./templates/index.html"))

func execCmd(cmdStr, arg string) (string, string, error) {
	var pingCmd = fmt.Sprintf("ping -c1 '%s'", arg)
	var argArr = []string{"-c", pingCmd}
	log.Printf("Command to exec: %s %s\n", cmdStr, argArr)

	ctx, cancel := context.WithTimeout(context.Background(), 5 * time.Second)
	defer cancel()

	cmd := exec.CommandContext(ctx, cmdStr, argArr...)

	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	err := cmd.Run()

	if ctx.Err() == context.DeadlineExceeded {
		return "", "Timeout", nil
	}

	if err != nil {
		return "", string(stderr.Bytes()), err
	}

	outStr, errStr := string(stdout.Bytes()), string(stderr.Bytes())
	return outStr, errStr, nil
}

func handler(w http.ResponseWriter, r *http.Request) {
	var paramKey = "pingUrl"
	params, ok := r.URL.Query()[paramKey]
	if !ok || len(params[0]) < 1 {
		log.Printf("URL Param '%s' is missing\n", paramKey)
		var defaultURL = fmt.Sprintf("%s?%s=%s", urlBase, paramKey, "1.1.1.1")
		http.Redirect(w, r, defaultURL, 302)
		return
	}

	outStr, errStr, err := execCmd("bash", params[0])
	var page = &Page{Request: params[0], Response: outStr, ResponseError: errStr, UrlBase: urlBase}
	if err != nil {
		page.ResponseError += "\n" + err.Error()
	}

	err = templates.ExecuteTemplate(w, "index.html", page)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

func main() {
	PrepareFlags()
	fs := http.FileServer(http.Dir("./static"))
	http.Handle(urlBase + "static/", http.StripPrefix(urlBase + "static/", fs))
	http.HandleFunc(urlBase, handler)

	log.Println("Serving HTTP server on :5001")
	log.Fatal(http.ListenAndServe(":5001", nil))
}
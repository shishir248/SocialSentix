package main

import (
	"bufio"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
)

type Symbol struct {
	Ticker string
}

func symbolHandler(w http.ResponseWriter, r *http.Request) {
	symbol := Symbol{r.URL.Path[1:]}

	t, _ := template.ParseFiles("./src/symbol.html")
	t.Execute(w, symbol)
}

func readLines(path string) ([]string, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines, scanner.Err()
}

func homeHandler(w http.ResponseWriter, r *http.Request) {
	t, _ := template.ParseFiles("./src/index.html")
	t.Execute(w, nil)
}

func main() {
	styles := http.FileServer(http.Dir("./src/assets/"))
	fmt.Println(http.StripPrefix("/src/", styles))
	http.Handle("/assets/", http.StripPrefix("/assets/", styles))

	symbols, err := readLines("../tickers.txt")
	if err != nil {
		log.Fatalf("unable to read file: %v", err)
	}

	for _, symbol := range symbols {
		url := fmt.Sprintf("/%s", symbol)
		http.HandleFunc(url, symbolHandler)
	}

	http.HandleFunc("/", homeHandler)
	http.HandleFunc("/home", homeHandler)

	fmt.Printf("Starting server at port 5946\n")
	if err := http.ListenAndServe(":5946", nil); err != nil {
		log.Fatal(err)
	}
}

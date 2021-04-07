package main

import (
	"fmt"
	"github.com/lucas-clemente/quic-go/h2quic"
	"io/ioutil"
	"math/rand"
	"net/http"
	"sync"
)

func initHTTP() {
	randSource := rand.NewSource(5831045521)
	random := rand.New(randSource)

	http.HandleFunc("/hello", func(res http.ResponseWriter, req *http.Request) {
		fmt.Println("receiving request")
		res.WriteHeader(200)
		res.Write(
			[]byte("hello!"),
		)
	})

	http.HandleFunc("/random-bin", func(res http.ResponseWriter, req *http.Request) {
		fmt.Println("receiving request to /random-bin")
		bytes, err := ioutil.ReadFile("/home/lhz/1.ogv")
		if err != nil {
		}
		res.WriteHeader(200)
		res.Write(bytes)
	})

	http.HandleFunc("/random-num", func(res http.ResponseWriter, req *http.Request) {
		res.WriteHeader(200)
		res.Write([]byte(string(random.Intn(1000000))))
	})

	http.HandleFunc("/greet", func(res http.ResponseWriter, req *http.Request) {
		name := req.URL.Query().Get("name")

		if name == "" {
			res.Write(
				[]byte("hello unnamed!"),
			)
		} else {
			res.Write(
				[]byte("hello " + name + "!"),
			)
		}
	})

	http.Handle("/files/", http.StripPrefix("/files/", http.FileServer(http.Dir("./files"))))
}

func init() {
	fmt.Println("running server initialization...")
	initHTTP()
}

func main() {
	fmt.Println("running main body...")

	certFile := "/home/lhz/server/server-cert.pem"
	keyFile := "/home/lhz/server/server-key.pem"
	listenURL := "172.20.6.96:4435"

	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		fmt.Printf("server running on %s\n", listenURL)
		err := h2quic.ListenAndServeQUIC(
			listenURL,
			certFile,
			keyFile,
			nil,
		)
		if err != nil {
			fmt.Println(err)
		}
		wg.Done()
	}()
	wg.Wait()
}

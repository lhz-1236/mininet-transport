package main

import (
	"fmt"
	"flag"
	"github.com/lucas-clemente/quic-go/h2quic"
        "github.com/lucas-clemente/quic-go/internal/utils"
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
		for i :=0;i<100;i++{
		    res.Write(bytes)
		}
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
	flag.Parse()
	listenURL := flag.Args()
	fmt.Println("running main body...")
	certFile := "/home/lhz/server/server-certmp.pem"
	keyFile := "/home/lhz/server/server-keymp.pem"

	utils.SetLogLevel(utils.LogLevelInfo)
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		fmt.Printf("server running on %s\n", listenURL[0])
		err := h2quic.ListenAndServeQUIC(
			listenURL[0],
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

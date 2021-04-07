package main

import (
	"bytes"
	"crypto/tls"
	"fmt"
	"github.com/lucas-clemente/quic-go"
	"github.com/lucas-clemente/quic-go/h2quic"
	"github.com/lucas-clemente/quic-go/internal/utils"
	"io"
	"flag"
	"net/http"
	"time"
)

func main() {
       	multipath := flag.Bool("m", false, "multipath")
	flag.Parse()
	listenURL := flag.Args()
	quicConfig := &quic.Config{
		CreatePaths: *multipath,
	}

	client := http.Client{
		Transport: &h2quic.RoundTripper{
			QuicConfig: quicConfig,
			TLSClientConfig: &tls.Config{
				InsecureSkipVerify: true,
			},
		},
	}
	utils.SetLogLevel(utils.LogLevelInfo)
	start := time.Now()
	res, err := client.Get("https://"+listenURL[0]+":4435/random-bin")
	if err != nil {
		panic(err.Error())
	}

	if err != nil {
		panic(err.Error())
	} else {
		buf := &bytes.Buffer{}
		io.Copy(buf, res.Body)
		elapsed := time.Since(start)
		fmt.Printf("LARGE FILE TOOK %s", elapsed)
	}
}

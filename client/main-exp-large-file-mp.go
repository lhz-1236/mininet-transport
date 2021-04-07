package main

import (
	"bytes"
	"crypto/tls"
	"fmt"
	"github.com/lucas-clemente/quic-go"
	"github.com/lucas-clemente/quic-go/h2quic"
	"github.com/lucas-clemente/quic-go/internal/utils"
	"io"
	//"io/ioutil"
	"net/http"
	"time"
)

func main() {
	quicConfig := &quic.Config{
		//	CacheHandshake: true,
		CreatePaths: true,
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
	res, err := client.Get("https://10.0.0.22:4435/random-bin")
	if err != nil {
		panic(err.Error())
	}

	if err != nil {
		panic(err.Error())
	} else {
		//f :=bufio.
		buf := &bytes.Buffer{}
		io.Copy(buf, res.Body)
		elapsed := time.Since(start)
		//f1.Write(res.Body)
	  //fmt.Println(buf)
		fmt.Printf("LARGE FILE TOOK %s", elapsed)
	}
}

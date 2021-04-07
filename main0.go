package main

import (
	"fmt"
	"flag"
)


func main() {
       	multipath := flag.Bool("m", false, "multipath")
	flag.Parse()
	listenURL := flag.Args()
        fmt.Println(*multipath)
	fmt.Println(listenURL)
}

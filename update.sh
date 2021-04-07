cd ~/go/src/github.com/lucas-clemente/quic-go/code/client
export GOBIN="/home/lhz/go/src/github.com/lucas-clemente/quic-go/code/client"
go install main-exp-large-file-mp.go
go install main-exp-large-file1.go
go install main-exp-large-file3.go
cd ~/go/src/github.com/lucas-clemente/quic-go/code/server
export GOBIN="/home/lhz/go/src/github.com/lucas-clemente/quic-go/code/server"
go install mainmp.go
go install main1.go
go install main3.go

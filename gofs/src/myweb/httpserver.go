package myweb

import (
	"fmt"
	"net/http"
)

type MyMux struct {

}


func sayhelloName(w http.ResponseWriter, r *http.Request) {
	_, _ = fmt.Fprintf(w, "Hello myroute!")
}
func (p *MyMux) ServeHTTP(w http.ResponseWriter, r *http.Request){
	if r.URL.Path == "/" {
		_, _ = fmt.Fprintf(w, "hello http server")
		return
	}
	http.NotFound(w, r)
	return
}
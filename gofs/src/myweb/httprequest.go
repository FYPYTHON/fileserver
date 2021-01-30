package myweb

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"mylog"
	"net/http"
	"net/url"
	"strings"
)

type HttpRequest struct {
	Server string
	Url    string
}
var httprequest HttpRequest

func init(){
	httprequest.Server = "127.0.0.1:9080"
	httprequest.Url = "/login"
	//httprequest = HttpRequest{Server:"127.0.0.1:9080", Url:"/login"}
}

func GetHttprequest() HttpRequest{
	return httprequest
}

func Map2json(params map[string] string) string{
	str, err := json.Marshal(params)
	if err != nil {
		mylog.Error.Println(err)
	}
	return string(str)
}
func Json2map(str []byte) map[string] interface{} {
	// string to byte: byte = []byte(string)
	tempmap := make(map[string] interface{})
	err := json.Unmarshal(str, &tempmap)
	if err != nil{
		mylog.Error.Println(err)
	}
	return tempmap

}
func (httprequest * HttpRequest) Post (params map[string] string) error {
	api_url := httprequest.Server + httprequest.Url
	fmt.Println("api url:" + api_url)
	jsonstr := Map2json(params)
	fmt.Println("parmas to json ", jsonstr)
	//map2 := json2map([]byte(jsonstr))
	//fmt.Println("json byte to map", map2)
	jsonstr = `{"inputCode":"App","password":"1234","userAccount":"test"}`
	jsonbyte := []byte(jsonstr)
	buffer := bytes.NewBuffer(jsonbyte)
	fmt.Println("params buffer", buffer)
	//otherp := strings.NewReader("userAccount=Tornado")
	request, err := http.NewRequest("POST", api_url, strings.NewReader(jsonstr) )
	if err != nil {
		mylog.Error.Println("http.NewRequest: %v", err)
		return err
	}
	request.Header.Set("Content-Type", "application/json;charset=UTF-8")
	request.Header.Set("User-Agent", "Mobile")
	client := http.Client{}
	resp, err := client.Do(request)
	if err != nil {
		mylog.Error.Println("client.Do: %v", err)
		return err
	}
	fmt.Println(resp.StatusCode)
	defer resp.Body.Close()
	respBytes, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		mylog.Error.Println("ioutil.ReadAll: %v", err)
		return err
	}
	fmt.Println(string(respBytes))
	return err

}

func (httprequest * HttpRequest) PostRequest(params url.Values) string {
	api_url := httprequest.Server + httprequest.Url
	params.Add("inputCode", "APP")
	params.Add("password","1234")
	params.Add("userAccount", "test")
	resp, _ := http.PostForm(api_url, params)

	resp.Header.Add("User-Agent", "Mobile")
	resp.Header.Set("Content-Type", "application/json;charset=UTF-8")
	body, _ := ioutil.ReadAll(resp.Body)
	fmt.Println(string(body))
	return "ok"
}

func (httprequest * HttpRequest) PostNew(params url.Values) string {
	api_url := httprequest.Server + httprequest.Url
	//bytesData, _ := json.Marshal(params)

	databyte := bytes.NewBufferString(params.Encode())

	client := &http.Client{}
	//req, _ := http.NewRequest("POST", api_url, bytes.NewReader(bytesData))
	req, err := http.NewRequest("POST", api_url, databyte)
	if err != nil {
		mylog.Error.Println("http.NewRequest: %v", err)
		return err.Error()
	}
	//resp, _ := client.PostForm(api_url, data)
	req.Header.Set("User-Agent", "Mobile")
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")


	resp, err := client.Do(req)
	if err != nil {
		mylog.Error.Println("client.Do: %v", err)
		return err.Error()
	}
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		mylog.Error.Println("ioutil.ReadAll: %v", err)
		return err.Error()
	}
	return string(body)
}

func (httprequest * HttpRequest) Get(params url.Values) string {
	api_url := httprequest.Server + httprequest.Url
	Url, err:= url.Parse(api_url)
	if err != nil {
		return err.Error()
	}

	Url.RawQuery = params.Encode()
	urlPath := Url.String()
	resp, err := http.Get(urlPath)

	if err != nil {
		return err.Error()
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	fmt.Println(body)
	return string(body)
}

func (httprequest * HttpRequest) GetNew(params url.Values) string {
	api_url := httprequest.Server + httprequest.Url
	//bytesData, _ := json.Marshal(params)

	databyte := bytes.NewBufferString(params.Encode())

	client := &http.Client{}
	//req, _ := http.NewRequest("POST", api_url, bytes.NewReader(bytesData))
	req, err := http.NewRequest("GET", api_url, databyte)
	if err != nil {
		mylog.Error.Println("http.NewRequest: %v", err)
		return err.Error()
	}

	req.Header.Set("User-Agent", "Mobile")
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")


	resp, err := client.Do(req)
	if err != nil {
		mylog.Error.Println("client.Do: %v", err)
		return err.Error()
	}
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		mylog.Error.Println("ioutil.ReadAll: %v", err)
		return err.Error()
	}
	return string(body)
}

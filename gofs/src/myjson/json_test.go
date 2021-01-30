package myjson

import "fmt"

func Jtest()  {
	strdata := `{
		"test": {
			"array": [1, "2", 3],
			"int": 10,
			"float": 5.150,
			"bignum": 9223372036854775807,
			"string": "simplejson",
			"bool": true
		}
	}`
	js, err := NewJson([]byte(strdata))
	if js != nil {
		arr, _ := js.Get("test").Get("array").Array()
		i, _ := js.Get("test").Get("int").Int()
		ms := js.Get("test").Get("string").MustString()
		fmt.Println(arr)
		fmt.Println(i)
		fmt.Println(ms)
	}
	fmt.Println(err)

}

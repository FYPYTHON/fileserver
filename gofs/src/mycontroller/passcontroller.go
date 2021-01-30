package mycontroller

import (
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/logs"
)

type PassController struct {
	beego.Controller
}

// @router /pass [get]
func (ps *PassController) Get(){
	common()
	ps.ServeJSON()
}

type Message interface {
	Msg()
	Send()
}
type Email struct {
	name string
	msg string
}
type Web struct {
	name string
	msg string
}
func (e *Email) Msg() {
	e.name = "email"
	e.msg = "have a email to send"
}

func (e *Email) Send(){
	e.Msg()
	logs.Info(e.name, e.msg)
}

func (w *Web) Msg(){
	w.name = "web"
	w.msg = "have web http info to send"
}

func (w *Web) Send(){
	w.Msg()
	logs.Info(w.name, w.msg)
}
func common(){
	//e := Email{}
	//w := Web{}
	//e.Send()
	//w.Send()
	c := Message(&Email{})
	d := Message(&Web{})
	c.Send()
	d.Send()
}
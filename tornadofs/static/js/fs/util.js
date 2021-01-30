"use strict";

let a = 1;

let alertModal = {
    template:`
    <div>
    <div class="modal fade" v-show="showMask" id="myModal" tabindex="-1"
        role="dialog" aria-labelledby="myModalLabel" aria-hidden="false" data-backdrop="static">
        <div class="modal-dialog modal-sm myalert">
            <div class="modal-header">
                <button class="close" type="button" @click="closeMask" data-dismiss="modal" aria-hidden="true">&times;</button>
                <h4 class="dialog-title">{{title}}</h4>
            </div>
            <div class="modal-body" v-html="content">{{mycontent}}</div>
            <div class="modal-footer">
                <div class="btn btn-info" @click="closeBtn" data-dismiss="modal" aria-hidden="true">
                    {{cancelText}}
                </div>
                <div class="btn btn-danger" @click="dangerBtn" data-dismiss="modal" aria-hidden="true">
                    {{dangerText}}
                </div>
                <div class="btn btn-primary" @click="confirmBtn" data-dismiss="modal" aria-hidden="true">
                    {{confirmText}}
                </div>
            </div>
        </div>
    </div>
    </div>
    `,
    props: {
        value: {},
        // 类型包括 defalut 默认， danger 危险， confirm 确认，
        type:{
            type: String,
            default: 'default'
        },
        content: {
            type: String,
            default: 'Message'
        },
        title: {
            type: String,
            default: '确认是否删除！'
        },
        cancelText: {
            type: String,
            default: '取消'
        },
        dangerText: {
            type: String,
            default: '删除'
        },

        confirmText: {
            type: String,
            default: '确认'
        },

    },
    data(){
        return{
            showMask: false,
            mycontent: this.content,
        }
    },
    methods:{
        closeMask(){
            this.showMask = false;
        },
        closeBtn(){
            this.closeMask();
        },
        dangerBtn(){
            this.closeMask();
        },
        confirmBtn(){
            this.closeMask();
        },
        showModal(){
            console.log("modal show");
            $('#myModal').modal('show');
            // $('#myModal').modal();
            // data-backdrop="static"
        },
        setContent(content){
        	console.log("setContent...");
        	this.mycontent = content;
        	// this.title = "展示"
        	// this.$emit("setProps", "title", content);
        	this.showMask = true;
        }
    },
}

let alertCmpt = {
    template:`
    <div class="mymodal col-sm-12" v-show="showMask">
	    <div class="modal-dialog col-sm-12">
	        <div class="modal-header col-sm-12">
	          <h3>{{title}}</h3>
	        </div>
	        <div class="modal-body col-sm-12">
	            <ul class="list-unstyled" v-for="item in content">
		            <li>{{item}}</li>
		        </ul>
	        </div>
	        <div class="modal-footer col-sm-12">
            	<button type="button" class="btn-close" @click="closeBtn">{{cancelText}}</button>
            	<button type="button" class="btn-confirm" @click="confirmBtn">{{confirmText}}</button>
        	</div>
	    </div>
    </div>

    `,
    data(){
        return{
            showMask: false,
            content: [],
            cancelText: "取消",
            confirmText: "确认",
            title: "匹配结果",
        }
    },
    methods:{
        closeMask(){
            this.showMask = false;
        },
        closeBtn(){
            this.closeMask();
        },
        confirmBtn(){
            this.closeMask();
        },
        showModal(){
            this.showMask = true;
        },
        setContent(content){
        	// console.log("setContent...");
        	this.content = content;
        	this.showModal();
        }
    },
}

let alertcommon = new Vue({
    el:'#modalapp',
    template:`<modalapp ref="myalert"></modalapp>`,
    components:{
        'modalapp':alertCmpt,
    },
})
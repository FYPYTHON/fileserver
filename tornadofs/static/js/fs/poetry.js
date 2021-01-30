"use strict";
// 解决兼容问题 
let store = {
    conenteId:'search',
    bodyId: 'bodyContent',
    poem: {},
    alticle: {},
    poemlike: [],
    aggdefault: "唐诗三百首",
    agglist:[],
    categorylist:[],
    filelist: {
        data: [],
        type: 0,
    },
    actions: {
        getFileList: function(agg, ftype){
            $.ajax({
                url: '/study',
                async : false,
                type: 'GET',
                data: {
                    agg: agg,
                    type: ftype
                },
                dataType: 'json',
                success: function (data) {

                    var all_file_directory = data.filelist;
                    store.filelist.data = all_file_directory;
                    store.agglist = data.agglist;
                }
            })
        },
        getFileCategoryList: function(agg, category, ftype){
            $.ajax({
                url: '/alticles',
                async : false,
                type: 'GET',
                data: {
                    agg: agg,
                    category: category,
                    type: ftype
                },
                dataType: 'json',
                success: function (data) {

                    var all_file_directory = data.filelist;
                    store.filelist.data = all_file_directory;
                    store.agglist = data.agglist;
                    store.categorylist = data.categorylist;
                }
            })
        },
        getFileListSync: function(agg, ftype){
            $.getJSON({
                url: '/study',
                type: 'GET',
                data: {
                    agg: path,
                    type: ftype
                },
                dataType: 'json',
                success: function (data) {
                    console.log("search ok...");
                    $("#searchResultSync li").html("");
                    var result = parseInt(data.error_code);
                    if(result != 0){
                        alert("errorcode:"+ data.error_code + "\nderccription:" + data.msg);
                    }
                    else{
                        // var all_file_directory = data.filelist.directory.concat(data.filelist.file);
                        var all_file_directory = data.filelist;
                        store.filelist.data = data.filelist;
                        store.agglist = data.agglist;
                        // console.log(all_file_directory);
                        $("#searchResultSync").html("");
                        for (var i = 0; i < all_file_directory.length; i++) {
                            var item = '<li>' + all_file_directory[i] + '</li>';
                            $("#searchResultSync").append(item);  
                        }
                    }
                }
            })
        },
        getPoemSync(pid, sync){
        	$.getJSON({
                url: '/poem',
                async : sync,
                type: 'GET',
                data: {
                    pid: pid,
                },
                dataType: 'json',
                success: function (data) {
                	var result = parseInt(data.error_code);
                	if(result != 0){
                		store.poem = data.poem;
                        alert(data.msg);
                    } else {
                    	store.poem = data.poem;
                    }
                }
            })
        },
        getAlticleSync(pid, sync){
        	$.getJSON({
                url: '/alticle',
                async : sync,
                type: 'GET',
                data: {
                    pid: pid,
                },
                dataType: 'json',
                success: function (data) {
                	var result = parseInt(data.error_code);
                	if(result != 0){
                		store.alticle = data.alticle;
                        alert(data.msg);
                    } else {
                    	store.alticle = data.alticle;
                    }
                }
            })
        },
        getPoemLikeSync(key, keys){
        	$.getJSON({
                url: '/poemlike',
                async : false,
                type: 'GET',
                data: {
                    keys: keys,
                    key: key,
                },
                dataType: 'json',
                success: function (data) {
                	var result = parseInt(data.error_code);
                	if(result != 0){
                        // alert(data.msg);
                        return data.msg
                    } else {
                    	if (data.poemlike.length < 1){
                    		alert("没有匹配的数据");
                    		return;
                    	}
                    	store.poemlike = [];
                    	var msg = "匹配 " + data.poemlike.length + "条\n";
                    	store.poemlike.push(msg);
                    	for (var i = 0; i < data.poemlike.length; i++) {
                    		msg = i + "、" + data.poemlike[i];
                    		store.poemlike.push(msg);
                    	}
                    	// console.log(msg);
                    	// alert(msg);
                    	// alertcommon.$children[0].setContent(msg);
                    	// store.poemlike = msg;
                    }
                }
            })
        },
        
    }
}


let searchContent = {
	template: `
	<div class="form form-group" id="searchContent">
		<div class="col-sm-4 ">
	        <label style="float:left;">请输入关键字：</label>
	    </div>
	    <div class="col-sm-8 ">
	        <input type="text" class="form-control" v-model="inputpath" ref="refpath" 
	         placeholder="请输入关键字" value="/">
	    </div>
	    <div class="col-sm-12 myseperator">  </div>
	    <div class="col-sm-3">
	        <button class="btn btn-primary" @click="search_poemlike()">{{searchbtn}}</button>
	    </div>
	    <alertCmpt ref="alertcmpt"></alertCmpt>
	</div>
	`
	,
	// <alertCmpt ref="alertcmpt"></alertCmpt>
	data() {
        return {
        	searchbtn: '搜索',
            type : 1,
            inputpath:null,
            filelist: store.filelist.data,
        }
    },
    components:{
    	'alertCmpt': alertCmpt,
    },
    methods:{
        search_poemlike(){
            // input取值 使用ref 或 v-model
            // var path = this.$refs.refpath.value
            if(this.inputpath == "" || this.inputpath == null){
            	alert("关键字为空");
            	return;
            }
            var keys = this.inputpath.split(" ");
            // console.log(keys);
            var newkeys = Array();
            for(var i=0; i<keys.length; i++){
            	if (keys[i] != ""){
            		newkeys.push(keys[i]);
            	}
            }
            // console.log(newkeys);
            if(newkeys.length > 1){
            	store.actions.getPoemLikeSync(null, newkeys);
            } else {
            	store.actions.getPoemLikeSync(newkeys[0], []);
            }
            
            // alertcommon.$refs.myalert.setContent(store.poemlike);
            this.$refs.alertcmpt.setContent(store.poemlike);
        }
    }
}

let poemContent = {
	template: `
	<div class="col-sm-12" v-show="showpoem">
		<div class="col-sm-4" style="margin-top:50px;"></div>
		<div class="col-sm-4 poemcontemt">{{poem['title']}}</div>
		<div class="col-sm-4"></div>
		<div class="col-sm-12 myseperator"></div>

		<div class="col-sm-4" style="margin-top:25px;"></div>
		<div class="col-sm-4 poemcontemt">{{poem['poet']}}</div>
		<div class="col-sm-4"></div>
		<div class="col-sm-12 myseperator"></div>

		<div class="col-sm-2" style="margin-top:20px;"></div>
		<div class="col-sm-8 poemcontemt ">
			<ul class="list-unstyled" v-for="item in poem['content']">
	            <li>{{item}}</li>
	        </ul>
	        <div class="col-sm-12 myseperator"></div>
		</div>
		<div class="col-sm-2"></div>
		<div class="col-sm-12 myseperator"></div>
		<button class="col-sm-2 btn btn-info" @click="show_describe()">{{btnname}}</button>
		<div class="col-sm-12 poemdescribe">
			
	        <div class="col-sm-12 myseperator"></div>
	        <ul class="col-sm-12 list-unstyled" v-show=isdetail v-for="detail in poem['describe']">
	            <li><p>{{detail}}</p></li>
	        </ul>
        </div>
	</div>
	`,
	data: function(){
		return {
			poem: store.poem,
			isdetail: false,
			btnname: '显示鉴赏',
			showpoem: false,
			// poem: this.$poem,
		}
	},
	watch: {
		poem: {
	　　　　handler(newValue, oldValue) {
				// console.log("...watch...");
	// 　　　　　　 console.log(newValue);
	　　　　},
	　　　　deep: true
	　　}
	},
	// data() {
	// 	return {
	// 		poem: store.poem,
	// 	}
	// },
	created: function(){
		if (store.filelist.data.length >= 1){
			store.actions.getPoemSync(store.filelist.data[0][0], false);
		}
		if (store.poem == ""){
			this.showpoem = false;
		} else {
			this.showpoem = true;
			this.poem = store.poem;
		}
		
		// console.log("created");
	},
	methods:{
		poemChange(){
			// console.log("recv");
			this.poem = store.poem;
		},
		show_describe(){
			if (this.isdetail == true)
			{
				this.isdetail =false;
				this.btnname = "显示鉴赏"
			} else {
				this.isdetail = true;
				this.btnname = "隐藏鉴赏"
			}
			
		},
	},
	
}

let navBar = {
	template:`
    <nav class="navbar navbar-default">
        <div class="container-fluid">
              <ul class="nav navbar-nav">
                <li class="active" @click="poemBody">{{home}}</li>
                <li @click="alticleBody">{{about}}</li>               
              </ul>
        </div>
    </nav>
    `,
    data:function(){
        return {
            home:'Home',
            about:'About'
        }
    },
    methods:{
    	poemBody(){
    		console.log(this.home);
    		store.bodyId = "bodyContent";
    		this.$emit("bodyChange");
    	},
    	alticleBody(){
    		console.log(this.about);
    		store.bodyId = "alticleContent";
    		this.$emit("bodyChange");
    	},

    }
}

let mainContent = {
	template:`
    <h1 class="fs-title ">{{ content }}</h1>
    `,
    data:function(){
        return {
            content:'文件列表查看'
        }
    }
}

let bodyContent = {
	// <componentb v-bind:is="compID"></componentb>
    template:`
    <div class="col-sm-12">
        <div class="col-sm-4 mymenu myborder">
            <div class="mytempdiv">
            	<label style="float:left;">请选择分类：</label>
            	<select class="myselect" v-model='aggname' @change="selectAgg($event)">
	                <option v-for="(name,index) in agglist" :value=name>{{name}}</option>
            	</select>
            </div>
            <ul class="list-unstyled" v-for="item in filelist">
	            <li :class="{liselected:selectIndex==item[0]}" :id=item[0] @click="show_detail(item[0])">{{item[1]}} {{item[2]}}</li>
	        </ul>
        </div>
        <div class="col-sm-8 mycontent myborder" id="compID">
            <div class="mytempdiv ">内容</div>
            <search></search>
            <poem ref='mypoem'></poem>
        </div>
    </div>
    `,
    data: function() {
        return {
        	selectIndex: 0,
        	aggname: store.aggdefault,
        	agglist: store.agglist,
            compID: store.conenteId,
            filelist: store.filelist.data,
        }
    },
    
    created: function(){
    	store.actions.getFileList(store.aggdefault, 10);
    	this.filelist = store.filelist.data;
    	this.agglist = store.agglist;
    	if (this.filelist.length > 0) {
    		this.selectIndex = this.filelist[0][0];
    	}
    	// this.aggname = store.aggdefault;
    	// console.log(this.filelist);
    },
    components:{
        'search': searchContent,
        'poem': poemContent,
    },
    methods:{
        showsearch(){
            this.compID = 'search';
            store.filelist.data = []
        },
        show_detail(pid){

        	store.actions.getPoemSync(pid, false);
        	this.$refs.mypoem.poemChange();

        },
        selectAgg(e){
        	// console.log(e);
        	// console.log(e.target.selectedIndex) // 选择项的index索引
            // console.log(e.target.value) // 选择项的value
            store.actions.getFileList(e.target.value, 10);
    		this.filelist = store.filelist.data;
        }
    }
}

let app = {
    template:`
    <div class="container">
        <div class="row">
            <nav-bar></nav-bar>
        </div>
        <div class="row">
            <main-content></main-content>
        </div>
        <div class="container-fluid">`+
            // <leftMenu></leftMenu>
            // <rightContent></rightContent>
            // `<bodyContent v-bind:is="bodyCmt"></bodyContent>
            `<bodyselect v-bind:is="bodyCmt"></bodyselect>
        </div>
    </div>
    `,
    data(){
    	return {
    		// bodyCmt: store.bodyId,
    		bodyCmt: 'alticleContent',
    	}
    },
    components:{
        'nav-bar':navBar,
        'main-content':mainContent,
        // 'leftMenu':leftMenu,
        // 'rightContent':rightContent,
        'bodyContent':bodyContent,
        'alticleContent': alticleBody,
    },
    methods: {
    	bodyChange(){
    		console.log("bodyChange...");
    		this.bodyCmt = store.bodyId;
    	},
    },
}

let root = new Vue({
    el:'#app',
    template:`<app></app>`,
    // poem: {},
    components:{
        'app':app
    },
})



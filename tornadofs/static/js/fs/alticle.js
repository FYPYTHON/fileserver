"use strict";

let alticleContent = {
	template: `
	<div class="col-sm-12" v-show="showalticle">
		<div class="col-sm-1" style="margin-top:50px;"></div>
		<div class="col-sm-10 alticlecontent">{{alticle['title']}}</div>
		<div class="col-sm-1"></div>
		<div class="col-sm-12 myseperator"></div>

		<div class="col-sm-1" style="margin-top:25px;"></div>
		<div class="col-sm-10 alticlecontent">{{alticle['author']}}</div>
		<div class="col-sm-1"></div>
		<div class="col-sm-12 myseperator"></div>

		<div class="col-sm-1" style="margin-top:20px;"></div>
		<div class="col-sm-10 alticlecontent ">
			<ul class="list-unstyled" v-for="item in alticle['content']">
	            <li>{{item}}</li>
	        </ul>
	        <div class="col-sm-12 myseperator"></div>
		</div>
		<div class="col-sm-1"></div>
		<div class="col-sm-12 myseperator"></div>
		<button class="col-sm-2 btn btn-info" @click="show_describe()">{{btnname}}</button>
		<div class="col-sm-12 poemdescribe">
			
	        <div class="col-sm-12 myseperator"></div>
	        <ul class="col-sm-12 list-unstyled" v-show=isdetail v-for="detail in alticle['describe']">
	            <li><p>{{detail}}</p></li>
	        </ul>
        </div>
	</div>
	`,
	data: function(){
		return {
			alticle: store.alticle,
			isdetail: false,
			btnname: '显示鉴赏',
			showalticle: false,
			// alticle: this.$alticle,
		}
	},
	watch: {
		alticle: {
	　　　　handler(newValue, oldValue) {
	// 　　　　　　 console.log(newValue);
	　　　　},
	　　　　deep: true
	　　}
	},
	created: function(){
		if (store.filelist.data.length >= 1){
			store.actions.getAlticleSync(store.filelist.data[0][0], false);
		}
		if (store.alticle == ""){
			this.showalticle = false;
		} else {
			this.showalticle = true;
			this.alticle = store.alticle;
		}
		
	},
	methods:{
		alticleChange(){
			// console.log("recv");
			this.alticle = store.alticle;
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

let alticleBody = {
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
            <div class="col-sm-12">
				<select class="myselect" v-model='categoryname' @change="selectCategory($event)">
		            <option v-for="(name,index) in categorylist" :value=name>{{name}}</option>
		    	</select>
			</div>
            <alticle ref='myalticle'></alticle>
        </div>
    </div>
    `,
    data: function() {
        return {
        	selectIndex: 0,
        	aggname: "中华上下五千年",
        	categoryname: "文章",
        	agglist: store.agglist,
        	categorylist: store.category,
            compID: store.conenteId,
            filelist: store.filelist.data,
        }
    },
    
    created: function(){
    	// console.log("alticle created");
    	store.actions.getFileCategoryList(this.aggname, this.categoryname, 10);
    	this.filelist = store.filelist.data;
    	this.agglist = store.agglist;
    	this.categorylist = store.categorylist;
    	if (this.filelist.length > 0) {
    		this.selectIndex = this.filelist[0][0];
    	}
    	this.initSelectIndex();
    	
    	// this.aggname = store.aggdefault;
    	// console.log(this.filelist);
    },
    components:{
        'alticle': alticleContent,
    },
    methods:{
        showsearch(){
            this.compID = 'search';
            store.filelist.data = []
        },
        show_detail(pid){
        	this.selectIndex = pid;
        	store.actions.getAlticleSync(pid, false);
        	this.$refs.myalticle.alticleChange();

        },
        initSelectIndex(){
        	if (this.filelist.length > 0) {
        		console.log("selectIndex change...");
	    		this.selectIndex = this.filelist[0][0];
	    	}
        },
        selectAgg(e){
        	// console.log(e);
        	// console.log(e.target.selectedIndex) // 选择项的index索引
            // console.log(e.target.value) // 选择项的value
            this.aggname = e.target.value;
            store.actions.getFileCategoryList(this.aggname, "", 10);
    		// this.filelist = store.filelist.data;

    		this.categorylist = store.categorylist;
    		this.categoryname = this.categorylist[0];
    		this.agglist = store.agglist;
    		this.filelist = store.filelist.data;
    		this.initSelectIndex();

        },
        selectCategory(e){
        	// console.log(e);
        	// console.log(e.target.selectedIndex) // 选择项的index索引
            // console.log(e.target.value) // 选择项的value
            this.categoryname = e.target.value;
            store.actions.getFileCategoryList(this.aggname, this.categoryname, 10);
            this.categorylist = store.categorylist;
    		this.filelist = store.filelist.data;
    		this.initSelectIndex();
        }
    }
}
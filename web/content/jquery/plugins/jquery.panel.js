/**
 * jQuery EasyUI 1.3.1
 * 
 * Licensed under the GPL terms
 * To use it on other terms please contact us
 *
 * Copyright(c) 2009-2012 stworthy [ stworthy@gmail.com ] 
 * 
 */
(function($){
function _1(_2){
_2.each(function(){
$(this).remove();
if($.browser.msie){
this.outerHTML="";
}
});
};
function _3(_4,_5){
var _6=$.data(_4,"panel").options;
var _7=$.data(_4,"panel").panel;
var _8=_7.children("div.panel-header");
var _9=_7.children("div.panel-body");
if(_5){
if(_5.width){
_6.width=_5.width;
}
if(_5.height){
_6.height=_5.height;
}
if(_5.left!=null){
_6.left=_5.left;
}
if(_5.top!=null){
_6.top=_5.top;
}
}
if(_6.fit==true){
var p=_7.parent();
p.addClass("panel-noscroll");
if(p[0].tagName=="BODY"){
$("html").addClass("panel-fit");
}
_6.width=p.width();
_6.height=p.height();
}
_7.css({left:_6.left,top:_6.top});
if(!isNaN(_6.width)){
_7._outerWidth(_6.width);
}else{
_7.width("auto");
}
_8.add(_9)._outerWidth(_7.width());
if(!isNaN(_6.height)){
_7._outerHeight(_6.height);
_9._outerHeight(_7.height()-_8._outerHeight());
}else{
_9.height("auto");
}
_7.css("height","");
_6.onResize.apply(_4,[_6.width,_6.height]);
_7.find(">div.panel-body>div").triggerHandler("_resize");
};
function _a(_b,_c){
var _d=$.data(_b,"panel").options;
var _e=$.data(_b,"panel").panel;
if(_c){
if(_c.left!=null){
_d.left=_c.left;
}
if(_c.top!=null){
_d.top=_c.top;
}
}
_e.css({left:_d.left,top:_d.top});
_d.onMove.apply(_b,[_d.left,_d.top]);
};
function _f(_10){
$(_10).addClass("panel-body");
var _11=$("<div class=\"panel\"></div>").insertBefore(_10);
_11[0].appendChild(_10);
_11.bind("_resize",function(){
var _12=$.data(_10,"panel").options;
if(_12.fit==true){
_3(_10);
}
return false;
});
return _11;
};
function _13(_14){
var _15=$.data(_14,"panel").options;
var _16=$.data(_14,"panel").panel;
if(_15.tools&&typeof _15.tools=="string"){
_16.find(">div.panel-header>div.panel-tool .panel-tool-a").appendTo(_15.tools);
}
_1(_16.children("div.panel-header"));
if(_15.title&&!_15.noheader){
var _17=$("<div class=\"panel-header\"><div class=\"panel-title\">"+_15.title+"</div></div>").prependTo(_16);
if(_15.iconCls){
_17.find(".panel-title").addClass("panel-with-icon");
$("<div class=\"panel-icon\"></div>").addClass(_15.iconCls).appendTo(_17);
}
var _18=$("<div class=\"panel-tool\"></div>").appendTo(_17);
_18.bind("click",function(e){
e.stopPropagation();
});
if(_15.tools){
if(typeof _15.tools=="string"){
$(_15.tools).children().each(function(){
$(this).addClass($(this).attr("iconCls")).addClass("panel-tool-a").appendTo(_18);
});
}else{
for(var i=0;i<_15.tools.length;i++){
var t=$("<a href=\"javascript:void(0)\"></a>").addClass(_15.tools[i].iconCls).appendTo(_18);
if(_15.tools[i].handler){
t.bind("click",eval(_15.tools[i].handler));
}
}
}
}
if(_15.collapsible){
$("<a class=\"panel-tool-collapse\" href=\"javascript:void(0)\"></a>").appendTo(_18).bind("click",function(){
if(_15.collapsed==true){
_39(_14,true);
}else{
_29(_14,true);
}
return false;
});
}
if(_15.minimizable){
$("<a class=\"panel-tool-min\" href=\"javascript:void(0)\"></a>").appendTo(_18).bind("click",function(){
_44(_14);
return false;
});
}
if(_15.maximizable){
$("<a class=\"panel-tool-max\" href=\"javascript:void(0)\"></a>").appendTo(_18).bind("click",function(){
if(_15.maximized==true){
_48(_14);
}else{
_28(_14);
}
return false;
});
}
if(_15.closable){
$("<a class=\"panel-tool-close\" href=\"javascript:void(0)\"></a>").appendTo(_18).bind("click",function(){
_19(_14);
return false;
});
}
_16.children("div.panel-body").removeClass("panel-body-noheader");
}else{
_16.children("div.panel-body").addClass("panel-body-noheader");
}
};
function _1a(_1b){
var _1c=$.data(_1b,"panel");
if(_1c.options.href&&(!_1c.isLoaded||!_1c.options.cache)){
_1c.isLoaded=false;
_1d(_1b);
var _1e=_1c.panel.find(">div.panel-body");
if(_1c.options.loadingMessage){
_1e.html($("<div class=\"panel-loading\"></div>").html(_1c.options.loadingMessage));
}
$.ajax({url:_1c.options.href,cache:false,success:function(_1f){
_1e.html(_1c.options.extractor.call(_1b,_1f));
if($.parser){
$.parser.parse(_1e);
}
_1c.options.onLoad.apply(_1b,arguments);
_1c.isLoaded=true;
}});
}
};
function _1d(_20){
var t=$(_20);
t.find(".combo-f").each(function(){
$(this).combo("destroy");
});
t.find(".m-btn").each(function(){
$(this).menubutton("destroy");
});
t.find(".s-btn").each(function(){
$(this).splitbutton("destroy");
});
};
function _21(_22){
$(_22).find("div.panel:visible,div.accordion:visible,div.tabs-container:visible,div.layout:visible").each(function(){
$(this).triggerHandler("_resize",[true]);
});
};
function _23(_24,_25){
var _26=$.data(_24,"panel").options;
var _27=$.data(_24,"panel").panel;
if(_25!=true){
if(_26.onBeforeOpen.call(_24)==false){
return;
}
}
_27.show();
_26.closed=false;
_26.minimized=false;
_26.onOpen.call(_24);
if(_26.maximized==true){
_26.maximized=false;
_28(_24);
}
if(_26.collapsed==true){
_26.collapsed=false;
_29(_24);
}
if(!_26.collapsed){
_1a(_24);
_21(_24);
}
};
function _19(_2a,_2b){
var _2c=$.data(_2a,"panel").options;
var _2d=$.data(_2a,"panel").panel;
if(_2b!=true){
if(_2c.onBeforeClose.call(_2a)==false){
return;
}
}
_2d.hide();
_2c.closed=true;
_2c.onClose.call(_2a);
};
function _2e(_2f,_30){
var _31=$.data(_2f,"panel").options;
var _32=$.data(_2f,"panel").panel;
if(_30!=true){
if(_31.onBeforeDestroy.call(_2f)==false){
return;
}
}
_1d(_2f);
_1(_32);
_31.onDestroy.call(_2f);
};
function _29(_33,_34){
var _35=$.data(_33,"panel").options;
var _36=$.data(_33,"panel").panel;
var _37=_36.children("div.panel-body");
var _38=_36.children("div.panel-header").find("a.panel-tool-collapse");
if(_35.collapsed==true){
return;
}
_37.stop(true,true);
if(_35.onBeforeCollapse.call(_33)==false){
return;
}
_38.addClass("panel-tool-expand");
if(_34==true){
_37.slideUp("normal",function(){
_35.collapsed=true;
_35.onCollapse.call(_33);
});
}else{
_37.hide();
_35.collapsed=true;
_35.onCollapse.call(_33);
}
};
function _39(_3a,_3b){
var _3c=$.data(_3a,"panel").options;
var _3d=$.data(_3a,"panel").panel;
var _3e=_3d.children("div.panel-body");
var _3f=_3d.children("div.panel-header").find("a.panel-tool-collapse");
if(_3c.collapsed==false){
return;
}
_3e.stop(true,true);
if(_3c.onBeforeExpand.call(_3a)==false){
return;
}
_3f.removeClass("panel-tool-expand");
if(_3b==true){
_3e.slideDown("normal",function(){
_3c.collapsed=false;
_3c.onExpand.call(_3a);
_1a(_3a);
_21(_3a);
});
}else{
_3e.show();
_3c.collapsed=false;
_3c.onExpand.call(_3a);
_1a(_3a);
_21(_3a);
}
};
function _28(_40){
var _41=$.data(_40,"panel").options;
var _42=$.data(_40,"panel").panel;
var _43=_42.children("div.panel-header").find("a.panel-tool-max");
if(_41.maximized==true){
return;
}
_43.addClass("panel-tool-restore");
if(!$.data(_40,"panel").original){
$.data(_40,"panel").original={width:_41.width,height:_41.height,left:_41.left,top:_41.top,fit:_41.fit};
}
_41.left=0;
_41.top=0;
_41.fit=true;
_3(_40);
_41.minimized=false;
_41.maximized=true;
_41.onMaximize.call(_40);
};
function _44(_45){
var _46=$.data(_45,"panel").options;
var _47=$.data(_45,"panel").panel;
_47.hide();
_46.minimized=true;
_46.maximized=false;
_46.onMinimize.call(_45);
};
function _48(_49){
var _4a=$.data(_49,"panel").options;
var _4b=$.data(_49,"panel").panel;
var _4c=_4b.children("div.panel-header").find("a.panel-tool-max");
if(_4a.maximized==false){
return;
}
_4b.show();
_4c.removeClass("panel-tool-restore");
var _4d=$.data(_49,"panel").original;
_4a.width=_4d.width;
_4a.height=_4d.height;
_4a.left=_4d.left;
_4a.top=_4d.top;
_4a.fit=_4d.fit;
_3(_49);
_4a.minimized=false;
_4a.maximized=false;
$.data(_49,"panel").original=null;
_4a.onRestore.call(_49);
};
function _4e(_4f){
var _50=$.data(_4f,"panel").options;
var _51=$.data(_4f,"panel").panel;
var _52=$(_4f).panel("header");
var _53=$(_4f).panel("body");
_51.css(_50.style);
_51.addClass(_50.cls);
if(_50.border){
_52.removeClass("panel-header-noborder");
_53.removeClass("panel-body-noborder");
}else{
_52.addClass("panel-header-noborder");
_53.addClass("panel-body-noborder");
}
_52.addClass(_50.headerCls);
_53.addClass(_50.bodyCls);
if(_50.id){
$(_4f).attr("id",_50.id);
}else{
$(_4f).attr("id","");
}
};
function _54(_55,_56){
$.data(_55,"panel").options.title=_56;
$(_55).panel("header").find("div.panel-title").html(_56);
};
var TO=false;
var _57=true;
$(window).unbind(".panel").bind("resize.panel",function(){
if(!_57){
return;
}
if(TO!==false){
clearTimeout(TO);
}
TO=setTimeout(function(){
_57=false;
var _58=$("body.layout");
if(_58.length){
_58.layout("resize");
}else{
$("body").children("div.panel,div.accordion,div.tabs-container,div.layout").triggerHandler("_resize");
}
_57=true;
TO=false;
},200);
});
$.fn.panel=function(_59,_5a){
if(typeof _59=="string"){
return $.fn.panel.methods[_59](this,_5a);
}
_59=_59||{};
return this.each(function(){
var _5b=$.data(this,"panel");
var _5c;
if(_5b){
_5c=$.extend(_5b.options,_59);
}else{
_5c=$.extend({},$.fn.panel.defaults,$.fn.panel.parseOptions(this),_59);
$(this).attr("title","");
_5b=$.data(this,"panel",{options:_5c,panel:_f(this),isLoaded:false});
}
if(_5c.content){
$(this).html(_5c.content);
if($.parser){
$.parser.parse(this);
}
}
_13(this);
_4e(this);
if(_5c.doSize==true){
_5b.panel.css("display","block");
_3(this);
}
if(_5c.closed==true||_5c.minimized==true){
_5b.panel.hide();
}else{
_23(this);
}
});
};
$.fn.panel.methods={options:function(jq){
return $.data(jq[0],"panel").options;
},panel:function(jq){
return $.data(jq[0],"panel").panel;
},header:function(jq){
return $.data(jq[0],"panel").panel.find(">div.panel-header");
},body:function(jq){
return $.data(jq[0],"panel").panel.find(">div.panel-body");
},setTitle:function(jq,_5d){
return jq.each(function(){
_54(this,_5d);
});
},open:function(jq,_5e){
return jq.each(function(){
_23(this,_5e);
});
},close:function(jq,_5f){
return jq.each(function(){
_19(this,_5f);
});
},destroy:function(jq,_60){
return jq.each(function(){
_2e(this,_60);
});
},refresh:function(jq,_61){
return jq.each(function(){
$.data(this,"panel").isLoaded=false;
if(_61){
$.data(this,"panel").options.href=_61;
}
_1a(this);
});
},resize:function(jq,_62){
return jq.each(function(){
_3(this,_62);
});
},move:function(jq,_63){
return jq.each(function(){
_a(this,_63);
});
},maximize:function(jq){
return jq.each(function(){
_28(this);
});
},minimize:function(jq){
return jq.each(function(){
_44(this);
});
},restore:function(jq){
return jq.each(function(){
_48(this);
});
},collapse:function(jq,_64){
return jq.each(function(){
_29(this,_64);
});
},expand:function(jq,_65){
return jq.each(function(){
_39(this,_65);
});
}};
$.fn.panel.parseOptions=function(_66){
var t=$(_66);
return $.extend({},$.parser.parseOptions(_66,["id","width","height","left","top","title","iconCls","cls","headerCls","bodyCls","tools","href",{cache:"boolean",fit:"boolean",border:"boolean",noheader:"boolean"},{collapsible:"boolean",minimizable:"boolean",maximizable:"boolean"},{closable:"boolean",collapsed:"boolean",minimized:"boolean",maximized:"boolean",closed:"boolean"}]),{loadingMessage:(t.attr("loadingMessage")!=undefined?t.attr("loadingMessage"):undefined)});
};
$.fn.panel.defaults={id:null,title:null,iconCls:null,width:"auto",height:"auto",left:null,top:null,cls:null,headerCls:null,bodyCls:null,style:{},href:null,cache:true,fit:false,border:true,doSize:true,noheader:false,content:null,collapsible:false,minimizable:false,maximizable:false,closable:false,collapsed:false,minimized:false,maximized:false,closed:false,tools:null,href:null,loadingMessage:"Loading...",extractor:function(_67){
var _68=/<body[^>]*>((.|[\n\r])*)<\/body>/im;
var _69=_68.exec(_67);
if(_69){
return _69[1];
}else{
return _67;
}
},onLoad:function(){
},onBeforeOpen:function(){
},onOpen:function(){
},onBeforeClose:function(){
},onClose:function(){
},onBeforeDestroy:function(){
},onDestroy:function(){
},onResize:function(_6a,_6b){
},onMove:function(_6c,top){
},onMaximize:function(){
},onRestore:function(){
},onMinimize:function(){
},onBeforeCollapse:function(){
},onBeforeExpand:function(){
},onCollapse:function(){
},onExpand:function(){
}};
})(jQuery);


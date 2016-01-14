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
function _1(_2,_3){
_3=_3||{};
if(_3.onSubmit){
if(_3.onSubmit.call(_2)==false){
return;
}
}
var _4=$(_2);
if(_3.url){
_4.attr("action",_3.url);
}
var _5="easyui_frame_"+(new Date().getTime());
var _6=$("<iframe id="+_5+" name="+_5+"></iframe>").attr("src",window.ActiveXObject?"javascript:false":"about:blank").css({position:"absolute",top:-1000,left:-1000});
var t=_4.attr("target"),a=_4.attr("action");
_4.attr("target",_5);
try{
_6.appendTo("body");
_6.bind("load",cb);
_4[0].submit();
}
finally{
_4.attr("action",a);
t?_4.attr("target",t):_4.removeAttr("target");
}
var _7=10;
function cb(){
_6.unbind();
var _8=$("#"+_5).contents().find("body");
var _9=_8.html();
if(_9==""){
if(--_7){
setTimeout(cb,100);
return;
}
return;
}
var ta=_8.find(">textarea");
if(ta.length){
_9=ta.val();
}else{
var _a=_8.find(">pre");
if(_a.length){
_9=_a.html();
}
}
if(_3.success){
_3.success(_9);
}
setTimeout(function(){
_6.unbind();
_6.remove();
},100);
};
};
function _b(_c,_d){
if(!$.data(_c,"form")){
$.data(_c,"form",{options:$.extend({},$.fn.form.defaults)});
}
var _e=$.data(_c,"form").options;
if(typeof _d=="string"){
var _f={};
if(_e.onBeforeLoad.call(_c,_f)==false){
return;
}
$.ajax({url:_d,data:_f,dataType:"json",success:function(_10){
_11(_10);
},error:function(){
_e.onLoadError.apply(_c,arguments);
}});
}else{
_11(_d);
}
function _11(_12){
var _13=$(_c);
for(var _14 in _12){
var val=_12[_14];
var rr=_15(_14,val);
if(!rr.length){
var f=_13.find("input[numberboxName=\""+_14+"\"]");
if(f.length){
f.numberbox("setValue",val);
}else{
$("input[name=\""+_14+"\"]",_13).val(val);
$("textarea[name=\""+_14+"\"]",_13).val(val);
$("select[name=\""+_14+"\"]",_13).val(val);
}
}
_16(_14,val);
}
_e.onLoadSuccess.call(_c,_12);
_1f(_c);
};
function _15(_17,val){
var _18=$(_c);
var rr=$("input[name=\""+_17+"\"][type=radio], input[name=\""+_17+"\"][type=checkbox]",_18);
$.fn.prop?rr.prop("checked",false):rr.attr("checked",false);
rr.each(function(){
var f=$(this);
if(f.val()==String(val)){
$.fn.prop?f.prop("checked",true):f.attr("checked",true);
}
});
return rr;
};
function _16(_19,val){
var _1a=$(_c);
var cc=["combobox","combotree","combogrid","datetimebox","datebox","combo"];
var c=_1a.find("[comboName=\""+_19+"\"]");
if(c.length){
for(var i=0;i<cc.length;i++){
var _1b=cc[i];
if(c.hasClass(_1b+"-f")){
if(c[_1b]("options").multiple){
c[_1b]("setValues",val);
}else{
c[_1b]("setValue",val);
}
return;
}
}
}
};
};
function _1c(_1d){
$("input,select,textarea",_1d).each(function(){
var t=this.type,tag=this.tagName.toLowerCase();
if(t=="text"||t=="hidden"||t=="password"||tag=="textarea"){
this.value="";
}else{
if(t=="file"){
var _1e=$(this);
_1e.after(_1e.clone().val(""));
_1e.remove();
}else{
if(t=="checkbox"||t=="radio"){
this.checked=false;
}else{
if(tag=="select"){
this.selectedIndex=-1;
}
}
}
}
});
if($.fn.combo){
$(".combo-f",_1d).combo("clear");
}
if($.fn.combobox){
$(".combobox-f",_1d).combobox("clear");
}
if($.fn.combotree){
$(".combotree-f",_1d).combotree("clear");
}
if($.fn.combogrid){
$(".combogrid-f",_1d).combogrid("clear");
}
_1f(_1d);
};
function _20(_21){
var _22=$.data(_21,"form").options;
var _23=$(_21);
_23.unbind(".form").bind("submit.form",function(){
setTimeout(function(){
_1(_21,_22);
},0);
return false;
});
};
function _1f(_24){
if($.fn.validatebox){
var t=$(_24);
t.find(".validatebox-text:not(:disabled)").validatebox("validate");
var _25=t.find(".validatebox-invalid");
_25.filter(":not(:disabled):first").focus();
return _25.length==0;
}
return true;
};
$.fn.form=function(_26,_27){
if(typeof _26=="string"){
return $.fn.form.methods[_26](this,_27);
}
_26=_26||{};
return this.each(function(){
if(!$.data(this,"form")){
$.data(this,"form",{options:$.extend({},$.fn.form.defaults,_26)});
}
_20(this);
});
};
$.fn.form.methods={submit:function(jq,_28){
return jq.each(function(){
_1(this,$.extend({},$.fn.form.defaults,_28||{}));
});
},load:function(jq,_29){
return jq.each(function(){
_b(this,_29);
});
},clear:function(jq){
return jq.each(function(){
_1c(this);
});
},validate:function(jq){
return _1f(jq[0]);
}};
$.fn.form.defaults={url:null,onSubmit:function(){
return $(this).form("validate");
},success:function(_2a){
},onBeforeLoad:function(_2b){
},onLoadSuccess:function(_2c){
},onLoadError:function(){
}};
})(jQuery);


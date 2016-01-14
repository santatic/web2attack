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
var v=$("<input type=\"hidden\">").insertAfter(_2);
var _3=$(_2).attr("name");
if(_3){
v.attr("name",_3);
$(_2).removeAttr("name").attr("numberboxName",_3);
}
return v;
};
function _4(_5){
var _6=$.data(_5,"numberbox").options;
var fn=_6.onChange;
_6.onChange=function(){
};
_7(_5,_6.parser.call(_5,_6.value));
_6.onChange=fn;
};
function _8(_9){
return $.data(_9,"numberbox").field.val();
};
function _7(_a,_b){
var _c=$.data(_a,"numberbox");
var _d=_c.options;
var _e=_8(_a);
_b=_d.parser.call(_a,_b);
_d.value=_b;
_c.field.val(_b);
$(_a).val(_d.formatter.call(_a,_b));
if(_e!=_b){
_d.onChange.call(_a,_b,_e);
}
};
function _f(_10){
var _11=$.data(_10,"numberbox").options;
$(_10).unbind(".numberbox").bind("keypress.numberbox",function(e){
if(e.which==45){
if($(this).val().indexOf("-")==-1){
return true;
}else{
return false;
}
}
if(e.which==46){
if($(this).val().indexOf(".")==-1){
return true;
}else{
return false;
}
}else{
if((e.which>=48&&e.which<=57&&e.ctrlKey==false&&e.shiftKey==false)||e.which==0||e.which==8){
return true;
}else{
if(e.ctrlKey==true&&(e.which==99||e.which==118)){
return true;
}else{
return false;
}
}
}
}).bind("paste.numberbox",function(){
if(window.clipboardData){
var s=clipboardData.getData("text");
if(!/\D/.test(s)){
return true;
}else{
return false;
}
}else{
return false;
}
}).bind("dragenter.numberbox",function(){
return false;
}).bind("blur.numberbox",function(){
_7(_10,$(this).val());
$(this).val(_11.formatter.call(_10,_8(_10)));
}).bind("focus.numberbox",function(){
var vv=_8(_10);
if($(this).val()!=vv){
$(this).val(vv);
}
});
};
function _12(_13){
if($.fn.validatebox){
var _14=$.data(_13,"numberbox").options;
$(_13).validatebox(_14);
}
};
function _15(_16,_17){
var _18=$.data(_16,"numberbox").options;
if(_17){
_18.disabled=true;
$(_16).attr("disabled",true);
}else{
_18.disabled=false;
$(_16).removeAttr("disabled");
}
};
$.fn.numberbox=function(_19,_1a){
if(typeof _19=="string"){
var _1b=$.fn.numberbox.methods[_19];
if(_1b){
return _1b(this,_1a);
}else{
return this.validatebox(_19,_1a);
}
}
_19=_19||{};
return this.each(function(){
var _1c=$.data(this,"numberbox");
if(_1c){
$.extend(_1c.options,_19);
}else{
_1c=$.data(this,"numberbox",{options:$.extend({},$.fn.numberbox.defaults,$.fn.numberbox.parseOptions(this),_19),field:_1(this)});
$(this).removeAttr("disabled");
$(this).css({imeMode:"disabled"});
}
_15(this,_1c.options.disabled);
_f(this);
_12(this);
_4(this);
});
};
$.fn.numberbox.methods={options:function(jq){
return $.data(jq[0],"numberbox").options;
},destroy:function(jq){
return jq.each(function(){
$.data(this,"numberbox").field.remove();
$(this).validatebox("destroy");
$(this).remove();
});
},disable:function(jq){
return jq.each(function(){
_15(this,true);
});
},enable:function(jq){
return jq.each(function(){
_15(this,false);
});
},fix:function(jq){
return jq.each(function(){
_7(this,$(this).val());
});
},setValue:function(jq,_1d){
return jq.each(function(){
_7(this,_1d);
});
},getValue:function(jq){
return _8(jq[0]);
},clear:function(jq){
return jq.each(function(){
var _1e=$.data(this,"numberbox");
_1e.field.val("");
$(this).val("");
});
}};
$.fn.numberbox.parseOptions=function(_1f){
var t=$(_1f);
return $.extend({},$.fn.validatebox.parseOptions(_1f),$.parser.parseOptions(_1f,["decimalSeparator","groupSeparator","prefix","suffix",{min:"number",max:"number",precision:"number"}]),{disabled:(t.attr("disabled")?true:undefined),value:(t.val()||undefined)});
};
$.fn.numberbox.defaults=$.extend({},$.fn.validatebox.defaults,{disabled:false,value:"",min:null,max:null,precision:0,decimalSeparator:".",groupSeparator:"",prefix:"",suffix:"",formatter:function(_20){
if(!_20){
return _20;
}
_20=_20+"";
var _21=$(this).numberbox("options");
var s1=_20,s2="";
var _22=_20.indexOf(".");
if(_22>=0){
s1=_20.substring(0,_22);
s2=_20.substring(_22+1,_20.length);
}
if(_21.groupSeparator){
var p=/(\d+)(\d{3})/;
while(p.test(s1)){
s1=s1.replace(p,"$1"+_21.groupSeparator+"$2");
}
}
if(s2){
return _21.prefix+s1+_21.decimalSeparator+s2+_21.suffix;
}else{
return _21.prefix+s1+_21.suffix;
}
},parser:function(s){
s=s+"";
var _23=$(this).numberbox("options");
if(_23.groupSeparator){
s=s.replace(new RegExp("\\"+_23.groupSeparator,"g"),"");
}
if(_23.decimalSeparator){
s=s.replace(new RegExp("\\"+_23.decimalSeparator,"g"),".");
}
if(_23.prefix){
s=s.replace(new RegExp("\\"+$.trim(_23.prefix),"g"),"");
}
if(_23.suffix){
s=s.replace(new RegExp("\\"+$.trim(_23.suffix),"g"),"");
}
s=s.replace(/\s/g,"");
var val=parseFloat(s).toFixed(_23.precision);
if(isNaN(val)){
val="";
}else{
if(typeof (_23.min)=="number"&&val<_23.min){
val=_23.min.toFixed(_23.precision);
}else{
if(typeof (_23.max)=="number"&&val>_23.max){
val=_23.max.toFixed(_23.precision);
}
}
}
return val;
},onChange:function(_24,_25){
}});
})(jQuery);


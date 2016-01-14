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
var _3=$("<span class=\"spinner\">"+"<span class=\"spinner-arrow\">"+"<span class=\"spinner-arrow-up\"></span>"+"<span class=\"spinner-arrow-down\"></span>"+"</span>"+"</span>").insertAfter(_2);
$(_2).addClass("spinner-text").prependTo(_3);
return _3;
};
function _4(_5,_6){
var _7=$.data(_5,"spinner").options;
var _8=$.data(_5,"spinner").spinner;
if(_6){
_7.width=_6;
}
var _9=$("<div style=\"display:none\"></div>").insertBefore(_8);
_8.appendTo("body");
if(isNaN(_7.width)){
_7.width=$(_5).outerWidth();
}
_8._outerWidth(_7.width);
$(_5)._outerWidth(_8.width()-_8.find(".spinner-arrow").outerWidth());
_8.insertAfter(_9);
_9.remove();
};
function _a(_b){
var _c=$.data(_b,"spinner").options;
var _d=$.data(_b,"spinner").spinner;
_d.find(".spinner-arrow-up,.spinner-arrow-down").unbind(".spinner");
if(!_c.disabled){
_d.find(".spinner-arrow-up").bind("mouseenter.spinner",function(){
$(this).addClass("spinner-arrow-hover");
}).bind("mouseleave.spinner",function(){
$(this).removeClass("spinner-arrow-hover");
}).bind("click.spinner",function(){
_c.spin.call(_b,false);
_c.onSpinUp.call(_b);
$(_b).validatebox("validate");
});
_d.find(".spinner-arrow-down").bind("mouseenter.spinner",function(){
$(this).addClass("spinner-arrow-hover");
}).bind("mouseleave.spinner",function(){
$(this).removeClass("spinner-arrow-hover");
}).bind("click.spinner",function(){
_c.spin.call(_b,true);
_c.onSpinDown.call(_b);
$(_b).validatebox("validate");
});
}
};
function _e(_f,_10){
var _11=$.data(_f,"spinner").options;
if(_10){
_11.disabled=true;
$(_f).attr("disabled",true);
}else{
_11.disabled=false;
$(_f).removeAttr("disabled");
}
};
$.fn.spinner=function(_12,_13){
if(typeof _12=="string"){
var _14=$.fn.spinner.methods[_12];
if(_14){
return _14(this,_13);
}else{
return this.validatebox(_12,_13);
}
}
_12=_12||{};
return this.each(function(){
var _15=$.data(this,"spinner");
if(_15){
$.extend(_15.options,_12);
}else{
_15=$.data(this,"spinner",{options:$.extend({},$.fn.spinner.defaults,$.fn.spinner.parseOptions(this),_12),spinner:_1(this)});
$(this).removeAttr("disabled");
}
$(this).val(_15.options.value);
$(this).attr("readonly",!_15.options.editable);
_e(this,_15.options.disabled);
_4(this);
$(this).validatebox(_15.options);
_a(this);
});
};
$.fn.spinner.methods={options:function(jq){
var _16=$.data(jq[0],"spinner").options;
return $.extend(_16,{value:jq.val()});
},destroy:function(jq){
return jq.each(function(){
var _17=$.data(this,"spinner").spinner;
$(this).validatebox("destroy");
_17.remove();
});
},resize:function(jq,_18){
return jq.each(function(){
_4(this,_18);
});
},enable:function(jq){
return jq.each(function(){
_e(this,false);
_a(this);
});
},disable:function(jq){
return jq.each(function(){
_e(this,true);
_a(this);
});
},getValue:function(jq){
return jq.val();
},setValue:function(jq,_19){
return jq.each(function(){
var _1a=$.data(this,"spinner").options;
_1a.value=_19;
$(this).val(_19);
});
},clear:function(jq){
return jq.each(function(){
var _1b=$.data(this,"spinner").options;
_1b.value="";
$(this).val("");
});
}};
$.fn.spinner.parseOptions=function(_1c){
var t=$(_1c);
return $.extend({},$.fn.validatebox.parseOptions(_1c),$.parser.parseOptions(_1c,["width","min","max",{increment:"number",editable:"boolean"}]),{value:(t.val()||undefined),disabled:(t.attr("disabled")?true:undefined)});
};
$.fn.spinner.defaults=$.extend({},$.fn.validatebox.defaults,{width:"auto",value:"",min:null,max:null,increment:1,editable:true,disabled:false,spin:function(_1d){
},onSpinUp:function(){
},onSpinDown:function(){
}});
})(jQuery);


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
$(_2).addClass("validatebox-text");
};
function _3(_4){
var _5=$.data(_4,"validatebox");
_5.validating=false;
var _6=_5.tip;
if(_6){
_6.remove();
}
$(_4).unbind();
$(_4).remove();
};
function _7(_8){
var _9=$(_8);
var _a=$.data(_8,"validatebox");
_9.unbind(".validatebox").bind("focus.validatebox",function(){
_a.validating=true;
_a.value=undefined;
(function(){
if(_a.validating){
if(_a.value!=_9.val()){
_a.value=_9.val();
_13(_8);
}else{
_10(_8);
}
setTimeout(arguments.callee,200);
}
})();
}).bind("blur.validatebox",function(){
_a.validating=false;
_b(_8);
}).bind("mouseenter.validatebox",function(){
if(_9.hasClass("validatebox-invalid")){
_c(_8);
}
}).bind("mouseleave.validatebox",function(){
if(!_a.validating){
_b(_8);
}
});
};
function _c(_d){
var _e=$.data(_d,"validatebox").message;
var _f=$.data(_d,"validatebox").tip;
if(!_f){
_f=$("<div class=\"validatebox-tip\">"+"<span class=\"validatebox-tip-content\">"+"</span>"+"<span class=\"validatebox-tip-pointer\">"+"</span>"+"</div>").appendTo("body");
$.data(_d,"validatebox").tip=_f;
}
_f.find(".validatebox-tip-content").html(_e);
_10(_d);
};
function _10(_11){
var box=$(_11);
var tip=$.data(_11,"validatebox").tip;
if(tip){
tip.css({display:"block",left:box.offset().left+box.outerWidth(),top:box.offset().top});
}
};
function _b(_12){
var tip=$.data(_12,"validatebox").tip;
if(tip){
tip.remove();
$.data(_12,"validatebox").tip=null;
}
};
function _13(_14){
var _15=$.data(_14,"validatebox");
var _16=$.data(_14,"validatebox").options;
var tip=$.data(_14,"validatebox").tip;
var box=$(_14);
var _17=box.val();
function _18(msg){
$.data(_14,"validatebox").message=msg;
};
if(_16.required){
if(_17==""){
box.addClass("validatebox-invalid");
_18(_16.missingMessage);
if(_15.validating){
_c(_14);
}
return false;
}
}
if(_16.validType){
var _19=/([a-zA-Z_]+)(.*)/.exec(_16.validType);
var _1a=_16.rules[_19[1]];
if(_17&&_1a){
var _1b=eval(_19[2]);
if(!_1a["validator"](_17,_1b)){
box.addClass("validatebox-invalid");
var _1c=_1a["message"];
if(_1b){
for(var i=0;i<_1b.length;i++){
_1c=_1c.replace(new RegExp("\\{"+i+"\\}","g"),_1b[i]);
}
}
_18(_16.invalidMessage||_1c);
if(_15.validating){
_c(_14);
}
return false;
}
}
}
box.removeClass("validatebox-invalid");
_b(_14);
return true;
};
$.fn.validatebox=function(_1d,_1e){
if(typeof _1d=="string"){
return $.fn.validatebox.methods[_1d](this,_1e);
}
_1d=_1d||{};
return this.each(function(){
var _1f=$.data(this,"validatebox");
if(_1f){
$.extend(_1f.options,_1d);
}else{
_1(this);
$.data(this,"validatebox",{options:$.extend({},$.fn.validatebox.defaults,$.fn.validatebox.parseOptions(this),_1d)});
}
_7(this);
});
};
$.fn.validatebox.methods={destroy:function(jq){
return jq.each(function(){
_3(this);
});
},validate:function(jq){
return jq.each(function(){
_13(this);
});
},isValid:function(jq){
return _13(jq[0]);
}};
$.fn.validatebox.parseOptions=function(_20){
var t=$(_20);
return $.extend({},$.parser.parseOptions(_20,["validType","missingMessage","invalidMessage"]),{required:(t.attr("required")?true:undefined)});
};
$.fn.validatebox.defaults={required:false,validType:null,missingMessage:"This field is required.",invalidMessage:null,rules:{email:{validator:function(_21){
return /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i.test(_21);
},message:"Please enter a valid email address."},url:{validator:function(_22){
return /^(https?|ftp):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i.test(_22);
},message:"Please enter a valid URL."},length:{validator:function(_23,_24){
var len=$.trim(_23).length;
return len>=_24[0]&&len<=_24[1];
},message:"Please enter a value between {0} and {1}."},remote:{validator:function(_25,_26){
var _27={};
_27[_26[1]]=_25;
var _28=$.ajax({url:_26[0],dataType:"json",data:_27,async:false,cache:false,type:"post"}).responseText;
return _28=="true";
},message:"Please fix this field."}}};
})(jQuery);


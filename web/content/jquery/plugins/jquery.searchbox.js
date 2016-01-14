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
$(_2).hide();
var _3=$("<span class=\"searchbox\"></span>").insertAfter(_2);
var _4=$("<input type=\"text\" class=\"searchbox-text\">").appendTo(_3);
$("<span><span class=\"searchbox-button\"></span></span>").appendTo(_3);
var _5=$(_2).attr("name");
if(_5){
_4.attr("name",_5);
$(_2).removeAttr("name").attr("searchboxName",_5);
}
return _3;
};
function _6(_7,_8){
var _9=$.data(_7,"searchbox").options;
var sb=$.data(_7,"searchbox").searchbox;
if(_8){
_9.width=_8;
}
sb.appendTo("body");
if(isNaN(_9.width)){
_9.width=sb.outerWidth();
}
sb._outerWidth(_9.width);
sb.find("input.searchbox-text")._outerWidth(sb.width()-sb.find("a.searchbox-menu").outerWidth()-sb.find("span.searchbox-button").outerWidth());
sb.insertAfter(_7);
};
function _a(_b){
var _c=$.data(_b,"searchbox");
var _d=_c.options;
if(_d.menu){
_c.menu=$(_d.menu).menu({onClick:function(_e){
_f(_e);
}});
var _10=_c.menu.children("div.menu-item:first");
_c.menu.children("div.menu-item").each(function(){
var _11=$.extend({},$.parser.parseOptions(this),{selected:($(this).attr("selected")?true:undefined)});
if(_11.selected){
_10=$(this);
return false;
}
});
_10.triggerHandler("click");
}else{
_c.searchbox.find("a.searchbox-menu").remove();
_c.menu=null;
}
function _f(_12){
_c.searchbox.find("a.searchbox-menu").remove();
var mb=$("<a class=\"searchbox-menu\" href=\"javascript:void(0)\"></a>").html(_12.text);
mb.prependTo(_c.searchbox).menubutton({menu:_c.menu,iconCls:_12.iconCls});
_c.searchbox.find("input.searchbox-text").attr("name",$(_12.target).attr("name")||_12.text);
_6(_b);
};
};
function _13(_14){
var _15=$.data(_14,"searchbox");
var _16=_15.options;
var _17=_15.searchbox.find("input.searchbox-text");
var _18=_15.searchbox.find(".searchbox-button");
_17.unbind(".searchbox").bind("blur.searchbox",function(e){
_16.value=$(this).val();
if(_16.value==""){
$(this).val(_16.prompt);
$(this).addClass("searchbox-prompt");
}else{
$(this).removeClass("searchbox-prompt");
}
}).bind("focus.searchbox",function(e){
if($(this).val()!=_16.value){
$(this).val(_16.value);
}
$(this).removeClass("searchbox-prompt");
}).bind("keydown.searchbox",function(e){
if(e.keyCode==13){
e.preventDefault();
var _19=$.fn.prop?_17.prop("name"):_17.attr("name");
_16.value=$(this).val();
_16.searcher.call(_14,_16.value,_19);
return false;
}
});
_18.unbind(".searchbox").bind("click.searchbox",function(){
var _1a=$.fn.prop?_17.prop("name"):_17.attr("name");
_16.searcher.call(_14,_16.value,_1a);
}).bind("mouseenter.searchbox",function(){
$(this).addClass("searchbox-button-hover");
}).bind("mouseleave.searchbox",function(){
$(this).removeClass("searchbox-button-hover");
});
};
function _1b(_1c){
var _1d=$.data(_1c,"searchbox");
var _1e=_1d.options;
var _1f=_1d.searchbox.find("input.searchbox-text");
if(_1e.value==""){
_1f.val(_1e.prompt);
_1f.addClass("searchbox-prompt");
}else{
_1f.val(_1e.value);
_1f.removeClass("searchbox-prompt");
}
};
$.fn.searchbox=function(_20,_21){
if(typeof _20=="string"){
return $.fn.searchbox.methods[_20](this,_21);
}
_20=_20||{};
return this.each(function(){
var _22=$.data(this,"searchbox");
if(_22){
$.extend(_22.options,_20);
}else{
_22=$.data(this,"searchbox",{options:$.extend({},$.fn.searchbox.defaults,$.fn.searchbox.parseOptions(this),_20),searchbox:_1(this)});
}
_a(this);
_1b(this);
_13(this);
_6(this);
});
};
$.fn.searchbox.methods={options:function(jq){
return $.data(jq[0],"searchbox").options;
},menu:function(jq){
return $.data(jq[0],"searchbox").menu;
},textbox:function(jq){
return $.data(jq[0],"searchbox").searchbox.find("input.searchbox-text");
},getValue:function(jq){
return $.data(jq[0],"searchbox").options.value;
},setValue:function(jq,_23){
return jq.each(function(){
$(this).searchbox("options").value=_23;
$(this).searchbox("textbox").val(_23);
$(this).searchbox("textbox").blur();
});
},getName:function(jq){
return $.data(jq[0],"searchbox").searchbox.find("input.searchbox-text").attr("name");
},selectName:function(jq,_24){
return jq.each(function(){
var _25=$.data(this,"searchbox").menu;
if(_25){
_25.children("div.menu-item[name=\""+_24+"\"]").triggerHandler("click");
}
});
},destroy:function(jq){
return jq.each(function(){
var _26=$(this).searchbox("menu");
if(_26){
_26.menu("destroy");
}
$.data(this,"searchbox").searchbox.remove();
$(this).remove();
});
},resize:function(jq,_27){
return jq.each(function(){
_6(this,_27);
});
}};
$.fn.searchbox.parseOptions=function(_28){
var t=$(_28);
return $.extend({},$.parser.parseOptions(_28,["width","prompt","menu"]),{value:t.val(),searcher:(t.attr("searcher")?eval(t.attr("searcher")):undefined)});
};
$.fn.searchbox.defaults={width:"auto",prompt:"",value:"",menu:null,searcher:function(_29,_2a){
}};
})(jQuery);


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
$(_2).appendTo("body");
$(_2).addClass("menu-top");
var _3=[];
_4($(_2));
var _5=null;
for(var i=0;i<_3.length;i++){
var _6=_3[i];
_7(_6);
_6.children("div.menu-item").each(function(){
_10(_2,$(this));
});
_6.bind("mouseenter",function(){
if(_5){
clearTimeout(_5);
_5=null;
}
}).bind("mouseleave",function(){
_5=setTimeout(function(){
_19(_2);
},100);
});
}
function _4(_8){
_3.push(_8);
_8.find(">div").each(function(){
var _9=$(this);
var _a=_9.find(">div");
if(_a.length){
_a.insertAfter(_2);
_9[0].submenu=_a;
_4(_a);
}
});
};
function _7(_b){
_b.addClass("menu").find(">div").each(function(){
var _c=$(this);
if(_c.hasClass("menu-sep")){
_c.html("&nbsp;");
}else{
var _d=$.extend({},$.parser.parseOptions(this,["name","iconCls","href"]),{disabled:(_c.attr("disabled")?true:undefined)});
_c.attr("name",_d.name||"").attr("href",_d.href||"");
var _e=_c.addClass("menu-item").html();
_c.empty().append($("<div class=\"menu-text\"></div>").html(_e));
if(_d.iconCls){
$("<div class=\"menu-icon\"></div>").addClass(_d.iconCls).appendTo(_c);
}
if(_d.disabled){
_f(_2,_c[0],true);
}
if(_c[0].submenu){
$("<div class=\"menu-rightarrow\"></div>").appendTo(_c);
}
_c._outerHeight(22);
}
});
_b.hide();
};
};
function _10(_11,_12){
_12.unbind(".menu");
_12.bind("mousedown.menu",function(){
return false;
}).bind("click.menu",function(){
if($(this).hasClass("menu-item-disabled")){
return;
}
if(!this.submenu){
_19(_11);
var _13=$(this).attr("href");
if(_13){
location.href=_13;
}
}
var _14=$(_11).menu("getItem",this);
$.data(_11,"menu").options.onClick.call(_11,_14);
}).bind("mouseenter.menu",function(e){
_12.siblings().each(function(){
if(this.submenu){
_18(this.submenu);
}
$(this).removeClass("menu-active");
});
_12.addClass("menu-active");
if($(this).hasClass("menu-item-disabled")){
_12.addClass("menu-active-disabled");
return;
}
var _15=_12[0].submenu;
if(_15){
var _16=_12.offset().left+_12.outerWidth()-2;
if(_16+_15.outerWidth()+5>$(window)._outerWidth()+$(document).scrollLeft()){
_16=_12.offset().left-_15.outerWidth()+2;
}
var top=_12.offset().top-3;
if(top+_15.outerHeight()>$(window)._outerHeight()+$(document).scrollTop()){
top=$(window)._outerHeight()+$(document).scrollTop()-_15.outerHeight()-5;
}
_1f(_15,{left:_16,top:top});
}
}).bind("mouseleave.menu",function(e){
_12.removeClass("menu-active menu-active-disabled");
var _17=_12[0].submenu;
if(_17){
if(e.pageX>=parseInt(_17.css("left"))){
_12.addClass("menu-active");
}else{
_18(_17);
}
}else{
_12.removeClass("menu-active");
}
});
};
function _19(_1a){
var _1b=$.data(_1a,"menu").options;
_18($(_1a));
$(document).unbind(".menu");
_1b.onHide.call(_1a);
return false;
};
function _1c(_1d,pos){
var _1e=$.data(_1d,"menu").options;
if(pos){
_1e.left=pos.left;
_1e.top=pos.top;
if(_1e.left+$(_1d).outerWidth()>$(window)._outerWidth()+$(document).scrollLeft()){
_1e.left=$(window)._outerWidth()+$(document).scrollLeft()-$(_1d).outerWidth()-5;
}
if(_1e.top+$(_1d).outerHeight()>$(window)._outerHeight()+$(document).scrollTop()){
_1e.top-=$(_1d).outerHeight();
}
}
_1f($(_1d),{left:_1e.left,top:_1e.top},function(){
$(document).unbind(".menu").bind("mousedown.menu",function(){
_19(_1d);
$(document).unbind(".menu");
return false;
});
_1e.onShow.call(_1d);
});
};
function _1f(_20,pos,_21){
if(!_20){
return;
}
if(pos){
_20.css(pos);
}
_20.show(0,function(){
if(!_20[0].shadow){
_20[0].shadow=$("<div class=\"menu-shadow\"></div>").insertAfter(_20);
}
_20[0].shadow.css({display:"block",zIndex:$.fn.menu.defaults.zIndex++,left:_20.css("left"),top:_20.css("top"),width:_20.outerWidth(),height:_20.outerHeight()});
_20.css("z-index",$.fn.menu.defaults.zIndex++);
if(_21){
_21();
}
});
};
function _18(_22){
if(!_22){
return;
}
_23(_22);
_22.find("div.menu-item").each(function(){
if(this.submenu){
_18(this.submenu);
}
$(this).removeClass("menu-active");
});
function _23(m){
m.stop(true,true);
if(m[0].shadow){
m[0].shadow.hide();
}
m.hide();
};
};
function _24(_25,_26){
var _27=null;
var tmp=$("<div></div>");
function _28(_29){
_29.children("div.menu-item").each(function(){
var _2a=$(_25).menu("getItem",this);
var s=tmp.empty().html(_2a.text).text();
if(_26==$.trim(s)){
_27=_2a;
}else{
if(this.submenu&&!_27){
_28(this.submenu);
}
}
});
};
_28($(_25));
tmp.remove();
return _27;
};
function _f(_2b,_2c,_2d){
var t=$(_2c);
if(_2d){
t.addClass("menu-item-disabled");
if(_2c.onclick){
_2c.onclick1=_2c.onclick;
_2c.onclick=null;
}
}else{
t.removeClass("menu-item-disabled");
if(_2c.onclick1){
_2c.onclick=_2c.onclick1;
_2c.onclick1=null;
}
}
};
function _2e(_2f,_30){
var _31=$(_2f);
if(_30.parent){
_31=_30.parent.submenu;
}
var _32=$("<div class=\"menu-item\"></div>").appendTo(_31);
$("<div class=\"menu-text\"></div>").html(_30.text).appendTo(_32);
if(_30.iconCls){
$("<div class=\"menu-icon\"></div>").addClass(_30.iconCls).appendTo(_32);
}
if(_30.id){
_32.attr("id",_30.id);
}
if(_30.href){
_32.attr("href",_30.href);
}
if(_30.name){
_32.attr("name",_30.name);
}
if(_30.onclick){
if(typeof _30.onclick=="string"){
_32.attr("onclick",_30.onclick);
}else{
_32[0].onclick=eval(_30.onclick);
}
}
if(_30.handler){
_32[0].onclick=eval(_30.handler);
}
_10(_2f,_32);
if(_30.disabled){
_f(_2f,_32[0],true);
}
};
function _33(_34,_35){
function _36(el){
if(el.submenu){
el.submenu.children("div.menu-item").each(function(){
_36(this);
});
var _37=el.submenu[0].shadow;
if(_37){
_37.remove();
}
el.submenu.remove();
}
$(el).remove();
};
_36(_35);
};
function _38(_39){
$(_39).children("div.menu-item").each(function(){
_33(_39,this);
});
if(_39.shadow){
_39.shadow.remove();
}
$(_39).remove();
};
$.fn.menu=function(_3a,_3b){
if(typeof _3a=="string"){
return $.fn.menu.methods[_3a](this,_3b);
}
_3a=_3a||{};
return this.each(function(){
var _3c=$.data(this,"menu");
if(_3c){
$.extend(_3c.options,_3a);
}else{
_3c=$.data(this,"menu",{options:$.extend({},$.fn.menu.defaults,$.fn.menu.parseOptions(this),_3a)});
_1(this);
}
$(this).css({left:_3c.options.left,top:_3c.options.top});
});
};
$.fn.menu.methods={show:function(jq,pos){
return jq.each(function(){
_1c(this,pos);
});
},hide:function(jq){
return jq.each(function(){
_19(this);
});
},destroy:function(jq){
return jq.each(function(){
_38(this);
});
},setText:function(jq,_3d){
return jq.each(function(){
$(_3d.target).children("div.menu-text").html(_3d.text);
});
},setIcon:function(jq,_3e){
return jq.each(function(){
var _3f=$(this).menu("getItem",_3e.target);
if(_3f.iconCls){
$(_3f.target).children("div.menu-icon").removeClass(_3f.iconCls).addClass(_3e.iconCls);
}else{
$("<div class=\"menu-icon\"></div>").addClass(_3e.iconCls).appendTo(_3e.target);
}
});
},getItem:function(jq,_40){
var t=$(_40);
var _41={target:_40,id:t.attr("id"),text:$.trim(t.children("div.menu-text").html()),disabled:t.hasClass("menu-item-disabled"),href:t.attr("href"),name:t.attr("name"),onclick:_40.onclick};
var _42=t.children("div.menu-icon");
if(_42.length){
var cc=[];
var aa=_42.attr("class").split(" ");
for(var i=0;i<aa.length;i++){
if(aa[i]!="menu-icon"){
cc.push(aa[i]);
}
}
_41.iconCls=cc.join(" ");
}
return _41;
},findItem:function(jq,_43){
return _24(jq[0],_43);
},appendItem:function(jq,_44){
return jq.each(function(){
_2e(this,_44);
});
},removeItem:function(jq,_45){
return jq.each(function(){
_33(this,_45);
});
},enableItem:function(jq,_46){
return jq.each(function(){
_f(this,_46,false);
});
},disableItem:function(jq,_47){
return jq.each(function(){
_f(this,_47,true);
});
}};
$.fn.menu.parseOptions=function(_48){
return $.extend({},$.parser.parseOptions(_48,["left","top"]));
};
$.fn.menu.defaults={zIndex:110000,left:0,top:0,onShow:function(){
},onHide:function(){
},onClick:function(_49){
}};
})(jQuery);


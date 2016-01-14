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
var _3=$(_2).children("div.tabs-header");
var _4=0;
$("ul.tabs li",_3).each(function(){
_4+=$(this).outerWidth(true);
});
var _5=_3.children("div.tabs-wrap").width();
var _6=parseInt(_3.find("ul.tabs").css("padding-left"));
return _4-_5+_6;
};
function _7(_8){
var _9=$.data(_8,"tabs").options;
var _a=$(_8).children("div.tabs-header");
var _b=_a.children("div.tabs-tool");
var _c=_a.children("div.tabs-scroller-left");
var _d=_a.children("div.tabs-scroller-right");
var _e=_a.children("div.tabs-wrap");
_b._outerHeight(_a.outerHeight()-(_9.plain?2:0));
var _f=0;
$("ul.tabs li",_a).each(function(){
_f+=$(this).outerWidth(true);
});
var _10=_a.width()-_b._outerWidth();
if(_f>_10){
_c.show();
_d.show();
_b.css("right",_d.outerWidth());
_e.css({marginLeft:_c.outerWidth(),marginRight:_d.outerWidth()+_b._outerWidth(),left:0,width:_10-_c.outerWidth()-_d.outerWidth()});
}else{
_c.hide();
_d.hide();
_b.css("right",0);
_e.css({marginLeft:0,marginRight:_b._outerWidth(),left:0,width:_10});
_e.scrollLeft(0);
}
};
function _11(_12){
var _13=$.data(_12,"tabs").options;
var _14=$(_12).children("div.tabs-header");
if(_13.tools){
if(typeof _13.tools=="string"){
$(_13.tools).addClass("tabs-tool").appendTo(_14);
$(_13.tools).show();
}else{
_14.children("div.tabs-tool").remove();
var _15=$("<div class=\"tabs-tool\"></div>").appendTo(_14);
for(var i=0;i<_13.tools.length;i++){
var _16=$("<a href=\"javascript:void(0);\"></a>").appendTo(_15);
_16[0].onclick=eval(_13.tools[i].handler||function(){
});
_16.linkbutton($.extend({},_13.tools[i],{plain:true}));
}
}
}else{
_14.children("div.tabs-tool").remove();
}
};
function _17(_18){
var _19=$.data(_18,"tabs").options;
var cc=$(_18);
if(_19.fit==true){
var p=cc.parent();
p.addClass("panel-noscroll");
if(p[0].tagName=="BODY"){
$("html").addClass("panel-fit");
}
_19.width=p.width();
_19.height=p.height();
}
cc.width(_19.width).height(_19.height);
var _1a=$(_18).children("div.tabs-header");
_1a._outerWidth(_19.width);
_7(_18);
var _1b=$(_18).children("div.tabs-panels");
var _1c=_19.height;
if(!isNaN(_1c)){
_1b._outerHeight(_1c-_1a.outerHeight());
}else{
_1b.height("auto");
}
var _1d=_19.width;
if(!isNaN(_1d)){
_1b._outerWidth(_1d);
}else{
_1b.width("auto");
}
};
function _1e(_1f){
var _20=$.data(_1f,"tabs").options;
var tab=_21(_1f);
if(tab){
var _22=$(_1f).children("div.tabs-panels");
var _23=_20.width=="auto"?"auto":_22.width();
var _24=_20.height=="auto"?"auto":_22.height();
tab.panel("resize",{width:_23,height:_24});
}
};
function _25(_26){
var _27=$.data(_26,"tabs").tabs;
var cc=$(_26);
cc.addClass("tabs-container");
cc.wrapInner("<div class=\"tabs-panels\"/>");
$("<div class=\"tabs-header\">"+"<div class=\"tabs-scroller-left\"></div>"+"<div class=\"tabs-scroller-right\"></div>"+"<div class=\"tabs-wrap\">"+"<ul class=\"tabs\"></ul>"+"</div>"+"</div>").prependTo(_26);
cc.children("div.tabs-panels").children("div").each(function(i){
var _28=$.extend({},$.parser.parseOptions(this),{selected:($(this).attr("selected")?true:undefined)});
var pp=$(this);
_27.push(pp);
_32(_26,pp,_28);
});
cc.children("div.tabs-header").find(".tabs-scroller-left, .tabs-scroller-right").hover(function(){
$(this).addClass("tabs-scroller-over");
},function(){
$(this).removeClass("tabs-scroller-over");
});
cc.bind("_resize",function(e,_29){
var _2a=$.data(_26,"tabs").options;
if(_2a.fit==true||_29){
_17(_26);
_1e(_26);
}
return false;
});
};
function _2b(_2c){
var _2d=$.data(_2c,"tabs").options;
var _2e=$(_2c).children("div.tabs-header");
var _2f=$(_2c).children("div.tabs-panels");
if(_2d.plain==true){
_2e.addClass("tabs-header-plain");
}else{
_2e.removeClass("tabs-header-plain");
}
if(_2d.border==true){
_2e.removeClass("tabs-header-noborder");
_2f.removeClass("tabs-panels-noborder");
}else{
_2e.addClass("tabs-header-noborder");
_2f.addClass("tabs-panels-noborder");
}
$(".tabs-scroller-left",_2e).unbind(".tabs").bind("click.tabs",function(){
var _30=$(".tabs-wrap",_2e);
var pos=_30.scrollLeft()-_2d.scrollIncrement;
_30.animate({scrollLeft:pos},_2d.scrollDuration);
});
$(".tabs-scroller-right",_2e).unbind(".tabs").bind("click.tabs",function(){
var _31=$(".tabs-wrap",_2e);
var pos=Math.min(_31.scrollLeft()+_2d.scrollIncrement,_1(_2c));
_31.animate({scrollLeft:pos},_2d.scrollDuration);
});
};
function _32(_33,pp,_34){
var _35=$.data(_33,"tabs");
_34=_34||{};
pp.panel($.extend({},_34,{border:false,noheader:true,closed:true,doSize:false,iconCls:(_34.icon?_34.icon:undefined),onLoad:function(){
if(_34.onLoad){
_34.onLoad.call(this,arguments);
}
_35.options.onLoad.call(_33,$(this));
}}));
var _36=pp.panel("options");
var _37=$(_33).children("div.tabs-header").find("ul.tabs");
_36.tab=$("<li></li>").appendTo(_37);
_36.tab.append("<a href=\"javascript:void(0)\" class=\"tabs-inner\">"+"<span class=\"tabs-title\"></span>"+"<span class=\"tabs-icon\"></span>"+"</a>");
_36.tab.unbind(".tabs").bind("click.tabs",{p:pp},function(e){
if($(this).hasClass("tabs-disabled")){
return;
}
_3f(_33,_38(_33,e.data.p));
}).bind("contextmenu.tabs",{p:pp},function(e){
if($(this).hasClass("tabs-disabled")){
return;
}
_35.options.onContextMenu.call(_33,e,$(this).find("span.tabs-title").html(),_38(_33,e.data.p));
});
_39(_33,{tab:pp,options:_36});
};
function _3a(_3b,_3c){
var _3d=$.data(_3b,"tabs").options;
var _3e=$.data(_3b,"tabs").tabs;
if(_3c.selected==undefined){
_3c.selected=true;
}
var pp=$("<div></div>").appendTo($(_3b).children("div.tabs-panels"));
_3e.push(pp);
_32(_3b,pp,_3c);
_3d.onAdd.call(_3b,_3c.title,_3e.length-1);
_7(_3b);
if(_3c.selected){
_3f(_3b,_3e.length-1);
}
};
function _39(_40,_41){
var _42=$.data(_40,"tabs").selectHis;
var pp=_41.tab;
var _43=pp.panel("options").title;
pp.panel($.extend({},_41.options,{iconCls:(_41.options.icon?_41.options.icon:undefined)}));
var _44=pp.panel("options");
var tab=_44.tab;
var _45=tab.find("span.tabs-title");
var _46=tab.find("span.tabs-icon");
_45.html(_44.title);
_46.attr("class","tabs-icon");
tab.find("a.tabs-close").remove();
if(_44.closable){
_45.addClass("tabs-closable");
var _47=$("<a href=\"javascript:void(0)\" class=\"tabs-close\"></a>").appendTo(tab);
_47.bind("click.tabs",{p:pp},function(e){
if($(this).parent().hasClass("tabs-disabled")){
return;
}
_49(_40,_38(_40,e.data.p));
return false;
});
}else{
_45.removeClass("tabs-closable");
}
if(_44.iconCls){
_45.addClass("tabs-with-icon");
_46.addClass(_44.iconCls);
}else{
_45.removeClass("tabs-with-icon");
}
if(_43!=_44.title){
for(var i=0;i<_42.length;i++){
if(_42[i]==_43){
_42[i]=_44.title;
}
}
}
tab.find("span.tabs-p-tool").remove();
if(_44.tools){
var _48=$("<span class=\"tabs-p-tool\"></span>").insertAfter(tab.find("a.tabs-inner"));
if(typeof _44.tools=="string"){
$(_44.tools).children().appendTo(_48);
}else{
for(var i=0;i<_44.tools.length;i++){
var t=$("<a href=\"javascript:void(0)\"></a>").appendTo(_48);
t.addClass(_44.tools[i].iconCls);
if(_44.tools[i].handler){
t.bind("click",{handler:_44.tools[i].handler},function(e){
if($(this).parents("li").hasClass("tabs-disabled")){
return;
}
e.data.handler.call(this);
});
}
}
}
var pr=_48.children().length*12;
if(_44.closable){
pr+=8;
}else{
pr-=3;
_48.css("right","5px");
}
_45.css("padding-right",pr+"px");
}
_7(_40);
$.data(_40,"tabs").options.onUpdate.call(_40,_44.title,_38(_40,pp));
};
function _49(_4a,_4b){
var _4c=$.data(_4a,"tabs").options;
var _4d=$.data(_4a,"tabs").tabs;
var _4e=$.data(_4a,"tabs").selectHis;
if(!_4f(_4a,_4b)){
return;
}
var tab=_50(_4a,_4b);
var _51=tab.panel("options").title;
var _52=_38(_4a,tab);
if(_4c.onBeforeClose.call(_4a,_51,_52)==false){
return;
}
var tab=_50(_4a,_4b,true);
tab.panel("options").tab.remove();
tab.panel("destroy");
_4c.onClose.call(_4a,_51,_52);
_7(_4a);
for(var i=0;i<_4e.length;i++){
if(_4e[i]==_51){
_4e.splice(i,1);
i--;
}
}
var _53=_4e.pop();
if(_53){
_3f(_4a,_53);
}else{
if(_4d.length){
_3f(_4a,0);
}
}
};
function _50(_54,_55,_56){
var _57=$.data(_54,"tabs").tabs;
if(typeof _55=="number"){
if(_55<0||_55>=_57.length){
return null;
}else{
var tab=_57[_55];
if(_56){
_57.splice(_55,1);
}
return tab;
}
}
for(var i=0;i<_57.length;i++){
var tab=_57[i];
if(tab.panel("options").title==_55){
if(_56){
_57.splice(i,1);
}
return tab;
}
}
return null;
};
function _38(_58,tab){
var _59=$.data(_58,"tabs").tabs;
for(var i=0;i<_59.length;i++){
if(_59[i][0]==$(tab)[0]){
return i;
}
}
return -1;
};
function _21(_5a){
var _5b=$.data(_5a,"tabs").tabs;
for(var i=0;i<_5b.length;i++){
var tab=_5b[i];
if(tab.panel("options").closed==false){
return tab;
}
}
return null;
};
function _5c(_5d){
var _5e=$.data(_5d,"tabs").tabs;
for(var i=0;i<_5e.length;i++){
if(_5e[i].panel("options").selected){
_3f(_5d,i);
return;
}
}
if(_5e.length){
_3f(_5d,0);
}
};
function _3f(_5f,_60){
var _61=$.data(_5f,"tabs").options;
var _62=$.data(_5f,"tabs").tabs;
var _63=$.data(_5f,"tabs").selectHis;
if(_62.length==0){
return;
}
var _64=_50(_5f,_60);
if(!_64){
return;
}
var _65=_21(_5f);
if(_65){
_65.panel("close");
_65.panel("options").tab.removeClass("tabs-selected");
}
_64.panel("open");
var _66=_64.panel("options").title;
_63.push(_66);
var tab=_64.panel("options").tab;
tab.addClass("tabs-selected");
var _67=$(_5f).find(">div.tabs-header div.tabs-wrap");
var _68=tab.position().left+_67.scrollLeft();
var _69=_68-_67.scrollLeft();
var _6a=_69+tab.outerWidth();
if(_69<0||_6a>_67.innerWidth()){
var pos=Math.min(_68-(_67.width()-tab.width())/2,_1(_5f));
_67.animate({scrollLeft:pos},_61.scrollDuration);
}else{
var pos=Math.min(_67.scrollLeft(),_1(_5f));
_67.animate({scrollLeft:pos},_61.scrollDuration);
}
_1e(_5f);
_61.onSelect.call(_5f,_66,_38(_5f,_64));
};
function _4f(_6b,_6c){
return _50(_6b,_6c)!=null;
};
$.fn.tabs=function(_6d,_6e){
if(typeof _6d=="string"){
return $.fn.tabs.methods[_6d](this,_6e);
}
_6d=_6d||{};
return this.each(function(){
var _6f=$.data(this,"tabs");
var _70;
if(_6f){
_70=$.extend(_6f.options,_6d);
_6f.options=_70;
}else{
$.data(this,"tabs",{options:$.extend({},$.fn.tabs.defaults,$.fn.tabs.parseOptions(this),_6d),tabs:[],selectHis:[]});
_25(this);
}
_11(this);
_2b(this);
_17(this);
_5c(this);
});
};
$.fn.tabs.methods={options:function(jq){
return $.data(jq[0],"tabs").options;
},tabs:function(jq){
return $.data(jq[0],"tabs").tabs;
},resize:function(jq){
return jq.each(function(){
_17(this);
_1e(this);
});
},add:function(jq,_71){
return jq.each(function(){
_3a(this,_71);
});
},close:function(jq,_72){
return jq.each(function(){
_49(this,_72);
});
},getTab:function(jq,_73){
return _50(jq[0],_73);
},getTabIndex:function(jq,tab){
return _38(jq[0],tab);
},getSelected:function(jq){
return _21(jq[0]);
},select:function(jq,_74){
return jq.each(function(){
_3f(this,_74);
});
},exists:function(jq,_75){
return _4f(jq[0],_75);
},update:function(jq,_76){
return jq.each(function(){
_39(this,_76);
});
},enableTab:function(jq,_77){
return jq.each(function(){
$(this).tabs("getTab",_77).panel("options").tab.removeClass("tabs-disabled");
});
},disableTab:function(jq,_78){
return jq.each(function(){
$(this).tabs("getTab",_78).panel("options").tab.addClass("tabs-disabled");
});
}};
$.fn.tabs.parseOptions=function(_79){
return $.extend({},$.parser.parseOptions(_79,["width","height","tools",{fit:"boolean",border:"boolean",plain:"boolean"}]));
};
$.fn.tabs.defaults={width:"auto",height:"auto",plain:false,fit:false,border:true,tools:null,scrollIncrement:100,scrollDuration:400,onLoad:function(_7a){
},onSelect:function(_7b,_7c){
},onBeforeClose:function(_7d,_7e){
},onClose:function(_7f,_80){
},onAdd:function(_81,_82){
},onUpdate:function(_83,_84){
},onContextMenu:function(e,_85,_86){
}};
})(jQuery);


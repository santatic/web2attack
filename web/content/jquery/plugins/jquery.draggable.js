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
var _1=false;
function _2(e){
var _3=$.data(e.data.target,"draggable").options;
var _4=e.data;
var _5=_4.startLeft+e.pageX-_4.startX;
var _6=_4.startTop+e.pageY-_4.startY;
if(_3.deltaX!=null&&_3.deltaX!=undefined){
_5=e.pageX+_3.deltaX;
}
if(_3.deltaY!=null&&_3.deltaY!=undefined){
_6=e.pageY+_3.deltaY;
}
if(e.data.parent!=document.body){
_5+=$(e.data.parent).scrollLeft();
_6+=$(e.data.parent).scrollTop();
}
if(_3.axis=="h"){
_4.left=_5;
}else{
if(_3.axis=="v"){
_4.top=_6;
}else{
_4.left=_5;
_4.top=_6;
}
}
};
function _7(e){
var _8=$.data(e.data.target,"draggable").options;
var _9=$.data(e.data.target,"draggable").proxy;
if(!_9){
_9=$(e.data.target);
}
_9.css({left:e.data.left,top:e.data.top});
$("body").css("cursor",_8.cursor);
};
function _a(e){
_1=true;
var _b=$.data(e.data.target,"draggable").options;
var _c=$(".droppable").filter(function(){
return e.data.target!=this;
}).filter(function(){
var _d=$.data(this,"droppable").options.accept;
if(_d){
return $(_d).filter(function(){
return this==e.data.target;
}).length>0;
}else{
return true;
}
});
$.data(e.data.target,"draggable").droppables=_c;
var _e=$.data(e.data.target,"draggable").proxy;
if(!_e){
if(_b.proxy){
if(_b.proxy=="clone"){
_e=$(e.data.target).clone().insertAfter(e.data.target);
}else{
_e=_b.proxy.call(e.data.target,e.data.target);
}
$.data(e.data.target,"draggable").proxy=_e;
}else{
_e=$(e.data.target);
}
}
_e.css("position","absolute");
_2(e);
_7(e);
_b.onStartDrag.call(e.data.target,e);
return false;
};
function _f(e){
_2(e);
if($.data(e.data.target,"draggable").options.onDrag.call(e.data.target,e)!=false){
_7(e);
}
var _10=e.data.target;
$.data(e.data.target,"draggable").droppables.each(function(){
var _11=$(this);
if(_11.droppable("options").disabled){
return;
}
var p2=_11.offset();
if(e.pageX>p2.left&&e.pageX<p2.left+_11.outerWidth()&&e.pageY>p2.top&&e.pageY<p2.top+_11.outerHeight()){
if(!this.entered){
$(this).trigger("_dragenter",[_10]);
this.entered=true;
}
$(this).trigger("_dragover",[_10]);
}else{
if(this.entered){
$(this).trigger("_dragleave",[_10]);
this.entered=false;
}
}
});
return false;
};
function _12(e){
_1=false;
_2(e);
var _13=$.data(e.data.target,"draggable").proxy;
var _14=$.data(e.data.target,"draggable").options;
if(_14.revert){
if(_15()==true){
$(e.data.target).css({position:e.data.startPosition,left:e.data.startLeft,top:e.data.startTop});
}else{
if(_13){
_13.animate({left:e.data.startLeft,top:e.data.startTop},function(){
_16();
});
}else{
$(e.data.target).animate({left:e.data.startLeft,top:e.data.startTop},function(){
$(e.data.target).css("position",e.data.startPosition);
});
}
}
}else{
$(e.data.target).css({position:"absolute",left:e.data.left,top:e.data.top});
_15();
}
_14.onStopDrag.call(e.data.target,e);
$(document).unbind(".draggable");
setTimeout(function(){
$("body").css("cursor","");
},100);
function _16(){
if(_13){
_13.remove();
}
$.data(e.data.target,"draggable").proxy=null;
};
function _15(){
var _17=false;
$.data(e.data.target,"draggable").droppables.each(function(){
var _18=$(this);
if(_18.droppable("options").disabled){
return;
}
var p2=_18.offset();
if(e.pageX>p2.left&&e.pageX<p2.left+_18.outerWidth()&&e.pageY>p2.top&&e.pageY<p2.top+_18.outerHeight()){
if(_14.revert){
$(e.data.target).css({position:e.data.startPosition,left:e.data.startLeft,top:e.data.startTop});
}
_16();
$(this).trigger("_drop",[e.data.target]);
_17=true;
this.entered=false;
return false;
}
});
if(!_17&&!_14.revert){
_16();
}
return _17;
};
return false;
};
$.fn.draggable=function(_19,_1a){
if(typeof _19=="string"){
return $.fn.draggable.methods[_19](this,_1a);
}
return this.each(function(){
var _1b;
var _1c=$.data(this,"draggable");
if(_1c){
_1c.handle.unbind(".draggable");
_1b=$.extend(_1c.options,_19);
}else{
_1b=$.extend({},$.fn.draggable.defaults,$.fn.draggable.parseOptions(this),_19||{});
}
if(_1b.disabled==true){
$(this).css("cursor","");
return;
}
var _1d=null;
if(typeof _1b.handle=="undefined"||_1b.handle==null){
_1d=$(this);
}else{
_1d=(typeof _1b.handle=="string"?$(_1b.handle,this):_1b.handle);
}
$.data(this,"draggable",{options:_1b,handle:_1d});
_1d.unbind(".draggable").bind("mousemove.draggable",{target:this},function(e){
if(_1){
return;
}
var _1e=$.data(e.data.target,"draggable").options;
if(_1f(e)){
$(this).css("cursor",_1e.cursor);
}else{
$(this).css("cursor","");
}
}).bind("mouseleave.draggable",{target:this},function(e){
$(this).css("cursor","");
}).bind("mousedown.draggable",{target:this},function(e){
if(_1f(e)==false){
return;
}
$(this).css("cursor","");
var _20=$(e.data.target).position();
var _21={startPosition:$(e.data.target).css("position"),startLeft:_20.left,startTop:_20.top,left:_20.left,top:_20.top,startX:e.pageX,startY:e.pageY,target:e.data.target,parent:$(e.data.target).parent()[0]};
$.extend(e.data,_21);
var _22=$.data(e.data.target,"draggable").options;
if(_22.onBeforeDrag.call(e.data.target,e)==false){
return;
}
$(document).bind("mousedown.draggable",e.data,_a);
$(document).bind("mousemove.draggable",e.data,_f);
$(document).bind("mouseup.draggable",e.data,_12);
});
function _1f(e){
var _23=$.data(e.data.target,"draggable");
var _24=_23.handle;
var _25=$(_24).offset();
var _26=$(_24).outerWidth();
var _27=$(_24).outerHeight();
var t=e.pageY-_25.top;
var r=_25.left+_26-e.pageX;
var b=_25.top+_27-e.pageY;
var l=e.pageX-_25.left;
return Math.min(t,r,b,l)>_23.options.edge;
};
});
};
$.fn.draggable.methods={options:function(jq){
return $.data(jq[0],"draggable").options;
},proxy:function(jq){
return $.data(jq[0],"draggable").proxy;
},enable:function(jq){
return jq.each(function(){
$(this).draggable({disabled:false});
});
},disable:function(jq){
return jq.each(function(){
$(this).draggable({disabled:true});
});
}};
$.fn.draggable.parseOptions=function(_28){
var t=$(_28);
return $.extend({},$.parser.parseOptions(_28,["cursor","handle","axis",{"revert":"boolean","deltaX":"number","deltaY":"number","edge":"number"}]),{disabled:(t.attr("disabled")?true:undefined)});
};
$.fn.draggable.defaults={proxy:null,revert:false,cursor:"move",deltaX:null,deltaY:null,handle:null,disabled:false,edge:0,axis:null,onBeforeDrag:function(e){
},onStartDrag:function(e){
},onDrag:function(e){
},onStopDrag:function(e){
}};
})(jQuery);


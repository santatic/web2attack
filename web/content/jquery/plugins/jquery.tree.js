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
var _3=$(_2);
_3.addClass("tree");
return _3;
};
function _4(_5){
var _6=[];
_7(_6,$(_5));
function _7(aa,_8){
_8.children("li").each(function(){
var _9=$(this);
var _a=$.extend({},$.parser.parseOptions(this,["id","iconCls","state"]),{checked:(_9.attr("checked")?true:undefined)});
_a.text=_9.children("span").html();
if(!_a.text){
_a.text=_9.html();
}
var _b=_9.children("ul");
if(_b.length){
_a.children=[];
_7(_a.children,_b);
}
aa.push(_a);
});
};
return _6;
};
function _c(_d){
var _e=$.data(_d,"tree").options;
$(_d).unbind().bind("mouseover",function(e){
var tt=$(e.target);
var _f=tt.closest("div.tree-node");
if(!_f.length){
return;
}
_f.addClass("tree-node-hover");
if(tt.hasClass("tree-hit")){
if(tt.hasClass("tree-expanded")){
tt.addClass("tree-expanded-hover");
}else{
tt.addClass("tree-collapsed-hover");
}
}
e.stopPropagation();
}).bind("mouseout",function(e){
var tt=$(e.target);
var _10=tt.closest("div.tree-node");
if(!_10.length){
return;
}
_10.removeClass("tree-node-hover");
if(tt.hasClass("tree-hit")){
if(tt.hasClass("tree-expanded")){
tt.removeClass("tree-expanded-hover");
}else{
tt.removeClass("tree-collapsed-hover");
}
}
e.stopPropagation();
}).bind("click",function(e){
var tt=$(e.target);
var _11=tt.closest("div.tree-node");
if(!_11.length){
return;
}
if(tt.hasClass("tree-hit")){
_7d(_d,_11[0]);
return false;
}else{
if(tt.hasClass("tree-checkbox")){
_31(_d,_11[0],!tt.hasClass("tree-checkbox1"));
return false;
}else{
_c6(_d,_11[0]);
_e.onClick.call(_d,_14(_d,_11[0]));
}
}
e.stopPropagation();
}).bind("dblclick",function(e){
var _12=$(e.target).closest("div.tree-node");
if(!_12.length){
return;
}
_c6(_d,_12[0]);
_e.onDblClick.call(_d,_14(_d,_12[0]));
e.stopPropagation();
}).bind("contextmenu",function(e){
var _13=$(e.target).closest("div.tree-node");
if(!_13.length){
return;
}
_e.onContextMenu.call(_d,e,_14(_d,_13[0]));
e.stopPropagation();
});
};
function _15(_16){
var _17=$(_16).find("div.tree-node");
_17.draggable("disable");
_17.css("cursor","pointer");
};
function _18(_19){
var _1a=$.data(_19,"tree").options;
var _1b=$.data(_19,"tree").tree;
_1b.find("div.tree-node").draggable({disabled:false,revert:true,cursor:"pointer",proxy:function(_1c){
var p=$("<div class=\"tree-node-proxy tree-dnd-no\"></div>").appendTo("body");
p.html($(_1c).find(".tree-title").html());
p.hide();
return p;
},deltaX:15,deltaY:15,onBeforeDrag:function(e){
if($(e.target).hasClass("tree-hit")||$(e.target).hasClass("tree-checkbox")){
return false;
}
if(e.which!=1){
return false;
}
$(this).next("ul").find("div.tree-node").droppable({accept:"no-accept"});
var _1d=$(this).find("span.tree-indent");
if(_1d.length){
e.data.startLeft+=_1d.length*_1d.width();
}
},onStartDrag:function(){
$(this).draggable("proxy").css({left:-10000,top:-10000});
},onDrag:function(e){
var x1=e.pageX,y1=e.pageY,x2=e.data.startX,y2=e.data.startY;
var d=Math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2));
if(d>3){
$(this).draggable("proxy").show();
}
this.pageY=e.pageY;
},onStopDrag:function(){
$(this).next("ul").find("div.tree-node").droppable({accept:"div.tree-node"});
}}).droppable({accept:"div.tree-node",onDragOver:function(e,_1e){
var _1f=_1e.pageY;
var top=$(this).offset().top;
var _20=top+$(this).outerHeight();
$(_1e).draggable("proxy").removeClass("tree-dnd-no").addClass("tree-dnd-yes");
$(this).removeClass("tree-node-append tree-node-top tree-node-bottom");
if(_1f>top+(_20-top)/2){
if(_20-_1f<5){
$(this).addClass("tree-node-bottom");
}else{
$(this).addClass("tree-node-append");
}
}else{
if(_1f-top<5){
$(this).addClass("tree-node-top");
}else{
$(this).addClass("tree-node-append");
}
}
},onDragLeave:function(e,_21){
$(_21).draggable("proxy").removeClass("tree-dnd-yes").addClass("tree-dnd-no");
$(this).removeClass("tree-node-append tree-node-top tree-node-bottom");
},onDrop:function(e,_22){
var _23=this;
var _24,_25;
if($(this).hasClass("tree-node-append")){
_24=_26;
}else{
_24=_27;
_25=$(this).hasClass("tree-node-top")?"top":"bottom";
}
_24(_22,_23,_25);
$(this).removeClass("tree-node-append tree-node-top tree-node-bottom");
}});
function _26(_28,_29){
if(_14(_19,_29).state=="closed"){
_71(_19,_29,function(){
_2a();
});
}else{
_2a();
}
function _2a(){
var _2b=$(_19).tree("pop",_28);
$(_19).tree("append",{parent:_29,data:[_2b]});
_1a.onDrop.call(_19,_29,_2b,"append");
};
};
function _27(_2c,_2d,_2e){
var _2f={};
if(_2e=="top"){
_2f.before=_2d;
}else{
_2f.after=_2d;
}
var _30=$(_19).tree("pop",_2c);
_2f.data=_30;
$(_19).tree("insert",_2f);
_1a.onDrop.call(_19,_2d,_30,_2e);
};
};
function _31(_32,_33,_34){
var _35=$.data(_32,"tree").options;
if(!_35.checkbox){
return;
}
var _36=_14(_32,_33);
if(_35.onBeforeCheck.call(_32,_36,_34)==false){
return;
}
var _37=$(_33);
var ck=_37.find(".tree-checkbox");
ck.removeClass("tree-checkbox0 tree-checkbox1 tree-checkbox2");
if(_34){
ck.addClass("tree-checkbox1");
}else{
ck.addClass("tree-checkbox0");
}
if(_35.cascadeCheck){
_38(_37);
_39(_37);
}
_35.onCheck.call(_32,_36,_34);
function _39(_3a){
var _3b=_3a.next().find(".tree-checkbox");
_3b.removeClass("tree-checkbox0 tree-checkbox1 tree-checkbox2");
if(_3a.find(".tree-checkbox").hasClass("tree-checkbox1")){
_3b.addClass("tree-checkbox1");
}else{
_3b.addClass("tree-checkbox0");
}
};
function _38(_3c){
var _3d=_88(_32,_3c[0]);
if(_3d){
var ck=$(_3d.target).find(".tree-checkbox");
ck.removeClass("tree-checkbox0 tree-checkbox1 tree-checkbox2");
if(_3e(_3c)){
ck.addClass("tree-checkbox1");
}else{
if(_3f(_3c)){
ck.addClass("tree-checkbox0");
}else{
ck.addClass("tree-checkbox2");
}
}
_38($(_3d.target));
}
function _3e(n){
var ck=n.find(".tree-checkbox");
if(ck.hasClass("tree-checkbox0")||ck.hasClass("tree-checkbox2")){
return false;
}
var b=true;
n.parent().siblings().each(function(){
if(!$(this).children("div.tree-node").children(".tree-checkbox").hasClass("tree-checkbox1")){
b=false;
}
});
return b;
};
function _3f(n){
var ck=n.find(".tree-checkbox");
if(ck.hasClass("tree-checkbox1")||ck.hasClass("tree-checkbox2")){
return false;
}
var b=true;
n.parent().siblings().each(function(){
if(!$(this).children("div.tree-node").children(".tree-checkbox").hasClass("tree-checkbox0")){
b=false;
}
});
return b;
};
};
};
function _40(_41,_42){
var _43=$.data(_41,"tree").options;
var _44=$(_42);
if(_45(_41,_42)){
var ck=_44.find(".tree-checkbox");
if(ck.length){
if(ck.hasClass("tree-checkbox1")){
_31(_41,_42,true);
}else{
_31(_41,_42,false);
}
}else{
if(_43.onlyLeafCheck){
$("<span class=\"tree-checkbox tree-checkbox0\"></span>").insertBefore(_44.find(".tree-title"));
}
}
}else{
var ck=_44.find(".tree-checkbox");
if(_43.onlyLeafCheck){
ck.remove();
}else{
if(ck.hasClass("tree-checkbox1")){
_31(_41,_42,true);
}else{
if(ck.hasClass("tree-checkbox2")){
var _46=true;
var _47=true;
var _48=_49(_41,_42);
for(var i=0;i<_48.length;i++){
if(_48[i].checked){
_47=false;
}else{
_46=false;
}
}
if(_46){
_31(_41,_42,true);
}
if(_47){
_31(_41,_42,false);
}
}
}
}
}
};
function _4a(_4b,ul,_4c,_4d){
var _4e=$.data(_4b,"tree").options;
_4c=_4e.loadFilter.call(_4b,_4c,$(ul).prev("div.tree-node")[0]);
if(!_4d){
$(ul).empty();
}
var _4f=[];
var _50=$(ul).prev("div.tree-node").find("span.tree-indent, span.tree-hit").length;
_51(ul,_4c,_50);
if(_4e.dnd){
_18(_4b);
}else{
_15(_4b);
}
for(var i=0;i<_4f.length;i++){
_31(_4b,_4f[i],true);
}
setTimeout(function(){
_59(_4b,_4b);
},0);
var _52=null;
if(_4b!=ul){
var _53=$(ul).prev();
_52=_14(_4b,_53[0]);
}
_4e.onLoadSuccess.call(_4b,_52,_4c);
function _51(ul,_54,_55){
for(var i=0;i<_54.length;i++){
var li=$("<li></li>").appendTo(ul);
var _56=_54[i];
if(_56.state!="open"&&_56.state!="closed"){
_56.state="open";
}
var _57=$("<div class=\"tree-node\"></div>").appendTo(li);
_57.attr("node-id",_56.id);
$.data(_57[0],"tree-node",{id:_56.id,text:_56.text,iconCls:_56.iconCls,attributes:_56.attributes});
$("<span class=\"tree-title\"></span>").html(_56.text).appendTo(_57);
if(_4e.checkbox){
if(_4e.onlyLeafCheck){
if(_56.state=="open"&&(!_56.children||!_56.children.length)){
if(_56.checked){
$("<span class=\"tree-checkbox tree-checkbox1\"></span>").prependTo(_57);
}else{
$("<span class=\"tree-checkbox tree-checkbox0\"></span>").prependTo(_57);
}
}
}else{
if(_56.checked){
$("<span class=\"tree-checkbox tree-checkbox1\"></span>").prependTo(_57);
_4f.push(_57[0]);
}else{
$("<span class=\"tree-checkbox tree-checkbox0\"></span>").prependTo(_57);
}
}
}
if(_56.children&&_56.children.length){
var _58=$("<ul></ul>").appendTo(li);
if(_56.state=="open"){
$("<span class=\"tree-icon tree-folder tree-folder-open\"></span>").addClass(_56.iconCls).prependTo(_57);
$("<span class=\"tree-hit tree-expanded\"></span>").prependTo(_57);
}else{
$("<span class=\"tree-icon tree-folder\"></span>").addClass(_56.iconCls).prependTo(_57);
$("<span class=\"tree-hit tree-collapsed\"></span>").prependTo(_57);
_58.css("display","none");
}
_51(_58,_56.children,_55+1);
}else{
if(_56.state=="closed"){
$("<span class=\"tree-icon tree-folder\"></span>").addClass(_56.iconCls).prependTo(_57);
$("<span class=\"tree-hit tree-collapsed\"></span>").prependTo(_57);
}else{
$("<span class=\"tree-icon tree-file\"></span>").addClass(_56.iconCls).prependTo(_57);
$("<span class=\"tree-indent\"></span>").prependTo(_57);
}
}
for(var j=0;j<_55;j++){
$("<span class=\"tree-indent\"></span>").prependTo(_57);
}
}
};
};
function _59(_5a,ul,_5b){
var _5c=$.data(_5a,"tree").options;
if(!_5c.lines){
return;
}
if(!_5b){
_5b=true;
$(_5a).find("span.tree-indent").removeClass("tree-line tree-join tree-joinbottom");
$(_5a).find("div.tree-node").removeClass("tree-node-last tree-root-first tree-root-one");
var _5d=$(_5a).tree("getRoots");
if(_5d.length>1){
$(_5d[0].target).addClass("tree-root-first");
}else{
$(_5d[0].target).addClass("tree-root-one");
}
}
$(ul).children("li").each(function(){
var _5e=$(this).children("div.tree-node");
var ul=_5e.next("ul");
if(ul.length){
if($(this).next().length){
_5f(_5e);
}
_59(_5a,ul,_5b);
}else{
_60(_5e);
}
});
var _61=$(ul).children("li:last").children("div.tree-node").addClass("tree-node-last");
_61.children("span.tree-join").removeClass("tree-join").addClass("tree-joinbottom");
function _60(_62,_63){
var _64=_62.find("span.tree-icon");
_64.prev("span.tree-indent").addClass("tree-join");
};
function _5f(_65){
var _66=_65.find("span.tree-indent, span.tree-hit").length;
_65.next().find("div.tree-node").each(function(){
$(this).children("span:eq("+(_66-1)+")").addClass("tree-line");
});
};
};
function _67(_68,ul,_69,_6a){
var _6b=$.data(_68,"tree").options;
_69=_69||{};
var _6c=null;
if(_68!=ul){
var _6d=$(ul).prev();
_6c=_14(_68,_6d[0]);
}
if(_6b.onBeforeLoad.call(_68,_6c,_69)==false){
return;
}
var _6e=$(ul).prev().children("span.tree-folder");
_6e.addClass("tree-loading");
var _6f=_6b.loader.call(_68,_69,function(_70){
_6e.removeClass("tree-loading");
_4a(_68,ul,_70);
if(_6a){
_6a();
}
},function(){
_6e.removeClass("tree-loading");
_6b.onLoadError.apply(_68,arguments);
if(_6a){
_6a();
}
});
if(_6f==false){
_6e.removeClass("tree-loading");
}
};
function _71(_72,_73,_74){
var _75=$.data(_72,"tree").options;
var hit=$(_73).children("span.tree-hit");
if(hit.length==0){
return;
}
if(hit.hasClass("tree-expanded")){
return;
}
var _76=_14(_72,_73);
if(_75.onBeforeExpand.call(_72,_76)==false){
return;
}
hit.removeClass("tree-collapsed tree-collapsed-hover").addClass("tree-expanded");
hit.next().addClass("tree-folder-open");
var ul=$(_73).next();
if(ul.length){
if(_75.animate){
ul.slideDown("normal",function(){
_75.onExpand.call(_72,_76);
if(_74){
_74();
}
});
}else{
ul.css("display","block");
_75.onExpand.call(_72,_76);
if(_74){
_74();
}
}
}else{
var _77=$("<ul style=\"display:none\"></ul>").insertAfter(_73);
_67(_72,_77[0],{id:_76.id},function(){
if(_77.is(":empty")){
_77.remove();
}
if(_75.animate){
_77.slideDown("normal",function(){
_75.onExpand.call(_72,_76);
if(_74){
_74();
}
});
}else{
_77.css("display","block");
_75.onExpand.call(_72,_76);
if(_74){
_74();
}
}
});
}
};
function _78(_79,_7a){
var _7b=$.data(_79,"tree").options;
var hit=$(_7a).children("span.tree-hit");
if(hit.length==0){
return;
}
if(hit.hasClass("tree-collapsed")){
return;
}
var _7c=_14(_79,_7a);
if(_7b.onBeforeCollapse.call(_79,_7c)==false){
return;
}
hit.removeClass("tree-expanded tree-expanded-hover").addClass("tree-collapsed");
hit.next().removeClass("tree-folder-open");
var ul=$(_7a).next();
if(_7b.animate){
ul.slideUp("normal",function(){
_7b.onCollapse.call(_79,_7c);
});
}else{
ul.css("display","none");
_7b.onCollapse.call(_79,_7c);
}
};
function _7d(_7e,_7f){
var hit=$(_7f).children("span.tree-hit");
if(hit.length==0){
return;
}
if(hit.hasClass("tree-expanded")){
_78(_7e,_7f);
}else{
_71(_7e,_7f);
}
};
function _80(_81,_82){
var _83=_49(_81,_82);
if(_82){
_83.unshift(_14(_81,_82));
}
for(var i=0;i<_83.length;i++){
_71(_81,_83[i].target);
}
};
function _84(_85,_86){
var _87=[];
var p=_88(_85,_86);
while(p){
_87.unshift(p);
p=_88(_85,p.target);
}
for(var i=0;i<_87.length;i++){
_71(_85,_87[i].target);
}
};
function _89(_8a,_8b){
var _8c=_49(_8a,_8b);
if(_8b){
_8c.unshift(_14(_8a,_8b));
}
for(var i=0;i<_8c.length;i++){
_78(_8a,_8c[i].target);
}
};
function _8d(_8e){
var _8f=_90(_8e);
if(_8f.length){
return _8f[0];
}else{
return null;
}
};
function _90(_91){
var _92=[];
$(_91).children("li").each(function(){
var _93=$(this).children("div.tree-node");
_92.push(_14(_91,_93[0]));
});
return _92;
};
function _49(_94,_95){
var _96=[];
if(_95){
_97($(_95));
}else{
var _98=_90(_94);
for(var i=0;i<_98.length;i++){
_96.push(_98[i]);
_97($(_98[i].target));
}
}
function _97(_99){
_99.next().find("div.tree-node").each(function(){
_96.push(_14(_94,this));
});
};
return _96;
};
function _88(_9a,_9b){
var ul=$(_9b).parent().parent();
if(ul[0]==_9a){
return null;
}else{
return _14(_9a,ul.prev()[0]);
}
};
function _9c(_9d,_9e){
_9e=_9e||"checked";
var _9f="";
if(_9e=="checked"){
_9f="span.tree-checkbox1";
}else{
if(_9e=="unchecked"){
_9f="span.tree-checkbox0";
}else{
if(_9e=="indeterminate"){
_9f="span.tree-checkbox2";
}
}
}
var _a0=[];
$(_9d).find(_9f).each(function(){
var _a1=$(this).parent();
_a0.push(_14(_9d,_a1[0]));
});
return _a0;
};
function _a2(_a3){
var _a4=$(_a3).find("div.tree-node-selected");
if(_a4.length){
return _14(_a3,_a4[0]);
}else{
return null;
}
};
function _a5(_a6,_a7){
var _a8=$(_a7.parent);
var ul;
if(_a8.length==0){
ul=$(_a6);
}else{
ul=_a8.next();
if(ul.length==0){
ul=$("<ul></ul>").insertAfter(_a8);
}
}
if(_a7.data&&_a7.data.length){
var _a9=_a8.find("span.tree-icon");
if(_a9.hasClass("tree-file")){
_a9.removeClass("tree-file").addClass("tree-folder");
var hit=$("<span class=\"tree-hit tree-expanded\"></span>").insertBefore(_a9);
if(hit.prev().length){
hit.prev().remove();
}
}
}
_4a(_a6,ul[0],_a7.data,true);
_40(_a6,ul.prev());
};
function _aa(_ab,_ac){
var ref=_ac.before||_ac.after;
var _ad=_88(_ab,ref);
var li;
if(_ad){
_a5(_ab,{parent:_ad.target,data:[_ac.data]});
li=$(_ad.target).next().children("li:last");
}else{
_a5(_ab,{parent:null,data:[_ac.data]});
li=$(_ab).children("li:last");
}
if(_ac.before){
li.insertBefore($(ref).parent());
}else{
li.insertAfter($(ref).parent());
}
};
function _ae(_af,_b0){
var _b1=_88(_af,_b0);
var _b2=$(_b0);
var li=_b2.parent();
var ul=li.parent();
li.remove();
if(ul.children("li").length==0){
var _b2=ul.prev();
_b2.find(".tree-icon").removeClass("tree-folder").addClass("tree-file");
_b2.find(".tree-hit").remove();
$("<span class=\"tree-indent\"></span>").prependTo(_b2);
if(ul[0]!=_af){
ul.remove();
}
}
if(_b1){
_40(_af,_b1.target);
}
_59(_af,_af);
};
function _b3(_b4,_b5){
function _b6(aa,ul){
ul.children("li").each(function(){
var _b7=$(this).children("div.tree-node");
var _b8=_14(_b4,_b7[0]);
var sub=$(this).children("ul");
if(sub.length){
_b8.children=[];
_b6(_b8.children,sub);
}
aa.push(_b8);
});
};
if(_b5){
var _b9=_14(_b4,_b5);
_b9.children=[];
_b6(_b9.children,$(_b5).next());
return _b9;
}else{
return null;
}
};
function _ba(_bb,_bc){
var _bd=$(_bc.target);
var _be=_14(_bb,_bc.target);
if(_be.iconCls){
_bd.find(".tree-icon").removeClass(_be.iconCls);
}
var _bf=$.extend({},_be,_bc);
$.data(_bc.target,"tree-node",_bf);
_bd.attr("node-id",_bf.id);
_bd.find(".tree-title").html(_bf.text);
if(_bf.iconCls){
_bd.find(".tree-icon").addClass(_bf.iconCls);
}
if(_be.checked!=_bf.checked){
_31(_bb,_bc.target,_bf.checked);
}
};
function _14(_c0,_c1){
var _c2=$.extend({},$.data(_c1,"tree-node"),{target:_c1,checked:$(_c1).find(".tree-checkbox").hasClass("tree-checkbox1")});
if(!_45(_c0,_c1)){
_c2.state=$(_c1).find(".tree-hit").hasClass("tree-expanded")?"open":"closed";
}
return _c2;
};
function _c3(_c4,id){
var _c5=$(_c4).find("div.tree-node[node-id="+id+"]");
if(_c5.length){
return _14(_c4,_c5[0]);
}else{
return null;
}
};
function _c6(_c7,_c8){
var _c9=$.data(_c7,"tree").options;
var _ca=_14(_c7,_c8);
if(_c9.onBeforeSelect.call(_c7,_ca)==false){
return;
}
$("div.tree-node-selected",_c7).removeClass("tree-node-selected");
$(_c8).addClass("tree-node-selected");
_c9.onSelect.call(_c7,_ca);
};
function _45(_cb,_cc){
var _cd=$(_cc);
var hit=_cd.children("span.tree-hit");
return hit.length==0;
};
function _ce(_cf,_d0){
var _d1=$.data(_cf,"tree").options;
var _d2=_14(_cf,_d0);
if(_d1.onBeforeEdit.call(_cf,_d2)==false){
return;
}
$(_d0).css("position","relative");
var nt=$(_d0).find(".tree-title");
var _d3=nt.outerWidth();
nt.empty();
var _d4=$("<input class=\"tree-editor\">").appendTo(nt);
_d4.val(_d2.text).focus();
_d4.width(_d3+20);
_d4.height(document.compatMode=="CSS1Compat"?(18-(_d4.outerHeight()-_d4.height())):18);
_d4.bind("click",function(e){
return false;
}).bind("mousedown",function(e){
e.stopPropagation();
}).bind("mousemove",function(e){
e.stopPropagation();
}).bind("keydown",function(e){
if(e.keyCode==13){
_d5(_cf,_d0);
return false;
}else{
if(e.keyCode==27){
_db(_cf,_d0);
return false;
}
}
}).bind("blur",function(e){
e.stopPropagation();
_d5(_cf,_d0);
});
};
function _d5(_d6,_d7){
var _d8=$.data(_d6,"tree").options;
$(_d7).css("position","");
var _d9=$(_d7).find("input.tree-editor");
var val=_d9.val();
_d9.remove();
var _da=_14(_d6,_d7);
_da.text=val;
_ba(_d6,_da);
_d8.onAfterEdit.call(_d6,_da);
};
function _db(_dc,_dd){
var _de=$.data(_dc,"tree").options;
$(_dd).css("position","");
$(_dd).find("input.tree-editor").remove();
var _df=_14(_dc,_dd);
_ba(_dc,_df);
_de.onCancelEdit.call(_dc,_df);
};
$.fn.tree=function(_e0,_e1){
if(typeof _e0=="string"){
return $.fn.tree.methods[_e0](this,_e1);
}
var _e0=_e0||{};
return this.each(function(){
var _e2=$.data(this,"tree");
var _e3;
if(_e2){
_e3=$.extend(_e2.options,_e0);
_e2.options=_e3;
}else{
_e3=$.extend({},$.fn.tree.defaults,$.fn.tree.parseOptions(this),_e0);
$.data(this,"tree",{options:_e3,tree:_1(this)});
var _e4=_4(this);
if(_e4.length&&!_e3.data){
_e3.data=_e4;
}
}
_c(this);
if(_e3.lines){
$(this).addClass("tree-lines");
}
if(_e3.data){
_4a(this,this,_e3.data);
}else{
if(_e3.dnd){
_18(this);
}else{
_15(this);
}
}
_67(this,this);
});
};
$.fn.tree.methods={options:function(jq){
return $.data(jq[0],"tree").options;
},loadData:function(jq,_e5){
return jq.each(function(){
_4a(this,this,_e5);
});
},getNode:function(jq,_e6){
return _14(jq[0],_e6);
},getData:function(jq,_e7){
return _b3(jq[0],_e7);
},reload:function(jq,_e8){
return jq.each(function(){
if(_e8){
var _e9=$(_e8);
var hit=_e9.children("span.tree-hit");
hit.removeClass("tree-expanded tree-expanded-hover").addClass("tree-collapsed");
_e9.next().remove();
_71(this,_e8);
}else{
$(this).empty();
_67(this,this);
}
});
},getRoot:function(jq){
return _8d(jq[0]);
},getRoots:function(jq){
return _90(jq[0]);
},getParent:function(jq,_ea){
return _88(jq[0],_ea);
},getChildren:function(jq,_eb){
return _49(jq[0],_eb);
},getChecked:function(jq,_ec){
return _9c(jq[0],_ec);
},getSelected:function(jq){
return _a2(jq[0]);
},isLeaf:function(jq,_ed){
return _45(jq[0],_ed);
},find:function(jq,id){
return _c3(jq[0],id);
},select:function(jq,_ee){
return jq.each(function(){
_c6(this,_ee);
});
},check:function(jq,_ef){
return jq.each(function(){
_31(this,_ef,true);
});
},uncheck:function(jq,_f0){
return jq.each(function(){
_31(this,_f0,false);
});
},collapse:function(jq,_f1){
return jq.each(function(){
_78(this,_f1);
});
},expand:function(jq,_f2){
return jq.each(function(){
_71(this,_f2);
});
},collapseAll:function(jq,_f3){
return jq.each(function(){
_89(this,_f3);
});
},expandAll:function(jq,_f4){
return jq.each(function(){
_80(this,_f4);
});
},expandTo:function(jq,_f5){
return jq.each(function(){
_84(this,_f5);
});
},toggle:function(jq,_f6){
return jq.each(function(){
_7d(this,_f6);
});
},append:function(jq,_f7){
return jq.each(function(){
_a5(this,_f7);
});
},insert:function(jq,_f8){
return jq.each(function(){
_aa(this,_f8);
});
},remove:function(jq,_f9){
return jq.each(function(){
_ae(this,_f9);
});
},pop:function(jq,_fa){
var _fb=jq.tree("getData",_fa);
jq.tree("remove",_fa);
return _fb;
},update:function(jq,_fc){
return jq.each(function(){
_ba(this,_fc);
});
},enableDnd:function(jq){
return jq.each(function(){
_18(this);
});
},disableDnd:function(jq){
return jq.each(function(){
_15(this);
});
},beginEdit:function(jq,_fd){
return jq.each(function(){
_ce(this,_fd);
});
},endEdit:function(jq,_fe){
return jq.each(function(){
_d5(this,_fe);
});
},cancelEdit:function(jq,_ff){
return jq.each(function(){
_db(this,_ff);
});
}};
$.fn.tree.parseOptions=function(_100){
var t=$(_100);
return $.extend({},$.parser.parseOptions(_100,["url","method",{checkbox:"boolean",cascadeCheck:"boolean",onlyLeafCheck:"boolean"},{animate:"boolean",lines:"boolean",dnd:"boolean"}]));
};
$.fn.tree.defaults={url:null,method:"post",animate:false,checkbox:false,cascadeCheck:true,onlyLeafCheck:false,lines:false,dnd:false,data:null,loader:function(_101,_102,_103){
var opts=$(this).tree("options");
if(!opts.url){
return false;
}
$.ajax({type:opts.method,url:opts.url,data:_101,dataType:"json",success:function(data){
_102(data);
},error:function(){
_103.apply(this,arguments);
}});
},loadFilter:function(data,_104){
return data;
},onBeforeLoad:function(node,_105){
},onLoadSuccess:function(node,data){
},onLoadError:function(){
},onClick:function(node){
},onDblClick:function(node){
},onBeforeExpand:function(node){
},onExpand:function(node){
},onBeforeCollapse:function(node){
},onCollapse:function(node){
},onBeforeCheck:function(node,_106){
},onCheck:function(node,_107){
},onBeforeSelect:function(node){
},onSelect:function(node){
},onContextMenu:function(e,node){
},onDrop:function(_108,_109,_10a){
},onBeforeEdit:function(node){
},onAfterEdit:function(node){
},onCancelEdit:function(node){
}};
})(jQuery);


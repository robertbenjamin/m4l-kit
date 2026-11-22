var REPLICAS={};
function poly(pts,color,w){return '<polyline points="'+pts.map(function(p){return p[0].toFixed(2)+','+p[1].toFixed(2)}).join(' ')+'" style="fill:none;stroke:var(--'+color+');stroke-width:'+(w||1.5)+'"/>';}
REPLICAS.Saturator=function(el,w){
  var D=DATA.Saturator,d=LiveKit.device(el,{w:w,zoom:(window.LK_ZOOM||1)});d.titleName('Saturator','closed');
  d.display(4,4,219,109);d.dropdown(8,8,105,'Sinoid Fold');
  d.graph(8,25,211,67,D.curve,{under:function(g){g.svg('<rect x="'+D.shadeE[0]+'" y="26" width="'+(D.shadeE[1]-D.shadeE[0])+'" height="65" style="fill:var(--teal-shade)"/>');}});
  d.svg('<circle cx="14.5" cy="102.5" r="2.5" style="fill:var(--led-off)"/>');
  d.chooser(22,98.5,'No Clip',{triX:70.5});d.button(93,96,41,'Color','outline');
  d.text(146,98.5,'Amt Lo',{color:'text-dim'});d.text(184,98.5,'0.0 %',{color:'text-dim'});
  [[45.5,'Drive','6.2 dB'],[113.5,'Output','0.0 dB'],[181.5,'Dry/Wet','62 %']].forEach(function(c,i){d.dial({cx:c[0],cap:119.5,label:c[1],value:c[2],v:(D.ang[i]+150)/300});});
};
REPLICAS.ChannelEQ=function(el,w){
  var D=DATA.ChannelEQ,d=LiveKit.device(el,{w:w,zoom:(window.LK_ZOOM||1)});d.titleName('Channel EQ');
  d.display(4,4,239,103);
  [59,139,218].forEach(function(x){d.vline(x,4,70,'grid-decade');});
  d.hline(26,12,217,'grid-level');d.hline(26,44,217,'grid-decade');
  [[26,47],[71,130],[148,206],[230,243]].forEach(function(s){d.hline(s[0],76,s[1]-s[0],'grid-level');});
  d.svg('<path d="'+D.spectrum+'" style="fill:var(--spectrum)"/>');
  [['12',8.5,22.5],['0',40.5,22.5],['-12',72.5,23.5]].forEach(function(l){d.text(l[2],l[1],l[0],{align:'right',color:'text-axis'});});
  [[59,'100'],[139,'1k'],[218,'10k']].forEach(function(l){d.text(l[0],75.5,l[1],{align:'center',color:'text-axis'});});
  d.svg(poly(D.curve,'teal'));
  d.hline(4,85,239,'grid');
  d.rect(8,90,21,13,'orange');
  d.svg(D.icon.map(function(p){return '<rect x="'+p[0]+'" y="'+p[1]+'" width=".5" height=".5" style="fill:var(--display);fill-opacity:'+p[2]+'"/>';}).join(''));
  d.text(64.5,92.5,'5.78 kHz',{color:'orange'});
  d.pointer(86.5,106.5);
  [[36.5,'Low','-12 dB'],[86.5,'Mid','10 dB'],[136.5,'High','-0.5 dB'],[210.5,'Output','5.6 dB']].forEach(function(c,i){d.dial({cx:c[0],cap:115.5,label:c[1],value:c[2],v:(D.ang[i]+150)/300,bipolar:true,notch:true});});
  d.divider(173,111,56);
};
REPLICAS.AutoPanTremolo=function(el,w){
  var D=DATA.AutoPanTremolo,d=LiveKit.device(el,{w:w,zoom:(window.LK_ZOOM||1),gx:.5});d.titleName('Auto Pan-Tremolo');
  d.display(3.5,3.5,243,109);
  d.button(7.5,7.5,116,'Panning','on');d.button(126.5,7.5,116,'Tremolo','outline');
  d.cells(D.waveO,'orange');d.cells(D.waveT,'teal');
  d.text(9.5,81,'L',{color:'teal'});d.text(234.5,81,'R',{color:'orange'});
  d.segments(20.5,81.5,D.segs[0].map(function(s){return {c:s[0],a:s[1]};}));d.segments(126.5,81.5,D.segs[1].map(function(s){return {c:s[0],a:s[1]};}));
  d.dropdown(7.5,95.5,47,'',{color:'orange'});d.cells(D.ddicon,'on-accent');
  d.chooser(72.5,98,'Rate',{color:'orange',triX:111});
  d.button(128.5,95.5,13,'','on');d.cells(D.phase,'on-toggle');
  d.text(147.5,98,'180°',{color:'orange'});
  d.button(175.5,95.5,13,'','outline');d.cells(D.arrows,'orange');
  d.cells(D.wave,'text-dim');d.text(216.5,98,'0.0°',{color:'text-dim'});
  [[31,'Amount','59 %'],[95,'Freq','1.63 Hz'],[159,'Shape','17 %']].forEach(function(c,i){d.dial({cx:c[0],cap:119,label:c[1],value:c[2],v:(D.ang[i]+150)/300});});
  d.text(220,119,'Att | Mod',{align:'center'});
  d.numbox(197.5,131.5,45,'191 ms',.372);d.numbox(197.5,149.5,45,'50 %',.5,{bipolar:true});
};

/* Live Device Kit: draws Live 12 device parts at Live's 1x grid (100 % zoom). Body coordinates: (0,0) = top-left of the body under the title bar. */
(function(){
  var FAMILY='"Ableton Sans Small","Ableton Sans","Helvetica Neue",Arial,sans-serif';
  var P={CAP:2.1,SPAN:150,SPAN_L:150,GAP:5,SIZE:26.125,SIZE_L:37,SW:2.1,PW:2.2,CY:.4375,CX:0,PTR_IN:.25,PTR_IN_L:4.2,PTR_OUT:-1.25,LABEL:9.5,LABEL_L:11.5,VALUE:26.5,VALUE_L:39,NOTCH:5.4,TRI_TOP:5.375,TRI_H:4.5,TRI_W:9,TIP:1,CY_N:.125,KO:1.125,ADV:0,ADVMODE:0,TRACK:0,LDX:.5,LDX_N:1,VDX_N:.25,VDY_N:.5};
  var uid=0;
  var ctx=null;
  function width(s,size,weight){
    if(!ctx){ctx=document.createElement('canvas').getContext('2d');}
    ctx.font=(weight||400)+' '+(size||10)+'px '+FAMILY;
    return ctx.measureText(s).width;
  }
  function v(t){return 'var(--'+t+')';}
  function n(x){return (+x).toFixed(2);}
  var n2=n;
  function arc(cx,cy,r,a0,a1){
    var lo=Math.min(a0,a1),hi=Math.max(a0,a1);
    if(hi-lo<0.5)return '';
    function p(a){var t=a*Math.PI/180;return [cx+r*Math.sin(t),cy-r*Math.cos(t)];}
    var s=p(lo),e=p(hi);
    return 'M'+n(s[0])+' '+n(s[1])+'A'+r+' '+r+' 0 '+(hi-lo>180?1:0)+' 1 '+n(e[0])+' '+n(e[1]);
  }
  // ?ref=1&zoom=Z&theme=T: the first device draws alone, body only, at zoom Z on magenta, for pixel comparison
  var REF=(function(){try{var q=new URLSearchParams(location.search);return q.has('ref')?{zoom:+q.get('zoom')||2,theme:q.get('theme')||'dark'}:null;}catch(e){return null;}})(),refUsed=false;
  function device(el,o){
    o=o||{};
    var isRef=!!REF&&!refUsed&&o.ref!==false;
    if(isRef){refUsed=true;o.zoom=REF.zoom;o.title=false;}
    var w=o.w||227, H=o.h||169, zoom=o.zoom||2, GX=o.gx||0;
    var wrap=document.createElement('div');wrap.className='lk-wrap';wrap.style.zoom=zoom;
    if(isRef){wrap.classList.add('lk-ref-target','th-'+REF.theme);document.documentElement.classList.add('lk-ref');document.documentElement.setAttribute('data-lk-theme',REF.theme);}
    var title=document.createElement('div');title.className='lk-title';title.style.width=w+'px';
    var dev=document.createElement('div');dev.className='lk-dev';dev.style.width=w+'px';dev.style.height=H+'px';
    if(o.ground)dev.style.background=v(o.ground);
    var svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('class','lk-g');
    svg.setAttribute('width',w);svg.setAttribute('height',H);
    dev.appendChild(svg);
    if(o.title!==false){wrap.appendChild(title);}
    wrap.appendChild(dev);el.appendChild(wrap);
    var buf='';
    function g(s){buf+=s;svg.innerHTML=buf;return api;}
    function layout(s,size,weight){
      var xs=[],acc=0,i,a;
      if(!P.ADV){return {xs:null,w:width(s,size,weight)+P.TRACK*s.length};}
      for(i=0;i<s.length;i++){
        xs.push(acc);
        a=P.ADVMODE?width(s.slice(0,i+1),size,weight)-width(s.slice(0,i),size,weight):width(s[i],size,weight);
        acc+=Math.round(a/P.ADV)*P.ADV;
      }
      return {xs:xs,w:acc};
    }
    function text(x,cap,s,opt){
      opt=opt||{};var size=opt.size||10,weight=opt.weight||400;
      var L=layout(s,size,weight),tw=L.w;
      if(opt.align==='center')x-=tw/2;else if(opt.align==='right')x-=tw;
      if(opt.align==="center"||opt.align==="right")x=Math.round(x-GX)+GX;
      var parts=L.xs?s.split('').map(function(ch,i){return [ch,x+L.xs[i]];}):[[s,x]];
      parts.forEach(function(pt){
        var d=document.createElement('div');d.className='t';d.textContent=pt[0];
        d.style.left=pt[1]+'px';d.style.top=(cap-P.CAP*size/10)+'px';d.style.color=v(opt.color||'text');
        if(size!==10)d.style.fontSize=size+'px';if(weight!==400)d.style.fontWeight=weight;if(P.TRACK)d.style.letterSpacing=P.TRACK+'px';
        dev.appendChild(d);
      });
      return api;
    }
    function rect(x,y,w2,h,fill,o2){
      o2=o2||{};var s='<rect x="'+x+'" y="'+y+'" width="'+w2+'" height="'+h+'"'+(o2.r?' rx="'+o2.r+'"':'')+' style="fill:'+(fill?v(fill):'none')+(o2.opacity!=null?';fill-opacity:'+o2.opacity:'')+'"/>';
      if(o2.border)s+='<rect x="'+(x+.5)+'" y="'+(y+.5)+'" width="'+(w2-1)+'" height="'+(h-1)+'" style="fill:none;stroke:'+v(o2.border)+'"/>';
      return g(s);
    }
    var api={
      el:dev,width:w,text:text,rect:rect,svg:g,
      titleName:function(name,fold){
        var t='<div style="position:absolute;left:3px;top:2px;width:13px;height:13px;box-sizing:border-box;border-radius:50%;background:'+v('orange')+';border:1px solid '+v('ring')+'"></div>';
        var nx=21;
        if(fold){t+='<svg style="position:absolute;left:0;top:0" width="40" height="17"><path d="'+(fold==='open'?'M22.5 5.6H29.5L26 10.6Z':'M23.5 4.6L28.5 8.1L23.5 11.6Z')+'" style="fill:'+v('text')+'"/></svg>';nx=34;}
        t+='<div style="position:absolute;left:'+nx+'px;top:3px;font-family:var(--font-live);font-size:11px;line-height:12px;font-weight:700;color:'+v('text')+'">'+name+'</div>';
        title.innerHTML=t;return api;
      },
      display:function(x,y,w2,h){return rect(x,y,w2,h,'display',{r:2});},
      tile:function(x,y,w2,h,fill){return rect(x,y,w2,h,fill||'body',{r:2});},
      divider:function(x,y,h){return rect(x,y,1,h,'divider');},
      hline:function(x,y,w2,c){return rect(x,y,w2,1,c||'grid');},
      vline:function(x,y,h,c){return rect(x,y,1,h,c||'grid');},
      dial:function(d){
        var large=!!d.large, color=d.color||'teal';
        var size=large?P.SIZE_L:P.SIZE, span=large?P.SPAN_L:P.SPAN, SW=P.SW, PW=P.PW, r=size/2-SW/2;
        var ringTop=d.cap+(large?P.LABEL_L:P.LABEL)+(d.notch?P.NOTCH:0);
        var cy=ringTop+size/2+(d.notch?P.CY_N:P.CY), cx=d.cx+P.CX;
        var a=-span+2*span*d.v, base=d.bipolar?0:-span;
        function p(ang,rad){var t=ang*Math.PI/180;return [cx+rad*Math.sin(t),cy-rad*Math.cos(t)];}
        var gp=P.KO?0:P.GAP/2/r*180/Math.PI, p1=p(a,large?P.PTR_IN_L:P.PTR_IN), p2=p(a,r+SW/2+P.PTR_OUT), lit, ring;
        if(a>=base){lit=arc(cx,cy,r,base,a);ring=arc(cx,cy,r,-span,base)+arc(cx,cy,r,a+gp,span);}
        else{lit=arc(cx,cy,r,a,base);ring=arc(cx,cy,r,-span,a-gp)+arc(cx,cy,r,base,span);}
        var mk='',ma='';
        if(P.KO){var id='lkm'+(++uid);ma=' mask="url(#'+id+')"';
          mk='<mask id="'+id+'" maskUnits="userSpaceOnUse" x="'+(cx-size)+'" y="'+(cy-size)+'" width="'+(2*size)+'" height="'+(2*size)+'"><rect x="'+(cx-size)+'" y="'+(cy-size)+'" width="'+(2*size)+'" height="'+(2*size)+'" fill="#fff"/>'+
            '<line x1="'+n(p1[0])+'" y1="'+n(p1[1])+'" x2="'+n(p2[0])+'" y2="'+n(p2[1])+'" stroke="#000" stroke-linecap="round" stroke-width="'+(PW+2*P.KO)+'"/></mask>';}
        var s=mk+'<path d="'+ring+'"'+ma+' style="fill:none;stroke:'+v('ring')+';stroke-width:'+SW+'"/>'+
          '<path d="'+lit+'" style="fill:none;stroke:'+v(color)+';stroke-width:'+SW+'"/>'+
          '<line x1="'+n(p1[0])+'" y1="'+n(p1[1])+'" x2="'+n(p2[0])+'" y2="'+n(p2[1])+'" style="stroke:'+v('pointer')+';stroke-width:'+PW+'"/>'+
          '<circle cx="'+n(p1[0])+'" cy="'+n(p1[1])+'" r="'+(PW/2)+'" style="fill:'+v('pointer')+'"/>'+
          (P.TIP?'<circle cx="'+n(p2[0])+'" cy="'+n(p2[1])+'" r="'+(PW/2)+'" style="fill:'+v('pointer')+'"/>':'');
        if(d.notch){s+='<path d="M'+n(cx-P.TRI_W/2)+' '+n(ringTop-P.TRI_TOP)+'H'+n(cx+P.TRI_W/2)+'L'+n(cx)+' '+n(ringTop-P.TRI_TOP+P.TRI_H)+'Z" style="fill:'+v(Math.abs(d.v-.5)>.01?color:'ring')+'"/>';}
        g(s);
        if(d.label)text(cx+(d.notch?P.LDX_N:P.LDX),d.cap,d.label,{align:'center'});
        if(d.value)text(cx+(d.notch?P.VDX_N:0),ringTop+(large?P.VALUE_L:P.VALUE)+(d.notch?P.VDY_N:0),d.value,{align:'center'});
        return api;
      },
      numbox:function(x,y,w2,value,frac,o2){
        o2=o2||{};var iw=w2-2,x0=x+1,x1;
        rect(x,y,w2,13,'field',{border:'button-border'});
        if(o2.bipolar){x0=x+1+Math.floor(iw/2);x1=x0+Math.round(frac*iw/2);}else{x1=x0+Math.round(Math.max(0,Math.min(1,frac))*iw);}
        if(x1!==x0)rect(Math.min(x0,x1),y+1,Math.abs(x1-x0),11,'teal-deep');
        return text(x+w2/2+(o2.dx||0),y+(o2.cap!=null?o2.cap:3),value,{align:'center'});
      },
      segments:function(x,y,segs,o2){
        o2=o2||{};var w3=o2.w||3,h=o2.h||7,pitch=o2.pitch||4,s='';
        segs.forEach(function(sg,i){s+='<rect x="'+(x+i*pitch)+'" y="'+y+'" width="'+w3+'" height="'+h+'" style="fill:'+v(sg.c)+';fill-opacity:'+(sg.a==null?1:sg.a)+'"/>';});
        return g(s);
      },
      cells:function(list,ink){
        return g(list.map(function(p){return '<rect x="'+p[0]+'" y="'+p[1]+'" width=".5" height=".5" style="fill:'+v(ink)+';fill-opacity:'+p[2]+'"/>';}).join(''));
      },
      button:function(x,y,w2,label,state){
        if(state==='on'){rect(x,y,w2,13,'orange');return text(x+w2/2,y+2.5,label,{align:'center',color:'on-accent'});}
        if(state==='outline'){rect(x,y,w2,13,null,{border:'orange'});return text(x+w2/2,y+2.5,label,{align:'center',color:'orange'});}
        if(state==='mapped-on'){rect(x,y,w2,13,'text-dim');return text(x+w2/2,y+2.5,label,{align:'center',color:'on-accent'});}
        if(state==='mapped'){rect(x,y,w2,13,null,{border:'text-dim'});return text(x+w2/2,y+2.5,label,{align:'center',color:'text-dim'});}
        rect(x,y,w2,13,'box',{border:'ring'});return text(x+w2/2,y+2.5,label,{align:'center'});
      },
      toggle:function(x,y,w2,label,on){
        rect(x,y,w2,13,on?'orange':'button-off',{border:'button-border'});
        return label?text(x+w2/2,y+2.5,label,{align:'center',color:on?'on-toggle':'text'}):api;
      },
      connector:function(x1,x2,y){return rect(x1,y,x2-x1,1,'divider');},
      readout:function(x,cap,label,value){text(x,cap,label,{color:'text-dim'});return text(x,cap+13.6,value,{color:'orange'});},
      inlineReadout:function(x,cap,label,value){text(x,cap,label,{color:'text-dim'});return text(x+Math.round(width(label))+6,cap,value,{color:'orange'});},
      dropdown:function(x,y,w2,label,o2){
        o2=o2||{};rect(x,y,w2,13,o2.color||'teal');if(label)text(x+2,y+2.5,label,{color:'on-accent'});
        return g('<path d="M'+(x+w2-9)+' '+(y+4)+'h7l-3.5 4.75z" style="fill:'+v('on-accent')+'"/>');
      },
      chooser:function(x,cap,label,o2){
        o2=o2||{};var c=o2.color||'teal',tx=o2.triX!=null?o2.triX:x+width(label)-2+6;text(x,cap,label,{color:c});
        return g('<path d="M'+tx+' '+(cap+3.5)+'h5l-2.5 2.5z" style="fill:'+v(c)+'"/>');
      },
      pointer:function(x,y,dir){
        var d=dir==='left'?'M'+x+' '+(y-4)+'V'+(y+4)+'L'+(x-4)+' '+y+'Z':'M'+(x-4)+' '+y+'H'+(x+4)+'L'+x+' '+(y+4)+'Z';
        return g('<path d="'+d+'" style="fill:'+v('display')+'"/>');
      },
      graph:function(x,y,w2,h,pts,o2){
        o2=o2||{};var s='';
        if(o2.under)o2.under(api);
        if(o2.border!==false)s+='<rect x="'+(x+.5)+'" y="'+(y+.5)+'" width="'+(w2-1)+'" height="'+(h-1)+'" style="fill:none;stroke:'+v('grid')+'"/>';
        if(o2.cross!==false)s+='<path d="M'+(x+w2/2)+' '+y+'V'+(y+h)+'M'+x+' '+(y+h/2)+'H'+(x+w2)+'" style="fill:none;stroke:'+v('grid')+'"/>';
        g(s);
        var Q=pts.map(function(p){return n(p[0])+','+n(p[1]);}).join(' '), ins=o2.border!==false?1:0, cid='lkc'+(++uid);
        return g('<clipPath id="'+cid+'"><rect x="'+(x+ins)+'" y="'+(y+ins)+'" width="'+(w2-2*ins)+'" height="'+(h-2*ins)+'"/></clipPath>'+
          '<polyline clip-path="url(#'+cid+')" points="'+Q+'" style="fill:none;stroke:'+v(o2.color||'teal')+';stroke-width:1.5;stroke-linejoin:round;stroke-linecap:round"/>');
      },
      freqGrid:function(x,y,w2,h,lo,hi,marks){
        lo=lo||20;hi=hi||20000;marks=marks||[[100,'100'],[1000,'1k'],[10000,'10k']];
        var dec=Math.log10(hi/lo), last=-1e9, s='';
        marks.forEach(function(m){var gx=Math.round(x+w2*Math.log10(m[0]/lo)/dec)+.5;s+='<path d="M'+gx+' '+y+'V'+(y+h)+'" style="stroke:'+v('grid')+'"/>';});
        g(s);
        marks.forEach(function(m){
          var gx=Math.round(x+w2*Math.log10(m[0]/lo)/dec), tw=width(m[1]);
          var left=(gx+3+tw<=x+w2-2)?gx+3:gx-3-tw;
          if(left<last+4)return;text(left,y+h-11,m[1],{color:'text-axis'});last=left+tw;
        });
        return api;
      },
      led:function(cx,cy,on,c){return g('<circle cx="'+cx+'" cy="'+cy+'" r="2.5" style="fill:'+v(on?(c||'led-on'):'led-off')+'"/>');},
      handle:function(cx,cy){return g('<circle cx="'+cx+'" cy="'+cy+'" r="5.75" style="fill:'+v('display')+';stroke:'+v('orange')+';stroke-width:1.5"/>');},
      meter:function(m){
        var x=m.x,y=m.y,h=m.h,DB=36,GRDB=57;
        function frac(d){return Math.max(0,Math.min(1,1+d/DB));}
        rect(x,y,11,h,'display',{border:'grid'});
        var sep=y+16, by=sep+1, bh=h-16-2;
        if(m.gr!=null){
          rect(x+1,sep,9,1,'grid');
          rect(x+1,by,9,Math.max(1,Math.round(bh*Math.min(1,m.gr/GRDB))),'meter-gr');
        } else {
          var bars=m.stereo===false?[[x+1,9]]:[[x+1,4],[x+6,4]];
          bars.forEach(function(b,i){
            var pk=frac(m.peak-.4*i), rm=frac(m.rms-.4*i), gid='lkg'+Math.random().toString(36).slice(2);
            rect(b[0],sep,b[1],1,'grid');
            g('<defs><linearGradient id="'+gid+'" x1="0" y1="1" x2="0" y2="0"><stop offset=".72" style="stop-color:'+v('meter-green')+'"/><stop offset=".86" style="stop-color:'+v('meter-yellow')+'"/><stop offset="1" style="stop-color:'+v('meter-red')+'"/></linearGradient></defs>'+
              '<rect x="'+b[0]+'" y="'+by+'" width="'+b[1]+'" height="'+bh+'" fill="url(#'+gid+')"/>');
            rect(b[0],by,b[1],bh*(1-pk),'display');
            var dimTop=by+bh*(1-pk), dimTo=by+bh*(1-rm);
            if(m.dimAbove!=null)dimTo=Math.max(dimTo,by+bh*(1-frac(m.dimAbove)));
            if(dimTo>dimTop)rect(b[0],dimTop,b[1],dimTo-dimTop,'display',{opacity:.45});
            rect(b[0],Math.round(by+bh*(1-pk)),b[1],1,'meter-hold');
          });
        }
        if(m.marker!=null){var ty=by+bh*(1-frac(m.marker)),mx=x+12.5;g('<path d="M'+mx+' '+n(ty)+'L'+(mx+9.5)+' '+n(ty-5)+'V'+n(ty+5)+'Z" style="fill:'+v('text-dim')+'"/>');}
        if(m.label)text(x+5.5,y-11,m.label,{align:'center',color:'text-dim'});
        if(m.value)text(x+5.5,y+h+4,m.value,{align:'center',color:m.valueColor||'text-dim'});
        return api;
      },
      checkbox:function(x,y,sz,on,c){
        c=c||'orange';
        if(on)return rect(x,y,sz,sz,c);
        return g('<rect x="'+(x+.5)+'" y="'+(y+.5)+'" width="'+(sz-1)+'" height="'+(sz-1)+'" style="fill:none;stroke:'+v(c)+'"/>');
      },
      stepped:function(d){
        var n=d.steps.length,r=P.SIZE/2-P.SW/2,ringTop=d.cap+P.LABEL+10,cy=ringTop+P.SIZE/2+P.CY,cx=d.cx,s='';
        api.dial({cx:cx,cap:d.cap+10,v:d.index/(n-1),color:d.color});
        if(d.label)text(cx+P.LDX,d.cap,d.label,{align:'center'});
        d.steps.forEach(function(lab,i){
          var a=(-P.SPAN+2*P.SPAN*i/(n-1))*Math.PI/180,sn=Math.sin(a),cs=-Math.cos(a);
          s+='<line x1="'+n2(cx+sn*(r+2.5))+'" y1="'+n2(cy+cs*(r+2.5))+'" x2="'+n2(cx+sn*(r+4.5))+'" y2="'+n2(cy+cs*(r+4.5))+'" style="stroke:'+v('text')+'"/>';
          var tx=cx+sn*(r+8)+(sn>.3?3:sn<-.3?-3:0),ty=cy+cs*(r+8)-3.5;
          text(tx,ty,lab,{align:'center'});
        });
        return g(s);
      },
      icon:function(x,y,w2,h,url,ink){
        var d=document.createElement('div');
        d.style.cssText='position:absolute;left:'+x+'px;top:'+y+'px;width:'+w2+'px;height:'+h+'px;background:'+v(ink||'text')+';-webkit-mask:url('+url+') center/contain no-repeat;mask:url('+url+') center/contain no-repeat';
        dev.appendChild(d);return api;
      },
      fold:function(x,y,dir){
        dir=dir===true?'left':(dir===false||dir==null?'right':dir);
        var p={right:'M'+x+' '+y+'l6 3.5l-6 3.5z',left:'M'+(x+6)+' '+y+'l-6 3.5l6 3.5z',up:'M'+x+' '+(y+6.5)+'l3.5 -6.5l3.5 6.5z',down:'M'+x+' '+y+'h7l-3.5 6.5z'}[dir];
        return g('<path d="'+p+'" style="fill:'+v('text-dim')+'"/>');
      },
      roundButton:function(cx,cy,dir){
        var t=dir==='right'?'M'+(cx-2)+' '+(cy-3.5)+'l5 3.5l-5 3.5z':'M'+(cx-3.5)+' '+(cy-2)+'h7l-3.5 5z';
        return g('<circle cx="'+cx+'" cy="'+cy+'" r="6" style="fill:'+v('button-off')+';stroke:'+v('button-border')+'"/><path d="'+t+'" style="fill:'+v('text')+'"/>');
      },
      guide:function(y,label,color){g('<path d="M0 '+(y+.5)+'H'+w+'" style="stroke:'+v(color||'orange')+';stroke-opacity:.55"/>');if(label)text(w+4,y-1,label,{color:color||'orange'});return api;},
      vguide:function(x,label){g('<path d="M'+(x+.5)+' 0V169" style="stroke:'+v('orange')+';stroke-opacity:.55"/>');return api;}
    };
    return api;
  }
  window.LiveKit={device:device,textWidth:width,family:FAMILY,P:P,ref:REF};
})();

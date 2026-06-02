import streamlit.components.v1 as components

ANIMATION_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono:wght@400;500&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'DM Sans',sans-serif;
  background:#F4F6F7;padding:14px}
.top-bar{display:flex;align-items:center;
  gap:10px;margin-bottom:14px;flex-wrap:wrap}
button{padding:6px 14px;border-radius:8px;
  border:1px solid #D5DBDB;
  background:#fff;color:#0B2545;
  font-family:'DM Sans',sans-serif;
  font-size:13px;font-weight:500;cursor:pointer}
button:hover{background:#EBF5FB}
button.active{background:#FADBD8;
  color:#922B21;border-color:#F1948A}
.ctrl-group{display:flex;align-items:center;
  gap:8px;font-size:12px;color:#5D6D7E}
.ctrl-group input[type=range]{width:80px}
.metrics{display:grid;
  grid-template-columns:repeat(7,1fr);
  gap:6px;margin-bottom:12px}
.mc{background:#fff;border-radius:8px;
  padding:8px 10px;
  border-top:2.5px solid #2E86C1}
.mc.red{border-top-color:#C0392B}
.mc.green{border-top-color:#1A7A4A}
.mc.navy{border-top-color:#0B2545}
.ml{font-size:9px;font-weight:600;
  letter-spacing:.07em;text-transform:uppercase;
  color:#7F8C8D;margin-bottom:3px}
.mv{font-family:'DM Mono',monospace;
  font-size:18px;font-weight:500;color:#0D1B2A}
.flow{display:flex;align-items:flex-start;
  gap:0;margin-bottom:12px;overflow-x:auto}
.stage{display:flex;flex-direction:column;
  align-items:center;flex:1;min-width:0}
.sbox{width:100%;border:1px solid #D5DBDB;
  background:#fff;border-radius:12px;
  padding:8px 6px 10px;min-height:108px;
  display:flex;flex-direction:column;
  align-items:center;gap:3px}
.sbox.lit{border-color:#2E86C1;
  background:#EBF5FB}
.sn{font-size:10px;font-weight:600;
  color:#5D6D7E;text-transform:uppercase;
  letter-spacing:.05em;margin-bottom:3px;
  text-align:center}
.pa{display:flex;flex-wrap:wrap;
  justify-content:center;gap:4px;
  min-height:50px;align-content:flex-start}
.sc{font-size:10px;color:#95A5A6;
  margin-top:auto;padding-top:3px}
.arr{display:flex;align-items:center;
  justify-content:center;padding:0 3px;
  padding-top:34px;color:#BDC3C7;
  font-size:20px;flex-shrink:0}
.pd{width:24px;height:24px;border-radius:50%;
  display:flex;align-items:center;
  justify-content:center;font-size:8px;
  font-weight:600;cursor:pointer;
  transition:transform .12s;
  border:1.5px solid transparent;
  position:relative}
.pd:hover{transform:scale(1.3);z-index:9}
.pr{background:#f7c1c1;border-color:#e24b4a;
  color:#791f1f}
.py{background:#fac775;border-color:#ba7517;
  color:#633806}
.pg{background:#c0dd97;border-color:#639922;
  color:#27500a}
.pw{background:#F4F6F7;border-color:#95A5A6;
  color:#5D6D7E}
.pb{background:#2c3e50;border-color:#444;
  color:#F1EFE8}
.tip{display:none;position:fixed;
  background:#fff;border:1px solid #D5DBDB;
  border-radius:8px;padding:8px 10px;
  font-size:11px;z-index:99;
  pointer-events:none;min-width:110px;
  box-shadow:0 2px 8px rgba(0,0,0,.1)}
.tip.on{display:block}
.tr{display:flex;justify-content:space-between;
  gap:14px;margin-bottom:2px;color:#7F8C8D}
.tr span:last-child{color:#1C2833;
  font-weight:500}
.docs{display:grid;
  grid-template-columns:repeat(auto-fit,
    minmax(110px,1fr));
  gap:8px;margin-bottom:12px}
.dc{background:#fff;border:1px solid #D5DBDB;
  border-radius:10px;padding:10px 12px}
.dt{font-size:10px;font-weight:600;
  color:#7F8C8D;text-transform:uppercase;
  letter-spacing:.04em;margin-bottom:5px}
.dp{font-size:12px;font-weight:500;
  color:#0D1B2A;margin-bottom:3px;
  display:flex;align-items:center;gap:5px}
.busy{font-size:10px;color:#922B21;
  background:#FADBD8;padding:2px 7px;
  border-radius:99px;display:inline-block}
.free{font-size:10px;color:#1A7A4A;
  background:#D5F5E3;padding:2px 7px;
  border-radius:99px;display:inline-block}
.log{border:1px solid #E5E8E8;border-radius:8px;
  padding:8px 10px;max-height:80px;
  overflow-y:auto;background:#fff}
.le{font-size:10px;color:#7F8C8D;
  padding:1px 0;
  font-family:'DM Mono',monospace}
.sec{font-size:10px;font-weight:600;
  text-transform:uppercase;letter-spacing:.06em;
  color:#7F8C8D;margin:0 0 6px 0}
</style>
</head>
<body>
<div class="top-bar">
  <button id="btn" onclick="tog()">
    ▶ Start
  </button>
  <button onclick="rst()">↺ Reset</button>
  <div class="ctrl-group">
    Speed
    <input type="range" min="1" max="5"
      value="3" id="spd"
      oninput="setSp(this.value)">
    <span id="spv">3×</span>
  </div>
  <div class="ctrl-group">
    Doctors
    <input type="range" min="1" max="6"
      value="3" id="dsl"
      oninput="setDr(this.value)">
    <span id="drv">3</span>
  </div>
</div>

<div class="metrics">
  <div class="mc">
    <div class="ml">Queue</div>
    <div class="mv" id="mq">0</div>
  </div>
  <div class="mc">
    <div class="ml">Waiting</div>
    <div class="mv" id="mw">0</div>
  </div>
  <div class="mc green">
    <div class="ml">Treating</div>
    <div class="mv" id="mt">0</div>
  </div>
  <div class="mc green">
    <div class="ml">Done</div>
    <div class="mv" id="md">0</div>
  </div>
  <div class="mc">
    <div class="ml">Avg wait</div>
    <div class="mv" id="ma">—</div>
  </div>
  <div class="mc navy">
    <div class="ml">Util %</div>
    <div class="mv" id="mu">0%</div>
  </div>
  <div class="mc">
    <div class="ml">Time</div>
    <div class="mv" id="mm">0m</div>
  </div>
</div>

<div class="flow">
  <div class="stage">
    <div class="sbox" id="b-arr">
      <div class="sn">Arrival</div>
      <div class="pa" id="a-arr"></div>
      <div class="sc" id="c-arr">0</div>
    </div>
  </div>
  <div class="arr">›</div>
  <div class="stage">
    <div class="sbox" id="b-reg">
      <div class="sn">Registration</div>
      <div class="pa" id="a-reg"></div>
      <div class="sc" id="c-reg">0</div>
    </div>
  </div>
  <div class="arr">›</div>
  <div class="stage">
    <div class="sbox" id="b-tri">
      <div class="sn">Triage</div>
      <div class="pa" id="a-tri"></div>
      <div class="sc" id="c-tri">0</div>
    </div>
  </div>
  <div class="arr">›</div>
  <div class="stage" style="flex:1.4">
    <div class="sbox" id="b-que">
      <div class="sn">Priority Queue</div>
      <div class="pa" id="a-que"></div>
      <div class="sc" id="c-que">0</div>
    </div>
  </div>
  <div class="arr">›</div>
  <div class="stage" style="flex:1.4">
    <div class="sbox" id="b-trt">
      <div class="sn">Treatment</div>
      <div class="pa" id="a-trt"></div>
      <div class="sc" id="c-trt">0</div>
    </div>
  </div>
  <div class="arr">›</div>
  <div class="stage">
    <div class="sbox" id="b-ext">
      <div class="sn">Exit</div>
      <div class="pa" id="a-ext"></div>
      <div class="sc" id="c-ext">0</div>
    </div>
  </div>
</div>

<p class="sec">Doctor status</p>
<div class="docs" id="docs"></div>

<p class="sec">Event log</p>
<div class="log" id="log"></div>

<div class="tip" id="tip">
  <div class="tr">
    <span>ID</span>
    <span id="ti"></span>
  </div>
  <div class="tr">
    <span>Priority</span>
    <span id="tp"></span>
  </div>
  <div class="tr">
    <span>Stage</span>
    <span id="ts"></span>
  </div>
  <div class="tr">
    <span>Wait</span>
    <span id="tw"></span>
  </div>
</div>

<script>
const PRI=[
  {k:'red',   l:'Red',   c:'pr', w:5},
  {k:'yellow',l:'Yellow',c:'py', w:20},
  {k:'green', l:'Green', c:'pg', w:55},
  {k:'white', l:'White', c:'pw', w:19},
  {k:'black', l:'Black', c:'pb', w:1}
];
const ST_T={arr:[1,3],reg:[1,5],tri:[1,8]};
const TR_T={
  red:[45,180],yellow:[20,90],
  green:[10,45],white:[5,20],black:[0,0]
};
const DURATION = __DURATION__;
const STAGES=[
  'arr','reg','tri','que','trt','ext'
];
const SL={
  arr:'Arrival',reg:'Registration',
  tri:'Triage',que:'Queue',
  trt:'Treatment',ext:'Exit'
};
const PRO={red:1,yellow:2,green:3,white:4,black:5};

let pts=[],docs=[],nid=1,t=0,done=0;
let run=false,tmr=null,sp=3,nd=3;
let wts=[],arate=0.4;

function rnd(a,b){
  return Math.floor(Math.random()*(b-a+1))+a;
}
function wpick(){
  let r=Math.random()*100,s=0;
  for(let p of PRI){s+=p.w;if(r<s)return p;}
  return PRI[2];
}
function fmt(n){return Math.round(n);}

function initDocs(){
  docs=[];
  for(let i=0;i<nd;i++)
    docs.push({id:i+1,pat:null,tl:0});
  rdocs();
}

function rdocs(){
  const row=document.getElementById('docs');
  row.innerHTML='';
  for(let d of docs){
    const div=document.createElement('div');
    div.className='dc';
    const p=d.pat;
    div.innerHTML=`<div class="dt">
      Doctor ${d.id}</div>
      ${p
        ?`<div class="dp">
          <span class="pd ${p.pc}"
            style="width:16px;height:16px;
            font-size:7px">#${p.id}</span>
          Patient #${p.id}
          </div>
          <div class="busy">
            Busy · ${fmt(d.tl)}m left
          </div>`
        :`<div class="dp"
            style="color:#BDC3C7">—</div>
          <div class="free">Available</div>`
      }`;
    row.appendChild(div);
  }
}

function rstg(sk){
  const a=document.getElementById('a-'+sk);
  const c=document.getElementById('c-'+sk);
  const b=document.getElementById('b-'+sk);
  if(!a)return;
  const p=pts.filter(x=>x.stg===sk);
  a.innerHTML='';
  for(let pt of p){
    const d=document.createElement('div');
    d.className='pd '+pt.pc;
    d.textContent=pt.id;
    d.dataset.id=pt.id;
    d.addEventListener('mouseenter',
      e=>stip(e,pt));
    d.addEventListener('mouseleave',htip);
    a.appendChild(d);
  }
  c.textContent=p.length;
  b.classList.toggle('lit',p.length>0);
}

function rall(){
  for(let s of STAGES)rstg(s);
  rdocs();umets();
}

function umets(){
  const q=pts.filter(p=>p.stg==='que').length;
  const w=pts.filter(p=>
    ['arr','reg','tri','que']
    .includes(p.stg)).length;
  const tr=pts.filter(p=>p.stg==='trt').length;
  const bu=docs.filter(d=>d.pat).length;
  const u=nd>0?Math.round(bu/nd*100):0;
  const av=wts.length
    ?Math.round(wts.reduce((a,b)=>a+b,0)
      /wts.length):0;
  document.getElementById('mq').textContent=q;
  document.getElementById('mw').textContent=w;
  document.getElementById('mt').textContent=tr;
  document.getElementById('md').textContent=done;
  document.getElementById('ma').textContent
    =wts.length?av+'m':'—';
  document.getElementById('mu').textContent
    =u+'%';
  document.getElementById('mm').textContent
    =fmt(t)+'m';
}

function lg(msg){
  const w=document.getElementById('log');
  const e=document.createElement('div');
  e.className='le';
  e.textContent=`[t=${fmt(t)}m] ${msg}`;
  w.insertBefore(e,w.firstChild);
  while(w.children.length>40)
    w.removeChild(w.lastChild);
}

function stip(e,p){
  const tp=document.getElementById('tip');
  document.getElementById('ti').textContent
    ='#'+p.id;
  document.getElementById('tp').textContent
    =p.pl;
  document.getElementById('ts').textContent
    =SL[p.stg];
  const w=p.ts>0
    ?p.ts-p.at:t-p.at;
  document.getElementById('tw').textContent
    =fmt(w)+'m';
  tp.style.left=(e.clientX+12)+'px';
  tp.style.top=(e.clientY-10)+'px';
  tp.classList.add('on');
}
function htip(){
  document.getElementById('tip')
    .classList.remove('on');
}

function spawn(){
  const pr=wpick();
  const p={
    id:nid++,pc:pr.c,pl:pr.l,pk:pr.k,
    stg:'arr',at:t,ts:0,
    st:rnd(...ST_T.arr)
  };
  pts.push(p);
  lg(`Patient #${p.id} arrived (${pr.l})`);
  if(pr.k==='black'){
    setTimeout(()=>{
      p.stg='ext';
      lg(`#${p.id} DOA — exit`);
      done++;rall();
    },300);
  }
}

function tick(){
  if (t >= DURATION) {
    if (run) {
      clearInterval(tmr);
      run = false;
      const btn = document.getElementById('btn');
      btn.textContent = '🏁 Finished';
      btn.classList.remove('active');
      btn.disabled = true;
      lg('Simulation completed (' + DURATION + 'm reached).');
    }
    return;
  }
  const dt=0.5;
  t+=dt;
  if(Math.random()<arate*dt)spawn();

  for(let p of pts.filter(x=>
    ['arr','reg','tri'].includes(x.stg))){
    p.st-=dt;
    if(p.st<=0){
      const nx={
        arr:'reg',reg:'tri',tri:'que'
      }[p.stg];
      if(nx==='que'){
        p.qe=t;
        lg(`#${p.id} (${p.pl}) queued`);
      }
      p.stg=nx;
      if(nx==='reg')p.st=rnd(...ST_T.reg);
      else if(nx==='tri')
        p.st=rnd(...ST_T.tri);
    }
  }

  for(let d of docs){
    if(d.pat){
      d.tl-=dt;
      if(d.tl<=0){
        const p=d.pat;
        wts.push(p.ts-p.at);
        p.stg='ext';done++;
        lg(`#${p.id} done — exit`);
        d.pat=null;
        setTimeout(()=>{
          pts=pts.filter(x=>x.id!==p.id);
          rall();
        },1200);
      }
    }
  }

  const qs=pts.filter(p=>p.stg==='que')
    .sort((a,b)=>PRO[a.pk]-PRO[b.pk]);
  for(let d of docs){
    if(!d.pat&&qs.length){
      const p=qs.shift();
      p.stg='trt';
      p.ts=t;
      const tt=rnd(...TR_T[p.pk]);
      d.pat=p;d.tl=tt;
      lg(`Dr.${d.id} treating #${p.id}`
        +` (${p.pl}) · ${tt}m`);
    }
  }
  rall();
}

function tog(){
  const btn=document.getElementById('btn');
  if(run){
    clearInterval(tmr);run=false;
    btn.textContent='▶ Start';
    btn.classList.remove('active');
  } else {
    const iv=Math.max(50,400/sp);
    tmr=setInterval(tick,iv);
    run=true;
    btn.textContent='⏸ Pause';
    btn.classList.add('active');
  }
}

function rst(){
  clearInterval(tmr);run=false;
  pts=[];nid=1;t=0;done=0;wts=[];
  document.getElementById('btn')
    .textContent='▶ Start';
  document.getElementById('btn').disabled = false;
  document.getElementById('btn')
    .classList.remove('active');
  initDocs();rall();
  lg('Simulation reset.');
}

function setSp(v){
  sp=+v;
  document.getElementById('spv')
    .textContent=v+'×';
  if(run){
    clearInterval(tmr);
    tmr=setInterval(tick,Math.max(50,400/sp));
  }
}

function setDr(v){
  nd=+v;
  document.getElementById('drv').textContent=v;
  initDocs();
  lg(`Doctors changed to ${v}.`);
}

initDocs();rall();
lg('Ready. Click Start.');
</script>
</body>
</html>
"""


def render_animation(duration: int = 480, height: int = 680):
    html_content = ANIMATION_HTML.replace("__DURATION__", str(duration))
    components.html(
        html_content,
        height=height,
        scrolling=False
    )

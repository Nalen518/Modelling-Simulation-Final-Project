import streamlit.components.v1 as components

ANIMATION_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

.material-symbols-outlined {
  font-family: 'Material Symbols Outlined' !important;
  font-weight: normal; font-style: normal; font-size: 24px;
  line-height: 1; letter-spacing: normal; text-transform: none;
  display: inline-block; white-space: nowrap; direction: ltr;
  -webkit-font-smoothing: antialiased;
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
  vertical-align: middle;
}

*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',sans-serif;background:#0f1418;color:#dee3e8;padding:14px 16px}

/* ── Controls ── */
.controls{display:flex;align-items:center;gap:10px;margin-bottom:12px;flex-wrap:wrap}
.controls button{padding:5px 14px;border-radius:8px;border:1px solid #3e484f;
  background:#252b2e;color:#dee3e8;font-family:'Inter',sans-serif;
  font-size:12px;font-weight:600;cursor:pointer;transition:all .2s;
  display:flex;align-items:center;gap:4px}
.controls button:hover{background:#303539;border-color:#8ed5ff}
.controls button:disabled{opacity:.5;cursor:not-allowed}
.controls button.active{background:rgba(142,213,255,.15);color:#8ed5ff;border-color:#8ed5ff}
.ctrl-group{display:flex;align-items:center;gap:6px;font-size:12px;color:#bdc8d1}
.ctrl-group input[type=range]{width:72px;-webkit-appearance:none;background:transparent}
.ctrl-group input[type=range]::-webkit-slider-runnable-track{height:3px;background:#3e484f;border-radius:2px}
.ctrl-group input[type=range]::-webkit-slider-thumb{height:13px;width:13px;border-radius:50%;
  background:#8ed5ff;-webkit-appearance:none;margin-top:-5px;box-shadow:0 0 6px rgba(142,213,255,.4)}
.badge{padding:3px 9px;border-radius:6px;font-size:10px;font-weight:700;
  text-transform:uppercase;letter-spacing:.04em;display:inline-flex;align-items:center;gap:4px}
.badge.not-started{background:#303539;color:#bdc8d1}
.badge.running{background:rgba(74,222,128,.15);color:#4ade80}
.badge.paused{background:rgba(250,204,21,.15);color:#facc15}
.badge.completed{background:rgba(142,213,255,.15);color:#8ed5ff}
.live-dot{width:5px;height:5px;border-radius:50%;background:#ef4444;animation:pulse 1.5s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
.live-badge{display:inline-flex;align-items:center;gap:4px;font-size:9px;
  background:rgba(239,68,68,.18);color:#f87171;padding:2px 7px;border-radius:99px;font-weight:700}

/* ── KPI Cards ── */
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:12px}
.kpi-card{background:#252b2e;padding:12px 14px;border-radius:12px;
  border:1px solid #3e484f;overflow:hidden}
.kpi-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px}
.kpi-icon{font-size:26px!important}
.kpi-right{text-align:right}
.kpi-label{font-size:9px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#bdc8d1}
.kpi-value{font-family:'Inter',sans-serif;font-size:28px;font-weight:700;color:#dee3e8;
  letter-spacing:-.02em;line-height:1.1}
.kpi-value .unit{font-size:14px;color:#bdc8d1;margin-left:1px;font-weight:600}
.kpi-sub{font-size:10px;font-weight:600;color:#bdc8d1;text-align:right}
.sparkline{display:flex;align-items:flex-end;gap:2px;height:22px;margin-top:4px}
.sparkline .bar{flex:1;border-radius:2px 2px 0 0;transition:height .3s;min-height:2px}

/* ── Flow Card ── */
.flow-card{background:#1b2024;padding:14px 16px;border-radius:12px;
  border:1px solid #3e484f;margin-bottom:12px}
.flow-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.flow-label{font-size:10px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;
  color:#bdc8d1;display:flex;align-items:center;gap:8px}
.flow-time{font-size:12px;color:#bdc8d1}
.flow-time .val{color:#8ed5ff;font-weight:700}

.flow-row{display:flex;align-items:center;justify-content:space-between;padding:8px 0}
.station{display:flex;flex-direction:column;align-items:center;gap:6px;flex:1;min-width:0}
.station-icon{width:50px;height:50px;border-radius:12px;background:#303539;
  display:flex;align-items:center;justify-content:center;border:1px solid #3e484f;
  position:relative;transition:all .2s}
.station-icon.active{border-color:#8ed5ff;background:rgba(142,213,255,.06)}
.station-icon .material-symbols-outlined{font-size:24px!important;color:#dee3e8}
.station-badge{position:absolute;top:-7px;right:-7px;min-width:20px;height:20px;
  border-radius:99px;font-size:9px;font-weight:700;display:flex;align-items:center;
  justify-content:center;padding:0 4px;color:#0f1418;font-family:'JetBrains Mono',monospace}
.station-badge.primary{background:#8ed5ff}
.station-badge.tertiary{background:#ffc176;color:#472a00}
.station-badge.green{background:#4ade80}
.station-badge.red{background:#f87171}
.station-name{font-size:9px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:#bdc8d1}
.station-label{font-size:12px;font-weight:700;color:#dee3e8}
.station-stat{font-size:9px;font-weight:700;padding:2px 7px;border-radius:4px}
.station-stat.green{background:rgba(74,222,128,.1);color:#4ade80}
.station-stat.primary{color:#8ed5ff}
.station-stat.secondary{color:#c0c1ff}
.station-stat.muted{color:#bdc8d1}
.triage-dots{display:flex;gap:3px;justify-content:center}
.triage-dots .dot{width:6px;height:6px;border-radius:50%}
.flow-arrow{color:#3e484f;font-size:18px!important;flex-shrink:0;margin:0 2px}

/* ── Bottom Grid ── */
.bottom-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:8px}
.panel{background:#1b2024;padding:12px 14px;border-radius:12px;border:1px solid #3e484f}
.panel-header{display:flex;align-items:center;gap:6px;margin-bottom:10px}
.panel-header .material-symbols-outlined{color:#8ed5ff;font-size:18px!important}
.panel-header h3{font-size:10px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#bdc8d1}
.stat-row{display:flex;justify-content:space-between;align-items:center;padding:6px 0;
  border-bottom:1px solid #303539}
.stat-row:last-child{border-bottom:none}
.stat-row .label{font-size:12px;color:#bdc8d1}
.stat-row .value{font-family:'JetBrains Mono',monospace;font-size:14px;font-weight:600}
.stat-row .value.primary{color:#8ed5ff}
.stat-row .value.tertiary{color:#ffc176}
.stat-row .value.error{color:#f87171}
.stat-row .value.green{color:#4ade80}
.stat-row .value.white{color:#dee3e8}

.histogram{display:flex;align-items:flex-end;justify-content:space-between;height:100px;gap:3px;padding:0 2px}
.histogram .hbar{flex:1;border-radius:2px 2px 0 0;transition:height .4s,background .2s;
  min-height:2px;cursor:pointer}
.histogram .hbar:hover{background:#8ed5ff!important}
.histogram-labels{display:flex;justify-content:space-between;margin-top:4px;
  font-family:'JetBrains Mono',monospace;font-size:9px;color:#bdc8d1}

.eff-box{margin-top:10px;padding:8px 12px;background:#303539;border-radius:8px;
  border:1px solid #3e484f;display:flex;align-items:center;justify-content:space-between}
.eff-box .lbl{font-size:12px;font-weight:700;color:#dee3e8}
.eff-box .val{font-family:'Inter',sans-serif;font-size:20px;font-weight:700;color:#8ed5ff}

/* ── Event Log ── */
.log-section{margin-top:4px}
.log-header{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;
  color:#8ed5ff;margin-bottom:4px;display:flex;align-items:center;gap:5px}
.log-header .material-symbols-outlined{font-size:14px!important}
.log{background:#0a0f12;border:1px solid #3e484f;border-radius:8px;
  padding:6px 8px;max-height:64px;overflow-y:auto}
.le{font-size:10px;color:#bdc8d1;padding:1px 0;font-family:'JetBrains Mono',monospace}

/* ── Tooltip ── */
.tip{display:none;position:fixed;background:#252b2e;border:1px solid #3e484f;
  border-radius:8px;padding:8px 12px;font-size:11px;z-index:99;pointer-events:none;
  min-width:130px;box-shadow:0 4px 16px rgba(0,0,0,.4);color:#dee3e8}
.tip.on{display:block}
.tr{display:flex;justify-content:space-between;gap:16px;margin-bottom:3px;color:#bdc8d1}
.tr span:last-child{color:#dee3e8;font-weight:600}

::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:#3e484f;border-radius:10px}
</style>
</head>
<body>

<!-- Controls -->
<div class="controls">
  <button id="btn" onclick="tog()">▶ Start</button>
  <button onclick="rst()">↺ Reset</button>
  <div class="ctrl-group">
    Speed
    <input type="range" min="1" max="10" value="3" id="spd" oninput="setSp(this.value)">
    <span id="spv">3×</span>
  </div>
  <div class="ctrl-group" style="margin-left:auto;">
    <span class="live-badge"><span class="live-dot"></span>LIVE</span>
    Status: <span id="badge" class="badge not-started">Not Started</span>
  </div>
</div>

<!-- KPI Cards -->
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-header">
      <span class="material-symbols-outlined kpi-icon" style="color:#8ed5ff;">groups</span>
      <div class="kpi-right">
        <div class="kpi-label">TOTAL ARRIVALS</div>
        <div class="kpi-value" id="mtot">0</div>
      </div>
    </div>
    <div class="kpi-sub" id="kpi-sub-arr">arrived</div>
    <div class="sparkline" id="spark-arr"></div>
  </div>
  <div class="kpi-card">
    <div class="kpi-header">
      <span class="material-symbols-outlined kpi-icon" style="color:#ffc176;">schedule</span>
      <div class="kpi-right">
        <div class="kpi-label">AVG WAIT TIME</div>
        <div class="kpi-value" id="ma">—</div>
      </div>
    </div>
    <div class="kpi-sub" id="kpi-sub-wait">minutes</div>
    <div class="sparkline" id="spark-wait"></div>
  </div>
  <div class="kpi-card">
    <div class="kpi-header">
      <span class="material-symbols-outlined kpi-icon" style="color:#4ade80;">stethoscope</span>
      <div class="kpi-right">
        <div class="kpi-label">STAFF UTILIZATION</div>
        <div class="kpi-value" id="mu">0<span class="unit">%</span></div>
      </div>
    </div>
    <div class="kpi-sub" id="kpi-sub-util">doctor busy</div>
    <div class="sparkline" id="spark-util"></div>
  </div>
  <div class="kpi-card">
    <div class="kpi-header">
      <span class="material-symbols-outlined kpi-icon" style="color:#c0c1ff;">check_circle</span>
      <div class="kpi-right">
        <div class="kpi-label">COMPLETED CARE</div>
        <div class="kpi-value" id="md">0</div>
      </div>
    </div>
    <div class="kpi-sub" id="kpi-sub-done"></div>
  </div>
</div>

<!-- Flow Visualization -->
<div class="flow-card">
  <div class="flow-header">
    <div class="flow-label">
      LIVE PATIENT FLOW
      <span class="live-badge"><span class="live-dot"></span>LIVE</span>
    </div>
    <div class="flow-time">
      Simulation Time: <span class="val" id="mm">0 min</span>
      (<span id="spv2">3</span>×)
    </div>
  </div>
  <div class="flow-row">
    <div class="station">
      <div class="station-icon" id="si-arr">
        <span class="material-symbols-outlined">door_front</span>
      </div>
      <div style="text-align:center"><div class="station-name">Arrival</div><div class="station-label">Outside ER</div></div>
      <div class="station-stat green" id="sc-arr">In Last Hour: 0</div>
    </div>
    <span class="material-symbols-outlined flow-arrow">arrow_forward</span>
    <div class="station">
      <div class="station-icon" id="si-reg">
        <span class="material-symbols-outlined">person_search</span>
        <div class="station-badge primary" id="sb-reg" style="display:none">0</div>
      </div>
      <div style="text-align:center"><div class="station-name">Registration</div><div class="station-label">Counter</div></div>
      <div class="station-stat primary" id="sc-reg">Waiting: 0</div>
    </div>
    <span class="material-symbols-outlined flow-arrow">arrow_forward</span>
    <div class="station">
      <div class="station-icon" id="si-tri">
        <span class="material-symbols-outlined">assignment_ind</span>
        <div class="station-badge tertiary" id="sb-tri" style="display:none">0</div>
      </div>
      <div style="text-align:center"><div class="station-name">Triage</div><div class="station-label">Nurse Station</div></div>
      <div class="triage-dots" id="td-tri"></div>
    </div>
    <span class="material-symbols-outlined flow-arrow">arrow_forward</span>
    <div class="station">
      <div class="station-icon" id="si-trt">
        <span class="material-symbols-outlined">medical_services</span>
        <div class="station-badge green" id="sb-trt">0</div>
      </div>
      <div style="text-align:center"><div class="station-name">Doctor</div><div class="station-label" id="sl-trt">Treatment (0)</div></div>
      <div class="station-stat muted" id="sc-trt">In Treatment: 0</div>
    </div>
    <span class="material-symbols-outlined flow-arrow">arrow_forward</span>
    <div class="station">
      <div class="station-icon" id="si-ext">
        <span class="material-symbols-outlined">logout</span>
      </div>
      <div style="text-align:center"><div class="station-name">Discharge</div><div class="station-label">Exit</div></div>
      <div class="station-stat secondary" id="sc-ext">Total: 0</div>
    </div>
  </div>
</div>

<!-- Bottom Analytics Grid -->
<div class="bottom-grid">
  <div class="panel">
    <div class="panel-header">
      <span class="material-symbols-outlined">analytics</span>
      <h3>Queue Summary</h3>
    </div>
    <div class="stat-row"><span class="label">Patients Waiting (Total)</span><span class="value tertiary" id="qs-waiting">0</span></div>
    <div class="stat-row"><span class="label">Patients in Treatment</span><span class="value primary" id="qs-treating">0</span></div>
    <div class="stat-row"><span class="label">Max Queue Length</span><span class="value error" id="qs-maxq">0</span></div>
    <div class="stat-row"><span class="label">Current Time</span><span class="value white" id="qs-time">0 min</span></div>
  </div>
  <div class="panel">
    <div class="panel-header">
      <span class="material-symbols-outlined">bar_chart</span>
      <h3>Waiting Time Distribution</h3>
    </div>
    <div class="histogram" id="histo"></div>
    <div class="histogram-labels"><span>0m</span><span>15m</span><span>30m</span><span>45m</span><span>60m+</span></div>
  </div>
  <div class="panel">
    <div class="panel-header">
      <span class="material-symbols-outlined">speed</span>
      <h3>System Performance</h3>
    </div>
    <div class="stat-row"><span class="label">Throughput (pts/hr)</span><span class="value green" id="sp-tput">0</span></div>
    <div class="stat-row"><span class="label">Avg Time in System (min)</span><span class="value tertiary" id="sp-avgtime">—</span></div>
    <div class="stat-row"><span class="label">P(Wait > 30 min)</span><span class="value error" id="sp-pwait">0%</span></div>
    <div class="eff-box"><span class="lbl">Completion Rate</span><span class="val" id="sp-eff">0%</span></div>
  </div>
</div>

<!-- Event Log -->
<div class="log-section">
  <div class="log-header">
    <span class="material-symbols-outlined">terminal</span>Event Log
  </div>
  <div class="log" id="log"></div>
</div>

<!-- Tooltip -->
<div class="tip" id="tip">
  <div class="tr"><span>ID</span><span id="ti"></span></div>
  <div class="tr"><span>Priority</span><span id="tp"></span></div>
  <div class="tr"><span>Stage</span><span id="ts"></span></div>
  <div class="tr"><span>Wait</span><span id="tw"></span></div>
</div>

<script>
const PRI_MAP={1:{k:'red',l:'Red',c:'pr'},2:{k:'yellow',l:'Yellow',c:'py'},
  3:{k:'green',l:'Green',c:'pg'},4:{k:'white',l:'White',c:'pw'},5:{k:'black',l:'Black',c:'pb'}};
const PATIENTS=__PATIENTS_JSON__;
const N_DOCTORS=__N_DOCTORS__;
const DURATION=__DURATION__;
const SL={arr:'Arrival',reg:'Registration',tri:'Triage',que:'Queue',trt:'Treatment',ext:'Exit'};
const DOT_COLORS={1:'#f87171',2:'#ffc176',3:'#4ade80',4:'#bdc8d1',5:'#3e484f'};

let pts=[],docs=[],t=0,state='Not Started';
let run=false,tmr=null,sp=3;
let maxQueueSeen=0;
let sparkArr=[0,0,0,0,0,0,0,0];
let sparkWait=[0,0,0,0,0,0,0,0];
let sparkUtil=[0,0,0,0,0,0,0,0];
let lastSparkT=0;
let loggedEvents={};

if(window.__activeTimer__){clearInterval(window.__activeTimer__);window.__activeTimer__=null;}

function clearActiveTimer(){
  if(tmr){clearInterval(tmr);tmr=null;}
  if(window.__activeTimer__){clearInterval(window.__activeTimer__);window.__activeTimer__=null;}
}

function fmt(n){return Math.round(n);}

function initDocs(){
  docs=[];
  for(let i=0;i<N_DOCTORS;i++) docs.push({id:i+1,pat:null,tl:0});
}

/* ── Station Rendering (replaces dot-based rstg) ── */
function toggleActive(id,on){
  const el=document.getElementById(id);
  if(on) el.classList.add('active'); else el.classList.remove('active');
}

function updateStations(){
  const arrPts=pts.filter(x=>x.stg==='arr');
  const regPts=pts.filter(x=>x.stg==='reg');
  const triPts=pts.filter(x=>x.stg==='tri');
  const quePts=pts.filter(x=>x.stg==='que');
  const trtPts=pts.filter(x=>x.stg==='trt');
  const extPts=pts.filter(x=>x.stg==='ext');

  // Arrival
  const lastHr=PATIENTS.filter(x=>x.arrival_time<=t&&x.arrival_time>=Math.max(0,t-60)).length;
  document.getElementById('sc-arr').textContent='In Last Hour: '+lastHr;
  toggleActive('si-arr',arrPts.length>0);

  // Registration
  const regBadge=document.getElementById('sb-reg');
  regBadge.textContent=regPts.length;
  regBadge.style.display=regPts.length>0?'flex':'none';
  document.getElementById('sc-reg').textContent='Waiting: '+regPts.length;
  toggleActive('si-reg',regPts.length>0);

  // Triage
  const triBadge=document.getElementById('sb-tri');
  triBadge.textContent=triPts.length;
  triBadge.style.display=triPts.length>0?'flex':'none';
  toggleActive('si-tri',triPts.length>0);
  // Triage color dots (showing priority distribution in triage + queue)
  const tdEl=document.getElementById('td-tri');
  tdEl.innerHTML='';
  const combined=[...triPts,...quePts];
  const priCounts={};
  combined.forEach(p=>{const pr=p.raw.priority;priCounts[pr]=(priCounts[pr]||0)+1;});
  for(const pri of [1,2,3,4,5]){
    if(priCounts[pri]){
      const cnt=Math.min(priCounts[pri],6);
      for(let i=0;i<cnt;i++){
        const d=document.createElement('div');
        d.className='dot';d.style.background=DOT_COLORS[pri];
        tdEl.appendChild(d);
      }
    }
  }

  // Doctor Treatment
  const trtCount=trtPts.length;
  const trtBadge=document.getElementById('sb-trt');
  trtBadge.textContent=trtCount+'/'+N_DOCTORS;
  if(trtCount>=N_DOCTORS) trtBadge.className='station-badge red';
  else if(trtCount>0) trtBadge.className='station-badge green';
  else trtBadge.className='station-badge primary';
  document.getElementById('sl-trt').textContent='Treatment ('+N_DOCTORS+')';
  document.getElementById('sc-trt').textContent='In Treatment: '+trtCount;
  toggleActive('si-trt',trtCount>0);

  // Exit
  document.getElementById('sc-ext').textContent='Total: '+extPts.length;
  toggleActive('si-ext',extPts.length>0);

  // Track max queue
  if(quePts.length>maxQueueSeen) maxQueueSeen=quePts.length;
}

/* ── Sparkline Renderer ── */
function renderSparkline(id,data,color){
  const el=document.getElementById(id);
  el.innerHTML='';
  const mx=Math.max(...data,1);
  const maxVal=Math.max(...data);
  data.forEach(v=>{
    const bar=document.createElement('div');
    bar.className='bar';
    bar.style.height=Math.max(2,(v/mx)*22)+'px';
    bar.style.background=(v===maxVal&&v>0)?color:(color+'33');
    el.appendChild(bar);
  });
}

/* ── Histogram Renderer ── */
function renderHistogram(){
  const el=document.getElementById('histo');
  el.innerHTML='';
  const done=PATIENTS.filter(p=>p.treatment_end>0&&t>=p.treatment_end&&p.priority!==5);
  const buckets=[0,0,0,0,0,0,0,0];
  done.forEach(p=>{
    const w=p.treatment_start-p.triage_end;
    buckets[Math.min(Math.floor(w/10),7)]++;
  });
  const mx=Math.max(...buckets,1);
  buckets.forEach(v=>{
    const bar=document.createElement('div');
    bar.className='hbar';
    bar.style.height=Math.max(2,(v/mx)*100)+'px';
    bar.style.background=(v===mx&&v>0)?'#8ed5ff':'rgba(142,213,255,0.2)';
    el.appendChild(bar);
  });
}

/* ── Metrics Update (PRESERVED CALCULATIONS) ── */
function umets(){
  const totalArrived=PATIENTS.filter(p=>p.arrival_time<=t).length;
  const completedPts=PATIENTS.filter(p=>p.treatment_end>0&&t>=p.treatment_end&&p.priority!==5);
  const doneCount=completedPts.length;
  const waitingCount=pts.filter(p=>['arr','reg','tri','que'].includes(p.stg)).length;
  const treatingCount=pts.filter(p=>p.stg==='trt').length;

  let avgWait=0,maxWait=0,avgWaitStr='—';
  if(doneCount>0){
    const totalWait=completedPts.reduce((s,p)=>s+(p.treatment_start-p.triage_end),0);
    avgWait=totalWait/doneCount;
    avgWaitStr=avgWait.toFixed(1);
    maxWait=Math.max(...completedPts.map(p=>p.treatment_start-p.triage_end));
  }

  let totalTreatmentTime=0;
  PATIENTS.forEach(p=>{
    if(p.treatment_end>0&&t>=p.treatment_end&&p.priority!==5)
      totalTreatmentTime+=(p.treatment_end-p.treatment_start);
  });
  const utilization=N_DOCTORS>0?(totalTreatmentTime/Math.max(t*N_DOCTORS,1))*100:0;

  // KPI cards
  document.getElementById('mtot').textContent=totalArrived;
  document.getElementById('ma').innerHTML=avgWaitStr==='—'?'—':avgWaitStr+'<span class="unit">m</span>';
  document.getElementById('mu').innerHTML=utilization.toFixed(1)+'<span class="unit">%</span>';
  document.getElementById('md').textContent=doneCount;

  // KPI subtexts
  document.getElementById('kpi-sub-arr').textContent='arrived';
  document.getElementById('kpi-sub-wait').textContent=doneCount>0?('max: '+maxWait.toFixed(1)+'m'):'minutes';
  document.getElementById('kpi-sub-util').textContent=treatingCount+'/'+N_DOCTORS+' doctors busy';
  const sr=totalArrived>0?((doneCount/totalArrived)*100).toFixed(1):'0';
  document.getElementById('kpi-sub-done').textContent=sr+'% Success Rate';

  // Flow time
  document.getElementById('mm').textContent=Math.round(t)+' min';
  document.getElementById('spv2').textContent=sp;

  // Queue Summary panel
  document.getElementById('qs-waiting').textContent=waitingCount;
  document.getElementById('qs-treating').textContent=treatingCount;
  document.getElementById('qs-maxq').textContent=maxQueueSeen;
  document.getElementById('qs-time').textContent=Math.round(t)+' min';

  // System Performance panel
  document.getElementById('sp-tput').textContent=t>0?(doneCount/(t/60)).toFixed(1):'0';
  if(doneCount>0){
    const avgSys=completedPts.reduce((s,p)=>s+(p.treatment_end-p.arrival_time),0)/doneCount;
    document.getElementById('sp-avgtime').textContent=avgSys.toFixed(1);
    const over30=completedPts.filter(p=>(p.treatment_start-p.triage_end)>30).length;
    document.getElementById('sp-pwait').textContent=((over30/doneCount)*100).toFixed(1)+'%';
  }else{
    document.getElementById('sp-avgtime').textContent='—';
    document.getElementById('sp-pwait').textContent='0%';
  }
  document.getElementById('sp-eff').textContent=(totalArrived>0?((doneCount/totalArrived)*100).toFixed(1):'0')+'%';

  // Sparklines (update every ~30 sim minutes)
  if(t-lastSparkT>=30||t===0){
    lastSparkT=t;
    sparkArr.push(totalArrived);sparkArr.shift();
    sparkWait.push(avgWait);sparkWait.shift();
    sparkUtil.push(utilization);sparkUtil.shift();
    renderSparkline('spark-arr',sparkArr,'#8ed5ff');
    renderSparkline('spark-wait',sparkWait,'#ffc176');
    renderSparkline('spark-util',sparkUtil,'#4ade80');
  }

  renderHistogram();
}

/* ── Event Log ── */
function lg(msg){
  const w=document.getElementById('log');
  const e=document.createElement('div');
  e.className='le';
  e.textContent='[t='+fmt(t)+'m] '+msg;
  w.insertBefore(e,w.firstChild);
  while(w.children.length>40)w.removeChild(w.lastChild);
}

function logStageChanges(){
  pts.forEach(p=>{
    const key=p.id+'-'+p.stg;
    if(!loggedEvents[key]){
      loggedEvents[key]=true;
      if(p.stg==='arr') lg('Patient #'+p.id+' ('+p.pl+') arrived at IGD.');
      else if(p.stg==='reg') lg('Patient #'+p.id+' started registration.');
      else if(p.stg==='tri') lg('Patient #'+p.id+' finished registration, starting triage.');
      else if(p.stg==='que') lg('Patient #'+p.id+' triaged to '+p.pl+' Priority Queue.');
      else if(p.stg==='trt'){
        const docId=p.raw.doctor_id;
        lg('Patient #'+p.id+' started treatment by Doctor '+docId+'.');
      }else if(p.stg==='ext'){
        if(p.raw.priority===5) lg('Patient #'+p.id+' declared DOA.');
        else lg('Patient #'+p.id+' completed treatment and exited IGD.');
      }
    }
  });
}

/* ── Stage Logic (PRESERVED EXACTLY) ── */
function getStage(p,t){
  if(t<p.arrival_time)return null;
  if(p.priority===5&&p.triage_end>0&&t>=p.triage_end)return'ext';
  if(p.treatment_end>0&&t>=p.treatment_end)return'ext';
  if(p.treatment_start>0&&t>=p.treatment_start)return'trt';
  if(p.triage_end>0&&t>=p.triage_end)return'que';
  if(p.registration_end>0&&t>=p.registration_end)return'tri';
  if(p.registration_start>0&&t>=p.registration_start)return'reg';
  return'arr';
}

/* ── Doctor Assignment (PRESERVED EXACTLY) ── */
function assignDoctorsToPatients(){
  const treatedPatients=PATIENTS.filter(p=>p.treatment_start>0)
    .sort((a,b)=>a.treatment_start-b.treatment_start);
  const doctorFreeTime=Array(N_DOCTORS+1).fill(0);
  treatedPatients.forEach(p=>{
    let assignedDoc=1;
    for(let d=1;d<=N_DOCTORS;d++){
      if(doctorFreeTime[d]<=p.treatment_start){assignedDoc=d;break;}
    }
    if(doctorFreeTime[assignedDoc]>p.treatment_start){
      let minTime=Infinity;
      for(let d=1;d<=N_DOCTORS;d++){
        if(doctorFreeTime[d]<minTime){minTime=doctorFreeTime[d];assignedDoc=d;}
      }
    }
    p.doctor_id=assignedDoc;
    doctorFreeTime[assignedDoc]=p.treatment_end>0?p.treatment_end:Infinity;
  });
}

/* ── Lifecycle State Machine (PRESERVED) ── */
function updateState(newState){
  state=newState;
  const badge=document.getElementById('badge');
  const btn=document.getElementById('btn');
  badge.textContent=state;
  badge.className='badge '+state.toLowerCase().replace(' ','-');
  if(state==='Not Started'){btn.textContent='▶ Start';btn.disabled=false;btn.classList.remove('active');run=false;}
  else if(state==='Running'){btn.textContent='⏸ Pause';btn.disabled=false;btn.classList.add('active');run=true;}
  else if(state==='Paused'){btn.textContent='▶ Resume';btn.disabled=false;btn.classList.remove('active');run=false;}
  else if(state==='Completed'){btn.textContent='🏁 Done';btn.disabled=true;btn.classList.remove('active');run=false;}
}

/* ── Frame Update (PRESERVED LOGIC) ── */
function updateFrame(){
  pts=[];
  PATIENTS.forEach(raw=>{
    const stg=getStage(raw,t);
    if(stg){
      const pmap=PRI_MAP[raw.priority]||PRI_MAP[4];
      pts.push({id:raw.id,pc:pmap.c,pl:pmap.l,pk:pmap.k,stg:stg,at:raw.arrival_time,ts:raw.treatment_start,raw:raw});
    }
  });
  docs.forEach(d=>{d.pat=null;d.tl=0;});
  pts.filter(p=>p.stg==='trt').forEach(p=>{
    const docId=p.raw.doctor_id;
    if(docId&&docId<=N_DOCTORS){
      docs[docId-1].pat=p;
      docs[docId-1].tl=p.raw.treatment_end>0?Math.max(0,p.raw.treatment_end-t):0;
    }
  });
  updateStations();
  umets();
  logStageChanges();
}

/* ── Tick / Playback (PRESERVED) ── */
function tick(){
  if(t>=DURATION){
    if(state==='Running'){clearActiveTimer();updateState('Completed');lg('Simulation completed ('+DURATION+'m reached).');}
    return;
  }
  t+=0.5;
  updateFrame();
}

function tog(){
  if(state==='Running'){clearActiveTimer();updateState('Paused');}
  else if(state==='Not Started'||state==='Paused'){
    const iv=Math.max(50,400/sp);
    tmr=setInterval(tick,iv);window.__activeTimer__=tmr;updateState('Running');
  }
}

function rst(){
  clearActiveTimer();t=0;maxQueueSeen=0;lastSparkT=0;
  sparkArr=[0,0,0,0,0,0,0,0];sparkWait=[0,0,0,0,0,0,0,0];sparkUtil=[0,0,0,0,0,0,0,0];
  loggedEvents={};
  updateState('Not Started');
  document.getElementById('log').innerHTML='';
  initDocs();assignDoctorsToPatients();updateFrame();
  lg('Simulation reset.');
}

function setSp(v){
  sp=+v;document.getElementById('spv').textContent=v+'×';
  if(state==='Running'){clearActiveTimer();tmr=setInterval(tick,Math.max(50,400/sp));window.__activeTimer__=tmr;}
}

/* ── Init ── */
assignDoctorsToPatients();
initDocs();
updateFrame();
lg('Ready. Click Start.');
</script>
</body>
</html>
"""


def render_animation(patients_json: str, n_doctors: int, duration: int = 480, height: int = 700):
    html_content = ANIMATION_HTML.replace("__DURATION__", str(duration))
    html_content = html_content.replace("__PATIENTS_JSON__", patients_json)
    html_content = html_content.replace("__N_DOCTORS__", str(n_doctors))

    import hashlib
    config_str = f"{patients_json}_{n_doctors}_{duration}"
    content_hash = hashlib.md5(config_str.encode("utf-8")).hexdigest()
    html_content = html_content.replace(
        "Ready. Click Start.",
        f"Ready. Click Start. <!-- run_hash: {content_hash} -->"
    )

    components.html(
        html_content,
        height=height,
        scrolling=True
    )

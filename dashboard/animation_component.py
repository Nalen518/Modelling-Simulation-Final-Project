import streamlit.components.v1 as components

ANIMATION_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Raleway',sans-serif;
  background:#0B132B;color:#F1F5F9;padding:14px}
.top-bar{display:flex;align-items:center;
  gap:12px;margin-bottom:14px;flex-wrap:wrap}
button{padding:6px 14px;border-radius:8px;
  border:1px solid #1E2D4A;
  background:#1C2541;color:#F1F5F9;
  font-family:'Raleway',sans-serif;
  font-size:13px;font-weight:600;cursor:pointer;
  transition:all 0.2s ease}
button:hover{background:#2A3547;border-color:#06B6D4}
button:disabled{opacity:0.5;cursor:not-allowed}
button.active{background:rgba(6, 182, 212, 0.15);
  color:#06B6D4;border-color:#06B6D4;
  box-shadow:0 0 8px rgba(6, 182, 212, 0.3)}
.ctrl-group{display:flex;align-items:center;
  gap:8px;font-size:12.5px;color:#94A3B8}
.ctrl-group input[type=range]{width:85px;accent-color:#06B6D4}
.badge{padding:4px 10px;border-radius:6px;
  font-size:10.5px;font-weight:700;text-transform:uppercase;
  letter-spacing:.05em;display:inline-block;
  font-family:'Raleway',sans-serif}
.badge.not-started{background:#1A233A;color:#94A3B8;border:1px solid #2A3547}
.badge.running{background:#0C2B1B;color:#86EFAC;border:1px solid #22C55E}
.badge.paused{background:#2B2211;color:#FDE047;border:1px solid #EAB308}
.badge.completed{background:#132238;color:#93C5FD;border:1px solid #3B82F6}

.metrics{display:grid;
  grid-template-columns:repeat(auto-fit, minmax(110px, 1fr));
  gap:8px;margin-bottom:14px}
.mc{background:#1C2541;border-radius:10px;
  padding:10px 12px;min-height:78px;
  border:1px solid #1E2D4A;
  border-top:3px solid #06B6D4;
  box-shadow:0 4px 12px rgba(0,0,0,0.25);
  display:flex;flex-direction:column;
  justify-content:space-between;
  transition:all 0.2s ease}
.mc:hover{transform:translateY(-2px);
  box-shadow:0 6px 16px rgba(0,0,0,0.35);
  border-color:#06B6D4}
.mc.red{border-top-color:#EF4444}
.mc.green{border-top-color:#10B981}
.mc.blue{border-top-color:#3B82F6}
.mc.amber{border-top-color:#F59E0B}
.ml{font-size:10px;font-weight:700;
  letter-spacing:.06em;text-transform:uppercase;
  color:#94A3B8;margin-bottom:4px;
  font-family:'Raleway',sans-serif}
.mv{font-family:'JetBrains Mono',monospace;
  font-size:20px;font-weight:600;color:#FFFFFF}

.flow-layout{display:flex;flex-direction:column;gap:12px;margin-bottom:14px}
.flow-row{display:flex;align-items:center;gap:0;width:100%}
.flow-cols{display:grid;grid-template-columns:1.2fr 1fr;gap:14px;width:100%;align-items:stretch}
.stage-col, .status-col{min-width:0}

.stage{display:flex;flex-direction:column;
  align-items:center;flex:1;min-width:0}
.sbox{width:100%;border:1px solid #1E2D4A;
  background:#1C2541;border-radius:12px;
  padding:10px 8px 12px;min-height:114px;
  display:flex;flex-direction:column;
  align-items:center;gap:4px;
  box-shadow:0 4px 10px rgba(0,0,0,0.2);
  transition:border-color 0.2s ease, background-color 0.2s ease}
.sbox.lit{border-color:#06B6D4;
  background:rgba(6,182,212,0.04)}
.sn{font-size:10.5px;font-weight:700;
  color:#94A3B8;text-transform:uppercase;
  letter-spacing:.06em;margin-bottom:6px;
  text-align:center;font-family:'Raleway',sans-serif;
  transition:color 0.2s ease}
.sbox.lit .sn{color:#06B6D4}
.pa{display:flex;flex-wrap:wrap;
  justify-content:center;gap:4px;
  min-height:50px;align-content:flex-start}
.sc{font-size:11px;color:#94A3B8;
  font-family:'JetBrains Mono',monospace;
  margin-top:auto;padding-top:4px;
  font-weight:600;transition:color 0.2s ease}
.sbox.lit .sc{color:#F1F5F9}
.arr{display:flex;align-items:center;
  justify-content:center;padding:0 4px;
  padding-top:38px;color:#3A506B;
  font-size:22px;flex-shrink:0}

.scrollable-queue{max-height:180px;height:180px;display:flex;flex-direction:column}
.scrollable-queue .pa{flex:1;overflow-y:auto;width:100%;padding:4px;display:flex;flex-wrap:wrap;justify-content:center;gap:4px;align-content:flex-start}
.doctor-status-container{max-height:180px;height:180px;display:flex;flex-direction:column}
.docs-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px;width:100%;overflow-y:auto;flex:1;padding:4px}
.docs-grid .dc{background:#1C2541;border:1px solid #1E2D4A;border-radius:10px;padding:8px 10px;box-shadow:0 2px 6px rgba(0,0,0,0.15)}

.pd{width:24px;height:24px;border-radius:50%;
  display:flex;align-items:center;
  justify-content:center;font-size:8.5px;
  font-weight:700;cursor:pointer;
  transition:transform .15s, box-shadow .15s;
  border:1.5px solid transparent;
  position:relative;
  font-family:'JetBrains Mono',monospace}
.pd:hover{transform:scale(1.3);z-index:9;
  box-shadow:0 0 10px rgba(255,255,255,0.25)}
.pr{background:#f7c1c1;border-color:#e24b4a;color:#791f1f}
.py{background:#fac775;border-color:#ba7517;color:#633806}
.pg{background:#c0dd97;border-color:#639922;color:#27500a}
.pw{background:#2A3547;border-color:#95A5A6;color:#FFFFFF}
.pb{background:#1C2541;border-color:#475569;color:#F1F5F9}

.tip{display:none;position:fixed;
  background:#1C2541;border:1px solid #1E2D4A;
  border-radius:8px;padding:8px 12px;
  font-size:11px;z-index:99;
  pointer-events:none;min-width:120px;
  box-shadow:0 4px 16px rgba(0,0,0,0.35);
  color:#F1F5F9}
.tip.on{display:block}
.tr{display:flex;justify-content:space-between;
  gap:16px;margin-bottom:4px;color:#94A3B8}
.tr span:last-child{color:#F1F5F9;
  font-weight:600}

.dt{font-size:10px;font-weight:700;
  color:#94A3B8;text-transform:uppercase;
  letter-spacing:.04em;margin-bottom:6px}
.dp{font-size:12px;font-weight:600;
  color:#F1F5F9;margin-bottom:5px;
  display:flex;align-items:center;gap:6px}
.busy{font-size:10px;color:#FCA5A5;
  background:#371318;border:1px solid #EF4444;
  padding:2px 8px;border-radius:99px;display:inline-block}
.free{font-size:10px;color:#86EFAC;
  background:#0C2B1B;border:1px solid #22C55E;
  padding:2px 8px;border-radius:99px;display:inline-block}

.log{border:1px solid #1E2D4A;border-radius:8px;
  padding:8px 10px;max-height:80px;
  overflow-y:auto;background:#080D1A}
.le{font-size:10.5px;color:#94A3B8;
  padding:2px 0;
  font-family:'JetBrains Mono',monospace}
.sec{font-size:11px;font-weight:700;
  text-transform:uppercase;letter-spacing:.06em;
  color:#06B6D4;margin:12px 0 6px 0;
  font-family:'Raleway',sans-serif}

::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:#0B132B}
::-webkit-scrollbar-thumb{background:#1C2541;border-radius:3px;border:1px solid #1E2D4A}
::-webkit-scrollbar-thumb:hover{background:#2A3547}
</style>
</head>
<body>
<div class="top-bar">
  <button id="btn" onclick="tog()">▶ Start</button>
  <button onclick="rst()">↺ Reset</button>
  <div class="ctrl-group">
    Speed
    <input type="range" min="1" max="10"
      value="3" id="spd"
      oninput="setSp(this.value)">
    <span id="spv">3×</span>
  </div>
  <div class="ctrl-group" style="margin-left:auto;">
    Status: <span id="badge" class="badge not-started">Not Started</span>
  </div>
</div>

<div class="metrics">
  <div class="mc">
    <div class="ml">Total Patients</div>
    <div class="mv" id="mtot">0</div>
  </div>
  <div class="mc red">
    <div class="ml">Priority Queue Length</div>
    <div class="mv" id="mq">0</div>
  </div>
  <div class="mc amber">
    <div class="ml">Total Patients Waiting</div>
    <div class="mv" id="mw">0</div>
  </div>
  <div class="mc blue">
    <div class="ml">Patients Treating</div>
    <div class="mv" id="mt">0</div>
  </div>
  <div class="mc green">
    <div class="ml">Completed Patients</div>
    <div class="mv" id="md">0</div>
  </div>
  <div class="mc">
    <div class="ml">Average Wait</div>
    <div class="mv" id="ma">—</div>
  </div>
  <div class="mc">
    <div class="ml">Max Wait</div>
    <div class="mv" id="mmax">—</div>
  </div>
  <div class="mc blue">
    <div class="ml">Doctor Utilization</div>
    <div class="mv" id="mu">0%</div>
  </div>
  <div class="mc">
    <div class="ml">Simulation Time</div>
    <div class="mv" id="mm">0m</div>
  </div>
</div>

<div class="flow-layout">
  <!-- Row 1: Pre-queue stages -->
  <div class="flow-row">
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
  </div>

  <!-- Row 2: Two-column layout (Queue vs Doctor Status) -->
  <div class="flow-cols">
    <div class="stage-col">
      <div class="sbox scrollable-queue" id="b-que">
        <div class="sn">Priority Queue</div>
        <div class="pa" id="a-que"></div>
        <div class="sc" id="c-que">0</div>
      </div>
    </div>
    <div class="status-col">
      <div class="sbox doctor-status-container">
        <div class="sn">Doctor Status</div>
        <div class="docs-grid" id="docs"></div>
      </div>
    </div>
  </div>

  <!-- Row 3: Post-queue stages -->
  <div class="flow-row">
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
</div>

<p class="sec">Event log</p>
<div class="log" id="log"></div>

<div style="font-size:11px;color:#94A3B8;margin-top:14px;font-family:'Raleway',sans-serif;">
  *Patients remaining in stages after completion are still being processed when the simulation duration ends.
</div>

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
const PRI_MAP = {
  1: {k:'red',   l:'Red',   c:'pr'},
  2: {k:'yellow',l:'Yellow',c:'py'},
  3: {k:'green', l:'Green', c:'pg'},
  4: {k:'white', l:'White', c:'pw'},
  5: {k:'black', l:'Black', c:'pb'}
};
const PATIENTS = __PATIENTS_JSON__;
const N_DOCTORS = __N_DOCTORS__;
const DURATION = __DURATION__;
const STAGES=[
  'arr','reg','tri','que','trt','ext'
];
const SL={
  arr:'Arrival',reg:'Registration',
  tri:'Triage',que:'Queue',
  trt:'Treatment',ext:'Exit'
};

let pts=[],docs=[],t=0,state='Not Started';
let run=false,tmr=null,sp=3;

function fmt(n){return Math.round(n);}

function initDocs(){
  docs=[];
  for(let i=0;i<N_DOCTORS;i++)
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
            font-size:7px">${p.id}</span>
          Patient #${p.id}
          </div>
          <div class="busy">
            Busy · ${fmt(d.tl)}m left
          </div>`
        :`<div class="dp"
            style="color:#94A3B8">—</div>
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
  const totalArrived = PATIENTS.filter(p => p.arrival_time <= t).length;
  const completedPts = PATIENTS.filter(p => p.treatment_end > 0 && t >= p.treatment_end && p.priority !== 5);
  const doneCount = completedPts.length;
  const queueLength = pts.filter(p => p.stg === 'que').length;
  const waitingCount = pts.filter(p => ['arr', 'reg', 'tri', 'que'].includes(p.stg)).length;
  const treatingCount = pts.filter(p => p.stg === 'trt').length;
  
  let avgWaitStr = '—';
  let maxWaitStr = '—';
  if (doneCount > 0) {
    const totalWait = completedPts.reduce((sum, p) => sum + (p.treatment_start - p.triage_end), 0);
    const avgWait = totalWait / doneCount;
    avgWaitStr = avgWait.toFixed(2) + 'm';
    
    const maxWait = Math.max(...completedPts.map(p => p.treatment_start - p.triage_end));
    maxWaitStr = maxWait.toFixed(2) + 'm';
  }
  
  let totalTreatmentTime = 0;
  PATIENTS.forEach(p => {
    if (p.treatment_end > 0 && t >= p.treatment_end && p.priority !== 5) {
      totalTreatmentTime += (p.treatment_end - p.treatment_start);
    }
  });
  const utilization = N_DOCTORS > 0 ? (totalTreatmentTime / Math.max(t * N_DOCTORS, 1)) * 100 : 0;
  
  document.getElementById('mtot').textContent = totalArrived;
  document.getElementById('mq').textContent = queueLength;
  document.getElementById('mw').textContent = waitingCount;
  document.getElementById('mt').textContent = treatingCount;
  document.getElementById('md').textContent = doneCount;
  document.getElementById('ma').textContent = avgWaitStr;
  document.getElementById('mmax').textContent = maxWaitStr;
  document.getElementById('mu').textContent = utilization.toFixed(1) + '%';
  document.getElementById('mm').textContent = Math.round(t) + 'm';
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

// Keep track of previously logged events to avoid duplicate logging
let loggedEvents = {};

function logStageChanges() {
  pts.forEach(p => {
    const key = `${p.id}-${p.stg}`;
    if (!loggedEvents[key]) {
      loggedEvents[key] = true;
      if (p.stg === 'arr') {
        lg(`Patient #${p.id} (${p.pl}) arrived at IGD.`);
      } else if (p.stg === 'reg') {
        lg(`Patient #${p.id} started registration.`);
      } else if (p.stg === 'tri') {
        lg(`Patient #${p.id} finished registration, starting triage.`);
      } else if (p.stg === 'que') {
        lg(`Patient #${p.id} triaged to ${p.pl} Priority Queue.`);
      } else if (p.stg === 'trt') {
        const docId = p.raw.doctor_id;
        lg(`Patient #${p.id} started treatment by Doctor ${docId}.`);
      } else if (p.stg === 'ext') {
        if (p.raw.priority === 5) {
          lg(`Patient #${p.id} declared DOA (Death on Arrival).`);
        } else {
          lg(`Patient #${p.id} completed treatment and exited IGD.`);
        }
      }
    }
  });
}

function stip(e,p){
  const tp=document.getElementById('tip');
  document.getElementById('ti').textContent
    ='#'+p.id;
  document.getElementById('tp').textContent
    =p.pl;
  document.getElementById('ts').textContent
    =SL[p.stg];
  
  let w = 0;
  if (p.raw.treatment_start > 0) {
    w = p.raw.treatment_start - (p.raw.triage_end || p.raw.arrival_time);
  } else {
    w = t - (p.raw.triage_end || p.raw.arrival_time);
  }
  w = Math.max(0, w);
  
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

function getStage(p, t) {
  if (t < p.arrival_time) return null;
  if (p.priority === 5 && p.triage_end > 0 && t >= p.triage_end) return 'ext';
  if (p.treatment_end > 0 && t >= p.treatment_end) return 'ext';
  if (p.treatment_start > 0 && t >= p.treatment_start) return 'trt';
  if (p.triage_end > 0 && t >= p.triage_end) return 'que';
  if (p.registration_end > 0 && t >= p.registration_end) return 'tri';
  if (p.registration_start > 0 && t >= p.registration_start) return 'reg';
  return 'arr';
}

function assignDoctorsToPatients() {
  const treatedPatients = PATIENTS.filter(p => p.treatment_start > 0)
    .sort((a, b) => a.treatment_start - b.treatment_start);
  
  const doctorFreeTime = Array(N_DOCTORS + 1).fill(0);
  
  treatedPatients.forEach(p => {
    let assignedDoc = 1;
    for (let d = 1; d <= N_DOCTORS; d++) {
      if (doctorFreeTime[d] <= p.treatment_start) {
        assignedDoc = d;
        break;
      }
    }
    if (doctorFreeTime[assignedDoc] > p.treatment_start) {
      let minTime = Infinity;
      for (let d = 1; d <= N_DOCTORS; d++) {
        if (doctorFreeTime[d] < minTime) {
          minTime = doctorFreeTime[d];
          assignedDoc = d;
        }
      }
    }
    p.doctor_id = assignedDoc;
    doctorFreeTime[assignedDoc] = p.treatment_end > 0 ? p.treatment_end : Infinity;
  });
}

function updateState(newState) {
  state = newState;
  const badge = document.getElementById('badge');
  const btn = document.getElementById('btn');
  
  badge.textContent = state;
  badge.className = 'badge ' + state.toLowerCase().replace(' ', '-');
  
  if (state === 'Not Started') {
    btn.textContent = '▶ Start';
    btn.disabled = false;
    btn.classList.remove('active');
    run = false;
  } else if (state === 'Running') {
    btn.textContent = '⏸ Pause';
    btn.disabled = false;
    btn.classList.add('active');
    run = true;
  } else if (state === 'Paused') {
    btn.textContent = '▶ Start';
    btn.disabled = false;
    btn.classList.remove('active');
    run = false;
  } else if (state === 'Completed') {
    btn.textContent = '🏁 Completed';
    btn.disabled = true;
    btn.classList.remove('active');
    run = false;
  }
}

function updateFrame() {
  pts = [];
  
  PATIENTS.forEach(raw => {
      const stg = getStage(raw, t);
      if (stg) {
          const pmap = PRI_MAP[raw.priority] || PRI_MAP[4];
          pts.push({
              id: raw.id,
              pc: pmap.c,
              pl: pmap.l,
              pk: pmap.k,
              stg: stg,
              at: raw.arrival_time,
              ts: raw.treatment_start,
              raw: raw
          });
      }
  });

  docs.forEach(d => { d.pat = null; d.tl = 0; });
  
  const trt_pts = pts.filter(p => p.stg === 'trt');
  trt_pts.forEach(p => {
     const docId = p.raw.doctor_id;
     if (docId && docId <= N_DOCTORS) {
         docs[docId - 1].pat = p;
         docs[docId - 1].tl = p.raw.treatment_end > 0 ? Math.max(0, p.raw.treatment_end - t) : 0;
     }
  });

  rall();
  logStageChanges();
}

function tick(){
  if (t >= DURATION) {
    if (state === 'Running') {
      clearInterval(tmr);
      updateState('Completed');
      lg('Simulation completed (' + DURATION + 'm reached).');
    }
    return;
  }
  const dt = 0.5;
  t += dt;
  updateFrame();
}

function tog(){
  if (state === 'Running') {
    clearInterval(tmr);
    updateState('Paused');
  } else if (state === 'Not Started' || state === 'Paused') {
    const iv = Math.max(50, 400 / sp);
    tmr = setInterval(tick, iv);
    updateState('Running');
  }
}

function rst(){
  clearInterval(tmr);
  t = 0;
  loggedEvents = {};
  updateState('Not Started');
  document.getElementById('log').innerHTML = '';
  initDocs();
  assignDoctorsToPatients();
  updateFrame();
  lg('Simulation reset.');
}

function setSp(v){
  sp=+v;
  document.getElementById('spv')
    .textContent=v+'×';
  if(state === 'Running'){
    clearInterval(tmr);
    tmr=setInterval(tick,Math.max(50,400/sp));
  }
}

assignDoctorsToPatients();
initDocs();
updateFrame();
lg('Ready. Click Start.');
</script>
</body>
</html>
"""


def render_animation(patients_json: str, n_doctors: int, duration: int = 480, height: int = 680):
    html_content = ANIMATION_HTML.replace("__DURATION__", str(duration))
    html_content = html_content.replace("__PATIENTS_JSON__", patients_json)
    html_content = html_content.replace("__N_DOCTORS__", str(n_doctors))
    
    # Generate a unique hash based on configuration parameters and patients data
    # to force Streamlit's React container to completely unmount and remount
    # the iframe, ensuring a clean context, resetting timers, and avoiding stale/duplicate states.
    import hashlib
    config_str = f"{patients_json}_{n_doctors}_{duration}"
    content_hash = hashlib.md5(config_str.encode("utf-8")).hexdigest()
    
    components.html(
        html_content,
        height=height,
        scrolling=False,
        key=f"anim_iframe_{content_hash}"
    )

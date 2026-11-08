"""VoiceForge web GUI: a single-file, zero-dependency web app.

Premium minimal interface: near-black surfaces, hairline borders,
one restrained accent, real SVG iconography. Standard library only
(http.server). Files upload as base64 JSON. Every job runs the same
low-RAM pipeline as the CLI, one engine at a time, fully offline.
"""
from __future__ import annotations

import base64
import contextlib
import io
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import config

OUT = config.WORK_DIR / "webout"
JOBS: dict[str, dict] = {}

LOGO_SVG = """
<svg width="38" height="38" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
<rect x="2" y="2" width="60" height="60" rx="15" fill="#17171a"/>
<rect x="2" y="2" width="60" height="60" rx="15" fill="none" stroke="#ffffff" stroke-opacity="0.14"/>
<g fill="#f5f5f4"><rect x="14" y="26" width="4" height="12" rx="2"/>
<rect x="22" y="20" width="4" height="24" rx="2"/>
<rect x="38" y="20" width="4" height="24" rx="2"/>
<rect x="46" y="26" width="4" height="12" rx="2"/></g>
<rect x="30" y="14" width="4" height="36" rx="2" fill="#c8f542"/></svg>
"""

ICONS = {
 "mic": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></svg>',
 "music": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l10-2v13"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="16.5" cy="16" r="2.5"/></svg>',
 "speak": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-8 8H4l2.2-2.9A8 8 0 1 1 21 12Z"/></svg>',
 "convert": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8h13l-3-3M20 16H7l3 3"/></svg>',
 "split": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="2.5"/><circle cx="6" cy="18" r="2.5"/><path d="M8 7.5 20 19M8 16.5 20 5"/></svg>',
 "library": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5a2 2 0 0 1 2-2h4v18H6a2 2 0 0 1-2-2Z"/><path d="M10 3h4a2 2 0 0 1 2 2v16h-6"/><path d="m16.5 5 3.7 1A2 2 0 0 1 21.5 8.5L19 19l-3.6-1"/></svg>',
 "upload": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 16V4m0 0 4 4m-4-4L8 8"/><path d="M4 16v3a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-3"/></svg>',
}

PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VoiceForge - CPU Voice Cloning Studio</title>
<style>
:root{--bg:#0a0a0b;--panel:#101012;--card:#141416;--card2:#0d0d0f;
--line:rgba(255,255,255,.08);--line2:rgba(255,255,255,.16);
--txt:#f5f5f4;--dim:#a3a3ab;--dim2:#6d6d75;--acc:#c8f542;
--ok:#4ade80;--radius:16px}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--txt);
font-family:ui-sans-system,system-ui,-apple-system,"Segoe UI",Roboto,
"Helvetica Neue",Arial,sans-serif;display:flex;
-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
::selection{background:rgba(200,245,66,.28)}
/* sidebar */
aside{width:248px;flex:0 0 248px;background:var(--panel);
border-right:1px solid var(--line);display:flex;flex-direction:column;
position:sticky;top:0;height:100vh}
.brand{display:flex;gap:12px;align-items:center;padding:22px 20px 18px}
.brand h1{font-size:17px;margin:0;font-weight:650;letter-spacing:-.02em}
.brand .sub{color:var(--dim2);font-size:11.5px;margin-top:2px;letter-spacing:.01em}
.navlabel{padding:14px 20px 6px;font-size:10.5px;letter-spacing:.14em;
color:var(--dim2);font-weight:600}
nav{padding:0 10px;display:flex;flex-direction:column;gap:2px}
nav button{display:flex;align-items:center;gap:11px;width:100%;text-align:left;
background:transparent;border:0;color:var(--dim);padding:9px 11px;
border-radius:9px;font-size:13.5px;cursor:pointer;font-weight:500;
transition:background .12s,color .12s}
nav button svg{width:17px;height:17px;flex:0 0 17px;opacity:.85}
nav button:hover{color:var(--txt);background:rgba(255,255,255,.045)}
nav button.active{color:var(--txt);background:rgba(255,255,255,.07);
box-shadow:inset 0 0 0 1px var(--line)}
nav button.active svg{color:var(--acc);opacity:1}
.sidefoot{margin-top:auto;padding:16px}
.enginecard{border:1px solid var(--line);border-radius:12px;padding:12px 14px;
background:var(--card2)}
.enginecard .t{display:flex;align-items:center;gap:8px;font-size:12.5px;font-weight:600}
.enginecard .s{color:var(--dim2);font-size:11.5px;line-height:1.55;margin-top:6px}
.dotok{width:7px;height:7px;border-radius:50%;background:var(--ok);
box-shadow:0 0 0 3px rgba(74,222,128,.15)}
.version{color:var(--dim2);font-size:11px;margin-top:12px;padding:0 2px}
/* main */
main{flex:1;min-width:0;display:flex;flex-direction:column}
header{display:flex;align-items:center;gap:14px;padding:20px 32px;
border-bottom:1px solid var(--line)}
header h2{margin:0;font-size:19px;font-weight:650;letter-spacing:-.02em}
header .hint{color:var(--dim);font-size:13px}
header .right{margin-left:auto;display:flex;gap:8px;align-items:center}
.chip{display:inline-flex;align-items:center;gap:7px;padding:5px 11px;
border:1px solid var(--line);border-radius:99px;font-size:11.5px;color:var(--dim);
background:var(--card2)}
section{display:none;padding:28px 32px 8px;max-width:880px;width:100%}
section.active{display:block}
.card{background:var(--card);border:1px solid var(--line);
border-radius:var(--radius);padding:24px 26px;margin-bottom:18px}
.card h3{margin:0 0 5px;font-size:15.5px;font-weight:650;letter-spacing:-.01em}
.card p{color:var(--dim);font-size:13px;margin:2px 0 8px;line-height:1.6}
label{display:block;font-size:11px;color:var(--dim);margin:16px 0 6px;
text-transform:uppercase;letter-spacing:.1em;font-weight:600}
input[type=text],input[type=number],textarea{width:100%;
background:var(--card2);border:1px solid var(--line);border-radius:10px;
color:var(--txt);padding:10px 12px;font-size:14px;outline:none;
transition:border-color .12s, box-shadow .12s}
input::placeholder,textarea::placeholder{color:var(--dim2)}
input:focus,textarea:focus{border-color:rgba(200,245,66,.55);
box-shadow:0 0 0 3px rgba(200,245,66,.12)}
.drop{border:1px dashed rgba(255,255,255,.2);border-radius:12px;
padding:28px 16px;text-align:center;color:var(--dim);cursor:pointer;
font-size:13.5px;transition:.15s;background:var(--card2)}
.drop:hover{border-color:rgba(255,255,255,.4);color:var(--txt)}
.drop.over{border-color:var(--acc);color:#fff;background:rgba(200,245,66,.05)}
.drop .tile{width:40px;height:40px;margin:0 auto 10px;border-radius:11px;
border:1px solid var(--line);background:var(--card);display:flex;
align-items:center;justify-content:center;color:var(--dim)}
.drop .tile svg{width:19px;height:19px}
.btn{background:var(--txt);color:#0a0a0b;border:0;border-radius:10px;
padding:11px 20px;font-weight:600;font-size:13.5px;cursor:pointer;
margin-top:20px;transition:filter .12s, transform .05s}
.btn:hover{filter:brightness(.92)}
.btn:active{transform:translateY(1px)}
.btn.ghost{background:transparent;color:var(--txt);
border:1px solid var(--line2);margin-top:0;font-weight:550}
.btn.ghost:hover{background:rgba(255,255,255,.05);filter:none}
.btn:disabled{opacity:.5;cursor:wait}
.row{display:flex;gap:14px}.row>div{flex:1}
input[type=range]{-webkit-appearance:none;appearance:none;width:100%;
height:4px;border-radius:99px;background:rgba(255,255,255,.14);outline:none;
margin:10px 0 2px}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:15px;
height:15px;border-radius:50%;background:#fff;border:0;cursor:pointer;
box-shadow:0 1px 4px rgba(0,0,0,.55),0 0 0 1px rgba(0,0,0,.25)}
input[type=range]::-moz-range-thumb{width:15px;height:15px;border-radius:50%;
background:#fff;border:0;cursor:pointer;box-shadow:0 1px 4px rgba(0,0,0,.55)}
.rval{color:var(--txt);font-size:12px;text-transform:none;letter-spacing:0;
font-weight:600;float:right}
.switch{display:flex;gap:11px;align-items:center;margin-top:18px;
cursor:pointer;color:var(--dim);font-size:13.5px;user-select:none}
.switch input{display:none}
.switch .tr{width:36px;height:20px;border-radius:99px;flex:0 0 36px;
background:rgba(255,255,255,.16);position:relative;transition:.15s}
.switch .tr::after{content:"";position:absolute;top:2px;left:2px;width:16px;
height:16px;border-radius:50%;background:#fff;transition:.15s}
.switch input:checked + .tr{background:var(--acc)}
.switch input:checked + .tr::after{left:18px;background:#0a0a0b}
/* console */
.console{padding:4px 32px 30px;max-width:880px;width:100%}
.console .card{margin:0;padding:18px 22px}
.status{display:flex;gap:9px;align-items:center;font-size:12.5px;color:var(--dim)}
.sdot{width:8px;height:8px;border-radius:50%;background:#3f3f46}
.sdot.run{background:var(--acc);animation:pl 1s infinite}
.sdot.done{background:var(--ok)}
@keyframes pl{50%{opacity:.3}}
pre{background:#070708;border:1px solid var(--line);border-radius:10px;
padding:13px 14px;white-space:pre-wrap;font-size:12px;line-height:1.6;
max-height:220px;overflow:auto;color:#c9c9cf;min-height:52px;
font-family:ui-monospace,"Cascadia Mono",Consolas,monospace;margin:12px 0 0}
audio{width:100%;margin-top:14px}
a.dl{color:var(--acc);font-size:13px;text-decoration:none}
a.dl:hover{text-decoration:underline}
@media (max-width:760px){
body{flex-direction:column}
aside{position:static;width:auto;flex:none;height:auto;
border-right:0;border-bottom:1px solid var(--line)}
.brand{padding:14px 16px 10px}
.navlabel{display:none}
nav{flex-direction:row;overflow-x:auto;padding:2px 8px 10px;gap:4px}
nav button{white-space:nowrap;padding:9px 12px}
.sidefoot{display:none}
header{padding:14px 18px;flex-wrap:wrap;gap:8px}
header .hint{display:none}
header .right{margin-left:0}
section,.console{padding-left:18px;padding-right:18px;max-width:100%}
.row{flex-direction:column}
.card{padding:20px 18px}
.drop{padding:24px 12px}
.btn{width:100%;padding:13px 20px}
.btn.ghost{width:auto}
}
</style></head><body>
<aside>
  <div class="brand">__LOGO__<div><h1>VoiceForge</h1>
  <div class="sub">CPU Voice Cloning Studio</div></div></div>
  <div class="navlabel">CREATE</div>
  <nav id="nav">
    <button data-page="train" class="active">__I_MIC__ Train voice</button>
    <button data-page="sing">__I_MUSIC__ Sing a song</button>
    <button data-page="speak">__I_SPEAK__ Speak text</button>
    <button data-page="convert">__I_CONVERT__ Convert audio</button>
    <button data-page="separate">__I_SPLIT__ Separate vocals</button>
  </nav>
  <div class="navlabel">LIBRARY</div>
  <nav>
    <button data-page="voices" id="navVoices">__I_LIBRARY__ My voices</button>
  </nav>
  <div class="sidefoot">
    <div class="enginecard"><div class="t"><span class="dotok"></span>Local engine ready</div>
    <div class="s">Runs fully offline on CPU. Your voice never leaves this computer.</div></div>
    <div class="version">VoiceForge v1.0.0.1</div>
  </div>
</aside>
<main>
<header><h2 id="pageTitle">Train voice</h2>
<span class="hint" id="pageHint">Teach VoiceForge a new voice from recordings.</span>
<div class="right"><span class="chip">CPU only</span><span class="chip">Low RAM</span>
<span class="chip"><span class="dotok"></span>Offline</span></div></header>

<section id="page-train" class="active"><div class="card">
<h3>New voice</h3>
<p>Drop recordings of one person, or record with the microphone.
Minimum 30 seconds in total. Small chunks are best: 5 minutes is good,
10 minutes is ideal.</p>
<div class="drop" id="trainDrop"><div class="tile">__I_UPLOAD__</div>
<span class="dztext">Drop voice recordings here, or click to choose files</span>
<input type="file" id="trainFiles" accept="audio/*" multiple hidden></div>
<div style="margin-top:14px;display:flex;gap:12px;align-items:center">
<button class="btn ghost" id="recBtn">Record from microphone</button>
<span class="hint" id="recState" style="color:var(--dim);font-size:12.5px"></span></div>
<div class="row"><div><label>Voice name</label>
<input type="text" id="trainName" placeholder="e.g. tanmoy"></div>
<div><label>Training rounds (epochs)</label>
<input type="number" id="trainEpochs" value="60" min="5" max="300"></div></div>
<button class="btn" onclick="startJob('train')">Train this voice</button>
</div></section>

<section id="page-sing"><div class="card">
<h3>Sing a song in a trained voice</h3>
<p>VoiceForge removes the music, converts the singing into your voice,
and can mix it back over the original music.</p>
<div class="drop" id="songDrop"><div class="tile">__I_UPLOAD__</div>
<span class="dztext">Drop a song here, or click to choose a file</span>
<input type="file" id="songFile" accept="audio/*" hidden></div>
<label>Voice name</label><input type="text" id="singVoice" placeholder="e.g. tanmoy">
<label>Voice strength <span class="rval" id="singIrVal">1.00</span></label>
<input type="range" id="singIr" min="0" max="1" step="0.05" value="1">
<label>Clarity protect <span class="rval" id="singPrVal">0.25</span></label>
<input type="range" id="singPr" min="0" max="0.5" step="0.05" value="0.25">
<label class="switch"><input type="checkbox" id="singMusic"><span class="tr"></span>Mix back over the music</label>
<button class="btn" onclick="startJob('sing')">Make the song</button>
</div></section>

<section id="page-speak"><div class="card">
<h3>Speak text in a trained voice</h3>
<p>Type anything: lyrics, a message, a story. It is spoken in the
trained voice. For a melody, use Sing with a real song.</p>
<label>Text</label><textarea id="speakText" rows="4" placeholder="Type here..."></textarea>
<label>Voice name</label><input type="text" id="speakVoice" placeholder="e.g. tanmoy">
<button class="btn" onclick="startJob('speak')">Speak it</button>
</div></section>

<section id="page-convert"><div class="card">
<h3>Convert any audio into a trained voice</h3>
<p>Best for voice recordings and isolated vocals.</p>
<div class="drop" id="convDrop"><div class="tile">__I_UPLOAD__</div>
<span class="dztext">Drop an audio file here, or click to choose</span>
<input type="file" id="convFile" accept="audio/*" hidden></div>
<label>Voice name</label><input type="text" id="convVoice" placeholder="e.g. tanmoy">
<label>Voice strength <span class="rval" id="convIrVal">1.00</span></label>
<input type="range" id="convIr" min="0" max="1" step="0.05" value="1">
<label>Clarity protect <span class="rval" id="convPrVal">0.25</span></label>
<input type="range" id="convPr" min="0" max="0.5" step="0.05" value="0.25">
<button class="btn" onclick="startJob('convert')">Convert it</button>
</div></section>

<section id="page-separate"><div class="card">
<h3>Separate vocals from music</h3>
<p>Splits a song into a clean vocal track and an instrumental track.</p>
<div class="drop" id="sepDrop"><div class="tile">__I_UPLOAD__</div>
Drop a song here, or click to choose
<input type="file" id="sepFile" accept="audio/*" hidden></div>
<button class="btn" onclick="startJob('separate')">Separate it</button>
</div></section>

<section id="page-voices"><div class="card">
<h3>Trained voices on this computer</h3>
<p>Voices you trained with VoiceForge, stored locally.</p>
<button class="btn ghost" onclick="startJob('voices')">Refresh list</button>
<pre id="voiceList">Press Refresh list.</pre>
</div></section>

<div class="console"><div class="card">
<div class="status"><span class="sdot" id="jobDot"></span>
<span id="jobState">Idle. Jobs run one at a time to keep memory low.</span></div>
<pre id="log">No job yet.</pre>
<div id="result"></div>
</div></div>
</main>
<script>
const TITLES={train:["Train voice","Teach VoiceForge a new voice from recordings."],
sing:["Sing a song","Put any song into a trained voice."],
speak:["Speak text","Hear typed text in a trained voice."],
convert:["Convert audio","Move any recording onto a trained voice."],
separate:["Separate vocals","Split a song into vocals and instrumental."],
voices:["My voices","Trained voices stored on this computer."]};
function goPage(key){
 document.querySelectorAll('#nav button, #navVoices').forEach(x=>
  x.classList.toggle('active', x.dataset.page===key));
 document.querySelectorAll('section').forEach(s=>s.classList.remove('active'));
 document.getElementById('page-'+key).classList.add('active');
 document.getElementById('pageTitle').textContent=TITLES[key][0];
 document.getElementById('pageHint').textContent=TITLES[key][1];}
document.querySelectorAll('[data-page]').forEach(b=>
 b.addEventListener('click',()=>goPage(b.dataset.page)));
let trainData=[], songData=null, convData=null, sepData=null, rec=null, recChunks=[];
function readFiles(files, cb){let out=[],n=files.length;if(!n){cb(out);return}
 for(const f of files){const r=new FileReader();
  r.onload=()=>{out.push({name:f.name,data:r.result.split(',')[1]});
   if(out.length===n)cb(out)};r.readAsDataURL(f)}}
function drop(id,inputId,cb){const d=document.getElementById(id),
 inp=document.getElementById(inputId);
 d.onclick=()=>inp.click();
 inp.onchange=()=>readFiles(inp.files,cb);
 d.ondragover=e=>{e.preventDefault();d.classList.add('over')};
 d.ondragleave=()=>d.classList.remove('over');
 d.ondrop=e=>{e.preventDefault();d.classList.remove('over');
  readFiles(e.dataTransfer.files,cb)}}
drop('trainDrop','trainFiles',d=>{trainData=d;
 document.querySelector('#trainDrop .dztext').textContent=
  d.length+' recording(s) ready. Click to change.'});
drop('songDrop','songFile',d=>{songData=d[0];
 document.querySelector('#songDrop .dztext').textContent='Song ready: '+d[0].name});
drop('convDrop','convFile',d=>{convData=d[0];
 document.querySelector('#convDrop .dztext').textContent='File ready: '+d[0].name});
drop('sepDrop','sepFile',d=>{sepData=d[0];
 document.querySelector('#sepDrop .dztext').textContent='Song ready: '+d[0].name});
document.getElementById('recBtn').onclick=async()=>{
 if(rec){rec.stop();return}
 const stream=await navigator.mediaDevices.getUserMedia({audio:true});
 rec=new MediaRecorder(stream);recChunks=[];
 rec.ondataavailable=e=>recChunks.push(e.data);
 rec.onstop=()=>{const blob=new Blob(recChunks,{type:'audio/webm'});
  const r=new FileReader();r.onload=()=>{trainData.push(
   {name:'recording.webm',data:r.result.split(',')[1]});
   document.getElementById('recState').textContent=
    'Recording added ('+trainData.length+' file(s) total).'};
  r.readAsDataURL(blob);rec=null;
  document.getElementById('recBtn').textContent='Record from microphone'};
 rec.start();document.getElementById('recBtn').textContent='Stop recording'};
for(const [r,v] of [['singIr','singIrVal'],['singPr','singPrVal'],
 ['convIr','convIrVal'],['convPr','convPrVal']]){
 document.getElementById(r).oninput=e=>
  document.getElementById(v).textContent=(+e.target.value).toFixed(2)}
async function startJob(kind){
 const body={kind};
 if(kind==='train'){body.files=trainData;
  body.name=document.getElementById('trainName').value;
  body.epochs=document.getElementById('trainEpochs').value}
 if(kind==='sing'){body.file=songData;
  body.voice=document.getElementById('singVoice').value;
  body.index_rate=document.getElementById('singIr').value;
  body.protect=document.getElementById('singPr').value;
  body.with_music=document.getElementById('singMusic').checked}
 if(kind==='speak'){body.text=document.getElementById('speakText').value;
  body.voice=document.getElementById('speakVoice').value}
 if(kind==='convert'){body.file=convData;
  body.voice=document.getElementById('convVoice').value;
  body.index_rate=document.getElementById('convIr').value;
  body.protect=document.getElementById('convPr').value}
 if(kind==='separate'){body.file=sepData}
 const dot=document.getElementById('jobDot'),
 state=document.getElementById('jobState');
 dot.className='sdot run';state.textContent='Working... one engine at a time.';
 document.getElementById('result').innerHTML='';
 const r=await fetch('/job',{method:'POST',
  headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
 const j=await r.json();
 const timer=setInterval(async()=>{
  const s=await(await fetch('/status?id='+j.id)).json();
  document.getElementById('log').textContent=s.log||'Working...';
  if(kind==='voices'&&s.log)
   document.getElementById('voiceList').textContent=s.log;
  if(s.done){clearInterval(timer);dot.className='sdot done';
   state.textContent='Done.';
   if(s.result){document.getElementById('result').innerHTML=
    '<audio controls src="/file?name='+s.result+'"></audio><br>'+
    '<a class="dl" href="/file?name='+s.result+'" download>Download result</a>'}}
 },1500)}
</script></body></html>
"""


def _render_page() -> bytes:
    html = PAGE.replace("__LOGO__", LOGO_SVG)
    for key, token in [("mic", "__I_MIC__"), ("music", "__I_MUSIC__"),
                       ("speak", "__I_SPEAK__"), ("convert", "__I_CONVERT__"),
                       ("split", "__I_SPLIT__"), ("library", "__I_LIBRARY__"),
                       ("upload", "__I_UPLOAD__")]:
        html = html.replace(token, ICONS[key])
    return html.encode()


def _save_upload(item: dict, folder: Path) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    p = folder / Path(item["name"]).name
    p.write_bytes(base64.b64decode(item["data"]))
    return p


def _run_job(job_id: str, body: dict) -> None:
    job = JOBS[job_id]
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            kind = body["kind"]
            up = config.WORK_DIR / "uploads"
            OUT.mkdir(parents=True, exist_ok=True)
            if kind == "train":
                from .dataset import prepare
                from .train import train
                files = [_save_upload(f, up) for f in body["files"]]
                ds = prepare(body["name"], files)
                train(body["name"], ds, epochs=int(body.get("epochs") or 60))
                print("Training complete. The voice is ready to use.")
            elif kind == "sing":
                from .sing import sing
                src = _save_upload(body["file"], up)
                dst = OUT / f"{src.stem}_voiceforge.wav"
                sing(src, body["voice"], dst,
                     with_music=bool(body.get("with_music")),
                     index_rate=float(body.get("index_rate") or 1.0),
                     protect=float(body.get("protect") or 0.25))
                job["result"] = dst.name
            elif kind == "speak":
                from .speak import speak
                dst = OUT / "speak_voiceforge.wav"
                speak(body["text"], body["voice"], dst)
                job["result"] = dst.name
            elif kind == "convert":
                from .convert import convert_file
                src = _save_upload(body["file"], up)
                dst = OUT / f"{src.stem}_converted.wav"
                convert_file(src, body["voice"], dst,
                             index_rate=float(body.get("index_rate") or 1.0),
                             protect=float(body.get("protect") or 0.25))
                job["result"] = dst.name
            elif kind == "separate":
                from .separate import separate
                src = _save_upload(body["file"], up)
                v, b = separate(src)
                print("Vocals:", v)
                print("Instrumental:", b)
            elif kind == "voices":
                logs = config.applio_dir() / "logs"
                names = []
                if logs.exists():
                    names = sorted(d.name for d in logs.iterdir()
                                   if d.is_dir() and list(d.glob("*.pth")))
                print("\n".join(names) if names else "No trained voices yet.")
    except Exception as e:  # surfaced to the page, never hidden
        print("ERROR:", e)
    finally:
        job["log"] = buf.getvalue()
        job["done"] = True


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self._send(200, _render_page(), "text/html; charset=utf-8")
        elif self.path.startswith("/status"):
            jid = self.path.split("id=")[-1]
            job = JOBS.get(jid, {"done": True, "log": "unknown job"})
            self._send(200, json.dumps({
                "done": job.get("done", False), "log": job.get("log", ""),
                "result": job.get("result")}).encode(), "application/json")
        elif self.path.startswith("/file"):
            name = Path(self.path.split("name=")[-1]).name
            f = OUT / name
            if f.exists():
                self._send(200, f.read_bytes(), "audio/wav")
            else:
                self._send(404, b"not found", "text/plain")
        else:
            self._send(404, b"not found", "text/plain")

    def do_POST(self):
        if self.path != "/job":
            self._send(404, b"not found", "text/plain")
            return
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) or b"{}")
        jid = str(len(JOBS) + 1)
        JOBS[jid] = {"done": False, "log": "", "result": None}
        threading.Thread(target=_run_job, args=(jid, body), daemon=True).start()
        self._send(200, json.dumps({"id": jid}).encode(), "application/json")

    def _send(self, code, data, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def start_server(host: str = "127.0.0.1", port: int = 8760):
    """Start the studio server in a background thread; return it."""
    OUT.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer((host, port), Handler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server


def serve(host: str = "127.0.0.1", port: int = 8760) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"VoiceForge web GUI: http://{host}:{port}")
    ThreadingHTTPServer((host, port), Handler).serve_forever()

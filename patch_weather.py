from pathlib import Path
import re, json, shutil, zipfile
root=Path('/mnt/data/work/weatherfix')
app=root/'client/src/App.tsx'
css=root/'client/src/styles.css'
path=(root/'india_path.txt').read_text().strip()
s=app.read_text()
# Add INDIA path constant before WeatherMap if absent
if 'const INDIA_MAP_PATH=' not in s:
    marker='function WeatherMap({role}:{role:Role}){'
    s=s.replace(marker, f"const INDIA_MAP_PATH='{path}';\nconst INDIA_BOUNDS={{minLon:67.5,maxLon:98.5,minLat:6,maxLat:36.5}};\n\n{marker}",1)
start=s.index('function WeatherMap({role}:{role:Role}){')
end=s.index('function HelpDesk({role}:{role:Role}){', start)
new_func=r'''function WeatherMap({role}:{role:Role}){
 const places:any={
  Sehore:{lat:23.199,lon:77.085,label:'Sehore, MP',note:'Farm cluster · soybean / wheat'},
  Bhopal:{lat:23.2599,lon:77.4126,label:'Bhopal, MP',note:'Mandi / storage hub'},
  Indore:{lat:22.7196,lon:75.8577,label:'Indore, MP',note:'Large mandi & processing market'},
  Nagpur:{lat:21.1458,lon:79.0882,label:'Nagpur, MH',note:'High buyer demand / receiving hub'},
  Jaipur:{lat:26.9124,lon:75.7873,label:'Jaipur, RJ',note:'Long-haul buyer market'},
  Lucknow:{lat:26.8467,lon:80.9462,label:'Lucknow, UP',note:'Large regional market'},
  Ahmedabad:{lat:23.0225,lon:72.5714,label:'Ahmedabad, GJ',note:'Processor / bulk buyer market'}
 };
 const weather:any={
  Sehore:{temp:'28°C',rain:'40%',risk:'Medium',note:'Rain risk · 40% chance',advice:role==='farmer'?'Cover the lot before dispatch':'Keep a delivery buffer'},
  Bhopal:{temp:'29°C',rain:'32%',risk:'Low',note:'Mostly dry conditions',advice:role==='farmer'?'Good for short-haul dispatch':'Good for routine receiving'},
  Indore:{temp:'30°C',rain:'35%',risk:'Low',note:'Light rain possible',advice:role==='farmer'?'Normal dispatch window':'Normal receiving window'},
  Nagpur:{temp:'31°C',rain:'58%',risk:'High',note:'Thunderstorm risk',advice:role==='farmer'?'Prefer earlier dispatch':'Prefer earlier receiving slot'},
  Jaipur:{temp:'33°C',rain:'18%',risk:'Low',note:'Dry route conditions',advice:role==='farmer'?'Long-haul route looks stable':'Long-haul inbound conditions stable'},
  Lucknow:{temp:'29°C',rain:'48%',risk:'Medium',note:'Scattered rain possible',advice:role==='farmer'?'Build rain buffer into route':'Build receiving buffer'},
  Ahmedabad:{temp:'32°C',rain:'28%',risk:'Low',note:'Mostly dry conditions',advice:role==='farmer'?'Normal dispatch window':'Normal receiving window'}
 };
 const routeMatrix:any={
  'Sehore-Bhopal':190,'Sehore-Indore':285,'Sehore-Nagpur':760,'Sehore-Jaipur':590,'Sehore-Lucknow':760,'Sehore-Ahmedabad':720,
  'Bhopal-Indore':195,'Bhopal-Nagpur':350,'Bhopal-Jaipur':600,'Bhopal-Lucknow':610,'Bhopal-Ahmedabad':525,
  'Indore-Nagpur':415,'Indore-Jaipur':570,'Indore-Lucknow':940,'Indore-Ahmedabad':400,
  'Nagpur-Jaipur':1050,'Nagpur-Lucknow':950,'Nagpur-Ahmedabad':610,
  'Jaipur-Lucknow':570,'Jaipur-Ahmedabad':670,'Lucknow-Ahmedabad':1180
 };
 const routeDistance=(a:string,b:string)=>routeMatrix[`${a}-${b}`]||routeMatrix[`${b}-${a}`]||420;
 const [from,setFrom]=useState(role==='farmer'?'Sehore':'Bhopal');
 const [to,setTo]=useState(role==='farmer'?'Bhopal':'Sehore');
 const [mode,setMode]=useState<'Truck'|'Tractor'|'Rail'>('Truck');
 const a=places[from], b=places[to];
 const dist=routeDistance(from,to);
 const modeMeta:any={
  Truck:{icon:Truck,rate:38,eta:Math.max(1,Math.ceil(dist/360))+'–'+Math.max(1,Math.ceil(dist/300))+' days',capacity:'12–22 T'},
  Tractor:{icon:Tractor,rate:52,eta:Math.max(1,Math.ceil(dist/180))+'–'+Math.max(1,Math.ceil(dist/140))+' days',capacity:'4–8 T'},
  Rail:{icon:TrainFront,rate:21,eta:Math.max(1,Math.ceil(dist/550))+'–'+Math.max(1,Math.ceil(dist/420))+' days',capacity:'50+ T'}
 };
 const meta=modeMeta[mode];
 const estimated=Math.round(dist*meta.rate);
 const mapX=(lon:number)=>((lon-INDIA_BOUNDS.minLon)/(INDIA_BOUNDS.maxLon-INDIA_BOUNDS.minLon))*760;
 const mapY=(lat:number)=>((INDIA_BOUNDS.maxLat-lat)/(INDIA_BOUNDS.maxLat-INDIA_BOUNDS.minLat))*700;
 const x1=mapX(a.lon),y1=mapY(a.lat),x2=mapX(b.lon),y2=mapY(b.lat);
 const dx=x2-x1,dy=y2-y1,len=Math.max(1,Math.hypot(dx,dy));
 const nx=-dy/len,ny=dx/len;
 const curve=Math.min(36,Math.max(10,len*0.10));
 const cx=(x1+x2)/2+nx*curve,cy=(y1+y2)/2+ny*curve;
 const routeD=`M ${x1.toFixed(1)} ${y1.toFixed(1)} Q ${cx.toFixed(1)} ${cy.toFixed(1)} ${x2.toFixed(1)} ${y2.toFixed(1)}`;
 const mapPercent=(x:number,y:number)=>({left:`${(x/760)*100}%`,top:`${(y/700)*100}%`});
 const fromPt=mapPercent(x1,y1),toPt=mapPercent(x2,y2);
 const allPlaces=Object.entries(places) as any[];
 const modeClass=mode.toLowerCase();
 const weatherNodes=[
  {name:'Route start',p:mapPercent(x1,y1),risk:weather[from].risk},
  {name:'Mid-route',p:mapPercent((x1+x2)/2,(y1+y2)/2),risk:weather[(dist>500? 'Nagpur':from)].risk},
  {name:'Destination',p:mapPercent(x2,y2),risk:weather[to].risk}
 ];
 const fromOptions=Object.keys(places),toOptions=Object.keys(places).filter(x=>x!==from);
 const selectFrom=(v:string)=>{if(v===to){const fallback=Object.keys(places).find(x=>x!==v)||'Bhopal';setTo(fallback)}setFrom(v)};
 const selectTo=(v:string)=>{if(v!==from)setTo(v)};
 return <><div className="page-intro"><div><p className="eyebrow">Weather intelligence + route planning</p><h2>{role==='farmer'?'Plan your farm-to-market journey':'Plan your supplier-to-buyer journey'}</h2><p>Choose the origin, destination and transport mode. The India map, route, weather risk, ETA and demo cost update together.</p></div><Badge tone="blue">Fast India route view · demo data</Badge></div><Card><div className="weather-route-controls"><label>From<select value={from} onChange={e=>selectFrom(e.target.value)}>{fromOptions.map(c=><option key={c}>{c}</option>)}</select></label><div className="route-arrow">→</div><label>To<select value={to} onChange={e=>selectTo(e.target.value)}>{toOptions.map(c=><option key={c}>{c}</option>)}</select></label><label>Transport<select value={mode} onChange={e=>setMode(e.target.value as any)}><option>Truck</option><option>Tractor</option><option>Rail</option></select></label></div><div className="weather-mode-row">{(Object.keys(modeMeta) as Array<'Truck'|'Tractor'|'Rail'>).map(m=>{const M=modeMeta[m].icon;return <button type="button" key={m} className={`weather-mode-chip ${mode===m?'selected':''}`} onClick={()=>setMode(m)}><M size={15}/><span>{m}</span><small>{modeMeta[m].capacity}</small></button>})}</div><div className={`weather-map india-route-map ${role==='farmer'?'weather-map-farmer':'weather-map-buyer'}`}><div className="india-map-sky"><div className="india-map-grid"></div><div className="weather-sun"></div><div className="weather-cloud"><span></span><i></i><i></i><i></i><i></i></div></div><svg className="india-route-svg" viewBox="0 0 760 700" preserveAspectRatio="xMidYMid meet" aria-label={`Route from ${a.label} to ${b.label}`}><defs><filter id="routeShadow"><feDropShadow dx="0" dy="3" stdDeviation="3" floodOpacity="0.20"/></filter></defs><path d={INDIA_MAP_PATH} className="india-land"/><path d={routeD} className={`india-route-line ${modeClass}`} filter="url(#routeShadow)"/><path d={routeD} className="india-route-glow"/><g className="route-flow"><circle r="6"><animateMotion dur={mode==='Rail'?'3.8s':mode==='Tractor'?'5s':'4.4s'} repeatCount="indefinite" path={routeD}/></circle></g>{allPlaces.map(([key,p])=>{const pp=mapPercent(p.lon,p.lat);const active=key===from||key===to;return <g key={key} className={`india-place-dot ${active?'active':''}`}><circle cx={(pp.left as string).replace('%','')*7.6} cy={(pp.top as string).replace('%','')*7} r={active?6:3.5}/>{active&&<text x={(pp.left as string).replace('%','')*7.6+10} y={(pp.top as string).replace('%','')*7-8}>{p.label}</text>}</g>})}</svg><button type="button" className="india-route-pin from" style={fromPt} onClick={()=>selectFrom(from)}><span className="pin-dot"></span><b>{a.label}</b><small>{a.note}</small></button><button type="button" className="india-route-pin to" style={toPt} onClick={()=>selectTo(to)}><span className="pin-dot"></span><b>{b.label}</b><small>{b.note}</small></button><div className="india-map-badge"><strong>INDIA · ROUTE VIEW</strong><span>Route stays aligned with the map when the selection changes.</span></div><div className="india-map-weather"><strong>{weather[to].risk} weather risk</strong><span>{weather[to].note}</span><small>{weather[to].temp} · {weather[to].rain} rain probability</small></div><div className="india-route-status">{role==='farmer'?'🌾 Crop dispatch':'📦 Inbound procurement'} · {mode}</div><div className="india-route-legend"><span><i className="legend-dot route"/>Selected route</span><span><i className="legend-dot high"/>Destination weather</span></div></div><div className="route-summary-grid"><div><span>Route</span><strong>{from} → {to}</strong><small>{dist} km · demo route estimate</small></div><div><span>Transport</span><strong>{mode}</strong><small>{meta.capacity} capacity · {meta.eta}</small></div><div><span>Estimated cost</span><strong>₹{estimated.toLocaleString('en-IN')}</strong><small>Modeled estimate, not a live quote</small></div><div><span>Weather advice</span><strong>{weather[to].risk} risk</strong><small>{weather[to].advice}</small></div></div><div className="route-checkpoint-row">{weatherNodes.map((n,i)=><div key={`${n.name}-${i}`}><span className="eyebrow">{n.name}</span><strong>{n.risk} risk</strong><small>{i===0?a.label:i===2?b.label:'Corridor checkpoint'}</small></div>)}</div><div className="route-location-note"><MapPin size={15}/><div><b>{a.label}</b> → <b>{b.label}</b><span>{a.note} → {b.note}. Choose another location or transport above to recalculate the demo journey.</span></div></div></Card></>}
'''
s=s[:start]+new_func+s[end:]
app.write_text(s)

css_s=css.read_text()
css_s += r'''

/* Lightweight India-only weather route map: no external iframe, no drifting overlay */
.india-route-map{height:520px;position:relative;overflow:hidden;border:1px solid #dce7dc;background:linear-gradient(180deg,#eef6ed 0%,#e5efe2 48%,#dcebd9 100%);border-radius:16px;box-shadow:inset 0 1px 0 rgba(255,255,255,.7)}
.india-map-sky{position:absolute;inset:0;overflow:hidden;background:radial-gradient(circle at 78% 14%,rgba(255,221,117,.22),transparent 18%),radial-gradient(circle at 18% 60%,rgba(103,168,126,.13),transparent 32%),linear-gradient(180deg,rgba(245,250,243,.90),rgba(224,239,224,.92))}
.india-map-grid{position:absolute;inset:0;opacity:.34;background-image:linear-gradient(rgba(83,112,91,.08) 1px,transparent 1px),linear-gradient(90deg,rgba(83,112,91,.08) 1px,transparent 1px);background-size:44px 44px}
.india-route-svg{position:absolute;inset:20px 110px 16px 110px;width:calc(100% - 220px);height:calc(100% - 36px);z-index:3;overflow:visible}
.india-land{fill:#eef4e8;stroke:#89a895;stroke-width:2.2;filter:drop-shadow(0 8px 14px rgba(46,81,56,.10))}
.india-route-line{fill:none;stroke:#1f6a47;stroke-width:9;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:18 12}
.india-route-line.truck{stroke:#1f6a47}.india-route-line.tractor{stroke:#ad6b25}.india-route-line.rail{stroke:#6e4e9f;stroke-width:8;stroke-dasharray:4 12}
.india-route-glow{fill:none;stroke:rgba(255,255,255,.72);stroke-width:15;stroke-linecap:round;opacity:.32}
.route-flow circle{fill:#fff;border:4px solid #205d3f;stroke:#205d3f;stroke-width:3}
.india-place-dot circle{fill:#b7cab8;stroke:#fff;stroke-width:2}.india-place-dot.active circle{fill:#2e7a52}.india-place-dot text{font-size:12px;font-weight:800;fill:#345644;paint-order:stroke;stroke:#fff;stroke-width:4px;stroke-linejoin:round}
.india-route-pin{position:absolute;transform:translate(-50%,-50%);z-index:6;min-width:145px;max-width:185px;text-align:left;border:1px solid #dbe5da;background:rgba(255,255,255,.96);padding:9px 11px 10px 28px;border-radius:11px;box-shadow:0 10px 22px rgba(33,57,39,.13);cursor:pointer;backdrop-filter:blur(8px)}
.india-route-pin:hover{transform:translate(-50%,-50%) translateY(-2px)}
.india-route-pin .pin-dot{position:absolute;left:10px;top:13px;width:11px;height:11px;border-radius:50%;background:#2c7850;box-shadow:0 0 0 6px rgba(44,120,80,.15)}
.india-route-pin.to .pin-dot{background:#b77728;box-shadow:0 0 0 6px rgba(183,119,40,.15)}
.india-route-pin b{display:block;font-size:10px;color:#2f4937}.india-route-pin small{display:block;margin-top:3px;color:#69756c;font-size:8px;line-height:1.25}
.india-map-badge{position:absolute;left:16px;top:14px;z-index:7;background:rgba(255,255,255,.88);border:1px solid #dce5da;border-radius:11px;padding:9px 11px;box-shadow:0 8px 18px rgba(37,61,45,.09);backdrop-filter:blur(6px)}
.india-map-badge strong{display:block;font-size:9px;letter-spacing:.06em;color:#315741}.india-map-badge span{display:block;margin-top:3px;font-size:8px;color:#68746a}
.india-map-weather{position:absolute;right:16px;top:14px;z-index:7;display:flex;flex-direction:column;gap:3px;background:rgba(255,255,255,.92);border:1px solid #dfe7dd;border-radius:11px;padding:9px 11px;box-shadow:0 8px 18px rgba(37,61,45,.09);backdrop-filter:blur(6px)}
.india-map-weather strong{font-size:9px;color:#355a40}.india-map-weather span,.india-map-weather small{font-size:8px;color:#677269}
.india-route-status{position:absolute;left:16px;bottom:16px;z-index:7;background:rgba(31,72,48,.9);color:#fff;padding:7px 10px;border-radius:999px;font-size:8px;font-weight:800;letter-spacing:.03em;box-shadow:0 8px 18px rgba(32,76,48,.2)}
.india-route-legend{position:absolute;right:16px;bottom:16px;z-index:7;display:flex;gap:12px;flex-wrap:wrap;background:rgba(255,255,255,.87);padding:7px 9px;border-radius:9px;font-size:7.5px;color:#5f6b61}
.india-route-legend span{display:flex;align-items:center;gap:5px}.india-route-legend .legend-dot.route{background:#2f7a55}.india-route-legend .legend-dot.high{background:#b9782c}
.route-checkpoint-row{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px}.route-checkpoint-row>div{padding:10px 12px;border:1px solid #dfe7dc;border-radius:10px;background:linear-gradient(180deg,#fbfcf8,#f1f7ef)}.route-checkpoint-row strong{display:block;margin-top:4px;font-size:13px;color:#315b41}.route-checkpoint-row small{display:block;margin-top:2px;font-size:8px;color:var(--muted)}
/* More polished app-wide background */
.portal main{background:radial-gradient(circle at 12% 8%,rgba(108,164,118,.10),transparent 26%),radial-gradient(circle at 88% 22%,rgba(205,164,70,.08),transparent 24%),linear-gradient(180deg,#f7faf4 0%,#eef4ec 48%,#f7f8f2 100%);position:relative}
.portal .content{position:relative;z-index:1}.portal .content:before{content:'';position:absolute;inset:0;pointer-events:none;opacity:.3;background-image:linear-gradient(rgba(64,94,72,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(64,94,72,.03) 1px,transparent 1px);background-size:32px 32px}
.portal .content>*{position:relative;z-index:2}.portal .card{box-shadow:0 10px 28px rgba(43,71,52,.06);backdrop-filter:blur(2px)}
@media(max-width:900px){.india-route-svg{inset:32px 35px 20px;width:calc(100% - 70px);height:calc(100% - 52px)}.india-route-pin{min-width:118px;max-width:150px}.india-map-weather{right:10px;top:10px}.india-map-badge{left:10px;top:10px}.route-checkpoint-row{grid-template-columns:1fr}}
@media(max-width:650px){.india-route-map{height:460px}.india-route-svg{inset:42px 10px 20px;width:calc(100% - 20px);height:calc(100% - 62px)}.india-route-pin{min-width:110px;max-width:125px;padding:8px 8px 8px 23px}.india-route-pin .pin-dot{left:7px}.india-route-pin.to{transform:translate(-60%,-50%)}.india-route-pin.from{transform:translate(-40%,-50%)}.india-map-weather{max-width:155px}.india-route-status{left:9px;bottom:9px}.india-route-legend{right:9px;bottom:9px}}
'''
css.write_text(css_s)
# Add map attribution note to README
readme=root/'README.md'
rs=readme.read_text()
if 'India-only weather route' not in rs:
    rs += '\n\n### Weather route view\nThe weather dashboard uses a lightweight India-only map with the selected route rendered in the same coordinate system as the map, so the route does not drift when selections change. The map is local UI/data and is intended as a demo route planner, not live turn-by-turn navigation.\n'
    readme.write_text(rs)

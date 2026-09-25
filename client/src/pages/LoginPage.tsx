import {useState} from 'react';
import {Link,useNavigate} from 'react-router-dom';
import {ArrowLeft,Check,Languages,Sprout} from 'lucide-react';
import {Role,useAuthStore} from '../store/auth';
import {getLang,languages,setLang,ui,Lang} from '../i18n';

const accounts={farmer:{email:'farmer@kisansathi.demo',password:'demo1234',name:'Ramesh Kumar'},buyer:{email:'buyer@kisansathi.demo',password:'demo1234',name:'Shakti Foods Pvt Ltd'}};
export default function LoginPage(){
 // Login is intentionally NOT automatic. Every browser load starts signed out.
 const [role,setRole]=useState<Role>('farmer'); const [email,setEmail]=useState(''); const [password,setPassword]=useState(''); const [remember,setRemember]=useState(false); const [error,setError]=useState(''); const [aadhaar,setAadhaar]=useState(''); const [aadhaarVerified,setAadhaarVerified]=useState(false);
 const [lang,setCurrentLang]=useState<Lang>(getLang()); const t=ui[lang]; const login=useAuthStore(s=>s.login); const navigate=useNavigate();
 const changeLang=(v:Lang)=>{setLang(v);setCurrentLang(v)};
 const submit=()=>{setError(''); const a=accounts[role]; if(email.trim().toLowerCase()!==a.email||password!==a.password){setError(t.wrong);return;} setError(''); login({id:`demo-${role}`,name:a.name,role},remember); navigate(`/${role}/dashboard`);};
 return <div className="center login-page"><div className="card login-card">
  <div className="login-language"><Languages size={16}/><span>{t.language}</span><select value={lang} onChange={e=>changeLang(e.target.value as Lang)}>{languages.map(l=><option key={l.key} value={l.key}>{l.native}</option>)}</select></div>
  <Link to="/" className="login-back-home"><ArrowLeft size={14}/> Back to main page</Link><div className="brand-lock"><div className="mark" aria-label="Kissan Sathi"><Sprout size={20} strokeWidth={2.4}/></div><div><strong>KISSAN SATHI</strong><span>Sell smarter from the farm gate</span></div></div>
  <div className="login-kicker">{t.sample}</div><h1>{t.open}</h1><p>{t.credentials}</p>
  <div className="aadhaar-demo"><div><strong>Quick demo: Aadhaar login</strong><span>Prototype verification only — do not enter a real Aadhaar number.</span></div><div className="aadhaar-row"><input inputMode="numeric" maxLength={12} value={aadhaar} onChange={e=>setAadhaar(e.target.value.replace(/\D/g,'').slice(0,12))} placeholder="Demo Aadhaar: 999999999999"/><button type="button" className="table-action" onClick={()=>{if(aadhaar==='999999999999'){setAadhaarVerified(true);setEmail(accounts[role].email);setPassword(accounts[role].password);setError('')}else setError('Use the demo Aadhaar 999999999999 for this prototype.')}}>{aadhaarVerified?'Verified ✓':'Verify demo ID'}</button></div></div>
  <div className="role-toggle">{(['farmer','buyer'] as Role[]).map(r=><button type="button" className={role===r?'selected':''} key={r} onClick={()=>{setRole(r);setEmail('');setPassword('');setAadhaarVerified(false);setAadhaar('');setError('')}}>{r==='farmer'?t.farmer:t.buyer}</button>)}</div>
  <label>{t.email}<input value={email} onChange={e=>setEmail(e.target.value)} placeholder={accounts[role].email} autoComplete="username"/></label>
  <label>{t.password}<input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="demo1234" autoComplete="current-password" onKeyDown={e=>{if(e.key==='Enter')submit()}}/></label>
  {error&&<div className="alert error">{error}</div>}
  <div className="demo-credentials"><strong>{role==='farmer'?t.farmer:t.buyer}</strong><span>{accounts[role].email}</span><span>{accounts[role].password}</span></div>
  <label className="remember-me"><button type="button" className={`remember-box ${remember?'checked':''}`} onClick={()=>setRemember(v=>!v)} aria-pressed={remember} aria-label="Remember me">{remember&&<Check size={12}/>}</button><span>Remember me <small>Stay signed in on this browser</small></span></label>
  <button type="button" className="button full" onClick={submit}>{t.loginButton}</button><small className="muted">{t.credentials}</small>
 </div></div>;
}

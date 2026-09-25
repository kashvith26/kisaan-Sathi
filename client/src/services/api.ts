const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:4000/api';
export async function apiGet<T>(path:string):Promise<T>{ const r=await fetch(`${API_BASE}${path}`); if(!r.ok) throw new Error(`API ${r.status}`); return r.json(); }
export async function apiPost<T>(path:string,body:unknown):Promise<T>{ const r=await fetch(`${API_BASE}${path}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}); if(!r.ok) throw new Error(`API ${r.status}`); return r.json(); }

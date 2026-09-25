import {env} from '../config/env.js';
export async function aiHealth(){const r=await fetch(`${env.AI_SERVICE_URL}/health`); if(!r.ok) throw new Error(`AI service ${r.status}`); return r.json();}

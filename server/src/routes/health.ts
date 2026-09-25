import {Router} from 'express'; import {healthDb} from '../services/db.js'; import {aiHealth} from '../services/aiClient.js';
const r=Router();
r.get('/',async(_req,res)=>{let db:any={ok:false}; let ai:any={ok:false}; try{db=await healthDb()}catch(e){db={ok:false,error:(e as Error).message}} try{ai=await aiHealth()}catch(e){ai={ok:false,error:(e as Error).message}} res.json({service:'server',ok:db.ok&&ai.ok,db,ai})}); export default r;

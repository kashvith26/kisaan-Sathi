import {Router} from 'express'; import {z} from 'zod'; import {issueDemoToken} from '../middleware/auth.js';
const r=Router(); const schema=z.object({email:z.string().email(),password:z.string().min(4),role:z.enum(['farmer','buyer'])});
r.post('/register',(req,res)=>{const p=schema.parse(req.body); const user={id:`demo-${p.role}`,name:p.role==='farmer'?'Ramesh Kumar':'Shakti Buyer',role:p.role};res.status(201).json({user,token:issueDemoToken(user)})});
r.post('/login',(req,res)=>{const p=schema.parse(req.body);const user={id:`demo-${p.role}`,name:p.role==='farmer'?'Ramesh Kumar':'Shakti Buyer',role:p.role};res.json({user,token:issueDemoToken(user)})});
export default r;

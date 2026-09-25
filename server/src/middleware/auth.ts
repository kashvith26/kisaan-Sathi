import {Request,Response,NextFunction} from 'express';
export type AuthUser={sub:string;role:'farmer'|'buyer';name?:string};
declare global{namespace Express{interface Request{auth?:AuthUser}}}
export function issueDemoToken(u:any){return Buffer.from(JSON.stringify({...u,sub:u.sub||u.id,exp:Date.now()+86400000})).toString('base64url');}
export function requireAuth(req:Request,res:Response,next:NextFunction){const h=req.headers.authorization; if(!h?.startsWith('Bearer ')) return res.status(401).json({error:'Authentication required'}); try{req.auth=JSON.parse(Buffer.from(h.slice(7),'base64url').toString());next()}catch{return res.status(401).json({error:'Invalid token'})}}
export function requireRole(role:'farmer'|'buyer'){return (req:Request,res:Response,next:NextFunction)=>req.auth?.role===role?next():res.status(403).json({error:'Forbidden'})}

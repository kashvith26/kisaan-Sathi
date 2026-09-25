import { create } from 'zustand';
export type Role = 'farmer'|'buyer';
export type User = { id:string; name:string; role:Role };
const STORAGE_KEY='kissan-sathi-remembered-user';
function loadRememberedUser():User|null{
  try{
    if(typeof window==='undefined') return null;
    const raw=window.localStorage.getItem(STORAGE_KEY);
    return raw?JSON.parse(raw) as User:null;
  }catch{return null;}
}
type AuthState = { user:User|null; login:(u:User,remember?:boolean)=>void; updateProfile:(patch:Partial<Pick<User,'name'>>) => void; logout:()=>void };
export const useAuthStore=create<AuthState>((set)=>({
  user:loadRememberedUser(),
  login:(user,remember=false)=>{
    try{
      if(typeof window!=='undefined'){
        if(remember) window.localStorage.setItem(STORAGE_KEY,JSON.stringify(user));
        else window.localStorage.removeItem(STORAGE_KEY);
      }
    }catch{}
    set({user});
  },
  updateProfile:(patch)=>set(state=>state.user?{user:{...state.user,...patch}}:state),
  logout:()=>{
    try{if(typeof window!=='undefined') window.localStorage.removeItem(STORAGE_KEY);}catch{}
    set({user:null});
  }
}));

import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './styles.css';

ReactDOM.createRoot(document.getElementById('root')!).render(<React.StrictMode><BrowserRouter><App /></BrowserRouter></React.StrictMode>);
if ('serviceWorker' in navigator) window.addEventListener('load',async()=>{try{const regs=await navigator.serviceWorker.getRegistrations(); for(const r of regs) await r.unregister(); if('caches' in window){const keys=await caches.keys(); await Promise.all(keys.filter(k=>k.toLowerCase().includes('kissan-sathi')).map(k=>caches.delete(k)));}}catch{}});

// NavaBharat AI advertiser marketplace. SELF CONTAINED for Supabase Dashboard editor.
// Set verify_jwt=false; every privileged action checks ADMIN_API_TOKEN or a private booking token.
// @ts-ignore Deno resolves this ESM URL when deployed
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
declare const Deno: {env:{get:(name:string)=>string|undefined},serve:(handler:(req:Request)=>Promise<Response>)=>void};
const cors={'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'authorization,apikey,content-type,x-admin-token','Access-Control-Allow-Methods':'POST,OPTIONS'};
const json=(x:unknown,status=200)=>new Response(JSON.stringify(x),{status,headers:{...cors,'Content-Type':'application/json','Cache-Control':'no-store'}});
const env=(k:string)=>Deno.env.get(k)||'';
const db=()=>createClient(env('SUPABASE_URL'),env('SUPABASE_SERVICE_ROLE_KEY'),{auth:{persistSession:false}});
const clean=(v:unknown,n=200)=>String(v??'').trim().slice(0,n);
const eq=(a:string,b:string)=>{if(a.length!==b.length)return false;let r=0;for(let i=0;i<a.length;i++)r|=a.charCodeAt(i)^b.charCodeAt(i);return r===0};
async function hexSha(s:string){const b=new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s)));return [...b].map(v=>v.toString(16).padStart(2,'0')).join('')}
async function hmac(s:string,key:string){const k=await crypto.subtle.importKey('raw',new TextEncoder().encode(key),{name:'HMAC',hash:'SHA-256'},false,['sign']);const b=new Uint8Array(await crypto.subtle.sign('HMAC',k,new TextEncoder().encode(s)));return [...b].map(x=>x.toString(16).padStart(2,'0')).join('')}
function https(v:unknown){const raw=clean(v,1000);if(!raw)return '';const u=new URL(raw);if(u.protocol!=='https:'||!u.hostname||u.username||u.password)throw Error('Use a normal HTTPS website link.');if(/^(localhost|127\.|10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.|\[)/i.test(u.hostname))throw Error('Use a public website link.');return u.toString()}
function validateVideo(s:string){if(!s)return '';const u=new URL(s),h=u.hostname.toLowerCase().replace(/^www\./,'');if(['youtube.com','m.youtube.com','youtu.be','youtube-nocookie.com','vimeo.com','player.vimeo.com'].includes(h))return s;if(/\.(mp4|webm)(\?|$)/i.test(u.pathname+u.search))return s;throw Error('Video ads require a YouTube, Vimeo, or direct HTTPS MP4/WebM URL.');}
function price(type:string,place:string,days:number){const n=place==='home';if(type==='slideshow')return days===7?(n?199:99):(n?499:299);return days===7?(n?249:149):(n?599:399)}
function authHeader(key:string,secret:string){return 'Basic '+btoa(`${key}:${secret}`)}
async function razorpayOrder(key:string,secret:string,body:any){const r=await fetch('https://api.razorpay.com/v1/orders',{method:'POST',headers:{Authorization:authHeader(key,secret),'Content-Type':'application/json'},body:JSON.stringify(body)});const j=await r.json().catch(()=>({}));if(!r.ok)throw Error('Razorpay order creation failed: '+clean(j.error?.description||r.status,180));return j}
async function requireBooking(d:any,id:unknown,token:unknown){const public_id=clean(id,40),t=clean(token,150);if(!public_id||t.length<30)throw Error('Booking ID and private recovery code are required.');const {data,error}=await d.from('ad_campaigns').select('*').eq('public_id',public_id).maybeSingle();if(error||!data)throw Error('Booking not found.');if(!eq(await hexSha(t),data.recovery_hash))throw Error('Incorrect private recovery code.');return data}
function publicRow(c:any){return {id:c.id,title:c.title,description:c.description,advertiser_name:c.advertiser_name,destination_url:c.destination_url,video_url:c.video_url,format:c.format,placement:c.placement,images:c.images||[],ends_at:c.ends_at}}
function base64bytes(input:string){const b=atob(input);const arr=new Uint8Array(b.length);for(let i=0;i<b.length;i++)arr[i]=b.charCodeAt(i);return arr}
async function signedRow(d:any,c:any){const row=publicRow(c);const paths=(c.images||[]).filter((p:unknown)=>typeof p==='string').slice(0,6);
 const urls=[];for(const path of paths){const {data}=await d.storage.from('ad-campaign-media').createSignedUrl(path,1800);if(data?.signedUrl)urls.push(data.signedUrl)}row.images=urls;return row}
function adminAccess(req:Request){const provided=clean(req.headers.get('x-admin-token'),256);const secret=env('ADMIN_API_TOKEN');if(!secret||!provided||!eq(provided,secret))throw Error('Admin authorization failed.');}
Deno.serve(async req=>{
 if(req.method==='OPTIONS')return new Response('ok',{headers:cors});
 if(req.method!=='POST')return json({error:'POST required'},405);
 try{
  const raw=await req.text();if(raw.length>1600000)return json({error:'Request too large'},413);
  const x=JSON.parse(raw||'{}'),action=clean(x.action,40),d=db(),key=env('RAZORPAY_KEY_ID'),secret=env('RAZORPAY_KEY_SECRET');
  if(action==='public'){
   const {data,error}=await d.from('ad_campaigns').select('id,title,description,advertiser_name,destination_url,video_url,format,placement,images,ends_at').eq('status','active').lte('starts_at',new Date().toISOString()).gt('ends_at',new Date().toISOString()).order('starts_at',{ascending:false}).limit(40);
   if(error)throw error;const result=await Promise.all((data||[]).map(c=>signedRow(d,c)));return json({ads:result});
  }
  if(action==='create'){
   if(env('AD_MARKET_ENABLED')!=='true')throw Error('Advertisement bookings are not enabled yet. The free slideshow maker is still available.');
   if(!key||!secret)throw Error('Razorpay is not configured.');
   const format=clean(x.format,20),placement=clean(x.placement,20),days=Number(x.days);
   if(!['slideshow','video'].includes(format)||!['home','search','jobs','creator','video'].includes(placement)||![7,30].includes(days))throw Error('Invalid advertisement package.');
   const advertiser_name=clean(x.name,90),title=clean(x.title,90),description=clean(x.description,420),email=clean(x.email,120),destination_url=https(x.destination_url),video_url=validateVideo(https(x.video_url));
   if(advertiser_name.length<2||title.length<3||!destination_url||!/^\S+@\S+\.\S+$/.test(email))throw Error('Enter a valid name, headline, destination and email.');
   const dayAgo=new Date(Date.now()-86400000).toISOString();
   const {count:recent,error:rateError}=await d.from('ad_campaigns').select('id',{count:'exact',head:true}).eq('email',email).gte('created_at',dayAgo);
   if(rateError)throw rateError;if(Number(recent||0)>=5)throw Error('Too many bookings for this email today. Try again later.');
   if(format==='video'&&!video_url)throw Error('A YouTube/Vimeo/video link is required.');
   const amt=price(format,placement,days),public_id='AD-'+crypto.randomUUID().slice(0,10).toUpperCase();
   const token=[...crypto.getRandomValues(new Uint8Array(24))].map(v=>v.toString(16).padStart(2,'0')).join('');
   const rr=await razorpayOrder(key,secret,{amount:amt*100,currency:'INR',receipt:public_id,notes:{kind:'nava-ad',ad_id:public_id}});
   const {error}=await d.from('ad_campaigns').insert({public_id,recovery_hash:await hexSha(token),razorpay_order_id:rr.id,advertiser_name,title,description,email,destination_url,video_url,format,placement,duration_days:days,amount_inr:amt,images:[],payment_status:'unpaid',status:'awaiting_payment'});
   if(error)throw error;
   return json({booking_id:public_id,recovery_code:token,razorpay_order_id:rr.id,key_id:key,amount:amt*100,currency:'INR',description:'NavaBharat AI sponsored placement'});
  }
  if(action==='verify'||action==='status'){
   const c=await requireBooking(d,x.booking_id,x.recovery_code);
   if(action==='verify'||(action==='status'&&c.payment_status!=='paid')){
    if(!key||!secret)throw Error('Razorpay is not configured.');
    const paymentId=clean(x.razorpay_payment_id,100),signature=clean(x.razorpay_signature,200);
    if(action==='verify'&&paymentId&&signature){
     if(x.razorpay_order_id!==c.razorpay_order_id||!eq(await hmac(c.razorpay_order_id+'|'+paymentId,secret),signature))throw Error('Invalid payment signature.');
    }
    const r=await fetch('https://api.razorpay.com/v1/orders/'+encodeURIComponent(c.razorpay_order_id),{headers:{Authorization:authHeader(key,secret)}});const j=await r.json().catch(()=>({}));if(!r.ok)throw Error('Unable to check Razorpay payment.');
    const paid=j.status==='paid'&&j.currency==='INR'&&Number(j.amount)===c.amount_inr*100&&Number(j.amount_paid)>=c.amount_inr*100;
    if(paid&&c.payment_status!=='paid'){
     const {error}=await d.from('ad_campaigns').update({payment_status:'paid',status:'pending_review',razorpay_payment_id:paymentId||null,paid_at:new Date().toISOString()}).eq('id',c.id).eq('payment_status','unpaid');if(error)throw error;
    }
    return json({paid:paid||c.payment_status==='paid',status:paid&&c.payment_status!=='paid'?'pending_review':c.status,booking_id:c.public_id});
   }
   return json({paid:c.payment_status==='paid',status:c.status,booking_id:c.public_id});
  }
  if(action==='upload'){
   const c=await requireBooking(d,x.booking_id,x.recovery_code);
   if(c.payment_status!=='paid'||!['pending_review','rejected'].includes(c.status)||c.format!=='slideshow')throw Error('Image uploads are allowed only for paid, unapproved slideshow bookings.');
   const existing=(c.images||[]);if(existing.length>=6)throw Error('Maximum six slideshow photos.');
   const data=clean(x.base64,600000),mime=clean(x.mime,50);if(mime!=='image/jpeg'||data.length>500000||!data)throw Error('Please upload compressed JPEG images under 350 KB.');
   const bytes=base64bytes(data);if(bytes.length>350000||bytes.length<100||bytes[0]!==255||bytes[1]!==216)throw Error('Invalid JPEG image.');
   const path=c.id+'/'+crypto.randomUUID()+'.jpg';
   const {error:upErr}=await d.storage.from('ad-campaign-media').upload(path,bytes,{contentType:'image/jpeg',upsert:false});if(upErr)throw upErr;
   const {error}=await d.from('ad_campaigns').update({images:[...existing,path],status:'pending_review'}).eq('id',c.id).eq('payment_status','paid');if(error){await d.storage.from('ad-campaign-media').remove([path]);throw error;}
   return json({uploaded:true,count:existing.length+1});
  }
  if(action==='admin-list'){
   adminAccess(req);
   const {data,error}=await d.from('ad_campaigns').select('id,public_id,title,advertiser_name,email,description,format,placement,duration_days,amount_inr,payment_status,status,images,video_url,destination_url,starts_at,ends_at,created_at').order('created_at',{ascending:false}).limit(100);if(error)throw error;
   const paid=(data||[]).filter(a=>a.payment_status==='paid');const campaigns=await Promise.all((data||[]).map(async c=>({ ...c,review_urls: await Promise.all((c.images||[]).slice(0,6).map(async p=>(await d.storage.from('ad-campaign-media').createSignedUrl(p,900)).data?.signedUrl||'')) })));
   return json({campaigns,gross_revenue_inr:paid.reduce((n,a)=>n+Number(a.amount_inr||0),0),paid_bookings:paid.length});
  }
  if(action==='admin-update'){
   adminAccess(req);
   const id=clean(x.id,80),status=clean(x.status,20);if(!['active','paused','rejected'].includes(status))throw Error('Invalid status.');
   const {data:c,error}=await d.from('ad_campaigns').select('*').eq('id',id).maybeSingle();if(error||!c)throw Error('Campaign not found.');if(c.payment_status!=='paid')throw Error('Campaign is not paid.');
   if(status==='active'&&c.format==='slideshow'&&!(c.images||[]).length)throw Error('Slideshow has no approved photos.');
   const update:any={status};if(status==='active'&&c.status!=='active'){
    const now=new Date();update.starts_at=now.toISOString();update.ends_at=new Date(now.getTime()+c.duration_days*86400000).toISOString();
   }
   const {error:u}=await d.from('ad_campaigns').update(update).eq('id',id);if(u)throw u;return json({ok:true});
  }
  if(action==='admin-delete-media'){
   adminAccess(req);const id=clean(x.id,80);
   const {data:c}=await d.from('ad_campaigns').select('id,images,status,ends_at').eq('id',id).maybeSingle();if(!c)throw Error('Campaign not found.');
   if(c.status==='active'&&c.ends_at&&new Date(c.ends_at)>new Date())throw Error('Cannot delete an active campaign’s media.');
   const count=(c.images||[]).length;
   if(count){const {error:r}=await d.storage.from('ad-campaign-media').remove(c.images);if(r)throw r;}
   const {error:u}=await d.from('ad_campaigns').update({images:[]}).eq('id',id);if(u)throw u;
   return json({ok:true,deleted:count});
  }
  return json({error:'Unknown action'},400);
 }catch(e){const m=String((e as Error)?.message||e);const status=/authorization|private recovery code|Incorrect private/.test(m)?403:400;console.error('ad-market:',m);return json({error:m.slice(0,230)},status)}
});

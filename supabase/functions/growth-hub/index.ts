// NavaBharat AI Phase 2: affiliate offers, anonymous audience estimates, admin totals.
// Self-contained Edge Function, deployed through Supabase dashboard. verify_jwt=false.
// No new keys. NEVER exposes provider secrets or admin financial data publicly.
// @ts-ignore Deno ESM module import is available in deployed Supabase runtime.
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
declare const Deno:{env:{get:(k:string)=>string|undefined},serve:(h:(r:Request)=>Promise<Response>)=>void};
const CORS={'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'content-type,authorization,apikey,x-admin-token','Access-Control-Allow-Methods':'POST,OPTIONS'};
const reply=(obj:unknown,status=200)=>new Response(JSON.stringify(obj),{status,headers:{...CORS,'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'}});
const env=(s:string)=>Deno.env.get(s)||'';
const db=()=>createClient(env('SUPABASE_URL'),env('SUPABASE_SERVICE_ROLE_KEY'),{auth:{persistSession:false}});
const str=(v:unknown,max=150)=>String(v??'').trim().slice(0,max);
const idok=(v:unknown)=>/^[a-f0-9-]{36}$/i.test(str(v,50));
const today=()=>new Date().toISOString().slice(0,10);
const cutoff=(n:number)=>new Date(Date.now()-n*86400000).toISOString().slice(0,10);
function safeEqual(a:string,b:string){if(a.length!==b.length)return false;let d=0;for(let i=0;i<a.length;i++)d|=a.charCodeAt(i)^b.charCodeAt(i);return d===0}
async function fingerprint(v:unknown){
  // Client token is per day, random and not an account/device identifier.
  const s=str(v,100);if(!/^[a-f0-9-]{32,100}$/i.test(s))throw Error('Invalid anonymous event token.');
  const source=new TextEncoder().encode('nava-growth-v1:'+s);
  const hash=new Uint8Array(await crypto.subtle.digest('SHA-256',source));
  return [...hash].map(n=>n.toString(16).padStart(2,'0')).join('');
}
function checkAdmin(req:Request){
  const supplied=str(req.headers.get('x-admin-token'),256),expected=env('ADMIN_API_TOKEN');
  if(!expected||!supplied||!safeEqual(supplied,expected))throw Error('Admin authorization failed.');
}
function validAffiliateURL(value:unknown){
  const raw=str(value,1800);const u=new URL(raw);
  if(u.protocol!=='https:'||u.username||u.password)throw Error('Affiliate tracking URL must use HTTPS.');
  const h=u.hostname.toLowerCase();
  if(h==='localhost'||h.endsWith('.localhost')||h==='0.0.0.0'||/^(127\.|10\.|192\.168\.|169\.254\.|172\.(1[6-9]|2\d|3[01])\.)/.test(h)||/^\d+\.\d+\.\d+\.\d+$/.test(h))throw Error('Please use a public affiliate tracking link.');
  return u.href;
}
function isOwnSite(value:string){
 try{const h=new URL(value).hostname.toLowerCase();return h==='navabharatai.racharlagpt.in'||h==='racharlagpt.in'||h.endsWith('.racharlagpt.in')}catch{return false}
}
Deno.serve(async req=>{
 if(req.method==='OPTIONS')return new Response('ok',{headers:CORS});
 if(req.method!=='POST')return reply({error:'POST required'},405);
 try{
  const raw=await req.text();if(raw.length>15000)return reply({error:'Request too large'},413);
  const x=JSON.parse(raw||'{}'),action=str(x.action,50),d=db();
  if(action==='offers'){
   const {data,error}=await d.from('nava_affiliate_offers').select('id,title,provider,category,description,affiliate_url').eq('active',true).order('sort_order',{ascending:true}).order('created_at',{ascending:false}).limit(50);
   if(error)throw error;return reply({offers:data||[]});
  }
  if(action==='visit'){
   const hash=await fingerprint(x.token),page=str(x.page,35).replace(/[^a-z0-9_-]/ig,'')||'home';
   const {error}=await d.from('nava_site_visitors').upsert({day:today(),visitor_hash:hash,first_page:page},{onConflict:'day,visitor_hash',ignoreDuplicates:true});
   if(error)throw error;return reply({ok:true});
  }
  if(action==='affiliate-click'){
   if(!idok(x.offer_id))throw Error('Invalid offer ID.');
   const hash=await fingerprint(x.token);
   const {data:offer,error:offerError}=await d.from('nava_affiliate_offers').select('id').eq('id',x.offer_id).eq('active',true).maybeSingle();
   if(offerError||!offer)throw Error('Offer unavailable.');
   const {error}=await d.from('nava_affiliate_clicks').upsert({day:today(),offer_id:offer.id,visitor_hash:hash},{onConflict:'day,offer_id,visitor_hash',ignoreDuplicates:true});
   if(error)throw error;return reply({ok:true});
  }
  // ALL ACTIONS BELOW REQUIRE THE EXACT EXISTING x-admin-token.
  checkAdmin(req);
  if(action==='admin-dashboard'){
   const [financial,traffic,offers,earnings,clicks]=await Promise.all([
    d.rpc('nava_growth_financial_stats'),
    d.rpc('nava_growth_traffic_stats'),
    d.from('nava_affiliate_offers').select('*').order('created_at',{ascending:false}).limit(100),
    d.from('nava_affiliate_earnings').select('*').order('earned_on',{ascending:false}).limit(100),
    d.from('nava_affiliate_clicks').select('offer_id,day').gte('day',cutoff(29)).limit(5000)
   ]);
   for(const r of [financial,traffic,offers,earnings,clicks])if(r.error)throw r.error;
   const clickCount:Record<string,number>={};for(const r of clicks.data||[])clickCount[r.offer_id]=(clickCount[r.offer_id]||0)+1;
   return reply({financial:financial.data,traffic:traffic.data,offers:offers.data||[],earnings:earnings.data||[],clicks30_by_offer:clickCount,click_report_capped:(clicks.data||[]).length===5000,ga4_url:'https://analytics.google.com/'});
  }
  if(action==='admin-list-offers'){
   // Independent of financial RPC calls: Admin can always manage offers if the statistics query fails.
   const {data,error}=await d.from('nava_affiliate_offers').select('id,title,provider,category,description,affiliate_url,active,sort_order,created_at').order('created_at',{ascending:false}).limit(100);
   if(error)throw error;
   return reply({offers:data||[]});
  }
  if(action==='admin-save-offer'){
   const title=str(x.title,100),provider=str(x.provider,65),category=str(x.category,50)||'Learning',description=str(x.description,450),sort_order=Math.min(10000,Math.max(0,Number(x.sort_order)||100));
   if(title.length<3||provider.length<2)throw Error('Enter an offer title and network/provider.');
   const active=!!x.active;
   const rawURL=str(x.url,1800);
   // Drafts can be saved while the network approval is still pending. Only approved links can be public.
   const affiliate_url=rawURL?validAffiliateURL(rawURL):'';
   if(active&&(!affiliate_url||isOwnSite(affiliate_url)||x.approved!==true))throw Error('Publish only a genuine approved partner tracking URL, not your own website. Otherwise save as a draft.');
   const payload={title,provider,category,description,affiliate_url,sort_order:Math.round(sort_order),active,updated_at:new Date().toISOString()};
   if(x.id){if(!idok(x.id))throw Error('Invalid offer ID.');const {data,error}=await d.from('nava_affiliate_offers').update(payload).eq('id',x.id).select('id').maybeSingle();if(error)throw error;if(!data)throw Error('Offer not found.');}
   else {const {error}=await d.from('nava_affiliate_offers').insert(payload);if(error)throw error;}
   return reply({ok:true});
  }
  if(action==='admin-toggle-offer'){
   if(!idok(x.id))throw Error('Invalid offer ID.');
   const active=!!x.active;
   if(active){
    if(x.approved!==true)throw Error('Confirm that this is an approved partner tracking link.');
    const {data:offer,error:lookup}=await d.from('nava_affiliate_offers').select('affiliate_url').eq('id',x.id).maybeSingle();
    if(lookup)throw lookup;if(!offer)throw Error('Offer not found.');
    const url=offer.affiliate_url?validAffiliateURL(offer.affiliate_url):'';
    if(!url||isOwnSite(url))throw Error('Add a genuine approved partner tracking URL before publishing; your website link is not an affiliate offer.');
   }
   const {data,error}=await d.from('nava_affiliate_offers').update({active,updated_at:new Date().toISOString()}).eq('id',x.id).select('id').maybeSingle();
   if(error)throw error;if(!data)throw Error('Offer not found.');
   return reply({ok:true});
  }
  if(action==='admin-delete-offer'){
   if(!idok(x.id))throw Error('Invalid offer ID.');
   const {data:offer,error:lookup}=await d.from('nava_affiliate_offers').select('id,active').eq('id',x.id).maybeSingle();
   if(lookup)throw lookup;if(!offer)throw Error('Offer not found.');
   if(offer.active)throw Error('Unpublish this offer before deleting it.');
   // The existing SQL schema has ON DELETE CASCADE for this offer's click records.
   const {data,error}=await d.from('nava_affiliate_offers').delete().eq('id',x.id).eq('active',false).select('id').maybeSingle();
   if(error)throw error;if(!data)throw Error('Offer not found or still published.');
   return reply({ok:true,deleted:true});
  }
  if(action==='admin-add-earning'){
   const amount=Number(x.amount_inr),provider=str(x.provider,80),income_type=str(x.income_type,20)||'affiliate',earned_on=str(x.earned_on,10),reference_note=str(x.note,280);
   if(!['affiliate','monetag','other'].includes(income_type)||!provider||!Number.isFinite(amount)||amount<0||amount>100000000||!/^\d{4}-\d{2}-\d{2}$/.test(earned_on))throw Error('Enter a valid network, amount and date.');
   const {error}=await d.from('nava_affiliate_earnings').insert({provider,income_type,amount_inr:Math.round(amount*100)/100,earned_on,reference_note,confirmed:!!x.confirmed});if(error)throw error;
   return reply({ok:true});
  }
  if(action==='admin-confirm-earning'){
   if(!idok(x.id))throw Error('Invalid earnings entry ID.');
   const {error}=await d.from('nava_affiliate_earnings').update({confirmed:!!x.confirmed}).eq('id',x.id);if(error)throw error;
   return reply({ok:true});
  }
  if(action==='admin-prune-analytics'){
   // Only anonymous analytics records; never touches orders or media.
   const old=cutoff(30);
   const [v,c]=await Promise.all([d.from('nava_site_visitors').delete().lt('day',old),d.from('nava_affiliate_clicks').delete().lt('day',old)]);
   if(v.error)throw v.error;if(c.error)throw c.error;return reply({ok:true,older_than:old});
  }
  return reply({error:'Unknown action'},400);
 }catch(e){const msg=String((e as Error)?.message||e);console.error('growth-hub:',msg.slice(0,200));return reply({error:msg.includes('authorization')?'Admin authorization failed.':msg.slice(0,220)},msg.includes('authorization')?403:400)}
});

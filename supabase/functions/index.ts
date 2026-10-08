import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
export const cors={'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'authorization, x-client-info, apikey, content-type'};
export const json=(x:any,status=200)=>new Response(JSON.stringify(x),{status,headers:{...cors,'Content-Type':'application/json'}});
export const db=()=>createClient(Deno.env.get('SUPABASE_URL')!,Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!);
export const secret=(n:string)=>Deno.env.get(n)||'';
export const keys=()=>['GEMINI_API_KEY','GEMINI_API_KEY_2','GEMINI_API_KEY_3','GEMINI_AI_KEY_1','GEMINI_AI_KEY_2','GEMINI_AI_KEY_3'].map(secret).filter(Boolean);
export async function geminiText(prompt:string,grounded=false){let last='';const models=[secret('GEMINI_MODEL')||'gemini-3.8-flash','gemini-3.8-flash','gemini-3.7-flash','gemini-3.6-flash','gemini-3.5-flash'].filter((v,i,a)=>v&&a.indexOf(v)===i);for(const key of keys()){for(const model of models){for(const bearer of [false,true]){try{const url=grounded?'https://generativelanguage.googleapis.com/v1beta/interactions':`https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(model)}:generateContent`;const payload=grounded?{model,input:prompt,tools:[{type:'google_search'}]}:{contents:[{parts:[{text:prompt}]}],generationConfig:{temperature:.4}};const headers:any={'Content-Type':'application/json'};if(bearer)headers.Authorization=`Bearer ${key}`;else headers['x-goog-api-key']=key;const r=await fetch(url,{method:'POST',headers,body:JSON.stringify(payload)});const raw=await r.text();if(!r.ok){last=raw.slice(0,500);if((r.status===401||r.status===403)&&bearer)break;continue}const j=JSON.parse(raw);const a=grounded?(j.output_text||j.outputText||''):(j.candidates?.[0]?.content?.parts||[]).map((p:any)=>p.text||'').join('');if(a)return a;last='Empty Gemini response';break}catch(e){last=String(e)}}}}throw Error('Gemini unavailable: '+last)}
export function b64bytes(v:string){return Uint8Array.from(atob(v.replace(/^data:[^,]+,/,'').replace(/\s/g,'')),c=>c.charCodeAt(0))}
export function findAudio(body:any){const out:any[]=[];const walk=(o:any)=>{if(!o)return;if(Array.isArray(o))return o.forEach(walk);if(typeof o==='object'){if(o.audio_url?.url)out.push(o.audio_url.url);if(typeof o.url==='string'&&(o.url.startsWith('data:audio/')||o.url.startsWith('http')))out.push(o.url);if(typeof o.data==='string'&&o.data.length>1000)out.push(o.data);Object.values(o).forEach(walk)}};walk(body);return out[0]||''}
export async function uploadAsset(audio:Uint8Array,mime:string,kind:string){const d=db(),id=crypto.randomUUID(),path=`${kind}/${id}.${mime.includes('wav')?'wav':'mp3'}`;const {error}=await d.storage.from('generated-audio').upload(path,audio,{contentType:mime,upsert:false});if(error)throw error;const {data,error:se}=await d.storage.from('generated-audio').createSignedUrl(path,3600);if(se)throw se;return {id,path,url:data.signedUrl}}

Deno.serve(async req=>{if(req.method==='OPTIONS')return new Response('ok',{headers:cors});try{
 const token=req.headers.get('x-admin-token')||''; if(!token||token!==secret('ADMIN_API_TOKEN'))throw Error('Unauthorized');
 const x=await req.json(); if(!x.data)throw Error('Audio file required');
 const d=db(), id=crypto.randomUUID(); const bytes=b64bytes(x.data); if(bytes.length>25*1024*1024)throw Error('File too large (25 MB maximum)');
 const ext=(x.mime||'audio/mpeg').includes('wav')?'wav':(x.mime||'').includes('ogg')?'ogg':'mp3';
 if(x.type==='music'){
   const path=`music/${id}.${ext}`; const up=await d.storage.from('music-library').upload(path,bytes,{contentType:x.mime||'audio/mpeg',upsert:false}); if(up.error)throw up.error;
   const publicUrl=`${Deno.env.get('SUPABASE_URL')}/storage/v1/object/public/music-library/${path}`; const {data,error}=await d.from('music_library').insert({id,title:x.title||`Track ${id.slice(0,8)}`,audio_path:path,audio_url:publicUrl,preview_url:publicUrl,language:x.language||null,genre:x.genre||null,published:true}).select().single(); if(error)throw error;
   return json({ok:true,item:data});
 }
 if(x.type==='ringtone'){
   if(!x.rights_confirmed||!x.license)throw Error('Rights confirmation and license/permission reference are required');
   const full=`ringtones/${id}.${ext}`; const up=await d.storage.from('ringtone-full').upload(full,bytes,{contentType:x.mime||'audio/mpeg',upsert:false}); if(up.error)throw up.error;
   const prev=`ringtones/${id}-preview.${ext}`; const pv=await d.storage.from('ringtone-preview').upload(prev,bytes,{contentType:x.mime||'audio/mpeg',upsert:false}); if(pv.error)throw pv.error; const regular=Math.max(10,Number(x.regular_price_inr||20)); const offer=Math.max(10,Number(x.price_inr||10)); if(offer>regular)throw Error('Offer price cannot exceed regular price'); const {data,error}=await d.from('ringtones').insert({id,title:x.title||`Ringtone ${id.slice(0,8)}`,movie:x.movie||null,artist:x.artist||null,language:x.language||'English',category:x.category||'Ringtone',full_path:full,preview_path:prev,source_license:x.license,rights_confirmed:true,regular_price_inr:regular,price_inr:offer,active:true}).select().single(); if(error)throw error;
   return json({ok:true,item:data});
 }
 throw Error('Unknown upload type');
}catch(e){return json({error:String(e.message||e)},403)}});
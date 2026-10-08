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
 const d=db(); const [r,m]=await Promise.all([
  d.from('ringtones').select('id,title,movie,artist,language,category,price_inr,active,created_at').order('created_at',{ascending:false}),
  d.from('music_library').select('id,title,language,genre,published,created_at').order('created_at',{ascending:false})
 ]);
 if(r.error)throw r.error;if(m.error)throw m.error;return json({ringtones:r.data||[],music:m.data||[]});
}catch(e){return json({error:String(e.message||e)},403)}});

import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
export const cors={'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'authorization, x-client-info, apikey, content-type, x-admin-token'};
export const json=(x:any,status=200)=>new Response(JSON.stringify(x),{status,headers:{...cors,'Content-Type':'application/json'}});
export const db=()=>createClient(Deno.env.get('SUPABASE_URL')!,Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!);
export const secret=(n:string)=>Deno.env.get(n)||'';
export const keys=()=>['GEMINI_API_KEY','GEMINI_API_KEY_2','GEMINI_API_KEY_3','GEMINI_AI_KEY_1','GEMINI_AI_KEY_2','GEMINI_AI_KEY_3'].map(secret).filter(Boolean);
export async function geminiText(prompt:string,grounded=false){let last='';const models=[secret('GEMINI_MODEL')||'gemini-3.8-flash','gemini-3.8-flash','gemini-3.7-flash','gemini-3.6-flash','gemini-3.5-flash'].filter((v,i,a)=>v&&a.indexOf(v)===i);for(const key of keys()){for(const model of models){for(const bearer of [false,true]){try{const url=grounded?'https://generativelanguage.googleapis.com/v1beta/interactions':`https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(model)}:generateContent`;const payload=grounded?{model,input:prompt,tools:[{type:'google_search'}]}:{contents:[{parts:[{text:prompt}]}],generationConfig:{temperature:.4}};const headers:any={'Content-Type':'application/json'};if(bearer)headers.Authorization=`Bearer ${key}`;else headers['x-goog-api-key']=key;const r=await fetch(url,{method:'POST',headers,body:JSON.stringify(payload)});const raw=await r.text();if(!r.ok){last=raw.slice(0,500);if((r.status===401||r.status===403)&&bearer)break;continue}const j=JSON.parse(raw);const a=grounded?(j.output_text||j.outputText||''):(j.candidates?.[0]?.content?.parts||[]).map((p:any)=>p.text||'').join('');if(a)return a;last='Empty Gemini response';break}catch(e){last=String(e)}}}}throw Error('Gemini unavailable: '+last)}
export function b64bytes(v:string){return Uint8Array.from(atob(v.replace(/^data:[^,]+,/,'').replace(/\s/g,'')),c=>c.charCodeAt(0))}
export function findAudio(body:any){const out:any[]=[];const walk=(o:any)=>{if(!o)return;if(Array.isArray(o))return o.forEach(walk);if(typeof o==='object'){if(o.audio_url?.url)out.push(o.audio_url.url);if(typeof o.url==='string'&&(o.url.startsWith('data:audio/')||o.url.startsWith('http')))out.push(o.url);if(typeof o.data==='string'&&o.data.length>1000)out.push(o.data);Object.values(o).forEach(walk)}};walk(body);return out[0]||''}
export async function uploadAsset(audio:Uint8Array,mime:string,kind:string){const d=db(),id=crypto.randomUUID(),path=`${kind}/${id}.${mime.includes('wav')?'wav':'mp3'}`;const {error}=await d.storage.from('generated-audio').upload(path,audio,{contentType:mime,upsert:false});if(error)throw error;const {data,error:se}=await d.storage.from('generated-audio').createSignedUrl(path,3600);if(se)throw se;return {id,path,url:data.signedUrl}}

const langs:any={English:['en-IN','IN','en'],Telugu:['te-IN','IN','te'],Hindi:['hi-IN','IN','hi'],Tamil:['ta-IN','IN','ta'],Kannada:['kn-IN','IN','kn'],Malayalam:['ml-IN','IN','ml']};
Deno.serve(async req=>{
 if(req.method==='OPTIONS')return new Response('ok',{headers:cors});
 try{
  const x=await req.json();const lang=String(x.language||'English');const q=String(x.query||'India').trim()||'India';const limit=Math.min(20,Math.max(5,Number(x.limit||12)));
  const langs:any={English:['en-IN','IN','en'],Telugu:['te-IN','IN','te'],Hindi:['hi-IN','IN','hi'],Tamil:['ta-IN','IN','ta'],Kannada:['kn-IN','IN','kn'],Malayalam:['ml-IN','IN','ml']};
  const [hl,gl,ceid]=langs[lang]||langs.English;
  // Primary: Google News RSS. If Google is unavailable, use GDELT's live article-list JSON.
  try{
   const u='https://news.google.com/rss/search?q='+encodeURIComponent(q)+'&hl='+hl+'&gl='+gl+'&ceid='+ceid;
   const r=await fetch(u,{headers:{'User-Agent':'NavaBharatAI/1.0 news-reader'},signal:AbortSignal.timeout(8000)});
   if(r.ok){
    const xml=await r.text();
    const items=[...xml.matchAll(/<item>([\s\S]*?)<\/item>/g)].slice(0,limit).map(m=>{const b=m[1];const get=(tag:string)=>{const z=b.match(new RegExp('<'+tag+'>([\\s\\S]*?)<\\/'+tag+'>'));return z?z[1].replace(/<!\[CDATA\[|\]\]>/g,'').trim():''};return {title:get('title'),link:get('link'),pubDate:get('pubDate'),source:get('source')}}).filter(x=>x.title&&x.link);
    if(items.length)return json({items,provider:'Google News'});
   }
  }catch{}
  const gd='https://api.gdeltproject.org/api/v2/doc/doc?query='+encodeURIComponent(q)+'&mode=artlist&format=json&maxrecords='+limit+'&timespan=1d&sort=datedesc';
  try{
    const gr=await fetch(gd,{headers:{'User-Agent':'NavaBharatAI/1.0 news-reader'},signal:AbortSignal.timeout(8000)});
    if(gr.ok){
      const gj=await gr.json();const items=(gj.articles||[]).map((a:any)=>({title:a.title||a.name||'',link:a.url||a.documentidentifier||'',pubDate:a.seendate||a.date||'',source:a.domain||a.sourcecountry||'News'})).filter((x:any)=>x.title&&x.link).slice(0,limit);
      if(items.length)return json({items,provider:'GDELT'});
    }
  }catch{}
  // Final server-side fallback: Gemini web grounding. Provider keys remain server-side.
  for(const key of keys()){
    try{
      const r=await fetch('https://generativelanguage.googleapis.com/v1beta/interactions',{method:'POST',headers:{'Content-Type':'application/json','x-goog-api-key':key},signal:AbortSignal.timeout(20000),body:JSON.stringify({
        model:'gemini-3.8-flash',
        input:`Find the latest ${limit} news headlines for "${q}" in ${lang}. Return JSON only as an array of objects with title, url, source and published fields. Use real source URLs from web search; never invent URLs.`,
        tools:[{type:'google_search'}]
      })});
      if(!r.ok)continue;
      const j=await r.json();
      const text=j.output_text||j.outputText||j.steps?.flatMap((s:any)=>s.content||[]).filter((c:any)=>c.type==='text').map((c:any)=>c.text||'').join('')||'';
      const m=text.match(/\[[\s\S]*\]/); if(!m)continue;
      const arr=JSON.parse(m[0]);
      const items=Array.isArray(arr)?arr.map((a:any)=>({title:String(a.title||''),link:String(a.url||''),pubDate:String(a.published||''),source:String(a.source||'Web Search')})).filter((x:any)=>x.title&&/^https?:\/\//.test(x.link)).slice(0,limit):[];
      if(items.length)return json({items,provider:'Gemini Search'});
    }catch{}
  }
  throw Error('Live news feeds are temporarily unavailable.');
 }catch(e){return json({error:String(e.message||e)},502)}
});

import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
export const cors={'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'authorization, x-client-info, apikey, content-type, x-admin-token'};
export const json=(x:any,status=200)=>new Response(JSON.stringify(x),{status,headers:{...cors,'Content-Type':'application/json'}});
export const db=()=>createClient(Deno.env.get('SUPABASE_URL')!,Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!);
export const secret=(n:string)=>Deno.env.get(n)||'';
export const keys=()=>['GEMINI_API_KEY','GEMINI_API_KEY_2','GEMINI_API_KEY_3','GEMINI_AI_KEY_1','GEMINI_AI_KEY_2','GEMINI_AI_KEY_3'].map(secret).filter(Boolean);
export async function geminiText(prompt:string,grounded=false){let last='';const models=[secret('GEMINI_MODEL')||'gemini-3.8-flash','gemini-3.8-flash','gemini-3.7-flash','gemini-3.6-flash','gemini-3.5-flash'].filter((v,i,a)=>v&&a.indexOf(v)===i);for(const key of keys()){for(const model of models){for(const bearer of [false,true]){try{const url=grounded?'https://generativelanguage.googleapis.com/v1beta/interactions':`https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(model)}:generateContent`;const payload=grounded?{model,input:prompt,tools:[{type:'google_search'}]}:{contents:[{parts:[{text:prompt}]}]};const headers:any={'Content-Type':'application/json'};if(bearer)headers.Authorization=`Bearer ${key}`;else headers['x-goog-api-key']=key;const r=await fetch(url,{method:'POST',headers,body:JSON.stringify(payload)});const raw=await r.text();if(!r.ok){last=raw.slice(0,500);if((r.status===401||r.status===403)&&bearer)break;continue}const j=JSON.parse(raw);const a=grounded?(j.output_text||j.outputText||''):(j.candidates?.[0]?.content?.parts||[]).map((p:any)=>p.text||'').join('');if(a)return a;last='Empty Gemini response';break}catch(e){last=String(e)}}}}throw Error('Gemini unavailable: '+last)}
export function b64bytes(v:string){return Uint8Array.from(atob(v.replace(/^data:[^,]+,/,'').replace(/\s/g,'')),c=>c.charCodeAt(0))}
export function findAudio(body:any){const out:any[]=[];const walk=(o:any)=>{if(!o)return;if(Array.isArray(o))return o.forEach(walk);if(typeof o==='object'){if(o.audio_url?.url)out.push(o.audio_url.url);if(typeof o.url==='string'&&(o.url.startsWith('data:audio/')||o.url.startsWith('http')))out.push(o.url);if(typeof o.data==='string'&&o.data.length>1000)out.push(o.data);Object.values(o).forEach(walk)}};walk(body);return out[0]||''}
export async function uploadAsset(audio:Uint8Array,mime:string,kind:string){const d=db(),id=crypto.randomUUID(),path=`${kind}/${id}.${mime.includes('wav')?'wav':'mp3'}`;const {error}=await d.storage.from('generated-audio').upload(path,audio,{contentType:mime,upsert:false});if(error)throw error;const {data,error:se}=await d.storage.from('generated-audio').createSignedUrl(path,600);if(se)throw se;return {id,path,url:data.signedUrl}}

async function ace(lyrics:string,style:string,lang:string,duration:number,vocal:string){const key=secret('ACESTEP_API_KEY')||secret('ACE_API_KEY')||secret('ACE_APP_KEY');if(!key)throw Error('ACE key not configured');const base='https://api.acemusic.ai';const body={model:'acemusic/acestep-v1.5-turbo',messages:[{role:'user',content:`<prompt>Create a complete original ${style} audio piece. Use ${vocal}. Perform the supplied original idea/lyrics naturally in ${lang}. Polished beginning and ending.</prompt>\n<lyrics>${lyrics}</lyrics>`}],audio_config:{format:'mp3',vocal_language:lang,instrumental:vocal==='Instrumental',duration},use_cot_caption:false};const r=await fetch(base+'/v1/chat/completions',{method:'POST',headers:{Authorization:`Bearer ${key}`,'Content-Type':'application/json'},body:JSON.stringify(body)});if(!r.ok)throw Error('ACE HTTP '+r.status+': '+(await r.text()).slice(0,400));const u=findAudio(await r.json());if(!u)throw Error('ACE returned no audio');if(u.startsWith('http')){const a=await fetch(u);return {bytes:new Uint8Array(await a.arrayBuffer()),mime:a.headers.get('content-type')||'audio/mpeg'}}return {bytes:Uint8Array.from(atob(u.split(',').pop()!),c=>c.charCodeAt(0)),mime:u.includes('wav')?'audio/wav':'audio/mpeg'}}
async function lyria(lyrics:string,style:string,lang:string,duration:number,vocal:string){
  let last='';
  for(const key of keys()){
    for(const authMode of ['api-key','bearer']){
      try{
        const headers:any={'Content-Type':'application/json'};
        if(authMode==='api-key')headers['x-goog-api-key']=key;else headers['Authorization']=`Bearer ${key}`;
        const r=await fetch('https://generativelanguage.googleapis.com/v1beta/interactions',{
          method:'POST',headers,signal:AbortSignal.timeout(120000),
          body:JSON.stringify({model:secret('GEMINI_MUSIC_MODEL')||'lyria-3.5',input:`Create an original finished song in ${lang}. Style: ${style}. Vocal arrangement: ${vocal}. Approx ${duration}s. Original user idea/lyrics:
${lyrics}`,response_format:{type:'audio'}})
        });
        const raw=await r.text();
        if(!r.ok){last=raw.slice(0,450);continue}
        const j=JSON.parse(raw);
        const b=j.output_audio?.data||j.outputAudio?.data||j.output?.find?.((x:any)=>x.type==='audio')?.data||j.steps?.flatMap((x:any)=>x.content||[]).find((x:any)=>x.type==='audio')?.data;
        if(b)return {bytes:Uint8Array.from(atob(b),c=>c.charCodeAt(0)),mime:j.output_audio?.mime_type||j.outputAudio?.mime_type||'audio/mpeg'};
        last='Lyria returned no audio';
      }catch(e){last=String(e)}
    }
  }
  throw Error('Gemini Lyria failed: '+last)
}
async function apiFrame(lyrics:string,style:string,vocal:string){const key=secret('APIFRAME_API_KEY');if(!key)throw Error('APIFrame key not configured');const base='https://api.apiframe.ai/v2';const p:any={custom_mode:true,instrumental:vocal==='Instrumental',style,title:'NavaBharat AI Song'};const r=await fetch(base+'/music/generate',{method:'POST',headers:{'X-API-Key':key,'Content-Type':'application/json'},body:JSON.stringify({model:'suno',prompt:lyrics.slice(0,3000),sunoParams:p})});if(!r.ok)throw Error('APIFrame HTTP '+r.status);const j=await r.json();const id=j.id||j.job_id||j.jobId||j.task_id;if(!id)throw Error('APIFrame no job id');for(let i=0;i<40;i++){await new Promise(r=>setTimeout(r,5000));const q=await fetch(base+'/jobs/'+id,{headers:{'X-API-Key':key}});if(!q.ok)continue;const b=await q.json();const u=b.audioUrl||b.audio_url||b.audio;if(u){const a=await fetch(u);return {bytes:new Uint8Array(await a.arrayBuffer()),mime:'audio/mpeg'}}if(['failed','error','cancelled'].includes(String(b.status||b.state).toLowerCase()))break}throw Error('APIFrame generation timed out')}

async function generateGeminiImage(prompt:string,aspect_ratio:string='1:1',image_size:string='1K'){
  let last='No image response from Gemini';
  const models=['gemini-nano-banana-2.1','gemini-3.1-flash-image','gemini-2.5-flash-image'];
  for(const key of keys()){
    for(const model of models){
      for(const authMode of ['api-key','bearer']){
        try{
          const headers:any={'Content-Type':'application/json'};
          if(authMode==='api-key')headers['x-goog-api-key']=key;else headers['Authorization']=`Bearer ${key}`;
          const r=await fetch(`https://generativelanguage.googleapis.com/v1/models/${model}:generateContent`,{
            method:'POST',headers,signal:AbortSignal.timeout(60000),
            body:JSON.stringify({
              contents:[{parts:[{text:`${prompt}\nAspect ratio: ${aspect_ratio}. Image size target: ${image_size}.` }]}],
              generationConfig:{responseModalities:['TEXT','IMAGE']}
            })
          });
          const raw=await r.text();
          if(!r.ok){last=`${model} HTTP ${r.status}: ${raw.slice(0,350)}`;continue}
          const j=JSON.parse(raw);
          const parts=j.candidates?.[0]?.content?.parts||[];
          const part=parts.find((x:any)=>x.inlineData?.data||x.inline_data?.data);
          const data=part?.inlineData?.data||part?.inline_data?.data;
          const mime=part?.inlineData?.mimeType||part?.inline_data?.mime_type||'image/png';
          if(data)return {bytes:Uint8Array.from(atob(data),c=>c.charCodeAt(0)),mime,model};
          last=`${model} returned no inline image data`;
        }catch(e){last=String(e)}
      }
    }
  }
  throw Error('AI image generation failed: '+last);
}
async function uploadGeneratedImage(bytes:Uint8Array,kind:string,mime='image/png'){
  const d=db(),id=crypto.randomUUID(),path=`${kind}/${id}.png`;
  const {error}=await d.storage.from('generated-images').upload(path,bytes,{contentType:mime,upsert:false});
  if(error)throw error;
  const {data,error:se}=await d.storage.from('generated-images').createSignedUrl(path,600);
  if(se)throw se;
  return {id,path,url:data.signedUrl};
}
Deno.serve(async req=>{
 if(req.method==='OPTIONS')return new Response('ok',{headers:cors});
 try{
  const x=await req.json();
  const {kind,lyrics,language='English',style='',duration=15,vocal_type='Instrumental',admin_test=false,test_provider=''}=x;
  if(admin_test){const token=req.headers.get('x-admin-token')||'';if(!token||token!==secret('ADMIN_API_TOKEN'))throw Error('Unauthorized')}
  if(kind==='design'||kind==='3d-design'){
    const title=String(x.title||'').trim(),subtitle=String(x.subtitle||'').trim(),footer=String(x.footer||'NavaBharat AI').trim();
    if(!title)throw Error('Design headline is required');
    const ratio=String(x.aspect_ratio||'1:1'), size=String(x.image_size||'1K');
    const designPrompt=kind==='3d-design'
      ? `Create a premium commercial 3D typography poster. Exact headline text: "${title}". Supporting text: "${subtitle}". Footer: "${footer}". Style: ${style||'cinematic luxury 3D'}. Background: ${x.background||'dark premium studio'}. Make the headline the hero, physically dimensional extruded lettering, realistic reflections, depth, rim lighting, tasteful particles, strong hierarchy, polished advertising art direction, no placeholder text, no UI, no watermark, no mockup. Aspect ratio ${ratio}.`
      : `Create a premium professional advertising poster for this exact customer request. Exact headline text: "${title}". Supporting text: "${subtitle}". Footer/brand: "${footer}". Theme: ${style||'modern Indian premium editorial'}. Use a rich AI-generated scene/background relevant to the customer's wording, sophisticated composition, realistic lighting, depth, cinematic color grading, strong visual hierarchy, elegant typography, commercial-quality social media design, no UI, no mockup, no placeholder text, no watermark. Aspect ratio ${ratio}.`;
    const img=await generateGeminiImage(designPrompt,ratio,size);
    const up=await uploadGeneratedImage(img.bytes,kind);
    const d=db();
    const {data,error}=await d.from('generated_assets').insert({id:up.id,kind,storage_path:up.path,preview_path:up.path,provider:'gemini-image',metadata:{language,style,aspect_ratio:ratio,image_size:size,title,subtitle,footer}}).select().single();
    if(error)throw error;
    return json({asset_id:data.id,preview_url:up.url,provider:'Gemini Image'});
  }
  const providers=(admin_test&&test_provider?[test_provider]:(secret('MUSIC_PROVIDER_ORDER')||'acestep,gemini,apiframe').split(',').map(x=>x.trim()));
  let audio:any=null,last='',used='';
  for(const p of providers){try{
    audio=p==='acestep'?await ace(lyrics,style,language,Math.min(Number(duration),60),vocal_type):p==='gemini'?await lyria(lyrics,style,language,Math.min(Number(duration),60),vocal_type):await apiFrame(lyrics,style,vocal_type);
    if(audio){used=p;break}
  }catch(e){last=String(e)}}
  if(!audio)throw Error('All music providers failed. '+last);
  const up=await uploadAsset(audio.bytes,audio.mime,kind==='ringtone'?'ringtones-generated':'songs');
  const client=db();
  const {data,error}=await client.from('generated_assets').insert({id:up.id,kind,storage_path:up.path,preview_path:up.path,provider:used,metadata:{language,style,duration}}).select().single();
  if(error)throw error;
  return json({asset_id:data.id,preview_url:up.url,provider:data.provider});
 }catch(e){return json({error:String(e.message||e)},500)}
});

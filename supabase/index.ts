import {createClient} from 'https://esm.sh/@supabase/supabase-js@2';
const cors={'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'authorization, x-client-info, apikey, content-type, x-admin-token','Cache-Control':'no-store'};
const j=(value:any,status=200)=>new Response(JSON.stringify(value),{status,headers:{...cors,'Content-Type':'application/json'}});
Deno.serve(async req=>{if(req.method==='OPTIONS')return new Response('ok',{headers:cors});
try{
 const d=createClient(Deno.env.get('SUPABASE_URL')!,Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!);
 const input=req.method==='POST'?await req.json():{};
 if(req.method==='POST'&&input.action==='set'){
  const expected=Deno.env.get('ADMIN_API_TOKEN')||Deno.env.get('ADMIN_TOKEN');
  if(!expected || req.headers.get('x-admin-token')!==expected)return j({error:'Unauthorized'},403);
  if(typeof input.enabled!=='boolean')return j({error:'enabled must be boolean'},400);
  const message=String(input.message||'We are improving NavaBharat AI. Please visit again shortly.').slice(0,250);
  const {error}=await d.from('nava_site_settings').update({maintenance_enabled:input.enabled,maintenance_message:message,updated_at:new Date().toISOString()}).eq('id',1);if(error)throw error;
 }
 const {data,error}=await d.from('nava_site_settings').select('maintenance_enabled,maintenance_message,updated_at').eq('id',1).single();if(error)throw error;
 return j({maintenance:!!data.maintenance_enabled,message:data.maintenance_message,updated_at:data.updated_at});
}catch(e){return j({error:String((e as Error).message||e)},503)}});

import {cors,json,db,secret} from './_shared.ts';
Deno.serve(async req=>{if(req.method==='OPTIONS')return new Response('ok',{headers:cors});try{
 const token=req.headers.get('x-admin-token')||'';if(!token||token!==secret('ADMIN_API_TOKEN'))throw Error('Unauthorized');
 const {id}=await req.json();const d=db();const {error}=await d.from('music_library').update({published:false}).eq('id',id);if(error)throw error;return json({ok:true});
}catch(e){return json({error:String(e.message||e)},403)}});

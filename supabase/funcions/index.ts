import {cors,json,db,secret} from '../_shared.ts';
Deno.serve(async req=>{if(req.method==='OPTIONS')return new Response('ok',{headers:cors});try{
 const token=req.headers.get('x-admin-token')||''; if(!token||token!==secret('ADMIN_API_TOKEN'))throw Error('Unauthorized');
 const d=db(); const [r,m]=await Promise.all([
  d.from('ringtones').select('id,title,movie,artist,language,category,price_inr,active,created_at').order('created_at',{ascending:false}),
  d.from('music_library').select('id,title,language,genre,published,created_at').order('created_at',{ascending:false})
 ]);
 if(r.error)throw r.error;if(m.error)throw m.error;return json({ringtones:r.data||[],music:m.data||[]});
}catch(e){return json({error:String(e.message||e)},403)}});
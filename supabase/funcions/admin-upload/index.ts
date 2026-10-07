import {cors,json,db,secret,b64bytes} from '../_shared.ts';
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

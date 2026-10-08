import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
export const cors={'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'authorization, x-client-info, apikey, content-type, x-admin-token'};
export const json=(x:any,status=200)=>new Response(JSON.stringify(x),{status,headers:{...cors,'Content-Type':'application/json'}});
export const db=()=>createClient(Deno.env.get('SUPABASE_URL')!,Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!);
export const secret=(n:string)=>Deno.env.get(n)||'';

Deno.serve(async req=>{
 if(req.method==='OPTIONS')return new Response('ok',{headers:cors});
 try{
  const {kind,item_id,asset_id,amount,customer}=await req.json();
  const d=db(); let amt=Number(amount);
  if(kind==='ringtone'){
    if(item_id){
      const {data:r,error}=await d.from('ringtones').select('id,price_inr,active').eq('id',item_id).single();
      if(error)throw error;if(!r||!r.active)throw Error('Ringtone unavailable');
      amt=Math.max(10,Number(r.price_inr||10));
    }else if(asset_id){
      const {data:a,error}=await d.from('generated_assets').select('id,kind').eq('id',asset_id).single();
      if(error)throw error;if(!a||a.kind!=='ringtone')throw Error('Generated ringtone asset not found');
      amt=10;
    }else throw Error('Ringtone item is required');
  }else if(kind==='song'){
    if(!asset_id)throw Error('Song asset is required');
    const {data:a,error}=await d.from('generated_assets').select('id,kind').eq('id',asset_id).single();
    if(error)throw error;if(!a||a.kind!=='song')throw Error('Song asset not found');
    amt=19;
  }else if(kind==='design'){
    if(!asset_id)throw Error('Design asset is required');
    const {data:a,error}=await d.from('generated_assets').select('id,kind').eq('id',asset_id).single();
    if(error)throw error;if(!a||!['design','3d-design'].includes(a.kind))throw Error('Design asset not found');
    amt=9;
  }else if(kind==='tip'||kind==='gift'){
    amt=Number(amount);
  }
  if(!amt||amt<1||(kind==='ringtone'&&amt<10)||(kind==='song'&&amt<19)||(kind==='design'&&amt<9))throw Error('Invalid payment amount');
  const key=secret('RAZORPAY_KEY_ID'),sec=secret('RAZORPAY_KEY_SECRET');
  if(!key||!sec)throw Error('Razorpay keys are not configured in Supabase');
  const publicId='NAVA-'+crypto.randomUUID().slice(0,8).toUpperCase();
  const auth=btoa(`${key}:${sec}`);
  const rr=await fetch('https://api.razorpay.com/v1/orders',{method:'POST',headers:{Authorization:`Basic ${auth}`,'Content-Type':'application/json'},body:JSON.stringify({
    amount:Math.round(amt*100),currency:'INR',receipt:publicId,notes:{nava_order_id:publicId,kind:String(kind)}
  })});
  const rj=await rr.json();if(!rr.ok)throw Error(rj.error?.description||rj.error?.code||'Razorpay order creation failed');
  const {data:o,error}=await d.from('orders').insert({
    public_order_id:publicId,kind,item_id:item_id||null,asset_id:asset_id||null,amount_inr:amt,
    razorpay_order_id:rj.id,customer_email:customer?.email||null,customer_data:customer||{}
  }).select().single();
  if(error)throw error;
  return json({order_id:publicId,razorpay_order_id:rj.id,key_id:key,amount:Math.round(amt*100),currency:'INR',description:`NavaBharat AI ${kind} — ₹${amt}`});
 }catch(e){return json({error:String(e.message||e)},500)}
});

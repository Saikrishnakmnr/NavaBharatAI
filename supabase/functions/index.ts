import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
export const cors={'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'authorization, x-client-info, apikey, content-type, x-admin-token'};
export const json=(x:any,status=200)=>new Response(JSON.stringify(x),{status,headers:{...cors,'Content-Type':'application/json'}});
export const db=()=>createClient(Deno.env.get('SUPABASE_URL')!,Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!);
export const secret=(n:string)=>Deno.env.get(n)||'';
Deno.serve(async req=>{
 if(req.method==='OPTIONS')return new Response('ok',{headers:cors});
 try{
  const {order_id}=await req.json();const d=db();
  const {data:o,error}=await d.from('orders').select('*').eq('public_order_id',String(order_id||'')).single();
  if(error||!o)throw Error('Order not found');
  if(o.razorpay_status!=='paid'&&o.razorpay_order_id){
    const key=secret('RAZORPAY_KEY_ID'),sec=secret('RAZORPAY_KEY_SECRET');if(!key||!sec)throw Error('Razorpay keys are not configured');
    const r=await fetch('https://api.razorpay.com/v1/orders/'+encodeURIComponent(o.razorpay_order_id),{headers:{Authorization:`Basic ${btoa(`${key}:${sec}`)}`}});
    const j=await r.json();if(r.ok&&j.status==='paid'&&Number(j.amount_paid||0)>=Number(o.amount_inr)*100){
      const now=new Date();o.razorpay_status='paid';
      await d.from('orders').update({razorpay_status:'paid',paid_at:now.toISOString()}).eq('id',o.id);
      if(['ringtone','song','design'].includes(o.kind)){
        const {data:existing}=await d.from('download_entitlements').select('id').eq('order_id',o.id).maybeSingle();
        if(!existing)await d.from('download_entitlements').insert({order_id:o.id,item_id:o.item_id||null,asset_id:o.asset_id||null,expires_at:new Date(now.getTime()+30*864e5).toISOString()});
      }
    }
  }
  return json({order_id:o.public_order_id,paid:o.razorpay_status==='paid',kind:o.kind,message:o.razorpay_status==='paid'?'Payment confirmed':'Payment pending'});
 }catch(e){return json({error:String(e.message||e)},404)}
});

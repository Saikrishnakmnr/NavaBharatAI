import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
export const cors={'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'authorization, x-client-info, apikey, content-type, x-admin-token'};
export const json=(x:any,status=200)=>new Response(JSON.stringify(x),{status,headers:{...cors,'Content-Type':'application/json'}});
export const db=()=>createClient(Deno.env.get('SUPABASE_URL')!,Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!);
export const secret=(n:string)=>Deno.env.get(n)||'';

async function hmacHex(message:string,keyText:string){
 const key=await crypto.subtle.importKey('raw',new TextEncoder().encode(keyText),{name:'HMAC',hash:'SHA-256'},false,['sign']);
 const sig=new Uint8Array(await crypto.subtle.sign('HMAC',key,new TextEncoder().encode(message)));
 return [...sig].map(b=>b.toString(16).padStart(2,'0')).join('');
}
function safeEq(a:string,b:string){if(a.length!==b.length)return false;let x=0;for(let i=0;i<a.length;i++)x|=a.charCodeAt(i)^b.charCodeAt(i);return x===0}

Deno.serve(async req=>{
 if(req.method==='OPTIONS')return new Response('ok',{headers:cors});
 try{
  const x=await req.json();const orderId=String(x.order_id||'').trim();if(!orderId)throw Error('Order ID is required');
  const d=db();const {data:o,error}=await d.from('orders').select('*').eq('public_order_id',orderId).single();if(error||!o)throw Error('Order not found');
  const key=secret('RAZORPAY_KEY_ID'),sec=secret('RAZORPAY_KEY_SECRET');if(!key||!sec)throw Error('Razorpay keys are not configured');
  const auth=btoa(`${key}:${sec}`);
  const rOrderId=String(x.razorpay_order_id||o.razorpay_order_id||'');
  const rPaymentId=String(x.razorpay_payment_id||'');
  const signature=String(x.razorpay_signature||'');
  if(rPaymentId&&signature){
    if(!rOrderId||rOrderId!==o.razorpay_order_id)throw Error('Payment order mismatch');
    const expected=await hmacHex(`${rOrderId}|${rPaymentId}`,sec);
    if(!safeEq(expected,signature))throw Error('Payment signature verification failed');
  }
  if(!rOrderId)throw Error('Razorpay order not linked');
  const rr=await fetch('https://api.razorpay.com/v1/orders/'+encodeURIComponent(rOrderId),{headers:{Authorization:`Basic ${auth}`}});
  const ro=await rr.json();if(!rr.ok)throw Error(ro.error?.description||'Unable to verify Razorpay order');
  const paidAmount=Number(ro.amount_paid||0), expectedAmount=Number(o.amount_inr)*100;
  const paid=String(ro.status||'').toLowerCase()==='paid'&&paidAmount>=expectedAmount;
  if(paid){
    const now=new Date();
    const paymentId=rPaymentId||o.razorpay_payment_id||null;
    await d.from('orders').update({razorpay_status:'paid',razorpay_payment_id:paymentId,paid_at:now.toISOString()}).eq('id',o.id);
    if(['ringtone','song','design'].includes(o.kind)){
      const {data:existing}=await d.from('download_entitlements').select('id').eq('order_id',o.id).maybeSingle();
      if(!existing)await d.from('download_entitlements').insert({order_id:o.id,item_id:o.item_id||null,asset_id:o.asset_id||null,expires_at:new Date(now.getTime()+30*864e5).toISOString()});
    }
  }
  return json({paid,order_id:orderId,kind:o.kind});
 }catch(e){return json({error:String(e.message||e)},500)}
});

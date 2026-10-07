import {cors,json,db,secret} from '../_shared.ts';
Deno.serve(async req=>{
  if(req.method==='OPTIONS')return new Response('ok',{headers:cors});
  try{
    const d=db();
    const {data}=await d.from('orders').select('*').eq('public_order_id',String((await req.json()).order_id||'')).single();
    if(!data)throw Error('Order not found');
    if(data.razorpay_status!=='paid'&&data.razorpay_link_id){
      const key=secret('RAZORPAY_KEY_ID'),sec=secret('RAZORPAY_KEY_SECRET');
      if(!key||!sec)throw Error('Razorpay keys are not configured');
      const auth=btoa(`${key}:${sec}`);
      const r=await fetch('https://api.razorpay.com/v1/payment_links/'+data.razorpay_link_id,{headers:{Authorization:`Basic ${auth}`}});
      const j=await r.json();
      if(j.status==='paid'){
        const now=new Date();
        await d.from('orders').update({razorpay_status:'paid',razorpay_payment_id:j.payments?.[0]?.payment_id||null,paid_at:now.toISOString()}).eq('id',data.id);
        data.razorpay_status='paid';
        if(data.kind==='ringtone'||data.kind==='song'){
          const {data:existing}=await d.from('download_entitlements').select('id').eq('order_id',data.id).maybeSingle();
          if(!existing)await d.from('download_entitlements').insert({order_id:data.id,item_id:data.item_id||null,asset_id:data.asset_id||null,expires_at:new Date(now.getTime()+30*864e5).toISOString()});
        }
      }
    }
    return json({order_id:data.public_order_id,paid:data.razorpay_status==='paid',kind:data.kind,message:data.razorpay_status==='paid'?'Payment confirmed':'Payment pending'});
  }catch(e){return json({error:String(e.message||e)},404)}
});

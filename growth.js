/* NavaBharat AI Phase 2. Affiliate links and admin growth dashboard.
   No provider key in browser. Free tools / payments are not changed. */
(function(){
'use strict';
const $=s=>document.querySelector(s);
const escapeHTML=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const safeURL=value=>{try{const u=new URL(value);return u.protocol==='https:'?u.href:''}catch{return ''}};
let offerData=[],lastAdminData=null;
const fmtMoney=n=>'₹'+(Number(n)||0).toLocaleString('en-IN',{maximumFractionDigits:2});
const day=()=>new Date().toISOString().slice(0,10);
function safeSessionToken(){
  try{
    const k='nava_growth_daily_event',old=JSON.parse(localStorage.getItem(k)||'null');
    if(old?.day===day()&&/^[a-f0-9-]{36}$/i.test(old.token))return old.token;
    const token=crypto.randomUUID();localStorage.setItem(k,JSON.stringify({day:day(),token}));return token;
  }catch{return crypto.randomUUID()}
}
async function api(body,admin=false,keepalive=false){
 const c=window.NAVA_CONFIG||{};
 if(!c.SUPABASE_URL||!c.SUPABASE_ANON_KEY)throw Error('Site connection not configured.');
 const headers={'Content-Type':'application/json','apikey':c.SUPABASE_ANON_KEY};
 if(admin){const token=sessionStorage.getItem('nava_admin_token');if(!token)throw Error('Unlock Admin first.');headers['x-admin-token']=token}
 const r=await fetch(c.SUPABASE_URL+'/functions/v1/growth-hub',{method:'POST',headers,body:JSON.stringify(body),keepalive});
 const x=await r.json().catch(()=>({}));if(!r.ok)throw Error(x.error||'Growth service unavailable.');return x;
}
function offerCards(offers){
 if(!offers.length)return '<div class="notice">Approved affiliate offers will appear here after you add and publish your first genuine tracking link in Admin. No offers are currently active.</div>';
 return `<div class="growth-offer-grid">${offers.map(o=>{
  const href=safeURL(o.affiliate_url);
  if(!href)return '';
  return `<article class="card growth-offer-card"><div class="growth-offer-tag">Partner recommendation · ${escapeHTML(o.category)}</div><h3>${escapeHTML(o.title)}</h3><p class="muted">${escapeHTML(o.description||'Learn more about this partner offer.')}</p><p class="growth-provider">${escapeHTML(o.provider)}</p><a class="btn secondary" data-growth-offer="${escapeHTML(o.id)}" href="${escapeHTML(href)}" target="_blank" rel="sponsored nofollow noopener noreferrer">View partner offer ↗</a></article>`;
 }).join('')}</div>`;
}
function attachClickTracking(parent){
 parent.querySelectorAll('a[data-growth-offer]').forEach(link=>{
  link.addEventListener('click',()=>{
   if(navigator.doNotTrack==='1'||localStorage.getItem('nava_growth_optout')==='yes')return;
   const id=link.dataset.growthOffer;
   api({action:'affiliate-click',offer_id:id,token:safeSessionToken()},false,true).catch(()=>{});
  });
 });
}
async function renderOffers(target){
 if(!target)return;
 target.innerHTML='<div class="notice">Loading partner resources…</div>';
 try{const r=await api({action:'offers'});offerData=r.offers||[];if(!target.isConnected)return;target.innerHTML=offerCards(offerData);attachClickTracking(target)}
 catch{target.innerHTML='<div class="notice">Partner listings are temporarily unavailable. Your main NavaBharat AI tools are unaffected.</div>'}
}
function page(){return `<section class="hero"><div class="hero-badge">Optional partner recommendations</div><h1>🔗 Resources & Affiliate Offers</h1><p>Free services remain available. We recommend only offers added after joining and reviewing the relevant affiliate programs.</p></section><div class="card growth-disclosure" style="margin-top:18px"><h3>Affiliate disclosure</h3><p class="muted">Some external partner links can earn NavaBharat AI a commission when you make an eligible purchase. Your purchase decision is voluntary, and qualifying commissions depend on the partner’s terms. We clearly separate these offers from jobs, official notices and AI answers.</p><p class="muted"><b>Amazon disclosure:</b> As an Amazon Associate I earn from qualifying purchases (if Amazon Associates links are published).</p></div><div id="growthOffers" style="margin-top:18px"></div><div class="card" style="margin-top:18px"><h3>Want free tools instead?</h3><div class="row"><button class="btn secondary" onclick="go('solve')">AI Solve</button><button class="btn secondary" onclick="go('jobs')">Jobs & Exams</button><button class="btn secondary" onclick="go('video')">Video Studio</button></div></div>`}
function adminPanel(){return `<section class="card growth-admin-panel" style="margin-bottom:18px"><h3>📊 Visitors, Revenue & Affiliate Control</h3><p class="muted">Only the protected server-side Admin token can read earnings or edit affiliate offers. Visitors are estimated anonymous browsers per day, not exact people. GA4 is the source for detailed site analytics.</p><div class="row"><button class="btn secondary" onclick="NavaGrowth.loadAdmin()">Load Growth Dashboard</button><a class="btn secondary" href="https://analytics.google.com/" target="_blank" rel="noopener noreferrer">Open GA4 ↗</a><a class="btn secondary" href="https://publishers.monetag.com/" target="_blank" rel="noopener noreferrer">Open Monetag ↗</a><button class="btn secondary" onclick="NavaGrowth.prune()">Prune analytics older than 30 days</button></div><div id="growthAdminOut" class="growth-admin-out"></div><div class="grid growth-admin-forms"><div class="card"><h3>🔗 Add / Edit Affiliate Offer</h3><input type="hidden" id="growthOfferId"><label>Offer title<input id="growthOfferTitle" class="field" maxlength="100" placeholder="Example: Approved course partner offer"></label><label>Network/provider<input id="growthOfferProvider" class="field" maxlength="65" placeholder="Example: Cuelinks / Amazon Associates"></label><label>Category<select id="growthOfferCategory" class="field"><option>Learning</option><option>Technology</option><option>Creator Tools</option><option>Books</option><option>Jobs & Exams</option><option>Other</option></select></label><label>Description<textarea id="growthOfferDescription" class="field" maxlength="450" placeholder="What is offered and why it is relevant"></textarea></label><label>Approved partner tracking URL (HTTPS)<input id="growthOfferURL" class="field" type="url" placeholder="https://partner-tracking-link"></label><label>Sort order<input id="growthOfferOrder" class="field" type="number" value="100" min="0" max="10000"></label><label class="check"><input id="growthOfferActive" type="checkbox"> Publish this approved affiliate offer</label><div class="row"><button class="btn" onclick="NavaGrowth.saveOffer()">Save offer</button><button class="btn secondary" onclick="NavaGrowth.clearOffer()">Clear form</button></div><div id="growthOfferStatus" role="status"></div></div><div class="card"><h3>💰 Record Revenue from External Platforms</h3><p class="muted">Enter figures only from your actual affiliate or Monetag dashboard. They are manual entries, not automatically verified by this app.</p><label>Revenue source<select id="growthIncomeType" class="field"><option value="affiliate">Affiliate program</option><option value="monetag">Monetag</option><option value="other">Other</option></select></label><label>Provider name<input id="growthIncomeProvider" class="field" maxlength="80" placeholder="Network or payment source"></label><label>Amount in INR<input id="growthIncomeAmount" class="field" type="number" min="0" step="0.01" placeholder="0.00"></label><label>Date<input id="growthIncomeDate" class="field" type="date"></label><label>Statement / payout reference<input id="growthIncomeNote" class="field" maxlength="280" placeholder="Optional record from provider dashboard"></label><label class="check"><input id="growthIncomeConfirmed" type="checkbox"> Confirmed using a real network statement / payout</label><button class="btn" onclick="NavaGrowth.saveEarning()">Record external income</button><div id="growthIncomeStatus" role="status"></div></div></div></section>`}
function metric(label,value,note){return `<div class="growth-stat"><span class="growth-stat-label">${escapeHTML(label)}</span><b>${escapeHTML(value)}</b><small>${escapeHTML(note)}</small></div>`}
function displayAdmin(data){
 const f=data.financial||{},t=data.traffic||{},clicks=data.clicks30_by_offer||{};
 const stat=`<div class="growth-stats">${metric('Today (est. browsers)',String(t.today_unique_browsers_estimate??0),'Not exact people · not GA4 users')}${metric('Last 7 days (browser-days)',String(t.last7_browser_days??0),'A returning browser counts again next day')}${metric('Last 30 days (browser-days)',String(t.last30_browser_days??0),'Anonymous on-site estimate')}${metric('Existing paid tools (gross)',fmtMoney(f.core_paid_gross_inr),'Razorpay-paid music/ringtones/support/orders')}${metric('Paid advertiser bookings (gross)',fmtMoney(f.ad_paid_gross_inr),'Before refunds, fees and taxes')}${metric('Confirmed affiliate income (manual)',fmtMoney(f.affiliate_confirmed_manual_inr),'From network statements you entered')}${metric('Confirmed Monetag income (manual)',fmtMoney(f.monetag_confirmed_manual_inr),'Only if manually recorded')}${metric('Affiliate clicks last 30d (est.)',String(t.affiliate_clicks_last30_estimate??0),'Not sales or commissions')}</div>`;
 const entries=(data.offers||[]).map(o=>`<div class="notice growth-offer-admin"><b>${escapeHTML(o.title)}</b> · ${escapeHTML(o.provider)} · ${o.active?'Published':'Draft'} · ${Number(clicks[o.id]||0)} estimated click(s) in last 30d<div class="row" style="margin-top:9px"><button class="btn small secondary" onclick="NavaGrowth.editOffer('${escapeHTML(o.id)}')">Edit</button><button class="btn small secondary" onclick="NavaGrowth.toggleOffer('${escapeHTML(o.id)}',${!o.active})">${o.active?'Unpublish':'Publish'}</button></div></div>`).join('')||'<div class="notice">No affiliate offers created.</div>';
 const earnings=(data.earnings||[]).slice(0,20).map(e=>`<div class="notice"><b>${escapeHTML(e.provider)}</b> · ${escapeHTML(e.income_type||'affiliate')} · ${fmtMoney(e.amount_inr)} · ${escapeHTML(e.earned_on||'')} · ${e.confirmed?'Confirmed manually':'Unconfirmed'}<div class="muted">${escapeHTML(e.reference_note||'')}</div>${!e.confirmed?`<button class="btn small secondary" onclick="NavaGrowth.confirmEarning('${escapeHTML(e.id)}')">Mark confirmed after checking statement</button>`:''}</div>`).join('')||'<div class="notice">No external income entered.</div>';
 return `<h4 style="margin-top:18px">Revenue and visitors</h4>${stat}<p class="muted">Gross figures exclude payment fees, taxes, refunds and chargebacks. Manual affiliate/Monetag income may overlap with other accounting if entered twice. Use GA4 for authoritative site-traffic reporting. ${data.click_report_capped?'Offer click breakdown capped at 5,000 recent rows.':''}</p><h4>Active and draft affiliate offers</h4>${entries}<h4 style="margin-top:18px">Recorded external earnings</h4>${earnings}`;
}
async function loadAdmin(){const target=$('#growthAdminOut');if(!target)return;target.innerHTML='<div class="notice">Loading secure admin summary…</div>';try{lastAdminData=await api({action:'admin-dashboard'},true);target.innerHTML=displayAdmin(lastAdminData)}catch(e){target.innerHTML='<div class="notice">Dashboard unavailable: '+escapeHTML(e.message)+'</div>'}}
function readForm(){return {action:'admin-save-offer',id:$('#growthOfferId')?.value||undefined,title:$('#growthOfferTitle')?.value,provider:$('#growthOfferProvider')?.value,category:$('#growthOfferCategory')?.value,description:$('#growthOfferDescription')?.value,url:$('#growthOfferURL')?.value,sort_order:$('#growthOfferOrder')?.value,active:$('#growthOfferActive')?.checked}}
async function saveOffer(){const st=$('#growthOfferStatus');if(st)st.textContent='Saving…';try{await api(readForm(),true);if(st)st.textContent='Offer saved. Refreshing dashboard…';clearOffer();await loadAdmin()}catch(e){if(st)st.textContent='Could not save: '+e.message}}
function clearOffer(){for(const f of ['growthOfferId','growthOfferTitle','growthOfferProvider','growthOfferURL','growthOfferDescription']){const el=$('#'+f);if(el)el.value=''}if($('#growthOfferCategory'))$('#growthOfferCategory').value='Learning';if($('#growthOfferOrder'))$('#growthOfferOrder').value='100';if($('#growthOfferActive'))$('#growthOfferActive').checked=false}
function editOffer(id){const o=(lastAdminData?.offers||[]).find(x=>x.id===id);if(!o)return;const m={growthOfferId:o.id,growthOfferTitle:o.title,growthOfferProvider:o.provider,growthOfferCategory:o.category,growthOfferURL:o.affiliate_url,growthOfferDescription:o.description,growthOfferOrder:o.sort_order};Object.entries(m).forEach(([k,v])=>{const el=$('#'+k);if(el)el.value=String(v??'')});if($('#growthOfferActive'))$('#growthOfferActive').checked=!!o.active;$('#growthOfferTitle')?.focus()}
async function toggleOffer(id,active){try{await api({action:'admin-toggle-offer',id,active},true);await loadAdmin()}catch(e){alert(e.message)}}
async function saveEarning(){const st=$('#growthIncomeStatus');if(st)st.textContent='Saving…';try{await api({action:'admin-add-earning',income_type:$('#growthIncomeType')?.value,provider:$('#growthIncomeProvider')?.value,amount_inr:$('#growthIncomeAmount')?.value,earned_on:$('#growthIncomeDate')?.value,note:$('#growthIncomeNote')?.value,confirmed:$('#growthIncomeConfirmed')?.checked},true);if(st)st.textContent='Revenue record saved.';await loadAdmin()}catch(e){if(st)st.textContent='Could not save: '+e.message}}
async function confirmEarning(id){if(!confirm('Confirm only if you checked the actual payment or network statement.'))return;try{await api({action:'admin-confirm-earning',id,confirmed:true},true);await loadAdmin()}catch(e){alert(e.message)}}
async function prune(){if(!confirm('Remove only anonymous analytics data older than 30 days? Paid orders and media are not affected.'))return;try{await api({action:'admin-prune-analytics'},true);await loadAdmin()}catch(e){alert(e.message)}}
async function visit(){
 try{
  if(navigator.doNotTrack==='1'||localStorage.getItem('nava_growth_optout')==='yes')return;
  const k='nava_growth_sent';if(localStorage.getItem(k)===day())return;
  await api({action:'visit',token:safeSessionToken(),page:new URLSearchParams(location.search).get('page')||'home'});
  localStorage.setItem(k,day());
 }catch{} // Visitor measurement never interrupts a user feature.
}
async function contextualOffers(page){
 const content=$('#app .content');if(!content)return;
 const holder=document.createElement('section');holder.className='card growth-contextual';holder.style.marginTop='18px';
 holder.innerHTML='<div class="growth-offer-tag">Optional affiliate recommendations</div><h3>Useful partner resources</h3><div class="growth-context-out"></div><p class="muted">Some links may earn a commission. Recommendations are not official job notices.</p>';
 content.appendChild(holder);
 try{
  const r=await api({action:'offers'});if(!holder.isConnected)return;
  const categories={jobs:['Jobs & Exams','Learning','Books'],creator:['Creator Tools','Technology'],video:['Creator Tools','Technology'],search:['Learning','Technology'],home:[]};
  const matches=(r.offers||[]).filter(o=>!categories[page]?.length||categories[page].includes(o.category)).slice(0,2);
  if(!matches.length){holder.remove();return}
  const target=holder.querySelector('.growth-context-out');target.innerHTML=offerCards(matches);attachClickTracking(target);
 }catch{holder.remove()}
}
function afterRender(p){if(p==='resources')renderOffers($('#growthOffers'));if(['home','search','jobs','creator','video'].includes(p))contextualOffers(p);if(p==='admin'){const d=$('#growthIncomeDate');if(d&&!d.value)d.value=day()}}
function optOut(){try{localStorage.setItem('nava_growth_optout','yes');alert('Anonymous visitor analytics are disabled in this browser.')}catch{alert('Unable to update privacy setting.')}}
function standaloneResources(){const target=$('#affiliateResourceOffers');if(target)renderOffers(target)}
window.NavaGrowth={page,adminPanel,afterRender,visit,loadAdmin,saveOffer,clearOffer,editOffer,toggleOffer,saveEarning,confirmEarning,prune,optOut,standaloneResources};
})();

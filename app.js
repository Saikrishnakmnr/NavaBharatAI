const C=window.NAVA_CONFIG||{};const sup=window.supabase;let sb=null,current='home',ringtones=[],pending={};const $=s=>document.querySelector(s),esc=s=>String(s??'').replace(/[&<>'"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[m]));
if(C.SUPABASE_URL&&C.SUPABASE_ANON_KEY&&sup)sb=sup.createClient(C.SUPABASE_URL,C.SUPABASE_ANON_KEY);function toast(m){const x=$('#toast');x.textContent=m;x.classList.add('show');setTimeout(()=>x.classList.remove('show'),3200)}async function api(fn,body={}){if(!C.SUPABASE_URL||!C.SUPABASE_ANON_KEY)throw Error('App services are not configured yet.');const r=await fetch(C.SUPABASE_URL+'/functions/v1/'+fn,{method:'POST',headers:{'Content-Type':'application/json','apikey':C.SUPABASE_ANON_KEY,'Authorization':'Bearer '+C.SUPABASE_ANON_KEY},body:JSON.stringify(body)});let j={};try{j=await r.json()}catch{}if(!r.ok)throw Error(j.error||'Request failed');return j}
const pages=[['home','🏠 Home'],['solve','🧠 AI Solve'],['music-generator','🎼 Music Generator'],['ringtone-generator','🎵 Ringtone Generator'],['ringtone-library','📚 Ringtone Library'],['search','🔎 NavaBharat Search'],['science','🔬 Science'],['translator','🌐 Translator'],['live','📡 Live Tools'],['current-affairs','🗞️ Current Affairs'],['jobs','💼 Jobs & Exams'],['music-library','🎧 RacharlaGPT Music'],['admin','🔐 Admin'],['video','🎬 Video Studio'],['advertise','📢 Advertise & Slideshow'],['creator','✨ Creator Studio'],['premium','💎 Premium & Support'],['about','ℹ️ About'],['privacy','🔒 Privacy'],['contact','✉️ Contact']];$('#nav').innerHTML=pages.map(x=>`<button data-page="${x[0]}">${x[1]}</button>`).join('');document.querySelectorAll('#nav button').forEach(b=>b.onclick=()=>go(b.dataset.page));$('#menu').onclick=()=>$('#sidebar').classList.add('open');$('#closeNav').onclick=()=>$('#sidebar').classList.remove('open');$('#theme').onclick=()=>{document.body.classList.toggle('light');localStorage.setItem('nava-theme',document.body.classList.contains('light')?'light':'dark')};if(localStorage.getItem('nava-theme')==='light')document.body.classList.add('light');
function go(p){p=({music:'music-generator',song:'music-generator','create-song':'music-generator'}[p]||p);if(p!=='admin'&&window.__adminPoll){clearInterval(window.__adminPoll);window.__adminPoll=null}current=p;history.replaceState({},'',p==='home'?'/':'/?page='+p);document.querySelectorAll('#nav button').forEach(b=>b.classList.toggle('active',b.dataset.page===p));$('#crumb').textContent=pages.find(x=>x[0]===p)?.[1]||'NavaBharat AI';$('#sidebar').classList.remove('open');render();window.scrollTo({top:0,behavior:'smooth'})}
function share(text,url=location.href){const t=encodeURIComponent(text),u=encodeURIComponent(url);return `<div class="share-grid"><a target="_blank" href="https://wa.me/?text=${t}%20${u}">WhatsApp</a><a target="_blank" href="https://t.me/share/url?url=${u}&text=${t}">Telegram</a><a target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=${u}">Facebook</a><a target="_blank" href="https://twitter.com/intent/tweet?text=${t}&url=${u}">X</a><a target="_blank" href="https://www.instagram.com/">Instagram</a></div>`}
function home(){return `<section class="hero"><h1>India's glossy AI workspace.</h1><p>NavaBharat AI is a product of RacharlaGPT. Create original songs and ringtones, explore a rights-aware ringtone catalog, solve questions, translate, search and publish creator content — from one mobile/desktop-friendly app.</p><div class="row"><button class="btn" onclick="go('music-generator')">🎼 Create a Song</button><button class="btn secondary" onclick="go('ringtone-generator')">🎵 Make a Ringtone</button></div></section><div class="grid">${[['solve','🧠 AI Solve','Answers, explanations and study help.'],['music-generator','🎼 Music Generator','Lyrics + idea → original AI song. Preview free; download ₹19.'],['ringtone-generator','🎵 Ringtone Generator','Customer idea/lyrics → original ringtone. Preview free; ₹10 offer.'],['ringtone-library','📚 Ringtone Library','Search and preview a rights-cleared catalog; ₹10 offer download.'],['search','🔎 NavaBharat Search','Google search plus shareable result cards.'],['creator','✨ Creator Studio','YouTube, Instagram, LinkedIn and X content.'],['advertise','📢 Business Slideshow & Video Ads','Create free slideshows, book approved sponsored placements.'],['premium','💎 Premium & Support','Razorpay support, personalised orders and recovery.']].map(x=>`<div class="card"><h3>${x[1]}</h3><p class="muted">${x[2]}</p><button class="btn secondary" onclick="go('${x[0]}')">Open</button></div>`).join('')}</div>`}
function aiPage(title,placeholder,button,promptType){return `<section class="hero"><h1>${title}</h1><p>AI-powered answers, explanations and creative assistance in your selected language.</p></section><div class="card" style="margin-top:18px"><textarea id="aiInput" class="field" placeholder="${placeholder}"></textarea><div class="row" style="margin-top:12px"><select id="aiLang" class="field" style="max-width:220px"><option>English</option><option>Telugu</option><option>Hindi</option><option>Tamil</option><option>Kannada</option><option>Malayalam</option></select><button class="btn" onclick="runAI('${promptType}')">${button}</button></div><div id="aiOut" style="margin-top:18px"></div></div>`}
function navaRich(text){
  const src=String(text||'').replace(/\r\n?/g,'\n').slice(0,60000);
  const inline=(v)=>{
    let t=esc(v);
    t=t.replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>');
    t=t.replace(/`([^`]+)`/g,'<code>$1</code>');
    return t;
  };
  let blocks=[],list=[],quote=[];
  const close=()=>{if(list.length){blocks.push('<ul>'+list.map(v=>'<li>'+inline(v)+'</li>').join('')+'</ul>');list=[]}if(quote.length){blocks.push('<blockquote>'+quote.map(inline).join('<br>')+'</blockquote>');quote=[]}};
  for(const raw of src.split('\n')){
    let line=raw.trim();
    if(!line){close();continue}
    let m=line.match(/^(#{1,5})\s+(.+)$/);
    if(m){close();let level=Math.min(5,m[1].length+1);blocks.push('<h'+level+'>'+inline(m[2])+'</h'+level+'>');continue}
    if(/^---+$/.test(line)){close();blocks.push('<hr>');continue}
    m=line.match(/^(?:[-*•]\s+|\d+[.)]\s+)(.+)$/);
    if(m){if(quote.length)close();list.push(m[1]);continue}
    if(line.startsWith('> ')){if(list.length)close();quote.push(line.slice(2));continue}
    close();blocks.push('<p>'+inline(line)+'</p>');
  }
  close();return '<div class="nava-rich">'+blocks.join('')+'</div>';
}
function navaNewsCards(items,provider='Live feed'){
  return (items||[]).filter(x=>{try{const u=new URL(x.link);return ['https:','http:'].includes(u.protocol)}catch{return false}}).map(x=>`<div class="card nava-news-item"><h4><a href="${esc(x.link)}" target="_blank" rel="noopener noreferrer">${esc(x.title||'Read headline')}</a></h4><small>${esc(x.source||provider)} · ${esc(x.pubDate||'Date unavailable')}</small></div>`).join('');
}
async function runAI(type){const input=$('#aiInput').value.trim(),lang=$('#aiLang').value;if(!input)return toast('Enter your request first.');$('#aiOut').innerHTML='<div class="notice">Generating…</div>';try{const j=await api('ai-text',{type,input,language:lang});$('#aiOut').innerHTML=`<div class="nava-answer">${navaRich(j.text||'No answer')}</div>${share('NavaBharat AI: '+input)}`;window.gtag?.('event','ai_tool',{tool:type})}catch(e){$('#aiOut').innerHTML=`<div class="notice">${esc(e.message)}</div>`}}
function solve(){return aiPage('🧠 AI Solve','Ask a maths, science, coding, reasoning or general question…','Solve','solve')}function science(){return aiPage('🔬 Science Lab','Explain a science topic, experiment or concept…','Explain','science')}function translator(){return aiPage('🌐 Translator','Paste text and choose the output language…','Translate','translate')}function live(){return `<section class="hero"><h1>📰 Live News RSS</h1><p>News from linked publishers and official sources, not AI-invented headlines. Choose your language and search any topic.</p></section><div class="card nava-live-wide"><div class="grid"><select id="liveLang" class="field"><option>English</option><option>Telugu</option><option>Hindi</option><option>Tamil</option><option>Kannada</option><option>Malayalam</option></select><input id="liveQ" class="field" placeholder="Optional news topic"></div><button class="btn" style="margin-top:12px" onclick="loadLiveRSS()">🔄 Fetch Latest RSS News</button><div id="liveRSS" style="margin-top:18px"></div></div>`}function navaExternalNewsLinks(q){const query=String(q||'India news').trim()||'India news';const g='https://news.google.com/search?q='+encodeURIComponent(query);const w='https://www.google.com/search?tbm=nws&q='+encodeURIComponent(query);return `<div class="notice">Matching live headlines are not available from the connected feeds right now. These external search links may have more results; verify their dates and sources.</div><div class="row"><a class="btn secondary" target="_blank" rel="noopener noreferrer" href="${esc(g)}">Google News ↗</a><a class="btn secondary" target="_blank" rel="noopener noreferrer" href="${esc(w)}">Search latest reports ↗</a></div>`}
function navaOfficialJobLinks(){return `<div class="card"><h3>Official recruitment portals</h3><p class="muted">Check current notices and apply only through the responsible official portal.</p><div class="row"><a target="_blank" rel="noopener noreferrer" href="https://ssc.gov.in/">SSC ↗</a><a target="_blank" rel="noopener noreferrer" href="https://upsc.gov.in/">UPSC ↗</a><a target="_blank" rel="noopener noreferrer" href="https://www.rrbapply.gov.in/">Railways ↗</a><a target="_blank" rel="noopener noreferrer" href="https://www.ibps.in/">IBPS ↗</a><a target="_blank" rel="noopener noreferrer" href="https://www.ncs.gov.in/">NCS ↗</a></div></div>`}
async function loadLiveRSS(){
 const q=$('#liveQ').value.trim(),lang=$('#liveLang').value;
 $('#liveRSS').innerHTML='<div class="notice" role="status">Fetching source-linked news…</div>';
 try{
  const j=await api('live-rss',{kind:'news',query:q||'India news',language:lang,limit:12});
  const cards=navaNewsCards(j.items,j.provider);
  $('#liveRSS').innerHTML=cards||navaExternalNewsLinks(q||'India news');
 }catch(e){$('#liveRSS').innerHTML=navaExternalNewsLinks(q||'India news')}
}
function search(){return `<section class="hero"><h1>🔎 NavaBharat Search</h1><p>Google web search, AI topic explanations when available, linked news sources and share-ready visuals.</p></section><div class="card"><div class="row"><input id="q" class="field" placeholder="Search topic or try: milk /mindmap" style="flex:1"><button class="btn" onclick="doSearch()">Search Google</button><button class="btn secondary" onclick="groundSearch()">🤖 AI Summary</button></div><div id="searchShare" style="margin-top:18px"></div><div id="searchAI" style="margin-top:18px"></div></div>`}function doSearch(){const q=$('#q').value.trim().replace(/\s*\/(?:mindmap|handwrittennotes|visualizations|infographics|stickynotes)\s*$/i,'');if(!q)return toast('Type something to search first.');window.open('https://www.google.com/search?q='+encodeURIComponent(q),'_blank');$('#searchShare').innerHTML='<h3>Share search</h3>'+share('NavaBharat AI search: '+q)}async function groundSearch(){
 const input=$('#q').value.trim();
 const command=input.match(/\s*\/(mindmap|handwrittennotes|visualizations|infographics|stickynotes)\s*$/i);
 const modes={mindmap:'mindmap',handwrittennotes:'notes',visualizations:'visualization',infographics:'infographic',stickynotes:'sticky'};
 const requestedKind=command?modes[command[1].toLowerCase()]:null;
 const q=command?input.slice(0,command.index).trim():input;
 if(!q)return toast('Type a search topic first.');
 $('#searchAI').innerHTML='<div class="notice" role="status">Preparing summary and checking independent news sources…</div>';
 const [ai,news]=await Promise.allSettled([
  api('ai-text',{type:'search',input:q,language:'English'}),
  api('live-rss',{kind:'search',query:q,language:'English',limit:8})
 ]);
 const answer=ai.status==='fulfilled'?String(ai.value.text||''):'';
 const items=news.status==='fulfilled'?(news.value.items||[]):[];
 window.__searchState=answer?{q,ans:answer,items}:null;
 const web='https://www.google.com/search?q='+encodeURIComponent(q);
 const fallback=`<p class="muted">The AI summary is temporarily unavailable. Read live linked articles (if found) or search the web directly.</p><a class="btn secondary" target="_blank" rel="noopener noreferrer" href="${esc(web)}">🌐 Google Web Search ↗</a>`;
 $('#searchAI').innerHTML=`<div class="card"><h3>${answer?'⚡ AI Topic Summary':'🔎 Search resources'}</h3>${answer?navaRich(answer):fallback}${share('NavaBharat AI search: '+q)}</div>${answer?'<div class="row"><button class="btn secondary" onclick="makeSearchImage(\'mindmap\')">🗺️ Mind Map</button><button class="btn secondary" onclick="makeSearchImage(\'notes\')">✍️ Handwritten Notes</button><button class="btn secondary" onclick="makeSearchImage(\'infographic\')">📊 Infographic</button><button class="btn secondary" onclick="makeSearchImage(\'visualization\')">🔄 Visualization</button><button class="btn secondary" onclick="makeSearchImage(\'sticky\')">🗒️ Sticky Notes</button></div>':''}<div id="searchVisual" class="card" style="margin-top:16px"><p class="muted">${answer?'Choose a visual above.':'Visuals require an AI answer.'}</p></div><div class="card" style="margin-top:16px"><h3>📰 Topic-related news links</h3>${navaNewsCards(items,news.status==='fulfilled'?news.value.provider:'Linked sources')||navaExternalNewsLinks(q)}</div>`;
 if(requestedKind&&answer)makeSearchImage(requestedKind);
}
// Browser-only visual cards: structured graphics, not image-model calls.
// Only text already present in the successful AI response is used for content.
function navaVisualIdeas(answer){
  const lines=String(answer||'').replace(/\r/g,'').split('\n').map(v=>v.trim());
  let pieces=[],section='';
  for(const line of lines){
    if(!line || /^[-_=*]{3,}$/.test(line) || /^\|?\s*[-:| ]+\|?$/.test(line))continue;
    const heading=line.match(/^#{1,6}\s+(.+)$/);
    if(heading){section=heading[1].replace(/\*\*/g,'').trim();continue;}
    let t=line.replace(/^(?:[-*•]\s+|\d+[.)]\s+)/,'')
      .replace(/\*\*/g,'').replace(/`/g,'').replace(/^>\s*/,'')
      .replace(/!\[[^\]]*\]\([^)]*\)/g,'').replace(/\[([^\]]+)\]\([^)]*\)/g,'$1')
      .replace(/\|/g,' · ').replace(/\s+/g,' ').trim();
    if(!t || t.length<9 || /^https?:\/\//i.test(t))continue;
    if(section&&section.length<34&&!t.toLowerCase().startsWith(section.toLowerCase())) t=section+': '+t;
    if(t.length>175){
      const cut=t.match(/^.{20,150}?[.!?।](?=\s|$)/);
      if(cut)t=cut[0];
    }
    if(!pieces.some(x=>x.toLocaleLowerCase()===t.toLocaleLowerCase()))pieces.push(t);
    if(pieces.length>=12)break;
  }
  if(pieces.length<4){
    const sentences=String(answer||'').replace(/[#*`]/g,'').split(/(?<=[.!?।])\s+/);
    for(let t of sentences){t=t.replace(/\s+/g,' ').trim();if(t.length>14&&!pieces.includes(t))pieces.push(t);if(pieces.length>=10)break}
  }
  return pieces.filter(x=>x.length>6).slice(0,8);
}
function navaCanvasText(ctx, value, x, y, maxWidth, maxLines=3, lineHeight=34){
  const text=String(value||'').replace(/\s+/g,' ').trim();
  let tokens=text.split(' ');
  if(tokens.length===1 && ctx.measureText(text).width>maxWidth){tokens=Array.from(text)}
  const space=tokens.length>1&&text.includes(' ')?' ':'';
  const lines=[];let line='';
  for(const word of tokens){
    const attempt=line?(line+space+word):word;
    if(ctx.measureText(attempt).width>maxWidth&&line){lines.push(line);line=word}else line=attempt;
  }
  if(line)lines.push(line);
  const output=lines.slice(0,maxLines);
  if(lines.length>maxLines&&output.length){
    let last=output[output.length-1];
    while(last.length>1&&ctx.measureText(last+'…').width>maxWidth)last=Array.from(last).slice(0,-1).join('');
    output[output.length-1]=last+'…';
  }
  output.forEach((line,i)=>ctx.fillText(line,x,y+i*lineHeight));
  return output.length*lineHeight;
}
function navaRoundBox(ctx,x,y,w,h,r,fill,stroke){
  ctx.beginPath();ctx.roundRect(x,y,w,h,r);
  if(fill){ctx.fillStyle=fill;ctx.fill()}
  if(stroke){ctx.lineWidth=2;ctx.strokeStyle=stroke;ctx.stroke()}
}
function navaLine(ctx,x1,y1,x2,y2,color,width=5){
  ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.strokeStyle=color;ctx.lineWidth=width;ctx.lineCap='round';ctx.stroke();
}
function navaGraphic(kind,topic,answer){
  const tall=['notes','sticky','infographic'].includes(kind);
  const c=document.createElement('canvas');c.width=1400;c.height=tall?1600:1100;
  const x=c.getContext('2d');if(!x)throw Error('Canvas is unavailable.');
  const W=c.width,H=c.height;
  const ideas=navaVisualIdeas(answer);
  if(!ideas.length)throw Error('There are no summary points to visualize.');
  const palettes=['#55D6C2','#FFD166','#FF769C','#8DA9FF','#BFA3FF','#F4AB64','#92DB70','#72D5F4'];
  const bg=x.createLinearGradient(0,0,W,H);bg.addColorStop(0,'#0b1532');bg.addColorStop(.5,'#182557');bg.addColorStop(1,'#29205b');
  const isNotes=kind==='notes';
  x.fillStyle=isNotes?'#f9f4e6':bg;x.fillRect(0,0,W,H);
  // Decorative halftone field.
  if(!isNotes){
    x.fillStyle='rgba(255,255,255,.055)';
    for(let cy=30;cy<H;cy+=38)for(let cx=30;cx<W;cx+=38){x.beginPath();x.arc(cx,cy,2,0,Math.PI*2);x.fill()}
  }
  const dark='#102041',white='#f8f9ff';
  const heading={mindmap:'IDEA MIND MAP',notes:'HANDWRITTEN NOTES',sticky:'STICKY NOTE BOARD',infographic:'VISUAL INFOGRAPHIC',visualization:'CONCEPT FLOW'}[kind]||'NavaBharat Visual';
  if(isNotes){
    for(let yy=230;yy<H-90;yy+=65)navaLine(x,115,yy,W-80,yy,'#bfd7eb',2);
    navaLine(x,158,100,158,H-70,'#f0a9af',3);
    for(let y=160;y<H-50;y+=170){x.beginPath();x.arc(63,y,12,0,Math.PI*2);x.fillStyle='#c8cfcc';x.fill()}
  }
  x.textAlign='left';x.fillStyle=isNotes?'#19607c':'#7ddcf0';x.font='700 29px system-ui, sans-serif';x.fillText('NavaBharat AI  /  RacharlaGPT',86,90);
  x.fillStyle=isNotes?dark:white;x.font='900 60px system-ui, sans-serif';x.fillText(heading,86,170);
  x.font='800 46px system-ui, sans-serif';navaCanvasText(x,topic,90,244,W-180,2,54);
  if(kind==='mindmap'){
    // Genuine connected concept network with a central topic and satellite nodes.
    const cx=700,cy=610,radX=470,radY=235;const nodes=ideas.slice(0,6);
    nodes.forEach((text,i)=>{const a=-Math.PI/2+(2*Math.PI*i/nodes.length);const nx=cx+Math.cos(a)*radX,ny=cy+Math.sin(a)*radY;
      x.beginPath();x.moveTo(cx,cy);x.bezierCurveTo(cx+(nx-cx)*.45,cy, nx-(nx-cx)*.2,ny,nx,ny);x.strokeStyle=palettes[i];x.lineWidth=7;x.stroke();
    });
    nodes.forEach((text,i)=>{const a=-Math.PI/2+(2*Math.PI*i/nodes.length);const nx=cx+Math.cos(a)*radX,ny=cy+Math.sin(a)*radY;
      navaRoundBox(x,nx-184,ny-88,368,176,25,'#f8f9ff',palettes[i]);
      x.fillStyle=dark;x.font='800 24px system-ui, sans-serif';navaCanvasText(x,text,nx-160,ny-30,323,4,33);
    });
    const middle=x.createLinearGradient(cx-190,cy-120,cx+200,cy+150);middle.addColorStop(0,'#FFBA5B');middle.addColorStop(1,'#FF67B4');
    navaRoundBox(x,cx-217,cy-110,434,220,32,middle);
    x.fillStyle=dark;x.font='900 33px system-ui, sans-serif';navaCanvasText(x,topic,cx-188,cy-16,376,3,43);
  }else if(kind==='notes'){
    x.fillStyle='#0e4160';x.font='italic 700 33px "Comic Sans MS", "Segoe Print", cursive';
    ideas.slice(0,8).forEach((text,i)=>{
      const y=345+i*150;if(y>H-140)return;
      x.fillStyle=['#f4be69','#b9e5e3','#ffcae5','#cbcef9'][i%4];
      navaRoundBox(x,206,y-58,1080,116,13,x.fillStyle);
      x.fillStyle='#173451';x.font='italic 700 27px "Comic Sans MS", "Segoe Print", system-ui';
      x.fillText(String(i+1).padStart(2,'0')+'.',233,y-7);
      navaCanvasText(x,text,312,y-18,930,3,33);
    });
  }else if(kind==='sticky'){
    const count=Math.min(ideas.length,6);
    const cols=2,margin=85,cardW=570,cardH=360;
    ideas.slice(0,count).forEach((text,i)=>{
      const xx=margin+(i%cols)*650,yy=325+Math.floor(i/cols)*390;
      x.save();x.translate(xx+cardW/2,yy+cardH/2);x.rotate((i%2?1:-1)*.025);
      x.shadowColor='rgba(0,0,0,.35)';x.shadowBlur=22;x.shadowOffsetY=17;
      navaRoundBox(x,-cardW/2,-cardH/2,cardW,cardH,13,['#ffe18b','#fbb0bd','#c4f6e5','#c9d6ff','#f7c1f8','#ffc49a'][i]);
      x.shadowColor='transparent';x.fillStyle='rgba(15,30,55,.25)';navaRoundBox(x,-64,-cardH/2-13,128,35,9,'rgba(255,255,255,.52)');
      x.fillStyle='#1f2941';x.font='900 34px system-ui';x.fillText('IDEA '+(i+1),-cardW/2+38,-cardH/2+77);
      x.font='700 30px system-ui';navaCanvasText(x,text,-cardW/2+38,-cardH/2+134,cardW-76,5,41);
      x.restore();
    });
  }else if(kind==='infographic'){
    navaRoundBox(x,82,307,1236,184,30,'#f9f9ff');x.fillStyle=dark;
    x.font='900 36px system-ui';x.fillText('TOPIC AT A GLANCE',130,370);
    x.font='700 31px system-ui';navaCanvasText(x,ideas[0],130,423,1120,2,41);
    ideas.slice(1,7).forEach((text,i)=>{
      const xx=82+(i%2)*635,yy=545+Math.floor(i/2)*296;
      const color=palettes[i%palettes.length];navaRoundBox(x,xx,yy,600,261,27,'#fafaff');
      navaRoundBox(x,xx,yy,20,261,9,color);x.fillStyle=dark;x.font='900 52px system-ui';x.fillText(String(i+1).padStart(2,'0'),xx+40,yy+82);
      x.fillStyle='#2c3756';x.font='700 27px system-ui';navaCanvasText(x,text,xx+40,yy+132,514,4,38);
    });
  }else{
    // Deliberately a concept flow, not a fake quantitative chart.
    ideas.slice(0,5).forEach((text,i)=>{
      const xx=120+(i%2)*650,yy=305+i*137,ww=540,hh=120;
      navaRoundBox(x,xx,yy,ww,hh,24,'#f9faff',palettes[i]);x.fillStyle=dark;
      x.font='900 30px system-ui';x.fillText(String(i+1).padStart(2,'0'),xx+24,yy+52);
      x.font='700 24px system-ui';navaCanvasText(x,text,xx+88,yy+41,420,3,29);
      if(i<4){const nx=120+((i+1)%2)*650,ny=305+(i+1)*137;
        navaLine(x,xx+ww/2,yy+hh,nx+ww/2,ny,palettes[i],5);
      }
    });
  }
  x.fillStyle=isNotes?'#34506c':'#ced9f0';x.font='25px system-ui, sans-serif';
  x.fillText('Created from AI summary · Review details before sharing',90,H-90);
  x.fillText('navabharatai.racharlagpt.in',90,H-50);
  return c;
}
function makeSearchImage(kind){
  const st=window.__searchState;if(!st)return;
  try{
    const c=navaGraphic(kind,st.q,st.ans);
    const data=c.toDataURL('image/png');
    const labels={mindmap:'Mind map',notes:'Handwritten notes',infographic:'Infographic',sticky:'Sticky notes',visualization:'Concept flow'};
    const out=$('#searchVisual');
    if(!out)return;
    out.innerHTML=`<h3>✨ ${esc(labels[kind]||'Visual')} · ${esc(st.q)}</h3><p class="muted">A visual design based on your AI summary, created locally without an extra image-generation API call.</p><img alt="${esc(labels[kind]||'Summary')} for ${esc(st.q)}" style="display:block;width:100%;height:auto;max-height:780px;object-fit:contain;border-radius:16px;margin:14px auto" src="${data}"><div class="row"><a class="btn" download="navabharat-${esc(kind)}.png" href="${data}">⬇ Download high-resolution PNG</a><button class="btn secondary" onclick="var i=document.querySelector('#searchVisual img');i.style.maxHeight=i.style.maxHeight==='none'?'780px':'none'">⛶ Expand / Collapse</button></div>`;
  }catch(err){const out=$('#searchVisual');if(out)out.innerHTML='<div class="notice">Could not create the visual: '+esc(err.message)+'</div>'}
}

function musicGenerator(){return `<section class="hero"><h1>🎼 RacharlaGPT Music Generator</h1><p>Original songs with vocals and instruments. Multiple protected AI providers are used automatically for reliable generation.</p></section><div class="card" style="margin-top:18px"><div class="grid"><div><label>Song idea / lyrics</label><textarea id="songLyrics" class="field" placeholder="Write lyrics or describe the song. Example: Telugu motivational song about never giving up."></textarea></div><div><label>Style</label><select id="songStyle" class="field"><option>Tollywood Mass Folk / High Beat</option><option>Bollywood Romantic / Melodic</option><option>Lo-Fi Chill & Acoustic</option><option>EDM / Cyberpunk Synthwave</option><option>Cinematic Orchestral Epic</option><option>Hip Hop / Indian Rap</option><option>Devotional / Bhakti Fusion</option><option>Classical Fusion & Sitar</option></select><label>Language</label><select id="songLang" class="field"><option>Telugu</option><option>Hindi</option><option>English</option><option>Tamil</option><option>Kannada</option><option>Malayalam</option></select><label>Duration</label><select id="songDur" class="field"><option value="15">15 sec</option><option value="30">30 sec</option><option value="45">45 sec</option><option value="60" selected>60 sec</option></select><label>Vocals</label><select id="songVocal" class="field"><option>Solo Male Vocalist</option><option>Solo Female Vocalist</option><option>Male & Female Chorus Duet</option><option>Instrumental</option></select></div></div><div class="row" style="margin-top:14px"><button class="btn secondary" onclick="writeLyrics()">✍️ Generate Original Lyrics</button><button class="btn" onclick="generateMedia('song')">🎼 Generate Song</button></div><div id="songOut" style="margin-top:18px"></div></div>`}
async function writeLyrics(){const field=$('#songLyrics'),v=field?.value.trim();if(!v)return toast('Enter a topic/idea first.');const card=field.closest('.card'),btn=[...card.querySelectorAll('button')].find(b=>b.getAttribute('onclick')==='writeLyrics()'),out=$('#songOut');if(btn?.disabled)return;const oldLabel=btn?.textContent||'';if(btn){btn.disabled=true;btn.textContent='⏳ Generating lyrics…'}out.innerHTML='<div class="notice" role="status" aria-live="polite">✍️ Generating original lyrics. Please wait; do not click again.</div>';try{const j=await api('ai-text',{type:'lyrics',input:v,language:$('#songLang').value});field.value=j.text||'';out.innerHTML='<div class="notice" role="status">✅ Original lyrics ready. Review or edit them before generating the song.</div>';toast('Original lyrics generated.')}catch(e){out.innerHTML='<div class="notice" role="alert">'+esc(e.message)+'</div>'}finally{if(btn){btn.disabled=false;btn.textContent=oldLabel}}}
async function generateMedia(kind){const lyrics=kind==='song'?$('#songLyrics').value.trim():$('#ringLyrics').value.trim(),lang=kind==='song'?$('#songLang').value:$('#ringLang').value,style=kind==='song'?$('#songStyle').value:$('#ringStyle').value,duration=kind==='song'?Number($('#songDur').value):Number($('#ringDur').value);if(!lyrics)return toast('Enter lyrics or an idea.');const out=$(kind==='song'?'#songOut':'#ringOut');out.innerHTML='<div class="notice">AI providers are generating your audio… preview is free.</div>';try{const j=await api('generate-media',{kind,lyrics,language:lang,style,duration,vocal_type:kind==='song'?$('#songVocal').value:'Instrumental'});out.innerHTML=`<div class="card"><span class="pill">${esc(j.provider||'AI')}</span><h3>Preview</h3><audio class="audio" controls src="${esc(j.preview_url)}" controlsList="nodownload noplaybackrate" oncontextmenu="return false"></audio><p class="muted">${kind==='ringtone'?'Offer ₹10 (regular ₹20).':'Full download ₹19.'}</p><button class="btn" onclick="payAsset('${esc(j.asset_id)}','${kind}')">💳 Pay & Unlock Download</button><p class="muted">Free preview only. Downloading and sharing unlock after verified payment.</p></div>`;pending.asset_id=j.asset_id;pending.kind=kind}catch(e){out.innerHTML=`<div class="notice">${esc(e.message)}</div>`}}
function ringtoneGenerator(){return `<section class="hero"><h1>🎵 Ringtone Generator</h1><p>Customer gives an idea or lyrics → original ringtone generation → free preview → ₹10 offer download.</p></section><div class="card" style="margin-top:18px"><textarea id="ringLyrics" class="field" placeholder="Example: 20-second energetic Telugu folk ringtone for a family celebration…"></textarea><div class="grid"><select id="ringLang" class="field"><option>Telugu</option><option>Hindi</option><option>English</option><option>Tamil</option><option>Kannada</option><option>Malayalam</option></select><select id="ringStyle" class="field"><option>Indian Folk</option><option>Devotional</option><option>Cinematic</option><option>EDM</option><option>Lo-Fi</option><option>Classical Fusion</option></select><select id="ringDur" class="field"><option value="10">10 sec</option><option value="15" selected>15 sec</option><option value="20">20 sec</option><option value="30">30 sec</option></select></div><div class="row" style="margin-top:14px"><button class="btn secondary" onclick="writeRingtoneIdea()">✨ Improve Idea</button><button class="btn" onclick="generateMedia('ringtone')">🎵 Generate Preview</button></div><div id="ringOut" style="margin-top:18px"></div></div>`}async function writeRingtoneIdea(){const field=$('#ringLyrics'),v=field?.value.trim();if(!v)return toast('Enter a ringtone idea.');const card=field.closest('.card'),btn=[...card.querySelectorAll('button')].find(b=>b.getAttribute('onclick')==='writeRingtoneIdea()'),out=$('#ringOut');if(btn?.disabled)return;const oldLabel=btn?.textContent||'';if(btn){btn.disabled=true;btn.textContent='⏳ Improving idea…'}out.innerHTML='<div class="notice" role="status" aria-live="polite">✨ Improving your idea. Please wait; do not click again.</div>';try{const j=await api('ai-text',{type:'ringtone_idea',input:v,language:$('#ringLang').value});field.value=j.text||'';out.innerHTML='<div class="notice" role="status">✅ Idea updated. Review it before generating.</div>'}catch(e){out.innerHTML='<div class="notice" role="alert">'+esc(e.message)+'</div>'}finally{if(btn){btn.disabled=false;btn.textContent=oldLabel}}}
async function startRazorpayPayment(payload,onPaid){
  try{
    if(typeof Razorpay==='undefined')throw Error('Payment checkout is unavailable. Please refresh once and try again.');
    const j=await api('create-payment',payload);
    pending.order_id=j.order_id; pending.kind=payload.kind; pending.asset_id=payload.asset_id||null; pending.item_id=payload.item_id||null;
    const opt={
      key:j.key_id||C.RAZORPAY_KEY_ID,
      amount:j.amount,
      currency:j.currency||'INR',
      name:'NavaBharat AI',
      description:j.description||'NavaBharat AI purchase',
      order_id:j.razorpay_order_id,
      theme:{color:'#ff3d8d'},
      handler:async function(resp){
        try{
          const v=await api('verify-payment',{
            order_id:j.order_id,
            razorpay_order_id:resp.razorpay_order_id,
            razorpay_payment_id:resp.razorpay_payment_id,
            razorpay_signature:resp.razorpay_signature
          });
          if(!v.paid)throw Error('Payment could not be verified yet.');
          pending.paid=true; toast('Payment verified successfully.');
          if(onPaid)await onPaid(j.order_id,v);
        }catch(e){toast('Payment verification: '+e.message)}
      },
      modal:{ondismiss:()=>toast('Payment window closed. Your order is still available in Premium → Recover Order.')},
      prefill:{email:payload.customer?.email||''}
    };
    new Razorpay(opt).open();
  }catch(e){toast(e.message)}
}
async function getPaidDownload(oid){
  const v=await api('verify-payment',{order_id:oid});
  if(!v.paid)throw Error('Payment not confirmed yet.');
  return {v,download:await api('create-download',{order_id:oid})};
}
function paidMediaActions(url,label){
  const safe=esc(url);
  return `<div class="notice success" style="margin-top:12px"><b>✅ Payment verified.</b> Your download is unlocked.</div><div class="row"><a class="btn" href="${safe}" target="_blank" rel="noopener" download>⬇ ${esc(label||'Download')}</a>${share('NavaBharat AI '+(label||'purchase'),url)}</div>`;
}
async function payAsset(id,kind){
  const amount=kind==='ringtone'?10:19;
  await startRazorpayPayment({kind,asset_id:id,amount},async oid=>{
    const d=await api('create-download',{order_id:oid});
    const out=$(kind==='ringtone'?'#ringOut':'#songOut');
    if(out)out.insertAdjacentHTML('beforeend',paidMediaActions(d.download_url,kind==='ringtone'?'Download Ringtone':'Download Song'));
  });
}
async function verifyOrder(){
  try{
    const oid=pending.order_id||new URLSearchParams(location.search).get('order_id')||$('#recover')?.value.trim();
    if(!oid)throw Error('Enter or recover the Order ID');
    const {download}=await getPaidDownload(oid);
    const out=$(pending.kind==='ringtone'?'#ringOut':pending.kind==='song'?'#songOut':'#designOut');
    if(out)out.insertAdjacentHTML('beforeend',paidMediaActions(download.download_url,'Download'));
    else window.open(download.download_url,'_blank','noopener');
  }catch(e){toast(e.message)}
}
async function ringtoneLibrary(){if(sb){const {data}=await sb.from('ringtones').select('*').eq('active',true).order('created_at',{ascending:false});ringtones=data||[]}return `<section class="hero"><h1>📚 Ringtone Library</h1><p>Movie/devotional/language categories are supported when the source is authorized or redistributable. Preview free; regular ₹20, launch offer ₹10.</p></section><div class="card" style="margin-top:18px"><input id="rtQ" class="field" placeholder="Search Telugu, Hindi, devotional, folk, English, Hollywood, Tollywood…" oninput="filterRT()"><div class="filters"><button onclick="setRT('All')">All</button><button onclick="setRT('Telugu')">Telugu</button><button onclick="setRT('Hindi')">Hindi</button><button onclick="setRT('English')">English</button><button onclick="setRT('Devotional')">Devotional</button><button onclick="setRT('Latest')">Latest</button><button onclick="setRT('Folk')">Folk</button></div><div id="rtGrid" class="grid">${ringtones.length?ringtones.map(rtCard).join(''):'<div class="notice">No catalog loaded yet. Run the authorized catalog importer from Supabase.</div>'}</div></div><div class="notice" style="margin-top:18px">⚖️ Commercial movie recordings cannot be copied/rehosted without redistribution rights. The importer is designed for licensed feeds, CC/public-domain sources and your own uploads. The app can still organize all languages/categories once lawful sources are connected.</div>`}let rtF='All';function setRT(f){rtF=f;filterRT()}function filterRT(){const q=($('#rtQ')?.value||'').toLowerCase();const a=ringtones.filter(x=>{const h=[x.title,x.movie,x.artist,x.language,x.category,x.tags].join(' ').toLowerCase();return(!q||h.includes(q))&&(rtF==='All'||x.language===rtF||x.category===rtF||rtF==='Latest')});$('#rtGrid').innerHTML=a.length?a.map(rtCard).join(''):'<div class="notice">No matches.</div>'}function rtCard(x){return `<div class="card"><div class="row"><span class="pill">${esc(x.language)}</span><span class="pill">${esc(x.category)}</span></div><h3>${esc(x.title)}</h3><p class="muted">${esc(x.movie||x.artist||'Authorized / public-domain source')}</p><button class="btn secondary" onclick="previewRT('${x.id}',this)">▶ Free Preview</button><audio class="audio" style="display:none" controls controlsList="nodownload noplaybackrate" oncontextmenu="return false"></audio><div class="row"><span class="price">₹${Number(x.price_inr||10)}</span><button class="btn" onclick="buyRT('${x.id}')">⬇ Download</button></div></div>`}async function previewRT(id,b){try{const j=await api('preview-ringtone',{item_id:id});const a=b.parentElement.querySelector('audio');a.src=j.preview_url;a.style.display='block';a.play()}catch(e){toast(e.message)}}async function buyRT(id){const item=ringtones.find(x=>String(x.id)===String(id));const amount=Math.max(10,Number(item?.price_inr||C.RINGTONE_OFFER_PRICE_INR||10));await startRazorpayPayment({kind:'ringtone',item_id:id,amount},async oid=>{const d=await api('create-download',{order_id:oid});const card=document.querySelector(`[onclick="buyRT('${id}')"]`)?.closest('.card');if(card)card.insertAdjacentHTML('beforeend',paidMediaActions(d.download_url,'Download Ringtone'));});}
function musicLibrary(){return `<section class="hero"><h1>🎧 RacharlaGPT Music Library</h1><p>Your own/generated tracks. Admin publishing is handled in Supabase; customer playback remains separate from the ringtone catalog.</p></section><div class="card"><button class="btn" onclick="loadMusic()">Load Library</button><div id="musicOut" class="grid" style="margin-top:15px"></div></div>`}async function loadMusic(){if(!sb)return toast('Configure Supabase first');const {data,error}=await sb.from('music_library').select('*').eq('published',true).order('created_at',{ascending:false});if(error)return toast('Music Library unavailable. Please run the database permission repair SQL.');$('#musicOut').innerHTML=(data||[]).map(x=>`<div class="card"><h3>${esc(x.title)}</h3><audio class="audio" controls controlsList="nodownload noplaybackrate" oncontextmenu="return false" src="${esc(x.preview_url||x.audio_url||'')}"></audio><p>${share('Listen on NavaBharat AI')}</p></div>`).join('')||'<div class="notice">No published tracks yet.</div>'}
async function adminTestProvider(provider){try{const token=sessionStorage.getItem('nava_admin_token')||'';if(!token)return toast('Unlock Admin first.');const r=await fetch(C.SUPABASE_URL+'/functions/v1/generate-media',{method:'POST',headers:{'Content-Type':'application/json','apikey':C.SUPABASE_ANON_KEY,'x-admin-token':token},body:JSON.stringify({kind:'song',lyrics:'ఆకాశం అంచున నా కల నిలిచింది\nనవ భారత గీతం నాలో మోగింది',language:'Telugu',style:'Tollywood Mass Folk / High Beat',duration:15,vocal_type:'Solo Male Vocalist',admin_test:true,test_provider:provider})});const j=await r.json();if(!r.ok)throw Error(j.error||'Provider test failed');const panel=$('#adminStatus');if(panel)panel.innerHTML=`<div class="notice">${esc(provider)} test succeeded. <audio class="audio" controls src="${esc(j.preview_url)}"></audio></div>`}catch(e){const panel=$('#adminStatus');if(panel)panel.innerHTML='<div class="notice">Provider test failed: '+esc(e.message)+'</div>'}}
function admin(){return `<section class="hero"><h1>🔐 Admin Studio</h1><p>Private management for your own RacharlaGPT Music tracks and your authorized ringtone catalog. Nothing here exposes provider keys.</p></section><div class="card"><h3>Admin access</h3><input id="adminToken" class="field" type="password" placeholder="Admin API token"><button class="btn" onclick="adminLogin()">Unlock Admin</button><div id="adminStatus" class="muted" style="margin-top:8px"></div><div class="row" style="margin-top:10px"><button class="btn secondary" onclick="adminTestProvider('acestep')">Test Music Engine A</button><button class="btn secondary" onclick="adminTestProvider('gemini')">Test Music Engine B</button><button class="btn secondary" onclick="adminTestProvider('apiframe')">Test Music Engine C</button></div></div><div id="adminPanel" class="hidden">${window.NavaAds?.adminPanel()||''}<div class="grid"><div class="card"><h3>🎧 Upload RacharlaGPT Music</h3><input id="musicFile" class="field" type="file" accept="audio/*"><input id="musicTitle" class="field" placeholder="Track title"><input id="musicLang" class="field" placeholder="Language"><input id="musicGenre" class="field" placeholder="Genre"><button class="btn" onclick="adminUploadMusic()">Upload & Publish</button></div><div class="card"><h3>🎵 Upload Ringtone</h3><input id="rtFile" class="field" type="file" accept="audio/*"><input id="rtTitle" class="field" placeholder="Ringtone title"><input id="rtMovie" class="field" placeholder="Movie / source name (optional)"><input id="rtArtist" class="field" placeholder="Artist / creator (optional)"><input id="rtLang" class="field" placeholder="Language"><input id="rtCategory" class="field" placeholder="Category e.g. Devotional / Folk"><input id="rtRegular" class="field" type="number" min="10" value="20" placeholder="Actual price ₹20+"><input id="rtPrice" class="field" type="number" min="10" value="10" placeholder="Offer price ₹10+"><input id="rtLicense" class="field" placeholder="License / permission reference"><label class="check"><input id="rtRights" type="checkbox"> I confirm I have redistribution rights for this upload</label><button class="btn" onclick="adminUploadRingtone()">Upload Ringtone</button></div><div class="card"><h3>🔄 Authorized Catalog</h3><p class="muted">Imports only sources whose license is recorded in Supabase. It does not scrape commercial movie sites.</p><button class="btn" onclick="refreshCatalog()">Refresh / Load Latest Authorized</button></div><div class="card"><h3>🗑️ Manage</h3><button class="btn secondary" onclick="adminLoadItems()">Load My Uploaded Items</button><div id="adminItems" style="margin-top:12px"></div></div></div></div>`}
function adminHeaders(){const t=sessionStorage.getItem('nava_admin_token')||$('#adminToken')?.value.trim();if(!t)throw Error('Enter the admin token');return {'x-admin-token':t}}
function adminLogin(){const t=$('#adminToken').value.trim();if(!t)return toast('Enter the admin token');sessionStorage.setItem('nava_admin_token',t);$('#adminPanel').classList.remove('hidden');$('#adminStatus').textContent='Admin controls unlocked for this browser session.';if('Notification' in window&&Notification.permission==='default')Notification.requestPermission().catch(()=>{});adminLoadItems().catch(e=>toast(e.message));clearInterval(window.__adminPoll);window.__adminPoll=setInterval(()=>adminLoadItems().catch(()=>{}),30000)}
function fileB64(file){return new Promise((resolve,reject)=>{const r=new FileReader();r.onload=()=>resolve(String(r.result));r.onerror=reject;r.readAsDataURL(file)})}
async function adminUploadMusic(){try{const f=$('#musicFile').files[0];if(!f)return toast('Choose an audio file');const body={type:'music',title:$('#musicTitle').value.trim()||f.name,language:$('#musicLang').value.trim(),genre:$('#musicGenre').value.trim(),data:await fileB64(f),mime:f.type};const j=await fetch(C.SUPABASE_URL+'/functions/v1/admin-upload',{method:'POST',headers:{'Content-Type':'application/json',...adminHeaders(),'apikey':C.SUPABASE_ANON_KEY},body:JSON.stringify(body)});const x=await j.json();if(!j.ok)throw Error(x.error||'Upload failed');toast('Music uploaded and published');adminLoadItems()}catch(e){toast(e.message)}}
async function adminUploadRingtone(){try{const f=$('#rtFile').files[0];if(!f)return toast('Choose an audio file');if(!$('#rtRights').checked)return toast('Confirm redistribution rights before uploading');const price=Math.max(10,Number($('#rtPrice').value||10));const body={type:'ringtone',title:$('#rtTitle').value.trim()||f.name,movie:$('#rtMovie').value.trim(),artist:$('#rtArtist').value.trim(),language:$('#rtLang').value.trim()||'English',category:$('#rtCategory').value.trim()||'Ringtone',regular_price_inr:Math.max(10,Number($('#rtRegular').value||20)),price_inr:price,license:$('#rtLicense').value.trim(),rights_confirmed:true,data:await fileB64(f),mime:f.type};const j=await fetch(C.SUPABASE_URL+'/functions/v1/admin-upload',{method:'POST',headers:{'Content-Type':'application/json',...adminHeaders(),'apikey':C.SUPABASE_ANON_KEY},body:JSON.stringify(body)});const x=await j.json();if(!j.ok)throw Error(x.error||'Upload failed');toast('Ringtone uploaded at ₹'+price);adminLoadItems()}catch(e){toast(e.message)}}
async function adminLoadItems(){try{const t=sessionStorage.getItem('nava_admin_token');if(!t)return;const j=await fetch(C.SUPABASE_URL+'/functions/v1/admin-list',{method:'POST',headers:{'Content-Type':'application/json',...adminHeaders(),'apikey':C.SUPABASE_ANON_KEY},body:'{}'});const x=await j.json();if(!j.ok)throw Error(x.error||'Admin list failed');const orders=x.orders||[];const previous=Number(sessionStorage.getItem('nava_last_order_count')||0);const paidGifts=orders.filter(o=>o.kind==='gift'&&o.razorpay_status==='paid');if(orders.length>previous&&previous>0){const newest=orders.find(o=>o.kind==='gift'&&o.razorpay_status==='paid')||orders[0];toast('New customer order received'+(newest?.public_order_id?' — '+newest.public_order_id:''));if('Notification' in window&&Notification.permission==='granted')new Notification('NavaBharat AI — New Order',{body:(newest?.kind==='gift'?'Personalised Song Gift':'New paid order')+' '+(newest?.public_order_id||'')});}sessionStorage.setItem('nava_last_order_count',String(orders.length));const orderHtml=orders.slice(0,20).map(o=>{const c=o.customer_data||{};return `<div class="notice"><b>💳 ${esc(o.kind)}</b> · <b>₹${esc(o.amount_inr)}</b> · ${esc(o.razorpay_status||'')}</div><div class="muted" style="margin:-4px 0 10px 0">Order: ${esc(o.public_order_id)} · ${esc(c.name||o.customer_email||'')} ${c.whatsapp?'· WhatsApp: '+esc(c.whatsapp):''}${c.message?' · '+esc(c.message):''}</div>`}).join('');const itemsEl=$('#adminItems');if(!itemsEl)return;itemsEl.innerHTML='<h4>Recent customer orders</h4>'+(orderHtml||'<p class="muted">No orders yet.</p>')+'<h4 style="margin-top:18px">Uploaded catalog</h4>'+(x.ringtones||[]).map(a=>`<div class="notice"><b>${esc(a.title)}</b> · ₹${a.price_inr} · ${esc(a.language||'')} <button class="btn small" onclick="adminDeleteRingtone('${a.id}')">Deactivate</button></div>`).join('')+(x.music||[]).map(a=>`<div class="notice"><b>🎧 ${esc(a.title)}</b> · ${esc(a.language||'')} <button class="btn small" onclick="adminDeleteMusic('${a.id}')">Unpublish</button></div>`).join('')||'No uploaded items.'}catch(e){toast(e.message)}}
async function adminDeleteRingtone(id){try{const r=await fetch(C.SUPABASE_URL+'/functions/v1/admin-delete-ringtone',{method:'POST',headers:{'Content-Type':'application/json',...adminHeaders(),'apikey':C.SUPABASE_ANON_KEY},body:JSON.stringify({id})});const j=await r.json();if(!r.ok)throw Error(j.error||'Delete failed');toast('Ringtone deactivated');adminLoadItems()}catch(e){toast(e.message)}}
async function adminDeleteMusic(id){try{const r=await fetch(C.SUPABASE_URL+'/functions/v1/admin-delete-music',{method:'POST',headers:{'Content-Type':'application/json',...adminHeaders(),'apikey':C.SUPABASE_ANON_KEY},body:JSON.stringify({id})});const j=await r.json();if(!r.ok)throw Error(j.error||'Unpublish failed');toast('Track unpublished');adminLoadItems()}catch(e){toast(e.message)}}
async function refreshCatalog(){try{const j=await fetch(C.SUPABASE_URL+'/functions/v1/refresh-catalog',{method:'POST',headers:{'Content-Type':'application/json',...adminHeaders(),'apikey':C.SUPABASE_ANON_KEY},body:'{}'}).then(async r=>{const j=await r.json();if(!r.ok)throw Error(j.error||'Catalog refresh failed');return j});toast('Catalog refreshed: '+(j.imported||0)+' authorized items')}catch(e){toast(e.message)}}
function currentAffairs(){return `<section class="hero"><h1>🗞️ Daily Current Affairs</h1><p>Dated, source-linked headlines and a free headline quiz without requiring AI.</p></section><div class="card"><div class="grid"><select id="caLang" class="field"><option>English</option><option>Telugu</option><option>Hindi</option><option>Tamil</option><option>Kannada</option><option>Malayalam</option></select><select id="caCat" class="field"><option>All</option><option>India</option><option>World</option><option>Business</option><option>Technology</option><option>Science</option><option>Sports</option><option>Education</option></select><select id="caCount" class="field"><option>5</option><option>10</option><option selected>12</option><option>15</option><option>20</option></select></div><button class="btn" onclick="loadCurrentAffairs()">📰 Load Today's Current Affairs</button><div id="caOut" style="margin-top:15px"></div></div>`}async function loadCurrentAffairs(){
 const lang=$('#caLang').value,cat=$('#caCat').value,count=Number($('#caCount').value);
 $('#caOut').innerHTML='<div class="notice" role="status">Fetching dated, linked headlines…</div>';
 window.__caItems=[];
 try{
  const j=await api('live-rss',{kind:'current_affairs',category:cat,query:cat==='All'?'India latest news':cat,language:lang,limit:count});
  const items=(j.items||[]).slice(0,count);
  window.__caItems=items;
  const cards=navaNewsCards(items,j.provider);
  $('#caOut').innerHTML=(cards||navaExternalNewsLinks(cat==='All'?'India current affairs':cat+' news'))+
   (items.length>=3?'<button class="btn secondary" onclick="makeCurrentQuiz()">📝 Free Headline Quiz (no AI required)</button>':'');
 }catch(e){$('#caOut').innerHTML=navaExternalNewsLinks(cat==='All'?'India current affairs':cat+' news')}
}
function makeCurrentQuiz(){
 const items=(window.__caItems||[]).filter(x=>x.title&&x.link).slice(0,12);
 if(items.length<3)return toast('Load at least three linked headlines first.');
 const chosen=items.slice(0,Math.min(5,items.length));
 const quizzes=chosen.map((item,i)=>{
  const other=items.filter(x=>x!==item).slice(i%2).concat(items.filter(x=>x!==item)).slice(0,3);
  const options=[...other,item].sort((a,b)=>((a.title.length+i)%7)-((b.title.length+i)%7));
  const clue=item.title.split(/\s+/).slice(0,Math.min(5,item.title.split(/\s+/).length)).join(' ');
  return `<div class="card"><h4>${i+1}. Which real headline begins with "${esc(clue)}…"?</h4><ol>${options.map(x=>'<li>'+esc(x.title)+'</li>').join('')}</ol><details><summary>Show answer and source</summary><p><strong>${esc(item.title)}</strong></p><a href="${esc(item.link)}" target="_blank" rel="noopener noreferrer">Read original linked source ↗</a></details></div>`;
 });
 $('#caOut').insertAdjacentHTML('beforeend','<div class="card"><h3>📝 Source-linked headline recognition quiz</h3><p class="muted">Created only from the retrieved headline titles. It does not invent facts or depend on Gemini.</p>'+quizzes.join('')+'</div>');
}
function jobs(){return `<section class="hero"><h1>💼 Jobs & Competitive Exams</h1><p>Recruitment-specific news links and official exam portals. Confirm vacancies on the official source.</p></section><div class="card"><select id="jobsCat" class="field"><option>All Government Jobs</option><option>Banking & Finance</option><option>SSC & Railways</option><option>UPSC & Civil Services</option><option>State Public Service Commissions</option></select><button class="btn" onclick="loadJobs()">🔍 Search Job & Exam Updates</button><div id="jobsOut" style="margin-top:15px"></div></div>`}async function loadJobs(){
 const cat=$('#jobsCat').value;
 $('#jobsOut').innerHTML='<div class="notice" role="status">Checking recruitment-specific headlines…</div>';
 try{
  const r=await api('live-rss',{kind:'jobs',category:cat,query:cat,language:'English',limit:20});
  const cards=navaNewsCards(r.items,r.provider);
  $('#jobsOut').innerHTML=(cards||navaExternalNewsLinks(cat+' government recruitment'))+navaOfficialJobLinks()+
   '<p class="muted">News articles are leads, not official vacancies. Check eligibility, deadlines and application links directly on the recruitment portal.</p>';
 }catch(e){$('#jobsOut').innerHTML=navaOfficialJobLinks()+navaExternalNewsLinks(cat+' government recruitment')}
}
function creator(){return `<section class="hero"><h1>✨ Creator Studio</h1><p>Generate YouTube, Instagram, LinkedIn and X content with share-ready drafts.</p></section><div class="card"><input id="creatorTopic" class="field" placeholder="Content topic / idea"><select id="creatorPlatform" class="field"><option>YouTube Video Script & Metadata</option><option>Instagram Reel Caption & Hashtags</option><option>LinkedIn Thought Leadership Post</option><option>Twitter/X Thread</option></select><button class="btn" style="margin-top:12px" onclick="creatorGo()">✨ Generate Viral Content</button><div id="creatorOut" style="margin-top:18px"></div></div>`}async function creatorGo(){const topic=$('#creatorTopic').value.trim();if(!topic)return;$('#creatorOut').innerHTML='<div class="notice">Creating…</div>';try{const j=await api('ai-text',{type:'creator',input:topic+'\nPlatform: '+$('#creatorPlatform').value,language:'English'});$('#creatorOut').innerHTML=`<pre class="output">${esc(j.text)}</pre>${share('NavaBharat AI creator draft: '+topic)}`}catch(e){toast(e.message)}}
function design(){return `<section class="hero"><h1>🎨 NavaBharat Design Studio</h1><p>Create posters, 3D-style text graphics, thumbnails and stories. Free preview has branding; HD no-watermark export ₹9.</p></section><div class="card"><h3>🎨 Poster Design</h3><div class="grid"><div><input id="dTitle" class="field" placeholder="Main headline"><textarea id="dSub" class="field" placeholder="Supporting text"></textarea><input id="dFoot" class="field" value="NavaBharat AI"></div><div><select id="dFormat" class="field"><option>Instagram Square</option><option>Instagram Portrait</option><option>Instagram / WhatsApp Story</option><option>YouTube Thumbnail</option><option>LinkedIn Post</option><option>Quote Poster</option><option>Announcement</option></select><select id="dTheme" class="field"><option>Aurora</option><option>Sunset</option><option>Ocean</option><option>Emerald</option><option>Royal</option><option>Midnight</option></select><input id="dPhoto" class="field" type="file" accept="image/*"><button class="btn" onclick="makeDesign()">✨ Create Design</button></div></div><div id="designOut" style="margin-top:18px"></div></div><div class="card" style="margin-top:18px"><h3>🧊 3D Text Poster</h3><div class="grid"><input id="d3Text" class="field" maxlength="60" placeholder="Happy Sankranti / హ్యాపీ బర్త్‌డే"><input id="d3Sub" class="field" maxlength="90" placeholder="Small line"><select id="d3Fmt" class="field"><option>Instagram Square</option><option>Instagram Portrait</option><option>Instagram / WhatsApp Story</option><option>YouTube Thumbnail</option></select><select id="d3Style" class="field"><option>Chrome 3D</option><option>Neon 3D</option><option>Gold 3D</option><option>Glass 3D</option></select><select id="d3Bg" class="field"><option>Midnight</option><option>Aurora</option><option>Sunset</option><option>Ocean</option><option>Royal</option><option>Emerald</option></select><input id="d3Foot" class="field" value="NavaBharat AI"></div><button class="btn" onclick="make3DPoster()">🧊 Create 3D Poster</button><div id="design3dOut" style="margin-top:18px"></div></div>`}
function wrapCanvas(x,t,cx,cy,w,lh){let words=String(t||'').split(/\s+/),line='';for(const word of words){const test=line?line+' '+word:word;if(x.measureText(test).width>w){x.fillText(line,cx,cy);line=word;cy+=lh}else line=test}if(line)x.fillText(line,cx,cy)}
async function makeDesign(){
 const title=$('#dTitle').value.trim(); if(!title)return toast('Enter a headline.');
 const subtitle=$('#dSub').value.trim(),footer=$('#dFoot').value.trim()||'NavaBharat AI';
 const ratioMap={'Instagram Square':'1:1','Instagram Portrait':'4:5','Instagram / WhatsApp Story':'9:16','YouTube Thumbnail':'16:9','LinkedIn Post':'16:9','Quote Poster':'4:5','Announcement':'1:1'};
 const p={kind:'design',title,subtitle,footer,style:$('#dTheme').value,aspect_ratio:ratioMap[$('#dFormat').value]||'1:1',image_size:'2K'};
 $('#designOut').innerHTML='<div class="notice">✨ AI is designing a professional visual preview…</div>';
 try{const j=await api('generate-media',p);localStorage.setItem('nava-design-pending',JSON.stringify({...p,asset_id:j.asset_id,preview_url:j.preview_url}));$('#designOut').innerHTML=`<div class="ai-preview"><img style="width:100%;border-radius:18px;display:block" src="${esc(j.preview_url)}"><div class="preview-badge">AI PREVIEW • HD unlocked after purchase</div></div><div class="row"><span class="muted">Preview only — download & sharing unlock after payment.</span><button class="btn" onclick="payDesignHD()">💎 Unlock HD</button></div>`}
 catch(e){$('#designOut').innerHTML='<div class="notice">'+esc(e.message)+'</div>'}
}
async function make3DPoster(){
 const title=$('#d3Text').value.trim(); if(!title)return toast('Type some text first.');
 const subtitle=$('#d3Sub').value.trim(),footer=$('#d3Foot').value.trim()||'NavaBharat AI';
 const ratioMap={'Instagram Square':'1:1','Instagram Portrait':'4:5','Instagram / WhatsApp Story':'9:16','YouTube Thumbnail':'16:9'};
 const p={kind:'3d-design',title,subtitle,footer,style:$('#d3Style').value,background:$('#d3Bg').value,aspect_ratio:ratioMap[$('#d3Fmt').value]||'1:1',image_size:'2K'};
 $('#design3dOut').innerHTML='<div class="notice">🧊 AI is building a premium 3D visual…</div>';
 try{const j=await api('generate-media',p);localStorage.setItem('nava-design-pending',JSON.stringify({...p,asset_id:j.asset_id,preview_url:j.preview_url}));$('#design3dOut').innerHTML=`<div class="ai-preview"><img style="width:100%;border-radius:18px;display:block" src="${esc(j.preview_url)}"><div class="preview-badge">AI 3D PREVIEW • HD unlocked after purchase</div></div><div class="row"><span class="muted">Preview only — download & sharing unlock after payment.</span><button class="btn" onclick="payDesignHD()">💎 Unlock HD</button></div>`}
 catch(e){$('#design3dOut').innerHTML='<div class="notice">'+esc(e.message)+'</div>'}
}
async function payDesignHD(){
 const p=JSON.parse(localStorage.getItem('nava-design-pending')||'null');
 if(!p?.asset_id)return toast('Create the AI design first.');
 await startRazorpayPayment({kind:'design',asset_id:p.asset_id,amount:9,customer:{design:{type:p.kind||p.type,title:p.title}}},async oid=>{
   const d=await api('create-download',{order_id:oid});
   const out=p.kind==='3d-design'?$('#design3dOut'):$('#designOut');
   if(out)out.insertAdjacentHTML('beforeend',paidMediaActions(d.download_url,'Download HD Design'));
 });
}
async function downloadPaidDesign(){
 const oid=pending.order_id||new URLSearchParams(location.search).get('order_id');
 if(!oid)return toast('Create an HD order first.');
 const {download}=await getPaidDownload(oid);
 const out=$('#designOut')||$('#design3dOut');
 if(out)out.insertAdjacentHTML('beforeend',paidMediaActions(download.download_url,'Download HD Design'));
}
function shareDesign(){const p=JSON.parse(localStorage.getItem('nava-design-pending')||'null');if(!p?.preview_url)return toast('Create a design first.');if(!pending.paid)return toast('Sharing unlocks after verified payment.');if(navigator.share){navigator.share({title:'NavaBharat AI Design',url:location.href}).catch(()=>{})}else{navigator.clipboard?.writeText(p.preview_url);toast('Preview link copied.')}} 
function video(){return `<section class="hero"><h1>🎬 Video Studio & Audio Extractor</h1><p>Extract MP3 or create shareable reels locally in your browser. Your free photos and audio are not uploaded to Supabase.</p></section><div class="grid"><div class="card"><h3>🎵 Extract MP3</h3><input id="videoFile" class="field" type="file" accept="video/*"><button class="btn" style="margin-top:10px" onclick="extractAudio()">⚡ Extract MP3</button><div id="videoOut"></div></div><div class="card"><h3>🎞️ Build Reel Video</h3><label for="reelImgs">Photos (up to 12)</label><input id="reelImgs" class="field" type="file" accept="image/jpeg,image/png,image/webp" multiple><label for="reelMusic">Optional music (MP3, WAV, M4A)</label><input id="reelMusic" class="field" type="file" accept="audio/*"><div class="grid nava-reel-controls"><label>Video aspect ratio<select class="field" id="reelRatio"><option value="9:16">Vertical 9:16 (Reels / Shorts)</option><option value="1:1">Square 1:1</option><option value="16:9">Landscape 16:9</option></select></label><label>Video resolution<select class="field" id="reelQuality"><option value="360">Fast (360p width)</option><option value="540" selected>Standard HD (540p width)</option><option value="720">HD (720p width)</option><option value="1080">Full HD (slower)</option></select></label><label>Seconds per photo<input id="reelSeconds" class="field" type="number" min="1" max="8" step="1" value="3"></label></div><div class="notice" role="note">Reel creation can take time on mobile. The music loops if it is shorter than the reel. You can download only after rendering succeeds.</div><button id="reelBuildBtn" class="btn" onclick="buildReel()">🎞️ Render Reel MP4</button><div id="reelOut" role="status" aria-live="polite" style="margin-top:12px"></div></div></div>`}
let ffmpegInstance=null;async function getFFmpeg(){
 if(ffmpegInstance)return ffmpegInstance;
 if(!window.FFmpegWASM){
   const base='https://cdn.jsdelivr.net/npm/@ffmpeg/ffmpeg@0.12.10/dist/umd/';
   const main=await fetch(base+'ffmpeg.js',{cache:'force-cache'}).then(r=>{if(!r.ok)throw Error('FFmpeg library unavailable');return r.text()});
   const workerURL=URL.createObjectURL(await fetch(base+'814.ffmpeg.js',{cache:'force-cache'}).then(r=>{if(!r.ok)throw Error('FFmpeg worker unavailable');return r.blob()}));
   window.__navaFfmpegWorkerURL=workerURL;
   const patched=main
     .replace(/new Worker\(new URL\(e\.p\+e\.u\(814\),e\.b\),\{type:void 0\}\)/g,'new Worker(window.__navaFfmpegWorkerURL,{type:void 0})')
     .replace(/new Worker\(new URL\(e\.p \+ e\.u\(814\), e\.b\),\{ type: void 0 \}\)/g,'new Worker(window.__navaFfmpegWorkerURL,{type:void 0})');
   const boot=patched;
   const s=document.createElement('script');s.text=boot;document.head.appendChild(s);
 }
 const {FFmpeg}=window.FFmpegWASM;if(!FFmpeg)throw Error('FFmpeg failed to initialize');
 const f=new FFmpeg();const baseCore='https://cdn.jsdelivr.net/npm/@ffmpeg/core@0.12.6/dist/umd';
 await f.load({coreURL:baseCore+'/ffmpeg-core.js',wasmURL:baseCore+'/ffmpeg-core.wasm'});ffmpegInstance=f;return f
}
async function extractAudio(){const file=$('#videoFile')?.files?.[0];if(!file)return toast('Upload a video first.');try{const f=await getFFmpeg();await f.writeFile('input',new Uint8Array(await file.arrayBuffer()));await f.exec(['-i','input','-vn','-codec:a','libmp3lame','-b:a','192k','output.mp3']);const data=await f.readFile('output.mp3');const blob=new Blob([data.buffer],{type:'audio/mpeg'}),url=URL.createObjectURL(blob);$('#videoOut').innerHTML=`<div class="notice">Audio extracted successfully.</div><audio class="audio" controls src="${url}"></audio><br><a class="btn" download="${esc(file.name.replace(/\.[^.]+$/,'')+'_audio.mp3')}" href="${url}">⬇ Download MP3</a>`}catch(e){$('#videoOut').innerHTML='<div class="notice">Extraction error: '+esc(e.message)+'</div>'}}
let navaLastReelURL=null;let navaReelBusy=false;
async function navaReelConvertImage(file, w, h){
  if(!/^image\/(png|jpeg|webp)$/.test(file.type))throw Error('Use JPG, PNG or WebP images.');
  const img=await createImageBitmap(file);try{
    const canvas=document.createElement('canvas');canvas.width=w;canvas.height=h;
    const ctx=canvas.getContext('2d',{alpha:false});if(!ctx)throw Error('Canvas is unavailable');
    ctx.fillStyle='#0b1024';ctx.fillRect(0,0,w,h);
    const scale=Math.min(w/img.width,h/img.height),width=Math.round(img.width*scale),height=Math.round(img.height*scale);
    ctx.drawImage(img,Math.round((w-width)/2),Math.round((h-height)/2),width,height);
    const blob=await new Promise(resolve=>canvas.toBlob(resolve,'image/jpeg',.86));
    if(!blob)throw Error('Unable to process one of your photos.');
    return new Uint8Array(await blob.arrayBuffer());
  }finally{img.close?.()}
}
async function buildReel(){
 const images=[...($('#reelImgs')?.files||[])],music=$('#reelMusic')?.files?.[0];
 if(navaReelBusy)return;
 if(!images.length)return toast('Select photos first.');
 if(images.length>12)return toast('Choose up to 12 photos per reel to protect phone memory.');
 const ratio=$('#reelRatio')?.value||'9:16',quality=Number($('#reelQuality')?.value||540),secs=Number($('#reelSeconds')?.value||3);
 if(!['9:16','1:1','16:9'].includes(ratio)||![360,540,720,1080].includes(quality)||!Number.isInteger(secs)||secs<1||secs>8)return toast('Check reel settings.');
 const [a,b]=ratio.split(':').map(Number);let width=quality,height=Math.round(quality*b/a/2)*2;
 if(width%2)width++;const duration=images.length*secs;
 if(music&&music.size>25*1024*1024)return toast('Choose music smaller than 25 MB.');
 navaReelBusy=true;const btn=$('#reelBuildBtn'),out=$('#reelOut');if(btn){btn.disabled=true;btn.textContent='Rendering… please wait'}
 let ff=null;const paths=[];
 try{
  out.innerHTML='<div class="notice">Preparing photos… Please keep this tab open.</div>';
  ff=await getFFmpeg();
  for(let i=0;i<images.length;i++){
    out.textContent=`Preparing photo ${i+1} of ${images.length}…`;
    const path=`nava_slide_${i}.jpg`;await ff.writeFile(path,await navaReelConvertImage(images[i],width,height));paths.push(path);
  }
  let list=paths.map(p=>`file '${p}'\nduration ${secs}\n`).join('');list+=`file '${paths[paths.length-1]}'\n`;
  await ff.writeFile('nava_slides.txt',new TextEncoder().encode(list));paths.push('nava_slides.txt');
  const args=['-f','concat','-safe','0','-i','nava_slides.txt'];
  if(music){
    const ext=(music.name.split('.').pop()||'mp3').toLowerCase();if(!['mp3','wav','m4a','aac','ogg'].includes(ext))throw Error('Please use MP3, WAV, M4A, AAC or OGG music.');
    const mp='nava_music.'+ext;await ff.writeFile(mp,new Uint8Array(await music.arrayBuffer()));paths.push(mp);
    args.push('-stream_loop','-1','-i',mp);
  }
  args.push('-t',String(duration),'-vf',`scale=${width}:${height}:flags=lanczos,setsar=1`,'-r','24','-c:v','libx264','-preset','ultrafast','-crf','27','-pix_fmt','yuv420p');
  if(music)args.push('-c:a','aac','-b:a','128k');else args.push('-an');
  args.push('-movflags','+faststart','nava_export.mp4');paths.push('nava_export.mp4');
  out.innerHTML='<div class="notice">Encoding MP4… This can take a few minutes.</div>';
  const code=await ff.exec(args);if(code!==0)throw Error('Video encoder failed (code '+code+'). Try Fast quality.');
  const data=await ff.readFile('nava_export.mp4');if(!data||data.length<1024)throw Error('Video was not generated successfully.');
  if(navaLastReelURL)URL.revokeObjectURL(navaLastReelURL);
  navaLastReelURL=URL.createObjectURL(new Blob([data],{type:'video/mp4'}));
  out.innerHTML=`<div class="notice ok">MP4 ready: ${width}×${height} · approximately ${duration} seconds.</div><video class="nava-reel-preview" controls playsinline preload="metadata" src="${navaLastReelURL}"></video><a class="btn" download="navabharat_reel_${ratio.replace(':','x')}.mp4" href="${navaLastReelURL}">⬇ Download Reel MP4</a>`;
 }catch(e){out.innerHTML='<div class="notice">Reel rendering failed: '+esc(e.message)+'. Try fewer images or Fast quality.</div>'}
 finally{
  if(ff)for(const path of paths){try{await ff.deleteFile(path)}catch{}}
  navaReelBusy=false;if(btn){btn.disabled=false;btn.textContent='🎞️ Render Reel MP4'}
 }
}
function premium(){return `<section class="hero"><h1>💎 Premium & Support</h1><p>Secure Razorpay support, personalised song requests and order recovery — no customer login required.</p></section><div class="grid"><div class="card"><h3>❤️ Support RacharlaGPT</h3><p class="muted">Support the project and help keep the free tools available.</p><div class="row">${[19,49,99,199].map(x=>`<button class="btn" onclick="tip(${x})">₹${x}</button>`).join('')}</div></div><div class="card"><h3>🎁 Personalised Song</h3><input id="giftName" class="field" placeholder="Name"><input id="giftWa" class="field" placeholder="WhatsApp number"><textarea id="giftMsg" class="field" placeholder="Occasion and message"></textarea><button class="btn" onclick="giftPay()">Continue to Razorpay</button></div><div class="card"><h3>🔎 Recover Order</h3><input id="recover" class="field" placeholder="Order ID"><button class="btn" style="margin-top:10px" onclick="recover()">Check Status</button><div id="recoverOut"></div></div></div><div class="notice" style="margin-top:18px">All payments are processed through Razorpay. Your card/UPI details never enter this website.</div>`}async function tip(a){await startRazorpayPayment({kind:'tip',amount:a},async()=>toast('Thank you for your support ❤️'));}async function giftPay(){const name=$('#giftName').value.trim(),wa=$('#giftWa').value.trim(),msg=$('#giftMsg').value.trim();if(!name||!wa)return toast('Name and WhatsApp are required.');await startRazorpayPayment({kind:'gift',amount:99,customer:{name,whatsapp:wa,message:msg}},async()=>toast('Personalised song order paid successfully.'));}async function recover(){try{const j=await api('order-status',{order_id:$('#recover').value.trim()});$('#recoverOut').innerHTML=`<div class="notice">${esc(j.message||'')}<br>${esc(j.order_id||'')}</div>`}catch(e){toast(e.message)}}
function about(){return `<section class="hero"><h1>ℹ️ About NavaBharat AI</h1><p>NavaBharat AI is a product of RacharlaGPT, created to bring practical AI tools, music creation, search and creator utilities together in a fast web app.</p></section><div class="card" style="margin-top:18px"><h3>Brand & Developer</h3><p class="muted">Designed & developed by <b>Saikrishna Racharla</b>.</p><p><a href="https://youtube.com/@racharlagpt" target="_blank">youtube.com/@racharlagpt</a></p><p>Karimnagar, Telangana, India</p></div>`}function privacy(){return `<section class="hero"><h1>🔒 Privacy</h1><p>We use Supabase for application data, Razorpay for payments and analytics/advertising services where enabled. Payment credentials are handled by Razorpay. API provider secrets are kept server-side in Supabase Edge Functions.</p></section><div class="card" style="margin-top:18px"><h3>Data principles</h3><p class="muted">No customer account is required for small purchases. Order IDs are used for recovery. Generated media may be retained according to the service's storage/cleanup policy. Do not upload sensitive personal information.</p></div>`}function contact(){return `<section class="hero"><h1>✉️ Contact</h1><p>For support, copyright/licensing questions, paid-order issues or business enquiries.</p></section><div class="card" style="margin-top:18px"><p>Email: <a href="mailto:${C.CONTACT_EMAIL}">${C.CONTACT_EMAIL}</a></p><p>Karimnagar, Telangana, India</p><p>YouTube: <a href="${C.CHANNEL_URL}" target="_blank">@racharlagpt</a></p></div>`}
function render(){const map={home,solve,musicGenerator,'music-generator':musicGenerator,music:musicGenerator,song:musicGenerator,'create-song':musicGenerator,'ringtone-generator':ringtoneGenerator,'ringtone-library':ringtoneLibrary,search,science,translator,live,'current-affairs':currentAffairs,jobs,'music-library':musicLibrary,admin,video,advertise:()=>window.NavaAds?.page()||'<div class="notice">Advertisement tools are loading. Please refresh.</div>',creator,premium,about,privacy,contact};const f=map[current]||home;const r=f();if(r instanceof Promise)r.then(x=>{ $('#app').innerHTML='<div class="content">'+x+'</div>';window.NavaAds?.afterRender(current);}).catch(e=>$('#app').innerHTML='<div class="content"><div class="notice">Unable to render this page: '+esc(e.message)+'</div></div>');else {$('#app').innerHTML='<div class="content">'+r+'</div>';window.NavaAds?.afterRender(current);}}window.go=go;window.runAI=runAI;window.writeLyrics=writeLyrics;window.generateMedia=generateMedia;window.writeRingtoneIdea=writeRingtoneIdea;window.payAsset=payAsset;window.verifyOrder=verifyOrder;window.setRT=setRT;window.filterRT=filterRT;window.previewRT=previewRT;window.buyRT=buyRT;window.loadMusic=loadMusic;window.creatorGo=creatorGo;window.makeDesign=makeDesign;window.extractAudio=extractAudio;window.buildReel=buildReel;window.make3DPoster=make3DPoster;window.payDesignHD=payDesignHD;window.downloadPaidDesign=downloadPaidDesign;window.loadLiveRSS=loadLiveRSS;window.loadCurrentAffairs=loadCurrentAffairs;window.makeCurrentQuiz=makeCurrentQuiz;window.loadJobs=loadJobs;window.adminTestProvider=adminTestProvider;window.makeSearchImage=makeSearchImage;window.tip=tip;window.giftPay=giftPay;window.recover=recover;async function handlePaymentReturn(){const q=new URLSearchParams(location.search);const oid=q.get('order_id');if(q.get('payment')!=='done'||!oid)return;try{const j=await api('verify-payment',{order_id:oid});if(j.paid){toast('Payment confirmed: '+oid);if(['song','ringtone','design'].includes(j.kind||'')){const d=await api('create-download',{order_id:oid});location.href=d.download_url;return}if(j.kind==='design'){downloadPaidDesign();return}}else toast('Payment is still pending. Use Premium → Recover Order with '+oid)}catch(e){toast('Payment return: '+e.message)}}
const p=new URLSearchParams(location.search).get('page');go(p||'home');handlePaymentReturn();
fetch('/version.json?ts='+Date.now(),{cache:'no-store'}).then(r=>r.json()).then(v=>{
 if(v.version!==C.APP_VERSION){
   $('#updateBar').classList.remove('hidden');
   $('#refreshBtn').onclick=async()=>{ $('#updateBar').classList.add('hidden'); try{const regs=await navigator.serviceWorker?.getRegistrations?.()||[]; await Promise.all(regs.map(r=>r.update()));}catch{} location.reload(); };
 }else $('#updateBar').classList.add('hidden');
}).catch(()=>$('#updateBar').classList.add('hidden'));

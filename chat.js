/* Free, isolated chat extension for NavaBharat AI. No payment or login dependency. */
(() => {
  'use strict';
  const HISTORY_KEY = 'nava-free-chat-v1';
  const PREF_KEY = 'nava-free-chat-preferences-v1';
  const MODES = {
    chat: { title: 'NavaBharat Chat', short: 'AI Chat', icon: 'chat', intro: 'A little curiosity. A world of possibilities.', te: 'మీ భాషలో అడగండి. కలిసి తెలుసుకుందాం.', description: 'Ideas, explanations and everyday help — in your language.', prompts: ['Help me write a clear message', 'Explain a topic simply', 'Give me ideas for my small business'] },
    student: { title: 'Student Chat', short: 'Students', icon: 'book', intro: 'Every question is a good place to start.', te: 'అడగండి. అర్థం చేసుకోండి. సాధన చేయండి.', description: 'Understand a concept, work through a problem, or practise for an exam.', prompts: ['Explain 15% of 200 step by step', 'Help me make an SSC CGL study plan', 'Give me one physics practice question'] },
    astro: { title: 'Astro Chat', short: 'Astrology', icon: 'sun', intro: 'Explore astrology, one conversation at a time.', te: 'జ్యోతిష్యాన్ని సులభంగా తెలుసుకుందాం.', description: 'Traditional interpretations, thoughtful explanations, and room for uncertainty.', prompts: ['వృషభ రాశి గురించి సులభంగా చెప్పండి', 'What if I do not know my birth time?', 'Explain rashi and nakshatra'] }
  };
  const LANGUAGES = ['Auto', 'Telugu', 'English', 'Hindi', 'Tamil', 'Kannada', 'Malayalam', 'Marathi', 'Bengali', 'Gujarati', 'Punjabi', 'Odia', 'Urdu', 'Assamese', 'Nepali', 'Sanskrit', 'Arabic', 'Spanish', 'French', 'German', 'Portuguese', 'Japanese', 'Korean', 'Chinese', 'Other'];
  const TOPICS = ['All subjects', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'Languages', 'Coding', 'SSC CGL', 'SSC', 'Railways', 'AP Groups', 'Telangana Groups'];
  const PATHS = {chat:'chat', student:'solve', astro:'astro'};
  const strokes = {
    chat:'M21 11.5a8.4 8.4 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.4 8.4 0 0 1 3.8-.9h.5a8.5 8.5 0 0 1 8 8v.5Z',
    book:'M12 7v14m0-14C9 4 5 4 2 5v15c3-1 7-1 10 1 3-2 7-2 10-1V5c-3-1-7-1-10 2Z',
    sun:'M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5M16 12a4 4 0 1 1-8 0 4 4 0 0 1 8 0',
    plus:'M12 5v14M5 12h14', send:'m22 2-7 20-4-9L2 9l20-7ZM22 2 11 13',
    list:'M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01',
    notes:'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6ZM14 2v6h6M8 13h8M8 17h6',
    map:'M12 3v5M5 16v-4h14v4M12 8v8M3 17h4v4H3zM10 17h4v4h-4zM17 17h4v4h-4zM10 1h4v4h-4z',
    download:'M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5',
    share:'M8 12l8-5M8 12l8 5M8 12a2 2 0 1 1-4 0 2 2 0 0 1 4 0ZM20 5a2 2 0 1 1-4 0 2 2 0 0 1 4 0ZM20 19a2 2 0 1 1-4 0 2 2 0 0 1 4 0',
    copy:'M9 9h12v12H9zM15 5V3H3v12h2',trash:'M3 6h18M9 6V3h6v3M5 6l1 15h12l1-15M10 10v7m4-7v7',close:'m6 6 12 12M6 18 18 6',stop:'M5 5h14v14H5z',globe:'M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0ZM3 12h18M12 3c5 5 5 13 0 18-5-5-5-13 0-18'
  };
  const icon = name => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${name==='spark'?'<path d="m12 2 3 7 7 3-7 3-3 7-3-7-7-3 7-3Z"/>':`<path d="${strokes[name]||strokes.chat}"/>`}</svg>`;
  const safe = v => String(v ?? '').replace(/[&<>"']/g, x => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));
  const uid = () => crypto.randomUUID();
  let prefs = {save:false,language:'Telugu',other:''}, threads = [], selected = {}, mode = 'chat', view = 'chat', historyOpen = false;
  let pending = null, error = '', query = '', mounted = false;
  try { const p = JSON.parse(localStorage.getItem(PREF_KEY)||'{}'); prefs={save:p.save===true,language:LANGUAGES.includes(p.language)?p.language:'Telugu',other:typeof p.other==='string'?p.other.slice(0,40):''}; } catch {}
  if(prefs.save) try {
    const rows=JSON.parse(localStorage.getItem(HISTORY_KEY)||'[]');
    if(Array.isArray(rows)) threads=rows.slice(0,10).filter(t=>t&&MODES[t.mode]&&Array.isArray(t.messages)).map(t=>({
      id:uid(),mode:t.mode,title:String(t.title||'Conversation').slice(0,60),created:Number(t.created)||Date.now(),draft:'',profile:{},topic:TOPICS.includes(t.topic)?t.topic:'All subjects',style:['Explain','Hints first','Practice'].includes(t.style)?t.style:'Explain',
      messages:t.messages.slice(-30).filter(m=>m&&['user','assistant'].includes(m.role)&&typeof m.content==='string').map(m=>({role:m.role,content:m.content.slice(0,12000),at:Number(m.at)||Date.now()}))
    }));
  } catch {}
  function save() {
    try {
      localStorage.setItem(PREF_KEY,JSON.stringify(prefs));
      if(!prefs.save){localStorage.removeItem(HISTORY_KEY);return;}
      const data=JSON.stringify(threads.filter(t=>t.messages.length).slice(0,10).map(({id,mode,title,created,messages,topic,style})=>({id,mode,title,created,messages:messages.slice(-30),topic,style})));
      if(data.length>1000000) throw Error('History is full');
      localStorage.setItem(HISTORY_KEY,data);
    } catch { window.toast?.('Could not save on this device. You can still chat and download your notes.'); }
  }
  function active() {
    let t=threads.find(t=>t.id===selected[mode]);
    if(!t){t=threads.find(t=>t.mode===mode);if(!t){t={id:uid(),mode,title:'New conversation',created:Date.now(),messages:[],draft:'',profile:{},topic:'All subjects',style:'Explain'};threads.unshift(t);}selected[mode]=t.id;}
    return t;
  }
  const lastAnswer = () => [...active().messages].reverse().find(m=>m.role==='assistant')?.content||'';
  const rich = text => typeof window.navaRich==='function'?window.navaRich(text):`<p>${safe(text).replace(/\n/g,'<br>')}</p>`;
  function languageOptions(){return LANGUAGES.map(l=>`<option value="${l}" ${prefs.language===l?'selected':''}>${l==='Auto'?'Auto · match my message':l==='Telugu'?'తెలుగు · Telugu':l==='Other'?'Other language…':l}</option>`).join('');}
  function sidebar(){return `<aside class="nc-history ${historyOpen?'is-open':''}" aria-label="Your conversations"><div class="nc-history-heading"><span>Conversations</span><button class="nc-icon nc-mobile" data-action="history" aria-label="Close conversations">${icon('close')}</button></div><button class="nc-new" data-action="new">${icon('plus')} New conversation</button><label class="nc-search"><span class="nc-sr">Search conversations</span><input id="nc-search" placeholder="Search your chats" value="${safe(query)}"></label><div class="nc-history-list">${historyList()}</div><div class="nc-device"><label><input id="nc-save" type="checkbox" ${prefs.save?'checked':''}> Save chats on this device</label><p>${prefs.save?'Saved locally. Other people using this browser may see them.':'Off by default. Chats disappear when you reload.'}</p><button data-action="clear" class="nc-text-button">${icon('trash')} Clear all chats</button></div></aside>`;}
  function historyList(){return threads.filter(t=>t.mode===mode&&t.title.toLowerCase().includes(query.toLowerCase())).map(t=>`<button class="nc-thread ${t.id===active().id?'is-active':''}" data-thread="${t.id}" aria-pressed="${t.id===active().id}"><span class="nc-thread-icon">${icon(MODES[t.mode].icon)}</span><span><strong>${safe(t.title)}</strong><small>${t.messages.length?'Private conversation':'Start something new'}</small></span></button>`).join('')||'<p class="nc-empty-history">No matching conversations.</p>';}
  function page(nextMode){if(nextMode!==mode){error='';query='';view='chat';historyOpen=false;}mode=MODES[nextMode]?nextMode:'chat';mounted=false;const t=active(),m=MODES[mode];return `<section id="nc-root" class="nc-root nc-${mode}" aria-label="${m.title}">${sidebar()}<div class="nc-main"><div class="nc-top"><button class="nc-icon nc-mobile" data-action="history" aria-label="Open conversations">${icon('list')}</button><span class="nc-avatar">${icon(m.icon)}</span><div class="nc-title"><h1>${m.title}</h1><span>Free for everyone · No Pro plan</span></div><span class="nc-free">FREE</span></div><div class="nc-modebar" aria-label="Chat mode">${Object.entries(MODES).map(([k,v])=>`<button data-mode="${k}" class="${k===mode?'is-active':''}" aria-pressed="${k===mode}">${icon(v.icon)} ${v.short}</button>`).join('')}<label class="nc-language"><span class="nc-sr">Answer language</span>${icon('globe')}<select id="nc-language">${languageOptions()}</select></label></div><div class="nc-other-language" ${prefs.language==='Other'?'':'hidden'}><label>Answer language <input id="nc-other" maxlength="40" value="${safe(prefs.other)}" placeholder="For example: Italian"></label></div>${mode==='student'?`<div class="nc-context"><label>Subject or exam<select id="nc-topic">${TOPICS.map(x=>`<option ${t.topic===x?'selected':''}>${x}</option>`).join('')}</select></label><label>Learning style<select id="nc-style">${['Explain','Hints first','Practice'].map(x=>`<option ${t.style===x?'selected':''}>${x}</option>`).join('')}</select></label><span>Practice help · Check official exam notices</span></div>`:''}${mode==='astro'?birthDetails(t):''}<div class="nc-viewbar"><div role="group" aria-label="Answer view">${[['chat','chat','Chat'],['notes','notes','Notes'],['map','map','Mind map']].map(([v,i,label])=>`<button data-view="${v}" class="${view===v?'is-active':''}" aria-pressed="${view===v}">${icon(i)} ${label}</button>`).join('')}</div><button class="nc-icon" data-action="new" aria-label="New conversation">${icon('plus')}</button></div><div id="nc-messages" class="nc-messages" tabindex="0" aria-label="Conversation">${conversation()}</div><div id="nc-error" class="nc-error" role="alert" ${error?'':'hidden'}>${safe(error)}${error?'<button data-action="retry">Try again</button>':''}</div><form id="nc-form" class="nc-composer"><label for="nc-input" class="nc-sr">Your message</label><textarea id="nc-input" rows="2" maxlength="6000" placeholder="మీ ప్రశ్న అడగండి… Ask in any language">${safe(t.draft||'')}</textarea><button type="${pending?'button':'submit'}" class="nc-send" ${pending?'data-action="stop"':''} aria-label="${pending?'Stop waiting':'Send message'}">${icon(pending?'stop':'send')}</button></form><div class="nc-footnote"><span>${mode==='astro'?'Traditional interpretations, not certain predictions.':'AI can make mistakes. Check important answers.'}</span><button class="nc-text-button" data-action="privacy">Privacy</button></div><div id="nc-status" class="nc-sr" aria-live="polite" role="status"></div></div><dialog id="nc-dialog" class="nc-dialog"></dialog></section>`;}
  function birthDetails(t){return `<details class="nc-birth"><summary>${icon('sun')} Birth details <span>Optional · Time unknown is OK</span></summary><p>These details go to the AI provider when you send a message. Add only what you want to share. No calculated birth chart is provided.</p><div class="nc-birth-grid"><label>Date<input id="nc-birth-date" type="date" value="${safe(t.profile.date||'')}" max="${new Date().toISOString().slice(0,10)}"></label><label>Birthplace<input id="nc-birth-place" maxlength="120" placeholder="City or town" value="${safe(t.profile.place||'')}"></label><label>Time, if known<input id="nc-birth-time" type="time" value="${safe(t.profile.time||'')}"></label><label>Rashi, if known<input id="nc-birth-rashi" maxlength="60" placeholder="For example: Vrushabha" value="${safe(t.profile.rashi||'')}"></label></div><button data-action="clear-birth" class="nc-text-button">Clear birth details</button></details>`;}
  function welcome(){const m=MODES[mode];return `<div class="nc-welcome"><span class="nc-welcome-symbol">${icon(m.icon)}</span><span class="nc-eyebrow">NAVABHARAT AI · RACHARLAGPT</span><h2>${m.intro}</h2><p class="nc-telugu" lang="te">${m.te}</p><p>${m.description}</p><div class="nc-prompts">${m.prompts.map((p,i)=>`<button data-prompt="${i}">${safe(p)}<span aria-hidden="true">↗</span></button>`).join('')}</div><span class="nc-availability">No login needed · Subject to service availability</span></div>`;}
  function conversation(){const t=active();if(view!=='chat')return visual();return (!t.messages.length?welcome():t.messages.map((m,i)=>`<article class="nc-message nc-${m.role}"><div class="nc-message-label">${m.role==='assistant'?icon('spark')+' NavaBharat AI':'You'}</div><div class="nc-bubble">${m.role==='assistant'?rich(m.content):`<p>${safe(m.content).replace(/\n/g,'<br>')}</p>`}<time>${new Date(m.at).toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})}</time></div>${m.role==='assistant'?`<div class="nc-answer-actions"><button data-copy="${i}">${icon('copy')} Copy</button><button data-answer="${i}" data-action="answer-share">${icon('share')} Share</button><button data-view="notes">${icon('notes')} Notes</button></div>`:''}</article>`).join(''))+(pending?.thread===t.id?'<div class="nc-thinking" role="status"><span></span><span></span><span></span> Preparing your answer…</div>':'');}
  function sections(text){const parts=text.split(/\n(?=#{1,4}\s)/).filter(x=>x.trim());if(parts.length>1)return parts.slice(0,12).map(x=>{const [h,...b]=x.split('\n');return {title:h.replace(/^#+\s*/,''),text:b.join('\n')||h};});return text.split(/\n\s*\n/).filter(Boolean).slice(0,12).map((x,i)=>({title:`Key point ${i+1}`,text:x}));}
  function visual(){const answer=lastAnswer();if(!answer)return '<div class="nc-visual-empty">'+icon('notes')+'<h2>Your ideas, beautifully organised.</h2><p>Ask a question first. Then view its answer as notes or a mind map.</p></div>';return `<div class="nc-visual"><div class="nc-visual-top"><div><span class="nc-eyebrow">FROM YOUR LATEST ANSWER</span><h2>${view==='map'?'Your answer at a glance':'A little clarity, on every note.'}</h2></div><div class="nc-export-actions"><button data-action="print">${icon('download')} Print / PDF</button><button data-action="download">${icon('notes')} Save text</button><button data-action="image">${icon('download')} Save image</button><button data-action="share">${icon('share')} Share</button></div></div>${view==='map'?`<div class="nc-map-root">${safe(active().title)}</div>`:''}<div class="nc-note-grid ${view==='map'?'nc-map-grid':''}">${sections(answer).map((s,i)=>`<article class="nc-note nc-note-${i%4}"><span class="nc-note-number">${String(i+1).padStart(2,'0')}</span><h3>${safe(s.title)}</h3>${rich(s.text)}</article>`).join('')}</div><p class="nc-outline-caption">${view==='map'?'Visual outline of the answer’s sections.':'Notes arranged from the answer.'} Up to 12 sections shown. Save text or Print / PDF includes the full answer.</p></div>`;}
  function redraw(focus=false){if(!document.querySelector('#nc-root'))return;const app=document.querySelector('#app .content');if(!app)return;app.innerHTML=page(mode);afterRender(PATHS[mode]);if(focus)document.querySelector('#nc-input')?.focus();}
  function refreshMessages(){if(!document.querySelector('#nc-root'))return;const el=document.querySelector('#nc-messages');el.innerHTML=conversation();if(view==='chat')el.scrollTop=el.scrollHeight;}
  function persistDraft(){const el=document.querySelector('#nc-input');if(el)active().draft=el.value;}
  function afterRender(p){mounted=['chat','solve','astro'].includes(p);if(!mounted)return;const root=document.querySelector('#nc-root');if(!root)return;
    root.addEventListener('click',onClick);root.querySelector('#nc-form').addEventListener('submit',e=>{e.preventDefault();send();});
    const input=root.querySelector('#nc-input');input.addEventListener('input',()=>{active().draft=input.value;});input.addEventListener('keydown',e=>{if(e.key==='Enter'&&(e.ctrlKey||e.metaKey)&&!e.isComposing){e.preventDefault();send();}});
    root.querySelector('#nc-search').addEventListener('input',e=>{query=e.target.value;root.querySelector('.nc-history-list').innerHTML=historyList();});
    root.querySelector('#nc-save').addEventListener('change',e=>{prefs.save=e.target.checked;save();persistDraft();redraw();});
    root.querySelector('#nc-language').addEventListener('change',e=>{prefs.language=e.target.value;save();persistDraft();redraw();});
    root.querySelector('#nc-other')?.addEventListener('input',e=>{prefs.other=e.target.value;save();});
    root.querySelector('#nc-topic')?.addEventListener('change',e=>{active().topic=e.target.value;save();});
    root.querySelector('#nc-style')?.addEventListener('change',e=>{active().style=e.target.value;save();});
    for(const field of ['date','place','time','rashi'])root.querySelector('#nc-birth-'+field)?.addEventListener('input',e=>{active().profile[field]=e.target.value;});
    root.querySelector('#nc-dialog').addEventListener('click',e=>{if(e.target.closest('[data-dialog-close]'))root.querySelector('#nc-dialog').close();});
    if(view==='chat'){const el=root.querySelector('#nc-messages');el.scrollTop=el.scrollHeight;}
  }
  async function onClick(e){const b=e.target.closest('button');if(!b)return;
    if(b.dataset.mode){persistDraft();view='chat';error='';historyOpen=false;query='';window.go(PATHS[b.dataset.mode]);return;}
    if(b.dataset.view){persistDraft();view=b.dataset.view;redraw();return;}
    if(b.dataset.thread){persistDraft();selected[mode]=b.dataset.thread;error='';historyOpen=false;redraw();return;}
    if(b.dataset.prompt!==undefined){active().draft=MODES[mode].prompts[Number(b.dataset.prompt)];redraw(true);return;}
    if(b.dataset.copy!==undefined){try{await navigator.clipboard.writeText(active().messages[Number(b.dataset.copy)].content);window.toast?.('Answer copied');}catch{dialog('Copy your answer',`<textarea readonly rows="10">${safe(active().messages[Number(b.dataset.copy)].content)}</textarea>`);}return;}
    switch(b.dataset.action){
      case 'history': persistDraft();historyOpen=!historyOpen;redraw();break;
      case 'new': persistDraft();selected[mode]='';threads.unshift({id:uid(),mode,title:'New conversation',created:Date.now(),messages:[],draft:'',profile:{},topic:'All subjects',style:'Explain'});threads=threads.slice(0,10);selected[mode]=threads[0].id;historyOpen=false;error='';view='chat';save();redraw(true);break;
      case 'clear':if(confirm('Delete all chat history from this device? This cannot be undone.')){pending?.controller.abort();threads=[];selected={};error='';save();redraw();}break;
      case 'clear-birth':active().profile={};persistDraft();redraw();break;
      case 'stop':pending?.controller.abort();break;
      case 'retry':send(true);break;
      case 'privacy':dialog('Your conversations, your choice','<p>No login or payment is required for chat. Messages and optional birth details are sent to the configured AI provider to generate a reply. Its privacy terms apply.</p><p>History is kept only in this tab unless you enable “Save chats on this device”. Local history is not encrypted and does not sync across devices. Birth form fields are not saved separately. Details you put in messages remain part of the conversation.</p><p>You control copying and sharing. Share links do not publish your private conversation.</p>');break;
      case 'print':printAnswer();break;
      case 'download':download(new Blob([lastAnswer()],{type:'text/plain;charset=utf-8'}),'navabharat-notes.txt');break;
      case 'image':downloadImage();break;
      case 'share':showShare(lastAnswer());break;
      case 'answer-share':showShare(active().messages[Number(b.dataset.answer)].content);break;
    }
  }
  async function send(retry=false){
    if(pending)return window.toast?.('Please wait for the current reply, or stop it first.');
    const t=active();persistDraft();const input=retry?[...t.messages].reverse().find(m=>m.role==='user')?.content:(t.draft||'').trim();
    if(!input)return;const lang=prefs.language==='Other'?prefs.other.trim():prefs.language;
    if(!lang){window.toast?.('Enter the language you want for the answer.');return;}
    const history=(retry?t.messages.slice(0,-1):t.messages).slice(-12).map(({role,content})=>({role,content:content.slice(0,4000)}));
    if(!retry){t.messages.push({role:'user',content:input,at:Date.now()});t.messages=t.messages.slice(-30);t.draft='';if(t.title==='New conversation')t.title=input.slice(0,52);}
    const request={thread:t.id,controller:new AbortController()};pending=request;error='';view='chat';historyOpen=false;save();redraw();
    const timeout=setTimeout(()=>request.controller.abort('timeout'),65000);
    try{
      const c=window.NAVA_CONFIG||{};if(!c.SUPABASE_URL||!c.SUPABASE_ANON_KEY)throw Error('AI service is not configured yet.');
      const res=await fetch(c.SUPABASE_URL+'/functions/v1/ai-text',{method:'POST',headers:{'Content-Type':'application/json',apikey:c.SUPABASE_ANON_KEY,Authorization:'Bearer '+c.SUPABASE_ANON_KEY},signal:request.controller.signal,body:JSON.stringify({type:t.mode==='student'?'student_chat':t.mode==='astro'?'astro_chat':'chat',input,language:lang,history,topic:t.topic,learning_style:t.style,birth:t.mode==='astro'?t.profile:undefined})});
      let data={};try{data=await res.json();}catch{}
      if(!res.ok)throw Error(data.error||(res.status===429?'The free service is busy. Please try again shortly.':'The AI service could not reply. Please try again.'));
      if(typeof data.text!=='string'||!data.text.trim())throw Error('The service returned an empty answer. Please try again.');
      if(request.controller.signal.aborted)return;
      t.messages.push({role:'assistant',content:data.text.slice(0,12000),at:Date.now()});t.messages=t.messages.slice(-30);save();
      if(mounted&&active().id===t.id){const status=document.querySelector('#nc-status');if(status)status.textContent='Answer ready.';}
    }catch(e){if(mounted&&active().id===t.id)error=request.controller.signal.aborted?(request.controller.signal.reason==='timeout'?'The service is taking too long. Please try again later.':'Stopped waiting. You can retry your question.'):(e.message||'Connection problem. Please try again.');}
    finally{clearTimeout(timeout);if(pending===request)pending=null;if(mounted)redraw();}
  }
  function dialog(title,body){const d=document.querySelector('#nc-dialog');d.innerHTML=`<div class="nc-dialog-top"><h2>${safe(title)}</h2><button class="nc-icon" data-dialog-close aria-label="Close dialog">${icon('close')}</button></div>${body}`;d.showModal();}
  function showShare(text){const c=window.NAVA_CONFIG||{};let url=location.origin+'/?page='+PATHS[mode];try{const u=new URL(c.SITE_URL);if(u.protocol==='https:')url=u.origin+'/?page='+PATHS[mode];}catch{}
    dialog('Preview before sharing',`<p>Choose only the text you want to share. Remove personal or birth details first.</p><textarea id="nc-share-text" rows="7">${safe(text)}</textarea><div class="nc-share-actions"><button id="nc-native-share">Share…</button><button id="nc-wa-share">WhatsApp</button><button id="nc-x-share">X</button><button id="nc-copy-share">Copy text</button><button id="nc-linkedin-share">LinkedIn · app link</button></div><p class="nc-small">Your private chat is not published. LinkedIn shares the app link; copy your selected text to add it to your post.</p>`);
    const selectedText=()=>document.querySelector('#nc-share-text').value;
    document.querySelector('#nc-native-share').onclick=async()=>{try{if(navigator.share)await navigator.share({title:'NavaBharat AI',text:selectedText(),url});else{await navigator.clipboard.writeText(selectedText()+'\n'+url);window.toast?.('Copied for sharing');}}catch(e){if(e.name!=='AbortError')window.toast?.('Use Copy text or download your notes.');}};
    document.querySelector('#nc-copy-share').onclick=async()=>{try{await navigator.clipboard.writeText(selectedText()+'\n'+url);window.toast?.('Copied');}catch{window.toast?.('Select and copy the text above.');}};
    document.querySelector('#nc-wa-share').onclick=()=>window.open('https://wa.me/?text='+encodeURIComponent(selectedText().slice(0,5000)+'\n'+url),'_blank','noopener,noreferrer');
    document.querySelector('#nc-x-share').onclick=()=>window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(selectedText().slice(0,220))+'&url='+encodeURIComponent(url),'_blank','noopener,noreferrer');
    document.querySelector('#nc-linkedin-share').onclick=()=>window.open('https://www.linkedin.com/sharing/share-offsite/?url='+encodeURIComponent(url),'_blank','noopener,noreferrer');
  }
  function download(blob,name){const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),10000);}
  function printAnswer(){const text=lastAnswer();if(!text)return;document.querySelector('#nc-print')?.remove();const el=document.createElement('section');el.id='nc-print';el.innerHTML=`<h1>NavaBharat AI</h1><h2>${safe(active().title)}</h2>${rich(text)}<p>AI-generated answer · Review before relying on it.</p>`;document.body.appendChild(el);document.body.classList.add('nc-printing');const cleanup=()=>{document.body.classList.remove('nc-printing');el.remove();};window.addEventListener('afterprint',cleanup,{once:true});window.print();}
  async function downloadImage(){const answer=lastAnswer();if(!answer)return;try{await document.fonts?.ready;const canvas=document.createElement('canvas');canvas.width=1200;const ctx=canvas.getContext('2d');if(!ctx)throw Error('Canvas unavailable');ctx.font='28px system-ui, sans-serif';const lines=[];for(const paragraph of answer.slice(0,1800).replace(/[#*`]/g,'').split('\n')){let line='';for(const word of paragraph.split(/\s+/)){if(ctx.measureText(line+' '+word).width>1030&&line){lines.push(line);line=word;}else line+=(line?' ':'')+word;}lines.push(line);}canvas.height=280+Math.min(lines.length,45)*44;ctx.fillStyle='#f5f7f6';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.fillStyle='#0f766e';ctx.fillRect(0,0,1200,100);ctx.fillStyle='#ffffff';ctx.font='bold 32px system-ui, sans-serif';ctx.fillText('NavaBharat AI · '+MODES[mode].title,65,64);ctx.fillStyle='#172b28';ctx.font='28px system-ui, sans-serif';lines.slice(0,45).forEach((line,i)=>ctx.fillText(line,65,170+i*44,1060));ctx.fillStyle='#526761';ctx.font='22px system-ui, sans-serif';ctx.fillText('Answer excerpt · Full answer available in your notes',65,canvas.height-70);canvas.toBlob(blob=>{if(blob)download(blob,'navabharat-answer.png');else window.toast?.('Image export unavailable. Use Print / PDF.');},'image/png');}catch{window.toast?.('Image export unavailable. Use Print / PDF.');}}
  window.NavaChat={page,afterRender,leave(){mounted=false;},icon};
})();

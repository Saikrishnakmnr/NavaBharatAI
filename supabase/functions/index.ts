// NavaBharat AI — self-contained linked-news aggregator (no Gemini, no Storage, no SQL).
// Supabase Dashboard: existing `live-rss` function, verify_jwt=false.
const cors: Record<string, string> = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type, x-admin-token',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};
const json = (value: unknown, status = 200) => new Response(JSON.stringify(value), {
  status, headers: { ...cors, 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
});
const LANGS: Record<string, [string, string, string]> = {
  English: ['en-IN', 'IN', 'en'], Telugu: ['te-IN', 'IN', 'te'],
  Hindi: ['hi-IN', 'IN', 'hi'], Tamil: ['ta-IN', 'IN', 'ta'],
  Kannada: ['kn-IN', 'IN', 'kn'], Malayalam: ['ml-IN', 'IN', 'ml'],
};
type News = { title: string; link: string; pubDate: string; source: string };
const escapeHtml = (x: string) => x.replace(/<[^>]*>/g, '').trim();
function decodeXml(s: string) {
  return escapeHtml(s.replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1')
    .replace(/&#(\d+);/g, (_m,n) => String.fromCodePoint(Math.min(0x10ffff, Number(n))))
    .replace(/&#x([0-9a-f]+);/gi, (_m,n) => String.fromCodePoint(Math.min(0x10ffff, parseInt(n,16))))
    .replace(/&amp;/gi, '&').replace(/&quot;/gi, '"').replace(/&apos;/gi, "'")
    .replace(/&lt;/gi, '<').replace(/&gt;/gi, '>'));
}
function cleanLink(v: string) {
  try { const u = new URL(decodeXml(v)); return (u.protocol === 'https:' || u.protocol === 'http:') ? u.href : ''; }
  catch { return ''; }
}
function extractRSS(xml: string): News[] {
  const items: News[] = [];
  for (const m of xml.matchAll(/<item(?:\s[^>]*)?>([\s\S]*?)<\/item>/gi)) {
    const b = m[1];
    const tag = (t: string) => b.match(new RegExp(`<${t}(?:\\s[^>]*)?>([\\s\\S]*?)<\\/${t}>`, 'i'))?.[1] || '';
    const title = decodeXml(tag('title'));
    const link = cleanLink(tag('link'));
    if (!title || !link) continue;
    items.push({ title: title.slice(0, 300), link, pubDate: decodeXml(tag('pubDate')),
      source: decodeXml(tag('source')) || new URL(link).hostname });
  }
  return items;
}
async function rss(url: string): Promise<News[]> {
  const r = await fetch(url, { headers: { 'Accept': 'application/rss+xml, application/xml, text/xml, */*' }, signal: AbortSignal.timeout(6500) });
  if (!r.ok) return [];
  const raw = await r.text();
  if (!raw.includes('<rss') && !raw.includes('<item')) return [];
  return extractRSS(raw.slice(0, 1200000));
}
async function gdelt(q: string, limit: number): Promise<News[]> {
  const u = 'https://api.gdeltproject.org/api/v2/doc/doc?query=' + encodeURIComponent(q) +
    '&mode=artlist&format=json&maxrecords=' + limit + '&timespan=7d&sort=datedesc';
  const r = await fetch(u, { signal: AbortSignal.timeout(6500) });
  if (!r.ok) return [];
  const data = await r.json();
  return (Array.isArray(data.articles) ? data.articles : []).map((a: any) => {
    const link = cleanLink(String(a.url || a.documentidentifier || ''));
    return { title: String(a.title || '').slice(0,300), link,
      pubDate: String(a.seendate || a.date || ''), source: String(a.domain || 'GDELT') };
  }).filter((a: News) => Boolean(a.title && a.link));
}
const jobWords = /\b(job|jobs|recruitment|recruit|vacanc(?:y|ies)|opening|posts?|notification|apply online|application|exams?|hiring|ssc|upsc|ibps|rrb|railway|ps[csc]|constable|teacher|bank po|apprentice|rojgar|sarkari|employment|group [1-4abcd]|admit card)\b/i;
const nonTopic = new Set(['a','an','the','and','or','for','in','on','of','to','india','indian','news','latest','today','current','affairs','government','official','results','search','all','with','about','update','updates']);
function topicTokens(q: string) { return q.toLocaleLowerCase().split(/[^\p{L}\p{N}]+/u).filter(w => w.length > 2 && !nonTopic.has(w)).slice(0,7); }
function relevant(item: News, kind: string, q: string, category: string) {
  const t = item.title.toLowerCase();
  if (kind === 'jobs') {
    if (!jobWords.test(t)) return false;
    const bank = /bank|ibps|sbi|rbi|nabard|finance|po\b|clerk/i;
    const rail = /ssc|rrb|railway|rail road|ntpc|group d|cgl|chsl/i;
    const civil = /upsc|civil services|ias|ips|ifs|prelims/i;
    const state = /psc|public service commission|tspsc|tgpsc|appsc|bpsc|mpsc|opsc|kpsc|group [1-4]/i;
    if (/banking|finance/i.test(category)) return bank.test(t);
    if (/ssc|railway/i.test(category)) return rail.test(t);
    if (/upsc|civil/i.test(category)) return civil.test(t);
    if (/state public/i.test(category)) return state.test(t);
    return true;
  }
  if (kind === 'current_affairs') {
    if (category === 'All' || category === 'India' || !category) return true;
    const groups: Record<string, RegExp> = {
      World: /world|international|global|united nations|america|china|europe|asia|war|diplomac/i,
      Business: /business|econom|market|stock|finance|trade|bank|rupee|inflation/i,
      Technology: /technology|tech|artificial intelligence|\bai\b|software|startup|chip|digital|cyber/i,
      Science: /science|space|research|scientist|biology|physics|climate|isro|nasa/i,
      Sports: /sport|cricket|football|tennis|olympic|match|tournament|hockey/i,
      Education: /education|school|university|exam|student|college|scholarship|neet|jee/i,
    };
    return groups[category]?.test(t) || false;
  }
  // Search mode: searching 'milk' must never return unrelated politics news.
  if (kind === 'search') {
    const tokens = topicTokens(q);
    return !tokens.length || tokens.some(token => t.includes(token));
  }
  // Generic news may show a broad India feed. A specific topic still needs a match.
  const tokens = topicTokens(q);
  return !tokens.length || tokens.some(token => t.includes(token));
}
function searchQuery(q: string, kind: string, category: string) {
  if (kind === 'jobs') {
    const topic: Record<string,string> = {
      'Banking & Finance': 'IBPS SBI RBI bank recruitment jobs vacancy',
      'SSC & Railways': 'SSC RRB railway recruitment notification vacancy',
      'UPSC & Civil Services': 'UPSC civil services recruitment examination notification',
      'State Public Service Commissions': 'state PSC APPSC TGPSC recruitment jobs notification',
    };
    return (topic[category] || 'India government jobs recruitment vacancy notification') + ' when:30d';
  }
  if (kind === 'current_affairs') return (category === 'All' || category === 'India' ? 'India latest news' : `India ${category} latest news`) + ' when:7d';
  const value = q.trim() || 'India news';
  return value.length > 250 ? value.slice(0,250) : value;
}
function latest(items: News[], max: number) {
  const seen = new Set<string>();
  return items.filter(x => {
    const key = x.title.toLowerCase().replace(/\s+/g,' ').slice(0,120);
    if (seen.has(key)) return false; seen.add(key); return true;
  }).slice(0,max);
}

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  if (req.method !== 'POST') return json({ error: 'Method not allowed' }, 405);
  try {
    const x = await req.json();
    const language = LANGS[String(x.language)] ? String(x.language) : 'English';
    const category = String(x.category || 'All');
    const kind = ['jobs','current_affairs','search','news'].includes(String(x.kind)) ? String(x.kind) : 'news';
    const q = String(x.query || 'India news').trim().slice(0,250) || 'India news';
    const limit = Math.min(20, Math.max(1, Number(x.limit) || 12));
    const terms = searchQuery(q, kind, category);
    const [hl,gl,ceid] = LANGS[language];
    const google = 'https://news.google.com/rss/search?q=' + encodeURIComponent(terms) +
      '&hl=' + encodeURIComponent(hl) + '&gl=' + gl + '&ceid=' + gl + ':' + ceid;
    const bing = 'https://www.bing.com/news/search?q=' + encodeURIComponent(terms.replace(/\s+when:\d+d/g,'')) + '&format=rss';
    const gd = terms.replace(/\s+when:\d+d/g,'');
    // Independent live sources, concurrently; no Gemini request, fabricated headline or storage upload.
    const sources = await Promise.allSettled([rss(google), rss(bing), gdelt(gd,Math.min(50,limit*3))]);
    const names = ['Google News','Bing News','GDELT'];
    const groups = sources.map((r,i) => ({ provider:names[i], items:r.status==='fulfilled' ? r.value : [] }));
    let all: News[] = [];
    for (const group of groups) {
      const filtered = group.items.filter(item => relevant(item,kind,q,category));
      if (filtered.length) all.push(...filtered.map(item => ({ ...item, source:item.source || group.provider })));
    }
    all = latest(all,limit);
    return json({ items: all, provider: groups.filter(g=>g.items.length).map(g=>g.provider).join(', ') || 'No available feed',
      fetched_at: new Date().toISOString(), query: terms, kind, matched: all.length,
      message: all.length ? undefined : 'No matching linked articles were available. Use the official/source search links.' });
  } catch (error) {
    console.warn('live-rss error', String((error as Error)?.name || 'RequestError'));
    // A successful JSON fallback keeps the frontend useful; no invented stories.
    return json({ items: [], provider:'Unavailable', message:'Live sources are temporarily unavailable.' });
  }
});

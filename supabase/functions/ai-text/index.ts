// Restored from NavaBharatAI Premium No-Streamlit FULL-AUDITED v13 ai-text/_shared.ts logic.
// Self-contained for Supabase Dashboard's individual Edge Function editor.
const cors: Record<string,string> = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type, x-admin-token',
  'Access-Control-Allow-Methods': 'POST, OPTIONS'
};
const json = (value: unknown, status = 200) => new Response(JSON.stringify(value), {
  status, headers: { ...cors, 'Content-Type': 'application/json' }
});
const secret = (name: string) => Deno.env.get(name) || '';
const keys = () => ['GEMINI_API_KEY','GEMINI_API_KEY_2','GEMINI_API_KEY_3','GEMINI_AI_KEY_1','GEMINI_AI_KEY_2','GEMINI_AI_KEY_3'].map(secret).filter(Boolean);

// V13 model list and request shape; no invented model-name updates here.
async function geminiText(prompt: string, grounded = false): Promise<string> {
  let last = '';
  const models = [secret('GEMINI_MODEL') || 'gemini-3.8-flash','gemini-3.8-flash','gemini-3.7-flash','gemini-3.6-flash','gemini-3.5-flash'].filter((v, i, a) => v && a.indexOf(v) === i);
  for (const key of keys()) {
    for (const model of models) {
      for (const bearer of [false, true]) {
        try {
          const url = grounded
            ? 'https://generativelanguage.googleapis.com/v1beta/interactions'
            : `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(model)}:generateContent`;
          const payload = grounded
            ? { model, input: prompt, tools: [{ type: 'google_search' }] }
            : { contents: [{ parts: [{ text: prompt }] }], generationConfig: { temperature: 0.4 } };
          const headers: Record<string,string> = { 'Content-Type': 'application/json' };
          if (bearer) headers.Authorization = `Bearer ${key}`;
          else headers['x-goog-api-key'] = key;
          const response = await fetch(url, { method: 'POST', headers, body: JSON.stringify(payload) });
          const raw = await response.text();
          if (!response.ok) {
            last = raw.slice(0, 500);
            if ((response.status === 401 || response.status === 403) && bearer) break;
            continue;
          }
          const result = JSON.parse(raw);
          const answer = grounded
            ? (result.output_text || result.outputText || result.steps?.flatMap((s: any) => s.content || []).filter((c: any) => c.type === 'text').map((c: any) => c.text || '').join(''))
            : (result.candidates?.[0]?.content?.parts || []).map((part: any) => part.text || '').join('');
          if (answer) return answer;
          last = 'Empty Gemini response';
          break;
        } catch (error) { last = String(error); }
      }
    }
  }
  throw new Error('Gemini unavailable: ' + last);
}

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  if (req.method !== 'POST') return json({ error: 'Method not allowed' }, 405);
  try {
    const body = await req.json();
    const type = String(body.type || 'solve');
    const input = String(body.input || '').trim();
    const language = String(body.language || 'English');
    if (!input) return json({ error: 'Please enter a question or topic.' }, 400);
    const prompts: Record<string,string> = {
      solve: `Solve/explain this clearly with steps for a learner: ${input}`,
      science: `Explain this science question accurately with examples: ${input}`,
      translate: `Translate the following into ${language}. Preserve meaning and formatting:\n${input}`,
      lyrics: `Write completely original song lyrics in ${language} for this topic. Use verse, memorable chorus and bridge. Do not imitate a named artist and do not reproduce copyrighted lyrics. Topic: ${input}`,
      ringtone_idea: `Turn this customer idea into a concise original ringtone concept in ${language}, with melody/mood/instrument cues and optional original hook. Do not imitate a named artist: ${input}`,
      creator: `Create polished, engaging content for this platform/topic. Include hook, structure, CTA and useful hashtags.\n${input}`,
      current_affairs: `Provide a current-affairs briefing for India/world/business/technology/science/sports/education as requested. Prefer current verifiable information and clearly label uncertainty. Then give 5 quiz questions.\n${input}`,
      search: `Research this topic and return a concise factual summary, key entities, major points, and useful source names/URLs. Clearly separate known facts from uncertainty. Topic: ${input}`,
      jobs: `Find and summarize current Indian government jobs, recruitment and exam updates relevant to the request. Include official portal names/URLs where known and avoid inventing deadlines.\n${input}`
    };
    const grounded = type === 'current_affairs' || type === 'jobs' || type === 'search';
    const text = await geminiText(prompts[type] || input, grounded);
    return json({ text });
  } catch (error) {
    return json({ error: String((error as Error)?.message || error) }, 500);
  }
});

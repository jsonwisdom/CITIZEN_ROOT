// CI-FIRST tests for the publication-approved national evidence dashboard.
// Uses only Node built-ins and the pinned source manifest; no network / deployments.
import assert from 'node:assert/strict';
import { readFileSync, copyFileSync, rmSync } from 'node:fs';
import { createHash } from 'node:crypto';
const file='site/national-evidence-dashboard/worker.js';
const temporary='site/national-evidence-dashboard/worker.ci.mjs';
copyFileSync(file,temporary);
try{
  const {default:worker}=await import('../site/national-evidence-dashboard/worker.ci.mjs');
  const invoke=async(path,method='GET')=>worker.fetch(new Request('https://test.example'+path,{method}));
  const base=await invoke('/');
  assert.equal(base.status,200);assert.match(base.headers.get('content-security-policy'),/frame-ancestors 'none'/);
  const html=await base.text();
  assert.match(html,/Legal causation/i);assert.match(html,/no government authority/i);
  assert.match(html,/Recompute root in browser/);
  const manifest=await (await invoke('/api/manifest')).json();
  const original=JSON.parse(readFileSync('jurisdictions/US_2026_STATE_RECEIPTS_ORIGINAL_LOG_SHA256_V0_1.json','utf8')).states;
  assert.equal(manifest.root,'85c1c9e8bf6ca6245a4c5966213508a168a25e9a766fd2798bd1f3ac44a86b7b');
  assert.equal(manifest.states.length,50);assert.equal(new Set(manifest.states.map(x=>x.fips)).size,50);
  assert.equal(manifest.legal_causation,'HOLD');assert.equal(manifest.government_authority,false);
  let totals={places:0,counties:0,edges:0,multicounty:0,changed:0};
  for(const s of manifest.states){assert.equal(s.hash,original[s.fips]);for(const k of Object.keys(totals))totals[k]+=s[k]}
  assert.deepEqual(totals,{places:32070,counties:3143,edges:33531,multicounty:1330,changed:834});
  const sha=(...pieces)=>createHash('sha256').update(Buffer.concat(pieces)).digest();
  let nodes=manifest.states.slice().sort((a,b)=>a.fips.localeCompare(b.fips)).map(x=>sha(Buffer.from('cw-us26-leaf-v1\0'),Buffer.from(x.fips),Buffer.from(x.hash,'hex')));
  while(nodes.length>1){if(nodes.length%2)nodes.push(nodes.at(-1));const next=[];for(let i=0;i<nodes.length;i+=2)next.push(sha(Buffer.from('cw-us26-node-v1\0'),nodes[i],nodes[i+1]));nodes=next}
  assert.equal(nodes[0].toString('hex'),manifest.root);
  const health=await (await invoke('/api/health')).json();assert.equal(health.root,manifest.root);assert.equal(health.government_authority,false);
  const mn=await (await invoke('/api/state/27')).json();assert.equal(mn.state.name,'Minnesota');assert.equal(mn.state.edges,968);
  assert.equal((await invoke('/api/state/03')).status,404);
  assert.equal((await invoke('/api/manifest','POST')).status,405);
  const head=await invoke('/api/health','HEAD');assert.equal(head.status,200);assert.equal(await head.text(),'');
  console.log('CW_DASHBOARD_CI_PASS states=50 national_root='+manifest.root+' tests=12');
}finally{rmSync(temporary,{force:true})}

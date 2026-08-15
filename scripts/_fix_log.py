#!/usr/bin/env python3
"""SCRATCH: fix 5 - ai-bot-log-analyzer: add source-IP + published-range verification."""
import os, re, subprocess
os.chdir("/sessions/optimistic-youthful-planck/mnt/rawmktg")
F="tools/ai-bot-log-analyzer.html"
h=open(F,encoding="utf-8").read()

new_script=r'''<script>
(function(){
  var root=document.getElementById('log'); if(!root) return;
  var ta=document.getElementById('logIn');
  var AGENTS=['OAI-SearchBot','ChatGPT-User','Claude-SearchBot','ClaudeBot','PerplexityBot','Perplexity-User','GPTBot','Google-Extended','Googlebot','Applebot-Extended','Amazonbot','Bytespider','CCBot','meta-externalagent'];
  var CITATION={'OAI-SearchBot':1,'PerplexityBot':1,'Claude-SearchBot':1,'Googlebot':1,'Perplexity-User':1,'ChatGPT-User':1};
  // Published crawler IP ranges we can verify authoritatively, browser-side.
  var RANGES={'Googlebot':['66.249.64.0/19'],'Google-Extended':['66.249.64.0/19']};
  function agentOf(line){var low=line.toLowerCase();for(var i=0;i<AGENTS.length;i++){if(low.indexOf(AGENTS[i].toLowerCase())>=0)return AGENTS[i];}return null;}
  function statusOf(line){var m=line.match(/"\s+(\d{3})\s/); if(m) return m[1];
    m=line.match(/"[A-Z]+\s[^"]*"\s(\d{3})/); if(m) return m[1];
    m=line.match(/\s(\d{3})\s\d+\s/); return m?m[1]:null;}
  function pathOf(line){var m=line.match(/"[A-Z]+\s(\S+)\s+HTTP/); return m?m[1]:'';}
  function ipOf(line){var m=line.match(/^\s*([0-9]{1,3}(?:\.[0-9]{1,3}){3})\b/); if(m) return m[1];
    m=line.match(/^\s*([0-9a-fA-F:]{3,}:[0-9a-fA-F:]+)\s/); return m?m[1]:null;}
  function ipInt(ip){var p=ip.split('.'); if(p.length!==4) return null; return (((+p[0])<<24)>>>0)+((+p[1])<<16)+((+p[2])<<8)+(+p[3]);}
  function inCidr(ip,cidr){var a=cidr.split('/'), base=ipInt(a[0]), n=+a[1], x=ipInt(ip); if(base===null||x===null) return false; var mask=n===0?0:((0xFFFFFFFF<<(32-n))>>>0); return ((x&mask)>>>0)===((base&mask)>>>0);}
  function verify(agent,ip){var r=RANGES[agent]; if(!r) return 'unknown'; if(!ip) return 'noip'; for(var i=0;i<r.length;i++){ if(inCidr(ip,r[i])) return 'verified'; } return 'spoof';}
  function run(){
    var lines=(ta.value||'').split(/\r?\n/).filter(function(l){return l.trim();});
    var stats={total:0,llms:0,blocked403:0,blocked429:0,verified:0,spoof:0};
    var byAgent={};
    lines.forEach(function(ln){
      var a=agentOf(ln); if(!a) return;
      stats.total++;
      var st=statusOf(ln)||'---', pth=pathOf(ln), ip=ipOf(ln), vf=verify(a,ip);
      if(pth.indexOf('/llms.txt')===0||pth.indexOf('/llms-full.txt')===0) stats.llms++;
      if(!byAgent[a]) byAgent[a]={n:0,st:{},cit:CITATION[a]?1:0,verified:0,spoof:0,checkable:!!RANGES[a]};
      byAgent[a].n++; byAgent[a].st[st]=(byAgent[a].st[st]||0)+1;
      if(vf==='verified'){byAgent[a].verified++; stats.verified++;}
      if(vf==='spoof'){byAgent[a].spoof++; stats.spoof++;}
      if(CITATION[a]&&st==='403') stats.blocked403++;
      if(CITATION[a]&&st==='429') stats.blocked429++;
    });
    var S=document.getElementById('logStats');
    if(!stats.total){S.innerHTML='';document.getElementById('logAgents').innerHTML='';document.getElementById('logFlags').innerHTML='<div class="flag">Paste log lines to analyze.</div>';return;}
    S.innerHTML=''
     +'<div class="lt-stat"><div class="n">'+stats.total.toLocaleString()+'</div><div class="k">AI bot requests</div></div>'
     +'<div class="lt-stat"><div class="n good">'+stats.verified.toLocaleString()+'</div><div class="k">IP-verified</div></div>'
     +'<div class="lt-stat"><div class="n '+(stats.spoof?'warn':'good')+'">'+stats.spoof+'</div><div class="k">possible spoof</div></div>'
     +'<div class="lt-stat"><div class="n '+((stats.blocked403+stats.blocked429)?'warn':'good')+'">'+(stats.blocked403+stats.blocked429)+'</div><div class="k">403/429 to citation bots</div></div>';
    var names=Object.keys(byAgent).sort(function(a,b){return byAgent[b].n-byAgent[a].n;});
    document.getElementById('logAgents').innerHTML=names.map(function(a){
      var d=byAgent[a]; var bad=(d.st['403']||0)+(d.st['429']||0);
      var codes=Object.keys(d.st).sort().map(function(c){return c+'×'+d.st[c];}).join('  ');
      var vtag = d.spoof ? '<span class="as blocked">'+d.spoof+' spoof?</span>'
               : d.checkable ? (d.verified? '<span class="as ok">'+d.verified+' IP-verified</span>':'<span class="as">no IP match</span>')
               : '<span class="as">UA-only</span>';
      var btag = d.cit&&bad ? '<span class="as blocked">'+bad+' blocked</span>' : '';
      return '<div class="agrow"><span class="an">'+a+'<br><span style="color:rgba(255,255,255,.4);font-size:10px">'+codes+'</span></span>'+vtag+btag+'<span class="ac">'+d.n+'</span></div>';
    }).join('');
    var flags=[];
    if(stats.spoof){flags.push('<div class="flag">'+stats.spoof+' request'+(stats.spoof===1?'':'s')+' claim a verifiable crawler (Google) from a source IP outside its published range, likely spoofed. Do not treat these as real crawler visits.</div>');}
    if(stats.blocked403||stats.blocked429){flags.push('<div class="flag">Citation bots are being blocked ('+(stats.blocked403+stats.blocked429)+' 403/429 responses). Your WAF or rate limiter is a direct, usually invisible cause of missing AI citations, fix this before anything else.</div>');}
    else{flags.push('<div class="flag ok">No citation bots are being blocked in this sample. Good.</div>');}
    flags.push('<div class="flag">User-agent strings are trivially spoofable. This tool verifies source IPs against Google’s published crawler range; for GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot and PerplexityBot, confirm each source IP against the provider’s published range and a reverse-DNS forward-confirm before trusting the visit.</div>');
    if(stats.llms===0){flags.push('<div class="flag">Zero requests to /llms.txt in this sample, consistent with public search crawlers bypassing the file. Focus on crawlable HTML and clean status codes.</div>');}
    document.getElementById('logFlags').innerHTML=flags.join('');
  }
  ta.addEventListener('input',run); run();
})();
</script>'''

# replace the old log script block
old=[s for s in re.findall(r'<script>(?!window\.dataLayer).*?</script>', h, re.S) if "getElementById('log')" in s][-1]
h=h.replace(old,new_script,1)

# deck + hint + method copy: mention verification
h=h.replace("Paste your server access log and see which AI crawlers hit your site, what status codes they get, and whether your citation bots are being blocked.",
            "Paste your server access log and see which AI crawlers hit your site, what status codes they get, whether your citation bots are being blocked, and whether the requests are genuine, verified against published crawler IP ranges.",1)
h=h.replace("It detects named AI user agents, tallies status codes, and flags 403/429s hitting your citation bots, the silent cause of missing AI citations.",
            "It detects named AI user agents, tallies status codes, verifies source IPs against published crawler ranges to flag spoofed user agents, and flags 403/429s hitting your citation bots, the silent cause of missing AI citations.",1)

open(F,"w",encoding="utf-8").write(h)
m=[s for s in re.findall(r'<script>(?!window\.dataLayer).*?</script>',h,re.S) if "getElementById('log')" in s][-1]
open("/tmp/log.js","w").write(m[8:-9])
r=subprocess.run(["node","--check","/tmp/log.js"],capture_output=True,text=True)
print("log node:", "OK" if r.returncode==0 else "FAIL "+r.stderr[:400])
print("has ipOf:", 'function ipOf' in h, "| inCidr:", 'function inCidr' in h, "| verify stat:", 'IP-verified' in h)

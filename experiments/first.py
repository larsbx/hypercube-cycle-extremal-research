"""All 4096 edge-deleted Q3 subgraphs, by ordinary cycle support."""
from pathlib import Path
from itertools import combinations
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from source import checked_source
checked_source()
edges=[(u,u^(1<<a)) for u in range(8) for a in range(3) if u<(u^(1<<a))]

def cycles(m):
    # Independent edge-subset characterization: connected 2-regular graph.
    out=[]
    for ids in combinations(range(12),m):
        vertices={v for i in ids for v in edges[i]}
        if len(vertices)!=m: continue
        adj={v:set() for v in vertices}
        for i in ids:
            u,v=edges[i]; adj[u].add(v);adj[v].add(u)
        if any(len(adj[v])!=2 for v in vertices):continue
        seen=set(); stack=[min(vertices)]
        while stack:
            v=stack.pop()
            if v not in seen: seen.add(v);stack.extend(adj[v]-seen)
        if seen!=vertices:continue
        support=len({(edges[i][0]^edges[i][1]).bit_length()-1 for i in ids})
        out.append((sum(1<<i for i in ids),support))
    return out

catalog={m:cycles(m) for m in (4,6,8)}
assert [len(catalog[m]) for m in (4,6,8)]==[6,16,6]
records={}
for mask in range(1<<12):
    e=mask.bit_count()
    counts={(m,s):sum(c&mask==c and support==s for c,support in cc)
            for m,cc in catalog.items() for s in (2,3)}
    row=records.setdefault(e,{'edge_count':e,'subgraphs':0,'min':dict(counts),'max':dict(counts)})
    row['subgraphs']+=1
    for key,v in counts.items():row['min'][key]=min(row['min'][key],v);row['max'][key]=max(row['max'][key],v)
rows=[]
for e,r in sorted(records.items()):
    rows.append({'edges':e,'subgraphs':r['subgraphs'],'strata':[
        {'length':m,'support':s,'minimum':r['min'][m,s],'maximum':r['max'][m,s]}
        for m,s in sorted(r['min'])]})
# Double-count cycle incidences among one-edge deletions, independent of support.
for m,cc in catalog.items():
    assert sum(sum(c&mask==c for c,_ in cc) for mask in range(1<<12) if mask.bit_count()==11)==(12-m)*len(cc)
assert sum(r['subgraphs'] for r in rows)==4096
print(json.dumps({'domain':'all spanning edge subsets of Q3','full_cube_cycles':{str(m):len(c) for m,c in catalog.items()},
    'envelopes':rows,'status':'finite exact envelopes only; no dimension-uniform extremal theorem'},indent=2))

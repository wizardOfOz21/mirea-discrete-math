from pathlib import Path
import json,html
BASE=Path(__file__).resolve().parent.parent
D=json.loads((BASE/'_data/tasks-msc2020.json').read_text())
N={n['code']:n for n in D['nodes']};T=D['tasks'];E=html.escape
# Only primary topics establish branches; secondary topics stay in their primary subsection.
primaries=list(dict.fromkeys(t['primary'] for t in T))
selected={c:[] for c in primaries}
owner={c:c for c in primaries}
for t in T:
 for q in t['secondary']:
  c=q['code']
  if N[c]['parent']==N[t['primary']]['parent'] and c not in owner:
   owner[c]=t['primary'];selected[t['primary']].append(c)
# Group by section, retaining task order rather than sorting topic codes.
sections=list(dict.fromkeys(N[N[c]['parent']]['parent'] for c in primaries))
order=[c for sec in sections for c in primaries if N[N[c]['parent']]['parent']==sec]
for t in T:
 assert t['primary'] in N
 for q in t['secondary']:assert q['code'] in N
colors={'root':('#e0f4f4','#1f8a8a'),'section':('#e3effc','#2f6fbf'),'group':('#f5f3fd','#6b4fbf'),'topic':('#e8f5ec','#27834b')}
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1900" height="1130" viewBox="0 0 1900 1130" font-family="Arial, sans-serif">','<rect width="1900" height="1130" fill="white"/>']
def text(x,y,v,size=22,weight=400,color='#1e293b'):
 s.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}">{E(v)}</text>')
def rect(x,y,w,h,kind):
 fill,stroke=colors[kind];s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
def path(points):
 s.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in points)+'" fill="none" stroke="#94a3b8" stroke-width="2"/>')
def tags(c):
 return ', '.join(t['id']+('★' if t['primary']==c else '') for t in T if t['primary']==c or (c in owner and N[t['primary']]['parent']==N[c]['parent'] and any(q['code']==c for q in t['secondary'])))
short={'05C50':'Графы и линейная алгебра','05C70':'Паросочетания и подмножества рёбер','05C60':'Изоморфизмы и гомоморфизмы','05C45':'Эйлеровость и гамильтоновость','13M05':'Структура конечных коммутативных колец','13M10':'Многочлены и конечные коммутативные кольца'}
text(32,48,'MSC2020 · общее дерево задач',36,700,'#2455ab')
text(32,87,'★ основной код задачи',21,color='#475569')
positions={};y=155
for c in order:
 h=62+len(selected[c])*32
 positions[c]=(y,h,y+h/2);y+=h+16
assert y<1260,y
subsections=list(dict.fromkeys(N[c]['parent'] for c in order))
gy={g:sum(positions[c][2] for c in order if N[c]['parent']==g)/len([c for c in order if N[c]['parent']==g]) for g in subsections}
sy={sec:sum(positions[c][2] for c in order if N[N[c]['parent']]['parent']==sec)/len([c for c in order if N[N[c]['parent']]['parent']==sec]) for sec in sections}
ry=(min(sy.values())+max(sy.values()))/2
path([(140,ry),(158,ry),(158,min(sy.values())),(158,max(sy.values()))])
for sec in sections:
 cy=sy[sec];path([(158,cy),(180,cy)])
 gs=[g for g in subsections if N[g]['parent']==sec]
 path([(445,cy),(466,cy),(466,min(gy[g] for g in gs)),(466,max(gy[g] for g in gs))])
 for g in gs:
  cyg=gy[g];path([(466,cyg),(485,cyg)])
  ys=[positions[c][2] for c in order if N[c]['parent']==g]
  path([(805,cyg),(824,cyg),(824,min(ys)),(824,max(ys))])
  for c in order:
   if N[c]['parent']==g:path([(824,positions[c][2]),(845,positions[c][2])])
rect(20,ry-34,120,68,'root');text(31,ry+8,'MSC2020',22,700)
def groupcard(x,cy,w,code,kind):
 title=N[code]['title_ru'];words=title.split();lines=[];line=''
 for word in words:
  if len(line+' '+word)>int(w/12):lines.append(line);line=word
  else:line=(line+' '+word).strip()
 lines.append(line)
 h=38+len(lines)*24;rect(x,cy-h/2,w,h,kind);text(x+13,cy-h/2+29,code,24,700)
 for j,line in enumerate(lines):text(x+13,cy-h/2+53+24*j,line,20)
for sec,cy in sy.items():groupcard(180,cy,265,sec,'section')
for g,cy in gy.items():groupcard(485,cy,320,g,'group')
for c in order:
 top,h,cy=positions[c];rect(845,top,1015,h,'topic')
 text(862,top+35,c,24,700);text(968,top+35,short.get(c,N[c]['title_ru']),23,700)
 s.append(f'<rect x="1650" y="{top+10}" width="197" height="35" rx="8" fill="#fdf0dc"/>')
 text(1660,top+35,tags(c),22,700,'#8a5914')
 for j,q in enumerate(selected[c]):
  yy=top+66+32*j;text(862,yy,q,22,700);text(968,yy,short.get(q,N[q]['title_ru']),21)
  text(1660,yy,tags(q),21,400,'#8a5914')
s.append('</svg>')
svg='\n'.join(s);(BASE/'_src/tree.svg').write_text(svg)
md=['# MSC2020: общее дерево задач','','![Общее дерево](tree.svg)','','<!-- Источник: https://msc2020.org/; данные: ../_data/tasks-msc2020.json -->']
(BASE/'_src/tasks-msc2020.md').write_text('\n'.join(md)+'\n')
(BASE/'_src/tasks-msc2020.html').write_text('<!doctype html><meta charset="utf-8"><title>MSC2020 — задачи</title><style>@page{size:A3 landscape;margin:6mm}body{margin:0}svg{width:100%;height:283mm;display:block}</style>'+svg)
print(f'Общее дерево: {len(primaries)} основных тем, {sum(map(len,selected.values()))} дополнительных; {len(sections)} раздела.')

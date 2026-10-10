#!/usr/bin/env python3
"""Static validation of the Golden Fall V0.9 authoring data used by the game (game/data). Adapted from the pack's tests/validate_pack.py."""
from pathlib import Path
from itertools import product
import json
from datetime import date
BASE=Path(__file__).resolve().parents[1]
DOCS=BASE/'docs'/'golden_fall'
def load(name):return json.loads((BASE/'game'/'data'/name).read_text(encoding='utf-8'))

def validate():
 d=load('dialogues_en.json'); e=load('events_en.json'); b=load('blip_profiles.json'); web=load('web_pages_en.json'); messages=load('messages_en.json'); s=load('state_example.json'); q=load('qa_cases.json')
 assert all(a['schema_version']=='0.9.0' for a in (d,e,b,web,messages,s,q))
 assert d['locale']=='en-US' and web['locale']=='en-US' and messages['locale']=='en-US'
 assert [date.fromisoformat(day['date']).weekday() for day in e['days']]==[2,3,4]
 assert [day['day_index'] for day in e['days']]==[0,1,2]
 nodes={n['id']:n for n in d['nodes']}
 assert len(nodes)==len(d['nodes'])
 assert set(('fri_opening','fri_radio'))<=nodes.keys()
 assert set(('HANNAH','JUNE','???')) <= b['speakers'].keys()
 assert b['defaults']['max_notes_per_second']<=9
 choices=[]
 for name in ['fri_opening','fri_radio']:
  node=nodes[name]
  assert node['speaker']=='HANNAH' and node['day']==2
  assert len(node['choices'])==3
  assert len({c['id'] for c in node['choices']})==3
  for c in node['choices']:
   assert c['text'] and c['reply_text'] and c['reply_id']
   assert c['text'].strip()==c['text']
  choices.append(node['choices'])
 seq=d['rehearsal']['sequence']; expected={'fri_opening','fri_radio'}
 for step in seq:
  if step['kind'].startswith('stored_'):
   assert step['node_id'] in expected
  if step['kind']=='stored_selected_choice':
   assert step['display_speaker']=='???'
 for a,c in product(choices[0],choices[1]):
  stored={'fri_opening':a,'fri_radio':c}
  replay=[(step['display_speaker'],stored[step['node_id']]['text']) for step in seq if step['kind']=='stored_selected_choice']
  assert replay==[('???',a['text']),('???',c['text'])]
  assert all(x[0]!='YOU' for x in replay)
 assert s['friday_example']['dialogue_choices']['fri_opening']['selected_text']==choices[0][0]['text']
 assert s['friday_example']['dialogue_choices']['fri_radio']['selected_text']==choices[1][1]['text']
 assert len(web['pages'])>=2 and all(date.fromisoformat(p['published']) <= date(2003,10,17) for p in web['pages'])
 assert len(q['manual_checks'])>=16
 assert [msg['day'] for msg in messages['messages']]==[0,1,2]
 assert any('callback_if_flags' in n for n in d['nodes'] if n['id']=='hannah_day2')
 assert any('callback_if_flags' in n for n in d['nodes'] if n['id']=='june_day2')
 doc=(DOCS/'03_THE_REHEARSAL.md').read_text(encoding='utf8')
 assert '???' in doc and 'no voice' in doc.lower() and 'No monster' in doc
 for f in ['README.md','AGENTS.md','CODEX_START_PROMPT.md','docs/00_CANON.md','docs/01_MICRO_MVP_GAMEPLAY.md','docs/02_THREE_DAYS.md','docs/03_THE_REHEARSAL.md','docs/04_CHARACTERS_AND_SCRIPT.md','docs/05_DIALOGUE_UI_AND_BLIPS.md','docs/06_SPACES_ART_SOUND.md','docs/07_COMPUTER_AND_WEB.md','docs/08_STATE_DATA_CONTRACT.md','docs/09_PRODUCTION_AND_TESTS.md','docs/10_FUTURE_NOT_NOW.md','docs/11_V08_MIGRATION.md']:
  assert (DOCS/f.replace('docs/','')).stat().st_size > 300, f
 print('PASS: JSON, IDs, nine Friday choice combinations, ??? labeling, event days, web chronology, all required docs')
import unittest
class GoldenFallPackTests(unittest.TestCase):
    def test_pack_contracts(self): validate()
if __name__=='__main__': validate()

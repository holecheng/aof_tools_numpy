import json


case = '''
{"case_num":1086008,"showdown_ranks":[[0,0,0,1086008],[300784,438986,346238,0],[317281,278610,490117,0],[473919,381692,230397,0]],"final_ranks":[[0,0,0,1],[0,1,0,0],[0,0,1,0],[1,0,0,0]]}
'''
if isinstance(case, str):
    a = json.loads(
        case
    )
else:
    a = case

print(type(a))




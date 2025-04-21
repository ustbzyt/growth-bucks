import json

with open('behaviors.json', encoding='utf-8') as f:
    behaviors = json.load(f)

max_score = 0
for b in behaviors:
    if b['frequency'] == 'daily':
        max_score += b['points'] * 7
    elif b['frequency'] == 'weekly':
        max_score += b['points']
    elif b['frequency'] == 'occasionally':
        max_score += b['points'] * 3

print("本周理论最高得分：", max_score)

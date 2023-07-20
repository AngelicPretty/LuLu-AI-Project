import json

# 打开 JSON 文件并读取其内容
with open('emoji.json') as f:
	data = json.load(f)

# 获取 cat_Hi 的值
cat_hi_value = data['emoji'][0]['cat']['cat_Hi']

print(cat_hi_value)

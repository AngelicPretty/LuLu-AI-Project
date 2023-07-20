
import os
import requests
import json
import openai

#设置代理
#os.environ["HTTP_PROXY"] = "127.0.0.1:1089"
#os.environ["HTTPS_PROXY"] = "127.0.0.1:8889"
# 设置OpenAI API密钥和端点URL
openai.api_key = 'sk-lQJ1P17Hwrzcu3DOD4Da04034267424a94B818AeFb5f2fFf'
openai.api_base = "https://openkey.cloud/v1/chat/completions"
url = "https://openkey.cloud/v1/chat/completions"
# 定义用于向API发送请求并获取响应的函数
def chat_gpt(prompt):
	headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Bearer sk-lQJ1P17Hwrzcu3DOD4Da04034267424a94B818AeFb5f2fFf'
		}
	data = {
			"model": "gpt-3.5-turbo",
			f"messages": prompt
		}
	response = requests.post(url, headers=headers, json=data)
	print("[+] Send Status: ", response.status_code)
	resp = response.json()
	content = resp['choices'][0]['message']['content']
	print("[+] LuLu AI: ", content)
	return content

def __init__(messages=[]) -> None:
        # 初始化对话列表，可以加入一个key为system的字典，有助于形成更加个性化的回答
        # self.conversation_list = [{'role':'system','content':'你是一个非常友善的助手'}]
        messages = []

# 接受并发送消息
def send_chatgpt_message(text):
	# Open lulu prompt file
	file = open('./resources/lulu_prompts.txt', 'r')
	prompts = file.read()
	file.close()

	messages = [{f"role": "system","content": prompts}]
	'''
	while True:
	'''
	try:
			#text = input("[+] Input Messages: ")
			#if text == 'quit':
				#break
		d = {"role":"user","content":text}
		messages.append(d)
		text = chat_gpt(messages)
			#d = {"role":"assistant","content":text}
			#messages.append(d)
		return text
	except:
		messages.pop()
		print("[-] LuLu AI: ERROR!")
		text = "LuLu AI bot 发生错误！请稍候重试"
		return text

if __name__ == "__main__":
	#send_chatgpt_message()
	print("[+] Welcome to LuLu AI Bot~")

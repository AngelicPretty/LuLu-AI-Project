# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import json
import random
import Chatgpt
import vpn_user
import lulu_bot_api

from typing import List
from botbuilder.core import CardFactory, TurnContext, MessageFactory
from botbuilder.core.teams import TeamsActivityHandler, TeamsInfo
from botbuilder.schema import CardAction, HeroCard, Mention, ConversationParameters, Attachment, Activity, CardImage, ChannelAccount
from botbuilder.schema.teams import TeamInfo, TeamsChannelAccount
from botbuilder.schema._connector_client_enums import ActionTypes
from resources.sentences import sentences

ADAPTIVECARDTEMPLATE = "resources/UserMentionCardTemplate.json"

class TeamsConversationBot(TeamsActivityHandler):
	def __init__(self, app_id: str, app_password: str):
		self._app_id = app_id
		self._app_password = app_password

	async def on_message_activity(self, turn_context: TurnContext):
		if turn_context.activity.attachments == None:
			TurnContext.remove_recipient_mention(turn_context.activity)
			text = turn_context.activity.text.strip().lower()
			print("[+] From:", turn_context.activity.from_property.name)
			print("[+] Content message: ", turn_context.activity.text)
			print("[+] Time: ", turn_context.activity.timestamp)
		else:
			print("[+] From:", turn_context.activity.from_property.name)
			print("[+] Content message type: Image")
			print("[+] Time: ", turn_context.activity.timestamp)
			text = "image"

		if "bot:" in text:
			await self._chatgpt(turn_context, text)
			return

		if "搜索" in text:
			await self._user_profiles(turn_context, text)
			return

		if "vpn:" in text:
			await self._user_vpn(turn_context, text)
			return

		if "hi" in text or "你好" in text:
			await self._lulu_activity(turn_context)
			return

		if "chatgpt" in text:
			await self._chatgpt_info(turn_context, text)
			return

		if "wifi" in text:
			await self._wifi_card(turn_context)
			return

		if "重置" in text or "密码" in text:
			await self._password_reset(turn_context, text)
			return

		if "wifi" in text:
			await self._wifi_card(turn_context)
			return

		if "who" in text:
			await self._get_member(turn_context)
			return

		if "card" in text:
			await self._send_card(turn_context, True)
			return

		if "bitlocker:" in text:
			await self._devices_id(turn_context, text)
			return

		if "devices_id:" in text:
			await self._recoverykeys_id(turn_context, text)
			return

		if "todesk" in text:
			await self._todesk_url(turn_context)
			return

		if "image" in text:
			await self._image_reply(turn_context)
			return

		else:
			await self._chatgpt(turn_context, text)
			return

	async def _lulu_activity(self, turn_context: TurnContext):
		print("[+] LuLu: Welcome")
		# Test info turn context activity def
		reply_activity = MessageFactory.text("见到你很高兴,我是一名仙灵女巫名字叫LuLu~, 是你最好的助手!")
		await turn_context.send_activity(reply_activity)
		reply_activity = MessageFactory.text('<URIObject uri=\"https://static.asm.skype.com/pes/v1/items/eacf8b631a2e489d8f1da9e230e7ca72\" url_thumbnail=\"" type=\"Sticker.1\"><OriginalName v=\"Love\"></OriginalName></URIObject>')
		await turn_context.send_activity(reply_activity)

	async def _user_profiles(self, turn_context: TurnContext, message):
		reply_activity = MessageFactory.text("正在搜索用户中！请稍等片刻...")
		await turn_context.send_activity(reply_activity)
		search_name = message[message.index("搜索") + 2:]
		json_resp = lulu_bot_api.user_profiles(search_name)
		if json_resp is not None:
			reply_activity = MessageFactory.text("LuLu已经成功搜索到！")
			await turn_context.send_activity(reply_activity)
			displayName = lulu_bot_api.json_to_str(json_resp["displayName"])
			displayName = bytes(displayName, 'utf-8').decode('unicode_escape')
			user_id = json_resp["id"]
			officeLocation = lulu_bot_api.json_to_str(json_resp["officeLocation"])
			jobTitle = lulu_bot_api.json_to_str(json_resp["jobTitle"])
			mail = lulu_bot_api.json_to_str(json_resp["mail"])
			reply = "姓名: " + displayName + "\n" + "UID: "  + user_id + "\n" + "职位名称: " + jobTitle  + "\n" + "办公地点: " + officeLocation + "\n" + " 邮箱地址: " + mail
			reply_activity = MessageFactory.text(reply)
			await turn_context.send_activity(reply_activity)
		elif json_resp is False:
			reply_activity = MessageFactory.text("对不起哦,LuLu的皮克斯服务器发生错误,请联系IT")
			await turn_context.send_activity(reply_activity)
		else:
			reply_activity = MessageFactory.text("对不起,LuLu没有找到相关人员,请重新搜索")
			await turn_context.send_activity(reply_activity)

	async def _chatgpt_info(self, turn_context: TurnContext, message):
		reply_activity = MessageFactory.text("LuLu正在接入ChatGpt中！请稍等片刻...")
		await turn_context.send_activity(reply_activity)
		reply_activity = MessageFactory.text("ChatGpt接入成功！请前面加上bot:对我进行对话...")
		await turn_context.send_activity(reply_activity)

	async def _chatgpt(self, turn_context: TurnContext, message):
		reply = Chatgpt.send_chatgpt_message(message)
		reply_activity = MessageFactory.text(reply)
		await turn_context.send_activity(reply_activity)

	async def _password_reset(self, turn_context: TurnContext, message):
		reply_activity = MessageFactory.text("正在重置密码中！请稍等片刻...")
		await turn_context.send_activity(reply_activity)
		user = message[message.index("密码") + 2:]
		json_resp, user_name = lulu_bot_api.change_password(user)
		if json_resp is not None:
			tmpassword = json_resp["newPassword"]
			reply = "LuLu成功为您重置密码!\n" + "用户名: " + user_name + "\n" + "临时密码: " + tmpassword + "\n"
			reply_activity = MessageFactory.text(reply)
			await turn_context.send_activity(reply_activity)
		else:
			reply_activity = MessageFactory.text("对不起哦,LuLu没有寻找到这个人,重置密码失败！")
			await turn_context.send_activity(reply_activity)

	async def _wifi_card(self, turn_context: TurnContext):
		reply_activity = MessageFactory.text("您好,WiFi密码为wuhan2013")
		await turn_context.send_activity(reply_activity)
		image_path = 'resources/WiFi_Card.png'
		with open(image_path, "rb") as image_file:
			image_data = image_file.read()
		image_name = os.path.basename(image_path)
		image_attachment = Attachment(
			content_url="http://lulubot.free.idcfengye.com/image/WiFi_Card.png",
			content_type="image/png",
			name = image_name
		)
		#attachment = lulu_bot_api.image_send(path)
		reply_activity = MessageFactory.attachment(image_attachment)
		await turn_context.send_activity(reply_activity)

	async def on_members_added_activity(self, members_added: List[ChannelAccount], turn_context: TurnContext):
		print("[+] LuLu join chat success!")
		print("[+] LuLu id: ", turn_context.activity.recipient.id)
		for member in members_added:
			print("[+] New member id: ", member.id)
			if member.id == turn_context.activity.recipient.id:
				# Paimon bot welcome Reply content
				reply_activity = MessageFactory.text("大家好，我是仙灵女巫璐璐 Bot~, 欢迎加入本群组！")
				await turn_context.send_activity(reply_activity)
				reply_activity = MessageFactory.text('<URIObject uri=\"https://static.asm.skype.com/pes/v1/items/51126a4346384193afa1a96e815e4087\" url_thumbnail=\"https://static.asm.skype.com/pes/v1/items/51126a4346384193afa1a96e815e4087\" type=\"Sticker.1\"><OriginalName v=\"Hi\"></OriginalName></URIObject>')
				await turn_context.send_activity(reply_activity)

	async def _send_card(self, turn_context: TurnContext, isUpdate):
		card = HeroCard(
			title="Paimon Hero Card",
			subtitle="Your bots — wherever your users are talking",
			text="Build and connect intelligent bots to interact with your users naturally wherever they are, from text/sms to Skype, Slack, Office 365 mail and other popular services.",
			images=[CardImage(url="https://docs.microsoft.com/en-us/bot-framework/media/how-it-works/architecture-resize.png")],
			buttons=[CardAction(type=ActionTypes.open_url,
					title="Get Started",
					value="https://docs.microsoft.com/en-us/bot-framework/")]
			)
		reply_activity = MessageFactory.attachment(CardFactory.hero_card(card))
		await turn_context.send_activity(reply_activity)

	async def _get_member(self, turn_context: TurnContext):
		TeamsChannelAccount: member = None
		try:
			member = await TeamsInfo.get_member(turn_context, turn_context.activity.from_property.id)
		except Exception as e:
			if "MemberNotFoundInConversation" in e.args[0]:
				await turn_context.send_activity("Member not found.")
				return
			else:
				raise
		else:
			await turn_context.send_activity(f"You are: {member.name}")

	async def _devices_id(self, turn_context: TurnContext, message):
		reply_activity = MessageFactory.text("LuLu正在搜索注册设备！请稍等片刻...")
		await turn_context.send_activity(reply_activity)
		message = message[message.index("bitlocker:") + 10:]
		reply = lulu_bot_api.user_devices(message)
		if reply is not None:
			print("[+] Get user devices success!")
			devices_name = []
			for json_str in reply:
				obj = json_str["displayName"]
				devices_name.append(obj)
			devices_id = []
			for json_str in reply:
				obj = json_str["deviceId"]
				devices_id.append(obj)
			buttons=[]
			for i in range(len(devices_name)):
				obj = CardAction(type=ActionTypes.post_back, title=devices_name[i],value="devices_id:{0}".format(devices_id[i]))
				buttons.append(obj)
			card = HeroCard(title="Devices name",subtitle="璐璐 bot - your best friend!", text="请选择要获取的设备名称", buttons=buttons)
			reply_activity = MessageFactory.attachment(CardFactory.hero_card(card))
			await turn_context.send_activity(reply_activity)
		else:
			print("[-] Failed to get user registration device!")
			reply_activity = MessageFactory.text("获取用户注册设备失败！")
			await turn_context.send_activity(reply_activity)

	async def _recoverykeys_id(self, turn_context: TurnContext, message):
		message = message[message.index("devices_id:") + 11:]
		reply, bearer_token = lulu_bot_api.user_recoverykeys(message)
		if reply["value"]:
			volume_type = []
			for json_str in reply["value"]:
				obj = lulu_bot_api.volume_type(json_str["volumeType"])
				volume_type.append(obj)
			recoverykeys = []
			for json_str in reply["value"]:
				obj = json_str["id"]
				key_id = lulu_bot_api.recovery_key(bearer_token, obj)
				recoverykeys.append(key_id)
			buttons=[]
			for i in range(len(volume_type)):
				obj = CardAction(type=ActionTypes.im_back, title=volume_type[i],value=recoverykeys[i])
				buttons.append(obj)
			card = HeroCard(title="Recover Bitlocker key",subtitle="璐璐 bot - your best friend!", text="请选择要获取恢复密钥的设备", buttons=buttons)
			reply_activity = MessageFactory.attachment(CardFactory.hero_card(card))
			await turn_context.send_activity(reply_activity)
		else:
			print("[-] Failed to get user device bitlocker key")
			reply_activity = MessageFactory.text("此用户设备设备没有使用恢复密钥")
			await turn_context.send_activity(reply_activity)

	async def _todesk_url(self, turn_context: TurnContext):
		reply_activity = MessageFactory.text("https://newdl.todesk.com/windows/ToDesk_Lite.exe")
		await turn_context.send_activity(reply_activity)

	async def _image_reply(self, turn_context: TurnContext):
		reply_activity = MessageFactory.text("是可爱的料理！璐璐下次就把皮克斯加进去")
		await turn_context.send_activity(reply_activity)

	async def _user_vpn(self, turn_context: TurnContext, message):
		message = message[message.index("vpn:") + 4:]
		reply = vpn_user.vpn_pass(message)
		if reply != False:
			print("[+] VPN user: ", reply["displayName"])
			print("[+] VPN pass: ", reply["pass"])
			reply = reply["displayName"] + " " + reply["pass"]
			reply_activity = MessageFactory.text(reply)
			await turn_context.send_activity(reply_activity)
		else:
			reply_activity = MessageFactory.text("抱歉,LuLu没有搜到~")
			await turn_context.send_activity(reply_activity)
			print("[+] Not found pass or user")

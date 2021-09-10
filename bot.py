# -*- coding: utf-8 -*-
import vk_api, time, random, json, vk_api.upload
from python3_anticaptcha import ImageToTextTask
from vk_api.longpoll import VkLongPoll, VkEventType

class Bot():
	def __init__(self, token, anticaptcha_key = ""):
		self.__anticaptcha_key = anticaptcha_key
		self.__api = vk_api.VkApi(token = token, captcha_handler = self.__captcha_handler)
		try:
			self.__longpoll = VkLongPoll(self.__api)
		except:
			raise NameError("Невалидный токен")
		self.__response_chance_in_chats = 0
		self.__response_chance_in_private_messages = 0
		self.__attachment_response_chance = 0
		self.__voice_message_response_chance = 0
		self.__sticker_sending_delay = 0
		self.__ignore_message_list = []
		self.__ignore_list = []
		self.__ignore_chat_list = []
		self.__template_list = []
		self.__attachment_list = []
		self.__voice_message_list = []
		self.join_chat_by_link_in_private_messages = True
		self.join_chat_by_link_in_chats = True
		self.messages_forwarding = True
		self.messages_forwarding_when_sticker_sent = True
		self.attachment_with_message = True

	def __captcha_handler(self,captcha):
		key = ImageToTextTask.ImageToTextTask(anticaptcha_key = self.__anticaptcha_key , save_format = 'const').captcha_handler(captcha_link = captcha.get_url())
		return captcha.try_again(key['solution']['text'])

	def set_ignore_message_list(self, ignore_message_list: list) -> None:
		if type(ignore_message_list) is list:
			self.__ignore_message_list = ignore_message_list
		else:
			print("Предупреждение: ignore_message_list не установлен, так как в функцию set_ignore_message_list должен быть передан объект типа list.\n")

	def set_ignore_chat_list(self, ignore_chat_list: list) -> None:
		if type(ignore_chat_list) is list:
			self.__ignore_chat_list = ignore_chat_list
		else:
			print("Предупреждение: ignore_chat_list не установлен, так как в функцию set_ignore_chat_list должен быть передан объект типа list.\n")

	def set_ignore_list(self, ignore_list: list) -> None:
		if type(ignore_list) is list:
			self.__ignore_list = ignore_list
		else:
			print("Предупреждение: ignore_list не установлен, так как в функцию set_ignore_list должен быть передан объект типа list.\n")

	def set_response_chance_in_chats(self, response_chance: int) -> None:
		if type(response_chance) is int:
			if 0 <= response_chance <= 100:
				self.__response_chance_in_chats = response_chance
				return
		print("Предупреждение: response_chance_in_chats не установлен, так как в функцию set_response_chance_in_chats должно быть передано число (int) от 0 до 100.\n")

	def set_response_chance_in_private_messages(self, response_chance: int) -> None:
		if type(response_chance) is int:
			if 0 <= response_chance <= 100:
				self.__response_chance_in_private_messages = response_chance
				return
		print("Предупреждение: response_chance_in_private_messages не установлен, так как в функцию set_response_chance_in_private_messages должно быть передано число (int) от 0 до 100.\n")

	def set_attachment_response_chance(self, attachment_response_chance: int) -> None:
		if type(attachment_response_chance) is int:
			if 0 <= attachment_response_chance <= 100:
				self.__attachment_response_chance = attachment_response_chance
				return
		print("Предупреждение: attachment_response_chance не установлен, так как в функцию set_attachment_response_chance должно быть передано число (int) от 0 до 100.\n")

	def set_voice_message_response_chance(self, voice_message_response_chance: int) -> None:
		if type(voice_message_response_chance) is int:
			if 0 <= voice_message_response_chance <= 100:
				self.__voice_message_response_chance = voice_message_response_chance
				return
		print("Предупреждение: voice_message_response_chance не установлен, так как в функцию set_voice_message_response_chance должно быть передано число (int) от 0 до 100.\n")

	def set_template_list(self, template_list: list) -> None:
		if type(template_list) is list:
			self.__template_list = template_list
		else:
			print("Предупреждение: template_list не установлен, так как в функцию set_template_list должен быть передан объект типа list.\n")

	def set_attachment_list(self, attachment_list: list) -> None:
		if type(attachment_list) is list:
			self.__attachment_list = attachment_list
		else:
			print("Предупреждение: attachment_list не установлен, так как в функцию set_attachment_list должен быть передан объект типа list.\n")

	def set_voice_message_list(self, voice_message_list: list) -> None:
		if type(voice_message_list) is list:
			self.__voice_message_list = voice_message_list
		else:
			print("Предупреждение: voice_message_list не установлен, так как в функцию set_voice_message_list должен быть передан объект типа list.\n")

	def set_sticker_sending_delay(self, delay: int) -> None:
		if type(delay) is int and delay >= 0:
			self.__sticker_sending_delay = delay
		else:
			print("Предупреждение: sticker_sending_delay не установлен, так как в функцию set_sticker_sending_delay должно быть передано число (int), которое больше либо равно 0.\n")

	def __reply(self, peer_id, user_id, message_id,  attachment = "", type = "typing"):
		message = None
		message_id_to_send_sticker = None
		sticker_id = None
		delay = 5
		if not self.messages_forwarding:
			if self.messages_forwarding_when_sticker_sent:
				message_id_to_send_sticker = message_id
			message_id = ""
		if "{delay:" in attachment:
			attachment = attachment.replace("{delay:", "{\"delay\":")
			index = attachment.find("{\"delay\":")
			try:
				delay = json.loads(attachment[index:])["delay"]
			except:
				print(f"Неверно указан параметр delay во вложении \"{attachment}\"")
			attachment = attachment[:index]
		if "{sticker_ids:" in attachment:
				attachment = attachment.replace("{sticker_ids:", "{\"sticker_ids\":")
				index = attachment.find("{\"sticker_ids\":")
				try:
					sticker_id = random.choice(json.loads(attachment[index:])["sticker_ids"])
				except:
					print(f"Неверно указан параметр sticker_ids во вложении \"{attachment}\"")
				attachment = attachment[:index]
		if type == "typing" and (self.attachment_with_message or not attachment):
			message = random.choice(self.__template_list)
			if "{delay:" in message:
				message = message.replace("{delay:", "{\"delay\":")
				index = message.find("{\"delay\":")
				try:
					delay = json.loads(message[index:])["delay"]
				except:
					print(f"Неверно указан параметр delay в шаблоне \"{message}\"")
				message = message[:index]
			if "{sticker_ids:" in message:
				message = message.replace("{sticker_ids:", "{\"sticker_ids\":")
				index = message.find("{\"sticker_ids\":")
				try:
					sticker_id = random.choice(json.loads(message[index:])["sticker_ids"])
				except:
					print(f"Неверно указан параметр sticker_ids в шаблоне \"{message}\"")
				message = message[:index]
			if "{name}" in message:
				message = message.format(name = f"[id{user_id}|{self.__api.method('users.get', {'user_ids': user_id})[0]['first_name']}]")
		for _ in range((delay - 1) // 5 + 1):
			if message or type =="audiomessage":
				self.__api.method("messages.setActivity", {"peer_id": peer_id, "type": type})
			time.sleep(10)
		if message or attachment:
			self.__api.method("messages.send", {"peer_id": peer_id, "random_id": 0, "message": message, "reply_to": message_id,"attachment": attachment})
		if sticker_id:
			if not self.messages_forwarding_when_sticker_sent:
				message_id_to_send_sticker = ""
			elif not message_id_to_send_sticker:
				message_id_to_send_sticker = message_id
			time.sleep(self.__sticker_sending_delay)
			self.__api.method("messages.send", {"peer_id": peer_id, "random_id": 0, "reply_to": message_id_to_send_sticker,"sticker_id": sticker_id})

	def __listen(self):
		for event in self.__longpoll.check():
			if event.type == VkEventType.MESSAGE_NEW:
				random_number = random.randint(1, 100)
				if not event.from_me and ((event.from_chat and random_number > 100 - self.__response_chance_in_chats) or (event.from_user and random_number > 100 - self.__response_chance_in_private_messages)) and event.user_id > 0  and (event.text or event.attachments) and not event.user_id in self.__ignore_list and not event.peer_id - 2000000000 in self.__ignore_chat_list:
					for message in self.__ignore_message_list:
						if message.lower() in event.text.lower():
							break
					else:
						if random.randint(1, 100) > 100 - self.__voice_message_response_chance:
							self.__reply(event.peer_id, event.user_id, event.message_id, attachment = random.choice(self.__voice_message_list), type = "audiomessage")
						elif random.randint(1, 100) > 100 - self.__attachment_response_chance:
							self.__reply(event.peer_id, event.user_id, event.message_id, attachment = random.choice(self.__attachment_list))
						else:
							self.__reply(event.peer_id, event.user_id, event.message_id)
				if "https://vk.me/join/" in event.text and ((event.from_chat and self.join_chat_by_link_in_chats) or (event.from_user and self.join_chat_by_link_in_private_messages)):
					try:
						self.__api.method('messages.joinChatByInviteLink',{'link': event.text[event.text.find("https://vk.me/join/"):]})
						print("Бот зашёл в беседу по инвайт-ссылке: {link}\n".format(link = event.text[event.text.find("https://vk.me/join/"):]))
					except:
						pass

	def run(self) -> None:
		if not self.__template_list and (self.__response_chance_in_chats  or self.__response_chance_in_private_messages):
			self.__response_chance_in_chats = 0
			self.__response_chance_in_private_messages = 0
			print("Предупреждение: template_list не установлен, поэтому response_chance_in_chats и response_chance_in_private_messages изменены на 0.")
		if not self.__attachment_list and self.__attachment_response_chance:
			self.__attachment_response_chance = 0
			print("Предупреждение: attachment_list не установлен, поэтому attachment_response_chance изменён на 0.")
		if not self.__voice_message_list and self.__voice_message_response_chance:
			self.__voice_message_response_chance = 0
			print("Предупреждение: voice_message_list не установлен, поэтому voice_message_response_chance изменён на 0.")
		match = {
			"TrueTrue": "Бот будет переходить в другие беседы по инвайт-ссылкам в личных сообщениях и беседах.",

			"TrueFalse": "Бот будет переходить в беседы по инвайт-ссылкам только в личных сообщениях.",

			"FalseTrue": "Бот будет переходить в другие беседы по инвайт-ссылкам только в беседах.",

			"FalseFalse": "Бот не будет переходить по инвайт-ссылкам в беседы."
		}
		print(f"Бот запущен!\nШанс ответа в беседе: {self.__response_chance_in_chats}%\nШанс ответа в личных сообщениях: {self.__response_chance_in_private_messages}%\nШанс отправки сообщения с вложением: {self.__attachment_response_chance}%\nШанс отправки голосового сообщения: {self.__voice_message_response_chance}%\nКоличество шаблонов: {len(self.__template_list)}\nКоличество вложений: {len(self.__attachment_list)}\nКоличество голосовых сообщений: {len(self.__voice_message_list)}\nПользователей в игнор листе: {len(self.__ignore_list)}\nБесед в игнор листе: {len(self.__ignore_chat_list)}\nСлов в игнор листе: {len(self.__ignore_message_list)}\n{match[str(self.join_chat_by_link_in_private_messages) + str(self.join_chat_by_link_in_chats)]}\n")
		while True:
			try:
				self.__listen()
			except Exception as error:
				print(f"Ошибка: {error}")

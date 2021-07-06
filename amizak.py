# coding=utf-8
import requests
import json
import time
from websocket import create_connection
import base64
from typing import BinaryIO
import random
from string import hexdigits
from uuid import UUID
from binascii import hexlify
from os import urandom
from locale import getdefaultlocale as locale

class Client:

	def __init__(self, email, password, deivce_id:str="01D4651E9A8F92763D2DEC4D62F1CAC312B9784014AC7ED24346EF8132D6D286F8A2087F4C320CE82B", proxy:dict=None):
		self.api = "https://service.narvii.com/api/v1/";
		self.proxy = proxy;
		self.headers = {
			"NDCDEVICEID": deivce_id,
			"NDC-MSG-SIG": "Aa0ZDPOEgjt1EhyVYyZ5FgSZSqJt",
			"Accept-Language": "en-US",
			"Content-Type": "application/json; charset=utf-8",
			"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/beyond1qlteue-user 5; com.narvii.amino.master/3.4.33562)", 
			"Host": "service.narvii.com",
			"Accept-Encoding": "gzip",
			"Connection": "Keep-Alive"
			}
		if not email and not password:
			self.sid = "?";
		else:
			self.authorization(email, password);

	def authorization(self, email, password):
		result = requests.post(f"{self.api}g/s/auth/login", data=json.dumps({"email":email,"secret":"0 "+password,"deviceID":self.headers["NDCDEVICEID"],"clientType":100,"action":"normal","timestamp":(int(time.time() * 1000))}), headers=self.headers, proxies=self.proxy)
		try:
			self.sid = result.json()["sid"];
			self.auid = result.json()["auid"];
			self.reload_socket();
		except:
			print(">>Error: "+result.json()["api:message"]);

	def request_verify_code(self, email):
		data = {
			"identity": email,
			"type": 1,
			"deviceID": self.headers["NDCDEVICEID"]
		}
		response = requests.post(f"{self.api}g/s/auth/request-security-validation", headers=self.headers, data=json.dumps(data), proxies=self.proxy)
		return response.json();

	def register(self, nickname: str = None, email: str = None, password: str = None, verificationCode:str=None, deviceId: str = None):
		if not deviceId:
			deviceId = self.headers["NDCDEVICEID"];

		data = json.dumps({
			"secret": f"0 {password}",
			"deviceID": deviceId,
			"email": email,
			"clientType": 100,
			"nickname": nickname,
			"latitude": 0,
			"longitude": 0,
			"address": None,
			"validationContext": {
				"data": {
					"code": verificationCode
				},
				"type": 1,
				"identity": email
			},
			"clientCallbackURL": "narviiapp://relogin",
			"type": 1,
			"identity": email,
			"timestamp": int(time.time() * 1000)
		})

		return requests.post(f"{self.api}g/s/auth/register", data=data, headers=self.headers, proxies=self.proxy).json();

	def get_from_deviceid(self, device_id:str="None"):
		return requests.get(f"{self.api}/g/s/auid?deviceId={device_id}", headers=self.headers, proxies=self.proxy).json();

	def reload_socket(self):
		self.socket_time = time.time();
		self.ws = create_connection("wss://ws1.narvii.com?signbody="+self.headers["NDCDEVICEID"]+"%7C"+str((int(time.time() * 1000)))+"&sid="+self.sid);

	def accept_host(self, community_id:int = None, chatId: str = None):
		data = json.dumps({"timestamp": int(time.time() * 1000)})

		response = requests.post(f"{self.api}/x{community_id}/s/chat/thread/{chatId}/accept-organizer?sid="+self.sid, headers=self.headers, data=data, proxies=self.proxy)
		return response.json()

	def get_notification(self, community_id, start:int = 0, size:int = 10):
		response = requests.get(f"{self.api}/x{community_id}/s/notification?start={start}&size={size}&sid="+self.sid, headers=self.headers, proxies=self.proxy);
		return response.json();

	def check_device(self, deviceId: str):
		data = json.dumps({
			"deviceID": deviceId,
			"bundleID": "com.narvii.amino.master",
			"clientType": 100,
			"timezone": -int(time.timezone) // 1000,
			"systemPushEnabled": True,
			"locale": locale()[0],
			"timestamp": int(time.time() * 1000)
		})

		response = requests.post(f"{self.api}/g/s/device", headers=self.headers, data=data, proxies=self.proxy).json()
		return response

	def get_wallet_info(self):
		response = requests.get(f"{self.api}/g/s/wallet?sid="+self.sid, headers=self.headers, proxies=self.proxy).json()
		return response

	def get_wallet_history(self, start:int = 0, size:int = 25):
		response = requests.get(f"{self.api}/g/s/wallet/coin/history?start={start}&size={size}&sid="+self.sid, headers=self.headers, proxies=self.proxy).json()
		return response

	def moderation_history_user(self, community_id:int = 0, userId: str = None, size: int = 25):
		response = requests.get(f"{self.api}x{community_id}/s/admin/operation?pagingType=t&size={size}&sid={self.sid}", headers=self.headers, proxies=self.proxy).json()
		return response

	def get_comms(self, start: int = 0, size: int = 25):
		response = requests.get(f"{self.api}g/s/community/joined?start={start}&size={size}&sid="+self.sid, headers=self.headers, proxies=self.proxy).json()
		return response

	def watch_ad(self):
		response = requests.post(f"{self.api}g/s/wallet/ads/video/start?sid={self.sid}", headers=self.headers, proxies=self.proxy).json()
		return response

	def transfer_host(self, community_id, chatId: str, userIds: list):
		data = json.dumps({
			"uidList": userIds,
			"timestamp": int(time.time() * 1000)
		})

		response = requests.post(f"{self.api}x{community_id}/s/chat/thread/{chatId}/transfer-organizer?sid="+self.sid, headers=self.headers, data=data, proxies=self.proxy).json()
		return response

	def join_chat(self, community_id, thread_id):
		response = requests.post(f"{self.api}x{community_id}/s/chat/thread/{chat_id}/member/{self.auid}?sid="+self.sid, headers=self.headers, proxies=self.proxy).json()
		return response

	def getMessages(self, community_id, thread_id, size):
		response = requests.get(f"{self.api}x{community_id}/s/chat/thread/{thread_id}/message?v=2&pagingType=t&size={size}&sid="+self.sid, headers=self.headers, proxies=self.proxy)
		return response

	def getThread(self, community_id, thread_id):
		response = requests.get(f"{self.api}x{community_id}/s/chat/thread/{thread_id}?sid="+self.sid, headers=self.headers, proxies=self.proxy)
		return response

	def sendAudio(self, path, community_id, thread_id):
		audio = base64.b64encode(open(path, "rb").read())
		return requests.post(f"{self.api}x{community_id}/s/chat/thread/{thread_id}/message?sid="+self.sid, data=json.dumps({"content":None,"type":2,"clientRefId":827027430,"timestamp":int(time.time() * 1000),"mediaType":110,"mediaUploadValue":audio,"attachedObject":None}), headers=self.headers, proxies=self.proxy).json();

	def ban(self, userId: str, community_id, reason: str, banType: int = None):

		response = requests.post(f"{self.api}x{community_id}/s/user-profile/{userId}/ban?sid="+self.sid, headers=self.headers, data=json.dumps({
			"reasonType": banType,
			"note": {
				"content": reason
			},
			"timestamp": int(time.time() * 1000)
		}), proxies=self.proxy).json();
		return response

	def get_banned_users(self, community_id, start: int = 0, size: int = 25):
		response = requests.get(f"{self.api}x{community_id}/s/user-profile?type=banned&start={start}&size={size}&sid="+self.sid, headers=self.headers, proxies=self.proxy).json()
		return response

	def unban(self, community_id, userId: str, reason: str):
		data = json.dumps({
			"note": {
				"content": reason
			},
			"timestamp": int(time.time() * 1000)
		})

		response = requests.post(f"{self.api}x{community_id}/s/user-profile/{userId}/unban?sid={self.sid}", headers=self.headers, data=data, proxies=self.proxy).json()
		return response

	def listen(self, return_data:int=1):
		if((time.time() - self.socket_time) > 100):
			self.ws.close()
			self.reload_socket()

		res = {}
		data = {}

		try:
			res = json.loads(self.ws.recv())
			if return_data == 1:
				data["json"] = res["o"]
		except:
			res["t"] = 0

		if res["t"] == 1000:
			data.update({
				"message_type":res["o"]["chatMessage"]["type"],
				"community_id":res["o"]["ndcId"],
				"thread_id":res["o"]["chatMessage"]["threadId"],
				"author":res["o"]["chatMessage"]["author"]["uid"] if "author" in res["o"]["chatMessage"] else None,
				"nickname":res["o"]["chatMessage"]["author"]["nickname"] if "author" in res["o"]["chatMessage"] else None,
				"role":res["o"]["chatMessage"]["author"]["role"] if "author" in res["o"]["chatMessage"] else None,
				"level":res["o"]["chatMessage"]["author"]["level"] if "author" in res["o"]["chatMessage"] else None,
				"message_id":res["o"]["chatMessage"]["messageId"],
				"content":res["o"]["chatMessage"]["content"] if "content" in res["o"]["chatMessage"] else "",
				"refId":res["o"]["chatMessage"]["clientRefId"] if "clientRefId" in res["o"]["chatMessage"] else "" 
				});
				
		elif res["t"] in [10, 0]:
			data.update({
				"message_type":-1,
				"community_id":res["o"]["payload"]["ndcId"],
				"thread_id":res["o"]["payload"]["tid"]
			})
		return data

	def setNickname(self, nickname, community_id):
		result = requests.post(f"{self.api}x{community_id}/s/user-profile/{Amino.auid}?sid="+self.sid,
			data=c.dumps({"nickname":nickname, "timestamp":(int(time.time() * 1000))}),
			headers=self.headers, proxies=self.proxy).json()
		return result

	def createUserChat(self, message, community_id, uid):
		result = requests.post(f"{self.api}x{community_id}/s/chat/thread?sid="+self.sid,
			data=json.dumps({'inviteeUids': [uid],"initialMessageContent":message,"type":0,"timestamp":(int(time.time() * 1000))}),
			headers=self.headers, proxies=self.proxy).json()
		return result

	def deleteMessage(self, thread_id: str, community_id, messageId: str, asStaff: bool = False, reason: str = None):
		data = json.dumps({
			"adminOpName": 102,
			"adminOpNote": {"content": reason},
			"timestamp": int(time.time() * 1000)
		})

		if not asStaff: response = requests.delete(f"{self.api}x{community_id}/s/chat/thread/{thread_id}/message/{messageId}?sid="+self.sid, headers=self.headers, proxies=self.proxy).json()
		else: response = requests.post(f"{self.api}x{community_id}/s/chat/thread/{thread_id}/message/{messageId}/admin?sid="+self.sid, headers=self.headers, data=data, proxies=self.proxy).json()
		
		return response

	def kick(self, author: str, thread_id: str, community_id, allowRejoin:int = 0):
		response = requests.delete(f"{self.api}x{community_id}/s/chat/thread/{thread_id}/member/{author}?allowRejoin={allowRejoin}&sid="+self.sid, headers=self.headers, proxies=self.proxy).json()
		return response

	def loadStickerImage(self, path):
		result = requests.post(self.api+"g/s/media/upload/target/sticker?sid="+self.sid,
			data=requests.get(path).content,
			headers=self.headers, proxies=self.proxy).json()
		return result

	def createStickerpack(self, name, stickers, community_id):
		result = requests.post(f"{self.api}x{com}/s/sticker-collection?sid="+self.sid,
			data=json.dumps({"collectionType":3,"description":"stickerpack","iconSourceStickerIndex":0,"name":name,"stickerList":stickers,"timestamp":(int(time.time() * 1000))}),
			headers=self.headers, proxies=self.proxy).json()
		return result

	def searchUserThread(self, uid, community_id):
		result = requests.get(f"{self.api}x{community_id}/s/chat/thread?type=exist-single&cv=1.2&q={uid}&sid="+self.sid, headers=self.headers, proxies=self.proxy).json()
		return result

	def vc_permission(self, community_id: str, thread_id: str, permission: int):
		response = requests.post(f"{self.api}x{community_id}/s/chat/thread/{thread_id}/vvchat-permission?sid="+self.sid, headers=self.headers, data=json.dumps({"vvChatJoinType": permission,"timestamp": int(time.time() * 1000)}), proxies=self.proxy).json()
		return response

	def sendEmbed(self, community_id: str, chatId: str, message: str = None, embedTitle: str = None, embedContent: str = None, embedImage: BinaryIO = None):
		data = {
			"type": 0,
			"content": message,
			"clientRefId": int(time.time() / 10 % 1000000000),
			"attachedObject": {
				"objectId": None,
				"objectType": 100,
				"link": None,
				"title": embedTitle,
				"content": embedContent,
				"mediaList": b""+embedImage
			},
			"extensions": {"mentionedArray": None},
			"timestamp": int(time.time() * 1000)
		}
		response = requests.post(f"{self.api}x{community_id}/s/chat/thread/{chatId}/message?sid="+self.sid, headers=self.headers, data=json.dumps(data), proxies=self.proxy).json()
		return response

	def send(self, message, community_id : str, thread_id, reply_message_id:str = None, notifcation : list = None, clientRefId:int=43196704):
		data = {"content":message,"type":0,"clientRefId":clientRefId,"mentionedArray": [notifcation], "timestamp":(int(time.time() * 1000))};
		if (reply_message_id != None): data["replyMessageId"] = reply_message_id;
		result = requests.post(f"{self.api}x{community_id}/s/chat/thread/{thread_id}/message?sid="+self.sid,
			data=json.dumps(data),
			headers=self.headers, proxies=self.proxy).json()
		return result

	def sendSystem(self, message, community_id, thread_id):
		result = requests.post(f"{self.api}x{community_id}/s/chat/thread/{thread_id}/message?sid="+self.sid,
			data=json.dumps({"content":message,"type":100,"clientRefId":43196704,"timestamp":(int(time.time() * 1000))}),
			headers=self.headers, proxies=self.proxy).json()
		return result

	def adminDeleteMessage(self, mid, community_id, thread_id):
		result = requests.post(f"{self.api}x{community_id}/s/chat/thread/{thread_id}/message/{mid}/admin?sid="+self.sid,
			data=json.dumps({"adminOpName": 102, "timestamp":(int(time.time() * 1000))}),
			headers=self.headers, proxies=self.proxy).json()
		return result

	def getUsersThread(self, community_id, thread_id):
		result = requests.get(f"{self.api}x{community_id}/s/chat/thread/{thread_id}/member?sid="+self.sid+"&type=default&start=0&size=50", headers=self.headers, proxies=self.proxy).json()
		return result

	def getThreads(self, community_id, start: int = 0, size: int = 5):
		result = requests.get(f"{self.api}x{community_id}/s/chat/thread?type=joined-me&start={start}&size={size}&sid="+self.sid, headers=self.headers, proxies=self.proxy).json()
		return result

	def thank_tip(self, community_id, thread_id: str, author: str):
		response = requests.post(f"{self.api}/x{community_id}/s/chat/thread/{thread_id}/tipping/tipped-users/{author}/thank?sid="+self.sid, headers=self.headers, proxies=self.proxy).json()
		return response

	def getUser(self, user_id, community_id):
		result = requests.get(f"{self.api}x{community_id}/s/user-profile/{user_id}?action=visit&sid="+self.sid, headers=self.headers, proxies=self.proxy).json()
		return result

	def get_tipped_users_wall(self, community_id, blog_id, start:int = 0, size:int = 25):
		response = requests.get(f"{self.api}/x{community_id}/s/blog/{blog_id}/tipping/tipped-users-summary?start={start}&size={size}&sid="+self.sid, headers=self.headers, proxies=self.proxy).json()
		return response

	def sendImage(self, image, community_id, thread_id):
		image = base64.b64encode(open(image, "rb").read())	
		result = requests.post(f"{self.api}x{community_id}/s/chat/thread/{thread_id}/message?sid="+self.sid,
			data=json.dumps({"type":0,"clientRefId":43196704,"timestamp":(int(time.time() * 1000)),"mediaType":100,"mediaUploadValue":image.strip().decode(),"mediaUploadValueContentType" : "image/jpg","mediaUhqEnabled":False,"attachedObject":None}),
			headers=self.headers, proxies=self.proxy).json()
		return result

	def join_community(self, community_id: str):
		response = requests.post(f"{self.api}x{community_id}/s/community/join?sid="+self.sid, data=json.dumps({"timestamp": int(time.time() * 1000)}), headers=self.headers, proxies=self.proxy).json()
		return response

	def invite_to_chat(self, community_id, thread_id: str, userId: [str, list]):
		if isinstance(userId, str): userIds = [userId]
		elif isinstance(userId, list): userIds = userId
		else: raise exceptions.WrongType(type(userId))

		data = json.dumps({
			"uids": userIds,
			"timestamp": int(time.time() * 1000)
		})

		response = requests.post(f"{self.api}/x{community_id}/s/chat/thread/{thread_id}/member/invite?sid="+self.sid, headers=self.headers, data=data, proxies=self.proxy).json()
		return response

	def join_chat(self, community_id, thread_id):
		response = requests.post(f"{self.api}x{community_id}/s/chat/thread/{thread_id}/member/{self.auid}?sid="+self.sid, headers=self.headers, proxies=self.proxy).json()
		return response

	def get_online_users(self, community_id, start: int = 0, size: int = 25):
		response = requests.get(f"{self.api}/x{community_id}/s/live-layer?topic=ndtopic:x{community_id}:online-members&start={start}&size={size}&sid="+self.sid, headers=self.headers, proxies=self.proxy).json()
		return response

	def get_users_community(self, community_id, start:int = 0, size:int = 25):
		response = requests.get(f"{self.api}x{community_id}/s/user-profile?type=recent&start={start}&size={size}&sid="+self.sid, headers=self.headers).json();
		return response

	def leave_chat(self, community_id, thread_id):
		response = requests.delete(f"{self.api}x{community_id}/s/chat/thread/{thread_id}/member/{self.auid}?sid="+self.sid, headers=self.headers, proxies=self.proxy).json()
		return response;

	def sendGif(self, image, community_id, thread_id):
		img = base64.b64encode(open(image, "rb").read())
		result = requests.post(f"{self.api}x{community_id}/s/chat/thread/{thread_id}/message?sid="+self.sid,
			data=json.dumps({"type":0,"clientRefId":43196704,"timestamp":(int(time.time() * 1000)),"mediaType":100,"mediaUploadValue":img.strip().decode(),"mediaUploadValueContentType" : "image/gid","mediaUhqEnabled":False,"attachedObject":None}),
			headers=self.headers, proxies=self.proxy).json()
		return result

	def commentProfile(self, content, community_id, author):
		result = requests.post(f"{self.api}x{community_id}/s/user-profile/{author}/comment?sid="+self.sid,
			data=json.dumps({"content":content,'mediaList': [],"eventSource":"PostDetailView","timestamp":(int(time.time() * 1000))}),
			headers=self.headers, proxies=self.proxy).json()
		return result

	def get_from_code(self, code: str):
		response = requests.get(f"{self.api}/g/s/link-resolution?q={code}", headers=self.headers, proxies=self.proxy).json()
		return response

	def get_user_blogs(self, community_id, author, start:int = 0,size:int = 25):
		response = requests.get(f"{self.api}/x{community_id}/s/blog?type=user&q={author}&start={start}&size={size}&sid="+self.sid, headers=self.headers, proxies=self.proxy).json()
		return response

	def get_community_info(self, community_id):
		response = requests.get(f"{self.api}/g/s-x{community_id}/community/info?withInfluencerList=1&withTopicList=true&influencerListOrderStrategy=fansCount", headers=self.headers, proxies=self.proxy).json()
		return response

	def check(self, community_id:int = 0, tz: int = -int(time.timezone) // 1000):
		data = json.dumps({"timezone": tz,"timestamp": int(time.time() * 1000)})

		response = requests.post(f"{self.api}/x{community_id}/s/check-in?sid="+self.sid, headers=self.headers, data=data, proxies=self.proxy).json()
		return response

	def send_coins_blog(self, community_id:int = 0, blogId:str = None, coins:int = None, transactionId:str = None):
		if(transactionId is None): transactionId = str(UUID(hexlify(urandom(16)).decode('ascii')));
		response = requests.post(f"{self.api}/x{community_id}/s/blog/{blogId}/tipping?sid="+self.sid, data=json.dumps({"coins": coins,"tippingContext": {"transactionId": transactionId},"timestamp": int(time.time() * 1000)}), headers=self.headers, proxies=self.proxy).json()
		return response

	def send_coins_chat(self, community_id:int = None, thread_id:str = None, coins:int = None, transactionId:str = None):
		if(transactionId is None): transactionId = str(UUID(hexlify(urandom(16)).decode('ascii')));
		response = requests.post(f"{self.api}/x{community_id}/s/chat/thread/{thread_id}/tipping?sid="+self.sid, data=json.dumps({"coins": coins,"tippingContext": {"transactionId":transactionId},"timestamp": int(time.time() * 1000)}), headers=self.headers, proxies=self.proxy).json()
		
		return response

	def lottery(self, community_id, tz: str = -int(time.timezone) // 1000):
		data = json.dumps({
			"timezone": tz,
			"timestamp": int(time.time() * 1000)
		})

		response = requests.post(f"{self.api}/x{community_id}/s/check-in/lottery?sid="+self.sid, headers=self.headers, data=data, proxies=self.proxy).json()
		return response

	def edit_thread(self, community_id:int = None, thread_id:str = None, content:str = None, title:str = None, backgroundImage:str = None):
		res = [];
		if backgroundImage is not None:
			data = json.dumps({"media": [100, backgroundImage, None], "timestamp": int(time.time() * 1000)});
			response = requests.post(f"{self.api}/x{community_id}/s/chat/thread/{thread_id}/member/{self.auid}/background?sid="+self.sid, data=data, headers=self.headers, proxies=self.proxy);
			res.append(response.json());

		data = {"timestamp":int(time.time() * 1000)}

		if(content): data["content"] = content
		if(title):   data["title"]   = title
		response = requests.post(f"{self.api}/x{community_id}/s/chat/thread/{thread_id}?sid="+self.sid, headers=self.headers, data=json.dumps(data), proxies=self.proxy);
		res.append(response.json())
		return res

	# Moder:{

	def moderation_history_community(self, community_id, size: int = 25):
		response = requests.get(f"{self.api}/x{community_id}/s/admin/operation?pagingType=t&size={size}&sid="+self.sid, headers=self.headers, proxies=self.proxy).json()
		return response

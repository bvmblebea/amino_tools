import terminal_banner

def mainmenu():
	print(terminal_banner.Banner("""
[1] Amino-Tools/spamTools
[2] Amino-Tools/chatTools
[3] Amino-Tools/activityTools
[4] Amino-Tools/profileTools
[5] Amino-Tools/raidTools
[0] Amino-Tools/Exit
"""))

def spamtoolsmenu():
	print("""[1] Amino-Tools/SpamBot
[2] Amino-Tools/WikiSpamBot
[3] Amino-Tools/WallSpamBot
[4] Amino-Tools/BlogCommentSpamBot
[0] Amino-Tools/Exit""")

def chattoolsmenu():
	print("""[1] Amino-Tools/ChatIdFinder
[2] Amino-Tools/ChatSecurity
[3] Amino-Tools/Co-HostKick
[4] Amino-Tools/FakeCoinTransaction
[0] Amino-Tools/Exit""")

def activitytoolsmenu():
	print("""[1] Amino-Tools/InviteBot
[2] Amino-Tools/LikeBot
[3] Amino-Tools/FollowBot
[4] Amino-Tools/UnfollowBot
[0] Amino-Tools/Exit""")

def profiletoolsmenu():
	print("""[1] Amino-Tools/AntiBan
[2] Amino-Tools/PostSpam
[3] Amino-Tools/WikiSpam
[0] Amino-Tools/Exit""")

def raidtoolsmenu():
	print("""[1] Amino-Tools/SystemMessageSpam
[2] Amino-Tools/SendSystemMessage
[3] Amino-Tools/Join&LeaveSpam
[4] Amino-Tools/CoinIpRecipient
[5] Amino-Tools/JoinActiveChats
[0] Amino-Tools/Exit""")

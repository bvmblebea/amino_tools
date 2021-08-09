# -*- coding: utf8 -*-
import pyfiglet
import asyncio

from aminotoolsconfigs import menuConfigs, toolsfunctions
from colored import fore, back, style, attr
attr(0)
print(fore.LIGHT_STEEL_BLUE + style.BOLD)
print("""Script by Lil Zevi
Github : https://github.com/LilZevi""")
print(pyfiglet.figlet_format("Amino", font="cosmic"))
print(pyfiglet.figlet_format("Tools", font="cosmic"))
theversion = ("4.4.2")
print(f"version = {theversion}")

menuConfigs.mainmenu()
tools = input("Type Number >> ")

if tools == "1":
	menuConfigs.spamtoolsmenu()
	spamtools = input("Type Number >> ")
	
	if spamtools == "1":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.spambot())

	elif spamtools == "2":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.wikispambot())

	elif spamtools == "3":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.wallspambot())

	elif spamtools == "4":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.blogspambot())

	elif spamtools == "0":
		toolsfunctions.scriptexit()
		exit()


elif tools == "2":
	menuConfigs.chattoolsmenu()
	chattools = input("Type Number >> ")
	
	if chattools == "1":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.chatidfinder())

	elif chattools == "2":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.chatsecurity())

	elif chattools == "3":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.cohostkick())

	elif chattools == "4":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.fakecointransaction())

	elif chattools == "0":
		toolsfunctions.scriptexit()
		exit()


elif tools == "3":
	menuConfigs.activitytoolsmenu()
	activitytools = input("Type Number >> ")

	if activitytools == "1":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.invitebot())
					
	elif activitytools == "2":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.likebot())

	elif activitytools == "3":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.followbot())
	
	elif activitytools == "4":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.unfollowbot())

	elif activitytools == "0":
		toolsfunctions.scriptexit()
		exit()

elif tools == "4":
	menuConfigs.profiletoolsmenu()
	profiletools = input("Type Number >> ")

	if profiletools == "1":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.antiban())

	elif profiletools == "2":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.postspam())

	elif profiletools == "3":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.wikispam())

	elif profiletools == "0":
		toolsfunctions.scriptexit()
		exit()

elif tools == "5":
	menuConfigs.raidtoolsmenu()
	raidtools = input("Type Number >> ")

	if raidtools == "1":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.sysmessagespam())
			
	elif raidtools == "2":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.sysmessagesend())
		
	elif raidtools == "3":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.joinleavespam())

	elif raidtools == "4":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.iprecipient())

	elif raidtools == "5":
		asyncio.get_event_loop().run_until_complete(toolsfunctions.joinactivechats())
		
	elif raidtools == "0":
		toolsfunctions.scriptexit()
		exit()

if tools == "0":
	toolsfunctions.scriptexit()
	exit()
	quit()
exit()
sys.exit()

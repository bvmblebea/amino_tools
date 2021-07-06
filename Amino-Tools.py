# -*- coding: utf8 -*-
import pyfiglet
from aminotoolsconfigs import menuConfigs
from aminotoolsconfigs import toolsfunctions
from colorama import init, Fore, Back, Style
init()
print(Fore.BLUE + Style.BRIGHT)
print("""Script by Lil Zevi
Github : https://github.com/LilZevi""")
print(pyfiglet.figlet_format("Amino", font="cosmic"))
print(pyfiglet.figlet_format("Tools", font="cosmic"))
theversion = ("3.9.2")
print(f"version = {theversion}")



menuConfigs.mainmenu()
tools = input("Type Number >> ")

if tools == "1":
	menuConfigs.spamtoolsmenu()
	spamtools = input("Type Number >> ")
	
	if spamtools == "1":
		toolsfunctions.spambot()

	elif spamtools == "2":
		toolsfunctions.wikispambot()

	elif spamtools == "3":
		toolsfunctions.wallspambot()

	elif spamtools == "4":
		toolsfunctions.blogspambot()

	elif spamtools == "0":
		toolsfunctions.scriptexit()
		exit()


elif tools == "2":
	menuConfigs.chattoolsmenu()
	chattools = input("Type Number >> ")
	
	if chattools == "1":
		toolsfunctions.chatidfinder()

	elif chattools == "2":
		toolsfunctions.chatsecurity()

	elif chattools == "3":
		toolsfunctions.cohostkick()

	elif chattools == "4":
		toolsfunctions.fakecointransaction()

	elif chattools == "0":
		toolsfunctions.scriptexit()
		exit()


elif tools == "3":
	menuConfigs.activitytoolsmenu()
	activitytools = input("Type Number >> ")

	if activitytools == "1":
		toolsfunctions.invitebot()
					
	elif activitytools == "2":
		toolsfunctions.likebot()

	elif activitytools == "3":
		toolsfunctions.followbot()
	
	elif activitytools == "4":
		toolsfunctions.unfollowbot()

	elif activitytools == "0":
		toolsfunctions.scriptexit()
		exit()

elif tools == "4":
	menuConfigs.profiletoolsmenu()
	profiletools = input("Type Number >> ")

	if profiletools == "1":
		toolsfunctions.antiban()

	elif profiletools == "2":
		toolsfunctions.postspam()

	elif profiletools == "3":
		toolsfunctions.wikispam()

	elif profiletools == "0":
		toolsfunctions.scriptexit()
		exit()

elif tools == "5":
	menuConfigs.raidtoolsmenu()
	raidtools = input("Type Number >> ")

	if raidtools == "1":
		toolsfunctions.sysmessagespam()
			
	elif raidtools == "2":
		toolsfunctions.sysmessagesend()
		
	elif raidtools == "3":
		toolsfunctions.joinleavespam()

	elif raidtools == "4":
		toolsfunctions.chatcrash()

	elif raidtools == "5":
		toolsfunctions.iprecipient()

	elif raidtools == "6":
		toolsfunctions.theaminoadvbo()

	elif raidtools == "7":
		toolsfunctions.joinactivechats()
	
	elif raidtools == "8":
		toolsfunctions.autoregister()
		
	elif raidtools == "0":
		toolsfunctions.scriptexit()
		exit()

elif tools == "6":
	menuConfigs.dontclickmenu()
	dontclickselect = input("Type Number >> ")

	if dontclickselect == "1":
		generatingnumber = int(input("How Much DeviceId Generate: "))

		toolsfunctions.deviceIdgeneratingproccess()
		print(f"\nGenerated {generatingnumber} deviceids")

	elif dontclickselect == "2":
		toolsfunctions.thecoingenerator()

		
if tools == "0":
	toolsfunctions.scriptexit()
	exit()
	quit()
exit()
sys.exit()

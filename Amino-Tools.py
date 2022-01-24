from sty import fg
from pyfiglet import figlet_format
from asyncio import get_event_loop
from amino_tools_configs import main_functions
print(
    f"""{fg(36)}Script by deluvsushi
Github : https://github.com/deluvsushi"""
)
print(figlet_format("Amino-Tools", font="smslant", width=58))

get_event_loop().run_until_complete(main_functions.main())

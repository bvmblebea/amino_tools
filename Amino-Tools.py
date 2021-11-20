import asyncio
import pyfiglet
from amino_tools_configs import main_functions
from sty import fg; print(fg(36))
print("""Script by deluvsushi
Github : https://github.com/deluvsushi""")
print(pyfiglet.figlet_format("Amino-Tools", font="smslant", width=58))

asyncio.get_event_loop().run_until_complete(main_functions.main())

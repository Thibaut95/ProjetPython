from Blackjack.connectionbot import *

# Lancer le programme.
loop = asyncio.get_event_loop()
loop.set_debug(True)
loop.run_until_complete(main())
loop.close()

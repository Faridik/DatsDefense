import api
from bot import Bot

ASCII_LOGO = """
  _  __         _           _    _   _   ___  ___ _____ 
 | |/ /_ _ _  _| |_ _  _ __| |_ | |_(_) | _ )/ _ \_   _|
 | ' <| '_| || |  _| || (_-< ' \| / / | | _ \ (_) || |  
 |_|\_\_|  \_,_|\__|\_, /__/_||_|_\_\_| |___/\___/ |_|  
                    |__/                                
"""

def main(bot: Bot):
    bot.go()

if __name__ == "__main__":
    bot = Bot()
    main(bot)
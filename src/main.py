"""
Main script
"""

# Import needed libs, modules
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import logging

from config import Config
from services import DataBase

# Init bot, logger
storage = MemoryStorage()
bot     = Bot(token=Config.token)
dp      = Dispatcher(bot=bot, storage=storage)
db      = DataBase(Config.db_file)

logging.basicConfig(level=logging.INFO, filename='log.log', filemode='w')
logger = logging.getLogger()

# Main function
async def main():
    from handlers import dp
    # Start bot
    try:
        logger.info("INFO: Bot started!")
        await dp.skip_updates()
        await dp.start_polling(dp) 
    # Stop bot
    finally:
        logger.info("INFO: Stopping bot...") 
        quit()
    
# Start point
if __name__ == "__main__":
    logger.info("INFO: Starting bot...")
    try:
        asyncio.run(main())
    # Exit on ctrl + c/close console/...
    except (KeyboardInterrupt, SystemExit): 
        logger.info("INFO: Bot stopped")
        print("Bot stopped!")

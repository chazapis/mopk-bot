# Copyright 2024 Antony Chazapis
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import dotenv
import discord
import time
import logging

# Setup logging
logger = logging.getLogger('bot')
logger.setLevel(logging.INFO)
discord.utils.setup_logging()

# Get environment
dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('DISCORD_CHANNEL')
if not TOKEN or not GUILD or not CHANNEL:
    logger.error(f'Missing environment... Exiting')
    sys.exit(1)

# Setup GPIO
try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    logger.warning(f'GPIO library not found... Skipping GPIO functionality')
    from nop import NOP
    GPIO = NOP() # Skip for local testing

DOORS = {1: 23, 2: 24} # Door number to GPIO mapping

GPIO.setmode(GPIO.BCM)
for v in DOORS.values():
    GPIO.setup(v, GPIO.OUT)

def open_door(door):
    logger.info(f'Opening door {door}...')
    GPIO.output(DOORS[door], GPIO.HIGH)
    time.sleep(1)
    GPIO.output(DOORS[door], GPIO.LOW)

# Setup Discord client and connect
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    logger.info(f'{client.user} is connected to guild {guild.name}(id: {guild.id}) listening on channel {CHANNEL}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.name != CHANNEL:
        return

    logger.info(f'New message from {message.author}: {message.content}')
    if message.content == 'open 1':
        await message.channel.send('opening 1!')
        open_door(1)
    elif message.content == 'open 2':
        await message.channel.send('opening 2!')
        open_door(2)

client.run(TOKEN, log_handler=None) # Disable double logging

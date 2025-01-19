import asyncio
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

TELEGRAM_BOT_TOKEN = '7819992909:AAHn51FAfPId42gmKUT5wPmCoyC4_g9OeN0'
ADMIN_USER_ID = 1662672529
APPROVED_IDS_FILE = 'approved_ids.txt'
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

approved_ids = load_approved_ids()

# Start command
async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (
        "*𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐁𝐎𝐓*\n"
        "*OWNER :- @GODxAloneBOY*\n"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

# Approve command to approve users and group chat IDs
async def approve(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You need admin permission to use this command.*", parse_mode='Markdown')
        return

    if len(args) != 1:
        await context.bot.send_message(chat_id=chat_id, text="* Usage » /approve id (user or group chat ID)*", parse_mode='Markdown')
        return

    target_id = args[0].strip()
    approved_ids.add(target_id)
    save_approved_ids(approved_ids)
    await context.bot.send_message(chat_id=chat_id, text=f"*✅ ID {target_id} approved.*", parse_mode='Markdown')

# Remove command to remove approved users and group chat IDs
async def remove(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You need admin permission to use this command.*", parse_mode='Markdown')
        return

    if len(args) != 1:
        await context.bot.send_message(chat_id=chat_id, text="* Usage » /remove id (user or group chat ID)*", parse_mode='Markdown')
        return

    target_id = args[0].strip()
    if target_id in approved_ids:
        approved_ids.discard(target_id)
        save_approved_ids(approved_ids)
        await context.bot.send_message(chat_id=chat_id, text=f"*✅ ID {target_id} removed.*", parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ ID {target_id} is not approved.*", parse_mode='Markdown')

# Clone command
async def clone(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    # Only the admin can use this command
    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(
            chat_id=chat_id,
            text="*⚠️ You need admin permission to use this command.*",
            parse_mode='Markdown'
        )
        return

    # Ensure the bot token is provided
    if len(args) != 1:
        await context.bot.send_message(
            chat_id=chat_id,
            text="* Usage » /clone <new_bot_token>*",
            parse_mode='Markdown'
        )
        return

    new_bot_token = args[0].strip()  # Get the new bot token from arguments

    try:
        # Path for the cloned bot
        clone_path = "./bot_clone"
        if not os.path.exists(clone_path):
            os.makedirs(clone_path)

        # Copy the current bot files to the cloned directory
        os.system(f"cp -r ./ {clone_path}")

        # Replace the token in the cloned bot's code
        with open(os.path.join(clone_path, "bot.py"), "r") as file:
            bot_code = file.read().replace(TELEGRAM_BOT_TOKEN, new_bot_token)

        with open(os.path.join(clone_path, "bot.py"), "w") as file:
            file.write(bot_code)

        # Run the cloned bot
        os.system(f"nohup python3 {os.path.join(clone_path, 'bot.py')} &")

        await context.bot.send_message(
            chat_id=chat_id,
            text="*✅ Bot cloned and deployed successfully with the new token.*",
            parse_mode='Markdown'
        )

    except Exception as e:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"*⚠️ Error cloning bot: {str(e)}*",
            parse_mode='Markdown'
        )

# Main function
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("approve", approve))
    application.add_handler(CommandHandler("remove", remove))
    application.add_handler(CommandHandler("clone", clone))
    application.run_polling()

if __name__ == '__main__':
    main()

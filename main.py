import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ================== CONFIG ==================
TOKEN = "8576842606:AAHHBGhubXY4LQ1XejUb1bSCXK4cbPEoAhw"
ADMIN_ID = 6103530574
DATA_FILE = "users.json"

# ================== DATA LOAD ==================
try:
    with open(DATA_FILE, "r") as f:
        users = json.load(f)
except:
    users = {}

used_transactions = []

LEVEL_COMMISSION = {1:60, 2:20, 3:5, 4:2.5, 5:1}
ACTIVATION_BONUS = 60
WITHDRAW_CONDITIONS = {250:3, 500:6, 750:9, 1000:12, 2000:24}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

# ================== START / MENU ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    # New user create
    if user_id not in users:
        users[user_id] = {
            "balance": 0,
            "active": False,
            "referrer": None,
            "refs": 0,
            "joined": True
        }

        # Referral system (safe)
        if context.args:
            ref_id = context.args[0]

            # ❌ Self referral block
            if ref_id == user_id:
                pass

            # ✅ Only valid user referral
            elif ref_id in users:
                users[user_id]["referrer"] = ref_id
                users[ref_id]["refs"] += 1

        save_data()

    keyboard = [
        [InlineKeyboardButton("💰 My Balance", callback_data="balance")],
        [InlineKeyboardButton("👥 Referral Link", callback_data="referral")],
        [InlineKeyboardButton("🔹 Activate Account (100৳)", callback_data="activate")],
        [InlineKeyboardButton("💵 Withdraw", callback_data="withdraw")],
        [InlineKeyboardButton("🎯 Tasks", callback_data="tasks")]
    ]

    await update.message.reply_text(
        "🚀 Welcome to Refer Earn Pro Bot!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
        [InlineKeyboardButton("💰 My Balance", callback_data="balance")],
        [InlineKeyboardButton("👥 My Referral Link", callback_data="referral")],
        [InlineKeyboardButton("🔹 Activate Account (100৳)", callback_data="activate")],
        [InlineKeyboardButton("💵 Withdraw", callback_data="withdraw")],
        [InlineKeyboardButton("🎯 Tasks", callback_data="tasks")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to Refer Earn Bot!", reply_markup=reply_markup)

# ================== BUTTON HANDLER ==================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = str(query.from_user.id)
    await query.answer()
    user = users.get(user_id)

    if query.data == "balance":
        status = "Active" if user.get("active") else "Free"
        await query.edit_message_text(
            f"💰 Balance: {user.get('balance',0)}৳\nStatus: {status}\nTotal Referrals: {user.get('refs',0)}"
        )

    elif query.data == "referral":
        bot_username = context.bot.username
        referral_link = f"https://t.me/{bot_username}?start={user_id}"
        await query.edit_message_text(f"👥 Your Referral Link:\n{referral_link}")

    elif query.data == "activate":
        if user.get("active"):
            await query.edit_message_text("✅ Account Already Active.")
        else:
            await query.edit_message_text(
                "💳 Activation Fee: 100৳\nSend Money to: 01944545512\n"
                "তারপর লিখো:\n/activate <mobile_number> <transaction_id>"
            )

    elif query.data == "withdraw":
        if not user.get("active"):
            await query.edit_message_text("❌ Free account cannot withdraw.")
            return
        text = "💵 Withdraw Options:\n\n"
        for amount, refs in WITHDRAW_CONDITIONS.items():
            text += f"{amount}৳ → {refs} Referrals\n"
        text += "\nUse: /withdraw <amount> <transaction_id>"
        await query.edit_message_text(text)

    elif query.data == "tasks":
        keyboard = [
            [InlineKeyboardButton("📘 Facebook Task", callback_data="fb_task")],
            [InlineKeyboardButton("▶️ YouTube Task", callback_data="yt_task")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]
        await query.edit_message_text("🎯 Complete Tasks & Earn Bonus", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "fb_task":
        keyboard = [
            [InlineKeyboardButton("🔗 Open Facebook", url="https://www.facebook.com/profile.php?id=61587170180010")],
            [InlineKeyboardButton("✅ Done", callback_data="fb_done")],
            [InlineKeyboardButton("🔙 Back", callback_data="tasks")]
        ]
        await update.callback_query.edit_message_text("📘 Follow Facebook then press Done", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "yt_task":
        keyboard = [
            [InlineKeyboardButton("🔗 Open YouTube", url="https://www.youtube.com/@rafferalprosidebd")],
            [InlineKeyboardButton("✅ Done", callback_data="yt_done")],
            [InlineKeyboardButton("🔙 Back", callback_data="tasks")]
        ]
        await update.callback_query.edit_message_text("▶️ Subscribe YouTube then press Done", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "fb_done":
        if "tasks_done" not in user:
            user["tasks_done"] = []
        if "facebook" in user["tasks_done"]:
            await update.callback_query.edit_message_text("❌ Facebook Task Already Completed.")
        else:
            user["balance"] += 10
            user["tasks_done"].append("facebook")
            save_data()
            await update.callback_query.edit_message_text("✅ Facebook Task Completed!\n💰 10৳ Added.")

    elif query.data == "yt_done":
        if "tasks_done" not in user:
            user["tasks_done"] = []
        if "youtube" in user["tasks_done"]:
            await update.callback_query.edit_message_text("❌ YouTube Task Already Completed.")
        else:
            user["balance"] += 10
            user["tasks_done"].append("youtube")
            save_data()
            await update.callback_query.edit_message_text("✅ YouTube Task Completed!\n💰 10৳ Added.")

    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("💰 My Balance", callback_data="balance")],
            [InlineKeyboardButton("👥 My Referral Link", callback_data="referral")],
            [InlineKeyboardButton("🔹 Activate Account (100৳)", callback_data="activate")],
            [InlineKeyboardButton("💵 Withdraw", callback_data="withdraw")],
            [InlineKeyboardButton("🎯 Tasks", callback_data="tasks")]
        ]
        await update.callback_query.edit_message_text("Welcome to Refer Earn Bot!", reply_markup=InlineKeyboardMarkup(keyboard))

# ================== ACTIVATE COMMAND ==================
async def activate_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    if len(context.args) != 2:
        await update.message.reply_text("Use:\n/activate <mobile_number> <transaction_id>")
        return
    mobile, trx_id = context.args
    if trx_id in used_transactions:
        await update.message.reply_text("❌ Transaction ID already used.")
        return
    user = users.get(user_id)
    if user["active"]:
        await update.message.reply_text("✅ Already Activated.")
        return
    # Activate user
    user["active"] = True
    user["balance"] += ACTIVATION_BONUS
    used_transactions.append(trx_id)
    # 5 Level Commission
    level_rewards = [60, 20, 5, 2.5, 1]
    current_ref = user.get("referrer")
    for level in range(5):
        if current_ref and current_ref in users:
            users[current_ref]["balance"] += level_rewards[level]
            users[current_ref]["refs"] += 1
            current_ref = users[current_ref].get("referrer")
        else:
            break
    save_data()
    await update.message.reply_text("✅ Account Activated!\n🎁 60৳ Bonus Added.\n💸 5 Level Commission Distributed.")

# ================== WITHDRAW COMMAND ==================
async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    if len(context.args) != 2:
        await update.message.reply_text("Use: /withdraw <amount> <transaction_id>")
        return
    amount, trx_id = int(context.args[0]), context.args[1]
    user = users.get(user_id)
    if not user.get("active"):
        await update.message.reply_text("❌ Activate first to withdraw.")
        return
    if trx_id in used_transactions:
        await update.message.reply_text("❌ Transaction ID already used.")
        return
    required_refs = WITHDRAW_CONDITIONS.get(amount)
    if not required_refs:
        await update.message.reply_text("❌ Invalid withdraw amount.")
        return
    if user["refs"] < required_refs:
        await update.message.reply_text(f"❌ You need {required_refs} referrals for {amount}৳ withdraw.")
        return
    if user["balance"] < amount:
        await update.message.reply_text("❌ Insufficient balance.")
        return
    # Auto-approve
    user["balance"] -= amount
    used_transactions.append(trx_id)
    save_data()
    await update.message.reply_text(f"✅ Withdraw approved for {amount}৳\nTransaction ID: {trx_id}")

# ================== ADMIN COMMAND ==================
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not admin.")
        return
    text = "📊 Users Summary:\n\n"
    for uid, data in users.items():
        status = "Active" if data.get("active") else "Free"
        text += f"ID: {uid}, Balance: {data.get('balance',0)}, Status: {status}, Refs: {data.get('refs',0)}\n"
    await update.message.reply_text(text)

# ================== BOT SETUP ==================
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("activate", activate_cmd))
app.add_handler(CommandHandler("withdraw", withdraw))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CallbackQueryHandler(button_handler))

print("Bot is running...")
app.run_polling()

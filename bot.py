import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

TOKEN = os.environ.get("BOT_TOKEN")

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📚 Learn Rules", callback_data="rules")],
        [InlineKeyboardButton("🏃 Positions", callback_data="positions")],
        [InlineKeyboardButton("⚽ Drills", callback_data="drills")],
        [InlineKeyboardButton("🧠 Quiz", callback_data="quiz")],
    ]
    update.message.reply_text(
        "⚽ Welcome to *Footy Academia!*\n\nYour personal football coach!\nWhat do you want to learn?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

POSITIONS = {
    "pos_gk": "🥅 *Goalkeeper*\nLast line of defense.\n\n💡 Always stay between ball and goal.",
    "pos_def": "🛡 *Defender*\nStop attackers.\n\n💡 Stay on your feet, stay goal-side.",
    "pos_mid": "⚙️ *Midfielder*\nEngine of the team.\n\n💡 Look up before receiving the ball.",
    "pos_st": "🎯 *Striker*\nScore goals!\n\n💡 Time your runs behind the defense.",
}

DRILLS = {
    "drill_beginner": "🟢 *Beginner*\n\n1. Ball juggling\n2. Cone dribbling\n3. Wall passing\n4. Shooting practice",
    "drill_inter": "🟡 *Intermediate*\n\n1. 1v1 defending\n2. Rondo 4v1\n3. First touch drills\n4. Crossing & finishing",
    "drill_advanced": "🔴 *Advanced*\n\n1. Team pressing\n2. Combination play\n3. Set pieces\n4. 5v5 games",
}

quiz_data = [
    {"q": "How many players per team?", "opts": ["9","10","11","12"], "ans": "11"},
    {"q": "What is a yellow card?", "opts": ["Goal","Warning","Red card","Penalty"], "ans": "Warning"},
    {"q": "How long is a match?", "opts": ["60 mins","75 mins","90 mins","120 mins"], "ans": "90 mins"},
]

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    if data == "rules":
        query.message.reply_text(
            "📚 *Rules*\n\n1️⃣ 11 players\n2️⃣ 90 mins\n3️⃣ No hands\n"
            "4️⃣ Offside rule\n5️⃣ Fouls = free kicks\n6️⃣ Yellow/Red cards\n7️⃣ Most goals wins!",
            parse_mode="Markdown"
        )
    elif data == "positions":
        keyboard = [
            [InlineKeyboardButton("🥅 Goalkeeper", callback_data="pos_gk")],
            [InlineKeyboardButton("🛡 Defender", callback_data="pos_def")],
            [InlineKeyboardButton("⚙️ Midfielder", callback_data="pos_mid")],
            [InlineKeyboardButton("🎯 Striker", callback_data="pos_st")],
        ]
        query.message.reply_text("Choose a position:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "drills":
        keyboard = [
            [InlineKeyboardButton("🟢 Beginner", callback_data="drill_beginner")],
            [InlineKeyboardButton("🟡 Intermediate", callback_data="drill_inter")],
            [InlineKeyboardButton("🔴 Advanced", callback_data="drill_advanced")],
        ]
        query.message.reply_text("Choose your level:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "quiz":
        context.user_data["qi"] = 0
        context.user_data["qs"] = 0
        send_question(query.message, context)
    elif data in POSITIONS:
        query.message.reply_text(POSITIONS[data], parse_mode="Markdown")
    elif data in DRILLS:
        query.message.reply_text(DRILLS[data], parse_mode="Markdown")
    elif data.startswith("quiz_"):
        ans = data.replace("quiz_", "")
        idx = context.user_data.get("qi", 0)
        correct = quiz_data[idx]["ans"]
        if ans == correct:
            context.user_data["qs"] = context.user_data.get("qs", 0) + 1
            query.message.reply_text("✅ Correct!")
        else:
            query.message.reply_text(f"❌ Wrong! Answer: *{correct}*", parse_mode="Markdown")
        context.user_data["qi"] = idx + 1
        send_question(query.message, context)

def send_question(message, context):
    idx = context.user_data.get("qi", 0)
    if idx >= len(quiz_data):
        score = context.user_data.get("qs", 0)
        message.reply_text(
            f"🏁 *Quiz Done!* Score: *{score}/{len(quiz_data)}*\n\n" +
            ("🏆 Perfect!" if score == len(quiz_data) else "💪 Try again with /start"),
            parse_mode="Markdown"
        )
        return
    q = quiz_data[idx]
    keyboard = [[InlineKeyboardButton(o, callback_data=f"quiz_{o}")] for o in q["opts"]]
    message.reply_text(
        f"🧠 *Q{idx+1}: {q['q']}*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
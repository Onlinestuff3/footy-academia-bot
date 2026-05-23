import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 Learn Rules", callback_data="rules")],
        [InlineKeyboardButton("🏃 Positions", callback_data="positions")],
        [InlineKeyboardButton("⚽ Drills & Training", callback_data="drills")],
        [InlineKeyboardButton("🧠 Take a Quiz", callback_data="quiz")],
    ]
    await update.message.reply_text(
        "⚽ Welcome to *Footy Academia!*\n\nYour personal football coach.\nWhat do you want to learn today?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

POSITION_INFO = {
    "pos_gk": "🥅 *Goalkeeper*\nLast line of defense. Great reflexes, commanding presence.\n\n💡 Always position between ball and goal.",
    "pos_def": "🛡 *Defender*\nStops attackers. Key skills: tackling, heading, positioning.\n\n💡 Stay on your feet and stay goal-side.",
    "pos_mid": "⚙️ *Midfielder*\nEngine of the team. Needs stamina, passing, vision.\n\n💡 Always look up before receiving the ball.",
    "pos_st": "🎯 *Striker*\nThe goal scorer! Needs finishing and composure.\n\n💡 Time your runs behind the defense.",
}

DRILL_INFO = {
    "drill_beginner": "🟢 *Beginner Drills*\n\n1. Ball Juggling - keep ball in air\n2. Cone Dribbling - dribble through 5 cones\n3. Wall Passing - pass against wall 10 mins\n4. Shooting - aim for corners from 12 yards",
    "drill_inter": "🟡 *Intermediate Drills*\n\n1. 1v1 defending in small zone\n2. Rondo 4v1 - keep ball from middle player\n3. First touch control - chest/thigh/foot\n4. Crossing and finishing drills",
    "drill_advanced": "🔴 *Advanced Drills*\n\n1. Pressing triggers as a team unit\n2. Combination play at speed\n3. Set pieces - corners and free kicks\n4. 5v5 small-sided high intensity games",
}

quiz_questions = [
    {"q": "How many players on a football team?", "options": ["9", "10", "11", "12"], "answer": "11"},
    {"q": "What does a yellow card mean?", "options": ["Goal", "Warning", "Sent off", "Penalty"], "answer": "Warning"},
    {"q": "How long is a standard match?", "options": ["60 mins", "75 mins", "90 mins", "120 mins"], "answer": "90 mins"},
]

async def send_quiz_question(message, context):
    idx = context.user_data.get("quiz_index", 0)
    if idx >= len(quiz_questions):
        score = context.user_data.get("quiz_score", 0)
        await message.reply_text(
            f"🏁 *Quiz Complete!*\nScore: *{score}/{len(quiz_questions)}*\n\n" +
            ("🏆 Perfect!" if score == len(quiz_questions) else "💪 Keep practicing! /quiz to retry."),
            parse_mode="Markdown"
        )
        return
    q = quiz_questions[idx]
    keyboard = [[InlineKeyboardButton(opt, callback_data=f"quiz_{opt}")] for opt in q["options"]]
    await message.reply_text(
        f"🧠 *Q{idx+1}: {q['q']}*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "rules":
        await query.message.reply_text(
            "📚 *Football Rules*\n\n1️⃣ 11 players per team\n2️⃣ 90 minute match\n"
            "3️⃣ No hands except GK\n4️⃣ Offside rule applies\n"
            "5️⃣ Fouls = free kicks\n6️⃣ 🟡 Yellow / 🔴 Red cards\n7️⃣ Most goals wins!",
            parse_mode="Markdown"
        )
    elif data == "positions":
        keyboard = [
            [InlineKeyboardButton("🥅 Goalkeeper", callback_data="pos_gk")],
            [InlineKeyboardButton("🛡 Defender", callback_data="pos_def")],
            [InlineKeyboardButton("⚙️ Midfielder", callback_data="pos_mid")],
            [InlineKeyboardButton("🎯 Striker", callback_data="pos_st")],
        ]
        await query.message.reply_text("Choose a position:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "drills":
        keyboard = [
            [InlineKeyboardButton("🟢 Beginner", callback_data="drill_beginner")],
            [InlineKeyboardButton("🟡 Intermediate", callback_data="drill_inter")],
            [InlineKeyboardButton("🔴 Advanced", callback_data="drill_advanced")],
        ]
        await query.message.reply_text("Choose your level:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "quiz":
        context.user_data["quiz_index"] = 0
        context.user_data["quiz_score"] = 0
        await send_quiz_question(query.message, context)
    elif data in POSITION_INFO:
        await query.message.reply_text(POSITION_INFO[data], parse_mode="Markdown")
    elif data in DRILL_INFO:
        await query.message.reply_text(DRILL_INFO[data], parse_mode="Markdown")
    elif data.startswith("quiz_"):
        answer = data.replace("quiz_", "")
        idx = context.user_data.get("quiz_index", 0)
        correct = quiz_questions[idx]["answer"]
        if answer == correct:
            context.user_data["quiz_score"] = context.user_data.get("quiz_score", 0) + 1
            await query.message.reply_text("✅ Correct!")
        else:
            await query.message.reply_text(f"❌ Wrong! Answer: *{correct}*", parse_mode="Markdown")
        context.user_data["quiz_index"] = idx + 1
        await send_quiz_question(query.message, context)

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    await app.initialize()
    await app.start()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
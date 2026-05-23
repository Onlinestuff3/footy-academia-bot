import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)

TOKEN = os.environ.get("BOT_TOKEN")

# ── /start ──────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 Learn Rules", callback_data="rules")],
        [InlineKeyboardButton("🏃 Positions", callback_data="positions")],
        [InlineKeyboardButton("⚽ Drills & Training", callback_data="drills")],
        [InlineKeyboardButton("🧠 Take a Quiz", callback_data="quiz")],
        [InlineKeyboardButton("📊 Choose My Level", callback_data="level")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "⚽ Welcome to *Footy Academia!*\n\nYour personal football coach.\nWhat do you want to learn today?",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# ── RULES ────────────────────────────────────────────────
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📚 *Basic Football Rules*\n\n"
        "1️⃣ Two teams of 11 players each\n"
        "2️⃣ Match is 90 mins (2x45)\n"
        "3️⃣ Use feet — no hands (except GK)\n"
        "4️⃣ *Offside:* You can't be behind the last defender when the ball is played to you\n"
        "5️⃣ *Foul:* Illegal tackle = free kick\n"
        "6️⃣ 🟡 Yellow = warning | 🔴 Red = sent off\n"
        "7️⃣ Most goals wins!\n\n"
        "Type /positions to learn player roles."
    )
    await update.message.reply_text(text, parse_mode="Markdown")

# ── POSITIONS ────────────────────────────────────────────
async def positions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🥅 Goalkeeper", callback_data="pos_gk")],
        [InlineKeyboardButton("🛡 Defender", callback_data="pos_def")],
        [InlineKeyboardButton("⚙️ Midfielder", callback_data="pos_mid")],
        [InlineKeyboardButton("🎯 Striker", callback_data="pos_st")],
    ]
    await update.message.reply_text(
        "🏃 *Choose a position to learn about:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ── DRILLS ───────────────────────────────────────────────
async def drills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🟢 Beginner Drills", callback_data="drill_beginner")],
        [InlineKeyboardButton("🟡 Intermediate Drills", callback_data="drill_inter")],
        [InlineKeyboardButton("🔴 Advanced Drills", callback_data="drill_advanced")],
    ]
    await update.message.reply_text(
        "⚽ *Choose your level for drills:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ── QUIZ ─────────────────────────────────────────────────
quiz_questions = [
    {
        "q": "How many players are on a football team?",
        "options": ["9", "10", "11", "12"],
        "answer": "11"
    },
    {
        "q": "What does a yellow card mean?",
        "options": ["Goal", "Warning", "Sent off", "Penalty"],
        "answer": "Warning"
    },
    {
        "q": "How long is a standard football match?",
        "options": ["60 mins", "75 mins", "90 mins", "120 mins"],
        "answer": "90 mins"
    },
]

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["quiz_index"] = 0
    context.user_data["quiz_score"] = 0
    await send_question(update, context)

async def send_question(update, context):
    idx = context.user_data.get("quiz_index", 0)
    if idx >= len(quiz_questions):
        score = context.user_data.get("quiz_score", 0)
        total = len(quiz_questions)
        await update.message.reply_text(
            f"🏁 Quiz done! You scored *{score}/{total}*\n\n"
            + ("⭐ Excellent!" if score == total else "Keep practicing! /quiz to try again"),
            parse_mode="Markdown"
        )
        return
    q = quiz_questions[idx]
    keyboard = [[InlineKeyboardButton(opt, callback_data=f"quiz_{opt}")] for opt in q["options"]]
    await update.message.reply_text(
        f"🧠 *Q{idx+1}: {q['q']}*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ── CALLBACKS ────────────────────────────────────────────
POSITION_INFO = {
    "pos_gk": "🥅 *Goalkeeper*\nLast line of defense. Must have great reflexes, commanding presence, and good with feet.\n\n💡 Tip: Always position yourself between the ball and the goal.",
    "pos_def": "🛡 *Defender*\nStops attackers from scoring. Key skills: tackling, heading, positioning.\n\n💡 Tip: Don't dive in — stay on your feet and stay goal-side.",
    "pos_mid": "⚙️ *Midfielder*\nThe engine of the team. Links defense to attack. Needs stamina, passing, and vision.\n\n💡 Tip: Always look up before receiving the ball.",
    "pos_st": "🎯 *Striker*\nThe goal scorer! Needs finishing, movement, and composure in front of goal.\n\n💡 Tip: Make runs in behind the defense — time them with the pass.",
}

DRILL_INFO = {
    "drill_beginner": (
        "🟢 *Beginner Drills*\n\n"
        "1. *Ball Juggling* — Keep the ball in the air using feet, knees, chest. Start with 1 touch.\n"
        "2. *Cone Dribbling* — Set 5 cones in a line, dribble through slowly.\n"
        "3. *Wall Passing* — Pass against a wall and control the return. 10 mins daily.\n"
        "4. *Shooting Practice* — Place ball 12 yards from goal, aim for corners."
    ),
    "drill_inter": (
        "🟡 *Intermediate Drills*\n\n"
        "1. *1v1 defending* — Attacker tries to beat defender in a small zone.\n"
        "2. *Rondo (4v1)* — 4 players keep ball from 1 in the middle.\n"
        "3. *First touch control* — Throw ball up, control with chest/thigh/foot.\n"
        "4. *Crossing & Finishing* — Winger crosses, striker finishes first time."
    ),
    "drill_advanced": (
        "🔴 *Advanced Drills*\n\n"
        "1. *Pressing Triggers* — Team learns when/how to press as a unit.\n"
        "2. *Combination Play* — 3-man passing patterns at speed (one-twos, overlaps).\n"
        "3. *Set Pieces* — Practice corners, free kicks with specific runs.\n"
        "4. *Small-sided games (5v5)* — High intensity, tight spaces, quick decisions."
    ),
}

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "rules":
        await query.message.reply_text(
            "📚 *Basic Football Rules*\n\n"
            "1️⃣ Two teams of 11 players\n2️⃣ 90 minute match\n"
            "3️⃣ No hands (except GK)\n4️⃣ Offside rule applies\n"
            "5️⃣ Fouls = free kicks\n6️⃣ 🟡 Yellow / 🔴 Red cards\n"
            "7️⃣ Most goals wins!",
            parse_mode="Markdown"
        )
    elif data == "positions":
        keyboard = [
            [InlineKeyboardButton("🥅 Goalkeeper", callback_data="pos_gk")],
            [InlineKeyboardButton("🛡 Defender", callback_data="pos_def")],
            [InlineKeyboardButton("⚙️ Midfielder", callback_data="pos_mid")],
            [InlineKeyboardButton("🎯 Striker", callback_data="pos_st")],
        ]
        await query.message.reply_text(
            "🏃 *Choose a position:*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data == "drills":
        keyboard = [
            [InlineKeyboardButton("🟢 Beginner", callback_data="drill_beginner")],
            [InlineKeyboardButton("🟡 Intermediate", callback_data="drill_inter")],
            [InlineKeyboardButton("🔴 Advanced", callback_data="drill_advanced")],
        ]
        await query.message.reply_text(
            "⚽ *Choose your level:*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
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
            await query.message.reply_text(f"❌ Wrong! The answer was *{correct}*", parse_mode="Markdown")
        context.user_data["quiz_index"] = idx + 1
        await send_quiz_question(query.message, context)

async def send_quiz_question(message, context):
    idx = context.user_data.get("quiz_index", 0)
    if idx >= len(quiz_questions):
        score = context.user_data.get("quiz_score", 0)
        await message.reply_text(
            f"🏁 *Quiz Complete!*\nScore: *{score}/{len(quiz_questions)}*\n\n"
            + ("🏆 Perfect score!" if score == len(quiz_questions) else "💪 Keep practicing! Use /quiz to retry."),
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

# ── MAIN ─────────────────────────────────────────────────
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(CommandHandler("positions", positions))
    app.add_handler(CommandHandler("drills", drills))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Footy Academia bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
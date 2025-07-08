‎
‎
‎```python
‎import openai
‎import requests
‎from telegram import Update, ReplyKeyboardMarkup
‎from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
‎from apscheduler.schedulers.background import BackgroundScheduler
‎
‎# === CONFIGURATION ===
‎TELEGRAM_BOT_TOKEN = "8141332488:AAFxCMsY4MZS-Yy_OADJjRvvvmNbBbThBNs"
‎OPENAI_API_KEY = "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"
‎SPORTS_API_KEY = "50b91d3cd0de1db0e39f8fe52d990406"
‎CANAL_ID = "@YMBG Infos Pronos Sport"
‎GROUP_ID = -1002712500298  # Groupe Telegram des usagers
‎
‎openai.api_key = OPENAI_API_KEY
‎
‎# === COMMANDES ===
‎def start(update: Update, context: CallbackContext):
‎    keyboard = [['/affiche', '/pronostic'], ['/strategie', '/infos']]
‎    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
‎    update.message.reply_text("🎯 Bienvenue sur YMB Bot!", reply_markup=reply_markup)
‎
‎def handle_text(update: Update, context: CallbackContext):
‎    text = update.message.text.lower()
‎    if text == "/affiche":
‎        update.message.reply_text(get_today_matches())
‎    else:
‎        update.message.reply_text(ask_openai(text))
‎
‎def ask_openai(prompt):
‎    response = openai.ChatCompletion.create(
‎        model="gpt-4",
‎        messages=[{"role": "user", "content": prompt}]
‎)
‎    return response.choices[0].message.content.strip()
‎
‎def get_today_matches():
‎    url = "https://v3.football.api-sports.io/fixtures?date=today"
‎    headers = {"x-apisports-key": SPORTS_API_KEY}
‎    response = requests.get(url, headers=headers)
‎    data = response.json()
‎    if not data['response']:
‎        return "Aucun match prévu aujourd'hui."
‎    matches = []
‎    for match in data['response'][:10]:
‎        teams = match['teams']
‎        time = match['fixture']['date'][11:16]
‎        matches.append(f"{time} – {teams['home']['name']} vs {teams['away']['name']}")
‎    return "\n".join(matches)
‎
‎def schedule_daily_post(bot):
‎    scheduler = BackgroundScheduler()
‎    def post():
‎        prompt = "Donne deux pronostics sportifs pour aujourd'hui avec analyse."
‎        message = ask_openai(prompt)
‎        # Publication dans le canal
‎        bot.send_message(chat_id=CANAL_ID, text=message)
‎        # Publication dans le groupe
‎        bot.send_message(chat_id=GROUP_ID, text=message)
‎    scheduler.add_job(post, 'cron', hour=7, minute=30)
‎    scheduler.start()
‎
‎# === LANCEMENT DU BOT ===
‎def main():
‎    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
‎    dp = updater.dispatcher
‎    dp.add_handler(CommandHandler("start", start))
‎    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
‎    schedule_daily_post(updater.bot)
‎    updater.start_polling()
‎    updater.idle()
‎
‎if __name__ == "__main__":
‎    main()
‎```
‎
‎

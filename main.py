"""
Main entry point for the Steam Reviews Sentiment Analysis Telegram Bot.
"""

import telebot
from config import BOT_TOKEN

# Import refactored modules
from steam_api import get_steam_reviews, get_game_name, SteamError
from analyzer import analyze_reviews
from visualizer import generate_charts

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    """
    Send a welcome message explaining the bot's functionality to the user.
    """
    welcome_text = (
        "👋 *Привет! Я бот для анализа отзывов Steam.*\n\n"
        "Отправьте мне числовой идентификатор игры (AppID), и я:\n"
        "1. Скачаю последние 100 англоязычных отзывов через Steam API.\n"
        "2. Проведу NLP-анализ тональности с помощью TextBlob.\n"
        "3. Посчитаю частоту ключевых слов (bug, lag, fun, story, optimization).\n"
        "4. Построю красивые графики распределения.\n\n"
        "📌 *Пример:* отправьте `730` для анализа CS:GO/CS2."
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def handle_appid(message):
    """
    Handle the AppID sent by the user, fetch reviews, analyze them,
    generate charts, and reply with a formatted report.
    """
    text = message.text.strip()

    if not text.isdigit():
        bot.reply_to(
            message,
            "⚠️ Пожалуйста, введите корректный числовой AppID игры в Steam (например, 730).",
        )
        return

    # Step 1: Get game name
    game_name = get_game_name(text)
    status_msg = (
        f"⌛ Получение и анализ отзывов для игры *{game_name}* " f"(AppID {text})..."
    )
    bot.reply_to(message, status_msg, parse_mode="Markdown")

    try:
        # Step 2: Fetch reviews
        reviews = get_steam_reviews(text)

        # Step 3: Run NLP analysis
        sentiment, pos_keywords, neg_keywords = analyze_reviews(reviews)

        # Step 4: Generate visual charts
        chart_img = generate_charts(sentiment, pos_keywords, neg_keywords)

        # Step 5: Format the Russian text report
        total_reviews = sum(
            [sentiment["Positive"], sentiment["Neutral"], sentiment["Negative"]]
        )
        report_caption = (
            f"🎮 *Игра:* {game_name} (ID: {text})\n"
            f"📊 *Всего проанализировано отзывов:* {total_reviews}\n\n"
            f"🔮 *Тональность (Sentiment):*\n"
            f"• 😊 Положительные: {sentiment['Positive']}\n"
            f"• 😐 Нейтральные: {sentiment['Neutral']}\n"
            f"• 😡 Отрицательные: {sentiment['Negative']}\n\n"
            f"📈 *Соотношение (без учета нейтральных):*\n"
            f"• 👍 Одобрение: {sentiment['pos_ratio']}%\n"
            f"• 👎 Критика: {sentiment['neg_ratio']}%\n\n"
            f"🔑 *Частота ключевых слов в отзывах:*\n"
            f"🟩 *В хороших отзывах:*\n"
            f"  • Fun (Веселье): {pos_keywords['fun']}\n"
            f"  • Story (Сюжет): {pos_keywords['story']}\n"
            f"  • Masterpiece (Шедевр): {pos_keywords['masterpiece']}\n"
            f"  • Amazing (Удивительно): {pos_keywords['amazing']}\n"
            f"  • Love (Любовь): {pos_keywords['love']}\n"
            f"🟥 *В плохих отзывах:*\n"
            f"  • Bug (Ошибки): {neg_keywords['bug']}\n"
            f"  • Lag (Задержки): {neg_keywords['lag']}\n"
            f"  • Crash (Вылеты): {neg_keywords['crash']}\n"
            f"  • Waste (Трата денег/времени): {neg_keywords['waste']}\n"
            f"  • Bad (Плохо): {neg_keywords['bad']}\n\n"
            f"🎨 График распределения подготовлен!"
        )

        # Send image with description
        bot.send_photo(
            chat_id=message.chat.id,
            photo=chart_img,
            caption=report_caption,
            parse_mode="Markdown",
            reply_to_message_id=message.message_id,
        )

    except SteamError as e:
        # Clean unified exception handler
        bot.send_message(
            message.chat.id,
            f"❌ *Ошибка при работе со Steam:* {e}",
            parse_mode="Markdown",
        )
    except Exception as e:  # pylint: disable=broad-exception-caught
        # Unanticipated errors
        bot.send_message(
            message.chat.id,
            f"🔥 Произошла критическая ошибка в работе бота.\n*(Детали: {e})*",
        )


if __name__ == "__main__":
    print("Робот запущен... (Ctrl+C для остановки)")
    bot.infinity_polling()

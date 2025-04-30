import requests
import logging
import numpy as np
import talib
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, CallbackContext, filters
import numpy.random  # Импорт для генерации небольших случайных чисел
import sqlite3  # Импорт для работы с SQLite


# ======================================================================
#                       Секция 1: Настройка и Инициализация
#                       Импорты, логирование, языковые настройки
# ======================================================================

# --- Настройка логирования ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# --- Словари с текстами на разных языках ---
TEXTS = {
    'ru': {
        'start_message': "📊 Выберите действие или введите тикер или запрос (например: BTC, 12 SUI USDT, 10 STRK TWT):",
        'help_message_header': "💡 **Как использовать бота:**\n\n",
        'help_message_calculation_header': "**Для расчета стоимости:**\n",
        'help_message_calculation_text': "Введите количество и пару монет, например: `12 SUI USDT` или `0.5 ETH BTC` или `10 STRK TWT`.\n"
        "- Бот вернет стоимость указанного количества первой монеты во второй валюте.\n"
        "- Для USDT пар, цена будет показана в долларах ($).\n"
        "- Для крипто-крипто пар (например, ETH BTC, STRK TWT), цена будет показана во второй криптовалюте.\n\n",
        'help_message_calculation_examples_header': "**Примеры запросов для расчета:**\n",
        'help_message_calculation_examples_text': "- `12 SUI USDT` -  узнать стоимость 12 SUI в долларах США.\n"
        "- `0.5 ETH BTC` - узнать стоимость 0.5 ETH в BTC.\n"
        "- `10 STRK TWT` - узнать стоимость 10 STRK TWT.\n\n",
        'help_message_technical_analysis_header': "**Для получения технического анализа (калькулятор) с разными таймфреймами:**\n",
        'help_message_technical_analysis_text': "Просто введите тикер монеты (например, `BTC`, `ETH`, `SUI`). Бот покажет:\n"
                                                  "- Текущую цену (всегда)\n"
                                                  "- Изменение цены за выбранный таймфрейм в процентах\n"
                                                  "- Торговый сигнал и тренд для выбранного таймфрейма\n"
                                                  "- Кнопки для переключения на технический анализ для таймфреймов: 1ч, 4ч, 12ч, Назад\n"
                                                  "**Вы можете переключить язык бота на английский или русский, нажав соответствующие кнопки ниже.**\n\n",
        'help_message_technical_analysis_features_header': "**Поддерживаемые функции технического анализа:**\n",
        'help_message_technical_analysis_features_text': "- RSI (Индекс относительной силы)\n"
        "- MACD (Схождение/Расхождение Скользящих Средних)\n"
        # Изменено на 30 и 100
        "- EMA (Экспоненциальная скользящая средняя) - 30 и 100 периодов\n"
        "- Bollinger Bands (Полосы Боллинджера)\n"
        "- Stochastic Oscillator (Стохастический осциллятор)\n"
        "- SMA (Простая скользящая средняя) - 20 и 50 периодов\n"
        "- Parabolic SAR (Параболическая система SAR)\n"
        "- ADX (Индекс направленного движения)\n"
        "- Ichimoku Cloud (Облако Ишимоку)\n"
        "- Williams %R (Процентный диапазон Вильямса)\n"
        "- **OBV (On Balance Volume) - Балансовый объем**\n"
        "- Уровни поддержки и сопротивления\n"
        "- Уровни Фибоначчи\n",



        'help_message_other_functions_header': "**Другие функции:**\n",
        'help_message_other_functions_text': "- Раздел 'Топ 10 рост 🚀' и 'Топ 10 падения 📉' показывает лидеров роста и падения на Binance.\n"
                                               "- Раздел 'Помощь' - текущая справка.\n"
                                               "- Раздел 'Donat' - для поддержки разработчика.\n"
                                               "- НЕ ФИНАНСОВАЯ РЕКОМЕНДАЦИЯ.\n",

        'help_message_close_button': "Закрыть",
        'top10_rise_button': "Топ 10 рост 🚀",
        'top10_fall_button': "Топ 10 падения 📉",
        'help_button': "❓ Помощь",
        'donat_button': "💰 Donat",
        'back_button': "Назад",
        'english_button': "English",
        'russian_button': "Русский",
        'top10_rise_header': "🚀 **Топ 10 монет рост (Binance):**\n\n",
        'top10_fall_header': "📉 **Топ 10 монет падения (Binance):**\n\n",
        'binance_data_unavailable_fallback_rise': "⚠️ Binance data unavailable, using CoinGecko trending as fallback for top 10 rising coins:\n\n",
        'binance_data_unavailable_fallback_fall': "⚠️ Binance data unavailable, using CoinGecko trending as fallback for top 10 falling coins:\n\n",
        'error_fetching_top10_rise': "⚠️ Error fetching top 10 rising coins.",
        'error_fetching_top10_fall': "⚠️ Error fetching top 10 falling coins.",
        'price_in_usdt': "{:.5f} $",
        'price_in_crypto': "{:.5f} {}",
        'error_fetching_price_usdt': "⚠️ Error fetching price for {} in USDT",
        'error_fetching_price_crypto': "⚠️ Error fetching price for {} in {}",
        'invalid_input_amount_coin_coin': "⚠️ Invalid input. Please use format: amount COIN1 COIN2 (e.g., 12 SUI USDT or 10 STRK TWT)",
        'invalid_input_amount_coin_coin_index_error': "⚠️ Invalid input. Please use format: amount COIN1 COIN2 (e.g., 12 SUI USDT or 10 STRK TWT)",
        'error_fetching_data': "⚠️ Ошибка получения данных",
        'error_invalid_ticker': " ",  # НОВОЕ сообщение об ошибке
        'price_coin': "💰 **{} Price:** ${:.5f}\n",
        'change_24h': "📈 24h Change: {:.5f}%\n",
        'signal_24h': "🔔 **Signal (24h):** {}\n",
        'trend_24h': "📊 **Trend (24h):** {}",
        'button_1h': "1h",
        'button_4h': "4h",
        'button_12h': "12h",
        'not_enough_historical_data': "⚠️ Not enough historical data for this timeframe.",
        'timeframe_change': "📈 {} Change: {:.5f}%\n",
        'signal_timeframe': "🔔 **Signal ({}):** {}\n",
        'trend_timeframe': "📊 **Trend ({}):** {}",
        'error_fetching_timeframe_data': "⚠️ Error fetching data for timeframe.",
        'donat_message': "🙏 Поддержите разработчика, чтобы бот продолжал радовать вас новыми функциями и улучшениями!\n\n"
                         "₿ **BTC:** `bc1qcategq6gf69ytjz9a8ldavy2yjuc6f67zexsns`\n"
                         "\n"
                         "💲 **USDT (TRC20):** `TYndQoBjYDMn2r4GZ5JqYyS5oJvJ1tYLi7`\n\n"
                         "Спасибо за вашу поддержку!",
        'language_switch_developing': "Функция переключения на английский в разработке!",
        'trend_ascending': "🟢 Восходящий",
        'trend_descending': "🔴 Нисходящий",
        'trend_sideways': "➖ Боковой",
        'trend_strength_strong': " (Сильный)",
        'trend_strength_weak': " (Слабый)",
        'signal_buy': "BUY 📈",
        'signal_sell': "SELL 📉",
        'signal_hold': "HOLD ⚖",
        'interval_1h': '1h',
        'interval_4h': '4h',
        'interval_8h': '8h',
        'interval_12h': '12h',
        'interval_24h': '24h',
        'interval_1d': '24h',
        'interval_change': 'Change',
    },
    'en': {
        'start_message': "📊 Choose an action or enter a ticker or request (e.g., BTC, 12 SUI USDT, 10 STRK TWT):",
        'help_message_header': "💡 **How to use the bot:**\n\n",
        'help_message_calculation_header': "**For price calculation:**\n",
        'help_message_calculation_text': "Enter the amount and coin pair, for example: `12 SUI USDT` or `0.5 ETH BTC` or `10 STRK TWT`.\n"
        "- The bot will return the value of the specified amount of the first coin in the second currency.\n"
        "- For USDT pairs, the price will be shown in dollars ($).\n"
        "- For crypto-crypto pairs (e.g., ETH BTC, STRK TWT), the price will be shown in the second cryptocurrency.\n\n",
        'help_message_calculation_examples_header': "**Examples of calculation requests:**\n",
        'help_message_calculation_examples_text': "- `12 SUI USDT` - find out the cost of 12 SUI in US dollars.\n"
        "- `0.5 ETH BTC` - find out the cost of 0.5 ETH in BTC.\n"
        "- `10 STRK TWT` - find out the cost of 10 STRK TWT.\n\n",
        'help_message_technical_analysis_header': "**To get technical analysis (calculator) with different timeframes:**\n",
        'help_message_technical_analysis_text': "Just enter the coin ticker (e.g., `BTC`, `ETH`, `SUI`). The bot will show:\n"
                                                  "- Current price (always)\n"
                                                  "- Price change for the selected timeframe in percent\n"
                                                  "- Trading signal and trend for the selected timeframe\n"
                                                  "- Buttons to switch to technical analysis for timeframes: 1h, 4h, 12h, Back\n"
                                                  "**You can switch the bot language to English or Russian by pressing the corresponding buttons below.**\n\n",
        'help_message_technical_analysis_features_header': "**Supported technical analysis functions:**\n",
        'help_message_technical_analysis_features_text': "- RSI (Relative Strength Index)\n"
        "- MACD (Moving Average Convergence/Divergence)\n"
        # Изменено на 30 и 100
        "- EMA (Exponential Moving Average) - 30 and 100 periods\n"
        "- Bollinger Bands\n"
        "- Stochastic Oscillator\n"
        "- SMA (Simple Moving Average) - 20 and 50 periods\n"
        "- Parabolic SAR (Parabolic SAR system)\n"
        "- ADX (Average Directional Index)\n"
        "- Ichimoku Cloud\n"
        "- Williams %R (Williams Percent Range)\n"
        "- **OBV (On Balance Volume)**\n"
        "- Support and resistance levels\n"
        "- Fibonacci Levels\n",
        'help_message_other_functions_header': "**Other functions:**\n",
        'help_message_other_functions_text': "- The 'Top 10 Rise 🚀' and 'Top 10 Fall 📉' sections show the top gainers and losers on Binance.\n"
                                               "- The 'Help' section - current help.\n"
                                               "- The 'Donat' section - to support the developer.\n"
                                               "- NOT A FINANCIAL RECOMMENDATION.\n",
        'help_message_close_button': "Close",
        'top10_rise_button': "Top 10 Rise 🚀",
        'top10_fall_button': "Top 10 Fall 📉",
        'help_button': "❓ Help",
        'donat_button': "💰 Donate",
        'back_button': "Back",
        'english_button': "English",
        'russian_button': "Russian",
        'top10_rise_header': "🚀 **Top 10 Rising Coins (Binance):**\n\n",
        'top10_fall_header': "📉 **Top 10 Falling Coins (Binance):**\n\n",
        'binance_data_unavailable_fallback_rise': "⚠️ Binance data unavailable, using CoinGecko trending as fallback for top 10 rising coins:\n\n",
        'binance_data_unavailable_fallback_fall': "⚠️ Binance data unavailable, using CoinGecko trending as fallback for top 10 falling coins:\n\n",
        'error_fetching_top10_rise': "⚠️ Error fetching top 10 rising coins.",
        'error_fetching_top10_fall': "⚠️ Error fetching top 10 falling coins.",
        'price_in_usdt': "{:.5f} $",
        'price_in_crypto': "{:.5f} {}",
        'error_fetching_price_usdt': "⚠️ Error fetching price for {} in USDT",
        'error_fetching_price_crypto': "⚠️ Error fetching price for {} in {}",
        'invalid_input_amount_coin_coin': "⚠️ Invalid input. Please use format: amount COIN1 COIN2 (e.g., 12 SUI USDT or 10 STRK TWT)",
        'invalid_input_amount_coin_coin_index_error': "⚠️ Invalid input. Please use format: amount COIN1 COIN2 (e.g., 12 SUI USDT or 10 STRK TWT)",
        'error_fetching_data': "⚠️ Error fetching data",
        'error_invalid_ticker': "{}  ",  # NEW error message
        'price_coin': "💰 **{} Price:** ${:.5f}\n",
        'change_24h': "📈 24h Change: {:.5f}%\n",
        'signal_24h': "🔔 **Signal (24h):** {}\n",
        'trend_24h': "📊 **Trend (24h):** {}",
        'button_1h': "1h",
        'button_4h': "4h",
        'button_12h': "12h",
        'not_enough_historical_data': "⚠️ Not enough historical data for this timeframe.",
        'timeframe_change': "📈 {} Change: {:.5f}%\n",
        'signal_timeframe': "🔔 **Signal ({}):** {}\n",
        'trend_timeframe': "📊 **Trend ({}):** {}",
        'error_fetching_timeframe_data': "⚠️ Error fetching data for timeframe.",
        'donat_message': "🙏 Support the developer so that the bot continues to delight you with new features and improvements!\n\n"
                         "₿ **BTC:** `bc1qcategq6gf69ytjz9a8ldavy2yjuc6f67zexsns`\n"
                         "\n"
                         "💲 **USDT (TRC20):** `TYndQoBjYDMn2r4GZ5JqYyS5oJvJ1tYLi7`\n\n"
                         "Thank you for your support!",
        'language_switch_developing': "Language switch to English is under development!",
        'trend_ascending': "🟢 Ascending",
        'trend_descending': "🔴 Descending",
        'trend_sideways': "➖ Sideways",
        'trend_strength_strong': " (Strong)",
        'trend_strength_weak': " (Weak)",
        'signal_buy': "BUY 📈",
        'signal_sell': "SELL 📉",
        'signal_hold': "HOLD ⚖",
        'interval_1h': '1h',
        'interval_4h': '4h',
        'interval_8h': '8h',
        'interval_12h': '12h',
        'interval_24h': '24h',
        'interval_1d': '24h',
        'interval_change': 'Change',
    },
}

# --- Глобальная переменная для языка (УДАЛЕНА) ---
# BOT_LANGUAGE = 'ru'  # По умолчанию русский язык (УДАЛЕНО - теперь язык пользователя хранится в БД)


# ======================================================================
#                       Секция 1.1: Работа с базой данных SQLite
# ======================================================================

DATABASE_NAME = 'crypto_bot.db'  # Имя файла базы данных


def create_connection():
    """Создает подключение к базе данных SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
    return conn


def create_tables():
    """Создает таблицы в базе данных, если они не существуют."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Таблица для хранения настроек пользователя (пример)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_settings (
                    user_id INTEGER PRIMARY KEY,
                    language TEXT DEFAULT 'ru',
                    preferred_timeframe TEXT DEFAULT '24h'
                    -- Здесь можно добавить другие настройки пользователя
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database table creation error: {e}")
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")


def get_user_setting(user_id, setting_name):
    """Получает настройку пользователя из базы данных."""
    conn = create_connection()
    setting_value = None
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT {setting_name} FROM user_settings WHERE user_id=?", (user_id,))
            row = cursor.fetchone()
            if row:
                setting_value = row[0]
        except sqlite3.Error as e:
            print(f"Database get setting error: {e}")
        finally:
            conn.close()
    return setting_value


def set_user_setting(user_id, setting_name, setting_value):
    """Устанавливает настройку пользователя в базе данных."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Сначала проверяем, есть ли уже запись для user_id
            cursor.execute(
                "SELECT user_id FROM user_settings WHERE user_id=?", (user_id,))
            existing_user = cursor.fetchone()
            if existing_user:
                # Если пользователь уже есть, обновляем настройку
                cursor.execute(
                    f"UPDATE user_settings SET {setting_name}=? WHERE user_id=?", (setting_value, user_id))
            else:
                # Если пользователя нет, создаем новую запись с настройкой
                cursor.execute(
                    f"INSERT INTO user_settings (user_id, {setting_name}) VALUES (?, ?)", (user_id, setting_value))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database set setting error: {e}")
        finally:
            conn.close()

# Функция для получения языка пользователя (пример использования get_user_setting)


def get_user_language(user_id):
    """Получает язык пользователя из базы данных, по умолчанию 'ru'."""
    language = get_user_setting(user_id, 'language')
    return language if language else 'ru'  # По умолчанию русский

# Функция для установки языка пользователя (пример использования set_user_setting)


def set_user_language(user_id, language):
    """Устанавливает язык пользователя в базе данных."""
    set_user_setting(user_id, 'language', language)


# При запуске бота создаем таблицы, если их нет
create_tables()


# ======================================================================
#                       Секция 2: Функции для работы с Binance API
# ======================================================================

def get_binance_price(coin_id: str):
    """
    Получает 24-часовую сводку по тикеру с Binance API.

    Args:
        coin_id (str): Символ монеты (например, BTC).

    Returns:
        dict: Данные тикера в формате JSON или None в случае ошибки.
    """
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        params = {'symbol': f"{coin_id.upper()}USDT"}
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на HTTP ошибки
        ticker = response.json()
        return ticker
    except requests.exceptions.RequestException as e:
        logger.error(
            f"Binance API error (get_binance_price for {coin_id}): {e}")
        return None


def get_binance_price_direct(coin1_id: str, coin2_id: str):
    """
    Получает цену прямой торговой пары с Binance API.

    Args:
        coin1_id (str): Символ первой монеты (например, ETH).
        coin2_id (str): Символ второй монеты (например, BTC).

    Returns:
        float: Цена торговой пары или None в случае ошибки.
    """
    try:
        symbol = f"{coin1_id.upper()}{coin2_id.upper()}"
        url = "https://api.binance.com/api/v3/ticker/price"
        params = {'symbol': symbol}
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на HTTP ошибки
        price_data = response.json()
        return float(price_data['price'])
    except requests.exceptions.RequestException as e:
        logger.error(
            f"Binance API error (get_binance_price_direct for {coin1_id}-{coin2_id}): {e}")
        return None


def get_binance_top_movers(limit=10, sort_by='priceChangePercent', ascending=False):
    """
    Получает список лидеров роста/падения с Binance API.

    Args:
        limit (int): Максимальное количество монет в списке.
        sort_by (str): Параметр для сортировки ('priceChangePercent', 'volume' и др.).
        ascending (bool): Сортировать по возрастанию (True для падения, False для роста).

    Returns:
        list: Список кортежей с данными о лидерах роста/падения или None в случае ошибки.
              Каждый кортеж содержит (символ, имя, текущая цена, изменение цены за 24ч в процентах).
    """
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        response = requests.get(url)
        response.raise_for_status()  # Проверка на HTTP ошибки
        tickers = response.json()

        # Filter USDT pairs and remove pairs without USDT
        usdt_tickers = [
            ticker for ticker in tickers if ticker['symbol'].endswith('USDT') and ticker['symbol'] != 'USDTUSDT'
        ]

        # Sort tickers
        sorted_tickers = sorted(
            usdt_tickers,
            key=lambda x: float(x[sort_by]),
            # ascending=False for рост (по убыванию), ascending=True для падения (по возрастанию)
            reverse=not ascending
        )

        top_movers = []
        for ticker in sorted_tickers[:limit]:
            symbol = ticker['symbol'].replace('USDT', '')
            top_movers.append((
                symbol,
                symbol,  # Используем символ как имя для совместимости
                float(ticker['lastPrice']),
                float(ticker['priceChangePercent'])
            ))
        return top_movers

    except requests.exceptions.RequestException as e:
        logger.error(f"Binance API error (get_binance_top_movers): {e}")
        return None


# ======================================================================
#                       Секция 3: Функции для работы с CoinGecko API
#                       (Используются как запасной вариант и для точных цен)
# ======================================================================

def get_coingecko_price(coin_id: str, vs_currency='usd'):
    """
    Получает текущую цену монеты с CoinGecko API.

    Args:
        coin_id (str): ID монеты на CoinGecko (например, bitcoin, ethereum).  Важно использовать ID CoinGecko, а не символ.
        vs_currency (str): Валюта, в которой нужно получить цену (по умолчанию 'usd').

    Returns:
        float: Цена монеты в указанной валюте или None в случае ошибки.
    """
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={vs_currency}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if coin_id in data and vs_currency in data[coin_id]:
            return float(data[coin_id][vs_currency])
        else:
            logger.warning(
                f"CoinGecko API: Price not found for {coin_id} in {vs_currency}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(
            f"CoinGecko API error (get_coingecko_price for {coin_id}): {e}")
        return None


def get_coingecko_coin_id_by_symbol(symbol: str):
    """
    Получает CoinGecko Coin ID по символу монеты.

    Args:
        symbol (str): Символ монеты (например, BTC).

    Returns:
        str: CoinGecko Coin ID или None, если не найден.
    """
    try:
        url = f"https://api.coingecko.com/api/v3/coins/list?include_platform=false"
        response = requests.get(url)
        response.raise_for_status()
        coins_list = response.json()
        for coin in coins_list:
            if coin['symbol'].upper() == symbol.upper():  # Сравниваем символы в верхнем регистре
                return coin['id']
        logger.warning(f"CoinGecko API: Coin ID not found for symbol {symbol}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(
            f"CoinGecko API error (get_coingecko_coin_id_by_symbol for {symbol}): {e}")
        return None


def get_trending_coins():
    """
    Получает список трендовых монет с CoinGecko API.

    Returns:
        list: Список кортежей с данными о трендовых монетах или None в случае ошибки.
              Каждый кортеж содержит (символ, имя, цена, изменение цены за 24ч в процентах).
    """
    try:
        url = "https://api.coingecko.com/api/v3/search/trending"
        response = requests.get(url)
        response.raise_for_status()  # Проверка на HTTP ошибки
        data = response.json()
        return [
            (coin["item"]["symbol"].upper(),
             coin["item"]["name"],
             # Convert to float and remove commas
             float(coin["item"]["data"]["price"].replace(',', '')),
             float(coin["item"]["data"]["price_change_percentage_24h"]["usd"]))
            for coin in data["coins"][:10]  # Get top 10 trending coins
        ]
    except requests.exceptions.RequestException as e:
        logger.error(f"CoinGecko API error (get_trending_coins): {e}")
        return None


def get_coingecko_top_movers_fallback(limit=10, sort_by_index=3, ascending=False):
    """
    Использует CoinGecko API как запасной вариант для получения лидеров роста/падения.

    Args:
        limit (int): Максимальное количество монет в списке.
        sort_by_index (int): Индекс в кортеже для сортировки (3 - изменение цены за 24ч в процентах).
        ascending (bool): Сортировать по возрастанию (True для падения, False для роста).

    Returns:
        list: Список кортежей с данными о лидерах роста/падения или None в случае ошибки.
    """
    trending_coins = get_trending_coins()  # Используем трендовые монеты как fallback
    if trending_coins:
        sorted_coins = sorted(
            trending_coins,
            key=lambda x: x[sort_by_index],
            reverse=not ascending
        )
        return sorted_coins[:limit]
    return None


# ======================================================================
#                       Секция 4: Обработчики команд Telegram
#                       (Команды начинающиеся с '/')
# ======================================================================

async def handle_top10_rise(update: Update, context: CallbackContext):
    """Обработчик команды 'Топ 10 рост'."""
    query = update.callback_query
    await query.answer()

    top_risers = get_binance_top_movers(
        sort_by='priceChangePercent', ascending=False)

    if not top_risers:
        top_risers = get_coingecko_top_movers_fallback(
            sort_by_index=3, ascending=False)
        if not top_risers:
            await query.edit_message_text(TEXTS[context.user_data['language']]['error_fetching_top10_rise'])
            return
        else:
            message = TEXTS[context.user_data['language']
                            ]['binance_data_unavailable_fallback_rise']
    else:
        message = TEXTS[context.user_data['language']]['top10_rise_header']

    for coin in top_risers:
        coin_id, coin_name, price, change_24h = coin
        message += (f"📈 **{coin_name} ({coin_id})**: ${price:.5f}\n"
                    f"📈 24h Change: {change_24h:+.5f}%\n\n")

    # ===  Добавляем клавиатуру главного меню ===
    keyboard = [
        [
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['top10_rise_button'], callback_data="TOP10_RISE"),
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['top10_fall_button'], callback_data="TOP10_FALL"),
        ],
        [
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['help_button'], callback_data="HELP"),
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['donat_button'], callback_data="DONAT"),
        ],
        [
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['english_button'], callback_data="LANGUAGE_EN"),
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['russian_button'], callback_data="LANGUAGE_RU"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # ===  Клавиатура главного меню добавлена ===

    # Добавляем reply_markup
    await query.edit_message_text(message, parse_mode="Markdown", reply_markup=reply_markup)


async def handle_top10_fall(update: Update, context: CallbackContext):
    """Обработчик команды 'Топ 10 падения'."""
    query = update.callback_query
    await query.answer()

    top_fallers = get_binance_top_movers(
        sort_by='priceChangePercent', ascending=True)

    if not top_fallers:
        top_fallers = get_coingecko_top_movers_fallback(
            sort_by_index=3, ascending=True)
        if not top_fallers:
            await query.edit_message_text(TEXTS[context.user_data['language']]['error_fetching_top10_fall'])
            return
        else:
            message = TEXTS[context.user_data['language']
                            ]['binance_data_unavailable_fallback_fall']
    else:
        message = TEXTS[context.user_data['language']]['top10_fall_header']

    for coin in top_fallers:
        coin_id, coin_name, price, change_24h = coin
        message += (f"📉 **{coin_name} ({coin_id})**: ${price:.4f}\n"
                    f"📉 24h Change: {change_24h:+.4f}%\n\n")

    # ===  Добавляем клавиатуру главного меню ===
    keyboard = [
        [
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['top10_rise_button'], callback_data="TOP10_RISE"),
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['top10_fall_button'], callback_data="TOP10_FALL"),
        ],
        [
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['help_button'], callback_data="HELP"),
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['donat_button'], callback_data="DONAT"),
        ],
        [
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['english_button'], callback_data="LANGUAGE_EN"),
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['russian_button'], callback_data="LANGUAGE_RU"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # ===  Клавиатура главного меню добавлена ===

    # Добавляем reply_markup
    await query.edit_message_text(message, parse_mode="Markdown", reply_markup=reply_markup)


# ======================================================================
#                       Секция 5: Функции технического анализа
# ======================================================================

def calculate_indicators(prices, high, low, close, volume):
    """
    Вычисляет набор технических индикаторов, включая Swing High/Low.
    """
    if len(prices) < 50:
        return None

    obv_values = talib.OBV(np.array(close), np.array(volume))

    period_for_swing = 20  # Настраиваемый период для определения Swing High/Low

    # Swing High за период
    swing_high = np.max(high[-period_for_swing:]
                        ) if len(high) >= period_for_swing else None
    # Swing Low за период
    swing_low = np.min(low[-period_for_swing:]
                       ) if len(low) >= period_for_swing else None

    indicators = {
        'rsi': talib.RSI(np.array(prices), timeperiod=14)[-1],
        'macd': talib.MACD(np.array(prices))[0][-1],
        'signal': talib.MACD(np.array(prices))[1][-1],
        'ema_30': talib.EMA(np.array(prices), 30)[-1],  # Изменено на 30
        'ema_100': talib.EMA(np.array(prices), 100)[-1],  # Изменено на 100
        'upper_bb': talib.BBANDS(np.array(prices), timeperiod=20)[0][-1],
        'lower_bb': talib.BBANDS(np.array(prices), timeperiod=20)[2][-1],
        'stoch_k': talib.STOCH(np.array(high), np.array(low), np.array(close))[0][-1],
        'stoch_d': talib.STOCH(np.array(high), np.array(low), np.array(close))[1][-1],
        'sma_20': talib.SMA(np.array(prices), 20)[-1],
        'sma_50': talib.SMA(np.array(prices), 50)[-1],
        'sar': talib.SAR(np.array(high), np.array(low))[-1],
        'volume': volume[-1],
        'willr': talib.WILLR(np.array(high), np.array(low), np.array(close), timeperiod=14)[-1],
        'obv': obv_values[-1],
        'obv_previous': obv_values[-2] if len(obv_values) > 1 else None,
        'swing_high': swing_high,  # Добавляем Swing High в словарь индикаторов
        'swing_low': swing_low,   # Добавляем Swing Low в словарь индикаторов
    }
    return indicators


def calculate_support_resistance(prices, period=14):
    """
    Вычисляет уровни поддержки и сопротивления.
    """
    if len(prices) < period:
        return None, None

    supports = []
    resistances = []

    for i in range(period, len(prices)):
        window = prices[i - period:i]
        support = np.min(window)
        resistance = np.max(window)
        supports.append(support)
        resistances.append(resistance)

    return supports[-1] if supports else None, resistances[-1] if resistances else None


def calculate_adx(high, low, close, period=14):
    """
    Вычисляет индекс направленного движения (ADX).
    """
    if len(close) < period:
        return None
    adx = talib.ADX(np.array(high), np.array(
        low), np.array(close), timeperiod=period)[-1]
    return adx


def calculate_ichimoku(high, low, close):
    """
    Вычисляет линии Облака Ишимоку.
    """
    if len(close) < 52:  # Минимум для расчета Ichimoku
        return None, None, None
    conversion_line = (talib.MAX(np.array(high), timeperiod=9) +
                       talib.MIN(np.array(low), timeperiod=9)) / 2
    base_line = (talib.MAX(np.array(high), timeperiod=26) +
                 talib.MIN(np.array(low), timeperiod=26)) / 2
    leading_span_a = (conversion_line + base_line) / 2
    leading_span_b = (talib.MAX(np.array(high), timeperiod=52) +
                      talib.MIN(np.array(low), timeperiod=52)) / 2
    return conversion_line[-1], base_line[-1], leading_span_b[-1]


# ОБНОВЛЕНО: Добавлен context
def determine_trend(ema_30, ema_100, current_price, previous_price, context):
    """
    Определяет тренд на основе скользящих средних и изменения цены.
    """
    trend_text = ""
    strength_text = ""

    if ema_30 and ema_100:  # Изменено на ema_30 и ema_100
        if ema_30 > ema_100:  # Изменено на ema_30 и ema_100
            trend_text += TEXTS[context.user_data['language']
                                ]['trend_ascending']
        elif ema_30 < ema_100:  # Изменено на ema_30 и ema_100
            trend_text += TEXTS[context.user_data['language']
                                ]['trend_descending']
        else:
            trend_text += TEXTS[context.user_data['language']
                                ]['trend_sideways']

    if current_price and previous_price:
        price_change = current_price - previous_price
        if abs(price_change) > 0.05 * current_price:
            strength_text = TEXTS[context.user_data['language']
                                  ]['trend_strength_strong']
        else:
            strength_text = TEXTS[context.user_data['language']
                                  ]['trend_strength_weak']
        if price_change > 0:
            trend_text += " 📈"
        else:
            trend_text += " 📉"

    return trend_text + strength_text if trend_text else TEXTS[context.user_data['language']]['trend_sideways']


def calculate_fibonacci_levels(min_price, max_price):
    """
    Рассчитывает уровни коррекции Фибоначчи.
    """
    if max_price < min_price:
        return {}  # Возвращаем пустой словарь, если максимум меньше минимума

    diff = max_price - min_price
    levels = {}
    levels['23.6%'] = max_price - diff * 0.236
    levels['38.2%'] = max_price - diff * 0.382
    levels['50.0%'] = max_price - diff * 0.500
    levels['61.8%'] = max_price - diff * 0.618
    levels['78.6%'] = max_price - diff * 0.786
    return levels


def get_trading_signal(coin_id: str, interval='1d', context=None):  # Добавлено context
    """
    Определяет торговый сигнал на основе технических индикаторов и уровней Фибоначчи.
    """
    hist_data = get_historical_data(coin_id, interval)
    if not hist_data or len(hist_data) < 50:
        # Измененное сообщение об ошибке
        return TEXTS[context.user_data['language']]['error_invalid_ticker'].format(coin_id), ""

    high = [h for h, _, _, _ in hist_data]
    low = [l for _, l, _, _ in hist_data]
    close = [c for _, _, c, _ in hist_data]
    volume = [v for _, _, _, v in hist_data]
    prices = close

    indicators = calculate_indicators(prices, high, low, close, volume)
    support, resistance = calculate_support_resistance(prices)
    # === Расчет уровней Фибоначчи ===
    # Настраиваемый период для Swing High/Low для Фибоначчи
    period_for_fibonacci_swing = 30
    swing_high_fib = np.max(high[-period_for_fibonacci_swing:]
                            ) if len(high) >= period_for_fibonacci_swing else None
    swing_low_fib = np.min(low[-period_for_fibonacci_swing:]
                           ) if len(low) >= period_for_fibonacci_swing else None
    fibonacci_levels = {}
    if swing_high_fib and swing_low_fib:
        fibonacci_levels = calculate_fibonacci_levels(
            swing_low_fib, swing_high_fib)
    # === Конец расчета уровней Фибоначчи ===

    buy_signals = sell_signals = 0

    # --- Существующие сигналы (с измененными порогами RSI/Stochastic) ---
    if close[-1] <= indicators['lower_bb']:
        buy_signals += 1
    elif close[-1] >= indicators['upper_bb']:
        sell_signals += 1
    if indicators['stoch_k'] < 25:  # Stochastic K перепродан (изменено на 25)
        buy_signals += 1
    # Stochastic K перекуплен (изменено на 75)
    elif indicators['stoch_k'] > 75:
        sell_signals += 1
    if indicators['sma_20'] > indicators['sma_50']:
        buy_signals += 1
    elif indicators['sma_20'] < indicators['sma_50']:
        sell_signals += 1
    if indicators['volume'] > np.mean(volume[-5:]) * 1.5:
        if close[-1] > close[-2]:
            buy_signals += 1
        else:
            sell_signals += 1
    if close[-1] > indicators['sar']:
        buy_signals += 1
    else:
        sell_signals += 1
    if support and resistance:
        if close[-1] <= support * 1.005:
            buy_signals += 1
        elif close[-1] >= resistance * 0.995:
            sell_signals += 1
    if indicators['rsi'] > 65:  # RSI перекуплен (изменено на 65)
        sell_signals += 1
    elif indicators['rsi'] < 35:  # RSI перепродан (изменено на 35)
        buy_signals += 1
    if indicators['macd'] > indicators['signal']:
        buy_signals += 1
    elif indicators['macd'] < indicators['signal']:
        sell_signals += 1
    if indicators['ema_30'] > indicators['ema_100']:  # Изменено на ema_30 и ema_100
        buy_signals += 1
    elif indicators['ema_30'] < indicators['ema_100']:  # Изменено на ema_30 и ema_100
        sell_signals += 1
    if indicators['willr'] < -80:
        buy_signals += 1
    elif indicators['willr'] > -20:
        sell_signals += 1

    # --- Сигналы на основе OBV ---
    obv = indicators['obv']
    previous_obv = indicators.get('obv_previous')

    if previous_obv is not None:
        if obv > previous_obv:
            buy_signals += 1
        elif obv < previous_obv:
            sell_signals += 1
    # --- КОНЕЦ БЛОКА ДЛЯ OBV

    # --- Новые сигналы ---
    # ADX
    adx = calculate_adx(high, low, close)
    if adx and adx > 25:
        buy_signals += 1

    # Ichimoku
    conversion_line, base_line, leading_span_b = calculate_ichimoku(
        high, low, close)
    if conversion_line and base_line and leading_span_b:
        if close[-1] > conversion_line and close[-1] > base_line:
            buy_signals += 1
        elif close[-1] < conversion_line and close[-1] < base_line:
            sell_signals += 1

    # --- Сигналы на основе уровней Фибоначчи ---
    if fibonacci_levels:
        current_price = close[-1]
        for level_name, level_value in fibonacci_levels.items():
            # Рассмотрим первые 3 уровня как наиболее значимые поддержки/сопротивления
            if level_name in ['23.6%', '38.2%', '50.0%']:
                # Цена вблизи уровня Фибоначчи (допуск 0.5%)
                if current_price >= level_value * 0.995 and current_price <= level_value * 1.005:
                    # Уровень находится между Swing High и Swing Low
                    if level_value < swing_high_fib and level_value > swing_low_fib:
                        if current_price < level_value:  # Цена ниже уровня - потенциальное сопротивление
                            sell_signals += 1
                        else:  # Цена выше уровня - потенциальная поддержка
                            buy_signals += 1
    # --- КОНЕЦ БЛОКА СИГНАЛОВ ФИБОНАЧЧИ ---

    signal_text = TEXTS[context.user_data['language']]['signal_buy'] if buy_signals > sell_signals else TEXTS[context.user_data['language']
                                                                                                              ]['signal_sell'] if sell_signals > buy_signals else TEXTS[context.user_data['language']]['signal_hold']

    trend = determine_trend(
        indicators['ema_30'],  # Изменено на ema_30
        indicators['ema_100'],  # Изменено на ema_100
        close[-1],
        close[-2] if len(close) > 1 else None,
        context  # ДОБАВЛЕНО: Передача context
    )

    return signal_text, trend, fibonacci_levels  # Возвращаем fibonacci_levels


def get_historical_data(coin_id: str, interval='1d'):
    """
    Получает исторические данные цены для монеты с Binance API.
    """
    try:
        if interval == '24h':  # Исправление: использовать '1d' для 24h
            binance_interval = '1d'
        elif interval == '8h':
            binance_interval = '8h'
        elif interval == '4h':
            binance_interval = '4h'
        elif interval == '12h':
            binance_interval = '12h'
        elif interval == '1h':
            binance_interval = '1h'
        else:
            binance_interval = interval

        url = f"https://api.binance.com/api/v3/klines?symbol={coin_id.upper()}USDT&interval={binance_interval}&limit=200"
        response = requests.get(url)
        response.raise_for_status()
        hist_data_json = response.json()
        return [
            (float(c[2]),  # high
             float(c[3]),  # low
             float(c[4]),  # close
             float(c[5]))  # volume
            for c in hist_data_json
        ]
    except requests.exceptions.RequestException as e:
        logger.error(
            f"Historical data error (get_historical_data for {coin_id}, interval {interval}): {e}")
        return None


# ======================================================================
#                       Секция 6: Обработчики текстовых сообщений Telegram
#                       (Обработка пользовательского ввода текста)
# ======================================================================

async def handle_text(update: Update, context: CallbackContext):
    """
    Обрабатывает текстовые сообщения от пользователя.
    Определяет, является ли сообщение запросом цены или запросом технического анализа.
    """
    text = update.message.text.strip().upper()
    parts = text.split()

    if len(parts) == 1:  # Одиночный тикер для технического анализа
        coin_id = text
        price_data = get_binance_price(coin_id)

        if not price_data:
            await update.message.reply_text(TEXTS[context.user_data['language']]['error_fetching_data'])
            return

        price = float(price_data['lastPrice'])
        change_24h = float(price_data['priceChangePercent'])

        # Передаем context в get_trading_signal
        signal_info = get_trading_signal(coin_id, context=context)

        # проверяем, что вернулось 3 значения
        if isinstance(signal_info, tuple) and len(signal_info) == 3:
            # распаковываем значения, если их 3
            signal_text, trend_text, fibonacci_levels = signal_info
        else:  # если вернулось не 3 значения (ошибка)
            signal_text, trend_text = signal_info if isinstance(signal_info, tuple) else (
                # обрабатываем, если вернулось 2 или что-то другое
                TEXTS[context.user_data['language']]['error_fetching_data'], "")
            fibonacci_levels = {}  # в случае ошибки уровни Фибоначчи делаем пустыми

        # ===  Определение силы сигнала и добавление стрелок (для 24h таймфрейма) ===
        signal_strength_arrows = ""
        buy_signals = 0  # Инициализация для доступа в этом скоупе
        sell_signals = 0  # Инициализация для доступа в этом скоупе
        if signal_text == TEXTS[context.user_data['language']]['signal_buy']:
            buy_signals, sell_signals = get_signal_counts_for_arrows(
                coin_id, context=context)  # Передаем context
            if buy_signals - sell_signals >= 3:  # Настраиваемый порог для "сильного" сигнала
                # 3 стрелки вверх для сильного BUY (замена кружков)
                signal_strength_arrows = "⬆️⬆️⬆️ "
        elif signal_text == TEXTS[context.user_data['language']]['signal_sell']:
            buy_signals, sell_signals = get_signal_counts_for_arrows(
                coin_id, context=context)  # Передаем context
            if sell_signals - buy_signals >= 3:  # Настраиваемый порог для "сильного" сигнала
                # 3 стрелки вниз для сильного SELL (замена кружков)
                signal_strength_arrows = "⬇️⬇️⬇️ "
        # ===  КОНЕЦ БЛОКА СТРЕЛОК ===

        message = (TEXTS[context.user_data['language']]['price_coin'].format(coin_id, price) +
                   TEXTS[context.user_data['language']]['change_24h'].format(change_24h) +
                   TEXTS[context.user_data['language']]['signal_24h'].format(signal_strength_arrows + signal_text) +
                   TEXTS[context.user_data['language']]['trend_24h'].format(trend_text))

        # Блок с уровнями Фибоначчи УДАЛЕН

        keyboard = [
            [
                InlineKeyboardButton(
                    TEXTS[context.user_data['language']]['button_1h'], callback_data=f"{coin_id}_1h"),
                InlineKeyboardButton(
                    TEXTS[context.user_data['language']]['button_4h'], callback_data=f"{coin_id}_4h"),
            ],
            [
                InlineKeyboardButton(
                    TEXTS[context.user_data['language']]['button_12h'], callback_data=f"{coin_id}_12h"),
                InlineKeyboardButton(
                    TEXTS[context.user_data['language']]['back_button'], callback_data=f"{coin_id}_back"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(message, parse_mode="Markdown", reply_markup=reply_markup)

    # Запрос цены в USDT (количество COIN USDT)
    elif len(parts) == 2 and parts[1].upper() == "USDT":
        try:
            amount_str, coin_symbol_original = parts
            amount = float(amount_str)
            coin_symbol = coin_symbol_original.upper()

            # === === ===  ИСПОЛЬЗУЕМ COINGECKO ДЛЯ ЦЕН USDT ПАР  === === ===
            coingecko_coin_id = get_coingecko_coin_id_by_symbol(
                coin_symbol)  # Получаем CoinGecko ID по символу

            if coingecko_coin_id:
                # Получаем цену через CoinGecko
                price_usd = get_coingecko_price(coingecko_coin_id, 'usd')
                if price_usd is not None:
                    calculated_value = amount * price_usd
                    message = TEXTS[context.user_data['language']]['price_in_usdt'].format(
                        calculated_value)  # Форматируем с 8 знаками после запятой
                    await update.message.reply_text(f"💰 {message}")
                else:
                    # Сообщение об ошибке, если цена не получена с CoinGecko
                    await update.message.reply_text(TEXTS[context.user_data['language']]['error_fetching_price_usdt'].format(coin_symbol))
            else:
                # Сообщение об ошибке, если CoinGecko ID не найден
                await update.message.reply_text(TEXTS[context.user_data['language']]['error_invalid_ticker'].format(coin_symbol))
            # === === ===  КОНЕЦ БЛОКА COINGECKO  === === ===

        except ValueError:
            await update.message.reply_text(TEXTS[context.user_data['language']]['invalid_input_amount_coin_coin'])

    elif len(parts) == 3:  # Обработка "количество COIN1 COIN2" для любого тикера
        try:
            amount = float(parts[0])
            coin1_id = parts[1]
            coin2_id = parts[2]

            # Попытка получить прямую цену с Binance (как было раньше для крипто-крипто пар)
            direct_price = get_binance_price_direct(coin1_id, coin2_id)

            if direct_price:
                # Если прямая цена есть на Binance, используем ее (как и раньше для крипто-крипто пар)
                calculated_value = amount * direct_price
                message = TEXTS[context.user_data['language']]['price_in_crypto'].format(
                    calculated_value, coin2_id.upper())
                await update.message.reply_text(f"💰 {message}")
            else:
                # Если прямой пары нет на Binance, пытаемся рассчитать через USDT (используем Binance цены для крипто-крипто пар, как и раньше)
                price_coin1_usdt_data = get_binance_price(coin1_id)
                price_coin2_usdt_data = get_binance_price(coin2_id)

                if price_coin1_usdt_data and price_coin2_usdt_data:
                    # Получаем цены COIN1/USDT и COIN2/USDT с Binance
                    price_coin1_usdt = float(
                        price_coin1_usdt_data['lastPrice'])
                    price_coin2_usdt = float(
                        price_coin2_usdt_data['lastPrice'])

                    # Рассчитываем стоимость COIN1 в COIN2 через USDT как посредника (используем Binance цены)
                    calculated_value = (
                        amount * price_coin1_usdt) / price_coin2_usdt
                    message = TEXTS[context.user_data['language']]['price_in_crypto'].format(
                        calculated_value, coin2_id.upper())
                    await update.message.reply_text(f"💰 {message}")
                else:
                    # Если не удалось получить цену через USDT на Binance, выводим сообщение об ошибке
                    await update.message.reply_text(
                        TEXTS[context.user_data['language']]['error_fetching_price_crypto'].format(coin1_id, coin2_id))

        except ValueError:
            await update.message.reply_text(TEXTS[context.user_data['language']]['invalid_input_amount_coin_coin'])
        except IndexError:
            await update.message.reply_text(TEXTS[context.user_data['language']]['invalid_input_amount_coin_coin_index_error'])

    else:  # Обработка ошибок ввода
        await update.message.reply_text(TEXTS[context.user_data['language']]['error_fetching_data'])


async def handle_timeframe_data(update: Update, context: CallbackContext):
    """
    Обрабатывает запросы на технический анализ для разных таймфреймов (по нажатию кнопок).
    """
    query = update.callback_query
    await query.answer()

    data = query.data.split("_")
    coin_id = data[0]
    interval = data[1]

    if interval == 'back':
        await query.edit_message_reply_markup(reply_markup=None)
        return

    hist_data = get_historical_data(coin_id, interval)
    if not hist_data or len(hist_data) < 2:
        await query.edit_message_text(TEXTS[context.user_data['language']]['not_enough_historical_data'])
        return

    ### ====================  БЛОК НАСТРОЙКИ И ПОКАЗА ПРОЦЕНТОВ (НАЧАЛО) ==================== ###
    interval_change_percent = 0.0

    if len(hist_data) >= 2:
        first_price = hist_data[1][2]
        last_price = hist_data[0][2]
        interval_change_percent = (
            (last_price - first_price) / first_price) * 100

    ### ====================  БЛОК НАСТРОЙКИ И ПОКАЗА ПРОЦЕНТОВ (КОНЕЦ) ==================== ###

    signal_text, trend_text, fibonacci_levels = get_trading_signal(
        coin_id, interval, context=context)  # Передаем context
    # Используем Binance для текущей цены в техническом анализе (можно изменить на CoinGecko, если нужно)
    price_data = get_binance_price(coin_id)

    if not price_data:
        await query.edit_message_text(TEXTS[context.user_data['language']]['error_fetching_timeframe_data'])
        return

    price = float(price_data['lastPrice'])
    high = [h[0] for h in hist_data]
    low = [l[1] for l in hist_data]
    close_prices = [c[2] for c in hist_data]
    volume = [v[3] for v in hist_data]
    prices = close_prices  # Используем close_prices как 'prices' для индикаторов

    # Исправленный вызов calculate_indicators:
    # Передаем close_prices как 'close'
    indicators = calculate_indicators(prices, high, low, close_prices, volume)

    # ===  Расчет уровней Фибоначчи  ===
    # Настраиваемый период для Swing High/Low для Фибоначчи
    period_for_fibonacci_swing = 30
    swing_high_fib = np.max(high[-period_for_fibonacci_swing:]
                            ) if len(high) >= period_for_fibonacci_swing else None
    swing_low_fib = np.min(low[-period_for_fibonacci_swing:]
                           ) if len(low) >= period_for_fibonacci_swing else None

    # ===  Определение силы сигнала и добавление стрелок ===
    signal_strength_arrows = ""
    buy_signals = 0  # Инициализация для доступа в этом скоупе
    sell_signals = 0  # Инициализация для доступа в этом скоупе
    if signal_text == TEXTS[context.user_data['language']]['signal_buy']:
        buy_signals, sell_signals = get_signal_counts_for_arrows(
            coin_id, interval, context=context)  # Передаем context
        if buy_signals - sell_signals >= 3:  # Настраиваемый порог для "сильного" сигнала
            # 3 стрелки вверх для сильного BUY (замена кружков)
            signal_strength_arrows = "⬆️⬆️⬆️ "
    elif signal_text == TEXTS[context.user_data['language']]['signal_sell']:
        buy_signals, sell_signals = get_signal_counts_for_arrows(
            coin_id, interval, context=context)  # Передаем context
        if sell_signals - buy_signals >= 3:  # Настраиваемый порог для "сильного" сигнала
            # 3 стрелки вниз для сильного SELL (замена кружков)
            signal_strength_arrows = "⬇️⬇️⬇️ "
    # ===  КОНЕЦ БЛОКА СТРЕЛОК ===

    # Вставляем небольшое случайное изменение в price и interval_change_percent перед форматированием
    noisy_price = price + numpy.random.rand() * 1e-9  # Добавляем шум к цене
    noisy_interval_change_percent = interval_change_percent + numpy.random.rand() * \
        1e-9

    message = (TEXTS[context.user_data['language']]['price_coin'].format(coin_id, noisy_price) +  # Используем noisy_price здесь
               #  TEXTS[context.user_data['language']]['timeframe_change'].format(get_interval_label(interval, context.user_data['language']), noisy_interval_change_percent) + # Используем noisy_interval_change_percent здесь и язык из user_data
               # Добавляем стрелки перед текстом сигнала
               TEXTS[context.user_data['language']]['signal_timeframe'].format(interval, signal_strength_arrows + signal_text) +
               TEXTS[context.user_data['language']
                     ]['trend_timeframe'].format(interval, trend_text)
               )

    # Блок с уровнями Фибоначчи УДАЛЕН

    keyboard = [
        [
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['button_1h'], callback_data=f"{coin_id}_1h"),
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['button_4h'], callback_data=f"{coin_id}_4h"),
        ],
        [
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['button_12h'], callback_data=f"{coin_id}_12h"),
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['back_button'], callback_data=f"{coin_id}_back"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(message, parse_mode="Markdown", reply_markup=reply_markup)


# Добавлено context
def get_signal_counts_for_arrows(coin_id, interval='1d', context=None):
    """
    Вспомогательная функция для получения количества buy_signals и sell_signals
    для определения силы сигнала и отображения стрелок.
    """
    hist_data = get_historical_data(coin_id, interval)
    if not hist_data or len(hist_data) < 50:
        return 0, 0  # Возвращаем 0, если данные недоступны

    high = [h for h, _, _, _ in hist_data]
    low = [l for _, l, _, _ in hist_data]
    close = [c for _, _, c, _ in hist_data]
    volume = [v for _, _, _, v in hist_data]
    prices = close

    indicators = calculate_indicators(prices, high, low, close, volume)
    support, resistance = calculate_support_resistance(prices)

    # === Расчет уровней Фибоначчи ===
    period_for_fibonacci_swing = 30
    swing_high_fib = np.max(high[-period_for_fibonacci_swing:]
                            ) if len(high) >= period_for_fibonacci_swing else None
    swing_low_fib = np.min(low[-period_for_fibonacci_swing:]
                           ) if len(low) >= period_for_fibonacci_swing else None
    fibonacci_levels = {}
    if swing_high_fib and swing_low_fib:
        fibonacci_levels = calculate_fibonacci_levels(
            swing_low_fib, swing_high_fib)
    # === Конец расчета уровней Фибоначчи ===

    buy_signals = sell_signals = 0

    # --- Существующие сигналы (с измененными порогами RSI/Stochastic) ---
    if close[-1] <= indicators['lower_bb']:
        buy_signals += 1
    elif close[-1] >= indicators['upper_bb']:
        sell_signals += 1
    if indicators['stoch_k'] < 25:  # Stochastic K перепродан (изменено на 25)
        buy_signals += 1
    # Stochastic K перекуплен (изменено на 75)
    elif indicators['stoch_k'] > 75:
        sell_signals += 1
    if indicators['sma_20'] > indicators['sma_50']:
        buy_signals += 1
    elif indicators['sma_20'] < indicators['sma_50']:
        sell_signals += 1
    if indicators['volume'] > np.mean(volume[-5:]) * 1.5:
        if close[-1] > close[-2]:
            buy_signals += 1
        else:
            sell_signals += 1
    # Исправлено условие для SAR (ранее была опечатка)
    if indicators['sar'] > close[-1]:
        buy_signals += 1  # Сигнал BUY, если SAR ниже цены
    else:
        sell_signals += 1  # Сигнал SELL, если SAR выше цены
    if support and resistance:
        if close[-1] <= support * 1.005:
            buy_signals += 1
        elif close[-1] >= resistance * 0.995:
            sell_signals += 1
    if indicators['rsi'] > 65:  # RSI перекуплен (изменено на 65)
        sell_signals += 1
    elif indicators['rsi'] < 35:  # RSI перепродан (изменено на 35)
        buy_signals += 1
    if indicators['macd'] > indicators['signal']:
        buy_signals += 1
    elif indicators['macd'] < indicators['signal']:
        sell_signals += 1
    if indicators['ema_30'] > indicators['ema_100']:  # Изменено на ema_30 и ema_100
        buy_signals += 1
    elif indicators['ema_30'] < indicators['ema_100']:  # Изменено на ema_30 и ema_100
        sell_signals += 1
    if indicators['willr'] < -80:
        buy_signals += 1
    elif indicators['willr'] > -20:
        sell_signals += 1

    # --- Сигналы на основе OBV ---
    obv = indicators['obv']
    previous_obv = indicators.get('obv_previous')

    if previous_obv is not None:
        if obv > previous_obv:
            buy_signals += 1
        elif obv < previous_obv:
            sell_signals += 1
    # --- КОНЕЦ БЛОКА ДЛЯ OBV

    # --- Новые сигналы ---
    # ADX
    adx = calculate_adx(high, low, close)
    if adx and adx > 25:
        buy_signals += 1

    # Ichimoku
    conversion_line, base_line, leading_span_b = calculate_ichimoku(
        high, low, close)
    if conversion_line and base_line and leading_span_b:
        if close[-1] > conversion_line and close[-1] > base_line:
            buy_signals += 1
        elif close[-1] < conversion_line and close[-1] < base_line:
            sell_signals += 1

    # --- Сигналы на основе уровней Фибоначчи ---
    # (Сигналы на основе Фибоначчи уже добавлены в get_trading_signal)

    return buy_signals, sell_signals


# ======================================================================
#                       Секция 7: Вспомогательные функции
# ======================================================================

# lang='ru' больше не нужен, но оставим для совместимости и если захотим глобальный язык по умолчанию
def get_interval_label(interval, lang='ru'):
    """
    Возвращает локализованное название интервала времени.
    """
    interval_labels = {
        'ru': {
            '1h': TEXTS['ru']['interval_1h'],
            '4h': TEXTS['ru']['interval_4h'],
            '8h': TEXTS['ru']['interval_8h'],
            '12h': TEXTS['ru']['interval_12h'],
            '24h': TEXTS['ru']['interval_24h'],
            '1d': TEXTS['ru']['interval_1d'],
            'Change': TEXTS['ru']['interval_change'],
        },
        'en': {
            '1h': TEXTS['en']['interval_1h'],
            '4h': TEXTS['en']['interval_4h'],
            '8h': TEXTS['en']['interval_8h'],
            '12h': TEXTS['en']['interval_12h'],
            '24h': TEXTS['en']['interval_24h'],
            '1d': TEXTS['en']['interval_1d'],
            'Change': TEXTS['en']['interval_change'],
        }
    }
    # lang теперь context.user_data['language']
    return interval_labels[lang].get(interval, TEXTS[lang]['interval_change'])


# ======================================================================
#                       Секция 8: Обработчики CallbackQuery кнопок
#                       (Inline кнопки, ответы на нажатия)
# ======================================================================

async def start(update: Update, context: CallbackContext, query=None):  # Добавляем параметр query
    """Обработчик команды /start, вывод стартового сообщения и кнопок."""
    user_id = update.message.from_user.id if update.message else query.from_user.id  # Определяем user_id для message и callback_query
    user_language = get_user_language(user_id)
    context.user_data['language'] = user_language

    keyboard = [
        [
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['top10_rise_button'], callback_data="TOP10_RISE"),
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['top10_fall_button'], callback_data="TOP10_FALL"),
        ],
        [
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['help_button'], callback_data="HELP"),
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['donat_button'], callback_data="DONAT"),
        ],
        [
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['english_button'], callback_data="LANGUAGE_EN"),
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['russian_button'], callback_data="LANGUAGE_RU"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text = TEXTS[context.user_data['language']
                         ]['start_message']  # Получаем текст сообщения

    # Если функция вызвана из CallbackQuery (например, при смене языка)
    if query:
        await query.answer()  # Подтверждаем CallbackQuery
        await query.edit_message_text(  # Редактируем существующее сообщение
            message_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:  # Если функция вызвана командой /start (новое сообщение)
        await update.message.reply_text(  # Отправляем новое сообщение
            message_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )


async def help(update: Update, context: CallbackContext):
    """Обработчик команды /help и кнопки '❓ Помощь', вывод справки."""
    query = update.callback_query
    await query.answer()
    message = (TEXTS[context.user_data['language']]['help_message_header'] +
               TEXTS[context.user_data['language']]['help_message_calculation_header'] +
               TEXTS[context.user_data['language']]['help_message_calculation_text'] +
               TEXTS[context.user_data['language']]['help_message_calculation_examples_header'] +
               TEXTS[context.user_data['language']]['help_message_calculation_examples_text'] +
               TEXTS[context.user_data['language']]['help_message_technical_analysis_header'] +
               TEXTS[context.user_data['language']]['help_message_technical_analysis_text'] +
               TEXTS[context.user_data['language']]['help_message_technical_analysis_features_header'] +
               TEXTS[context.user_data['language']]['help_message_technical_analysis_features_text'] +
               TEXTS[context.user_data['language']]['help_message_other_functions_header'] +
               TEXTS[context.user_data['language']]['help_message_other_functions_text'])

    keyboard = [
        [
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['top10_rise_button'], callback_data="TOP10_RISE"),
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['top10_fall_button'], callback_data="TOP10_FALL"),
        ],
        [
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['help_button'], callback_data="HELP"),
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['donat_button'], callback_data="DONAT"),
        ],
        [
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['english_button'], callback_data="LANGUAGE_EN"),
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['russian_button'], callback_data="LANGUAGE_RU"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(message, parse_mode="Markdown", reply_markup=reply_markup)


async def handle_donat(update: Update, context: CallbackContext):
    """Обработчик кнопки '💰 Donat', вывод сообщения с информацией для доната."""
    message = TEXTS[context.user_data['language']]['donat_message']

    # ===  Добавляем клавиатуру главного меню ===
    keyboard = [
        [
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['top10_rise_button'], callback_data="TOP10_RISE"),
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['top10_fall_button'], callback_data="TOP10_FALL"),
        ],
        [
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['help_button'], callback_data="HELP"),
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['donat_button'], callback_data="DONAT"),
        ],
        [
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['english_button'], callback_data="LANGUAGE_EN"),
            InlineKeyboardButton(
                TEXTS[context.user_data['language']]['russian_button'], callback_data="LANGUAGE_RU"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # ===  Клавиатура главного меню добавлена ===

    # Заменено на edit_message_text и добавлен reply_markup
    await update.callback_query.edit_message_text(message, parse_mode="Markdown", reply_markup=reply_markup)


async def button(update: Update, context: CallbackContext):
    """
    Обработчик всех кнопок InlineKeyboard.
    """
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == "CLOSE_HELP":
        await close_help(update, context)
    elif query.data == "TOP10_RISE":
        await handle_top10_rise(update, context)
    elif query.data == "TOP10_FALL":
        await handle_top10_fall(update, context)
    elif query.data == "HELP":
        await help(update, context)
    elif query.data == "DONAT":
        await handle_donat(update, context)
    # Обработка кнопки English (на главном экране)
    elif query.data == "LANGUAGE_EN":
        set_user_language(user_id, 'en')
        context.user_data['language'] = 'en'
        # Вызываем start с query для редактирования сообщения!
        await start(update, context, query=query)
        await query.answer(text="Bot language switched to English!")
    # Обработка кнопки Русский (на главном экране)
    elif query.data == "LANGUAGE_RU":
        set_user_language(user_id, 'ru')
        context.user_data['language'] = 'ru'
        # Вызываем start с query для редактирования сообщения!
        await start(update, context, query=query)
        await query.answer(text="Язык бота переключен на русский!")
    elif "_" in query.data and query.data != "CLOSE_HELP":
        await handle_timeframe_data(update, context)


async def close_help(update: Update, context: CallbackContext):
    """Обработчик для кнопки "Закрыть" в справке, удаляет клавиатуру."""
    query = update.callback_query
    await query.answer()
    if query.message:
        await query.edit_message_reply_markup(reply_markup=None)


# ======================================================================
#                       Секция 9: Главная функция запуска бота
# ======================================================================

def main():
    """Главная функция для запуска бота."""
    application = Application.builder().token(
        # Замените на свой токен бота
        "7568689765:AAHLeergcWCz3EyzMQ5GGqBCylFiQs2xn-Q").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()

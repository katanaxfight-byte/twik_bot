
# -*- coding: utf-8 -*-
"""
Telegram Bot - Чат Менеджер для групп с системой уровней
Работает на Pydroid 3
ФИНАЛЬНАЯ ВЕРСИЯ
"""

import telebot
from telebot import types
import sqlite3
import time
import random
import re
from datetime import datetime, timedelta
import threading
import math
import schedule

# ---------- НАСТРОЙКИ ----------
TOKEN = '8263170749:AAHiUNlxpT2sVCWZauKQKhMsNDHhjaoCN8Q'
OWNER_ID = 8264383583

bot = telebot.TeleBot(TOKEN)

# ---------- РУСИФИКАЦИЯ КОМАНД ----------
COMMANDS = {
    'reg': ['reg', 'рег', 'регистрация'],
    'mute': ['мут', 'mute'],
    'unmute': ['снятьмут', 'unmute'],
    'ban': ['бан', 'ban'],
    'unban': ['снятьбан', 'unban'],
    'kick': ['кик', 'kick'],
    'staff': ['staff', 'админы', 'администрация'],
    'makeadmin': ['makeadmin', 'назначить', 'датьадминку'],
    'unadmin': ['unadmin', 'снять', 'убратьадминку'],
    'setadminbot': ['setadminbot', 'датьадминкубота'],
    'profile': ['profile', 'профиль'],
    'stats': ['stats', 'статистика', 'стата'],
    'name': ['name', 'ник', 'никнейм'],
    'setname': ['setname', 'сменитьник', 'изменитьник'],
    'asetname': ['asetname', 'адмсменитьник'],
    'kazino': ['kaz', 'казино', 'casino', 'каз'],
    'pay': ['pay', 'перевод', 'перевести'],
    'тишина': ['тишина', 'muteall', 'slowmode'],
    'help': ['help', 'помощь', 'команды'],
    'verificate': ['verificate', 'верифицировать', 'verify'],
    'setmyadmin': ['setmyadmin', 'дайсебеадминку'],
    'givetwist': ['givetwist', 'выдатьтвисты', 'выдать'],
    'deltwist': ['deltwist', 'забратьтвисты', 'забрать'],
    'setstat': ['setstat', 'изменитьстату'],
    'deltop': ['deltop', 'убратьизтопа'],
    'createpromo': ['createpromo', 'создатьпромо'],
    'delpromo': ['delpromo', 'удалитьпромо'],
    'promo': ['promo', 'активироватьпромо'],
    'toptwist': ['toptwist', 'топ', 'топтвистов'],
    'warn': ['warn', 'пред', 'предупреждение'],
    'unwarn': ['unwarn', 'снятьпред'],
    'clear': ['clear', 'очистить', 'del'],
    'sethi': ['sethi', 'установитьприветствие'],
    'hi': ['hi', 'приветствие'],
    'addpravila': ['addpravila', 'установитьправила'],
    'pravila': ['pravila', 'правила'],
    'lixoradka': ['lixoradka', 'лихорадка'],
    'stoplixoradka': ['stoplixoradka', 'стоплихорадка'],
    'givetoper': ['givetoper', 'датьтопер'],
    'duel': ['duel', 'дуэль'],
    'obnulenie': ['obnulenie', 'обнуление'],
    'hui': ['хуй', 'hui', 'писюн'],
    'ukrast': ['украсть', 'ukrast', 'воровать'],
    'toppiska': ['топписька', 'toppiska', 'топписюнов'],
    'mainingshop': ['mainingshop', 'майнингшоп', 'магазин'],
    'mainingferma': ['mainingferma', 'ферма', 'майнингферма'],
    'upd': ['upd', 'обновления', 'списокобновлений'],
    'setupd': ['setupd', 'установитьобновления'],
    'bitcoin': ['биткоин', 'bitcoin', 'btc'],
    'exchange': ['обменять', 'exchange', 'обмен'],
    'transferbtc': ['переводбиткоин', 'transferbtc', 'переводbtc'],
    'zames': ['замес', 'zames'],
    'spisok': ['список', 'list'],
    'donat': ['донат', 'donat', 'дон'],
    'giverub': ['giverub', 'выдатьрубли'],
    'rate': ['курс', 'rate'],
    'changerate': ['изменитькурс', 'changerate'],
    'sellbtc': ['продатьбиткоин', 'sellbtc', 'продать'],
    'obnulbitoc': ['obnulbitoc', 'обнулбиток', 'обнулитьбиткоины'],
    'picture': ['картинка', 'picture', 'фото'],
    'delpicture': ['удалитькартинку',      '    delpicture', 'удалитьфото'],
    'winimage': ['win', 'выигрыш', 'победа'],
    'loseimage': ['lose', 'проигрыш', 'поражение'],
    'bonus': ['бонус', 'bonus'],
    'event': ['event', 'эвент', 'ивент'],
    'fight': ['бой', 'fight'],
    'givemedal': ['givemedal', 'выдатьмедаль'],
    'statsevent': ['statsevent', 'статистикаивента'],
    'gif': ['gif', 'гиф']
}

# ---------- ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ ----------
def init_db():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            nick TEXT,
            twists INTEGER DEFAULT 0,
            bitcoins REAL DEFAULT 0,
            registered_date TEXT,
            verified INTEGER DEFAULT 0,
            is_owner INTEGER DEFAULT 0,
            warns INTEGER DEFAULT 0,
            piska_size INTEGER DEFAULT 0,
            piska_last_grow TEXT,
            piska_last_steal TEXT,
            has_card1 INTEGER DEFAULT 0,
            card1_level INTEGER DEFAULT 0,
            card1_balance INTEGER DEFAULT 0,
            card1_last_collect TEXT,
            has_card2 INTEGER DEFAULT 0,
            card2_level INTEGER DEFAULT 0,
            card2_balance INTEGER DEFAULT 0,
            card2_last_collect TEXT,
            last_zames TEXT,
            rub_balance INTEGER DEFAULT 0
        )
    ''')

    # Добавляем колонки для видеокарт 3, 4, 5 (если их нет)
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN has_card3 INTEGER DEFAULT 0')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN card3_level INTEGER DEFAULT 0')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN card3_balance INTEGER DEFAULT 0')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN card3_last_collect TEXT')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN has_card4 INTEGER DEFAULT 0')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN card4_level INTEGER DEFAULT 0')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN card4_balance INTEGER DEFAULT 0')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN card4_last_collect TEXT')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN has_card5 INTEGER DEFAULT 0')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN card5_level INTEGER DEFAULT 0')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN card5_balance INTEGER DEFAULT 0')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN card5_last_collect TEXT')
    except:
        pass

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            update_text TEXT,
            created_date TEXT,
            created_by INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS message_stats (
            user_id INTEGER,
            chat_id INTEGER,
            messages_count INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, chat_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            user_id INTEGER,
            chat_id INTEGER,
            admin_level INTEGER DEFAULT 1,
            appointed_by INTEGER,
            appointed_date TEXT,
            PRIMARY KEY (user_id, chat_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS silence_mode (
            chat_id INTEGER PRIMARY KEY,
            until_time INTEGER,
            set_by INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS muted_users (
            user_id INTEGER,
            chat_id INTEGER,
            until_time INTEGER,
            reason TEXT,
            muted_by INTEGER,
            PRIMARY KEY (user_id, chat_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS banned_users (
            user_id INTEGER,
            chat_id INTEGER,
            until_time INTEGER,
            reason TEXT,
            banned_by INTEGER,
            PRIMARY KEY (user_id, chat_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS warns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            chat_id INTEGER,
            reason TEXT,
            warned_by INTEGER,
            warn_date TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS promocodes (
            code TEXT PRIMARY KEY,
            twists INTEGER,
            max_activations INTEGER,
            current_activations INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS promo_activations (
            user_id INTEGER,
            promo_code TEXT,
            PRIMARY KEY (user_id, promo_code)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bot_admins (
            user_id INTEGER PRIMARY KEY
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS greetings (
            chat_id INTEGER PRIMARY KEY,
            greeting_text TEXT,
            set_by INTEGER,
            set_date TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            chat_id INTEGER PRIMARY KEY,
            rules_text TEXT,
            set_by INTEGER,
            set_date TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS casino_settings (
            id INTEGER PRIMARY KEY DEFAULT 1,
            win_chance INTEGER DEFAULT 40
        )
    ''')
    cursor.execute('INSERT OR IGNORE INTO casino_settings (id, win_chance) VALUES (1, 40)')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS zames_battles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            challenger_id INTEGER,
            opponent_id INTEGER,
            bet_size INTEGER,
            status TEXT,
            created_date TEXT,
            chat_id INTEGER,
            message_id INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS btc_rate (
            id INTEGER PRIMARY KEY DEFAULT 1,
            rate INTEGER DEFAULT 1000000,
            last_change TEXT
        )
    ''')
    cursor.execute('INSERT OR IGNORE INTO btc_rate (id, rate, last_change) VALUES (1, 1000000, ?)',
                  (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile_media (
            user_id INTEGER PRIMARY KEY,
            file_id TEXT,
            media_type TEXT,  -- 'photo' или 'animation'
            updated_date TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS casino_images (
            id INTEGER PRIMARY KEY DEFAULT 1,
            win_image TEXT,
            lose_image TEXT
        )
    ''')
    cursor.execute('INSERT OR IGNORE INTO casino_images (id, win_image, lose_image) VALUES (1, NULL, NULL)')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_bonuses (
            user_id INTEGER PRIMARY KEY,
            last_bonus TEXT,
            total_bonuses INTEGER DEFAULT 0
        )
    ''')

    # ===== НОВЫЕ ТАБЛИЦЫ ДЛЯ ИВЕНТА =====
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event_boss (
            id INTEGER PRIMARY KEY DEFAULT 1,
            hp INTEGER DEFAULT 15000,
            max_hp INTEGER DEFAULT 15000,
            is_active INTEGER DEFAULT 1
        )
    ''')
    cursor.execute('INSERT OR IGNORE INTO event_boss (id, hp, max_hp, is_active) VALUES (1, 15000, 15000, 1)')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event_stats (
            user_id INTEGER PRIMARY KEY,
            damage_done INTEGER DEFAULT 0,
            duels_won INTEGER DEFAULT 0,
            battles_fought INTEGER DEFAULT 0,
            last_battle_time TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medals (
            user_id INTEGER PRIMARY KEY,
            medal_bravery INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS battle_state (
            user_id INTEGER PRIMARY KEY,
            hits_left INTEGER DEFAULT 3,
            battle_active INTEGER DEFAULT 0,
            battle_start_time TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

def update_users_table():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    columns_to_add = [
        ('warns', 'INTEGER DEFAULT 0'),
        ('piska_size', 'INTEGER DEFAULT 0'),
        ('piska_last_grow', 'TEXT'),
        ('piska_last_steal', 'TEXT'),
        ('has_card1', 'INTEGER DEFAULT 0'),
        ('card1_level', 'INTEGER DEFAULT 0'),
        ('card1_balance', 'INTEGER DEFAULT 0'),
        ('card1_last_collect', 'TEXT'),
        ('has_card2', 'INTEGER DEFAULT 0'),
        ('card2_level', 'INTEGER DEFAULT 0'),
        ('card2_balance', 'INTEGER DEFAULT 0'),
        ('card2_last_collect', 'TEXT'),
        ('last_zames', 'TEXT'),
        ('bitcoins', 'REAL DEFAULT 0'),
        ('rub_balance', 'INTEGER DEFAULT 0')
    ]
    
    for col_name, col_type in columns_to_add:
        try:
            cursor.execute(f'ALTER TABLE users ADD COLUMN {col_name} {col_type}')
        except:
            pass
    
    conn.commit()
    conn.close()

update_users_table()

# ---------- ПРАВА ПО УРОВНЯМ ----------
def get_level_permissions(level):
    permissions = {
        1: {'can_warn': True, 'can_mute': True, 'max_mute_time': 3600, 'can_kick': False, 'can_ban': False, 'can_unmute': False, 'can_unban': False, 'can_muteall': False, 'can_makeadmin': False, 'can_unadmin': False, 'can_setname': False, 'can_clear': True, 'max_clear': 10},
        2: {'can_warn': True, 'can_mute': True, 'max_mute_time': 86400, 'can_kick': True, 'can_ban': False, 'can_unmute': True, 'can_unban': False, 'can_muteall': False, 'can_makeadmin': False, 'can_unadmin': False, 'can_setname': True, 'can_clear': True, 'max_clear': 30},
        3: {'can_warn': True, 'can_mute': True, 'max_mute_time': 604800, 'can_kick': True, 'can_ban': True, 'max_ban_time': 604800, 'can_unmute': True, 'can_unban': False, 'can_muteall': True, 'max_muteall_time': 3600, 'can_makeadmin': False, 'can_unadmin': False, 'can_setname': True, 'can_clear': True, 'max_clear': 50},
        4: {'can_warn': True, 'can_mute': True, 'max_mute_time': 2592000, 'can_kick': True, 'can_ban': True, 'max_ban_time': 2592000, 'can_unmute': True, 'can_unban': True, 'can_muteall': True, 'max_muteall_time': 86400, 'can_makeadmin': True, 'max_makeadmin_level': 3, 'can_unadmin': True, 'max_unadmin_level': 3, 'can_setname': True, 'can_clear': True, 'max_clear': 100},
        5: {'can_warn': True, 'can_mute': True, 'max_mute_time': float('inf'), 'can_kick': True, 'can_ban': True, 'max_ban_time': float('inf'), 'can_unmute': True, 'can_unban': True, 'can_muteall': True, 'max_muteall_time': float('inf'), 'can_makeadmin': True, 'max_makeadmin_level': 5, 'can_unadmin': True, 'max_unadmin_level': 5, 'can_setname': True, 'can_clear': True, 'max_clear': float('inf')},
        6: {'can_warn': True, 'can_mute': True, 'max_mute_time': float('inf'), 'can_kick': True, 'can_ban': True, 'max_ban_time': float('inf'), 'can_unmute': True, 'can_unban': True, 'can_muteall': True, 'max_muteall_time': float('inf'), 'can_makeadmin': True, 'max_makeadmin_level': 6, 'can_unadmin': True, 'max_unadmin_level': 6, 'can_setname': True, 'can_clear': True, 'max_clear': float('inf')}
    }
    return permissions.get(level, permissions[1])

# ---------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ----------
def get_user(user_id):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user_if_not_exists(user_id, username, first_name, last_name):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if not user:
        registered_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        is_owner = 1 if user_id == OWNER_ID else 0
        try:
            cursor.execute('''
                INSERT INTO users (
                    user_id, username, first_name, last_name, nick, twists, bitcoins,
                    registered_date, verified, is_owner, warns, piska_size,
                    piska_last_grow, piska_last_steal, has_card1, card1_level, card1_balance,
                    card1_last_collect, has_card2, card2_level, card2_balance, card2_last_collect,
                    last_zames, rub_balance
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, username, first_name, last_name, first_name, 0, 0,
                registered_date, 0, is_owner, 0, 0, None, None, 0, 0, 0, None, 0, 0, 0, None, None, 0
            ))
        except Exception as e:
            cursor.execute('''
                INSERT INTO users (
                    user_id, username, first_name, last_name, nick, twists, 
                    registered_date, verified, is_owner
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name, first_name, 0, registered_date, 0, is_owner))
        conn.commit()
    else:
        cursor.execute('UPDATE users SET username = ?, first_name = ?, last_name = ? WHERE user_id = ?',
                      (username, first_name, last_name, user_id))
        conn.commit()
    conn.close()

def update_user_stats(user_id, chat_id):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO message_stats (user_id, chat_id, messages_count)
        VALUES (?, ?, 1)
        ON CONFLICT(user_id, chat_id) DO UPDATE SET messages_count = messages_count + 1
    ''', (user_id, chat_id))
    conn.commit()
    conn.close()

def check_admin(user_id, chat_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

def check_admin_level(user_id, chat_id):
    if user_id == OWNER_ID:
        return 6
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT admin_level FROM admins WHERE user_id = ? AND chat_id = ?', (user_id, chat_id))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    if check_admin(user_id, chat_id):
        return 1
    return 0

def check_permission(user_id, chat_id, permission, value=None):
    level = check_admin_level(user_id, chat_id)
    if user_id == OWNER_ID:
        return True
    if level == 0:
        return False
    permissions = get_level_permissions(level)
    if permission in permissions:
        if value is not None and isinstance(permissions[permission], (int, float)):
            return value <= permissions[permission]
        return permissions[permission]
    return False

def is_muted(user_id, chat_id):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT until_time, reason FROM muted_users WHERE user_id = ? AND chat_id = ?', (user_id, chat_id))
    result = cursor.fetchone()
    conn.close()
    if result:
        until_time, reason = result
        if time.time() < until_time:
            return True, until_time, reason
        else:
            remove_mute(user_id, chat_id)
    return False, None, None

def remove_mute(user_id, chat_id):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM muted_users WHERE user_id = ? AND chat_id = ?', (user_id, chat_id))
    conn.commit()
    conn.close()

def is_silence_mode(chat_id):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT until_time FROM silence_mode WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        until_time = result[0]
        if time.time() < until_time:
            return True, until_time
        else:
            remove_silence(chat_id)
    return False, None

def remove_silence(chat_id):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM silence_mode WHERE chat_id = ?', (chat_id,))
    conn.commit()
    conn.close()

def parse_time(time_str):
    units = {'h': 3600, 'm': 60, 'd': 86400, 's': 1}
    match = re.match(r'^(\d+)([hmds])?$', time_str.lower())
    if match:
        value = int(match.group(1))
        unit = match.group(2) or 'm'
        return value * units.get(unit, 60)
    return None

def get_target_user(message):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    return None

def get_admin_level_name(level):
    levels = {
        1: "Младший администратор",
        2: "Администратор",
        3: "Старший администратор",
        4: "Главный администратор",
        5: "Заместитель создателя",
        6: "Создатель"
    }
    return levels.get(level, "Пользователь")

def check_bot_admin(user_id):
    if user_id == OWNER_ID:
        return True
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bot_admins WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def get_warns_count(user_id, chat_id):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM warns WHERE user_id = ? AND chat_id = ?', (user_id, chat_id))
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Удалите все предыдущие функции с курсом и вставьте эти:

def get_btc_rate():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT rate, last_change FROM btc_rate WHERE id = 1')
    result = cursor.fetchone()
    conn.close()
    return result[0], result[1]

def set_btc_rate(new_rate):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE btc_rate SET rate = ?, last_change = ? WHERE id = 1',
                  (new_rate, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def cmd_rate(message):
    """Показывает текущий курс биткоина"""
    
    # Получаем текущий курс
    current_rate, last_change_str = get_btc_rate()
    
    # Просто показываем курс
    text = f"📊 КУРС БИТКОИНА\n\n"
    text += f"💰 Цена за 1 BTC: {current_rate:,.0f} твистов\n\n"
    text += f"📈 Возможен рост до: {int(current_rate * 1.1):,.0f} твистов\n"
    text += f"📉 Возможно падение до: {int(current_rate * 0.9):,.0f} твистов"
    
    bot.reply_to(message, text)

def cmd_changerate(message):
    """Изменяет курс биткоина (только для владельца)"""
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Только для владельца бота")
        return
    
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Использование: /изменитькурс [новая цена]")
        return
    
    try:
        new_rate = float(message.text.split()[1])
        if new_rate <= 0:
            bot.reply_to(message, "❌ Цена должна быть положительной")
            return
    except ValueError:
        bot.reply_to(message, "❌ Неверная цена. Укажите число")
        return
    
    set_btc_rate(new_rate)
    bot.reply_to(message, f"✅ Курс биткоина изменен на {new_rate:,.0f} твистов за 1 BTC")

def cmd_sellbtc(message):
    """Продажа биткоинов по текущему курсу"""
    user_id = message.from_user.id
    
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Использование: /продать [количество BTC]")
        return
    
    try:
        btc_amount = float(message.text.split()[1])
        if btc_amount <= 0:
            bot.reply_to(message, "❌ Количество должно быть положительным")
            return
    except ValueError:
        bot.reply_to(message, "❌ Неверное количество. Укажите число")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT bitcoins FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    current_btc = result[0] if result else 0
    
    if current_btc < btc_amount:
        bot.reply_to(message, f"❌ У вас недостаточно биткоинов. Текущий баланс: {current_btc} BTC")
        conn.close()
        return
    
    # Получаем актуальный курс
    rate, _ = get_btc_rate()
    twists_earned = int(btc_amount * rate)
    
    cursor.execute('UPDATE users SET bitcoins = bitcoins - ?, twists = twists + ? WHERE user_id = ?',
                  (btc_amount, twists_earned, user_id))
    conn.commit()
    
    cursor.execute('SELECT bitcoins, twists FROM users WHERE user_id = ?', (user_id,))
    new_btc, new_twists = cursor.fetchone()
    conn.close()
    
    bot.reply_to(message, f"✅ Продажа успешна!\n"
                         f"Продано: {btc_amount} BTC\n"
                         f"Получено: {twists_earned} твистов\n"
                         f"Курс: {rate:,.0f} твистов за 1 BTC\n\n"
                         f"💰 Новый баланс:\n"
                         f"• Твистов: {new_twists}\n"
                         f"• Биткоинов: {new_btc} BTC")
                         
# ===== ФУНКЦИИ ДЛЯ КАРТИНОК ПРОФИЛЯ =====
def save_profile_picture(message):
    """Сохраняет фото как картинку профиля"""
    user_id = message.from_user.id
    
    # Получаем фото максимального размера
    photo = message.photo[-1]
    file_id = photo.file_id
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    # Сохраняем или обновляем картинку профиля
    cursor.execute('''
        INSERT OR REPLACE INTO profile_pictures (user_id, file_id, updated_date)
        VALUES (?, ?, ?)
    ''', (user_id, file_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    conn.commit()
    conn.close()
    
    bot.reply_to(message, "✅ Картинка профиля успешно сохранена!")

def cmd_picture(message):
    """Заглушка для команды /картинка"""
    bot.reply_to(message, "❌ Отправьте фото с подписью /картинка")

def cmd_delpicture(message):
    """Удаляет картинку из профиля"""
    user_id = message.from_user.id
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM profile_pictures WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    bot.reply_to(message, "✅ Картинка профиля удалена")

# ===== ФУНКЦИИ ДЛЯ КАРТИНОК КАЗИНО =====
def save_win_image(message):
    """Сохраняет картинку выигрыша для казино"""
    photo = message.photo[-1]
    file_id = photo.file_id
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE casino_images SET win_image = ? WHERE id = 1', (file_id,))
    conn.commit()
    conn.close()
    
    bot.reply_to(message, "✅ Картинка выигрыша успешно сохранена!")

def save_lose_image(message):
    """Сохраняет картинку проигрыша для казино"""
    photo = message.photo[-1]
    file_id = photo.file_id
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE casino_images SET lose_image = ? WHERE id = 1', (file_id,))
    conn.commit()
    conn.close()
    
    bot.reply_to(message, "✅ Картинка проигрыша успешно сохранена!")

def cmd_winimage(message):
    """Устанавливает картинку выигрыша в казино (только для владельца)"""
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Только для владельца бота")
        return
    
    bot.reply_to(message, "Отправьте фото с подписью /win чтобы установить картинку выигрыша")

def cmd_loseimage(message):
    """Устанавливает картинку проигрыша в казино (только для владельца)"""
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Только для владельца бота")
        return
    
    bot.reply_to(message, "Отправьте фото с подписью /lose чтобы установить картинку проигрыша")

# ===== ОБРАБОТЧИК СООБЩЕНИЙ С ФОТО =====
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    """Обрабатывает сообщения с фотографиями"""
    if message.chat.type not in ['group', 'supergroup']:
        return
    
    user = message.from_user
    create_user_if_not_exists(user.id, user.username, user.first_name, user.last_name)
    
    # Проверяем мут и режим тишины
    muted, until_time, reason = is_muted(user.id, message.chat.id)
    if muted:
        bot.delete_message(message.chat.id, message.message_id)
        return

    silence, until_time = is_silence_mode(message.chat.id)
    if silence and not check_admin(user.id, message.chat.id):
        bot.delete_message(message.chat.id, message.message_id)
        return

    # Проверяем, есть ли в подписи к фото команда
    if message.caption:
        caption_text = message.caption.lower().strip()
        
        # Команда для картинки профиля
        if caption_text in ['/картинка', '/picture', '/фото']:
            save_profile_picture(message)
            return
        
        # Команды для картинок казино (только для владельца)
        if user.id == OWNER_ID:
            if caption_text in ['/win', '/выигрыш', '/победа']:
                save_win_image(message)
                return
            elif caption_text in ['/lose', '/проигрыш', '/поражение']:
                save_lose_image(message)
                return
    
    # Если это просто фото без команды, обновляем статистику
    update_user_stats(user.id, message.chat.id)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if message.chat.type not in ['group', 'supergroup']:
        return

    user = message.from_user
    create_user_if_not_exists(user.id, user.username, user.first_name, user.last_name)

    try:
        chat_member = bot.get_chat_member(message.chat.id, user.id)
        if chat_member.status == 'creator':
            level = check_admin_level(user.id, message.chat.id)
            if level < 6:
                conn = sqlite3.connect('bot_data.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO admins (user_id, chat_id, admin_level, appointed_by, appointed_date)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user.id, message.chat.id, 6, user.id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                conn.commit()
                conn.close()
    except:
        pass

    muted, until_time, reason = is_muted(user.id, message.chat.id)
    if muted:
        bot.delete_message(message.chat.id, message.message_id)
        return

    silence, until_time = is_silence_mode(message.chat.id)
    if silence and not check_admin(user.id, message.chat.id):
        bot.delete_message(message.chat.id, message.message_id)
        return

    update_user_stats(user.id, message.chat.id)
    process_commands(message)


# ===== ФУНКЦИЯ process_commands =====
def process_commands(message):
    if not message.text:
        return
    
    text = message.text.lower()
    parts = text.split()
    if not parts:
        return
    
    command = parts[0]
    if command.startswith('/'):
        command = command[1:]
    
    # Отладочный вывод
    print(f"👤 Пользователь {message.from_user.id} отправил команду: {command}")
    print(f"📝 Полный текст: {message.text}")
    
    # Специальная обработка для русских команд
    if command in ['каз', 'казино']:
        print("✅ Распознана команда: казино")
        cmd_kazino(message)
        return
    elif command in ['хуй', 'писюн']:
        print("✅ Распознана команда: хуй")
        cmd_hui(message)
        return
    elif command in ['gif', 'гиф']:
        cmd_picture(message)
        return
    elif command in ['украсть', 'воровать']:
        print("✅ Распознана команда: украсть")
    elif command in ['win', 'выигрыш', 'победа']:
        cmd_winimage(message)
        return
    elif command in ['event', 'эвент', 'ивент']:
        cmd_event(message)
        return
    elif command in ['бой', 'fight']:
        cmd_fight(message)
        return
    elif command in ['givemedal', 'выдатьмедаль']:
        cmd_givemedal(message)
        return
    elif command in ['statsevent', 'статистикаивента']:
        cmd_statsevent(message)
        return
    elif command in ['lose', 'проигрыш', 'поражение']:
        cmd_loseimage(message)
        return
        cmd_ukrast(message)
        return
    elif command in ['топписька', 'топписюнов']:
        print("✅ Распознана команда: топписька")
        cmd_toppiska(message)
        return
    elif command in ['mainingshop', 'майнингшоп', 'магазин']:
        print("✅ Распознана команда: магазин")
        # В функции process_commands, в разделе специальных команд добавьте:
    elif command in ['obnulbitoc', 'обнулбиток', 'обнулитьбиткоины']:
        cmd_obnulbitoc(message)
        return
        cmd_mainingshop(message)
        return
    elif command in ['бонус', 'bonus']:
        cmd_bonus(message)
        return
    elif command in ['mainingferma', 'ферма', 'майнингферма']:
        print("✅ Распознана команда: ферма")
        cmd_mainingferma(message)
        return
    elif command in ['upd', 'обновления', 'списокобновлений']:
        print("✅ Распознана команда: обновления")
        cmd_upd(message)
        return
    elif command in ['картинка', 'picture', 'фото']:
        cmd_picture(message)
        return
    elif command in ['удалитькартинку', 'delpicture', 'удалитьфото']:
       cmd_delpicture(message)
       return
    elif command in ['win', 'выигрыш', 'победа']:
        cmd_winimage(message)
        return
    elif command in ['lose', 'проигрыш', 'поражение']:
        cmd_loseimage(message)
        return
    elif command in ['setupd', 'установитьобновления']:
        print("✅ Распознана команда: установитьобновления")
        cmd_setupd(message)
        return
    elif command in ['биткоин', 'bitcoin', 'btc']:
        print("✅ Распознана команда: биткоин")
        cmd_bitcoin(message)
        return
    elif command in ['обменять', 'exchange', 'обмен']:
        print("✅ Распознана команда: обменять")
        cmd_exchange(message)
        return
    elif command in ['переводбиткоин', 'transferbtc', 'переводbtc']:
        print("✅ Распознана команда: переводбиткоин")
        cmd_transferbtc(message)
        return
    elif command in ['замес', 'zames']:
        print("✅ Распознана команда: замес")
        cmd_zames(message)
        return
    elif command in ['список', 'list']:
        print("✅ Распознана команда: список")
        cmd_spisok(message)
        return
    elif command in ['донат', 'donat', 'дон']:
        print("✅ Распознана команда: донат")
        cmd_donat(message)
        return
    elif command in ['giverub', 'выдатьрубли']:
        print("✅ Распознана команда: выдатьрубли")
        cmd_giverub(message)
        return
    elif command in ['курс', 'rate']:
        print("✅ Распознана команда: курс")
        cmd_rate(message)
        return
    elif command in ['изменитькурс', 'changerate']:
        print("✅ Распознана команда: изменитькурс")
        cmd_changerate(message)
        return
    elif command in ['продатьбиткоин', 'sellbtc', 'продать']:
        print("✅ Распознана команда: продать")
        cmd_sellbtc(message)
        return

    # Поиск команды в словаре
    for cmd, aliases in COMMANDS.items():
        if command in aliases:
            print(f"✅ Распознана команда из словаря: {cmd} (алиас: {command})")
            func_name = f"cmd_{cmd}"
            if func_name in globals():
                globals()[func_name](message)
                return
    
    print(f"❌ Команда не распознана: {command}")
                
# ---------- КОМАНДЫ ----------
def cmd_reg(message):
    # Проверяем, что это действительно команда регистрации
    parts = message.text.split()
    
    # Если команда вызвана без параметров, устанавливаем имя как first_name
    if len(parts) < 2:
        new_nick = message.from_user.first_name
    else:
        new_nick = ' '.join(parts[1:])
    
    # Ограничиваем длину ника
    if len(new_nick) > 32:
        bot.reply_to(message, "❌ Ник не может быть длиннее 32 символов")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET nick = ? WHERE user_id = ?', (new_nick, message.from_user.id))
    conn.commit()
    conn.close()
    
    bot.reply_to(message, f"✅ Регистрация успешна! Ваш ник: {new_nick}")

def cmd_help(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    level = check_admin_level(user_id, chat_id)
    is_bot_admin = check_bot_admin(user_id)

    help_text = f"📋 Доступные команды\nВаш уровень: {get_admin_level_name(level)}\n\n"
    help_text += "👤 Для всех:\n"
    help_text += "• /profile - Показать профиль\n"
    help_text += "• /name [ник] - Установить ник\n"
    help_text += "• /топ - Топ 30 по твистам\n"
    help_text += "• /список - Список активных промокодов\n"
    help_text += "• /promo [код] - Активировать промокод\n"
    help_text += "• /kaz [ставка] - Казино\n"
    help_text += "• /донат - Донат услуги\n"
    help_text += "• /pay [сумма] - Перевести твисты\n"
    help_text += "• /биткоин - Показать баланс биткоинов\n"
    help_text += "• /обменять [сумма] - Обменять твисты на биткоины\n"
    help_text += "• /переводбиткоин [сумма] - Перевести биткоины\n"
    help_text += "• /продать [количество] - Продать биткоины по текущему курсу\n"
    help_text += "• /курс - Текущий курс биткоина\n"
    help_text += "• /замес [см] - Бросить вызов на замес пиписьки\n"
    help_text += "• /staff - Список администрации\n"
    help_text += "• /hi - Показать приветствие группы\n"
    help_text += "• /pravila - Показать правила группы\n"
    help_text += "• /хуй - Узнать размер пиписьки\n"
    help_text += "• /украсть - Украсть пипиську у другого (раз в 4 часа)\n"
    help_text += "• /топписька - Топ самых больших пиписьек\n"
    help_text += "• /магазин  - Магазин видеокарт для майнинга\n"
    help_text += "• /ферма - Твоя майнинг ферма\n"
    help_text += "• /upd - Список последних обновлений бота\n\n"
    help_text += "• /бонус - Получить бонус\n\n"
    help_text += "• /картинка - Поставить картинку в профиль\n\n"
    help_text += "• /event - Эвент бота\n\n"
    help_text += "• /бой - Бой с боссом (эвент)\n\n"
    help_text += "• /gif - Установить гифку в профиль\n\n"

    if level > 0:
        help_text += "🛡️ Команды администратора:\n"
        perms = get_level_permissions(level)
        if perms['can_warn']:
            help_text += "• /warn [причина] - Выдать предупреждение\n"
        if perms['can_mute']:
            help_text += "• /mute [время] [причина] - Замутить\n"
        if perms['can_unmute']:
            help_text += "• /unmute - Снять мут\n"
        if perms['can_kick']:
            help_text += "• /kick [причина] - Кикнуть\n"
        if perms['can_ban']:
            help_text += "• /ban [время] [причина] - Забанить\n"
        if perms['can_unban']:
            help_text += "• /unban - Снять бан\n"
        if perms['can_muteall']:
            help_text += "• /тишина [время] - Режим тишины\n"
        if perms['can_clear']:
            help_text += "• /clear [кол-во] - Удалить сообщения\n"
        if perms['can_setname']:
            help_text += "• /setname [ник] - Сменить ник\n"
        if perms['can_makeadmin']:
            help_text += "• /makeadmin [уровень] - Назначить админа\n"
        if perms['can_unadmin']:
            help_text += "• /unadmin - Снять админа\n"
        help_text += "• /sethi [текст] - Установить приветствие\n"
        help_text += "• /addpravila [текст] - Установить правила\n\n"

    if is_bot_admin or user_id == OWNER_ID:
        help_text += "🤖 Для администраторов бота:\n"
        help_text += "• /выдать [кол-во] - Выдать твисты\n"
        help_text += "• /забрать [кол-во] - Забрать твисты\n"
        help_text += "• /asetname [ник] - Сменить ник\n"
        help_text += "• /createpromo - Создать промо\n"
        help_text += "• /delpromo [код] - Удалить промокод\n"
        help_text += "• /giverub [кол-во] - Выдать рубли (только владелец)\n\n"

    if user_id == OWNER_ID:
        help_text += "👑 Для владельца бота:\n"
        help_text += "• /verificate - Верифицировать\n"
        help_text += "• /setmyadmin - Получить админку 6\n"
        help_text += "• /setadminbot - Назначить админа бота\n"
        help_text += "• /lixoradka [%] - Изменить шанс казино\n"
        help_text += "• /stoplixoradka [%] - Вернуть шанс казино\n"
        help_text += "• /givetoper - Выдать префикс топера\n"
        help_text += "• /obnulenie - Обнулить балансы всех пользователей\n"
        help_text += "• /setupd [текст] - Добавить запись в список обновлений\n"
        help_text += "• /изменитькурс [новая цена] - Изменить курс биткоина\n"
        help_text += "• /giverub - Выдать донат\n\n"
        help_text += "• /obnulbitoc - Обнулить биткоины у всех\n\n"
        help_text += "• /lose - Изменить картинку проигрыша казино\n\n"
        help_text += "• /win - Изменить картинку выигрыша казино\n\n"
        help_text += "• /givemedal - Выдать медаль в профиль (эвент)\n\n"
        help_text += "• /statsevent -Посмотреть самого активного пользователя(эвент)\n\n"

    bot.reply_to(message, help_text)

# ===== ФУНКЦИЯ cmd_profile =====
def cmd_profile(message):
    target = get_target_user(message) or message.from_user
    user_id = target.id
    
    # Проверяем, что это не бот
    if user_id == bot.get_me().id:
        bot.reply_to(message, "❌ Нельзя посмотреть профиль бота")
        return

    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    # Получаем данные пользователя
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    
    if not user:
        bot.reply_to(message, f"❌ Пользователь {target.first_name} не найден в базе")
        conn.close()
        return
    
    # Получаем названия колонок
    col_names = [description[0] for description in cursor.description]
    
    # Создаем словарь с данными
    user_dict = {}
    for i, col_name in enumerate(col_names):
        if i < len(user):
            user_dict[col_name] = user[i]
    
    # Получаем значения
    nick = user_dict.get('nick', target.first_name)
    twists = user_dict.get('twists', 0)
    bitcoins = user_dict.get('bitcoins', 0.0)
    piska_size = user_dict.get('piska_size', 0)
    rub_balance = user_dict.get('rub_balance', 0)
    verified = user_dict.get('verified', 0)
    
    # Проверяем статус пользователя
    is_owner = user_id == OWNER_ID
    is_bot_admin = check_bot_admin(user_id) and not is_owner
    
    # Получаем медали
    cursor.execute('SELECT medal_bravery FROM medals WHERE user_id = ?', (user_id,))
    medal = cursor.fetchone()
    medal_bravery = medal[0] if medal else 0
    
    # Получаем медиа профиля если есть
    cursor.execute('SELECT file_id, media_type FROM profile_media WHERE user_id = ?', (user_id,))
    media = cursor.fetchone()
    has_media = media is not None
    file_id = media[0] if media else None
    media_type = media[1] if media else None
    
    conn.close()
    
    # Формируем текст профиля
    profile_text = f"🏠 Профиль • {nick}\n"
    
    if is_owner:
        profile_text += f"👑 ВЛАДЕЛЕЦ БОТА\n"
    elif is_bot_admin:
        profile_text += f"👺 АДМИН БОТА\n"
    
    if verified:
        profile_text += f"✅ Верифицирован\n"
    
    profile_text += f"💰 Баланс: {twists:,} твистов\n"
    profile_text += f"🍌 Писька: {piska_size} см\n"
    profile_text += f"💎 Донат: {rub_balance}₽\n"
    profile_text += f"🤑 Биткоины: {bitcoins} BTC\n"
    
    if medal_bravery > 0:
        profile_text += f"🏅 Медали: 🥇 За отвагу в чате (x{medal_bravery})\n"
    
    # Отправляем сообщение с обработкой ошибки
    if has_media and file_id:
        try:
            if media_type == 'photo':
                bot.send_photo(
                    message.chat.id,
                    file_id,
                    caption=profile_text,
                    reply_to_message_id=message.message_id
                )
            elif media_type == 'animation':
                bot.send_animation(
                    message.chat.id,
                    file_id,
                    caption=profile_text,
                    reply_to_message_id=message.message_id
                )
        except Exception as e:
            # Если ошибка с медиа, удаляем его из базы и отправляем без медиа
            print(f"Ошибка с медиа профиля: {e}")
            
            # Удаляем нерабочее медиа из базы
            conn2 = sqlite3.connect('bot_data.db')
            cursor2 = conn2.cursor()
            cursor2.execute('DELETE FROM profile_media WHERE user_id = ?', (user_id,))
            conn2.commit()
            conn2.close()
            
            # Отправляем без медиа
            bot.reply_to(message, profile_text)
    else:
        # Если нет медиа, отправляем только текст
        bot.reply_to(message, profile_text)

@bot.message_handler(content_types=['photo', 'animation'])
def handle_media(message):
    """Обрабатывает сообщения с фотографиями и гифками"""
    if message.chat.type not in ['group', 'supergroup']:
        return

    user = message.from_user
    create_user_if_not_exists(user.id, user.username, user.first_name, user.last_name)

    # Проверяем мут и режим тишины
    muted, until_time, reason = is_muted(user.id, message.chat.id)
    if muted:
        bot.delete_message(message.chat.id, message.message_id)
        return

    silence, until_time = is_silence_mode(message.chat.id)
    if silence and not check_admin(user.id, message.chat.id):
        bot.delete_message(message.chat.id, message.message_id)
        return

    # Проверяем, есть ли в подписи к медиа команда
    if message.caption:
        caption_text = message.caption.lower().strip()

        # Команда для медиа профиля
        if caption_text in ['/картинка', '/picture', '/фото', '/gif', '/гиф']:
            save_profile_media(message)
            return

    # Если это просто медиа без команды, обновляем статистику
    update_user_stats(user.id, message.chat.id)

# ===== ФУНКЦИИ ДЛЯ МЕДИА ПРОФИЛЯ =====
def save_profile_media(message):
    """Сохраняет фото или гифку как медиа профиля"""
    user_id = message.from_user.id
    
    # Определяем тип медиа и получаем file_id
    if message.photo:
        # Если фото - берем максимальный размер
        media = message.photo[-1]
        file_id = media.file_id
        media_type = 'photo'
        media_name = "Фото"
    elif message.animation:
        # Если гифка
        media = message.animation
        file_id = media.file_id
        media_type = 'animation'
        media_name = "GIF"
    else:
        bot.reply_to(message, "❌ Поддерживаются только фото и GIF")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    # Сохраняем или обновляем медиа профиля
    cursor.execute('''
        INSERT OR REPLACE INTO profile_media (user_id, file_id, media_type, updated_date)
        VALUES (?, ?, ?, ?)
    ''', (user_id, file_id, media_type, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    conn.commit()
    conn.close()
    
    bot.reply_to(message, f"✅ {media_name} профиля успешно сохранено!")

# ===== КОМАНДА ДЛЯ УДАЛЕНИЯ КАРТИНКИ =====
def cmd_delpicture(message):
    """Удаляет медиа из профиля"""
    user_id = message.from_user.id
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM profile_media WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    bot.reply_to(message, "✅ Медиа профиля удалено")

# ===== КОМАНДА ДЛЯ УДАЛЕНИЯ КАРТИНКИ =====
def cmd_delpicture(message):
    """Удаляет медиа из профиля"""
    user_id = message.from_user.id
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM profile_media WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    bot.reply_to(message, "✅ Медиа профиля удалено")


def cmd_name(message):
    # Проверяем, что команда вызвана с параметрами
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "❌ Укажите ник. Пример: /name НовыйНик")
        return

    # Проверяем, что это действительно команда /name
    if not message.text.startswith('/') and not message.text.lower().startswith(tuple(['name', 'ник', 'никнейм'])):
        return

    new_nick = ' '.join(parts[1:])

    # Ограничиваем длину ника
    if len(new_nick) > 32:
        bot.reply_to(message, "❌ Ник не может быть длиннее 32 символов")
        return

    # Запрещаем специальные символы в нике
    if any(char in new_nick for char in ['@', '#', '$', '%', '&', '*', '(', ')', '=', '+', '{', '}', '[', ']', '|', '\\', ';', ':', '"', "'", '<', '>', ',', '?', '/']):
        bot.reply_to(message, "❌ Ник не может содержать специальные символы")
        return

    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET nick = ? WHERE user_id = ?', (new_nick, message.from_user.id))
    conn.commit()
    conn.close()

    bot.reply_to(message, f"✅ Ваш ник изменен на: {new_nick}")

def cmd_setname(message):
    if not check_permission(message.from_user.id, message.chat.id, 'can_setname'):
        bot.reply_to(message, "❌ Нет прав")
        return
    target = get_target_user(message)
    if not target:
        bot.reply_to(message, "❌ Ответьте на сообщение")
        return
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Укажите ник")
        return
    new_nick = ' '.join(message.text.split()[1:])
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET nick = ? WHERE user_id = ?', (new_nick, target.id))
    conn.commit()
    conn.close()
    bot.reply_to(message, f"✅ Ник изменен на: {new_nick}")
    
    def cmd_winimage(message):
     if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Только для владельца бота")
        return
    
    bot.reply_to(message, "Отправьте фото с подписью /win чтобы установить картинку выигрыша")

def cmd_loseimage(message):
    """Устанавливает картинку проигрыша в казино (только для владельца)"""
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Только для владельца бота")
        return
    
    bot.reply_to(message, "Отправьте фото с подписью /lose чтобы установить картинку проигрыша")

def cmd_kazino(message):
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Укажите ставку")
        return
    try:
        bet = int(message.text.split()[1])
    except:
        bot.reply_to(message, "❌ Ставка должна быть числом")
        return
    if bet <= 0:
        bot.reply_to(message, "❌ Ставка должна быть положительной")
        return
    
    user_id = message.from_user.id
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT twists FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    if not result or result[0] < bet:
        bot.reply_to(message, "❌ Недостаточно твистов")
        conn.close()
        return
    
    cursor.execute('SELECT win_chance FROM casino_settings WHERE id = 1')
    win_chance = cursor.fetchone()[0]
    
    # Получаем картинки казино
    cursor.execute('SELECT win_image, lose_image FROM casino_images WHERE id = 1')
    images = cursor.fetchone()
    win_image = images[0] if images else None
    lose_image = images[1] if images else None
    
    win = random.randint(1, 100) <= win_chance
    if win:
        cursor.execute('UPDATE users SET twists = twists + ? WHERE user_id = ?', (bet, user_id))
        result_text = f"🎉 Вы выиграли {bet} твистов!"
        image_id = win_image
    else:
        cursor.execute('UPDATE users SET twists = twists - ? WHERE user_id = ?', (bet, user_id))
        result_text = f"😢 Вы проиграли {bet} твистов"
        image_id = lose_image
    
    conn.commit()
    conn.close()
    
    # Отправляем результат с картинкой если есть
    if image_id:
        bot.send_photo(
            message.chat.id,
            image_id,
            caption=result_text,
            reply_to_message_id=message.message_id
        )
    else:
        bot.reply_to(message, result_text)
    
def cmd_тишина(message):
    # Заглушка, чтобы ничего не делала
     pass

def cmd_mute(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    if not check_permission(user_id, chat_id, 'can_mute'):
        bot.reply_to(message, "❌ Нет прав")
        return
    
    target = get_target_user(message)
    if not target:
        bot.reply_to(message, "❌ Ответьте на сообщение пользователя")
        return
    
    if target.id == user_id:
        bot.reply_to(message, "❌ Нельзя замутить самого себя")
        return
    
    if check_admin(target.id, chat_id) and user_id != OWNER_ID:
        bot.reply_to(message, "❌ Нельзя замутить администратора")
        return
    
    args = message.text.split()
    time_str = '10m'
    reason = "Причина не указана"
    
    if len(args) >= 2:
        if parse_time(args[1]):
            time_str = args[1]
            if len(args) >= 3:
                reason = ' '.join(args[2:])
        else:
            reason = ' '.join(args[1:])
    
    seconds = parse_time(time_str)
    if not seconds:
        seconds = 600
    
    max_time = get_level_permissions(check_admin_level(user_id, chat_id))['max_mute_time']
    if seconds > max_time:
        bot.reply_to(message, f"❌ Максимальное время мута для вашего уровня: {max_time//60} минут")
        return
    
    until_time = int(time.time()) + seconds
    
    muted, existing_until, _ = is_muted(target.id, chat_id)
    if muted:
        remove_mute(target.id, chat_id)
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO muted_users (user_id, chat_id, until_time, reason, muted_by)
        VALUES (?, ?, ?, ?, ?)
    ''', (target.id, chat_id, until_time, reason, user_id))
    conn.commit()
    conn.close()
    
    if seconds < 60:
        time_str_formatted = f"{seconds} секунд"
    elif seconds < 3600:
        time_str_formatted = f"{seconds//60} минут"
    elif seconds < 86400:
        time_str_formatted = f"{seconds//3600} часов"
    else:
        time_str_formatted = f"{seconds//86400} дней"
    
    bot.reply_to(message, f"🔇 Пользователь {target.first_name} замьючен на {time_str_formatted}\nПричина: {reason}")

def cmd_unmute(message):
    if not check_permission(message.from_user.id, message.chat.id, 'can_unmute'):
        bot.reply_to(message, "❌ Нет прав")
        return
    target = get_target_user(message)
    if not target:
        bot.reply_to(message, "❌ Ответьте на сообщение")
        return
    
    muted, _, _ = is_muted(target.id, message.chat.id)
    if not muted:
        bot.reply_to(message, f"❌ Пользователь {target.first_name} не находится в муте")
        return
    
    remove_mute(target.id, message.chat.id)
    bot.reply_to(message, f"✅ С пользователя {target.first_name} снят мут")

def cmd_ban(message):
    if not check_permission(message.from_user.id, message.chat.id, 'can_ban'):
        bot.reply_to(message, "❌ Нет прав")
        return
    target = get_target_user(message)
    if not target:
        bot.reply_to(message, "❌ Ответьте на сообщение")
        return
    
    try:
        bot.ban_chat_member(message.chat.id, target.id)
        bot.reply_to(message, f"🔨 Пользователь забанен")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

def cmd_kick(message):
    if not check_permission(message.from_user.id, message.chat.id, 'can_kick'):
        bot.reply_to(message, "❌ Нет прав")
        return
    target = get_target_user(message)
    if not target:
        bot.reply_to(message, "❌ Ответьте на сообщение")
        return
    
    try:
        bot.ban_chat_member(message.chat.id, target.id)
        bot.unban_chat_member(message.chat.id, target.id)
        bot.reply_to(message, f"👢 Пользователь кикнут")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

def cmd_warn(message):
    if not check_permission(message.from_user.id, message.chat.id, 'can_warn'):
        bot.reply_to(message, "❌ Нет прав")
        return
    target = get_target_user(message)
    if not target:
        bot.reply_to(message, "❌ Ответьте на сообщение")
        return
    
    reason = ' '.join(message.text.split()[1:]) if len(message.text.split()) > 1 else "Без причины"
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO warns (user_id, chat_id, reason, warned_by, warn_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (target.id, message.chat.id, reason, message.from_user.id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    cursor.execute('SELECT COUNT(*) FROM warns WHERE user_id = ? AND chat_id = ?', (target.id, message.chat.id))
    warns_count = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    
    bot.reply_to(message, f"⚠️ Пользователю {target.first_name} выдано предупреждение {warns_count}/3\nПричина: {reason}")
    
    if warns_count >= 3:
        until_time = int(time.time()) + 3600
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO muted_users (user_id, chat_id, until_time, reason, muted_by) VALUES (?, ?, ?, ?, ?)',
                      (target.id, message.chat.id, until_time, "3 предупреждения", message.from_user.id))
        cursor.execute('DELETE FROM warns WHERE user_id = ? AND chat_id = ?', (target.id, message.chat.id))
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, f"🔇 Пользователь {target.first_name} получил мут на 1 час (3/3 предупреждений)")

def cmd_unwarn(message):
    if not check_permission(message.from_user.id, message.chat.id, 'can_warn'):
        bot.reply_to(message, "❌ Нет прав")
        return
    target = get_target_user(message)
    if not target:
        bot.reply_to(message, "❌ Ответьте на сообщение")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM warns
        WHERE user_id = ? AND chat_id = ?
        AND id = (SELECT id FROM warns WHERE user_id = ? AND chat_id = ? ORDER BY id DESC LIMIT 1)
    ''', (target.id, message.chat.id, target.id, message.chat.id))
    
    cursor.execute('SELECT COUNT(*) FROM warns WHERE user_id = ? AND chat_id = ?', (target.id, message.chat.id))
    warns_count = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    
    bot.reply_to(message, f"✅ Последнее предупреждение снято. У пользователя {target.first_name} осталось {warns_count} предупреждений")

def cmd_clear(message):
    if not check_permission(message.from_user.id, message.chat.id, 'can_clear'):
        bot.reply_to(message, "❌ Нет прав")
        return
    
    amount = 1
    if len(message.text.split()) > 1:
        try:
            amount = int(message.text.split()[1])
        except:
            pass
    
    try:
        bot.delete_message(message.chat.id, message.message_id)
        if message.reply_to_message:
            msg_id = message.reply_to_message.message_id
            for i in range(min(amount, 10)):
                try:
                    bot.delete_message(message.chat.id, msg_id - i)
                except:
                    pass
        bot.reply_to(message, f"✅ Удалено {amount} сообщений")
    except:
        pass

def cmd_staff(message):
    try:
        admins = bot.get_chat_administrators(message.chat.id)
        text = "👥 Администрация:\n\n"
        for admin in admins:
            user = admin.user
            status = "👑" if admin.status == 'creator' else "🛡️"
            text += f"{status} {user.first_name}\n"
        bot.reply_to(message, text)
    except:
        bot.reply_to(message, "❌ Ошибка")

def cmd_makeadmin(message):
    if not check_permission(message.from_user.id, message.chat.id, 'can_makeadmin'):
        bot.reply_to(message, "❌ Нет прав")
        return
    target = get_target_user(message)
    if not target:
        bot.reply_to(message, "❌ Ответьте на сообщение")
        return
    
    level = 1
    if len(message.text.split()) > 1:
        try:
            level = int(message.text.split()[1])
        except:
            pass
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO admins (user_id, chat_id, admin_level, appointed_by, appointed_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (target.id, message.chat.id, level, message.from_user.id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()
    bot.reply_to(message, f"✅ Пользователь {target.first_name} назначен администратором с уровнем {level}")

def cmd_unadmin(message):
    if not check_permission(message.from_user.id, message.chat.id, 'can_unadmin'):
        bot.reply_to(message, "❌ Нет прав")
        return
    target = get_target_user(message)
    if not target:
        bot.reply_to(message, "❌ Ответьте на сообщение")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM admins WHERE user_id = ? AND chat_id = ?', (target.id, message.chat.id))
    conn.commit()
    conn.close()
    bot.reply_to(message, f"✅ Пользователь {target.first_name} снят с должности администратора")

def cmd_verificate(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Только для владельца")
        return
    target = get_target_user(message)
    if not target:
        bot.reply_to(message, "❌ Ответьте на сообщение")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET verified = 1 WHERE user_id = ?', (target.id,))
    conn.commit()
    conn.close()
    bot.reply_to(message, f"✅ Пользователь {target.first_name} верифицирован")

def cmd_setmyadmin(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Только для владельца")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO admins (user_id, chat_id, admin_level, appointed_date) VALUES (?, ?, ?, ?)',
                  (OWNER_ID, message.chat.id, 6, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()
    bot.reply_to(message, "✅ Вы получили админку 6 уровня в этой группе")

def cmd_setadminbot(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Только для владельца")
        return
    target = get_target_user(message)
    if not target:
        bot.reply_to(message, "❌ Ответьте на сообщение")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO bot_admins (user_id) VALUES (?)', (target.id,))
    conn.commit()
    conn.close()
    bot.reply_to(message, f"✅ Пользователь {target.first_name} назначен администратором бота")

def cmd_givetwist(message):
    user_id = message.from_user.id
    
    if not check_bot_admin(user_id) and user_id != OWNER_ID:
        bot.reply_to(message, "❌ У вас нет прав администратора бота")
        return
    
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответьте на сообщение пользователя, которому хотите выдать твисты")
        return
    
    target = message.reply_to_message.from_user
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "❌ Использование: /выдать [количество] (ответом на сообщение)")
        return
    
    try:
        amount = int(args[1])
        if amount <= 0:
            bot.reply_to(message, "❌ Сумма должна быть положительной")
            return
    except ValueError:
        bot.reply_to(message, "❌ Неверная сумма. Укажите число")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET twists = twists + ? WHERE user_id = ?', (amount, target.id))
    conn.commit()
    
    cursor.execute('SELECT twists FROM users WHERE user_id = ?', (target.id,))
    new_balance = cursor.fetchone()[0]
    conn.close()
    
    bot.reply_to(message, f"✅ Пользователю {target.first_name} выдано {amount} твистов\n💰 Новый баланс: {new_balance}")

def cmd_deltwist(message):
    user_id = message.from_user.id
    
    if not check_bot_admin(user_id) and user_id != OWNER_ID:
        bot.reply_to(message, "❌ У вас нет прав администратора бота")
        return
    
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответьте на сообщение пользователя, у которого хотите забрать твисты")
        return
    
    target = message.reply_to_message.from_user
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "❌ Использование: /забрать [количество] (ответом на сообщение)")
        return
    
    try:
        amount = int(args[1])
        if amount <= 0:
            bot.reply_to(message, "❌ Сумма должна быть положительной")
            return
    except ValueError:
        bot.reply_to(message, "❌ Неверная сумма. Укажите число")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT twists FROM users WHERE user_id = ?', (target.id,))
    result = cursor.fetchone()
    current_twists = result[0] if result else 0
    
    if current_twists < amount:
        bot.reply_to(message, f"❌ У пользователя недостаточно твистов. Текущий баланс: {current_twists}")
        conn.close()
        return
    
    cursor.execute('UPDATE users SET twists = twists - ? WHERE user_id = ?', (amount, target.id))
    conn.commit()
    
    cursor.execute('SELECT twists FROM users WHERE user_id = ?', (target.id,))
    new_balance = cursor.fetchone()[0]
    conn.close()
    
    bot.reply_to(message, f"✅ У пользователя {target.first_name} забрано {amount} твистов\n💰 Новый баланс: {new_balance}")
    def cmd_asetname(message):
     if not check_bot_admin(message.from_user.id) and message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Нет прав")
        return
    target = get_target_user(message)
    if not target:
        bot.reply_to(message, "❌ Ответьте на сообщение")
        return
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Укажите ник")
        return
    
    new_nick = ' '.join(message.text.split()[1:])
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET nick = ? WHERE user_id = ?', (new_nick, target.id))
    conn.commit()
    conn.close()
    bot.reply_to(message, f"✅ Ник пользователя {target.first_name} изменен на: {new_nick}")

def cmd_createpromo(message):
    if not check_bot_admin(message.from_user.id) and message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ У вас нет прав администратора бота")
        return
    
    args = message.text.split()
    if len(args) < 4:
        bot.reply_to(message, "❌ Использование: /createpromo [код] [кол-во активаций] [твисты]")
        return
    
    code = args[1].upper()
    try:
        max_activations = int(args[2])
        twists = int(args[3])
        if max_activations <= 0 or twists <= 0:
            bot.reply_to(message, "❌ Числа должны быть положительными")
            return
    except:
        bot.reply_to(message, "❌ Неверные числа")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM promocodes WHERE code = ?', (code,))
    if cursor.fetchone():
        bot.reply_to(message, f"❌ Промокод {code} уже существует")
        conn.close()
        return
    
    cursor.execute('INSERT INTO promocodes (code, twists, max_activations, current_activations) VALUES (?, ?, ?, 0)',
                  (code, twists, max_activations))
    
    conn.commit()
    conn.close()
    bot.reply_to(message, f"✅ Промокод {code} создан! Твистов: {twists}, активаций: {max_activations}")

def cmd_delpromo(message):
    if not check_bot_admin(message.from_user.id) and message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ У вас нет прав администратора бота")
        return
    
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Использование: /delpromo [название промокода]")
        return
    
    code = message.text.split()[1].upper()
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM promocodes WHERE code = ?', (code,))
    promo = cursor.fetchone()
    
    if not promo:
        bot.reply_to(message, f"❌ Промокод {code} не найден")
        
        cursor.execute('SELECT code FROM promocodes')
        all_promos = cursor.fetchall()
        if all_promos:
            promo_list = ", ".join([p[0] for p in all_promos])
            bot.reply_to(message, f"📋 Существующие промокоды: {promo_list}")
        else:
            bot.reply_to(message, "📋 Промокодов пока нет")
        
        conn.close()
        return
    
    cursor.execute('DELETE FROM promocodes WHERE code = ?', (code,))
    cursor.execute('DELETE FROM promo_activations WHERE promo_code = ?', (code,))
    
    conn.commit()
    conn.close()
    
    bot.reply_to(message, f"✅ Промокод {code} успешно удален!")

def cmd_promo(message):
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Укажите код")
        return
    
    code = message.text.split()[1].upper()
    user_id = message.from_user.id
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM promocodes WHERE code = ?', (code,))
    promo = cursor.fetchone()
    
    if not promo:
        bot.reply_to(message, "❌ Промокод не найден")
        conn.close()
        return
    
    twists_amount = promo[1]
    max_activations = promo[2]
    current_activations = promo[3]
    
    cursor.execute('SELECT * FROM promo_activations WHERE user_id = ? AND promo_code = ?', (user_id, code))
    if cursor.fetchone():
        bot.reply_to(message, "❌ Вы уже активировали этот промокод")
        conn.close()
        return
    
    if current_activations >= max_activations:
        bot.reply_to(message, "❌ Промокод больше недействителен")
        conn.close()
        return
    
    cursor.execute('UPDATE users SET twists = twists + ? WHERE user_id = ?', (twists_amount, user_id))
    cursor.execute('UPDATE promocodes SET current_activations = current_activations + 1 WHERE code = ?', (code,))
    cursor.execute('INSERT INTO promo_activations (user_id, promo_code) VALUES (?, ?)', (user_id, code))
    
    conn.commit()
    conn.close()
    
    bot.reply_to(message, f"✅ Промокод активирован! Вы получили {twists_amount} твистов")

def cmd_toptwist(message):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, nick, twists FROM users WHERE twists > 0 ORDER BY twists DESC LIMIT 30')
    top = cursor.fetchall()
    conn.close()
    
    if not top:
        bot.reply_to(message, "📊 Топ твистов пуст")
        return
    
    text = "🏆 ТОП 30 ПО ТВИСТАМ:\n\n"
    for i, (user_id, nick, twists) in enumerate(top, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "📌"
        name = nick or f"ID {user_id}"
        text += f"{medal} {i}. {name} — {twists}\n"
    
    bot.reply_to(message, text)

def cmd_sethi(message):
    if not check_admin(message.from_user.id, message.chat.id):
        bot.reply_to(message, "❌ Только для админов")
        return
    
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Укажите текст")
        return
    
    text = ' '.join(message.text.split()[1:])
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO greetings (chat_id, greeting_text, set_by, set_date) VALUES (?, ?, ?, ?)',
                  (message.chat.id, text, message.from_user.id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()
    bot.reply_to(message, "✅ Приветствие установлено")

def cmd_hi(message):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT greeting_text FROM greetings WHERE chat_id = ?', (message.chat.id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        bot.reply_to(message, f"👋 {result[0]}")
    else:
        bot.reply_to(message, "❌ Приветствие не установлено")

def cmd_addpravila(message):
    if not check_admin(message.from_user.id, message.chat.id):
        bot.reply_to(message, "❌ Только для админов")
        return
    
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Укажите текст")
        return
    
    text = ' '.join(message.text.split()[1:])
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO rules (chat_id, rules_text, set_by, set_date) VALUES (?, ?, ?, ?)',
                  (message.chat.id, text, message.from_user.id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()
    bot.reply_to(message, "✅ Правила установлены")

def cmd_pravila(message):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT rules_text FROM rules WHERE chat_id = ?', (message.chat.id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        bot.reply_to(message, f"📜 {result[0]}")
    else:
        bot.reply_to(message, "❌ Правила не установлены")

def cmd_pay(message):
    user_id = message.from_user.id
    
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответьте на сообщение пользователя, которому хотите перевести твисты")
        return
    
    target = message.reply_to_message.from_user
    if target.id == user_id:
        bot.reply_to(message, "❌ Нельзя перевести твисты самому себе")
        return
    
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Использование: /pay [сумма]")
        return
    
    try:
        amount = int(message.text.split()[1])
        if amount <= 0:
            bot.reply_to(message, "❌ Сумма должна быть положительной")
            return
    except:
        bot.reply_to(message, "❌ Неверная сумма")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT twists FROM users WHERE user_id = ?', (user_id,))
    sender_twists = cursor.fetchone()
    if not sender_twists or sender_twists[0] < amount:
        bot.reply_to(message, "❌ У вас недостаточно твистов")
        conn.close()
        return
    
    cursor.execute('UPDATE users SET twists = twists - ? WHERE user_id = ?', (amount, user_id))
    cursor.execute('UPDATE users SET twists = twists + ? WHERE user_id = ?', (amount, target.id))
    
    conn.commit()
    conn.close()
    
    bot.reply_to(message, f"✅ Вы перевели {amount} твистов пользователю {target.first_name}")
    
@bot.message_handler(commands=['bonus', 'бонус'])
def handle_bonus_command(message):
    """Обработчик команды /бонус"""
    cmd_bonus(message)


def cmd_lixoradka(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Только для владельца")
        return
    
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Укажите процент")
        return
    
    try:
        percent = int(message.text.split()[1])
        if percent < 1 or percent > 100:
            bot.reply_to(message, "❌ От 1 до 100")
            return
    except:
        bot.reply_to(message, "❌ Неверное число")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE casino_settings SET win_chance = ? WHERE id = 1', (percent,))
    conn.commit()
    conn.close()
    
    bot.reply_to(message, f"✅ Шанс выигрыша в казино изменен на {percent}%")

def cmd_stoplixoradka(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Только для владельца")
        return
    
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Укажите процент")
        return
    
    try:
        percent = int(message.text.split()[1])
        if percent < 1 or percent > 100:
            bot.reply_to(message, "❌ От 1 до 100")
            return
    except:
        bot.reply_to(message, "❌ Неверное число")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE casino_settings SET win_chance = ? WHERE id = 1', (percent,))
    conn.commit()
    conn.close()
    
    bot.reply_to(message, f"✅ Шанс выигрыша в казино возвращен к {percent}%")
    def cmd_givetoper(message):
     if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Только для владельца")
        return
    
    target = get_target_user(message)
    if not target:
        bot.reply_to(message, "❌ Ответьте на сообщение")
        return
    
    bot.reply_to(message, f"✅ Префикс топера выдан пользователю {target.first_name}")


# ===== НОВЫЕ КОМАНДЫ =====
def cmd_obnulenie(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Только для владельца бота")
        return
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Да, обнулить", callback_data="obnulenie_confirm"),
        types.InlineKeyboardButton("❌ Отмена", callback_data="obnulenie_cancel")
    )
    
    bot.reply_to(message, "⚠️ ВЫ УВЕРЕНЫ? Это обнулит баланс ТВИСТОВ у ВСЕХ пользователей!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('obnulenie_'))
def obnulenie_callback(call):
    if call.from_user.id != OWNER_ID:
        bot.answer_callback_query(call.id, "Это не для вас")
        return
    
    if call.data == "obnulenie_confirm":
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET twists = 0')
        conn.commit()
        conn.close()
        
        bot.edit_message_text("✅ Все балансы успешно обнулены!", call.message.chat.id, call.message.message_id)
    else:
        bot.edit_message_text("❌ Операция отменена", call.message.chat.id, call.message.message_id)

def cmd_hui(message):
    user_id = message.from_user.id
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT piska_size, piska_last_grow FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    current_size = result[0] if result and result[0] else 0
    last_grow = result[1] if result and result[1] else None
    
    if last_grow:
        last_grow_time = datetime.strptime(last_grow, '%Y-%m-%d %H:%M:%S')
        time_diff = datetime.now() - last_grow_time
        if time_diff.total_seconds() < 7200:
            hours_left = 2 - (time_diff.total_seconds() / 3600)
            bot.reply_to(message, f"⏳ Пиписька еще растет! Подождите {hours_left:.1f} часов")
            conn.close()
            return
    
    if random.randint(1, 100) <= 5:
        growth = 10
    else:
        growth = random.randint(1, 9)
    
    new_size = current_size + growth
    
    cursor.execute('UPDATE users SET piska_size = ?, piska_last_grow = ? WHERE user_id = ?',
                  (new_size, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
    conn.commit()
    conn.close()
    
    if growth == 10:
        bot.reply_to(message, f"🍆 УХ ТЫ! Пиписька выросла на {growth} см! Теперь она {new_size} см! 🎉")
    else:
        bot.reply_to(message, f"🍆 Пиписька выросла на {growth} см! Теперь она {new_size} см\nВведи команду ещё раз через 2 часа!")

def cmd_ukrast(message):
    user_id = message.from_user.id
    
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответьте на сообщение пользователя, у которого хотите украсть пипиську")
        return
    
    target = message.reply_to_message.from_user
    if target.id == user_id:
        bot.reply_to(message, "❌ Нельзя украсть у самого себя")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT piska_last_steal FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    last_steal = result[0] if result else None
    
    if last_steal:
        last_steal_time = datetime.strptime(last_steal, '%Y-%m-%d %H:%M:%S')
        time_diff = datetime.now() - last_steal_time
        if time_diff.total_seconds() < 14400:
            hours_left = 4 - (time_diff.total_seconds() / 3600)
            bot.reply_to(message, f"⏳ Вы уже воровали! Подождите {hours_left:.1f} часов")
            conn.close()
            return
    
    cursor.execute('SELECT piska_size FROM users WHERE user_id = ?', (target.id,))
    target_size = cursor.fetchone()
    target_size = target_size[0] if target_size else 0
    
    if target_size <= 0:
        bot.reply_to(message, "❌ У этого пользователя нечего воровать")
        conn.close()
        return
    
    if random.randint(1, 100) <= 40:
        if random.randint(1, 100) <= 10:
            steal_amount = min(10, target_size)
        else:
            steal_amount = min(random.randint(1, 9), target_size)
        
        cursor.execute('UPDATE users SET piska_size = piska_size + ? WHERE user_id = ?', (steal_amount, user_id))
        cursor.execute('UPDATE users SET piska_size = piska_size - ? WHERE user_id = ?', (steal_amount, target.id))
        cursor.execute('UPDATE users SET piska_last_steal = ? WHERE user_id = ?', 
                      (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
        conn.commit()
        
        bot.reply_to(message, f"✅ Вы успешно украли {steal_amount} см у {target.first_name}! 🏴‍☠️")
    else:
        cursor.execute('UPDATE users SET piska_last_steal = ? WHERE user_id = ?',
                      (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
        conn.commit()
        bot.reply_to(message, f"❌ Кража провалилась! {target.first_name} поймал вас! 🚔")
    
    conn.close()

def cmd_toppiska(message):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, first_name, piska_size FROM users WHERE piska_size > 0 ORDER BY piska_size DESC LIMIT 10')
    top = cursor.fetchall()
    conn.close()
    
    if not top:
        bot.reply_to(message, "📊 Топ пиписьек пуст")
        return
    
    text = "🍆 ТОП САМЫХ БОЛЬШИХ ПИПИСЕК:\n\n"
    for i, (user_id, first_name, size) in enumerate(top, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "📌"
        name = first_name or f"ID {user_id}"
        text += f"{medal} {i}. {name} — {size} см\n"
    
    bot.reply_to(message, text)

# ===== БИТКОИН КОМАНДЫ =====
def get_btc_rate():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT rate, last_change FROM btc_rate WHERE id = 1')
    result = cursor.fetchone()
    conn.close()
    return result[0], result[1]

def set_btc_rate(new_rate):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE btc_rate SET rate = ?, last_change = ? WHERE id = 1',
                  (new_rate, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def cmd_bitcoin(message):
    """Показывает баланс биткоинов"""
    user_id = message.from_user.id
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT bitcoins FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    bitcoins = result[0] if result else 0
    conn.close()
    
    bot.reply_to(message, f"₿ Ваш баланс биткоинов: {bitcoins} BTC")

def cmd_exchange(message):
    """Обмен твистов на биткоины по текущему курсу"""
    user_id = message.from_user.id
    
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Введите сумму твистов, которую хотите обменять на биткоины")
        return
    
    try:
        twists_amount = int(message.text.split()[1])
        if twists_amount <= 0:
            bot.reply_to(message, "❌ Сумма должна быть положительной")
            return
    except ValueError:
        bot.reply_to(message, "❌ Неверная сумма. Укажите число")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    # Проверяем баланс твистов
    cursor.execute('SELECT twists FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    current_twists = result[0] if result else 0
    
    if current_twists < twists_amount:
        bot.reply_to(message, f"❌ У вас недостаточно твистов. Текущий баланс: {current_twists:,}")
        conn.close()
        return
    
    # Получаем текущий курс биткоина
    btc_rate, _ = get_btc_rate()
    
    # Рассчитываем сколько биткоинов получит пользователь
    btc_amount = twists_amount / btc_rate
    btc_amount = round(btc_amount, 8)
    
    # Обновляем балансы
    cursor.execute('UPDATE users SET twists = twists - ?, bitcoins = bitcoins + ? WHERE user_id = ?',
                  (twists_amount, btc_amount, user_id))
    conn.commit()
    
    # Получаем новые балансы
    cursor.execute('SELECT twists, bitcoins FROM users WHERE user_id = ?', (user_id,))
    new_twists, new_btc = cursor.fetchone()
    conn.close()
    
    text = f"✅ ОБМЕН УСПЕШЕН!\n\n"
    text += f"💱 Отдано твистов: {twists_amount:,}\n"
    text += f"₿ Получено биткоинов: {btc_amount}\n"
    text += f"📊 Курс: 1 BTC = {btc_rate:,} твистов\n\n"
    text += f"💰 Новый баланс:\n"
    text += f"• Твистов: {new_twists:,}\n"
    text += f"• Биткоинов: {new_btc}"
    
    bot.reply_to(message, text)

def cmd_transferbtc(message):
    """Перевод биткоинов другому пользователю"""
    user_id = message.from_user.id
    
    # Проверяем, есть ли ответ на сообщение
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответьте на сообщение пользователя, которому хотите перевести биткоины")
        return
    
    target = message.reply_to_message.from_user
    
    # Проверяем, не переводит ли пользователь сам себе
    if target.id == user_id:
        bot.reply_to(message, "❌ Нельзя перевести биткоины самому себе")
        return
    
    # Проверяем, указана ли сумма
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Использование: /переводбиткоин [сумма] (ответом на сообщение)")
        return
    
    try:
        amount = float(message.text.split()[1])
        if amount <= 0:
            bot.reply_to(message, "❌ Сумма должна быть положительной")
            return
    except ValueError:
        bot.reply_to(message, "❌ Неверная сумма. Укажите число")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    # Проверяем баланс отправителя
    cursor.execute('SELECT bitcoins FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    sender_btc = result[0] if result else 0
    
    if sender_btc < amount:
        bot.reply_to(message, f"❌ У вас недостаточно биткоинов. Текущий баланс: {sender_btc} BTC")
        conn.close()
        return
    
    # Проверяем, есть ли получатель в базе
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (target.id,))
    if not cursor.fetchone():
        # Создаем запись для получателя, если его нет
        create_user_if_not_exists(target.id, target.username, target.first_name, target.last_name)
    
    # Выполняем перевод
    cursor.execute('UPDATE users SET bitcoins = bitcoins - ? WHERE user_id = ?', (amount, user_id))
    cursor.execute('UPDATE users SET bitcoins = bitcoins + ? WHERE user_id = ?', (amount, target.id))
    conn.commit()
    
    # Получаем новые балансы
    cursor.execute('SELECT bitcoins FROM users WHERE user_id = ?', (user_id,))
    new_sender_btc = cursor.fetchone()[0]
    cursor.execute('SELECT bitcoins FROM users WHERE user_id = ?', (target.id,))
    new_receiver_btc = cursor.fetchone()[0]
    conn.close()
    
    text = f"✅ ПЕРЕВОД УСПЕШЕН!\n\n"
    text += f"💸 Отправлено: {amount} BTC\n"
    text += f"👤 Получатель: {target.first_name}\n\n"
    text += f"💰 Ваш новый баланс: {new_sender_btc} BTC"
    
    bot.reply_to(message, text)

def cmd_rate(message):
    """Показывает текущий курс биткоина"""
    
    # Получаем текущий курс
    current_rate, last_change_str = get_btc_rate()
    
    # Формируем текст
    text = f"📊 КУРС БИТКОИНА\n\n"
    text += f"💰 Цена за 1 BTC: {current_rate:,.0f} твистов\n\n"
    text += f"📈 Возможен рост до: {int(current_rate * 1.1):,.0f} твистов\n"
    text += f"📉 Возможно падение до: {int(current_rate * 0.9):,.0f} твистов"
    
    bot.reply_to(message, text)

def cmd_changerate(message):
    """Изменяет курс биткоина (только для владельца)"""
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Только для владельца бота")
        return
    
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Использование: /изменитькурс [новая цена]")
        return
    
    try:
        new_rate = float(message.text.split()[1])
        if new_rate <= 0:
            bot.reply_to(message, "❌ Цена должна быть положительной")
            return
    except ValueError:
        bot.reply_to(message, "❌ Неверная цена. Укажите число")
        return
    
    set_btc_rate(new_rate)
    bot.reply_to(message, f"✅ Курс биткоина изменен на {new_rate:,.0f} твистов за 1 BTC")

def cmd_sellbtc(message):
    """Продажа биткоинов по текущему курсу"""
    user_id = message.from_user.id
    
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Использование: /продать [количество BTC]")
        return
    
    try:
        btc_amount = float(message.text.split()[1])
        if btc_amount <= 0:
            bot.reply_to(message, "❌ Количество должно быть положительным")
            return
    except ValueError:
        bot.reply_to(message, "❌ Неверное количество. Укажите число")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT bitcoins FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    current_btc = result[0] if result else 0
    
    if current_btc < btc_amount:
        bot.reply_to(message, f"❌ У вас недостаточно биткоинов. Текущий баланс: {current_btc} BTC")
        conn.close()
        return
    
    # Получаем актуальный курс
    rate, _ = get_btc_rate()
    twists_earned = int(btc_amount * rate)
    
    cursor.execute('UPDATE users SET bitcoins = bitcoins - ?, twists = twists + ? WHERE user_id = ?',
                  (btc_amount, twists_earned, user_id))
    conn.commit()
    
    cursor.execute('SELECT bitcoins, twists FROM users WHERE user_id = ?', (user_id,))
    new_btc, new_twists = cursor.fetchone()
    conn.close()
    
    text = f"✅ ПРОДАЖА УСПЕШНА!\n\n"
    text += f"💸 Продано: {btc_amount} BTC\n"
    text += f"💰 Получено: {twists_earned:,} твистов\n"
    text += f"📊 Курс: {rate:,.0f} твистов за 1 BTC\n\n"
    text += f"💰 Новый баланс:\n"
    text += f"• Твистов: {new_twists:,}\n"
    text += f"• Биткоинов: {new_btc} BTC"
    
    bot.reply_to(message, text)

def cmd_obnulbitoc(message):
    """Обнуляет биткоины у всех пользователей (только для владельца)"""
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Только для владельца бота")
        return
    
    # Создаем клавиатуру для подтверждения
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Да, обнулить", callback_data="obnulbitoc_confirm"),
        types.InlineKeyboardButton("❌ Отмена", callback_data="obnulbitoc_cancel")
    )
    
    bot.reply_to(message, "⚠️ ВНИМАНИЕ! Вы уверены, что хотите ОБНУЛИТЬ биткоины у ВСЕХ пользователей?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('obnulbitoc_'))
def obnulbitoc_callback(call):
    if call.from_user.id != OWNER_ID:
        bot.answer_callback_query(call.id, "Это не для вас")
        return
    
    if call.data == "obnulbitoc_confirm":
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET bitcoins = 0')
        conn.commit()
        conn.close()
        
        bot.edit_message_text("✅ Все биткоины успешно обнулены!", call.message.chat.id, call.message.message_id)
    else:
        bot.edit_message_text("❌ Операция отменена", call.message.chat.id, call.message.message_id)
                         # ===== ЗАМЕС КОМАНДА =====
def cmd_zames(message):
    user_id = message.from_user.id
    
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответьте на сообщение пользователя, с которым хотите сделать замес")
        return
    
    target = message.reply_to_message.from_user
    if target.id == user_id:
        bot.reply_to(message, "❌ Нельзя сделать замес с самим собой")
        return
    
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Укажите размер ставки в см")
        return
    
    try:
        bet_size = int(message.text.split()[1])
        if bet_size <= 0:
            bot.reply_to(message, "❌ Размер ставки должен быть положительным")
            return
    except ValueError:
        bot.reply_to(message, "❌ Неверный размер. Укажите число")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT piska_size FROM users WHERE user_id = ?', (user_id,))
    challenger_size = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT piska_size FROM users WHERE user_id = ?', (target.id,))
    opponent_size = cursor.fetchone()[0] or 0
    
    if challenger_size < bet_size:
        bot.reply_to(message, f"❌ У вас недостаточно см для ставки. Ваш размер: {challenger_size} см")
        conn.close()
        return
    
    if opponent_size < bet_size:
        bot.reply_to(message, f"❌ У соперника недостаточно см для ставки. Его размер: {opponent_size} см")
        conn.close()
        return
    
    created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO zames_battles (challenger_id, opponent_id, bet_size, status, created_date, chat_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, target.id, bet_size, 'pending', created_date, message.chat.id))
    
    battle_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("✅ Принять", callback_data=f'zames_accept_{battle_id}'),
        types.InlineKeyboardButton("❌ Отказаться", callback_data=f'zames_decline_{battle_id}')
    )
    
    bot.send_message(
        message.chat.id,
        f"⚔️ {message.from_user.first_name} кинул замес на пипиську {target.first_name}!\n"
        f"💰 Ставка: {bet_size} см\n"
        f"Шанс на победу: 50/50",
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('zames_'))
def zames_callback(call):
    data = call.data.split('_')
    action = data[1]
    battle_id = int(data[2])
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT challenger_id, opponent_id, bet_size, status FROM zames_battles WHERE id = ?', (battle_id,))
    battle = cursor.fetchone()
    
    if not battle:
        bot.answer_callback_query(call.id, "❌ Замес не найден")
        conn.close()
        return
    
    challenger_id, opponent_id, bet_size, status = battle
    
    if status != 'pending':
        bot.answer_callback_query(call.id, "❌ Этот замес уже обработан")
        conn.close()
        bot.edit_message_text("❌ Замес уже завершен", call.message.chat.id, call.message.message_id)
        return
    
    if action == 'accept':
        if call.from_user.id != opponent_id:
            bot.answer_callback_query(call.id, "Это не ваш замес")
            conn.close()
            return
        
        winner_id = challenger_id if random.randint(0, 1) == 0 else opponent_id
        loser_id = opponent_id if winner_id == challenger_id else challenger_id
        
        cursor.execute('UPDATE users SET piska_size = piska_size + ? WHERE user_id = ?', (bet_size, winner_id))
        cursor.execute('UPDATE users SET piska_size = piska_size - ? WHERE user_id = ?', (bet_size, loser_id))
        
        cursor.execute('UPDATE zames_battles SET status = ? WHERE id = ?', ('completed', battle_id))
        conn.commit()
        
        winner = bot.get_chat(winner_id)
        loser = bot.get_chat(loser_id)
        
        bot.edit_message_text(
            f"✅ Замес состоялся!\n\n"
            f"🏆 Победитель: {winner.first_name}\n"
            f"📈 Выиграл {bet_size} см\n\n"
            f"😢 Проигравший: {loser.first_name}\n"
            f"📉 Потерял {bet_size} см",
            call.message.chat.id,
            call.message.message_id
        )
        
    elif action == 'decline':
        if call.from_user.id != opponent_id:
            bot.answer_callback_query(call.id, "Это не ваш замес")
            conn.close()
            return
        
        cursor.execute('UPDATE zames_battles SET status = ? WHERE id = ?', ('declined', battle_id))
        conn.commit()
        
        challenger = bot.get_chat(challenger_id)
        
        bot.edit_message_text(
            f"❌ {challenger.first_name}, ваш замес отклонен",
            call.message.chat.id,
            call.message.message_id
        )
    
    conn.close()
    
# ===== МАЙНИНГ КОМАНДЫ =====
def cmd_mainingshop(message):
    user_id = message.from_user.id
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT has_card1, has_card2, has_card3, has_card4, has_card5 FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    has_card1 = result[0] if result else 0
    has_card2 = result[1] if result else 0
    has_card3 = result[2] if result else 0
    has_card4 = result[3] if result else 0
    has_card5 = result[4] if result else 0
    conn.close()
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    if not has_card1:
        buy_button1 = types.InlineKeyboardButton("💳 Купить RTX 4090 (10,000 твистов)", callback_data=f"mining_buy1_{user_id}")
        markup.add(buy_button1)
    
    if not has_card2:
        buy_button2 = types.InlineKeyboardButton("💳 Купить MSI RTX 4090 SUPRIM X (500,000 твистов)", callback_data=f"mining_buy2_{user_id}")
        markup.add(buy_button2)
    
    if not has_card3:
        buy_button3 = types.InlineKeyboardButton("💳 Купить ASUS RTX 4090 ROG STRIX (8,500,000 твистов)", callback_data=f"mining_buy3_{user_id}")
        markup.add(buy_button3)
    
    if not has_card4:
        buy_button4 = types.InlineKeyboardButton("💳 Купить Gigabyte RTX 4090 AORUS XTREME (300,000,000 твистов)", callback_data=f"mining_buy4_{user_id}")
        markup.add(buy_button4)
    
    if not has_card5:
        buy_button5 = types.InlineKeyboardButton("💳 Купить ZOTAC RTX 4090 AMP EXTREME (1,500,000,000 твистов)", callback_data=f"mining_buy5_{user_id}")
        markup.add(buy_button5)
    
    exit_button = types.InlineKeyboardButton("🚪 Выйти из магазина", callback_data=f"mining_exit_{user_id}")
    markup.add(exit_button)
    
    shop_text = "🏪 МАГАЗИН МАЙНИНГА\n\n"
    shop_text += "📦 Доступные видеокарты:\n\n"
    
    shop_text += "1️⃣ RTX 4090\n"
    shop_text += "💰 Цена: 10,000 твистов\n"
    shop_text += "💎 Макс. прибыль: 25,000/час\n"
    shop_text += f"{'✅ КУПЛЕНО' if has_card1 else '❌ НЕ КУПЛЕНО'}\n\n"
    
    shop_text += "2️⃣ MSI GeForce RTX 4090 SUPRIM X\n"
    shop_text += "💰 Цена: 500,000 твистов\n"
    shop_text += "💎 Макс. прибыль: 125,000/час\n"
    shop_text += f"{'✅ КУПЛЕНО' if has_card2 else '❌ НЕ КУПЛЕНО'}\n\n"
    
    shop_text += "3️⃣ ASUS RTX 4090 ROG STRIX\n"
    shop_text += "💰 Цена: 8,500,000 твистов\n"
    shop_text += "💎 Макс. прибыль: 1,200,000/час\n"
    shop_text += f"{'✅ КУПЛЕНО' if has_card3 else '❌ НЕ КУПЛЕНО'}\n\n"
    
    shop_text += "4️⃣ Gigabyte RTX 4090 AORUS XTREME\n"
    shop_text += "💰 Цена: 300,000,000 твистов\n"
    shop_text += "💎 Макс. прибыль: 20,000,000/час\n"
    shop_text += f"{'✅ КУПЛЕНО' if has_card4 else '❌ НЕ КУПЛЕНО'}\n\n"
    
    shop_text += "5️⃣ ZOTAC RTX 4090 AMP EXTREME\n"
    shop_text += "💰 Цена: 1,500,000,000 твистов\n"
    shop_text += "💎 Макс. прибыль: 150,000,000/час\n"
    shop_text += f"{'✅ КУПЛЕНО' if has_card5 else '❌ НЕ КУПЛЕНО'}\n"
    
    bot.send_message(message.chat.id, shop_text, reply_markup=markup)

def cmd_mainingferma(message):
    user_id = message.from_user.id
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    # Получаем данные пользователя
    cursor.execute('''
        SELECT 
            has_card1, card1_level, card1_balance, card1_last_collect,
            has_card2, card2_level, card2_balance, card2_last_collect,
            has_card3, card3_level, card3_balance, card3_last_collect,
            has_card4, card4_level, card4_balance, card4_last_collect,
            has_card5, card5_level, card5_balance, card5_last_collect
        FROM users WHERE user_id = ?
    ''', (user_id,))
    result = cursor.fetchone()
    
    if not result:
        conn.close()
        markup = types.InlineKeyboardMarkup()
        shop_button = types.InlineKeyboardButton("🏪 Перейти в магазин", callback_data=f"mining_go_shop_{user_id}")
        markup.add(shop_button)
        bot.send_message(message.chat.id, "❌ У вас нет майнинг фермы!\n\nКупите видеокарту в магазине /mainingshop", reply_markup=markup)
        return
    
    (has_card1, card1_level, card1_balance, card1_last_collect,
     has_card2, card2_level, card2_balance, card2_last_collect,
     has_card3, card3_level, card3_balance, card3_last_collect,
     has_card4, card4_level, card4_balance, card4_last_collect,
     has_card5, card5_level, card5_balance, card5_last_collect) = result
    
    # Проверяем есть ли хоть одна видеокарта
    if not (has_card1 or has_card2 or has_card3 or has_card4 or has_card5):
        conn.close()
        markup = types.InlineKeyboardMarkup()
        shop_button = types.InlineKeyboardButton("🏪 Перейти в магазин", callback_data=f"mining_go_shop_{user_id}")
        markup.add(shop_button)
        bot.send_message(message.chat.id, "❌ У вас нет майнинг фермы!\n\nКупите видеокарту в магазине /mainingshop", reply_markup=markup)
        return
    
    # Обновляем балансы если прошло время
    current_time = datetime.now()
    
    # Карта 1
    if has_card1 and card1_last_collect:
        try:
            last_time = datetime.strptime(card1_last_collect, '%Y-%m-%d %H:%M:%S')
            hours_passed = (current_time - last_time).total_seconds() / 3600
            if hours_passed > 0:
                profit_per_hour1 = 5000 + (card1_level * 5000)
                new_balance = card1_balance + int(profit_per_hour1 * hours_passed)
                cursor.execute('UPDATE users SET card1_balance = ? WHERE user_id = ?', (new_balance, user_id))
                card1_balance = new_balance
                conn.commit()
        except:
            pass
    
    # Карта 2
    if has_card2 and card2_last_collect:
        try:
            last_time = datetime.strptime(card2_last_collect, '%Y-%m-%d %H:%M:%S')
            hours_passed = (current_time - last_time).total_seconds() / 3600
            if hours_passed > 0:
                profit_per_hour2 = 25000 + (card2_level * 25000)
                new_balance = card2_balance + int(profit_per_hour2 * hours_passed)
                cursor.execute('UPDATE users SET card2_balance = ? WHERE user_id = ?', (new_balance, user_id))
                card2_balance = new_balance
                conn.commit()
        except:
            pass
    
    # Карта 3
    if has_card3 and card3_last_collect:
        try:
            last_time = datetime.strptime(card3_last_collect, '%Y-%m-%d %H:%M:%S')
            hours_passed = (current_time - last_time).total_seconds() / 3600
            if hours_passed > 0:
                profit_per_hour3 = 240000 + (card3_level * 240000)  # Базовая 240к, макс 1.2м на 5 уровне
                new_balance = card3_balance + int(profit_per_hour3 * hours_passed)
                cursor.execute('UPDATE users SET card3_balance = ? WHERE user_id = ?', (new_balance, user_id))
                card3_balance = new_balance
                conn.commit()
        except:
            pass
    
    # Карта 4
    if has_card4 and card4_last_collect:
        try:
            last_time = datetime.strptime(card4_last_collect, '%Y-%m-%d %H:%M:%S')
            hours_passed = (current_time - last_time).total_seconds() / 3600
            if hours_passed > 0:
                profit_per_hour4 = 4000000 + (card4_level * 4000000)  # Базовая 4м, макс 20м на 5 уровне
                new_balance = card4_balance + int(profit_per_hour4 * hours_passed)
                cursor.execute('UPDATE users SET card4_balance = ? WHERE user_id = ?', (new_balance, user_id))
                card4_balance = new_balance
                conn.commit()
        except:
            pass
    
    # Карта 5
    if has_card5 and card5_last_collect:
        try:
            last_time = datetime.strptime(card5_last_collect, '%Y-%m-%d %H:%M:%S')
            hours_passed = (current_time - last_time).total_seconds() / 3600
            if hours_passed > 0:
                profit_per_hour5 = 30000000 + (card5_level * 30000000)  # Базовая 30м, макс 150м на 5 уровне
                new_balance = card5_balance + int(profit_per_hour5 * hours_passed)
                cursor.execute('UPDATE users SET card5_balance = ? WHERE user_id = ?', (new_balance, user_id))
                card5_balance = new_balance
                conn.commit()
        except:
            pass
    
    # Создаем клавиатуру
    markup = types.InlineKeyboardMarkup(row_width=1)
    max_level = 5
    
    farm_text = "⛏️ ТВОЯ МАЙНИНГ ФЕРМА\n\n"
    
    # Карта 1
    if has_card1:
        profit_per_hour1 = 5000 + (card1_level * 5000)
        upgrade_cost1 = 10000 if card1_level == 0 else 5000 * (card1_level + 1)
        
        farm_text += "1️⃣ RTX 4090\n"
        farm_text += f"📊 Уровень: {card1_level}/{max_level}\n"
        farm_text += f"💰 Прибыль в час: {profit_per_hour1:,} твистов\n"
        farm_text += f"💳 Баланс: {card1_balance:,} твистов\n"
        
        if card1_balance > 0:
            collect_button = types.InlineKeyboardButton(f"💰 Снять {card1_balance:,} твистов с RTX 4090", callback_data=f"mining_collect1_{user_id}")
            markup.add(collect_button)
        
        if card1_level < max_level:
            upgrade_button = types.InlineKeyboardButton(f"⬆️ Улучшить RTX 4090 до {card1_level + 1} уровня ({upgrade_cost1:,} тв)", callback_data=f"mining_upgrade1_{user_id}")
            markup.add(upgrade_button)
        
        farm_text += "\n"
    
    # Карта 2
    if has_card2:
        profit_per_hour2 = 25000 + (card2_level * 25000)
        upgrade_cost2 = 50000 if card2_level == 0 else 25000 * (card2_level + 1)
        
        farm_text += "2️⃣ MSI GeForce RTX 4090 SUPRIM X\n"
        farm_text += f"📊 Уровень: {card2_level}/{max_level}\n"
        farm_text += f"💰 Прибыль в час: {profit_per_hour2:,} твистов\n"
        farm_text += f"💳 Баланс: {card2_balance:,} твистов\n"
        
        if card2_balance > 0:
            collect_button = types.InlineKeyboardButton(f"💰 Снять {card2_balance:,} твистов с MSI SUPRIM X", callback_data=f"mining_collect2_{user_id}")
            markup.add(collect_button)
        
        if card2_level < max_level:
            upgrade_button = types.InlineKeyboardButton(f"⬆️ Улучшить MSI SUPRIM X до {card2_level + 1} уровня ({upgrade_cost2:,} тв)", callback_data=f"mining_upgrade2_{user_id}")
            markup.add(upgrade_button)
        
        farm_text += "\n"
    
    # Карта 3
    if has_card3:
        profit_per_hour3 = 240000 + (card3_level * 240000)
        upgrade_cost3 = 350000  # Фиксированная цена улучшения
        
        farm_text += "3️⃣ ASUS RTX 4090 ROG STRIX\n"
        farm_text += f"📊 Уровень: {card3_level}/{max_level}\n"
        farm_text += f"💰 Прибыль в час: {profit_per_hour3:,} твистов\n"
        farm_text += f"💳 Баланс: {card3_balance:,} твистов\n"
        
        if card3_balance > 0:
            collect_button = types.InlineKeyboardButton(f"💰 Снять {card3_balance:,} твистов с ASUS ROG STRIX", callback_data=f"mining_collect3_{user_id}")
            markup.add(collect_button)
        
        if card3_level < max_level:
            upgrade_button = types.InlineKeyboardButton(f"⬆️ Улучшить ASUS ROG STRIX до {card3_level + 1} уровня ({upgrade_cost3:,} тв)", callback_data=f"mining_upgrade3_{user_id}")
            markup.add(upgrade_button)
        
        farm_text += "\n"
    
    # Карта 4
    if has_card4:
        profit_per_hour4 = 4000000 + (card4_level * 4000000)
        upgrade_cost4 = 15000000  # Фиксированная цена улучшения
        
        farm_text += "4️⃣ Gigabyte RTX 4090 AORUS XTREME\n"
        farm_text += f"📊 Уровень: {card4_level}/{max_level}\n"
        farm_text += f"💰 Прибыль в час: {profit_per_hour4:,} твистов\n"
        farm_text += f"💳 Баланс: {card4_balance:,} твистов\n"
        
        if card4_balance > 0:
            collect_button = types.InlineKeyboardButton(f"💰 Снять {card4_balance:,} твистов с Gigabyte AORUS", callback_data=f"mining_collect4_{user_id}")
            markup.add(collect_button)
        
        if card4_level < max_level:
            upgrade_button = types.InlineKeyboardButton(f"⬆️ Улучшить Gigabyte AORUS до {card4_level + 1} уровня ({upgrade_cost4:,} тв)", callback_data=f"mining_upgrade4_{user_id}")
            markup.add(upgrade_button)
        
        farm_text += "\n"
    
    # Карта 5
    if has_card5:
        profit_per_hour5 = 30000000 + (card5_level * 30000000)
        upgrade_cost5 = 85000000  # Фиксированная цена улучшения
        
        farm_text += "5️⃣ ZOTAC RTX 4090 AMP EXTREME\n"
        farm_text += f"📊 Уровень: {card5_level}/{max_level}\n"
        farm_text += f"💰 Прибыль в час: {profit_per_hour5:,} твистов\n"
        farm_text += f"💳 Баланс: {card5_balance:,} твистов\n"
        
        if card5_balance > 0:
            collect_button = types.InlineKeyboardButton(f"💰 Снять {card5_balance:,} твистов с ZOTAC AMP EXTREME", callback_data=f"mining_collect5_{user_id}")
            markup.add(collect_button)
        
        if card5_level < max_level:
            upgrade_button = types.InlineKeyboardButton(f"⬆️ Улучшить ZOTAC AMP EXTREME до {card5_level + 1} уровня ({upgrade_cost5:,} тв)", callback_data=f"mining_upgrade5_{user_id}")
            markup.add(upgrade_button)
        
        farm_text += "\n"
    
    # Добавляем кнопки обновления и выхода
    if has_card1 or has_card2 or has_card3 or has_card4 or has_card5:
        refresh_button = types.InlineKeyboardButton("🔄 Обновить", callback_data=f"mining_refresh_{user_id}")
        markup.add(refresh_button)
    
    exit_button = types.InlineKeyboardButton("🚪 Выйти", callback_data=f"mining_exit_{user_id}")
    markup.add(exit_button)
    
    conn.close()
    
    bot.send_message(message.chat.id, farm_text, reply_markup=markup)
    
# ===== КОМАНДЫ ДЛЯ ОБНОВЛЕНИЙ =====
def cmd_upd(message):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT update_text, created_date FROM updates ORDER BY id DESC LIMIT 10')
    updates = cursor.fetchall()
    conn.close()
    
    if not updates:
        bot.reply_to(message, "📋 Список обновлений пуст")
        return
    
    text = "📋 ПОСЛЕДНИЕ ОБНОВЛЕНИЯ БОТА:\n\n"
    for i, (update_text, created_date) in enumerate(updates, 1):
        date_obj = datetime.strptime(created_date, '%Y-%m-%d %H:%M:%S')
        formatted_date = date_obj.strftime('%d.%m.%Y %H:%M')
        text += f"{i}. {update_text}\n   📅 {formatted_date}\n\n"
    
    bot.reply_to(message, text)

def cmd_setupd(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Только для владельца бота")
        return
    
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Использование: /setupd [текст обновления]")
        return
    
    update_text = ' '.join(message.text.split()[1:])
    created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO updates (update_text, created_date, created_by) VALUES (?, ?, ?)',
                  (update_text, created_date, OWNER_ID))
    conn.commit()
    conn.close()
    
    bot.reply_to(message, f"✅ Запись об обновлении добавлена:\n\n{update_text}")
    # ===== НОВЫЕ КОМАНДЫ =====
    
def cmd_spisok(message):
    """Показывает список активных промокодов"""
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM promocodes WHERE current_activations < max_activations')
    promos = cursor.fetchall()
    
    if not promos:
        bot.reply_to(message, "📋 Активных промокодов нет")
        conn.close()
        return
    
    text = "📋 АКТИВНЫЕ ПРОМОКОДЫ:\n\n"
    for promo in promos:
        code = promo[0]
        twists = promo[1]
        max_acts = promo[2]
        current = promo[3]
        left = max_acts - current
        text += f"🎫 {code}: {twists} твистов (осталось {left} активаций)\n"
    
    conn.close()
    bot.reply_to(message, text)

def cmd_donat(message):
    """Команда доната с кнопками"""
    user_id = message.from_user.id
    
    # Получаем рублевый баланс пользователя
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT rub_balance FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    rub_balance = result[0] if result else 0
    conn.close()
    
    # Создаем клавиатуру с кнопками
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("💎 Админ права (333₽)", callback_data=f"donat_admin_{user_id}")
    btn2 = types.InlineKeyboardButton("💰 Деньги 30.000.000 (35₽)", callback_data=f"donat_money_{user_id}")
    btn3 = types.InlineKeyboardButton("✅ Верификация (79₽)", callback_data=f"donat_verify_{user_id}")
    btn4 = types.InlineKeyboardButton("👑 ВЛАДЕЛЕЦ БОТА (999₽)", callback_data=f"donat_owner_{user_id}")
    
    markup.add(btn1, btn2, btn3, btn4)
    
    donat_text = f"💎 Админ права - [ 333₽ ]\n"
    donat_text += f"💰 Деньги ( 30.000.000 ) - [ 35₽ ]\n"
    donat_text += f"✅ Верификация в профиль - [ 79₽ ]\n"
    donat_text += f"👑 Должность ВЛАДЕЛЕЦ БОТА - [ 999₽ ]\n\n"
    donat_text += f"💵 Ваш рублевый баланс: {rub_balance}₽\n\n"
    donat_text += f"Чтобы задонатить обратись к владельцу бота - @usehyro"
    
    bot.send_message(message.chat.id, donat_text, reply_markup=markup)

def cmd_giverub(message):
    """Выдать рубли пользователю (только для владельца)"""
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Только для владельца бота")
        return
    
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответьте на сообщение пользователя")
        return
    
    target = message.reply_to_message.from_user
    
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Использование: /giverub [количество]")
        return
    
    try:
        amount = int(message.text.split()[1])
        if amount <= 0:
            bot.reply_to(message, "❌ Сумма должна быть положительной")
            return
    except ValueError:
        bot.reply_to(message, "❌ Неверная сумма")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    cursor.execute('UPDATE users SET rub_balance = rub_balance + ? WHERE user_id = ?', (amount, target.id))
    conn.commit()
    
    cursor.execute('SELECT rub_balance FROM users WHERE user_id = ?', (target.id,))
    new_balance = cursor.fetchone()[0]
    conn.close()
    
    bot.reply_to(message, f"✅ Пользователю {target.first_name} выдано {amount}₽\n💵 Новый баланс: {new_balance}₽")

@bot.callback_query_handler(func=lambda call: call.data.startswith('donat_'))
def donat_callback(call):
    data = call.data.split('_')
    action = data[1]
    target_user_id = int(data[2])
    
    if call.from_user.id != target_user_id:
        bot.answer_callback_query(call.id, "❌ Это не ваша кнопка")
        return
    
    if action == "admin":
        bot.answer_callback_query(call.id, "✅ Для покупки админ прав обратитесь к @usehyro")
    elif action == "money":
        bot.answer_callback_query(call.id, "✅ Для покупки денег обратитесь к @usehyro")
    elif action == "verify":
        bot.answer_callback_query(call.id, "✅ Для покупки верификации обратитесь к @usehyro")
    elif action == "owner":
        bot.answer_callback_query(call.id, "✅ Для покупки должности владельца обратитесь к @usehyro")

# ---------- ОБРАБОТЧИК НОВЫХ УЧАСТНИКОВ ----------
@bot.message_handler(content_types=['new_chat_members'])
def handle_new_members(message):
    for member in message.new_chat_members:
        if member.id == bot.get_me().id:
            bot.send_message(message.chat.id, "👋 Спасибо что добавили! Выдайте мне права администратора.")
            continue
        
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT greeting_text FROM greetings WHERE chat_id = ?', (message.chat.id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            bot.send_message(message.chat.id, f"👋 Добро пожаловать, {member.first_name}!\n{result[0]}")
            
@bot.callback_query_handler(func=lambda call: call.data.startswith('mining_'))
def mining_callback(call):
    data = call.data.split('_')
    action = data[1]
    target_user_id = int(data[2])

    if call.from_user.id != target_user_id:
        bot.answer_callback_query(call.id, "❌ Это не ваша кнопка")
        return

    user_id = call.from_user.id

    # Кнопки магазина
    if action == "buy1":
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT twists, has_card1 FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        twists = result[0]
        has_card = result[1]
        
        if has_card:
            bot.answer_callback_query(call.id, "У вас уже есть эта видеокарта!")
            conn.close()
            return
        
        if twists < 10000:
            bot.answer_callback_query(call.id, "Недостаточно твистов! Нужно 10,000")
            conn.close()
            return
        
        cursor.execute('UPDATE users SET twists = twists - 10000, has_card1 = 1, card1_level = 0, card1_balance = 0, card1_last_collect = ? WHERE user_id = ?',
                      (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
        conn.commit()
        conn.close()
        
        bot.answer_callback_query(call.id, "✅ Видеокарта RTX 4090 куплена!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        class FakeMessage:
            def __init__(self, chat_id, from_user_id):
                self.chat = type('obj', (object,), {'id': chat_id})
                self.from_user = type('obj', (object,), {'id': from_user_id})
                self.text = "/mainingshop"
        
        fake_msg = FakeMessage(call.message.chat.id, user_id)
        cmd_mainingshop(fake_msg)
        
    elif action == "buy2":
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT twists, has_card2 FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        twists = result[0]
        has_card = result[1]
        
        if has_card:
            bot.answer_callback_query(call.id, "У вас уже есть эта видеокарта!")
            conn.close()
            return
        
        if twists < 500000:
            bot.answer_callback_query(call.id, "Недостаточно твистов! Нужно 500,000")
            conn.close()
            return
        
        cursor.execute('UPDATE users SET twists = twists - 500000, has_card2 = 1, card2_level = 0, card2_balance = 0, card2_last_collect = ? WHERE user_id = ?',
                      (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
        conn.commit()
        conn.close()
        
        bot.answer_callback_query(call.id, "✅ Видеокарта MSI RTX 4090 SUPRIM X куплена!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        class FakeMessage:
            def __init__(self, chat_id, from_user_id):
                self.chat = type('obj', (object,), {'id': chat_id})
                self.from_user = type('obj', (object,), {'id': from_user_id})
                self.text = "/mainingshop"
        
        fake_msg = FakeMessage(call.message.chat.id, user_id)
        cmd_mainingshop(fake_msg)
        
    elif action == "buy3":
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT twists, has_card3 FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        twists = result[0]
        has_card = result[1]
        
        if has_card:
            bot.answer_callback_query(call.id, "У вас уже есть эта видеокарта!")
            conn.close()
            return
        
        if twists < 8500000:
            bot.answer_callback_query(call.id, "Недостаточно твистов! Нужно 8,500,000")
            conn.close()
            return
        
        cursor.execute('UPDATE users SET twists = twists - 8500000, has_card3 = 1, card3_level = 0, card3_balance = 0, card3_last_collect = ? WHERE user_id = ?',
                      (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
        conn.commit()
        conn.close()
        
        bot.answer_callback_query(call.id, "✅ Видеокарта ASUS RTX 4090 ROG STRIX куплена!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        class FakeMessage:
            def __init__(self, chat_id, from_user_id):
                self.chat = type('obj', (object,), {'id': chat_id})
                self.from_user = type('obj', (object,), {'id': from_user_id})
                self.text = "/mainingshop"
        
        fake_msg = FakeMessage(call.message.chat.id, user_id)
        cmd_mainingshop(fake_msg)
        
    elif action == "buy4":
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT twists, has_card4 FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        twists = result[0]
        has_card = result[1]
        
        if has_card:
            bot.answer_callback_query(call.id, "У вас уже есть эта видеокарта!")
            conn.close()
            return
        
        if twists < 300000000:
            bot.answer_callback_query(call.id, "Недостаточно твистов! Нужно 300,000,000")
            conn.close()
            return
        
        cursor.execute('UPDATE users SET twists = twists - 300000000, has_card4 = 1, card4_level = 0, card4_balance = 0, card4_last_collect = ? WHERE user_id = ?',
                      (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
        conn.commit()
        conn.close()
        
        bot.answer_callback_query(call.id, "✅ Видеокарта Gigabyte RTX 4090 AORUS XTREME куплена!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        class FakeMessage:
            def __init__(self, chat_id, from_user_id):
                self.chat = type('obj', (object,), {'id': chat_id})
                self.from_user = type('obj', (object,), {'id': from_user_id})
                self.text = "/mainingshop"
        
        fake_msg = FakeMessage(call.message.chat.id, user_id)
        cmd_mainingshop(fake_msg)
        
    elif action == "buy5":
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT twists, has_card5 FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        twists = result[0]
        has_card = result[1]
        
        if has_card:
            bot.answer_callback_query(call.id, "У вас уже есть эта видеокарта!")
            conn.close()
            return
        
        if twists < 1500000000:
            bot.answer_callback_query(call.id, "Недостаточно твистов! Нужно 1,500,000,000")
            conn.close()
            return
        
        cursor.execute('UPDATE users SET twists = twists - 1500000000, has_card5 = 1, card5_level = 0, card5_balance = 0, card5_last_collect = ? WHERE user_id = ?',
                      (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
        conn.commit()
        conn.close()
        
        bot.answer_callback_query(call.id, "✅ Видеокарта ZOTAC RTX 4090 AMP EXTREME куплена!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        class FakeMessage:
            def __init__(self, chat_id, from_user_id):
                self.chat = type('obj', (object,), {'id': chat_id})
                self.from_user = type('obj', (object,), {'id': from_user_id})
                self.text = "/mainingshop"
        
        fake_msg = FakeMessage(call.message.chat.id, user_id)
        cmd_mainingshop(fake_msg)
        
    elif action == "go":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        class FakeMessage:
            def __init__(self, chat_id, from_user_id):
                self.chat = type('obj', (object,), {'id': chat_id})
                self.from_user = type('obj', (object,), {'id': from_user_id})
                self.text = "/mainingshop"
        
        fake_msg = FakeMessage(call.message.chat.id, user_id)
        cmd_mainingshop(fake_msg)
        
    elif action == "exit":
        bot.delete_message(call.message.chat.id, call.message.message_id)

    # Кнопки фермы
    elif action == "collect1":
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT card1_balance FROM users WHERE user_id = ?', (user_id,))
        balance = cursor.fetchone()[0]
        
        if balance <= 0:
            bot.answer_callback_query(call.id, "Нет средств для снятия")
            conn.close()
            return
        
        cursor.execute('UPDATE users SET twists = twists + ?, card1_balance = 0, card1_last_collect = ? WHERE user_id = ?',
                      (balance, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
        conn.commit()
        conn.close()
        
        bot.answer_callback_query(call.id, f"✅ Снято {balance:,} твистов")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        class FakeMessage:
            def __init__(self, chat_id, from_user_id):
                self.chat = type('obj', (object,), {'id': chat_id})
                self.from_user = type('obj', (object,), {'id': from_user_id})
                self.text = "/ферма"
        
        fake_msg = FakeMessage(call.message.chat.id, user_id)
        cmd_mainingferma(fake_msg)
        
    elif action == "collect2":
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT card2_balance FROM users WHERE user_id = ?', (user_id,))
        balance = cursor.fetchone()[0]
        
        if balance <= 0:
            bot.answer_callback_query(call.id, "Нет средств для снятия")
            conn.close()
            return
        
        cursor.execute('UPDATE users SET twists = twists + ?, card2_balance = 0, card2_last_collect = ? WHERE user_id = ?',
                      (balance, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
        conn.commit()
        conn.close()
        
        bot.answer_callback_query(call.id, f"✅ Снято {balance:,} твистов")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        class FakeMessage:
            def __init__(self, chat_id, from_user_id):
                self.chat = type('obj', (object,), {'id': chat_id})
                self.from_user = type('obj', (object,), {'id': from_user_id})
                self.text = "/ферма"
        
        fake_msg = FakeMessage(call.message.chat.id, user_id)
        cmd_mainingferma(fake_msg)
        
    elif action == "collect3":
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT card3_balance FROM users WHERE user_id = ?', (user_id,))
        balance = cursor.fetchone()[0]
        
        if balance <= 0:
            bot.answer_callback_query(call.id, "Нет средств для снятия")
            conn.close()
            return
        
        cursor.execute('UPDATE users SET twists = twists + ?, card3_balance = 0, card3_last_collect = ? WHERE user_id = ?',
                      (balance, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
        conn.commit()
        conn.close()
        
        bot.answer_callback_query(call.id, f"✅ Снято {balance:,} твистов")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        class FakeMessage:
            def __init__(self, chat_id, from_user_id):
                self.chat = type('obj', (object,), {'id': chat_id})
                self.from_user = type('obj', (object,), {'id': from_user_id})
                self.text = "/ферма"
        
        fake_msg = FakeMessage(call.message.chat.id, user_id)
        cmd_mainingferma(fake_msg)
        
    elif action == "collect4":
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT card4_balance FROM users WHERE user_id = ?', (user_id,))
        balance = cursor.fetchone()[0]
        
        if balance <= 0:
            bot.answer_callback_query(call.id, "Нет средств для снятия")
            conn.close()
            return
        
        cursor.execute('UPDATE users SET twists = twists + ?, card4_balance = 0, card4_last_collect = ? WHERE user_id = ?',
                      (balance, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
        conn.commit()
        conn.close()
        
        bot.answer_callback_query(call.id, f"✅ Снято {balance:,} твистов")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        class FakeMessage:
            def __init__(self, chat_id, from_user_id):
                self.chat = type('obj', (object,), {'id': chat_id})
                self.from_user = type('obj', (object,), {'id': from_user_id})
                self.text = "/ферма"
        
        fake_msg = FakeMessage(call.message.chat.id, user_id)
        cmd_mainingferma(fake_msg)
        
    elif action == "collect5":
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT card5_balance FROM users WHERE user_id = ?', (user_id,))
        balance = cursor.fetchone()[0]
        
        if balance <= 0:
            bot.answer_callback_query(call.id, "Нет средств для снятия")
            conn.close()
            return
        
        cursor.execute('UPDATE users SET twists = twists + ?, card5_balance = 0, card5_last_collect = ? WHERE user_id = ?',
                      (balance, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
        conn.commit()
        conn.close()
        
        bot.answer_callback_query(call.id, f"✅ Снято {balance:,} твистов")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        class FakeMessage:
            def __init__(self, chat_id, from_user_id):
                self.chat = type('obj', (object,), {'id': chat_id})
                self.from_user = type('obj', (object,), {'id': from_user_id})
                self.text = "/ферма"
        
        fake_msg = FakeMessage(call.message.chat.id, user_id)
        cmd_mainingferma(fake_msg)
        
    elif action == "refresh":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        class FakeMessage:
            def __init__(self, chat_id, from_user_id):
                self.chat = type('obj', (object,), {'id': chat_id})
                self.from_user = type('obj', (object,), {'id': from_user_id})
                self.text = "/ферма"
        
        fake_msg = FakeMessage(call.message.chat.id, user_id)
        cmd_mainingferma(fake_msg)
        
    elif action == "upgrade1":
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT twists, card1_level FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        twists = result[0]
        level = result[1]
        
        upgrade_cost = 10000 if level == 0 else 5000 * (level + 1)
        
        if twists < upgrade_cost:
            bot.answer_callback_query(call.id, f"Недостаточно твистов! Нужно {upgrade_cost:,}")
            conn.close()
            return
        
        cursor.execute('UPDATE users SET twists = twists - ?, card1_level = card1_level + 1 WHERE user_id = ?',
                      (upgrade_cost, user_id))
        conn.commit()
        conn.close()
        
        bot.answer_callback_query(call.id, f"✅ Улучшено до уровня {level + 1}")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        class FakeMessage:
            def __init__(self, chat_id, from_user_id):
                self.chat = type('obj', (object,), {'id': chat_id})
                self.from_user = type('obj', (object,), {'id': from_user_id})
                self.text = "/ферма"
        
        fake_msg = FakeMessage(call.message.chat.id, user_id)
        cmd_mainingferma(fake_msg)
        
    elif action == "upgrade2":
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT twists, card2_level FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        twists = result[0]
        level = result[1]
        
        upgrade_cost = 50000 if level == 0 else 25000 * (level + 1)
        
        if twists < upgrade_cost:
            bot.answer_callback_query(call.id, f"Недостаточно твистов! Нужно {upgrade_cost:,}")
            conn.close()
            return
        
        cursor.execute('UPDATE users SET twists = twists - ?, card2_level = card2_level + 1 WHERE user_id = ?',
                      (upgrade_cost, user_id))
        conn.commit()
        conn.close()
        
        bot.answer_callback_query(call.id, f"✅ Улучшено до уровня {level + 1}")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        class FakeMessage:
            def __init__(self, chat_id, from_user_id):
                self.chat = type('obj', (object,), {'id': chat_id})
                self.from_user = type('obj', (object,), {'id': from_user_id})
                self.text = "/ферма"
        
        fake_msg = FakeMessage(call.message.chat.id, user_id)
        cmd_mainingferma(fake_msg)
        
    elif action == "upgrade3":
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT twists, card3_level FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        twists = result[0]
        level = result[1]
        
        upgrade_cost = 350000
        
        if twists < upgrade_cost:
            bot.answer_callback_query(call.id, f"Недостаточно твистов! Нужно {upgrade_cost:,}")
            conn.close()
            return
        
        cursor.execute('UPDATE users SET twists = twists - ?, card3_level = card3_level + 1 WHERE user_id = ?',
                      (upgrade_cost, user_id))
        conn.commit()
        conn.close()
        
        bot.answer_callback_query(call.id, f"✅ Улучшено до уровня {level + 1}")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        class FakeMessage:
            def __init__(self, chat_id, from_user_id):
                self.chat = type('obj', (object,), {'id': chat_id})
                self.from_user = type('obj', (object,), {'id': from_user_id})
                self.text = "/ферма"
        
        fake_msg = FakeMessage(call.message.chat.id, user_id)
        cmd_mainingferma(fake_msg)
        
    elif action == "upgrade4":
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT twists, card4_level FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        twists = result[0]
        level = result[1]
        
        upgrade_cost = 15000000
        
        if twists < upgrade_cost:
            bot.answer_callback_query(call.id, f"Недостаточно твистов! Нужно {upgrade_cost:,}")
            conn.close()
            return
        
        cursor.execute('UPDATE users SET twists = twists - ?, card4_level = card4_level + 1 WHERE user_id = ?',
                      (upgrade_cost, user_id))
        conn.commit()
        conn.close()
        
        bot.answer_callback_query(call.id, f"✅ Улучшено до уровня {level + 1}")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
    elif action == "upgrade5":
     conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT twists, card5_level FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    if not result:
        bot.answer_callback_query(call.id, "Ошибка получения данных")
        conn.close()
        return
        
    twists = result[0]
    level = result[1]
    
    # Проверяем, не максимальный ли уже уровень
    if level >= 5:
        bot.answer_callback_query(call.id, "Уже максимальный уровень!")
        conn.close()
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        class FakeMessage:
            def __init__(self, chat_id, from_user_id):
                self.chat = type('obj', (object,), {'id': chat_id})
                self.from_user = type('obj', (object,), {'id': from_user_id})
                self.text = "/ферма"
        
        fake_msg = FakeMessage(call.message.chat.id, user_id)
        cmd_mainingferma(fake_msg)
        return
    
    upgrade_cost = 85000000  # 85 миллионов за улучшение
    
    if twists < upgrade_cost:
        bot.answer_callback_query(call.id, f"❌ Недостаточно твистов! Нужно {upgrade_cost:,}")
        conn.close()
        return
    
    # Списываем твисты и повышаем уровень
    cursor.execute('UPDATE users SET twists = twists - ?, card5_level = card5_level + 1 WHERE user_id = ?',
                  (upgrade_cost, user_id))
    conn.commit()
    conn.close()
    
    bot.answer_callback_query(call.id, f"✅ ZOTAC AMP EXTREME улучшена до уровня {level + 1}")
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
    # Обновляем отображение фермы
    class FakeMessage:
        def __init__(self, chat_id, from_user_id):
            self.chat = type('obj', (object,), {'id': chat_id})
            self.from_user = type('obj', (object,), {'id': from_user_id})
            self.text = "/ферма"
    
    fake_msg = FakeMessage(call.message.chat.id, user_id)
    cmd_mainingferma(fake_msg)
        
class FakeMessage:
    def __init__(self, chat_id, from_user_id):
        self.chat = type('obj', (object,), {'id': chat_id})
        self.from_user = type('obj', (object,), {'id': from_user_id})
        self.text = "/ферма"
        
        fake_msg = FakeMessage(call.message.chat.id, user_id)
        cmd_mainingferma(fake_msg)
        
# ===== КОМАНДА БОНУС =====
def cmd_bonus(message):
    """Выдает случайный бонус пользователю (до 10,000,000 твистов, раз в час)"""
    user_id = message.from_user.id
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    # Создаем таблицу если её нет
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_bonuses (
            user_id INTEGER PRIMARY KEY,
            last_bonus TEXT,
            total_bonuses INTEGER DEFAULT 0
        )
    ''')
    
    # Проверяем, когда пользователь получал бонус последний раз
    cursor.execute('SELECT last_bonus FROM user_bonuses WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    if result and result[0]:
        try:
            last_bonus = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
            time_diff = datetime.now() - last_bonus
            minutes_passed = time_diff.total_seconds() / 60
            
            # Проверяем, прошел ли час (60 минут)
            if minutes_passed < 60:
                minutes_left = 60 - minutes_passed
                bot.reply_to(message, f"⏳ Бонус можно получить раз в час! Подождите еще {minutes_left:.0f} минут")
                conn.close()
                return
        except:
            # Если ошибка с датой, игнорируем и даем бонус
            pass
    
    # Генерируем случайный бонус от 1,000 до 10,000,000
    bonus_amount = random.randint(1000, 10000000)
    
    # Начисляем бонус
    cursor.execute('UPDATE users SET twists = twists + ? WHERE user_id = ?', (bonus_amount, user_id))
    
    # Записываем время получения бонуса
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT OR REPLACE INTO user_bonuses (user_id, last_bonus, total_bonuses)
        VALUES (?, ?, COALESCE((SELECT total_bonuses FROM user_bonuses WHERE user_id = ?), 0) + 1)
    ''', (user_id, current_time, user_id))
    
    conn.commit()
    
    # Получаем новый баланс
    cursor.execute('SELECT twists FROM users WHERE user_id = ?', (user_id,))
    new_balance = cursor.fetchone()[0]
    conn.close()
    
    # Формируем ответ
    if bonus_amount >= 5000000:
        text = f"🎉 ДЖЕКПОТ! 🎉\n\n"
        text += f"💰 Вы получили бонус {bonus_amount:,} твистов!\n"
        text += f"💎 Новый баланс: {new_balance:,} твистов"
    elif bonus_amount >= 1000000:
        text = f"🌟 КРУПНЫЙ БОНУС! 🌟\n\n"
        text += f"💰 Вы получили {bonus_amount:,} твистов!\n"
        text += f"💎 Новый баланс: {new_balance:,} твистов"
    else:
        text = f"🎁 Вы получили бонус {bonus_amount:,} твистов!\n"
        text += f"💰 Новый баланс: {new_balance:,} твистов"
    
    bot.reply_to(message, text)
    
    # ===== КОМАНДЫ ИВЕНТА =====
def cmd_event(message):
    """Показывает статус ивента"""
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT hp, max_hp, is_active FROM event_boss WHERE id = 1')
    boss = cursor.fetchone()
    hp, max_hp, is_active = boss
    
    cursor.execute('SELECT COUNT(*) FROM event_stats WHERE damage_done > 0')
    participants = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(damage_done) FROM event_stats')
    total_damage = cursor.fetchone()[0] or 0
    
    conn.close()
    
    if not is_active:
        text = "🎮 ИВЕНТ ЗАВЕРШЕН\n\n"
        text += f"Босс был повержен! Всего нанесено урона: {total_damage}\n"
        text += f"Участников: {participants}"
    else:
        hp_percent = (hp / max_hp) * 100
        text = "👋 Привет, боец! Мы проводим спец.операцию «Щит родины»\n\n"
        text += "В боте появился броневик, который хочет испортить праздник!\n"
        text += f"Твоя основная задача - нанести как больше урона боссу (осталось {hp} ❤️)\n\n"
        text += "🔹 Команды:\n"
        text += "• /дуэль @user - вызов на дуэль (снимает 5 ❤️ босса за победу)\n"
        text += "• /бой - начать бой с боссом (снимает 100 ❤️ за победу)\n\n"
        text += f"📊 Статистика:\n"
        text += f"❤️ Здоровье босса: {hp}/{max_hp} ({hp_percent:.1f}%)\n"
        text += f"👥 Участников: {participants}\n"
        text += f"💥 Всего урона: {total_damage}"
    
    bot.reply_to(message, text)

def cmd_fight(message):
    """Начинает бой с боссом"""
    user_id = message.from_user.id
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    # Проверяем активен ли ивент
    cursor.execute('SELECT hp, is_active FROM event_boss WHERE id = 1')
    hp, is_active = cursor.fetchone()
    
    if not is_active or hp <= 0:
        bot.reply_to(message, "❌ Ивент уже завершен!")
        conn.close()
        return
    
    # Проверяем, не в бою ли уже пользователь
    cursor.execute('SELECT battle_active, hits_left FROM battle_state WHERE user_id = ?', (user_id,))
    battle = cursor.fetchone()
    
    if battle and battle[0]:
        hits_left = battle[1]
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        shoot_button = types.InlineKeyboardButton(f"🔫 Застрелить (35 млн)", callback_data=f"fight_shoot_{user_id}")
        hit_button = types.InlineKeyboardButton(f"👊 Ударить (850 тыс)", callback_data=f"fight_hit_{user_id}")
        
        markup.add(shoot_button, hit_button)
        
        bot.send_message(
            message.chat.id,
            f"😈 Бой уже идет! Осталось ударов: {hits_left}\n"
            f"🔫 Застрелить - 100 урона, 35 млн твистов\n"
            f"👊 Ударить - 33 урона, 850 тыс твистов (3 удара = 100 урона)",
            reply_markup=markup
        )
        conn.close()
        return
    
    # Начинаем новый бой
    cursor.execute('INSERT OR REPLACE INTO battle_state (user_id, hits_left, battle_active, battle_start_time) VALUES (?, 3, 1, ?)',
                  (user_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    shoot_button = types.InlineKeyboardButton(f"🔫 Застрелить (35 млн)", callback_data=f"fight_shoot_{user_id}")
    hit_button = types.InlineKeyboardButton(f"👊 Ударить (850 тыс)", callback_data=f"fight_hit_{user_id}")
    
    markup.add(shoot_button, hit_button)
    
    bot.send_message(
        message.chat.id,
        "😈 Осмелился пойти со мной на бой? Ну ладно, я не против победить вновь какого-то сопляка\n\n"
        "🔫 Застрелить - 100 урона, 35 млн твистов\n"
        "👊 Ударить - 33 урона, 850 тыс твистов (3 удара = 100 урона)",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('fight_'))
def fight_callback(call):
    data = call.data.split('_')
    action = data[1]
    user_id = int(data[2])
    
    if call.from_user.id != user_id:
        bot.answer_callback_query(call.id, "❌ Это не ваш бой")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    # Проверяем активен ли ивент
    cursor.execute('SELECT hp FROM event_boss WHERE id = 1')
    boss_hp = cursor.fetchone()[0]
    
    if boss_hp <= 0:
        bot.answer_callback_query(call.id, "❌ Босс уже побежден!")
        cursor.execute('UPDATE battle_state SET battle_active = 0 WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        bot.edit_message_text("🎉 Босс побежден! Ивент завершен.", call.message.chat.id, call.message.message_id)
        return
    
    # Проверяем баланс пользователя
    cursor.execute('SELECT twists FROM users WHERE user_id = ?', (user_id,))
    twists = cursor.fetchone()[0]
    
    if action == "shoot":
        cost = 35000000
        damage = 100
        if twists < cost:
            bot.answer_callback_query(call.id, f"❌ Недостаточно твистов! Нужно {cost:,}")
            conn.close()
            return
        
        # Списываем твисты
        cursor.execute('UPDATE users SET twists = twists - ? WHERE user_id = ?', (cost, user_id))
        
        # Наносим урон боссу
        new_hp = max(0, boss_hp - damage)
        cursor.execute('UPDATE event_boss SET hp = ? WHERE id = 1', (new_hp,))
        
        # Обновляем статистику
        cursor.execute('''
            INSERT INTO event_stats (user_id, damage_done, duels_won, battles_fought)
            VALUES (?, ?, 0, 1)
            ON CONFLICT(user_id) DO UPDATE SET
                damage_done = damage_done + ?,
                battles_fought = battles_fought + 1
        ''', (user_id, damage, damage))
        
        # Завершаем бой
        cursor.execute('UPDATE battle_state SET battle_active = 0 WHERE user_id = ?', (user_id,))
        conn.commit()
        
        bot.answer_callback_query(call.id, f"✅ Вы нанесли {damage} урона боссу!")
        
        if new_hp <= 0:
            bot.edit_message_text(
                f"🎉 ПОБЕДА! Босс повержен!\n\n"
                f"💥 Вы нанесли последний удар!",
                call.message.chat.id,
                call.message.message_id
            )
        else:
            bot.edit_message_text(
                f"🫤 Это было мощно! Не думал, что ты настолько силен.\n"
                f"Но это еще не конец...\n\n"
                f"❤️ У босса осталось {new_hp} HP",
                call.message.chat.id,
                call.message.message_id
            )
        
    elif action == "hit":
        cost = 850000
        damage_per_hit = 33
        
        # Получаем текущее состояние боя
        cursor.execute('SELECT hits_left FROM battle_state WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        if not result:
            bot.answer_callback_query(call.id, "❌ Бой не найден")
            conn.close()
            return
        
        hits_left = result[0]
        
        if twists < cost:
            bot.answer_callback_query(call.id, f"❌ Недостаточно твистов! Нужно {cost:,}")
            conn.close()
            return
        
        # Списываем твисты
        cursor.execute('UPDATE users SET twists = twists - ? WHERE user_id = ?', (cost, user_id))
        
        # Уменьшаем количество оставшихся ударов
        hits_left -= 1
        cursor.execute('UPDATE battle_state SET hits_left = ? WHERE user_id = ?', (hits_left, user_id))
        
        if hits_left <= 0:
            # Наносим полный урон (100)
            new_hp = max(0, boss_hp - 100)
            cursor.execute('UPDATE event_boss SET hp = ? WHERE id = 1', (new_hp,))
            
            # Обновляем статистику
            cursor.execute('''
                INSERT INTO event_stats (user_id, damage_done, duels_won, battles_fought)
                VALUES (?, ?, 0, 1)
                ON CONFLICT(user_id) DO UPDATE SET
                    damage_done = damage_done + ?,
                    battles_fought = battles_fought + 1
            ''', (user_id, 100, 100))
            
            # Завершаем бой
            cursor.execute('UPDATE battle_state SET battle_active = 0 WHERE user_id = ?', (user_id,))
            conn.commit()
            
            bot.answer_callback_query(call.id, f"✅ Серия ударов завершена! Нанесено 100 урона!")
            
            if new_hp <= 0:
                bot.edit_message_text(
                    f"🎉 ПОБЕДА! Босс повержен!\n\n"
                    f"💥 Вы нанесли последний удар!",
                    call.message.chat.id,
                    call.message.message_id
                )
            else:
                bot.edit_message_text(
                    f"🫤 Это было мощно! Не думал, что ты настолько силен.\n"
                    f"Но это еще не конец...\n\n"
                    f"❤️ У босса осталось {new_hp} HP",
                    call.message.chat.id,
                    call.message.message_id
                )
        else:
            conn.commit()
            bot.answer_callback_query(call.id, f"👊 Удар! Осталось ударов: {hits_left}")
            
            # Обновляем сообщение
            markup = types.InlineKeyboardMarkup(row_width=2)
            shoot_button = types.InlineKeyboardButton(f"🔫 Застрелить (35 млн)", callback_data=f"fight_shoot_{user_id}")
            hit_button = types.InlineKeyboardButton(f"👊 Ударить (850 тыс) [{hits_left}/3]", callback_data=f"fight_hit_{user_id}")
            markup.add(shoot_button, hit_button)
            
            bot.edit_message_text(
                f"😈 Бой продолжается! Осталось ударов: {hits_left}\n\n"
                f"🔫 Застрелить - 100 урона, 35 млн твистов\n"
                f"👊 Ударить - 33 урона, 850 тыс твистов",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=markup
            )
    
    conn.close()

def cmd_givemedal(message):
    """Выдает медаль пользователю (только для владельца)"""
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Только для владельца бота")
        return
    
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответьте на сообщение пользователя")
        return
    
    target = message.reply_to_message.from_user
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO medals (user_id, medal_bravery)
        VALUES (?, 1)
        ON CONFLICT(user_id) DO UPDATE SET medal_bravery = medal_bravery + 1
    ''', (target.id,))
    
    conn.commit()
    conn.close()
    
    bot.reply_to(message, f"✅ Пользователю {target.first_name} выдана медаль «За отвагу в чате»")

def cmd_statsevent(message):
    """Показывает статистику ивента (только для владельца)"""
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Только для владельца бота")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT u.user_id, u.nick, u.first_name, e.damage_done, e.duels_won, e.battles_fought
        FROM event_stats e
        JOIN users u ON u.user_id = e.user_id
        ORDER BY e.damage_done DESC
        LIMIT 10
    ''')
    
    top_users = cursor.fetchall()
    
    cursor.execute('SELECT SUM(damage_done), SUM(duels_won), SUM(battles_fought) FROM event_stats')
    total = cursor.fetchone()
    total_damage, total_duels, total_battles = total
    
    cursor.execute('SELECT hp FROM event_boss WHERE id = 1')
    boss_hp = cursor.fetchone()[0]
    
    conn.close()
    
    text = "📊 СТАТИСТИКА ИВЕНТА\n\n"
    text += f"❤️ Осталось HP босса: {boss_hp}\n"
    text += f"💥 Всего урона: {total_damage or 0}\n"
    text += f"⚔️ Всего дуэлей: {total_duels or 0}\n"
    text += f"🤺 Всего боёв: {total_battles or 0}\n\n"
    
    if top_users:
        text += "🏆 ТОП УЧАСТНИКОВ:\n\n"
        for i, (user_id, nick, first_name, damage, duels, battles) in enumerate(top_users, 1):
            name = nick or first_name
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            text += f"{medal} {name} - {damage} урона\n"
    else:
        text += "Пока нет участников"
    
    bot.reply_to(message, text)

def cmd_duel(message):
    """Дуэль с другим пользователем (снимает 5 HP с босса за победу)"""
    user_id = message.from_user.id
    
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответьте на сообщение пользователя для дуэли")
        return
    
    target = message.reply_to_message.from_user
    
    if target.id == user_id:
        bot.reply_to(message, "❌ Нельзя дуэлировать с самим собой")
        return
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    # Проверяем активен ли ивент
    cursor.execute('SELECT hp, is_active FROM event_boss WHERE id = 1')
    hp, is_active = cursor.fetchone()
    
    if not is_active or hp <= 0:
        bot.reply_to(message, "❌ Ивент уже завершен!")
        conn.close()
        return
    
    # Проверяем ставку
    try:
        parts = message.text.split()
        bet = int(parts[1]) if len(parts) > 1 else 1000
    except:
        bet = 1000
    
    conn.close()
    
    # Создаем клавиатуру для дуэли
    markup = types.InlineKeyboardMarkup(row_width=2)
    accept_btn = types.InlineKeyboardButton("✅ Принять", callback_data=f"duel_event_accept_{user_id}_{target.id}_{bet}")
    decline_btn = types.InlineKeyboardButton("❌ Отказать", callback_data=f"duel_event_decline_{user_id}_{target.id}")
    
    markup.add(accept_btn, decline_btn)
    
    bot.send_message(
        message.chat.id,
        f"⚔️ {message.from_user.first_name} вызывает {target.first_name} на дуэль!\n"
        f"💰 Ставка: {bet} твистов\n"
        f"🎯 Победитель нанесет 5 урона боссу!",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('duel_event_'))
def duel_event_callback(call):
    data = call.data.split('_')
    action = data[2]
    challenger_id = int(data[3])
    opponent_id = int(data[4])
    
    if action == "accept":
        if call.from_user.id != opponent_id:
            bot.answer_callback_query(call.id, "❌ Это не ваш вызов")
            return
        
        bet = int(data[5])
        
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        
        # Проверяем балансы
        cursor.execute('SELECT twists FROM users WHERE user_id = ?', (challenger_id,))
        challenger_twists = cursor.fetchone()[0]
        
        cursor.execute('SELECT twists FROM users WHERE user_id = ?', (opponent_id,))
        opponent_twists = cursor.fetchone()[0]
        
        if challenger_twists < bet or opponent_twists < bet:
            bot.answer_callback_query(call.id, "❌ У одного из участников недостаточно средств")
            bot.edit_message_text("❌ Дуэль отменена из-за недостатка средств", call.message.chat.id, call.message.message_id)
            conn.close()
            return
        
        # Определяем победителя
        winner_id = challenger_id if random.randint(0, 1) == 0 else opponent_id
        loser_id = opponent_id if winner_id == challenger_id else challenger_id
        
        # Переводим твисты
        cursor.execute('UPDATE users SET twists = twists + ? WHERE user_id = ?', (bet, winner_id))
        cursor.execute('UPDATE users SET twists = twists - ? WHERE user_id = ?', (bet, loser_id))
        
        # Наносим урон боссу (5 HP)
        cursor.execute('SELECT hp FROM event_boss WHERE id = 1')
        boss_hp = cursor.fetchone()[0]
        new_hp = max(0, boss_hp - 5)
        cursor.execute('UPDATE event_boss SET hp = ? WHERE id = 1', (new_hp,))
        
        # Обновляем статистику
        cursor.execute('''
            INSERT INTO event_stats (user_id, damage_done, duels_won, battles_fought)
            VALUES (?, 5, 1, 0)
            ON CONFLICT(user_id) DO UPDATE SET
                damage_done = damage_done + 5,
                duels_won = duels_won + 1
        ''', (winner_id,))
        
        conn.commit()
        conn.close()
        
        winner_name = bot.get_chat(winner_id).first_name
        loser_name = bot.get_chat(loser_id).first_name
        
        text = f"⚔️ ДУЭЛЬ СОСТОЯЛАСЬ!\n\n"
        text += f"🏆 Победитель: {winner_name}\n"
        text += f"💰 Выигрыш: {bet} твистов\n"
        text += f"💥 Нанесено урона боссу: 5\n\n"
        
        if new_hp <= 0:
            text += f"🎉 Босс повержен! Ивент завершен!"
        
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        
    elif action == "decline":
        if call.from_user.id != opponent_id:
            bot.answer_callback_query(call.id, "❌ Это не ваш вызов")
            return
        
        challenger_name = bot.get_chat(challenger_id).first_name
        bot.edit_message_text(f"❌ {challenger_name}, ваш вызов отклонен", call.message.chat.id, call.message.message_id)

# ---------- ЗАПУСК БОТА ----------
if __name__ == '__main__':
    print("✅ Бот запущен!")
    print("✅ Команды: /profile, /список, /донат, /giverub, /курс, /продать")
    bot.infinity_polling()
    
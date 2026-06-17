import telebot
from telebot import types
from telebot.types import MessageEntity, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import random
import emoji
import time
import os
import json
from datetime import datetime

# ============================================================
# Bot Credentials
# ============================================================
TOKEN = "8897529808:AAFOr23D_uNaJy5dGjPcPdvC8D1se9e49nc"
ADMIN_IDS = [7898928200, 6907359862]
bot = telebot.TeleBot(TOKEN)

bot_active = True
user_db_file = "users.json"

def load_users():
    if os.path.exists(user_db_file):
        with open(user_db_file, "r") as f:
            return set(json.load(f))
    return set()

def save_users(users: set):
    with open(user_db_file, "w") as f:
        json.dump(list(users), f)

all_users: set = load_users()

# ============================================================
# EMOJI MAPPING - Normal Emoji -> Related Premium Emoji ID
# ============================================================
EMOJI_MAPPING = {
    # Check marks / Verification
    "✅": ["6246537187614005254", "6246782404476803545", "6010060634803148161", "6010498532488778300"],
    "✔️": ["6246871001062185760", "6010264538375525668", "6010487760710800947"],
    "☑️": ["6246537187614005254", "6010097953773983121"],
    
    # Eyes / Vision
    "👁️": ["6035338338406242050", "6035051267087143217", "6034945975963881533", "6034845323405299835"],
    "👁": ["6035338338406242050", "6035051267087143217"],
    "👀": ["6035225389356290238", "6035081585261287115", "6035243995154616907", "6035173858338672933"],
    
    # Fire / Hot / Trending
    "🔥": ["4956222745814762495", "4956606007221421405", "4956429969396859866", "6086954744268460848"],
    "💥": ["6032673796530377389", "4958479549265347295"],
    "⚡": ["5791970059597386804", "6087079590377820415", "6095843123252957701"],
    
    # Hearts / Love
    "❤️": ["5783157259152397008", "5801084710343938087", "6010280773351904888"],
    "💙": ["5780496071645991525", "6104780447684757396"],
    "💚": ["5888789252493283486"],
    "💛": ["5840261097719148872"],
    "🧡": ["5840263144212529797"],
    "💜": ["5840265018655703965"],
    "🖤": ["5840266939932994956"],
    
    # Stars / Rating
    "⭐": ["6244496562752331516", "5904618938578243567", "6010193314932855525"],
    "🌟": ["6010156854955480259", "6086924086791902713"],
    "✨": ["6010338729640596556", "6010086134023985536", "5801044672658805468"],
    
    # Vampire / Monster
    "🧛": ["6034871295072539452", "6035251193519805118", "6032673796530377389"],
    "🧛‍♂️": ["6034871295072539452", "6035251193519805118"],
    "👹": ["6034962795055812935"],
    "👺": ["6034962795055812935"],
    "👻": ["6035070298087231243"],
    "👿": ["6035242444671421879", "6032985916098750553"],
    "😈": ["6035136809950778133", "6032695825417638128", "6032739101508113500"],
    
    # Crown / King
    "👑": ["5794422335599546668", "6089003761496232797", "6247039939305808563"],
    
    # Money / Wealth
    "💰": ["6089104607328342288", "6086730718774300509", "6086664791026307819"],
    "💵": ["6089140105233044310"],
    "💎": ["6086778246882399112", "5791697221799907788"],
    
    # Thumbs up/down
    "👍": ["6089313931149448495", "4958626617535497157", "4956582500865410174"],
    "👎": ["6088789257285988672"],
    
    # Clapping
    "👏": ["6093744967304352336", "4956582500865410174"],
    
    # Smileys
    "😀": ["6093864814071780526", "6093922327978840798"],
    "😁": ["6035060329468137931"],
    "😂": ["5782741660936966676", "5782746664573867142"],
    "😃": ["6035337951859184840"],
    "😄": ["5782942227319756256"],
    "😅": ["5782670102486848559"],
    "😆": ["5782670102486848559"],
    "😉": ["6089024570612781324"],
    "😊": ["5780690182692935276"],
    "😍": ["6010179687001625256"],
    "🥰": ["6044369013952222465", "6044359320211034681"],
    "😘": ["6044373012566774137"],
    "😎": ["6032853480782172520", "6044373012566774137"],
    "😢": ["5780793884678296697"],
    "😭": ["5783024321324651865"],
    "😤": ["6034865170449175739", "6034855438053282213"],
    "😠": ["6035355642829475999", "6034843326245508065"],
    "😡": ["6035355642829475999"],
    "🤔": ["5782756916660802905", "5783034045130610245", "6093666528316625608"],
}

# ============================================================
# COUNTRY FLAG MAPPING - Flag Emoji -> Premium Flag ID
# ============================================================
FLAG_MAPPING = {
    "🇺🇸": "5433865586356531140", "🇬🇧": "5433827537241258614", "🇫🇷": "5433636707549331311",
    "🇩🇪": "5433845881046578644", "🇮🇳": "5433601609076586221", "🇯🇵": "5434147542369579483",
    "🇨🇳": "5435996255207567113", "🇷🇺": "5433674924168328689", "🇧🇷": "5433825269498525925",
    "🇮🇹": "5433627189901801019", "🇨🇦": "5433979415874779870", "🇦🇺": "5434067655977874913",
    "🇰🇷": "5434142701941437163", "🇪🇸": "5434026158003862063", "🇲🇽": "5434131139889478358",
    "🇮🇩": "5431739800883312139", "🇳🇱": "5431656358258685474", "🇹🇷": "5433792911214917126",
    "🇸🇦": "5433991338703991663", "🇦🇪": "5434013938821902926", "🇿🇦": "5431489619038320862",
    "🇵🇰": "5434064563601421981", "🇧🇩": "5433854239052935880",
    "🇱🇰": "5433609855413794108", "🇳🇵": "5433852744404317916", "🇲🇾": "5431620340662940910",
    "🇸🇬": "5433884376838454074", "🇵🇭": "5434119663736862995", "🇻🇳": "5431676201007592926",
    "🇹🇭": "5433814347396692144", "🇪🇬": "5433643519367461444", "🇳🇬": "5433982207603520017",
    "🇰🇪": "5433845881046578644", "🇦🇷": "5433845881046578644", "🇨🇱": "5433827537241258614",
    "🇵🇪": "5433827537241258614", "🇨🇴": "5433825269498525925", "🇻🇪": "5433767976937585990",
    "🇵🇹": "5433598722858562967", "🇸🇪": "5433628435442316429", "🇳🇴": "5434098446598419585",
    "🇩🇰": "5434129692485498098", "🇫🇮": "5434115081006756195", "🇮🇪": "5434012796360604182",
    "🇨🇭": "5433902785068283672", "🇦🇹": "5434027579638035690", "🇧🇪": "5431755073787016798",
    "🇬🇷": "5433972762970437003", "🇨🇿": "5434115081006756195", "🇭🇺": "5434001565021123877",
    "🇵🇱": "5433833485770964033", "🇷🇴": "5434132406904830055", "🇺🇦": "5434132406904830055",
}

# ============================================================
# PRIMARY EMOJIS FROM Reobashd pack (70 emojis)
# ============================================================
PRIMARY_EMOJIS = [
    "6035051267087143217", "6034945975963881533", "6034845323405299835", "6035169816774446606",
    "6035085583875837709", "6032965553658794901", "6035158121578501544", "6035208832257364215",
    "6035067476293718178", "6033130342964007608", "6035179291472302298", "6034986056598688136",
    "6032765485492214347", "6032660275973330342", "6034916516783198293", "6034904439335162652",
    "6034928023000585140", "6035372904303038740", "6035137110598492010", "6035338338406242050",
    "6035225389356290238", "6035081585261287115", "6035243995154616907", "6034865170449175739",
    "6035173858338672933", "6035210301136182368", "6035265083444042235", "6034871295072539452",
    "6035251193519805118", "6035136809950778133", "6032695825417638128", "6032739101508113500",
    "6032985916098750553", "6035374291577475270", "6035355642829475999", "6035337951859184840",
    "6035072209347678547", "6035060329468137931", "6033077437556855182", "6032823763903452409",
    "6034853694296560978", "6035015146412183834", "6035372401791864953", "6034955549445984368",
    "6032673796530377389", "6032916496542339992", "6034855438053282213", "6034962795055812935",
    "6034832094906028632", "6035087164423802534", "6035343380697846690", "6032737138708059114",
    "6035194237958493530", "6035317340311129897", "6035070298087231243", "6035242444671421879",
    "6034957847253487695", "6034925781027656042", "6033067975743902590", "6032975015471747801",
    "6034926000070988470", "6034843326245508065", "6032853480782172520", "6044373012566774137",
    "6044369013952222465", "6044359320211034681", "6044290806892729376", "6044238120528908813",
    "5791970059597386804", "5794422335599546668",
]

# ============================================================
# ALL PREMIUM EMOJIS (Complete pool for fallback)
# ============================================================
ALL_PREMIUM_EMOJIS = PRIMARY_EMOJIS + [
    "6246537187614005254", "6246610665914505571", "6244496562752331516", "6246782404476803545",
    "6247039939305808563", "6246774261218810895", "6246871001062185760",
    "5780840497958360623", "5780413823022273797", "5782940582347281850", "5783091623462180025",
    "5783151611270403662", "5783124312458270318", "5782741660936966676", "5782753386197685582",
    "5783029694328738752", "5782671841948603573", "5780425243340313827", "5783170625090622777",
    "5782858359493366808", "5783016603268420398", "5782914709464289647", "5782897082918507949",
    "5783023329187206172", "5782731481864475831", "5782734256413349701", "5783133172975801184",
    "5783157259152397008", "5783175250770399822", "5782876166427775766", "5782804668107199927",
    "5783176625159935132", "5782829832320586664", "5782670102486848559", "5782901906166780625",
    "6084695058894819673", "6086730718774300509", "6086664791026307819", "6089003761496232797",
    "6298332994260175589", "6296140830067395531", "6298821774423361023", "6136464120779638846",
    "4956222745814762495", "4958617898751886363", "4958479549265347295", "4958624886663678191",
]

ALL_PREMIUM_EMOJIS = list(set(ALL_PREMIUM_EMOJIS))

DEFAULT_EMOJI_ID = "6035338338406242050"
PLACEHOLDER = "🌟"
temp_data = {}

# ============================================================
# EMOJI CONVERSION FUNCTION (SMART MAPPING)
# ============================================================
_emoji_id_cache: dict = {}
EMOJI_CACHE_TTL = 1800

def _normalize_emoji(e: str) -> str:
    normalized = e.replace('\ufe0f', '').replace('\ufe0e', '').replace('\u200d', '')
    return normalized if normalized else e

def get_premium_emoji_for_normal_emoji(normal_emoji: str) -> str:
    now = time.time()
    cached = _emoji_id_cache.get(normal_emoji)
    if cached and (now - cached[1]) < EMOJI_CACHE_TTL:
        return cached[0]
    key = normal_emoji
    if key not in EMOJI_MAPPING and key not in FLAG_MAPPING:
        key = _normalize_emoji(normal_emoji)
    if key in EMOJI_MAPPING:
        chosen = random.choice(EMOJI_MAPPING[key])
    elif key in FLAG_MAPPING:
        chosen = FLAG_MAPPING[key]
    else:
        chosen = random.choice(ALL_PREMIUM_EMOJIS)
    _emoji_id_cache[normal_emoji] = (chosen, now)
    return chosen

def get_random_primary_emoji() -> str:
    return random.choice(PRIMARY_EMOJIS)

# ============================================================
# BUTTON CREATION
# ============================================================

def _extract_first_emoji(text: str):
    import unicodedata
    chars = list(text)
    i = 0
    while i < len(chars):
        ch = chars[i]
        if (i + 1 < len(chars)
                and '\U0001F1E0' <= ch <= '\U0001F1FF'
                and '\U0001F1E0' <= chars[i + 1] <= '\U0001F1FF'):
            seq = ch + chars[i + 1]
            cleaned = "".join(chars[:i] + chars[i + 2:]).strip()
            return seq, cleaned
        if emoji.is_emoji(ch):
            seq = ch
            j = i + 1
            while j < len(chars) and (
                chars[j] in ('\u200d', '\ufe0f', '\ufe0e')
                or unicodedata.category(chars[j]) in ('Mn', 'Mc')
                or '\U0001F3FB' <= chars[j] <= '\U0001F3FF'
            ):
                seq += chars[j]
                j += 1
            cleaned = "".join(chars[:i] + chars[j:]).strip()
            return seq, cleaned
        i += 1
    return None, text

def _make_btn(text: str, style: str = None, icon_id: str = None, **kwargs) -> InlineKeyboardButton:
    if icon_id and style:
        try:
            return InlineKeyboardButton(text=text, icon_custom_emoji_id=icon_id, style=style, **kwargs)
        except TypeError:
            pass
    if icon_id:
        try:
            return InlineKeyboardButton(text=text, icon_custom_emoji_id=icon_id, **kwargs)
        except TypeError:
            pass
    if style:
        try:
            return InlineKeyboardButton(text=text, style=style, **kwargs)
        except TypeError:
            pass
    return InlineKeyboardButton(text=text, **kwargs)

def make_button(text: str, style: str = None, **kwargs) -> InlineKeyboardButton:
    """Create button for user's custom buttons - NO auto emoji conversion"""
    return _make_btn(text, style=style, **kwargs)

def make_button_with_icon(text: str, style: str = None, **kwargs) -> InlineKeyboardButton:
    """Create button WITH premium emoji icon for bot's own buttons"""
    first_emoji, _ = _extract_first_emoji(text)
    if first_emoji:
        premium_id = get_premium_emoji_for_normal_emoji(first_emoji)
    else:
        premium_id = get_random_primary_emoji()
    return _make_btn(text, style=style, icon_id=premium_id, **kwargs)

def make_styled_row(buttons_config: list) -> list:
    row = []
    for cfg in buttons_config:
        cfg_copy = cfg.copy()
        text = cfg_copy.pop("text")
        style = cfg_copy.pop("style", None)
        row.append(make_button_with_icon(text, style=style, **cfg_copy))
    return row

# ============================================================
# FORCE JOIN CHANNELS
# ============================================================
REQUIRED_CHANNELS = [
    {"id": "-1003360548513", "name": "𝐄𝐗𝐔 𝐂𝐎𝐃𝐄𝐑 ⚡", "link": "https://t.me/exucoder1"},
    {"id": "-1003918756977", "name": "𝐙𝐄𝐑𝐈𝐍〆𝐂𝐎𝐃𝐄𝐗", "link": "https://t.me/+K8ApbzQOj-piZDU1"},
    {"id": "-1003669933791", "name": "𝐄𝐗𝐔〆𝐏𝐑𝐈𝐌𝐄", "link": "https://t.me/exucodex"},
    {"id": "-1003564583501", "name": "𝐕𝐀𝐍𝐙𝐎〆𝐂𝐈𝐙𝐘", "link": "https://t.me/vanzocizy"},
    {"id": "-1003645019104", "name": "ᴡᴇʙꜱɪᴛᴇ〆ꜰɪʟᴇ", "link": "https://t.me/webfileexu"},
]

def _utf16_len(ch: str) -> int:
    return len(ch.encode("utf-16-le")) // 2

def _utf16_len_str(s: str) -> int:
    return len(s.encode("utf-16-le")) // 2

def _build_pe_entities(text: str, use_primary: bool = True):
    entities = []
    utf16_offset = 0
    total_utf16 = _utf16_len_str(text)
    
    if total_utf16 > 0:
        entities.append(MessageEntity(type="bold", offset=0, length=total_utf16))
    
    for ch in text:
        ch_len = _utf16_len(ch)
        if ch == PLACEHOLDER:
            eid = random.choice(PRIMARY_EMOJIS) if use_primary else random.choice(ALL_PREMIUM_EMOJIS)
            entities.append(MessageEntity(
                type="custom_emoji",
                offset=utf16_offset,
                length=ch_len,
                custom_emoji_id=eid
            ))
        utf16_offset += ch_len
    
    return entities

def _send_pe(chat_id, text: str, use_primary: bool = True, reply_markup=None):
    entities = _build_pe_entities(text, use_primary)
    return bot.send_message(chat_id, text, entities=entities, reply_markup=reply_markup, parse_mode=None)

def _send_pe_return(chat_id, text: str, use_primary: bool = True, reply_markup=None):
    entities = _build_pe_entities(text, use_primary)
    return bot.send_message(chat_id, text, entities=entities, reply_markup=reply_markup, parse_mode=None)

def process_text_and_entities(text: str, original_entities: list):
    final_text = ""
    new_entities = []
    offset_map = {}
    old_off = 0
    new_off = 0
    
    for char in text:
        offset_map[old_off] = new_off
        old_ch_len = _utf16_len(char)
        
        if emoji.is_emoji(char):
            premium_id = get_premium_emoji_for_normal_emoji(char)
            ph_len = _utf16_len(PLACEHOLDER)
            new_entities.append(MessageEntity(
                type="custom_emoji",
                offset=new_off,
                length=ph_len,
                custom_emoji_id=premium_id
            ))
            final_text += PLACEHOLDER
            old_off += old_ch_len
            new_off += ph_len
        else:
            final_text += char
            old_off += old_ch_len
            new_off += old_ch_len
    
    offset_map[old_off] = new_off
    
    for ent in (original_entities or []):
        if ent.type == "custom_emoji":
            continue
        ns = offset_map.get(ent.offset)
        ne = offset_map.get(ent.offset + ent.length)
        if ns is not None and ne is not None and ne > ns:
            new_entities.append(MessageEntity(
                type=ent.type,
                offset=ns,
                length=ne - ns,
                url=ent.url,
                user=ent.user,
                language=ent.language,
                custom_emoji_id=ent.custom_emoji_id
            ))
    
    if final_text:
        total_len = _utf16_len_str(final_text)
        new_entities.append(MessageEntity(type="bold", offset=0, length=total_len))
    
    return final_text, new_entities

def is_admin(user_id):
    return user_id in ADMIN_IDS

def check_joined(uid: int) -> list:
    if is_admin(uid):
        return []
    
    not_joined = []
    for ch in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(ch["id"], uid)
            if member.status in ("left", "kicked", "banned"):
                not_joined.append(ch)
        except Exception:
            not_joined.append(ch)
    return not_joined

def send_join_notice(chat_id: int, not_joined: list):
    joined_count = len(REQUIRED_CHANNELS) - len(not_joined)
    total_count = len(REQUIRED_CHANNELS)
    
    keyboard = []
    for ch in not_joined:
        keyboard.append([InlineKeyboardButton(text=f"📢 {ch['name']}", url=ch["link"])])
    keyboard.append([make_button_with_icon(text="✅ 𝐈 𝐇𝐀𝐕𝐄 𝐉𝐎𝐈𝐍𝐄𝐃", style="success", callback_data="check_join")])
    markup = InlineKeyboardMarkup(keyboard)
    
    status_text = ""
    for ch in REQUIRED_CHANNELS:
        if ch in not_joined:
            status_text += f"📢  ❌ {ch['name']}\n"
        else:
            status_text += f"📢  ✅ {ch['name']}\n"
    
    text = f"""
{PLACEHOLDER}═══《 🔒 𝐀𝐂𝐂𝐄𝐒𝐒 𝐃𝐄𝐍𝐈𝐄𝐃! 》═══{PLACEHOLDER}

🚫 𝐀𝐂𝐂𝐄𝐒𝐒 𝐃𝐄𝐍𝐈𝐄𝐃!

📊 𝐏𝐑𝐎𝐆𝐑𝐄𝐒𝐒: {joined_count}/{total_count} 𝐉𝐎𝐈𝐍𝐄𝐃

⚠️ 𝐓𝐎 𝐔𝐒𝐄 𝐓𝐇𝐈𝐒 𝐁𝐎𝐓, 𝐘𝐎𝐔 𝐌𝐔𝐒𝐓 𝐉𝐎𝐈𝐍 𝐀𝐋𝐋 𝐂𝐇𝐀𝐍𝐍𝐄𝐋𝐒 𝐅𝐈𝐑𝐒𝐓!

{status_text}
👇 𝐂𝐋𝐈𝐂𝐊 𝐓𝐇𝐄 𝐁𝐔𝐓𝐓𝐎𝐍𝐒 𝐁𝐄𝐋𝐎𝐖 𝐓𝐎 𝐉𝐎𝐈𝐍: 👇

{PLACEHOLDER}═══════════════════════{PLACEHOLDER}
"""
    _send_pe(chat_id, text, reply_markup=markup)

def register_user(uid: int):
    if uid not in all_users:
        all_users.add(uid)
        save_users(all_users)

# ============================================================
# MAIN MENU - WITH EMOJI BUTTONS
# ============================================================
def get_menu(user_id):
    """Returns keyboard menu with emoji buttons"""
    is_admin_user = is_admin(user_id)
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    if is_admin_user:
        markup.row(
            KeyboardButton("🔴 𝐁𝐎𝐓 𝐎𝐅𝐅"),
            KeyboardButton("🟢 𝐁𝐎𝐓 𝐎𝐍")
        )
        markup.row(
            KeyboardButton("🌿 𝐌𝐀𝐊𝐄 𝐏𝐎𝐒𝐓"),
            KeyboardButton("💢 𝐁𝐑𝐎𝐀𝐃𝐂𝐀𝐒𝐓")
        )
        markup.row(
            KeyboardButton("👾 𝐔𝐒𝐄𝐑𝐒 𝐋𝐈𝐒𝐓"),
            KeyboardButton("🍁 𝐁𝐎𝐓 𝐒𝐓𝐀𝐓𝐒")
        )
        markup.row(
            KeyboardButton("🍂 𝐇𝐄𝐋𝐏"),
            KeyboardButton("🍀 𝐀𝐁𝐎𝐔𝐓 𝐁𝐎𝐓")
        )
    else:
        markup.row(KeyboardButton("🌿 𝐌𝐀𝐊𝐄 𝐏𝐎𝐒𝐓"))
        markup.row(
            KeyboardButton("🍂 𝐇𝐄𝐋𝐏"),
            KeyboardButton("🍀 𝐀𝐁𝐎𝐔𝐓 𝐁𝐎𝐓")
        )
        markup.row(KeyboardButton("🪾 𝐒𝐓𝐀𝐓𝐒"))
    
    return markup

def send_welcome_message(user_name: str, user_id: int):
    status = "𝐀𝐃𝐌𝐈𝐍" if is_admin(user_id) else "𝐔𝐒𝐄𝐑"
    
    text = f"""
{PLACEHOLDER}═══《 {PLACEHOLDER} 𝐆𝐨𝐨𝐝 𝐀𝐟𝐭𝐞𝐫𝐧𝐨𝐨𝐧! {PLACEHOLDER} 》═══{PLACEHOLDER}

{PLACEHOLDER} 𝐔𝐬𝐞𝐫: {user_name}
{PLACEHOLDER} 𝐔𝐬𝐞𝐫 𝐈𝐃: {user_id}
{PLACEHOLDER} 𝐒𝐭𝐚𝐭𝐮𝐬: {status}

╰═══════《 {PLACEHOLDER} 》═══════{PLACEHOLDER}

𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐄𝐌𝐎𝐉𝐈 𝐁𝐎𝐓

{PLACEHOLDER} 𝐀𝐛𝐨𝐮𝐭 𝐓𝐡𝐢𝐬 𝐁𝐨𝐭:
• {PLACEHOLDER} 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐀𝐧𝐢𝐦𝐚𝐭𝐞𝐝 𝐄𝐦𝐨𝐣𝐢 𝐂𝐨𝐧𝐯𝐞𝐫𝐭𝐞𝐫
• {PLACEHOLDER} 𝐂𝐨𝐧𝐯𝐞𝐫𝐭 𝐚𝐧𝐲 𝐞𝐦𝐨𝐣𝐢 𝐭𝐨 𝐩𝐫𝐞𝐦𝐢𝐮𝐦
• {PLACEHOLDER} 𝐏𝐫𝐞𝐬𝐞𝐫𝐯𝐞𝐬 𝐚𝐥𝐥 𝐟𝐨𝐫𝐦𝐚𝐭𝐭𝐢𝐧𝐠
• {PLACEHOLDER} 𝐒𝐮𝐩𝐩𝐨𝐫𝐭𝐬 𝐭𝐞𝐱𝐭, 𝐩𝐡𝐨𝐭𝐨, 𝐯𝐢𝐝𝐞𝐨, 𝐝𝐨𝐜𝐮𝐦𝐞𝐧𝐭
• {PLACEHOLDER} 𝐀𝐝𝐝 𝐦𝐮𝐥𝐭𝐢𝐩𝐥𝐞 𝐢𝐧𝐥𝐢𝐧𝐞 𝐛𝐮𝐭𝐭𝐨𝐧𝐬

━━━━━━━━━━━━━━━━━━━━━━

{PLACEHOLDER} 𝐀𝐜𝐜𝐞𝐬𝐬 𝐆𝐫𝐚𝐧𝐭𝐞𝐝!
𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 𝐬𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐣𝐨𝐢𝐧𝐞𝐝 𝐚𝐥𝐥 𝐜𝐡𝐚𝐧𝐧𝐞𝐥𝐬.

{PLACEHOLDER} 𝐐𝐮𝐢𝐜𝐤 𝐆𝐮𝐢𝐝𝐞:
• 𝐔𝐬𝐞 𝐦𝐞𝐧𝐮 𝐛𝐮𝐭𝐭𝐨𝐧𝐬 𝐭𝐨 𝐧𝐚𝐯𝐢𝐠𝐚𝐭𝐞
• /𝐡𝐞𝐥𝐩 𝐟𝐨𝐫 𝐦𝐨𝐫𝐞 𝐢𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧
• 𝐌𝐀𝐊𝐄 𝐏𝐎𝐒𝐓 𝐭𝐨 𝐜𝐫𝐞𝐚𝐭𝐞

⚠️ 𝐍𝐨𝐭𝐞: 𝐈𝐟 𝐲𝐨𝐮 𝐥𝐞𝐚𝐯𝐞 𝐚𝐧𝐲 𝐜𝐡𝐚𝐧𝐧𝐞𝐥, 𝐲𝐨𝐮 𝐰𝐢𝐥𝐥 𝐥𝐨𝐬𝐞 𝐚𝐜𝐜𝐞𝐬𝐬!

{PLACEHOLDER}━━━━━━━━━━━━━━━━━━━━━━{PLACEHOLDER}
"""
    return text

# Helper function to match button text with or without emoji prefix
def button_matches(text: str, *targets) -> bool:
    """Check if button text matches any target, ignoring emoji prefix"""
    if not text:
        return False
    # Strip any emoji prefix (like 🌿, 🔴, 🟢, etc.)
    cleaned = text.strip()
    # Remove first emoji if present
    first_char = cleaned[0] if cleaned else ""
    if emoji.is_emoji(first_char):
        cleaned = cleaned[1:].strip()
    for target in targets:
        if cleaned == target or text == target:
            return True
    return False

# ============================================================
# BOT COMMAND HANDLERS - UPDATED WITH EMOJI SUPPORT
# ============================================================

@bot.message_handler(commands=["start"])
def welcome(message):
    uid = message.from_user.id
    
    if not is_admin(uid):
        not_joined = check_joined(uid)
        if not_joined:
            send_join_notice(message.chat.id, not_joined)
            return
    
    register_user(uid)
    
    if not bot_active and not is_admin(uid):
        text = f"""
{PLACEHOLDER}═══《 🔴 𝐁𝐎𝐓 𝐎𝐅𝐅𝐋𝐈𝐍𝐄 》═══{PLACEHOLDER}

𝐁𝐎𝐓 𝐈𝐒 𝐍𝐎𝐖 𝐎𝐅𝐅𝐋𝐈𝐍𝐄.

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""
        _send_pe(message.chat.id, text)
        return
    
    name = message.from_user.first_name or "Friend"
    kb = get_menu(uid)
    text = send_welcome_message(name, uid)
    _send_pe(message.chat.id, text, reply_markup=kb)

@bot.message_handler(func=lambda m: button_matches(m.text, "𝐇𝐄𝐋𝐏"))
def help_msg(message):
    uid = message.from_user.id
    kb = get_menu(uid)
    
    text = f"""
{PLACEHOLDER}═══《 {PLACEHOLDER} 𝐇𝐎𝐖 𝐓𝐎 𝐔𝐒𝐄 》═══{PLACEHOLDER}

𝐒𝐓𝐄𝐏 𝟏: 𝐓𝐀𝐏 𝐌𝐀𝐊𝐄 𝐏𝐎𝐒𝐓

𝐒𝐓𝐄𝐏 𝟐: 𝐒𝐄𝐍𝐃 𝐘𝐎𝐔𝐑 𝐓𝐄𝐗𝐓 𝐌𝐄𝐒𝐒𝐀𝐆𝐄

𝐒𝐓𝐄𝐏 𝟑: 𝐂𝐇𝐎𝐎𝐒𝐄 𝐌𝐄𝐃𝐈𝐀

𝐒𝐓𝐄𝐏 𝟒: 𝐂𝐇𝐎𝐎𝐒𝐄 𝐁𝐔𝐓𝐓𝐎𝐍𝐒 (𝟏-𝟒)

𝐒𝐓𝐄𝐏 𝟓: 𝐄𝐍𝐓𝐄𝐑 𝐁𝐔𝐓𝐓𝐎𝐍 𝐍𝐀𝐌𝐄

𝐒𝐓𝐄𝐏 𝟔: 𝐄𝐍𝐓𝐄𝐑 𝐁𝐔𝐓𝐓𝐎𝐍 𝐔𝐑𝐋

𝐒𝐓𝐄𝐏 𝟕: 𝐂𝐇𝐎𝐎𝐒𝐄 𝐁𝐔𝐓𝐓𝐎𝐍 𝐂𝐎𝐋𝐎𝐑

𝐒𝐓𝐄𝐏 𝟖: 𝐏𝐑𝐄𝐕𝐈𝐄𝐖 & 𝐃𝐎𝐍𝐄!

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""
    _send_pe(message.chat.id, text, reply_markup=kb)

@bot.message_handler(func=lambda m: button_matches(m.text, "𝐀𝐁𝐎𝐔𝐓 𝐁𝐎𝐓"))
def about_bot(message):
    uid = message.from_user.id
    kb = get_menu(uid)
    total = len(all_users)
    
    text = f"""
{PLACEHOLDER}═══《 🔥 𝐀𝐁𝐎𝐔𝐓 𝐁𝐎𝐓 》═══{PLACEHOLDER}

𝐓𝐇𝐈𝐒 𝐁𝐎𝐓 𝐂𝐎𝐍𝐕𝐄𝐑𝐓𝐒 𝐍𝐎𝐑𝐌𝐀𝐋 𝐄𝐌𝐎𝐉𝐈𝐒 𝐓𝐎
𝐓𝐄𝐋𝐄𝐆𝐑𝐀𝐌 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐀𝐍𝐈𝐌𝐀𝐓𝐄𝐃 𝐄𝐌𝐎𝐉𝐈𝐒

📊 𝐒𝐓𝐀𝐓𝐈𝐒𝐓𝐈𝐂𝐒:
• 𝐓𝐎𝐓𝐀𝐋 𝐔𝐒𝐄𝐑𝐒: {total}
• 𝐄𝐌𝐎𝐉𝐈 𝐏𝐎𝐎𝐋: {len(ALL_PREMIUM_EMOJIS)}
• 𝐅𝐋𝐀𝐆𝐒: {len(FLAG_MAPPING)}
• 𝐕𝐄𝐑𝐒𝐈𝐎𝐍: 7.0

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""
    _send_pe(message.chat.id, text, reply_markup=kb)

@bot.message_handler(func=lambda m: button_matches(m.text, "𝐒𝐓𝐀𝐓𝐒", "𝐁𝐎𝐓 𝐒𝐓𝐀𝐓𝐒"))
def stats_msg(message):
    uid = message.from_user.id
    kb = get_menu(uid)
    total = len(all_users)
    status = "🟢 𝐎𝐍𝐋𝐈𝐍𝐄" if bot_active else "🔴 𝐎𝐅𝐅𝐋𝐈𝐍𝐄"
    
    text = f"""
{PLACEHOLDER}═══《 📊 𝐒𝐓𝐀𝐓𝐈𝐒𝐓𝐈𝐂𝐒 》═══{PLACEHOLDER}

𝐁𝐎𝐓 𝐒𝐓𝐀𝐓𝐔𝐒: {status}
𝐓𝐎𝐓𝐀𝐋 𝐔𝐒𝐄𝐑𝐒: {total}
𝐄𝐌𝐎𝐉𝐈 𝐏𝐎𝐎𝐋: {len(ALL_PREMIUM_EMOJIS)}
𝐅𝐋𝐀𝐆𝐒: {len(FLAG_MAPPING)}

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""
    _send_pe(message.chat.id, text, reply_markup=kb)

# ============================================================
# MAKE POST HANDLERS
# ============================================================
@bot.message_handler(func=lambda m: button_matches(m.text, "𝐌𝐀𝐊𝐄 𝐏𝐎𝐒𝐓"))
def start_post(message):
    uid = message.from_user.id
    register_user(uid)
    
    if not bot_active and not is_admin(uid):
        text = f"{PLACEHOLDER} 𝐁𝐎𝐓 𝐈𝐒 𝐎𝐅𝐅𝐋𝐈𝐍𝐄."
        _send_pe(message.chat.id, text)
        return
    
    temp_data[uid] = {
        "original_text": "",
        "original_entities": [],
        "media_type": None,
        "media_id": None,
        "media_name": None,
        "buttons": [],
        "refresh_count": 0,
        "button_count": 0,
        "current_button": 0,
        "processed_text": "",
        "processed_entities": [],
        "preview_msg_id": None,
        "action_msg_id": None,
    }
    
    text = f"""
{PLACEHOLDER}═══《 ✍️ 𝐂𝐑𝐄𝐀𝐓𝐄 𝐏𝐎𝐒𝐓 》═══{PLACEHOLDER}

𝐏𝐋𝐄𝐀𝐒𝐄 𝐒𝐄𝐍𝐃 𝐘𝐎𝐔𝐑 𝐓𝐄𝐗𝐓 𝐌𝐄𝐒𝐒𝐀𝐆𝐄 𝐍𝐎𝐖.

𝐒𝐔𝐏𝐏𝐎𝐑𝐓𝐒: 𝐁𝐎𝐋𝐃, 𝐈𝐓𝐀𝐋𝐈𝐂, 𝐋𝐈𝐍𝐊𝐒
🏳️ 𝐅𝐋𝐀𝐆𝐒 & 𝐄𝐌𝐎𝐉𝐈𝐒 𝐖𝐈𝐋𝐋 𝐁𝐄 𝐂𝐎𝐍𝐕𝐄𝐑𝐓𝐄𝐃!

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""
    sent = _send_pe_return(message.chat.id, text)
    bot.register_next_step_handler(sent, process_post_text)

def process_post_text(message):
    uid = message.from_user.id
    
    if message.text and message.text.strip() == "/cancel":
        kb = get_menu(uid)
        _send_pe(message.chat.id, f"{PLACEHOLDER} 𝐂𝐀𝐍𝐂𝐄𝐋𝐄𝐃!", reply_markup=kb)
        temp_data.pop(uid, None)
        return
    
    if uid not in temp_data:
        _send_pe(message.chat.id, f"{PLACEHOLDER} 𝐒𝐄𝐒𝐒𝐈𝐎𝐍 𝐄𝐗𝐏𝐈𝐑𝐄𝐃! 𝐏𝐋𝐄𝐀𝐒𝐄 /𝐒𝐓𝐀𝐑𝐓 𝐀𝐆𝐀𝐈𝐍.")
        return
    
    temp_data[uid]["original_text"] = message.text or ""
    temp_data[uid]["original_entities"] = message.entities or []
    
    ask_media_type(message.chat.id, uid)

def ask_media_type(chat_id: int, uid: int):
    text = f"""
{PLACEHOLDER}═══《 {PLACEHOLDER} 𝐀𝐃𝐃 𝐌𝐄𝐃𝐈𝐀 》═══{PLACEHOLDER}

𝐃𝐎 𝐘𝐎𝐔 𝐖𝐀𝐍𝐓 𝐓𝐎 𝐀𝐃𝐃 𝐌𝐄𝐃𝐈𝐀?

{PLACEHOLDER}═══════════════════{PLACEHOLDER}
"""
    keyboard = [
        make_styled_row([
            {"text": "𝐕𝐈𝐃𝐄𝐎", "style": "primary", "callback_data": f"media_video_{uid}"},
            {"text": "𝐈𝐌𝐀𝐆𝐄", "style": "primary", "callback_data": f"media_image_{uid}"},
        ]),
        make_styled_row([
            {"text": "𝐃𝐎𝐂𝐔𝐌𝐄𝐍𝐓", "style": "primary", "callback_data": f"media_doc_{uid}"},
            {"text": "𝐒𝐊𝐈𝐏", "style": "danger", "callback_data": f"media_skip_{uid}"},
        ]),
    ]
    markup = InlineKeyboardMarkup(keyboard)
    _send_pe(chat_id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("media_"))
def handle_media_selection(call):
    parts = call.data.split("_")
    action = parts[1]
    uid = int(parts[2]) if len(parts) > 2 else call.from_user.id
    chat_id = call.message.chat.id
    
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass
    
    if uid not in temp_data:
        bot.answer_callback_query(call.id, "Session expired!")
        return
    
    if action == "skip":
        temp_data[uid]["media_type"] = None
        ask_button_amount(chat_id, uid)
    
    elif action in ["video", "image", "doc"]:
        temp_data[uid]["media_type"] = action
        media_text = {"video": "𝐕𝐈𝐃𝐄𝐎", "image": "𝐈𝐌𝐀𝐆𝐄", "doc": "𝐃𝐎𝐂𝐔𝐌𝐄𝐍𝐓"}[action]
        
        text = f"""
{PLACEHOLDER}═══《 📤 𝐒𝐄𝐍𝐃 {media_text} 》═══{PLACEHOLDER}

𝐏𝐋𝐄𝐀𝐒𝐄 𝐒𝐄𝐍𝐃 𝐘𝐎𝐔𝐑 {media_text} 𝐍𝐎𝐖.

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""
        
        sent = _send_pe_return(chat_id, text)
        bot.register_next_step_handler(sent, receive_media, action)
    
    bot.answer_callback_query(call.id)

def receive_media(message, media_type):
    uid = message.from_user.id
    
    if message.text and message.text.strip() == "/cancel":
        kb = get_menu(uid)
        _send_pe(message.chat.id, f"{PLACEHOLDER} 𝐂𝐀𝐍𝐂𝐄𝐋𝐄𝐃!", reply_markup=kb)
        temp_data.pop(uid, None)
        return
    
    if uid not in temp_data:
        _send_pe(message.chat.id, f"{PLACEHOLDER} 𝐒𝐄𝐒𝐒𝐈𝐎𝐍 𝐄𝐗𝐏𝐈𝐑𝐄𝐃!")
        return
    
    if media_type == "video" and message.video:
        temp_data[uid]["media_id"] = message.video.file_id
        if message.caption:
            temp_data[uid]["original_text"] = message.caption
            temp_data[uid]["original_entities"] = message.caption_entities or []
    elif media_type == "image" and message.photo:
        temp_data[uid]["media_id"] = message.photo[-1].file_id
        if message.caption:
            temp_data[uid]["original_text"] = message.caption
            temp_data[uid]["original_entities"] = message.caption_entities or []
    elif media_type == "doc" and message.document:
        temp_data[uid]["media_id"] = message.document.file_id
        if message.caption:
            temp_data[uid]["original_text"] = message.caption
            temp_data[uid]["original_entities"] = message.caption_entities or []
    else:
        text = f"{PLACEHOLDER} 𝐏𝐋𝐄𝐀𝐒𝐄 𝐒𝐄𝐍𝐃 𝐀 𝐕𝐀𝐋𝐈𝐃 {media_type.upper()}!"
        sent = _send_pe_return(message.chat.id, text)
        bot.register_next_step_handler(sent, receive_media, media_type)
        return
    
    ask_button_amount(message.chat.id, uid)

def ask_button_amount(chat_id: int, uid: int):
    text = f"""
{PLACEHOLDER}═══《 🔘 𝐀𝐃𝐃 𝐁𝐔𝐓𝐓𝐎𝐍𝐒 》═══{PLACEHOLDER}

𝐃𝐎 𝐘𝐎𝐔 𝐖𝐀𝐍𝐓 𝐓𝐎 𝐀𝐃𝐃 𝐈𝐍𝐋𝐈𝐍𝐄 𝐁𝐔𝐓𝐓𝐎𝐍𝐒?

𝐒𝐄𝐋𝐄𝐂𝐓 𝐇𝐎𝐖 𝐌𝐀𝐍𝐘:

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""
    keyboard = [
        make_styled_row([
            {"text": "𝟏", "callback_data": f"btn_amt_1_{uid}"},
            {"text": "𝟐", "callback_data": f"btn_amt_2_{uid}"},
        ]),
        make_styled_row([
            {"text": "𝟑", "callback_data": f"btn_amt_3_{uid}"},
            {"text": "𝟒", "callback_data": f"btn_amt_4_{uid}"},
        ]),
        [make_button_with_icon(text="𝐍𝐎 𝐁𝐔𝐓𝐓𝐎𝐍𝐒", style="danger", callback_data=f"btn_amt_0_{uid}")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    _send_pe(chat_id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("btn_amt_"))
def handle_button_amount(call):
    parts = call.data.split("_")
    amount = int(parts[2])
    uid = int(parts[3]) if len(parts) > 3 else call.from_user.id
    chat_id = call.message.chat.id
    
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass
    
    if uid not in temp_data:
        bot.answer_callback_query(call.id, "Session expired!")
        return
    
    if amount == 0:
        temp_data[uid]["button_count"] = 0
        temp_data[uid]["buttons"] = []
        create_preview(chat_id, uid)
    else:
        temp_data[uid]["button_count"] = amount
        temp_data[uid]["buttons"] = []
        temp_data[uid]["current_button"] = 1
        ask_button_name(chat_id, uid)
    
    bot.answer_callback_query(call.id)

def ask_button_name(chat_id, uid):
    current = temp_data[uid]["current_button"]
    total = temp_data[uid]["button_count"]
    
    text = f"""
{PLACEHOLDER}═══《 🔘 𝐁𝐔𝐓𝐓𝐎𝐍 {current}/{total} - 𝐍𝐀𝐌𝐄 》═══{PLACEHOLDER}

𝐄𝐍𝐓𝐄𝐑 𝐓𝐇𝐄 𝐁𝐔𝐓𝐓𝐎𝐍 𝐍𝐀𝐌𝐄/𝐋𝐀𝐁𝐄𝐋
(𝐘𝐎𝐔 𝐂𝐀𝐍 𝐔𝐒𝐄 𝐄𝐌𝐎𝐉𝐈𝐒)

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""
    sent = _send_pe_return(chat_id, text)
    bot.register_next_step_handler(sent, save_button_name)

def save_button_name(message):
    uid = message.from_user.id
    chat_id = message.chat.id
    
    if message.text and message.text.strip() == "/cancel":
        kb = get_menu(uid)
        _send_pe(chat_id, f"{PLACEHOLDER} 𝐂𝐀𝐍𝐂𝐄𝐋𝐄𝐃!", reply_markup=kb)
        temp_data.pop(uid, None)
        return
    
    if uid not in temp_data:
        _send_pe(chat_id, f"{PLACEHOLDER} 𝐒𝐄𝐒𝐒𝐈𝐎𝐍 𝐄𝐗𝐏𝐈𝐑𝐄𝐃!")
        return
    
    button_name = (message.text or "").strip()[:30]
    if not button_name:
        text = f"{PLACEHOLDER} 𝐁𝐔𝐓𝐓𝐎𝐍 𝐍𝐀𝐌𝐄 𝐂𝐀𝐍𝐍𝐎𝐓 𝐁𝐄 𝐄𝐌𝐏𝐓𝐘! 𝐓𝐑𝐘 𝐀𝐆𝐀𝐈𝐍:"
        sent = _send_pe_return(chat_id, text)
        bot.register_next_step_handler(sent, save_button_name)
        return
    
    temp_data[uid]["buttons"].append({"name": button_name, "url": "", "color": None})
    ask_button_url(chat_id, uid)

def ask_button_url(chat_id, uid):
    current = temp_data[uid]["current_button"]
    total = temp_data[uid]["button_count"]
    
    text = f"""
{PLACEHOLDER}═══《 🔗 𝐁𝐔𝐓𝐓𝐎𝐍 {current}/{total} - 𝐔𝐑𝐋 》═══{PLACEHOLDER}

𝐄𝐍𝐓𝐄𝐑 𝐓𝐇𝐄 𝐁𝐔𝐓𝐓𝐎𝐍 𝐔𝐑𝐋/𝐋𝐈𝐍𝐊
(𝐌𝐔𝐒𝐓 𝐒𝐓𝐀𝐑𝐓 𝐖𝐈𝐓𝐇 https://)

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""
    sent = _send_pe_return(chat_id, text)
    bot.register_next_step_handler(sent, save_button_url)

def save_button_url(message):
    uid = message.from_user.id
    chat_id = message.chat.id
    
    if message.text and message.text.strip() == "/cancel":
        kb = get_menu(uid)
        _send_pe(chat_id, f"{PLACEHOLDER} 𝐂𝐀𝐍𝐂𝐄𝐋𝐄𝐃!", reply_markup=kb)
        temp_data.pop(uid, None)
        return
    
    if uid not in temp_data:
        _send_pe(chat_id, f"{PLACEHOLDER} 𝐒𝐄𝐒𝐒𝐈𝐎𝐍 𝐄𝐗𝐏𝐈𝐑𝐄𝐃!")
        return
    
    url = (message.text or "").strip()
    valid_prefixes = ("http://", "https://", "tg://")
    if not any(url.startswith(p) for p in valid_prefixes):
        text = f"{PLACEHOLDER} 𝐈𝐍𝐕𝐀𝐋𝐈𝐃 𝐔𝐑𝐋! 𝐓𝐑𝐘 𝐀𝐆𝐀𝐈𝐍:"
        sent = _send_pe_return(chat_id, text)
        bot.register_next_step_handler(sent, save_button_url)
        return
    
    idx = temp_data[uid]["current_button"] - 1
    temp_data[uid]["buttons"][idx]["url"] = url
    
    ask_button_color(chat_id, uid)

def ask_button_color(chat_id, uid):
    current = temp_data[uid]["current_button"]
    total = temp_data[uid]["button_count"]
    
    text = f"""
{PLACEHOLDER}═══《 🎨 𝐁𝐔𝐓𝐓𝐎𝐍 {current}/{total} - 𝐂𝐎𝐋𝐎𝐑 》═══{PLACEHOLDER}

𝐒𝐄𝐋𝐄𝐂𝐓 𝐓𝐇𝐄 𝐁𝐔𝐓𝐓𝐎𝐍 𝐂𝐎𝐋𝐎𝐑:

🔵 𝐏𝐑𝐈𝐌𝐀𝐑𝐘 - 𝐁𝐋𝐔𝐄
🔴 𝐃𝐀𝐍𝐆𝐄𝐑 - 𝐑𝐄𝐃
🟢 𝐒𝐔𝐂𝐂𝐄𝐒𝐒 - 𝐆𝐑𝐄𝐄𝐍
⚪ 𝐃𝐄𝐅𝐀𝐔𝐋𝐓 - 𝐆𝐑𝐀𝐘/𝐖𝐇𝐈𝐓𝐄

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        make_button_with_icon(text="𝐏𝐑𝐈𝐌𝐀𝐑𝐘", style="primary", callback_data=f"btn_color_primary_{uid}"),
        make_button_with_icon(text="𝐃𝐀𝐍𝐆𝐄𝐑", style="danger", callback_data=f"btn_color_danger_{uid}"),
        make_button_with_icon(text="𝐒𝐔𝐂𝐂𝐄𝐒𝐒", style="success", callback_data=f"btn_color_success_{uid}"),
        make_button_with_icon(text="𝐃𝐄𝐅𝐀𝐔𝐋𝐓", callback_data=f"btn_color_default_{uid}"),
    )
    
    _send_pe(chat_id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("btn_color_"))
def handle_button_color(call):
    parts = call.data.split("_")
    color = parts[2]
    uid = int(parts[3]) if len(parts) > 3 else call.from_user.id
    chat_id = call.message.chat.id
    
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass
    
    if uid not in temp_data:
        bot.answer_callback_query(call.id, "Session expired!")
        return
    
    idx = temp_data[uid]["current_button"] - 1
    temp_data[uid]["buttons"][idx]["color"] = color if color != "default" else None
    
    color_name = color.upper()
    if color == "primary":
        color_display = "🔵 𝐏𝐑𝐈𝐌𝐀𝐑𝐘 (𝐁𝐋𝐔𝐄)"
    elif color == "danger":
        color_display = "🔴 𝐃𝐀𝐍𝐆𝐄𝐑 (𝐑𝐄𝐃)"
    elif color == "success":
        color_display = "🟢 𝐒𝐔𝐂𝐂𝐄𝐒𝐒 (𝐆𝐑𝐄𝐄𝐍)"
    else:
        color_display = "⚪ 𝐃𝐄𝐅𝐀𝐔𝐋𝐓 (𝐆𝐑𝐀𝐘)"
    
    bot.answer_callback_query(call.id, f"Button color set to {color_display}!")
    
    if temp_data[uid]["current_button"] < temp_data[uid]["button_count"]:
        temp_data[uid]["current_button"] += 1
        ask_button_name(chat_id, uid)
    else:
        create_preview(chat_id, uid)

def create_preview(chat_id, uid):
    data = temp_data.get(uid)
    if not data:
        return
    
    processed_text, processed_entities = process_text_and_entities(
        data["original_text"],
        data["original_entities"]
    )
    data["processed_text"] = processed_text
    data["processed_entities"] = processed_entities
    
    reply_markup = None
    if data["buttons"]:
        keyboard = []
        for btn in data["buttons"]:
            style = btn.get("color")
            keyboard.append([make_button(
                text=btn["name"],
                style=style,
                url=btn["url"]
            )])
        reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        if data["media_type"] == "image" and data.get("media_id"):
            preview = bot.send_photo(chat_id, data["media_id"], caption=processed_text or None, caption_entities=processed_entities or None, reply_markup=reply_markup)
        elif data["media_type"] == "video" and data.get("media_id"):
            preview = bot.send_video(chat_id, data["media_id"], caption=processed_text or None, caption_entities=processed_entities or None, reply_markup=reply_markup)
        elif data["media_type"] == "doc" and data.get("media_id"):
            preview = bot.send_document(chat_id, data["media_id"], caption=processed_text or None, caption_entities=processed_entities or None, reply_markup=reply_markup)
        else:
            preview = bot.send_message(chat_id, processed_text if processed_text else f"{PLACEHOLDER} 𝐘𝐨𝐮𝐫 𝐩𝐨𝐬𝐭", entities=processed_entities or None, reply_markup=reply_markup)
        
        data["preview_msg_id"] = preview.message_id
        
    except Exception as e:
        _send_pe(chat_id, f"{PLACEHOLDER} ❌ 𝐄𝐫𝐫𝐨𝐫: {e}")
        return
    
    action_keyboard = [
        make_styled_row([
            {"text": "𝐑𝐄𝐅𝐑𝐄𝐒𝐇", "style": "primary", "callback_data": f"refresh_{uid}"},
            {"text": "𝐃𝐄𝐋𝐄𝐓𝐄", "style": "danger", "callback_data": f"delete_{uid}"},
        ]),
        make_styled_row([
            {"text": "𝐃𝐎𝐍𝐄", "style": "success", "callback_data": f"done_{uid}"},
            {"text": "𝐅𝐎𝐑𝐖𝐀𝐑𝐃", "style": "primary", "callback_data": f"forward_{uid}"},
        ]),
    ]
    action_markup = InlineKeyboardMarkup(action_keyboard)
    
    action_text = f"""
{PLACEHOLDER}═══《 ✨ 𝐏𝐑𝐄𝐕𝐈𝐄𝐖 𝐑𝐄𝐀𝐃𝐘 》═══{PLACEHOLDER}

𝐘𝐨𝐮𝐫 𝐩𝐨𝐬𝐭 𝐢𝐬 𝐫𝐞𝐚𝐝𝐲!

{PLACEHOLDER} 𝐑𝐄𝐅𝐑𝐄𝐒𝐇 - 𝐍𝐞𝐰 𝐞𝐦𝐨𝐣𝐢𝐬
{PLACEHOLDER} 𝐃𝐄𝐋𝐄𝐓𝐄 - 𝐑𝐞𝐦𝐨𝐯𝐞 𝐩𝐫𝐞𝐯𝐢𝐞𝐰
{PLACEHOLDER} 𝐃𝐎𝐍𝐄 - 𝐅𝐢𝐧𝐢𝐬𝐡
{PLACEHOLDER} 𝐅𝐎𝐑𝐖𝐀𝐑𝐃 - 𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭 𝐰𝐢𝐭𝐡 𝐛𝐮𝐭𝐭𝐨𝐧𝐬

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""
    
    entities = _build_pe_entities(action_text)
    action_msg = bot.send_message(chat_id, action_text, entities=entities, reply_markup=action_markup, parse_mode=None)
    data["action_msg_id"] = action_msg.message_id
    temp_data[uid] = data

@bot.callback_query_handler(func=lambda c: c.data.startswith(("refresh_", "delete_", "done_", "forward_")))
def handle_preview_actions(call):
    parts = call.data.split("_")
    action = parts[0]
    uid = int(parts[1]) if len(parts) > 1 else call.from_user.id
    chat_id = call.message.chat.id

    if uid not in temp_data:
        bot.answer_callback_query(call.id, "Session expired!")
        return

    data = temp_data[uid]

    if action == "refresh":
        bot.answer_callback_query(call.id, "🔄 Refreshing emojis...")
        if data.get("preview_msg_id"):
            try: bot.delete_message(chat_id, data["preview_msg_id"])
            except: pass
        if data.get("action_msg_id"):
            try: bot.delete_message(chat_id, data["action_msg_id"])
            except: pass
        processed_text, processed_entities = process_text_and_entities(data["original_text"], data["original_entities"])
        data["processed_text"] = processed_text
        data["processed_entities"] = processed_entities
        create_preview(chat_id, uid)

    elif action == "delete":
        bot.answer_callback_query(call.id, "Deleted!")
        if data.get("preview_msg_id"):
            try: bot.delete_message(chat_id, data["preview_msg_id"])
            except: pass
        if data.get("action_msg_id"):
            try: bot.delete_message(chat_id, data["action_msg_id"])
            except: pass
        temp_data.pop(uid, None)

    elif action == "done":
        bot.answer_callback_query(call.id, "Post created!")
        if data.get("action_msg_id"):
            try: bot.delete_message(chat_id, data["action_msg_id"])
            except: pass
        temp_data.pop(uid, None)
        kb = get_menu(uid)
        text = f"""
{PLACEHOLDER}═══《 ✅ 𝐏𝐎𝐒𝐓 𝐂𝐑𝐄𝐀𝐓𝐄𝐃! 》═══{PLACEHOLDER}

𝐘𝐨𝐮𝐫 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐞𝐦𝐨𝐣𝐢 𝐩𝐨𝐬𝐭 𝐢𝐬 𝐫𝐞𝐚𝐝𝐲!

𝐓𝐚𝐩 𝐌𝐀𝐊𝐄 𝐏𝐎𝐒𝐓 𝐭𝐨 𝐜𝐫𝐞𝐚𝐭𝐞 𝐚𝐧𝐨𝐭𝐡𝐞𝐫

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""
        _send_pe(chat_id, text, reply_markup=kb)

    elif action == "forward":
        preview_msg_id = data.get("preview_msg_id")
        if not preview_msg_id:
            bot.answer_callback_query(call.id, "No preview to forward!", show_alert=True)
            return
        bot.answer_callback_query(call.id, "📤 Broadcasting with buttons...")

        reply_markup = None
        if data.get("buttons"):
            keyboard = []
            for btn in data["buttons"]:
                style = btn.get("color")
                keyboard.append([make_button(text=btn["name"], style=style, url=btn["url"])])
            reply_markup = InlineKeyboardMarkup(keyboard)

        success = 0
        failed = 0
        total = len(all_users)

        status_text = f"{PLACEHOLDER} 📢 𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭𝐢𝐧𝐠 𝐭𝐨 {total} 𝐮𝐬𝐞𝐫𝐬..."
        status_msg = bot.send_message(chat_id, status_text)

        processed_text = data.get("processed_text", "")
        processed_entities = data.get("processed_entities", [])
        media_type = data.get("media_type")
        media_id = data.get("media_id")

        for target_uid in list(all_users):
            try:
                if media_type == "image" and media_id:
                    bot.send_photo(target_uid, media_id, caption=processed_text or None,
                                   caption_entities=processed_entities or None, reply_markup=reply_markup)
                elif media_type == "video" and media_id:
                    bot.send_video(target_uid, media_id, caption=processed_text or None,
                                   caption_entities=processed_entities or None, reply_markup=reply_markup)
                elif media_type == "doc" and media_id:
                    bot.send_document(target_uid, media_id, caption=processed_text or None,
                                      caption_entities=processed_entities or None, reply_markup=reply_markup)
                else:
                    bot.send_message(target_uid, processed_text if processed_text else f"{PLACEHOLDER} 𝐏𝐨𝐬𝐭",
                                     entities=processed_entities or None, reply_markup=reply_markup, parse_mode=None)
                success += 1
                time.sleep(0.05)
            except Exception:
                failed += 1

        try: bot.delete_message(chat_id, status_msg.message_id)
        except: pass

        result_text = f"""
{PLACEHOLDER}═══《 ✅ 𝐁𝐑𝐎𝐀𝐃𝐂𝐀𝐒𝐓 𝐃𝐎𝐍𝐄! 》═══{PLACEHOLDER}

𝐒𝐔𝐂𝐂𝐄𝐒𝐒: {success} ✅
𝐅𝐀𝐈𝐋𝐄𝐃: {failed} ❌
𝐁𝐔𝐓𝐓𝐎𝐍𝐒: 𝐈𝐍𝐂𝐋𝐔𝐃𝐄𝐃 ✅

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""
        _send_pe(chat_id, result_text, reply_markup=get_menu(uid))

@bot.callback_query_handler(func=lambda c: c.data == "check_join")
def handle_check_join(call):
    uid = call.from_user.id
    chat_id = call.message.chat.id
    
    not_joined = check_joined(uid)
    
    if not_joined:
        try: bot.delete_message(chat_id, call.message.message_id)
        except: pass
        send_join_notice(chat_id, not_joined)
    else:
        try: bot.delete_message(chat_id, call.message.message_id)
        except: pass
        register_user(uid)
        name = call.from_user.first_name or "Friend"
        kb = get_menu(uid)
        text = send_welcome_message(name, uid)
        _send_pe(chat_id, text, reply_markup=kb)
    
    bot.answer_callback_query(call.id)

# ============================================================
# ADMIN COMMANDS - UPDATED WITH EMOJI SUPPORT
# ============================================================
@bot.message_handler(func=lambda m: button_matches(m.text, "𝐁𝐎𝐓 𝐎𝐅𝐅") and is_admin(m.from_user.id))
def bot_off(message):
    global bot_active
    bot_active = False
    text = f"""
{PLACEHOLDER}═══《 🔴 𝐁𝐎𝐓 𝐎𝐅𝐅𝐋𝐈𝐍𝐄 》═══{PLACEHOLDER}

𝐁𝐎𝐓 𝐈𝐒 𝐍𝐎𝐖 𝐎𝐅𝐅𝐋𝐈𝐍𝐄.

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""
    _send_pe(message.chat.id, text, reply_markup=get_menu(message.from_user.id))

@bot.message_handler(func=lambda m: button_matches(m.text, "𝐁𝐎𝐓 𝐎𝐍") and is_admin(m.from_user.id))
def bot_on(message):
    global bot_active
    bot_active = True
    text = f"""
{PLACEHOLDER}═══《 🟢 𝐁𝐎𝐓 𝐎𝐍𝐋𝐈𝐍𝐄 》═══{PLACEHOLDER}

𝐁𝐎𝐓 𝐈𝐒 𝐍𝐎𝐖 𝐎𝐍𝐋𝐈𝐍𝐄!

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""
    _send_pe(message.chat.id, text, reply_markup=get_menu(message.from_user.id))

@bot.message_handler(func=lambda m: button_matches(m.text, "𝐔𝐒𝐄𝐑𝐒 𝐋𝐈𝐒𝐓") and is_admin(m.from_user.id))
def users_list(message):
    total = len(all_users)
    user_list = list(all_users)
    
    text = f"""
{PLACEHOLDER}═══《 👥 𝐑𝐄𝐆𝐈𝐒𝐓𝐄𝐑𝐄𝐃 𝐔𝐒𝐄𝐑𝐒 》═══{PLACEHOLDER}

𝐓𝐎𝐓𝐀𝐋: {total} 𝐔𝐒𝐄𝐑𝐒

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""
    _send_pe(message.chat.id, text, reply_markup=get_menu(message.from_user.id))
    
    if user_list:
        for i in range(0, len(user_list), 50):
            batch = user_list[i:i+50]
            batch_text = "\n".join([f"• {uid}" for uid in batch])
            bot.send_message(message.chat.id, batch_text)

@bot.message_handler(func=lambda m: button_matches(m.text, "𝐁𝐑𝐎𝐀𝐃𝐂𝐀𝐒𝐓") and is_admin(m.from_user.id))
def broadcast_start(message):
    text = f"""
{PLACEHOLDER}═══《 📢 𝐁𝐑𝐎𝐀𝐃𝐂𝐀𝐒𝐓 》═══{PLACEHOLDER}

𝐒𝐄𝐍𝐃 𝐘𝐎𝐔𝐑 𝐌𝐄𝐒𝐒𝐀𝐆𝐄 𝐍𝐎𝐖.

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""
    sent = _send_pe_return(message.chat.id, text)
    bot.register_next_step_handler(sent, do_broadcast)

def do_broadcast(message):
    if message.text and message.text.strip() == "/cancel":
        _send_pe(message.chat.id, f"{PLACEHOLDER} 𝐂𝐀𝐍𝐂𝐄𝐋𝐄𝐃!", reply_markup=get_menu(message.from_user.id))
        return
    
    success = 0
    failed = 0
    total = len(all_users)
    status_msg = bot.send_message(message.chat.id, f"📢 Broadcasting to {total} users...")
    
    for uid in list(all_users):
        try:
            bot.copy_message(uid, message.chat.id, message.message_id)
            success += 1
            time.sleep(0.05)
        except Exception:
            failed += 1
    
    try:
        bot.delete_message(message.chat.id, status_msg.message_id)
    except:
        pass
    
    text = f"""
{PLACEHOLDER}═══《 ✅ 𝐁𝐑𝐎𝐀𝐃𝐂𝐀𝐒𝐓 𝐃𝐎𝐍𝐄! 》═══{PLACEHOLDER}

𝐒𝐔𝐂𝐂𝐄𝐒𝐒: {success} ✅
𝐅𝐀𝐈𝐋𝐄𝐃: {failed} ❌

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""
    _send_pe(message.chat.id, text, reply_markup=get_menu(message.from_user.id))

@bot.message_handler(commands=["cancel"])
def cancel_step(message):
    uid = message.from_user.id
    temp_data.pop(uid, None)
    kb = get_menu(uid)
    _send_pe(message.chat.id, f"{PLACEHOLDER} 𝐂𝐀𝐍𝐂𝐄𝐋𝐄𝐃!", reply_markup=kb)

# ============================================================
# DEMO COMMAND
# ============================================================
@bot.message_handler(commands=["buttons"])
def demo_buttons(message):
    text = f"""
{PLACEHOLDER}═══《 🎨 𝐁𝐔𝐓𝐓𝐎𝐍 𝐒𝐓𝐘𝐋𝐄𝐒 𝐃𝐄𝐌𝐎 》═══{PLACEHOLDER}

🔵 𝐩𝐫𝐢𝐦𝐚𝐫𝐲 = 𝐁𝐋𝐔𝐄
🔴 𝐝𝐚𝐧𝐠𝐞𝐫 = 𝐑𝐄𝐃
🟢 𝐬𝐮𝐜𝐜𝐞𝐬𝐬 = 𝐆𝐑𝐄𝐄𝐍
⚪ 𝐝𝐞𝐟𝐚𝐮𝐥𝐭 = 𝐆𝐑𝐀𝐘/𝐖𝐇𝐈𝐓𝐄

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""
    keyboard = [
        [
            make_button_with_icon(text="𝐏𝐑𝐈𝐌𝐀𝐑𝐘", style="primary", callback_data="demo_primary"),
            make_button_with_icon(text="𝐃𝐀𝐍𝐆𝐄𝐑", style="danger", callback_data="demo_danger"),
        ],
        [
            make_button_with_icon(text="𝐒𝐔𝐂𝐂𝐄𝐒𝐒", style="success", callback_data="demo_success"),
            make_button_with_icon(text="𝐃𝐄𝐅𝐀𝐔𝐋𝐓", callback_data="demo_default"),
        ],
        [
            make_button_with_icon(text="Google", style="primary", url="https://google.com"),
            make_button_with_icon(text="YouTube", style="danger", url="https://youtube.com"),
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    _send_pe(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("demo_"))
def handle_demo_buttons(call):
    style_name = call.data.replace("demo_", "").upper()
    bot.answer_callback_query(call.id, f"You pressed the {style_name} style button!")

@bot.message_handler(func=lambda m: True)
def fallback(message):
    uid = message.from_user.id
    
    if not is_admin(uid):
        not_joined = check_joined(uid)
        if not_joined:
            send_join_notice(message.chat.id, not_joined)
            return
    
    register_user(uid)
    
    if not bot_active and not is_admin(uid):
        text = f"{PLACEHOLDER} 𝐁𝐎𝐓 𝐈𝐒 𝐎𝐅𝐅𝐋𝐈𝐍𝐄."
        _send_pe(message.chat.id, text)
        return
    
    kb = get_menu(uid)
    text = f"""
{PLACEHOLDER}═══《 {PLACEHOLDER} 𝐌𝐄𝐍𝐔 》═══{PLACEHOLDER}

𝐏𝐋𝐄𝐀𝐒𝐄 𝐂𝐇𝐎𝐎𝐒𝐄 𝐅𝐑𝐎𝐌 𝐓𝐇𝐄 𝐌𝐄𝐍𝐔:

🌿 𝐌𝐀𝐊𝐄 𝐏𝐎𝐒𝐓
🍂 𝐇𝐄𝐋𝐏
🍀 𝐀𝐁𝐎𝐔𝐓 𝐁𝐎𝐓
🪾 𝐒𝐓𝐀𝐓𝐒

{PLACEHOLDER}═════════════════════{PLACEHOLDER}
"""
    _send_pe(message.chat.id, text, reply_markup=kb)

if __name__ == "__main__":
    print("=" * 60)
    print("🔥 PREMIUM EMOJI BOT v7.0 STARTED 🔥")
    print("=" * 60)
    print(f"🤖 Bot Token: {TOKEN[:15]}...")
    print(f"👥 Admins: {ADMIN_IDS}")
    print(f"📦 Primary Emojis: {len(PRIMARY_EMOJIS)}")
    print(f"📦 Total Premium Emojis: {len(ALL_PREMIUM_EMOJIS)}")
    print(f"🏳️ Country Flags: {len(FLAG_MAPPING)}")
    print(f"🎨 Smart Emoji Mapping: ENABLED")
    print(f"🎨 Button Color Selection: ENABLED")
    print(f"📋 Menu: EMOJI BUTTONS ENABLED")
    print("=" * 60)
    
    bot.remove_webhook()
    time.sleep(1)
    bot.infinity_polling(timeout=30, long_polling_timeout=15)

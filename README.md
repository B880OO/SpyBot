# SpyBot

A Telegram bot that saves incoming messages (including media) and notifies when messages are **deleted** or **edited** by other users.

## 🚀 Features

- 🔔 Notifications for **deletions** and **edits** with message quotes
- 👤 Works through **Telegram Business Connection**
- 🛡️ Secure: No `eval/exec/subprocess` or auto-downloads. Network access limited to Telegram API and OpenRouter (for `.ai` commands)

## 🧰 Tech Stack

- Python 3.11+ (recommended 3.13)
- aiogram 3, SQLAlchemy 2 + asyncpg (PostgreSQL)
- pydantic-settings (ENV), colorlog
- (Optional) OpenRouter for `.ai` commands

## 📝 Commands

```
.trole     — sends trolling template
.love      — magical love animation
.1000-7    — sends anime pasta and changes avatar
.format    — fixes mixed keyboard layouts
.tr        — translator to Russian

.ai <text> — ask AI (via OpenRouter/Gemini)
.typing <delay>  — simulate "typing..." status
.node <delay>    — simulate "recording voice note" status
.voice <delay>   — simulate "recording voice message" status
```

> `<delay>` parameter is in seconds. Example: `.typing 5`

## ⚙️ Environment Variables

Copy `.env.example` to `.env` and configure:

```env
TOKEN=your_bot_token
DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST:5432/DBNAME
AI_KEY=openrouter_key_if_using_ai_commands
ADMINS=[123456789]  # list of admin Telegram IDs
```

## 🚀 Installation & Setup

### 🪟 Windows (PowerShell)

#### 1. Install Dependencies
- Install Python 3.11+ and [uv](https://docs.astral.sh/uv/)

#### 2. Setup Virtual Environment
```powershell
uv venv
.\.venv\Scripts\activate
uv sync
```

#### 3. Setup PostgreSQL
Install PostgreSQL for Windows (port 5432, user `postgres`). Create database:

```powershell
psql -U postgres -h localhost -p 5432 -c "CREATE DATABASE spybot;"
```

Update `.env` with your database URL:
```env
DATABASE_URL=postgresql+asyncpg://postgres:YOURPASS@localhost:5432/spybot
```

#### 4. Run the Bot
```powershell
cp .env.example .env
# Edit .env with your settings
uv run -m Bot
```

### 🐧 Linux/VPS (Ubuntu)

#### 1. System Dependencies
```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip postgresql postgresql-contrib
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 2. Database Setup
```bash
sudo -u postgres psql -c "CREATE USER spybot WITH PASSWORD 'strongpass';"
sudo -u postgres psql -c "CREATE DATABASE spybot OWNER spybot;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE spybot TO spybot;"
```

#### 3. Project Setup
```bash
git clone https://github.com/B880OO/SpyBot.git
cd SpyBot
uv venv
source .venv/bin/activate
uv sync
```

Configure environment:
```bash
cp .env.example .env
nano .env
# Set: DATABASE_URL=postgresql+asyncpg://spybot:strongpass@localhost:5432/spybot
```

#### 4. Run the Bot
```bash
uv run -m Bot
```

#### 5. Auto-start with systemd (Optional)
Create `/etc/systemd/system/spybot.service`:

```ini
[Unit]
Description=SpyBot Telegram Bot
After=network.target postgresql.service

[Service]
User=YOUR_USER
WorkingDirectory=/path/to/SpyBot
EnvironmentFile=/path/to/SpyBot/.env
ExecStart=/path/to/SpyBot/.venv/bin/python -m Bot
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now spybot
sudo journalctl -u spybot -f
```

## 🔌 Telegram Business Connection Setup

1. Enable Telegram Business in your account settings
2. Connect the bot to your business account
3. Send a message as your business profile - the bot will receive `business_connection_id` and start monitoring messages

## 🧪 Testing

- Send `/start` to register as a user
- Send test messages in business chat, try editing/deleting - bot will send notifications
- Check the `Messages` table in your database

## 🛠️ Troubleshooting

**Database Connection Issues:**
- `Could not parse SQLAlchemy URL`: Check `DATABASE_URL` format
- `Connection refused`: Verify PostgreSQL is running on port 5432
- `Authentication failed`: Check username/password in connection string

**Installation Issues:**
- `asyncpg wheel` fails: Update pip with `python -m pip install --upgrade pip`
- Translation issues: Consider replacing `googletrans` with `pygoogletranslation`

## ⚖️ Legal & Ethics

**Important:** This bot saves and analyzes messages, which may have legal and privacy implications. Ensure you:
- Have proper authorization to monitor messages
- Comply with local privacy laws (GDPR, etc.)
- Follow Telegram's Terms of Service
- Inform users when appropriate

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues or have questions:
- Open an [issue](https://github.com/B880OO/SpyBot/issues)
- Check existing issues for solutions

---

**⚠️ Disclaimer:** Use responsibly and in compliance with applicable laws and platform terms of service.

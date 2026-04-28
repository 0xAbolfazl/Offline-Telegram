offline-telegram/
├── .github/
│   └── workflows/
│       └── fetch.yml
├── dbs/
│   └── .gitkeep
├── .gitignore
├── requirements.txt
├── fetch_messages.py
├── crypto_utils.py
├── db.py
├── app.py
├── templates/
│   ├── index.html
│   └── chat.html
└── static/
    └── style.css



# Telegram Archive Bot / ربات آرشیو تلگرام

[English](#english) | [فارسی](#persian)

---

## English <a name="english"></a>

### Project Goal

This project is designed for environments where **Telegram is blocked**. It uses **GitHub Actions** to fetch text messages from a Telegram chat (group, channel, or user) every 12 hours, stores them in an **encrypted SQLite database**, and then commits that encrypted file directly into the repository. You can later view the messages through a **Flask web interface** that looks like Telegram.

### How It Works

1. GitHub Actions runs `fetch_messages.py` every 12 hours (or manually).
2. The script connects to Telegram using your API credentials (via `Telethon`).
3. It fetches the last 100 text messages from the specified chat.
4. Messages are saved into `messages.db` (SQLite).
5. The database is **encrypted** with AES (using `cryptography`) and saved as `messages.db.encrypted`.
6. The encrypted file is moved to the `dbs/` folder and **committed back to the repository**.
7. When you run `app.py` locally with the correct encryption key, it automatically decrypts the database and displays messages in a Telegram‑like UI.

### File Structure & Purpose

| File / Folder | Purpose |
|---------------|---------|
| `.github/workflows/fetch.yml` | GitHub Actions workflow – runs every 12 hours, calls `fetch_messages.py`, then commits the encrypted DB. |
| `fetch_messages.py` | Main script: connects to Telegram, fetches 100 messages, saves to `messages.db`, encrypts it, and produces `messages.db.encrypted`. |
| `db.py` | Handles SQLite database creation and queries (save chat, save message, retrieve messages). |
| `crypto_utils.py` | AES encryption/decryption functions using `cryptography`. |
| `app.py` | Flask web server. It copies the encrypted DB from `dbs/`, decrypts it (using key from `.env`), and starts the web UI. |
| `templates/index.html` | Shows the list of saved chats. |
| `templates/chat.html` | Shows messages of a selected chat with left/right bubbles (your messages in blue on the right). |
| `static/style.css` | Telegram‑like styling with responsive bubbles. |
| `requirements.txt` | Python dependencies: `flask`, `telethon`, `python-dotenv`, `cryptography`. |
| `dbs/` | Folder where the encrypted database (`messages.db.encrypted`) is stored and committed. |
| `.gitignore` | Excludes unencrypted DB, session files, `.env`, etc., but keeps `dbs/`. |

### Step‑by‑Step Setup

#### 1. Prerequisites on Your Local Machine
- Python 3.10 or higher
- Git

#### 2. Get Telegram API Credentials
- Visit [my.telegram.org](https://my.telegram.org/apps)
- Log in and create an application to get `API_ID` and `API_HASH`
- Also have your phone number (with country code) ready.

#### 3. Generate a Session String (optional but recommended)
On a machine where Telegram is accessible, run:
```python
from telethon import TelegramClient
client = TelegramClient('session', API_ID, API_HASH)
client.start(phone='+989123456789')
print(client.session.save())
Copy the output – this is your SESSION_STRING. It avoids re‑logging in every time.

4. Generate an Encryption Key
Run this script once locally:

python
import secrets, base64
key = secrets.token_bytes(32)
print(base64.b64encode(key).decode())
Save the output – this is your ENCRYPTION_KEY. Keep it secret!

5. Create GitHub Repository
Create a new private repository on GitHub (e.g., telegram-archive).

Clone it locally:

bash
git clone https://github.com/your-username/telegram-archive.git
cd telegram-archive
6. Add All Project Files
Create the folders and add all the files listed above (the complete code provided in the previous answers). Make sure you have:

.github/workflows/fetch.yml

fetch_messages.py, db.py, crypto_utils.py, app.py

templates/ with index.html, chat.html

static/style.css

requirements.txt, .gitignore

dbs/.gitkeep (empty file to keep the folder)

7. Set GitHub Secrets
Go to your repository → Settings → Secrets and variables → Actions → New repository secret. Add these:

Secret Name	Value
API_ID	Your numeric API ID
API_HASH	Your API hash string
PHONE	Your phone number (e.g., +989123456789)
SESSION_STRING	The session string (or leave empty)
CHAT_ID	Chat ID (numeric like -1001234567890 or username like @mygroup)
ENCRYPTION_KEY	The base64 key you generated
8. Push the Code
bash
git add .
git commit -m "Initial commit: Telegram archive bot"
git push origin main
9. Run the Workflow Manually (First Time)
Go to the Actions tab in your GitHub repo.

Select Fetch Telegram Messages → Run workflow.

Wait for it to finish. Check that the dbs/ folder now contains messages.db.encrypted (refresh the repo).

10. View Messages Locally
Pull the latest changes:

bash
git pull
Create a .env file in the project folder:

text
ENCRYPTION_KEY=your_base64_key_here
Install dependencies:

bash
pip install -r requirements.txt
Run the Flask app:

bash
python app.py
Open your browser at http://127.0.0.1:5000

You will see the list of chats. Click on a chat to view messages – your own messages appear in blue on the right, others in grey on the left.

Notes
The workflow runs automatically every 12 hours. You can also trigger it manually.

Only text messages are saved; images, files, and service messages are ignored.

The database is encrypted with AES‑CFB. Without the encryption key, even GitHub cannot read your messages.

Make your repository private for maximum security.

Troubleshooting
Error: ModuleNotFoundError – Run pip install -r requirements.txt.

Workflow fails because v3 of upload-artifact is deprecated – Already fixed in the provided YAML (uses v4).

Flask shows "Not Found" – Ensure templates/ and static/ folders exist and contain the correct files.

No messages appear – Check that CHAT_ID is correct and you are a member of that chat.

فارسی <a name="persian"></a>
هدف پروژه
این پروژه برای شرایطی طراحی شده که تلگرام فیلتر است. با استفاده از GitHub Actions، هر ۱۲ ساعت یکبار پیام‌های متنی یک چت تلگرام (گروه، کانال یا کاربر) را دریافت کرده، در یک دیتابیس SQLite رمزنگاری شده ذخیره می‌کند و فایل رمز شده را مستقیماً در ریپازیتوری گیت‌هاب commit می‌کند. سپس می‌توانید از طریق یک رابط وب Flask با ظاهری شبیه تلگرام، پیام‌ها را مشاهده کنید.

نحوه کار
GitHub Actions اسکریپت fetch_messages.py را هر ۱۲ ساعت (یا به صورت دستی) اجرا می‌کند.

اسکریپت با استفاده از اطلاعات API شما به تلگرام متصل می‌شود.

آخرین ۱۰۰ پیام متنی از چت مشخص شده را دریافت می‌کند.

پیام‌ها در فایل messages.db (SQLite) ذخیره می‌شوند.

دیتابیس با الگوریتم AES رمزنگاری شده و به صورت messages.db.encrypted ذخیره می‌گردد.

فایل رمزنگاری شده به پوشه dbs/ منتقل شده و در ریپازیتوری commit می‌شود.

وقتی app.py را روی سیستم خود با کلید رمز درست اجرا کنید، به صورت خودکار دیتابیس را رمزگشایی کرده و پیام‌ها را در قالبی شبیه تلگرام نمایش می‌دهد.

ساختار فایل‌ها و توضیح هر یک
فایل / پوشه	توضیح
.github/workflows/fetch.yml	فایل workflow گیت‌هاب اکشن – هر ۱۲ ساعت اجرا می‌شود، fetch_messages.py را فراخوانی کرده و سپس دیتابیس رمز شده را commit می‌کند.
fetch_messages.py	اسکریپت اصلی: اتصال به تلگرام، دریافت ۱۰۰ پیام، ذخیره در دیتابیس، رمزنگاری و ساخت فایل .encrypted.
db.py	مدیریت دیتابیس SQLite (ساخت جدول‌ها، ذخیره چت و پیام، بازیابی پیام‌ها).
crypto_utils.py	توابع رمزنگاری و رمزگشایی AES با استفاده از کتابخانه cryptography.
app.py	سرور Flask. فایل رمز شده را از dbs/ کپی کرده، با کلید موجود در .env رمزگشایی می‌کند و وب‌سایت را اجرا می‌نماید.
templates/index.html	نمایش لیست چت‌های ذخیره شده.
templates/chat.html	نمایش پیام‌های یک چت به صورت حباب‌های چپ و راست (پیام‌های خودتان آبی در سمت راست).
static/style.css	استایل شبیه تلگرام با حباب‌های واکنش‌گرا.
requirements.txt	وابستگی‌های پایتون: flask, telethon, python-dotenv, cryptography.
dbs/	پوشه‌ای که دیتابیس رمز شده (messages.db.encrypted) در آن ذخیره و commit می‌شود.
.gitignore	فایل‌های موقت و دیتابیس رمزنگاری نشده را نادیده می‌گیرد اما dbs/ را نگه می‌دارد.
راهنمای گام به گام اجرا
1. پیش‌نیازها روی سیستم خودتان
پایتون ۳.۱۰ یا بالاتر

Git

2. گرفتن اطلاعات API تلگرام
به my.telegram.org بروید

وارد شوید و یک اپلیکیشن بسازید تا API_ID و API_HASH را دریافت کنید

شماره تلفن خود (با کد کشور) را آماده داشته باشید.

3. ساخت Session String (اختیاری اما پیشنهادی)
روی سیستمی که تلگرام باز است، اجرا کنید:

python
from telethon import TelegramClient
client = TelegramClient('session', API_ID, API_HASH)
client.start(phone='+989123456789')
print(client.session.save())
خروجی را کپی کنید – این SESSION_STRING شماست.

4. ساختن کلید رمزنگاری
این کد را یکبار اجرا کنید:

python
import secrets, base64
key = secrets.token_bytes(32)
print(base64.b64encode(key).decode())
خروجی را ذخیره کنید – این ENCRYPTION_KEY است. کلید را مخفی نگه دارید!

5. ساخت ریپازیتوری در گیت‌هاب
یک ریپازیتوری خصوصی (Private) بسازید (مثلاً telegram-archive).

آن را روی سیستم خود کلون کنید:

bash
git clone https://github.com/your-username/telegram-archive.git
cd telegram-archive
6. اضافه کردن تمام فایل‌های پروژه
پوشه‌ها را ساخته و تمام فایل‌های ذکر شده در بالا (کدهای کامل که قبلاً داده شد) را اضافه کنید. مطمئن شوید که موارد زیر موجودند:

.github/workflows/fetch.yml

fetch_messages.py, db.py, crypto_utils.py, app.py

templates/ با index.html, chat.html

static/style.css

requirements.txt, .gitignore

dbs/.gitkeep (فایل خالی برای نگه داشتن پوشه)

7. تنظیم Secrets در گیت‌هاب
به ریپازیتوری → Settings → Secrets and variables → Actions → New repository secret بروید. این شش مقدار را اضافه کنید:

نام Secret	مقدار
API_ID	API ID عددی شما
API_HASH	رشته هش API
PHONE	شماره تلفن (مثال: +989123456789)
SESSION_STRING	رشته سشن (یا خالی بگذارید)
CHAT_ID	آیدی چت (عددی مثل -1001234567890 یا نام کاربری مثل @mygroup)
ENCRYPTION_KEY	کلید base64 که ساخته‌اید
8. ارسال کدها به گیت‌هاب
bash
git add .
git commit -m "نسخه اولیه: ربات آرشیو تلگرام"
git push origin main
9. اجرای دستی workflow (بار اول)
به تب Actions در ریپازیتوری گیت‌هاب بروید.

روی Fetch Telegram Messages کلیک کنید → Run workflow.

صبر کنید تا تمام شود. بررسی کنید که پوشه dbs/ شامل messages.db.encrypted شده باشد (صفحه ریپو را refresh کنید).

10. مشاهده پیام‌ها روی سیستم خودتان
آخرین تغییرات را بگیرید:

bash
git pull
فایل .env را در پوشه پروژه بسازید:

text
ENCRYPTION_KEY=your_base64_key_here
وابستگی‌ها را نصب کنید:

bash
pip install -r requirements.txt
برنامه Flask را اجرا کنید:

bash
python app.py
مرورگر را باز کرده و به آدرس http://127.0.0.1:5000 بروید.

لیست چت‌ها را می‌بینید. روی هر چت کلیک کنید – پیام‌های خودتان آبی در سمت راست و دیگران خاکستری در سمت چپ نمایش داده می‌شوند.

نکات مهم
workflow هر ۱۲ ساعت یکبار به صورت خودکار اجرا می‌شود. همچنین می‌توانید دستی اجرا کنید.

فقط پیام‌های متنی ذخیره می‌شوند (تصاویر، فایل‌ها و پیام‌های سیستمی نادیده گرفته می‌شوند).

دیتابیس با AES‑CFB رمزنگاری می‌شود. بدون کلید رمز، حتی گیت‌هاب هم نمی‌تواند پیام‌ها را بخواند.

برای امنیت بیشتر، ریپازیتوری خود را خصوصی (Private) نگه دارید.

رفع اشکال
خطا: ModuleNotFoundError – اجرا کنید: pip install -r requirements.txt

خطا در workflow به خاطر نسخه v3 آپلود آرتیفکت – در YAML ارائه شده رفع شده (از v4 استفاده می‌کند).

Flask خطای "Not Found" می‌دهد – مطمئن شوید پوشه‌های templates/ و static/ وجود دارند و فایل‌های درست درونشان هستند.

پیامی نمایش داده نمی‌شود – بررسی کنید CHAT_ID درست است و شما عضو آن چت هستید.
# Auto-Forward Message

**Bahasa Indonesia**:  
Proyek ini adalah skrip Python untuk mengotomatiskan forwarding pesan dari satu grup Telegram ke beberapa grup tujuan menggunakan library Telethon. Skrip ini mendukung multiple akun, looping untuk mem-forward pesan baru, dan opsi untuk menggunakan ID pesan tertentu atau pesan terbaru. Cocok untuk keperluan promosi atau distribusi pesan otomatis di Telegram.

**English**:  
Auto-Forward Message is a Python script that automates forwarding messages from a source Telegram group to multiple destination groups using the Telethon library. It supports multiple accounts, looping to forward new messages, and options to forward a specific message ID or the latest message. Ideal for automated promotions or message distribution on Telegram.

## Features
- **Multiple Accounts**: Forward messages using multiple Telegram accounts for increased reach.
- **Group Support**: Use group IDs (e.g., `-100987654321`) or usernames (e.g., `@NamaGrup`) for source and destination groups.
- **Message Flexibility**: Forward a specific message (by `message_id`) or the latest message from the source group.
- **Looping Mode**: Continuously check for new messages in the source group and forward them at specified intervals.
- **Random Delay**: Add random delays (e.g., 60-120 seconds) between forwards to avoid Telegram restrictions.
- **Error Handling**: Validates group access, handles session issues, and provides clear error messages.

## Prerequisites
- **Python 3.7+**: Ensure Python is installed on your system.
- **Telethon Library**: Python library for interacting with Telegram's API.
- **Telegram API Credentials**: Obtain `api_id` and `api_hash` from [my.telegram.org](https://my.telegram.org).
- **Termux (Optional)**: For running the script on Android devices.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Yuurichan-N3/Auto-Forward-Message.git
   cd Auto-Forward-Message
   ```

2. **Install Dependencies**:
   ```bash
   pip install telethon
   ```

3. **Set Up Termux (Optional for Android)**:
   - Install Termux from [F-Droid](https://f-droid.org/packages/com.termux/) or the Play Store.
   - Grant storage permission:
     ```bash
     termux-setup-storage
     ```
   - Install Python and Telethon:
     ```bash
     pkg install python
     pip install telethon
     ```

## Getting Telegram API Credentials
1. Visit [my.telegram.org](https://my.telegram.org) and log in with your Telegram phone number.
2. Select **API development tools**.
3. Create a new application:
   - **App title**: e.g., `AutoForwardBot`
   - **Short name**: e.g., `ForwardBot`
   - **Platform**: Choose `Other` or `Android`
   - **Description**: e.g., `Automated message forwarding`
4. Click **Create application** and note down your **App api_id** (number) and **App api_hash** (string).

## Usage
The script supports two modes:
- **Create**: Generates session files and `configuration.json`.
- **Run**: Forwards messages with optional looping.

### 1. Prepare Group IDs or Usernames
- Use `@GetIDsBot` to get group IDs:
  - Send `/start` to `@GetIDsBot`.
  - Forward a message from the source or destination group to get its **Chat ID** (e.g., `-100987654321`).
  - For a specific message, note the **Message ID** (e.g., `123`).
- For public groups, you can use usernames (e.g., `@NamaGrup`).
- Ensure all accounts are members of the source and destination groups.

### 2. Run the Script
```bash
python bot.py
```

#### Mode 1: Create
- Select `1` to create sessions and `configuration.json`.
- Input:
  - Number of Telegram accounts.
  - For each account: phone number (e.g., `+628123456789`), `api_id`, `api_hash`, verification code, and 2FA password (if enabled).
  - Source group ID or username (e.g., `-100987654321` or `@SourceGroup`).
  - Message ID (optional, leave blank for latest message).
  - Whether to use a fixed message ID for every loop (`y/n`).
  - Number of destination groups, then their IDs or usernames (e.g., `-100123456789`, `@TargetGroup`).
  - Minimum and maximum delay per forward (e.g., `60` and `120` seconds).
  - Loop interval for checking new messages (e.g., `300` for 5 minutes).
- Output: Session files (e.g., `session_628123456789.session`) and `configuration.json`.

#### Mode 2: Run
- Select `2` to forward messages.
- The script:
  - Displays `configuration.json` for verification.
  - Forwards the specified message (if `use_fixed_message_id: true`) or the latest message (if `null` or `use_fixed_message_id: false`) on the first iteration.
  - Loops every `loop_interval` seconds to check for new messages (unless using fixed `message_id`).
  - Press `Ctrl+C` to stop the loop.

### Example `configuration.json`
```json
{
  "accounts": [
    {
      "api_id": "123456",
      "api_hash": "abcdef1234567890abcdef1234567890",
      "phone": "+628123456789",
      "session": "session_628123456789"
    }
  ],
  "groups": [
    "-100123456789",
    "@TargetGroup1"
  ],
  "source_group": "-100987654321",
  "message_id": 123,
  "use_fixed_message_id": false,
  "delay": {
    "min_delay": 60.0,
    "max_delay": 120.0
  },
  "loop_interval": 300.0
}
```
- **`source_group`**: Group to forward messages from.
- **`groups`**: Destination groups to forward messages to.
- **`message_id`**: Specific message ID to forward (if `use_fixed_message_id: true`).
- **`use_fixed_message_id`**: If `true`, always forward the specified `message_id`; if `false`, forward new messages.
- **`loop_interval`**: Seconds between checking for new messages.

### Manual Configuration
- Edit `configuration.json` to add more destination groups or change settings.
- Ensure JSON format is valid and accounts are members of all groups.
- Example: Add a new group:
  ```json
  "groups": ["-100123456789", "@TargetGroup1", "-100345678901"]
  ```

## Telegram Restrictions
- **Rate Limits**: Maximum 20 messages per minute per group. The random delay (`min_delay` to `max_delay`) helps avoid bans.
- **Account Bans**: Use multiple accounts and reasonable delays to minimize risks.
- **Group Access**: Accounts must be members of all source and destination groups.

## Troubleshooting
- **Error: Group not found**:
  - Verify group IDs/usernames with `@GetIDsBot`.
  - Ensure accounts are members of the groups.
- **Error: Session invalid**:
  - Run mode `1` (Create) to regenerate session files.
- **Error: JSON decode error**:
  - Check `configuration.json` for syntax errors.
- **Loop not forwarding new messages**:
  - Ensure `"use_fixed_message_id": false` in `configuration.json`.
  - Check `loop_interval` (e.g., `300` seconds).
 
## 📜 Lisensi  

Script ini didistribusikan untuk keperluan pembelajaran dan pengujian. Penggunaan di luar tanggung jawab pengembang.  

Untuk update terbaru, bergabunglah di grup **Telegram**: [Klik di sini](https://t.me/sentineldiscus).


---

## 💡 Disclaimer
Penggunaan bot ini sepenuhnya tanggung jawab pengguna. Kami tidak bertanggung jawab atas penyalahgunaan skrip ini.

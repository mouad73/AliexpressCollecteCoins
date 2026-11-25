# AliExpress Coin Collector for Linux / Lubuntu

An automated Python tool to help collect daily coins on AliExpress with human-like interactions to avoid detection, adapted to run on Linux environments (such as Lubuntu/Ubuntu).

## Features

- Automatic login to AliExpress account
- Changes region to Korea (for maximum coin rewards)
- Collects daily coins with realistic human-like behavior
- Interactive manual confirmation steps for critical actions
- Secure credential management using environment variables
- Native WebDriver initialization on Linux via Selenium Manager (no `winreg` dependency or manual `chromedriver.exe` download)

## Prerequisites

- Python 3.7+ (including `python3-venv` for isolated environments)
- Google Chrome (or Chromium) browser
- A valid AliExpress account

## Installation on Linux

1. Clone the repository:
   ```
   git clone [https://github.com/mouad73/AliexpressCollecteCoins.git](https://github.com/mouad73/AliexpressCollecteCoins.git)
   cd AliexpressCollecteCoins
   
Note: If you plan to use SSH authentication with your own repository or fork on GitHub, generate an `ed25519` key using `ssh-keygen -t ed25519`, add it to `ssh-agent`, register the public key on GitHub, and clone via `git@github.com:YOUR_USERNAME/YOUR_REPO.git`.)

1. Create and activate a Python virtual environment (recommended on systems enforcing PEP 668 / `externally-managed-environment`):
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
 (If `venv` is not available, install it with `sudo apt update && sudo apt install -y python3-venv`.)

2. Install the required packages inside the virtual environment:
   ```
   pip install -r requirements.txt
   ```

3. Adapt `collect_coins.py` for Linux:
   Create a backup of the original file before editing:
   ```
   cp collect_coins.py collect_coins.py.bak
   ```

   Replace the `winreg` detection and `chromedriver-win64.zip` / `chromedriver.exe` download block with direct initialization via Selenium Manager:
   ```
   # Initialize WebDriver natively on Linux via Selenium Manager
   try:
    driver = webdriver.Chrome(options=chrome_options)
    print("WebDriver initialized successfully")
    ```
   
4. Create a `.env` file from the example template:
   ```
   cp .env.example .env
   ```

5. Edit the .env file with your AliExpress login credentials:
   ```
   ALIEXPRESS_EMAIL=your_actual_email@example.com
   ALIEXPRESS_PASSWORD=your_actual_password
   ```
## Usage
Run the script with:
   ```
   python collect_coins.py
   ```

Or invoke the virtual environment's Python interpreter directly:
   ```
   ~/AliexpressCollecteCoins/venv/bin/python collect_coins.py
   ```

The script will:
1. Open a Chrome browser window
2. Navigate to the AliExpress coin collection page
3. Log in with your credentials from the `.env` file
4. Ask for manual confirmation at critical steps (to ensure correct elements are clicked)
5. Change region to Korea for maximum coin benefits
6. Collect the daily coins
7. Close the browser when complete

## Automated Daily Collection on Linux (cron)

1. Instead of Windows Task Scheduler, you can schedule daily runs on Linux using `cron`:

Open your user `crontab`:
   ```
crontab -e
   ```

2. Add a line to run daily at your preferred time (e.g., 10:00 AM):
   ```
   0 10 * * * cd /home/your_username/AliexpressCollecteCoins && /home/your_username/AliexpressCollecteCoins/venv/bin/python collect_coins.py >> /home/your_username/AliexpressCollecteCoins/collector.log 2>&1
   ```
(Keep in mind that the script uses manual `input()` prompts, so fully unattended execution requires modifying the code.)

### Important Notes about Automation

- The script requires manual confirmation steps, so fully unattended operation isn't possible with the current version
- If you want completely unattended operation, you would need to modify the script to remove the `input()` prompts
- Running automated scripts that interact with websites may violate terms of service
- Use at your own risk and consider AliExpress's policies

## Interactive Confirmation Steps

This script uses interactive confirmations at critical points to ensure the correct elements are being selected. When prompted:

1. The target element will be highlighted with a red border
2. You'll be asked to press Enter to proceed
3. The script will then click the highlighted element and continue

This design prevents errors if AliExpress changes its interface layout.

## Security

- Your credentials are stored locally in the `.env` file, which should NEVER be committed to Git
- The `.gitignore` file includes `.env` to prevent accidental commits
- The script uses environment variables instead of hardcoded credentials

## Troubleshooting

1. `error: externally-managed-environment` when running `pip install`: Create and activate a virtual environment (`python3 -m venv venv && source venv/bin/activate`) before installing dependencies.

2. `No module named 'winreg'`: The original script attempts to read the Windows Registry and download `chromedriver.exe`. Remove that block and initialize `webdriver.Chrome(options=chrome_options)` directly on Linux.

3. Login Failures / Element Not Found Errors: AliExpress frequently updates its selectors, displayed currency/language (e.g., `BRL/R$` instead of `USD`), and login flows. Inspect the page in Chrome (`F12`) to update the selectors in the code.

4. Captcha Challenges: The script includes human-like behavior, but if you encounter captchas frequently, try reducing usage frequency or using a persistent Chrome profile.

## Legal Disclaimer

This tool is provided for educational purposes only. Use at your own risk. The creator is not responsible for account suspensions, lost coins, or other issues that may arise from automated interactions with AliExpress. Always review the AliExpress Terms of Service before using automation tools.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)

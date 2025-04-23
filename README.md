# AliExpress Coin Collector

An automated tool to help collect daily coins on AliExpress with human-like interactions to avoid detection.

## Features

- Automatic login to AliExpress account
- Changes region to Korea (for maximum coin rewards)
- Collects daily coins with realistic human-like behavior
- Interactive manual confirmation steps for critical actions
- Secure credential management using environment variables

## Prerequisites

- Python 3.7+
- Google Chrome browser
- A valid AliExpress account

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/YOUR_USERNAME/AliExpress-Coin-Collector.git
   cd AliExpress-Coin-Collector
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file for your credentials:
   ```
   cp .env.example .env
   ```

4. Edit the `.env` file with your AliExpress login credentials:
   ```
   ALIEXPRESS_EMAIL=your_actual_email@example.com
   ALIEXPRESS_PASSWORD=your_actual_password
   ```

## Usage

Run the script with:

```
python collect_coins.py
```

The script will:
1. Open a Chrome browser window
2. Navigate to the AliExpress coin collection page
3. Log in with your credentials from the `.env` file
4. Ask for manual confirmation at critical steps (to ensure correct elements are clicked)
5. Change region to Korea for maximum coin benefits
6. Collect the daily coins
7. Close the browser when complete

## Automated Daily Collection with Windows Task Scheduler

You can set up Windows Task Scheduler to run the script automatically once per day:

### Create a Batch File

1. Create a file named `run_collector.bat` in the project directory with the following content:
   ```bat
   @echo off
   cd /d %~dp0
   echo Running AliExpress Coin Collector at %date% %time%
   python collect_coins.py
   echo Collection completed at %date% %time%
   pause
   ```

### Set Up Task Scheduler

1. Press **Win + S** and search for "Task Scheduler"
2. Click on "Create Basic Task..." in the right panel
3. Enter a name (e.g., "AliExpress Coin Collector") and description
4. Select "Daily" for the trigger and set your preferred time (e.g., 10:00 AM)
5. Select "Start a program" for the action
6. Browse and select your `run_collector.bat` file
7. Set the "Start in" field to your project directory path (e.g., `C:\Users\username\AliExpress-Coin-Collector`)
8. Check "Open the Properties dialog..." and click Finish
9. In the Properties dialog:
   - Go to the "General" tab and check "Run whether user is logged in or not"
   - Go to the "Settings" tab and uncheck "Stop the task if it runs longer than..."
   - Click "OK" to save the task

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

If you encounter issues:

- **Login Failures**: Ensure your credentials in the `.env` file are correct
- **Element Not Found Errors**: AliExpress may have updated their website. Please create an issue on GitHub
- **Captcha Challenges**: The script includes human-like behavior, but if you encounter captchas frequently, try reducing usage frequency

## Legal Disclaimer

This tool is provided for educational purposes only. Use at your own risk. The creator is not responsible for account suspensions, lost coins, or other issues that may arise from automated interactions with AliExpress. Always review the AliExpress Terms of Service before using automation tools.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)
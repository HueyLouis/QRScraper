# PyQRScraper
A Tool I created for client who had a lot of QR Codes and wanted an automated process to scrape all the links and the data from each code

*This specific script is tailored to working with Instagram QR Codes*

# QR Code Script
This script performs various tasks on QR codes, including making QR codes readable, splitting QR codes, scanning QR codes, scanning for usernames, cleaning saved usernames, and getting accounts from clean usernames.

## Dependencies
- Python 3
- argparse
- csv
- subprocess
- os
- json
- pytesseract
- Pillow
- pyzbar

  ## Usage
To use the script, run it from the command line with the desired arguments. The available arguments are:
- **-make**: Make QR codes readable
- **-split**: Split QR codes
- **-scan**: Scan QR codes
- **-users**: Scan for Usernames
- **-clean-users**: Clean Saved Usernames (Often there would be missing characters)
- **-save-users**: Get accounts from clean usernames
For example, to make QR Codes readable run
```bash
python main.py -make
```

## Functionality
### Making QR Codes Readable
The **-make** argument makes QR codes readable by converting them to RGB mode with a white background. The readable QR codes are saved to the **readablesDir** directory.

### Splitting QR Codes
The **-split** argument splits QR codes into two images: one containing the QR code and one containing the username. The split images are saved to the **tagsDir** and **namesDir** directories, respectively.

### Scanning QR Codes
The **-scan** argument scans QR codes in the **tagsDir** directory and extracts data from the QR codes. If the QR code contains an Instagram link, the script extracts the username and bio picture and saves the results to the **output.json** file.

### Scanning for Usernames
The **-users** argument scans for usernames in the **namesDir** directory using the **pytesseract** library. The extracted usernames are saved to the **Usernames.csv** file.

### Cleaning Saved Usernames
The **-clean-users** argument cleans saved usernames in the **Usernames.csv** file by removing spaces and adding the '@' symbol if necessary. The cleaned usernames are saved to the **CleanedUsernames.csv** file.

### Collecting Accounts from Cleaned Usernames
The **-save-users** argument gets accounts from clean usernames in the **CleanedUsernames.csv** file by sending HTTP requests to Instagram and extracting the bio and profile picture. The results are saved to the **Accounts.txt** file.

## Credits
This script uses the following libraries:
- argparse
- csv
- subprocess
- os
- json
- pytesseract
- Pillow
- pyzbar

## Licence
[MIT](https://choosealicense.com/licenses/mit/)

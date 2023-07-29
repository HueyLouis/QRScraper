#!/usr/bin/env python3

import argparse
import csv
import subprocess
import os
import json
import pytesseract  #Image-text-processing
from PIL import Image, UnidentifiedImageError #This is to make Tags Readable
from pyzbar.pyzbar import decode #Scan QR Codes

#Starting Directories
rawTagsDir = '/home/hueylouis/Desktop/TrainingData/QRTags'
readablesDir = '/home/hueylouis/Desktop/TrainingData/QRTags/Readable'

os.makedirs(readablesDir, exist_ok=True) #Create if it doesnt exist

#QR Code Directories
tagsDir = "TagsSplit"
namesDir = "NamesSplit"

outputJSON = 'output.json'
usernamesFile = 'Usernames.csv'
cleanedUsernames = 'CleanedUsernames.csv'
accountsFile = 'Accounts.txt'

results = {} #Results Dictionary

def makeReadable():
    if not os.path.exists(readablesDir):   #Create Directory
        os.makedirs(readablesDir)

    #Loop through files
    for filename in os.listdir(rawTagsDir):
        if filename.endswith('.png'):
            print(f"Processing file (Transforming Files): {filename}")
            with Image.open(os.path.join(rawTagsDir, filename)) as img:
                if img.mode in ('RGBA', 'LA'):
                    if img.mode == 'RGBA':
                        # Convert image to RGBA mode
                        img = img.convert('RGBA')

                        # Split the channels
                        r, g, b, a = img.split()

                        # Count the number of unique colors in the alpha channel
                        num_colors = len(set(a.getdata()))

                        if num_colors == 2:
                            # Convert image to RGB with white background
                            new_img = Image.new("RGB", img.size, (255, 255, 255))
                            new_img.paste(img, mask=img.split()[3])
                            new_img.save(os.path.join(readablesDir, filename)) #Save to output directory 

                    elif img.mode == 'LA':
                        # Convert image to RGB with white background
                        new_img = Image.new("RGB", img.size, (255, 255, 255))
                        new_img.paste(img, mask=img.split()[1])
                        new_img.save(os.path.join(readablesDir, filename)) #Save to output directory 
                           
def splitTags():
    if not os.path.isdir(readablesDir):
        print("Error: Directory does not exist")
        exit()
        

    os.makedirs(tagsDir, exist_ok=True)
    os.makedirs(namesDir, exist_ok=True)

    #Loop through all images
    for filename in os.listdir(readablesDir):   #ChangeReadablesDirector
        if filename.endswith('.png'):
            img = Image.open(os.path.join(readablesDir, filename)) #Open the image
            print(f"Processing file (Splitting Images): {filename}")

            #Crop images
            top = img.crop((0,0, img.width, 528))
            bottom = img.crop((0, 528, img.width, img.height))

            #Save the split images
            top.save(os.path.join(tagsDir, filename))
            bottom.save(os.path.join(namesDir, filename))

def scanQRCode():
    #outputJSON = 'output.json'

    qrCodes = [] #Store decoded QR Codes

    #Loop through all QR Codes in the Tags Directory
    for filename in os.listdir(tagsDir):
        if filename.endswith('.png'):
            try:
                img = Image.open(os.path.join(tagsDir, filename))  #Open
            except UnidentifiedImageError:
                print(f"Error: Cannot identify image {filename}. Skipping...")
                continue
            
            print(f"Processsing file (Scanning QR Codes): {filename}")
            
            try:
                #Decode codes in the image
                decodedCodes = decode(img)
            except AssertionError:
                print(f"Error Assertion failed for file {filename}. Skipping...")
                continue
            
            #Append the decoded QR Codes to qrCodes list
            qrCodes.extend(decodedCodes)

            #Extract data from the QR Code
            for qrCode in decodedCodes:
                if 'instagram.com' in qrCodes.data.decode():
                    #Extract data from the QR Code
                    instagramLink = qrCode.data.decode()                        #Link
                    username = instagramLink.split('/')[-2]                     #Username
                    bioPicture = f'https://www.instagram.com/{username}/?__a=1' #Bio Picture

                    #Add results to the dictionary
                    results[filename] = {
                        'username': username,
                        'Bio_Picture': bioPicture
                    }

    #Write Results to output file
    with open(outputJSON, 'w') as f:
        json.dump(results, f)

class QRCodeNamesScanner:
    def __init__(self, nameDir):
        self.nameDir = nameDir

    def scanUsernames(self):
        textList = []

        #Loop through each PNG Image in the directory
        for filename in os.listdir(namesDir):
            if filename.endswith(".png"):
                namePath = os.path.join(namesDir, filename)
                img = Image.open(namePath)
                print(f"Processing file (Scanning Username): {filename}")
                text = pytesseract.image_to_string(img)

                textList.append(text)
        
        #Write extracted text to output file
        with open(usernamesFile, "w", newline='') as f:
            writer = csv.writer(f)
            for text in textList:
                writer.writerow([text])

    def cleanUsernames(self, usernamesInputFile=usernamesFile):
        with open(usernamesInputFile, 'r') as f:
            reader = csv.reader(f)
            usernames = list(reader)

        cleaned_usernames = []
        for usernames in username:
            print(f"Cleaning username: {usernames}")
            cleanedUsername = usernames[0].replace(" ", "") #Remove spaces
            if not cleanedUsername.startswith('@'):     #Add '@'
                cleanedUsername = '@' + cleanedUsername
            cleaned_usernames.append([cleanedUsername])

        with open(cleanedUsernames, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(cleaned_usernames)

    def findUsernames(self, inputUsernamesFile):
        with open(inputUsernamesFile, 'r') as f:
            reader = csv.reader(f)
            usernames = list(reader)

        results = []
        for usernames in usernames:
            print(f'Processing Username: {usernames}')
            cleanedUsernames = username[0].replace("@","")
            instagramLink = f"https://www/instagram.com/{cleanedUsernames}/?__a=1"
            try:
                response = request.get(instagramLink)
                response.raise_for_status()
                data = response.json()
                bio = data['graphq1']['user']['biography']
                profilePicture = data['graphq1']['user']['profile_pic_url_hd']
                results.append([cleanedUsername, bio, profilePicture])
            except request.exceptions.HTTPError as e:
                print(f"Error: {e}")
                continue

        with open(accountsFile, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Username', 'Bio', 'Profile Picture'])
            writer.writerows

#Parse command line arguments
parser = argparse.ArgumentParser(description='Script to perform task on QR Codes')
parser.add_argument('-make', action='store_true', help='Make QR codes readable')
parser.add_argument('-split', action='store_true', help='Split QR Codes')
parser.add_argument('-scan', action='store_true', help='Scan QR codes')
parser.add_argument('-users', action='store_true', help='Scan for Usernames')
parser.add_argument('-clean-users', action='store', dest='clean_users', metavar='USERNAMES', help='Clean saved Usernames', default=None)
parser.add_argument('-save-users', action='store', dest='save_users', metavar='ACCOUNT_DATA',help='Get Accounts from Clean Usernames')
args = parser.parse_args()

#Execute tasks based on command line arguments
if args.make:
    print('Making Readable QR Codes')
    makeReadable()
    print('QR Codes are now readable')

if args.split:
    print(f'Splitting QR Codes from usernames in {readablesDir}')
    splitTags()
    print('Completed...')

if args.scan:
    print(f'Scanning for QR Codes in {tagsDir}')
    scanQRCode()
    print('Completed...')

if args.users:
    print(f'Scanning for Usernames in {namesDir}')
    scanner = QRCodeNamesScanner(nameDir=namesDir)
    scanner.scanUsernames()
    print('Completed...')

if args.clean_users:
    if args.clean_users:
        cleanedUsernamesFile = args.clean_users
    else:
        cleanedUsernamesFile = usernamesFile
    print(f'Cleaning saved Usernames in {namesDir}')
    scanner = QRCodeNamesScanner(nameDir=namesDir)
    try:
        scanner.cleanUsernames(cleanedUsernamesFile)
        print('Completed...')
    except FileNotFoundError:
        print(f"Error: {cleanedUsernamesFile} not found.")

if args.save_users:
    if args.save_users:
        accountsReadFile = args.save_users
    else:
        accountsReadFile = cleanedUsernames
    print(f"Finding and Saving Usernames from {accountsReadFile}")
    scanner = QRCodeNamesScanner(nameDir=namesDir)
    try:
        scanner.findUsernames(accountsReadFile)
    except FileNotFoundError:
        print(f"Error: {accountsReadFile} not found")


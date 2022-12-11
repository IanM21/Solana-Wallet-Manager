# Solana-Wallet-Manager
Solana Wallet Manager (Cozy Tools)
### ps. sorry for the messy code, unsure if this works still or not. 

## Files Needed:
* pub.txt
* sub-wallets.txt
* config.json
* webhook.txt
* transaction.txt

## Setup
- Create [Hyper](https://hyper.co/) license system
- config.json includes License Key, Main Wallet Public & Private Key
- pub.txt => all "sub" wallets public keys
- sub-wallets.txt => nickname,walletaddress 
- webhook.txt => discord webhook URL
- transaction.txt => leave blank, never edit (used to store TX urls for webhook embed)

## Requirements
- Cloudscraper
- Requests
- BS4
- timeit
- solana.py
- base58
- json
- OS | SYS | time | colorama
- termcolor (cprint)
- pyfiglet 
- inquirer
- matplotlib
- emoji

from timeit import default_timer as timer
import token
import requests
import solana
from solana.message import Message
from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.transaction import Transaction
from solana.rpc.types import TxOpts
from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solana.transaction import Transaction, TransactionInstruction, AccountMeta
from spl.token.instructions import create_associated_token_account, transfer_checked, TransferCheckedParams, get_associated_token_address
from solana.rpc.types import TxOpts
from base58 import b58decode, b58encode
import base58
import json
import sys
import os
import time
import bs4
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format
import cloudscraper
import inquirer
import matplotlib.pyplot as plt
import emoji

# Fetch SOL/USD price from CoinGecko API

resp = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=sol,usd')
price = json.loads(resp.text)
sol_usd = price['solana']['usd']

# Fetch SOL/USD price change from CoinGecko API

resp111 = requests.get('https://api.coingecko.com/api/v3/coins/solana')
price_change = json.loads(resp111.text)
sol_change = price_change['market_data']['price_change_percentage_24h']

# Set terminal title

title='CozyTools V0.05 | SOL/USD: $' + str(sol_usd) + ' | Change: ' + str(sol_change) + '%'
os.system('echo -n -e "\033]0;{}\007"'.format(title))


def CozyTools():
    with open('config.json', 'r') as key_file:
        data = json.loads(key_file.read())
        license = data['license']
        rpc = data['rpc']
        main_wallet = data['main_wallet']
        privkey = data['privkey']
    key_file.close()

    cprint('Checking {}'.format(license), 'yellow')
    print('\n')

    # Check license status via hyper.co API
    url = "https://api.hyper.co/v6/licenses/" + license

    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer token"
    }

    response = requests.get(url, headers=headers)

    keyinfo = json.loads(response.text)

    keycheck = keyinfo['status']

    if keycheck == 'active':

        cprint('{} is active'.format(license), 'green')

        while True:
            
            cprint(figlet_format('Cozy Toolbox', font='larry3d'),
                    'blue', attrs=['bold'])

            optionlist = ['Magic Eden Lister', 'Magic Eden Floor Sniffer', 'Magic Eden Historical Data', 'Wallet Manager', 'RPC Ping Test', 'Exit']

            questions = [inquirer.List(
                                    'Options',
                                    message="Select A Task Option",
                                    choices=optionlist,
                                    ),
                ]
            answers = inquirer.prompt(questions)
            userchoice = (answers['Options'])

            if userchoice == 'Magic Eden Lister':

                def NFTLister():
                    cprint('\nLoading NFT Lister Module...\n', 'green')
                    time.sleep(2)

                    scraper = cloudscraper.create_scraper(
                        browser={
                            'browser': 'firefox',
                            'platform': 'windows',
                            'mobile': False
                        }
                    )

                    url2 = 'https://api.solanabeach.io/v1/account/' + main_wallet + '/tokens'
                    sitereq = scraper.get(url2).text

                    html2 = sitereq
                    soup2 = bs4.BeautifulSoup(html2,'html.parser')
                    site_json2=json.loads(soup2.text)

                    list1=[]
                    list2=[]
                    AvailNFTs=[]
                    dList = []
                    SelectedTokenName = []
                    SelectedTokenAddress = []
                    SelectedTokenATA = []
                    selectedNFT = []


                    for i in range(len(site_json2)):
                        tokenAddress = (site_json2[i]['mint']['address'])
                        tokenATA = (site_json2[i]['address']['address'])
                        tokenMeta = scraper.get('https://public-api.solscan.io/token/meta?tokenAddress=' + tokenAddress).text
                        metadata = json.loads(tokenMeta)
                        name = (metadata['name'])
                        
                        list1.append([name])
                        list2.append([tokenAddress] + [tokenATA])
                        AvailNFTs.append([name] + [tokenAddress] + [tokenATA])

                        one = {'Name': name, 'tokenAddress': tokenAddress, 'tokenATA': tokenATA}
                    
                        dct = dict(one)
                        
                        dList.append(one)                            

                    questions = [
                        inquirer.Checkbox('NFT',
                                        message="Select NFT to list",
                                        choices=dList + ['Exit'],
                                        ),
                        ]

                    answers = inquirer.prompt(questions)
                    selected = answers['NFT']

                    if selected == ['Exit']:
                            cprint('\nExiting NFT Lister Module\n', 'red')
                            CozyTools()

                    else: 
                        for i in range(len(answers['NFT'])):
                            selectedTokenName = selected[i]['Name']
                            selectedtokenAddress = selected[i]['tokenAddress']
                            selectedtokenATA = selected[i]['tokenATA']
                            sellerRefferal = 'autMW8SgBkVYeBgqYiTuJZnkvDZMVU2MHJh9Jh7CSQ2'

                            SelectedTokenName.append(answers['NFT'][i]['Name'])
                            SelectedTokenAddress.append(answers['NFT'][i]['tokenAddress'])
                            SelectedTokenATA.append(answers['NFT'][i]['tokenATA'])
                            selectedNFT.append(selectedTokenName)
                            selectedNFT.append(selectedtokenAddress)
                            selectedNFT.append(selectedtokenATA)
                            cprint("Name: {}, Token Address: {}, Token ATA: {}".format(selectedTokenName, selectedtokenAddress, selectedtokenATA), 'green')

                            #-----------------------------------------------------#
                            cprint('Enter Price to list {}:'.format(selectedTokenName), 'cyan')
                            price = input("")
                            cprint('listing {} at {} SOL'.format(selectedTokenName, price), 'green')
                            print('\n')

                            listingurl = ("https://api-mainnet.magiceden.io/v2/instructions/sell?seller={}&auctionHouseAddress=E8cU1WiRWjanGxmn96ewBgk9vPTcL6AEZ1t6F6fkgUWe&tokenMint={}&tokenAccount={}&price={}&sellerReferral={}&expiry=-1".format(main_wallet, selectedtokenAddress, selectedtokenATA, str(price), sellerRefferal))
                            payload3={}
                            headers3={
                                'Accept': 'application/json, text/plain',
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
                                'Origin':  'https://magiceden.io/',
                                'Content-Type': 'application/json; charset=utf-8',
                                'Referrer': 'https://magiceden.io/',
                            }

                            lister = scraper.get(listingurl, headers=headers3, data=payload3).text
                            print(listingurl)
                            

                            cprint('Got Instructions to list {} for {}, Sending Transaction Now'.format(selectedTokenName, price), 'green')

                            
                            x = lister
                            
                            y = json.loads(x)

                            z=(y['tx'])

                            instruction_data = (z['data'])
                            privatekey = (privkey)

                            solana_client = Client(rpc)

                            def sendTransaction(instruction_data):
                                wallet = Keypair.from_secret_key(base58.b58decode(privatekey))
                                msg = Message.deserialize(bytes(instruction_data))
                                txn = Transaction.populate(message=msg, signatures =[])
                                response2 = solana_client.send_transaction(txn, wallet, opts=TxOpts(skip_preflight=True, skip_confirmation=True)) 
                                #print(response2)

                                a = json.dumps(response2)
                                b = json.loads(a)
                                tx = 'https://solscan.io/tx/' + (b['result'])

                                cprint('\nTransaction Sent for {}'.format(selectedTokenName), 'green')
                                print(tx)
                            sendTransaction(instruction_data)
                            #-----------------------------------------------------#
                            print('Starting 5s delay to minimize cloudflare spam')
                            time.sleep(5)
                NFTLister()

            
            if userchoice == 'Magic Eden Floor Sniffer':

                def FloorSniffer():
                    cprint(figlet_format('\nStarting Magic Eden Floor Sniffer', font='term'),
                            'green', attrs=['bold'])

                    cprint('Checking {} \n'.format(main_wallet), 'green')

                    scraper = cloudscraper.create_scraper(
                        browser={
                            'browser': 'firefox',
                            'platform': 'windows',
                            'mobile': False
                        }
                    )

                    site_req = scraper.get('https://api-mainnet.magiceden.io/rpc/getNFTsByOwner/' + main_wallet).text

                    html = site_req

                    soup = bs4.BeautifulSoup(html,'html.parser')
                    site_json=json.loads(soup.text)
                    list = []
                    NFTs = ([d.get('collectionName') for d in site_json['results'] if d.get('collectionName')])
                    list = NFTs
                    questions = [
                        inquirer.List('NFTs',
                                    message="Select Collection To Sniff Floor Price Of",
                                    choices=list,
                                ),
                        ]
                    answers = inquirer.prompt(questions)
                    NFTCollection = answers['NFTs']

                    req2 = scraper.get("https://api-mainnet.magiceden.dev/v2/collections/" + NFTCollection + "/stats")

                    resp_data = req2.text

                    info = json.loads(resp_data)
                    floorPric = info['floorPrice']
                    floorPrice = (floorPric/1000000000)

                    ListedCount = info['listedCount']
                    volume = info['volumeAll']
                    volumeALL = (volume/1000000000)

                    print('\nFloor Price of {} is {} SOL'.format(NFTCollection, str(floorPrice)))
                    print('\n{} NFTs Listed On {}'.format(ListedCount, NFTCollection))
                    print('\n{} Total SOL Volume For {}'.format(str(volumeALL), NFTCollection))

                    time.sleep(7)
                FloorSniffer()

            if userchoice == 'Magic Eden Delister':
                cprint(figlet_format('\nRecoding Module, Update Soon', font='term'),
                        'red', attrs=['bold'])
                time.sleep(5)


            if userchoice == 'Wallet Manager':
                cprint(figlet_format('\nStarting Wallet Manager\n', font='term'),
                            'blue', attrs=['bold'])

                option_list = ['Wallet Gen', 'Balance Fetcher', 'Distribute SOL', 'Token Transfer']

                questions = [inquirer.List(
                                        'Options',
                                        message="Select A Task Option",
                                        choices=option_list,
                                        ),
                    ]
                answers = inquirer.prompt(questions)
                user_choice = (answers['Options'])

                if user_choice == 'Wallet Gen':
                    def WalletGen():

                        cprint(figlet_format('\nStarting Wallet Generator', font='term'),
                                'green', attrs=['bold'])
                        amt = input('How Many Wallets Would You Like To Create: ')
                        amount = int(amt)

                        for i in range(amount):
                            wallet = Keypair()
                            wallet_bytes = list(wallet.secret_key)
                            pubkey = wallet.public_key
                            output_file = open(str(pubkey) + '.json', 'w')
                            json.dump(wallet_bytes, output_file)

                        print(amt + ' Wallets Generated')
                        time.sleep(3)

                    WalletGen()

                if user_choice == 'Token Transfer':
                    def NFTSender():
                        import requests as r
                        scraper = cloudscraper.create_scraper(
                                            browser={
                                                'browser': 'firefox',
                                                'platform': 'windows',
                                                'mobile': False
                                            }
                                        )

                        SYSTEM_CLOCK_PROGRAM = 'SysvarC1ock11111111111111111111111111111111'
                        SYSTEM_RECENT_BLOCKHASH_PROGRAM = 'SysvarRecentB1ockHashes11111111111111111111'
                        SYSTEM_INSTRUCTIONS_PROGRAM = 'Sysvar1nstructions1111111111111111111111111'
                        TOKEN_PROGRAM_ID = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'
                        ASSOCIATED_TOKEN_ID = 'ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL'
                        METADATA_PROGRAM_ID = 'metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s'
                        SYSTEM_PROGRAM_ID = '11111111111111111111111111111111'
                        SYSTEM_RENT_PROGRAM = 'SysvarRent111111111111111111111111111111111'

                        NFT_TRANSFER_PROGRAM = "DeJBGdMFa1uynnnKiwrVioatTuHmNLpyFKnmB5kaFdzQ"
                        BURN_PROGRAM = "burn68h9dS2tvZwtCFMt79SyaEgvqtcZZWJphizQxgt"

                        client = Client(rpc)

                        url2 = 'https://api.solanabeach.io/v1/account/' + main_wallet + '/tokens'
                        sitereq = scraper.get(url2).text

                        html2 = sitereq
                        soup2 = bs4.BeautifulSoup(html2,'html.parser')
                        site_json2=json.loads(soup2.text)

                        list1=[]
                        list2=[]
                        AvailNFTs=[]
                        dList = []
                        SelectedTokenName = []
                        mint_address1 = []
                        mint_address = []

                        for i in range(len(site_json2)):
                            tokenAddress = (site_json2[i]['mint']['address'])
                            tokenAccount = (site_json2[i]['address']['address'])
                            
                            tokenMeta = r.get('https://public-api.solscan.io/token/meta?tokenAddress=' + tokenAddress).text
                            metadata = json.loads(tokenMeta)
                            name = metadata['name']
                            list1.append([name])
                            list2.append([tokenAddress])
                            AvailNFTs.append([name] + [tokenAddress])
                            """print('Loading NFTs as [Name | Mint Address]')
                            print(metadata['name'] + ' | ' + site_json2[i]['mint']['address'], '\n')"""

                            one = {'Name': name, 'tokenAddress': tokenAddress}
                                
                            dct = dict(one)

                            dList.append(one)

                        questions = [
                                inquirer.Checkbox('NFT',
                                                message="Select NFT to list",
                                                choices=dList,
                                                ),
                                ]

                        answers = inquirer.prompt(questions)
                        selected = answers['NFT']
                        cprint('You Selected {}'.format(selected), 'green')

                        for i in range(len(answers['NFT'])):
                            selectedTokenName = selected[i]['Name']
                            mint_address = selected[i]['tokenAddress']

                            print('\n')

                            SelectedTokenName.append(selected[i]['Name'])
                            mint_address1.append(selected[i]['tokenAddress'])

                        with open('pub.txt', 'r') as f2:
                            wallets = f2.readlines()
                        f2.close()
                        
                        wallet = [s.rstrip() for s in wallets]

                        questions = [inquirer.Checkbox(
                                            'Wallets',
                                            message="Press Space To Select A Wallet To Send NFTs To?",
                                            choices=wallet,
                                            ),
                        ]
                        answers = inquirer.prompt(questions)

                        selectedWallet = answers['Wallets']

                        to_address = str(selectedWallet).replace('[', '')
                        to_address = str(selectedWallet).replace(']', '')
                        to_address = str(selectedWallet).replace('\'', '')
                        #----------------------------------------------------
                        to_address = to_address.replace('[', '')
                        to_address = to_address.replace(']', '')
                        to_address = to_address.replace('\'', '')
                        cprint('Selected Wallet {}'.format(to_address), 'green')
                        #----------------------------------------------------

                        for mint_address in mint_address1:
                            mint_address.replace('[', '')
                            mint_address.replace(']', '')
                            mint_address.replace('\'', '')

                            input('Press Enter to continue...')
                            cprint('\nSending {} to {}\n'.format(mint_address, to_address), 'green')
                            def transfer_nft(privkey: str, mint_address: str, to_address: str):

                                OPTS = TxOpts(skip_preflight=True, skip_confirmation=True)
                                
                                payer = Keypair.from_secret_key(b58decode(privkey))
                                
                                transaction = Transaction(fee_payer=payer.public_key)

                                try:
                                        
                                    transaction.add(
                                        TransactionInstruction(
                                            keys=[
                                                AccountMeta(pubkey=PublicKey(to_address),is_signer=False, is_writable=False)
                                            ],
                                            program_id=PublicKey(NFT_TRANSFER_PROGRAM),
                                            data=b58decode("11111111111111111111111111111111")
                                        )
                                    )

                                    token_ata = get_associated_token_address(owner=PublicKey(to_address), mint=PublicKey(mint_address))

                                    check_account = client.get_account_info(token_ata)

                                    if not check_account['result']['value']:
                                        transaction.add(
                                            create_associated_token_account(
                                                payer=payer.public_key,
                                                owner=PublicKey(to_address),
                                                mint=PublicKey(mint_address)
                                            )
                                        )

                                    tokenholder = PublicKey(client.get_token_largest_accounts(mint_address)['result']['value'][0]['address'])

                                    transaction.add(
                                        transfer_checked(
                                            TransferCheckedParams(
                                                amount=1,
                                                dest=token_ata,
                                                source=tokenholder,
                                                owner=payer.public_key,
                                                decimals=0,
                                                program_id=PublicKey(TOKEN_PROGRAM_ID),
                                                mint=PublicKey(mint_address),
                                                signers=[]
                                            )
                                        ))
                                    
                                    tx_hash = client.send_transaction(transaction, payer, opts=OPTS)["result"]

                                    print("https://solscan.io/tx/{}".format(tx_hash))
                                
                                except:
                                    
                                    print('Error: Transaction Failed')

                            transfer_nft(privkey, mint_address, to_address)
                    NFTSender()

                if user_choice == 'Balance Fetcher':
                    def Balance():
                        from solathon.core.instructions import transfer
                        from solathon import Client, Transaction, PublicKey, Keypair
                        from texttable import Texttable

                        cprint(figlet_format('Starting Balance Fetcher', font='term'),
                                'green', attrs=['bold'])

                        with open('pub.txt', 'r') as f:
                            wallet = f.readlines()
                        f.close()

                        for i in range(len(wallet)):
                            wallet[i] = wallet[i].strip()

                            client = Client("https://api.mainnet-beta.solana.com")
                            public_key = PublicKey(wallet[i])
                            balance = client.get_balance(public_key)

                            lamportb = balance['result']['value']
                            SOLbalance = (lamportb / 1000000000)
                            balan = str(SOLbalance) + ' SOL'

                            table = Texttable()
                            table.add_row(['Wallet', 'Balance']),
                            table.add_row([wallet[i], balan]),

                            table.set_cols_align(['l', 'r'])
                            table.set_cols_valign(["t", "m"])

                            print(table.draw())
                            print()
                            
                    Balance()

                if user_choice == 'Distribute SOL':
                    def SendSOL():

                        from solathon.core.instructions import transfer
                        from solathon import Client, Transaction, PublicKey, Keypair

                        cprint(figlet_format('Starting SOL Transferer', font='term'),
                                'green', attrs=['bold'])

                        senderwallet = main_wallet

                        client = Client("https://api.mainnet-beta.solana.com")
                        sender = Keypair().from_private_key(privkey)
                        

                        with open('pub.txt', 'r') as f2:
                            wallets = f2.readlines()
                        f2.close()
                        
                        wallet = [s.rstrip() for s in wallets]

                        questions = [inquirer.Checkbox(
                                            'Wallets',
                                            message="Press Space To Select A Wallet To Send SOL To?",
                                            choices=wallet,
                                            ),
                        ]
                        answers = inquirer.prompt(questions)

                        pubkey = str(answers['Wallets'])
                        pubkey = pubkey.replace('[', '')
                        pubkey = pubkey.replace(']', '')
                        pubkey = pubkey.replace('\'', '')

                        receiver = PublicKey(pubkey)
                        print(receiver)

                        LetsSendThisMuch = input('Enter Amount of SOL to Transfer: ')
                        howmuch = (int(float(LetsSendThisMuch)* 10000))
                        amount = (howmuch * 100000)

                        instruction = transfer(
                            from_public_key=sender.public_key,
                            to_public_key=receiver, 
                            lamports=amount
                        )

                        transaction = Transaction(instructions=[instruction], signers=[sender])
                        result = client.send_transaction(transaction)

                        RawTX = result['result']
                        tx = 'https://solscan.io/tx/' + RawTX

                        print(tx)

                        # Webhook Stuff

                        cprint('\nSending {} SOL from {} to {} with TX URL of {}'.format(LetsSendThisMuch, senderwallet, pubkey, tx), 'cyan')
                        time.sleep(2)

                        from discord_webhook import DiscordWebhook, DiscordEmbed

                        with open('webhook.txt', 'r') as f3:
                            webhookurl = f3.read().rstrip()

                        webhook = DiscordWebhook(url=webhookurl)

                        # create embed object for webhook
                        embed = DiscordEmbed(title='CozyTools', description='Solana Distributer Success', color='65280')

                        # set author
                        embed.set_author(name='CozyTools', url='https://cozy-tools.hyper.co/dashboard', icon_url='https://cdn.discordapp.com/attachments/984587141206130802/993318700155404359/cozylogo.png')

                        # set timestamp (default is now)
                        embed.set_timestamp()

                        # add fields to embed
                        embed.add_embed_field(name='Sender', value=str(senderwallet))
                        embed.add_embed_field(name='Reciever', value=str(receiver))
                        embed.add_embed_field(name='Amount', value=str(LetsSendThisMuch) + ' SOL')
                        embed.add_embed_field(name='TX', value='https://solscan.io/tx/' + RawTX)
                        
                        # set footer
                        embed.set_footer(text='CozyTools Success', icon_url='https://cdn.discordapp.com/attachments/984587141206130802/993318700155404359/cozylogo.png')

                        # add embed object to webhook
                        webhook.add_embed(embed)

                        response = webhook.execute()

                        time.sleep(4)

                    SendSOL()

            if userchoice == 'Magic Eden Historical Data':
                def HistoricalData():
                    cprint(figlet_format('\nStarting Historical Data Fetcher', font='term'),
                            'green', attrs=['bold'])
                    time.sleep(2)


                    cprint('Checking {} \n'.format(main_wallet), 'green')

                    scraper = cloudscraper.create_scraper(
                        browser={
                            'browser': 'firefox',
                            'platform': 'windows',
                            'mobile': False
                        }
                    )

                    site_req = scraper.get('https://api-mainnet.magiceden.io/rpc/getNFTsByOwner/' + main_wallet).text

                    html = site_req

                    soup = bs4.BeautifulSoup(html,'html.parser')
                    site_json=json.loads(soup.text)
                    list = []
                    NFTs = ([d.get('collectionName') for d in site_json['results'] if d.get('collectionName')])
                    list = NFTs
                    questions = [
                        inquirer.List('NFTs',
                                    message="Select Collection To View Histrocial Volume For",
                                    choices=list,
                                ),
                        ]
                    answers = inquirer.prompt(questions)
                    NFTCollection = answers['NFTs']

                    req2 = scraper.get("https://api-mainnet.magiceden.io/rpc/getAggregatedCollectionMetricsBySymbol?edge_cache=true&symbols={}".format(NFTCollection))

                    resp_data = req2.text
                    history = json.loads(resp_data)
                    valueAT = (history['results'][0]['txVolume'])

                    VolumeAT = (valueAT['valueAT'])
                    Volume1h = (valueAT['value1h'])
                    Volume1d = (valueAT['value1d'])
                    Volume7d = (valueAT['value7d'])
                    Volume30d = (valueAT['value30d'])
                    print("The 1 Hour Volume of {} is {} SOL".format(NFTCollection,Volume1h))
                    print("The 1 Day Volume of {} is {} SOL".format(NFTCollection,Volume1d))
                    print("The 7 Day Volume of {} is {} SOL".format(NFTCollection,Volume7d))
                    print("The 30 Day Volume of {} is {} SOL".format(NFTCollection,Volume30d))
                    print("The All Time Volume of {} is {} SOL".format(NFTCollection,VolumeAT))

                    y = [Volume1h,Volume1d,Volume7d,Volume30d,VolumeAT]
                    x = ['1 Hour','1 Day','7 Day','30 Day','All Time']

                    plt.plot(x, y)

                    plt.xlabel('Timeframe')
                    plt.ylabel('Volume')
                    plt.title('Volume of {}'.format(NFTCollection))
                    plt.show()

                HistoricalData()

            if userchoice == 'RPC Ping Test':

                def Ping():
                    import subprocess

                    cprint('\nStarting RPC Ping Test', 'green'),

                    with open('config.json', 'r') as key_file:
                        data = json.loads(key_file.read())
                        rpc = data['rpc']

                    validrpc = rpc.replace('https://', '')

                    host = validrpc
                    print("\n")
                    ping = subprocess.getoutput(f"ping {host}")
                    print(ping)
                    time.sleep(5)
                Ping()

            if userchoice == 'Exit':
                print("Goodbye!")
                sys.exit()
    else:
        cprint('License Error, Please Reset Or Try Again', 'red')
CozyTools()
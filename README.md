# Furaffinity Bruteforcer

Brute force attack designed specifically for the site furaffinity.

## How does it work?
It uses selenium to create a bot that will visit furaffinity under a random useragent and a random proxy and attempts to login using a generated password, it bypasses recaptchas sent by the site using a [chrome extension](https://chromewebstore.google.com/detail/captcha-solver-auto-hcapt/hlifkpholllijblknnmbfagnkjneagid?hl=en) and on success will display the password that successfully was recognized by the site.

## Installation
You need to first have latest python and pip version installed.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install libraries specified in requirements.txt.

```bash
pip install -r requirements.txt
```

## Usage
<img src=""> </img>
You execute brute.py by opening command prompt and typing
```
python brute.py
```
You'll greeted by an input for target, amount of threads, proxy file, tested passwords file, dictionary file and buttons run or stop. Target is the username of your target, threads is the amount of processes you want to run at the same time, proxy file are custom proxies, tested passwords are passwords the brute force will avoid using, dictionary file are passwords will run first before generating different passwords, the run button will initiate the bruteforce attack and the stop button will stop all the bruteforce attack instances. 
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Support

# XMR Donations
<img src="https://cryptologos.cc/logos/monero-xmr-logo.png?v=032" alt="XMR" width="200"/>

If you'd like to support my work with Monero (XMR), you can send your donations to the following address:

4BEHHRhHMrYC3yQ5Xv71eDXeiUpshLXMHC7JWYrotAreXMknEjmZU38HMFCXUM43YoFya7qBD3Q5R61a13NnyA35Lst38NY

# Bitcoin Donations
<img src="https://cryptologos.cc/logos/bitcoin-btc-logo.png?v=032" alt="BTC" width="200"/>

For those who prefer to use Bitcoin (BTC) for donations, you can send your contributions to the following address:

bc1qn0vyhvw53825kgtuyx6kjuhs6zt3dq89j8vgz3

# Litecoin Donations
<img src="https://cryptologos.cc/logos/litecoin-ltc-logo.png?v=032" alt="LTC" width="200"/>

For those who prefer to use Litecoin (LTC) for donations, you can send your contributions to the following address:

LeYFT19HmytwLyMdvF6K7bg2VVyZzNERww

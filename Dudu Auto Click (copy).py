import sys
import os
import asyncio
import os
import subprocess
import platform
import requests
from qasync import QEventLoop
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, QCheckBox
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QIcon
import pyautogui
import random
from playwright.async_api import async_playwright


class AutoClicker(QWidget):
    def __init__(self):
        super().__init__()

        if not self.is_setup_done():
            self.check_and_install_browsers()
            self.mark_setup_done()

        self.initUI()
        self.running = False
        self.click_thread = None
        self.timer_task = None
        self.old_pos = None

    def is_setup_done(self):
        """Controlla se il setup è già stato completato."""
        return os.path.exists('setup_done.txt')

    def mark_setup_done(self):
        """Crea un file per indicare che il setup è stato completato."""
        with open('setup_done.txt', 'w') as f:
            f.write('Setup completato')

    def check_and_install_browsers(self):
        def download_file(url, file_name):
            response = requests.get(url, stream=True)
            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

        def install_chrome():
            if platform.system() == 'Windows':
                chrome_url = "https://dl.google.com/chrome/install/latest/chrome_installer.exe"
                chrome_installer = "chrome_installer.exe"
                download_file(chrome_url, chrome_installer)
                subprocess.run([chrome_installer], shell=True)
            elif platform.system() == 'Darwin':  # macOS
                chrome_url = "https://dl.google.com/chrome/mac/stable/GGRO/googlechrome.dmg"
                chrome_installer = "googlechrome.dmg"
                download_file(chrome_url, chrome_installer)
                subprocess.run(["hdiutil", "attach", chrome_installer])
                subprocess.run(["cp", "-r", "/Volumes/Google Chrome/Google Chrome.app", "/Applications/"])
                subprocess.run(["hdiutil", "detach", "/Volumes/Google Chrome"])
            elif platform.system() == 'Linux':
                subprocess.run(["sudo", "apt", "install", "google-chrome-stable"], shell=True)
            else:
                print("Sistema operativo non supportato per l'installazione di Chrome.")

        def install_firefox():
            if platform.system() == 'Windows':
                firefox_url = "https://download.mozilla.org/?product=firefox-latest&os=win&lang=en-US"
                firefox_installer = "firefox_installer.exe"
                download_file(firefox_url, firefox_installer)
                subprocess.run([firefox_installer], shell=True)
            elif platform.system() == 'Darwin':  # macOS
                firefox_url = "https://download.mozilla.org/?product=firefox-latest&os=osx&lang=en-US"
                firefox_installer = "firefox.dmg"
                download_file(firefox_url, firefox_installer)
                subprocess.run(["hdiutil", "attach", firefox_installer])
                subprocess.run(["cp", "-r", "/Volumes/Firefox/Firefox.app", "/Applications/"])
                subprocess.run(["hdiutil", "detach", "/Volumes/Firefox"])
            elif platform.system() == 'Linux':
                subprocess.run(["sudo", "apt", "install", "firefox"], shell=True)
            else:
                print("Sistema operativo non supportato per l'installazione di Firefox.")

        def check_chrome():
            try:
                if platform.system() == 'Windows':
                    chrome_path = os.path.join(os.environ['PROGRAMFILES'], 'Google', 'Chrome', 'Application', 'chrome.exe')
                    if not os.path.exists(chrome_path):
                        chrome_path = os.path.join(os.environ['PROGRAMFILES(X86)'], 'Google', 'Chrome', 'Application', 'chrome.exe')
                    if os.path.exists(chrome_path):
                        return True
                elif platform.system() == 'Darwin':
                    return os.path.exists("/Applications/Google Chrome.app")
                elif platform.system() == 'Linux':
                    result = subprocess.run(['which', 'google-chrome'], stdout=subprocess.PIPE)
                    return bool(result.stdout)
            except Exception as e:
                print(f"Errore durante la verifica di Chrome: {e}")
            return False

        def check_firefox():
            try:
                if platform.system() == 'Windows':
                    firefox_path = os.path.join(os.environ['PROGRAMFILES'], 'Mozilla Firefox', 'firefox.exe')
                    if not os.path.exists(firefox_path):
                        firefox_path = os.path.join(os.environ['PROGRAMFILES(X86)'], 'Mozilla Firefox', 'firefox.exe')
                    if os.path.exists(firefox_path):
                        return True
                elif platform.system() == 'Darwin':
                    return os.path.exists("/Applications/Firefox.app")
                elif platform.system() == 'Linux':
                    result = subprocess.run(['which', 'firefox'], stdout=subprocess.PIPE)
                    return bool(result.stdout)
            except Exception as e:
                print(f"Errore durante la verifica di Firefox: {e}")
            return False

        chrome_installed = check_chrome()
        firefox_installed = check_firefox()

        if not chrome_installed:
            print("Chrome non è installato. Sto installando l'ultima versione.")
            install_chrome()
        else:
            print("Chrome è già installato. Verifico la presenza di aggiornamenti.")
            if platform.system() == 'Windows':
                subprocess.run(['winget', 'upgrade', '--id=Google.Chrome'], shell=True)
            elif platform.system() == 'Darwin':
                subprocess.run(['brew', 'upgrade', '--cask', 'google-chrome'], shell=True)
            elif platform.system() == 'Linux':
                subprocess.run(['sudo', 'apt', 'update', 'google-chrome-stable'], shell=True)

        if not firefox_installed:
            print("Firefox non è installato. Sto installando l'ultima versione.")
            install_firefox()
        else:
            print("Firefox è già installato. Verifico la presenza di aggiornamenti.")
            if platform.system() == 'Windows':
                subprocess.run(['winget', 'upgrade', '--id=Mozilla.Firefox'], shell=True)
            elif platform.system() == 'Darwin':
                subprocess.run(['brew', 'upgrade', '--cask', 'firefox'], shell=True)
            elif platform.system() == 'Linux':
                subprocess.run(['sudo', 'apt', 'update', 'firefox'], shell=True)

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(300, 400)

        self.setWindowIcon(QIcon("dudu_bessmertnyy.ico"))


        self.method_checkbox = QCheckBox('Usa metodo timerpw', self)
        self.method_checkbox.stateChanged.connect(self.toggle_method)

        self.auction_id_input = QLineEdit(self)
        self.auction_id_input.setPlaceholderText('Inserisci ID asta')

        self.freq_label = QLabel('Frequenza:', self)
        self.freq_input = QLineEdit(self)
        self.freq_input.setPlaceholderText('Inserisci frequenza (ms, s, m, h)')

        self.button_label = QLabel('Pulsante del mouse:', self)
        self.button_select = QComboBox(self)
        self.button_select.addItems(['Sinistro', 'Destro'])

        self.click_type_label = QLabel('Tipo di click:', self)
        self.click_type_select = QComboBox(self)
        self.click_type_select.addItems(['Singolo', 'Doppio'])

        self.click_count_label = QLabel('Numero di click:', self)
        self.click_count_select = QComboBox(self)
        self.click_count_select.addItems(['1', '10', 'Infinito'])

        self.start_button = QPushButton('Avvia', self)
        self.start_button.clicked.connect(self.start_clicking)

        self.stop_button = QPushButton('Ferma', self)
        self.stop_button.clicked.connect(self.stop_clicking)

        self.minimize_button = QPushButton('_', self)
        self.minimize_button.clicked.connect(self.showMinimized)

        self.close_button = QPushButton('X', self)
        self.close_button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.method_checkbox)
        layout.addWidget(self.auction_id_input)
        layout.addWidget(self.freq_label)
        layout.addWidget(self.freq_input)
        layout.addWidget(self.button_label)
        layout.addWidget(self.button_select)
        layout.addWidget(self.click_type_label)
        layout.addWidget(self.click_type_select)
        layout.addWidget(self.click_count_label)
        layout.addWidget(self.click_count_select)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.minimize_button)
        control_layout.addWidget(self.close_button)
        layout.addLayout(control_layout)

        self.setLayout(layout)

    def toggle_method(self, state):
        if state == Qt.Checked:
            self.freq_input.setDisabled(True)
        else:
            self.freq_input.setDisabled(False)

    def start_clicking(self):
        if self.method_checkbox.isChecked():
            auction_id = self.auction_id_input.text()

            if auction_id:
                loop = QEventLoop()  
                asyncio.set_event_loop(loop)

                self.timer_task = QTimer(self)
                self.timer_task.setSingleShot(True)
                self.timer_task.timeout.connect(lambda: asyncio.ensure_future(self.run_both_browsers(auction_id)))
                self.timer_task.start(0)

        else:
            if self.running:
                return

            freq = self.freq_input.text()
            if freq.endswith('ms'):
                self.interval = float(freq[:-2]) / 1000
            elif freq.endswith('s'):
                self.interval = float(freq[:-1])
            elif freq.endswith('m'):
                self.interval = float(freq[:-1]) * 60
            elif freq.endswith('h'):
                self.interval = float(freq[:-1]) * 3600
            else:
                self.interval = float(freq)

            self.mouse_button = 'left' if self.button_select.currentText() == 'Sinistro' else 'right'
            self.click_type = 'single' if self.click_type_select.currentText() == 'Singolo' else 'double'

            selected_count = self.click_count_select.currentText()
            if selected_count == '1':
                self.click_count = 1
            elif selected_count == '10':
                self.click_count = 10
            else:
                self.click_count = -1

            self.running = True
            self.click_thread = threading.Thread(target=self.click_loop)
            self.click_thread.start()

    def click_loop(self):
        count = 0
        while self.running:
            if self.click_count != -1 and count >= self.click_count:
                break

            x = random.randint(1001, 1150)
            y = random.randint(480, 520)
            pyautogui.click(x, y, button=self.mouse_button, clicks=2 if self.click_type == 'double' else 1)

            count += 1
            time.sleep(self.interval)

        self.running = False

    def stop_clicking(self):
        self.running = False

        if self.click_thread:
            self.click_thread.join()
            self.click_thread = None

        if self.timer_task:
            self.timer_task.cancel()
            self.timer_task = None

        if hasattr(self, 'browser'):
            asyncio.ensure_future(self.browser.close())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    async def monitor_auction_chrome(self, auction_id):
        chrome_path = self.get_browser_path("chrome")

        auction_url = f"https://it.bidoo.com/auction.php?a={auction_id}"
        async with async_playwright() as p:
            browser = await p.chromium.launch(executable_path=chrome_path, headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                await page.goto(auction_url)
                print(f"Aperta l'asta {auction_id} su Chrome")

                await self.monitor_and_click(page, auction_id)

            except Exception as e:
                print(f"Errore durante il monitoraggio dell'asta su Chrome: {e}")
            finally:
                await browser.close()

    async def monitor_auction_firefox(self, auction_id):
        firefox_path = self.get_browser_path("firefox")

        auction_url = f"https://it.bidoo.com/auction.php?a={auction_id}"
        async with async_playwright() as p:
            browser = await p.firefox.launch(executable_path=firefox_path, headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                await page.goto(auction_url)
                print(f"Aperta l'asta {auction_id} su Firefox")

                await self.monitor_and_click(page, auction_id)

            except Exception as e:
                print(f"Errore durante il monitoraggio dell'asta su Firefox: {e}")
            finally:
                await browser.close()

    async def run_both_browsers(self, auction_id):
        await asyncio.gather(
            self.monitor_auction_chrome(auction_id),
            self.monitor_auction_firefox(auction_id)
        )

    async def monitor_and_click(self, page, auction_id):
        selected_count = self.click_count_select.currentText()

        click_count = 1 if selected_count == '1' else 10 if selected_count == '10' else float('inf')

        clicks_done = 0 

        while clicks_done < click_count:
            timer_selector = f"#DA{auction_id} > div.col-lg-5.col-md-5.col-sm-6.col-xs-12.action_auction > section.auction-action-container > div > div:nth-child(2) > section > div.auction-action-countdown > div > div"
            timer = await page.query_selector(timer_selector)

            if not timer:
                print("Timer non trovato. Uscita.")
                break

            timer_value = await timer.inner_text()

            print(f"Timer corrente: {timer_value}")

            if timer_value.strip() == "1":
                print("Timer a 1 secondo, eseguo il click.")

                await asyncio.sleep(0.5)

                x = random.randint(1001, 1150)
                y = random.randint(480, 520)
                pyautogui.click(x, y, button='left')

                clicks_done += 1
                print(f"Click eseguito alle coordinate: {x}, {y}, Click numero: {clicks_done}")

                if clicks_done >= click_count:
                    print("Numero massimo di click raggiunto.")
                    break

            await asyncio.sleep(0.1)

    def get_browser_path(self, browser_name):
        config_file = "config.txt"
        if os.path.exists(config_file):
            with open(config_file, "r") as file:
                lines = file.readlines()
                for line in lines:
                    if browser_name in line:
                        browser_path = line.split('=')[1].strip()
                        if os.path.exists(browser_path):
                            return browser_path
        raise FileNotFoundError(f"Il percorso di {browser_name} non è configurato.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    autoclicker = AutoClicker()
    autoclicker.show()
    with loop:
        loop.run_forever()

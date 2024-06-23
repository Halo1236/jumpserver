import os
import re
import shutil
import winreg
import tempfile
from urllib.parse import urlparse

from pywinauto import Application

from common import wait_pid, BaseApplication

_mode = 'safe'
_default_path = r'C:\Program Files\Chrome\chrome92\chrome.exe'
_default_params = ('--test-type --ignore-certificate-errors --disable-infobars --ignore-ssl-errors '
                   '-–disable-background-networking --allow-running-insecure-content --no-default-browser-check '
                   '--start-maximized')
_default_user_data_dir = ''
_default_url_block = 'enable'

with open('Chrome_Path.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    print(lines)
    if len(lines) >= 2:
        _mode = lines[0].strip()
        _default_path = lines[1].strip()
        _default_params = lines[2].strip()
        _default_url_block = lines[3].strip()
        _default_user_data_dir = lines[4].strip()


def load_extensions():
    extensions_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extensions')
    extension_names = os.listdir(extensions_root)
    extension_paths = [os.path.join(extensions_root, name) for name in extension_names]
    return extension_paths


class AppletApplication(BaseApplication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mode = _mode
        self.path = _default_path
        self.params = _default_params
        self.username = self.account.username
        self.password = self.account.secret
        self.host = self.asset.address
        self.pid = None
        self._tmp_user_dir = tempfile.TemporaryDirectory()
        self.default_user_data_dir = _default_user_data_dir
        self.default_url_block = _default_url_block

        addrs = re.split(r'[,，]+', self.asset.address)
        user_token_param = ''
        if self.username:
            sep = '&' if '?' in addrs[0] else '?'
            user_token_param = sep + self.username + '='
            if self.password:
                user_token_param += self.password
        self.host = addrs[0] + user_token_param
        self.allow_address = addrs

    def _get_exec_params(self):
        if not os.path.exists(self._tmp_user_dir.name):
            if self.default_user_data_dir:
                shutil.copytree(self.default_user_data_dir, self._tmp_user_dir.name)
        return f'{self.host} {self.params} --user-data-dir={self._tmp_user_dir.name}'

    def edit_regedit(self):
        self.cleanup_regedit()
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r'Software\Policies\Google\Chrome')
            if self.mode != 'dev':
                winreg.SetValueEx(key, 'DeveloperToolsAvailability', 0, winreg.REG_DWORD, 2)
            winreg.SetValueEx(key, 'PasswordManagerEnabled', 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, 'PrintingEnabled', 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, 'DownloadRestrictions', 0, winreg.REG_DWORD, 3)
            winreg.SetValueEx(key, 'PromptForDownloadLocation', 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, 'DefaultPopupsSetting', 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, 'AllowFileSelectionDialogs', 0, winreg.REG_DWORD, 0)

            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r'Software\Policies\Google\Chrome\URLAllowlist')
            for i, adr in enumerate(self.allow_address):
                winreg.SetValueEx(key, str(i + 1), 0, winreg.REG_SZ, urlparse(adr).netloc)

            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r'Software\Policies\Google\Chrome\URLBlocklist')
            winreg.SetValueEx(key, '1', 0, winreg.REG_SZ, 'file://*')
            winreg.SetValueEx(key, '2', 0, winreg.REG_SZ, 'view-source:https://*')
            winreg.SetValueEx(key, '3', 0, winreg.REG_SZ, 'view-source:http://*')

            winreg.SetValueEx(key, '6', 0, winreg.REG_SZ, 'chrome://downloads')
            winreg.SetValueEx(key, '7', 0, winreg.REG_SZ, 'chrome://bookmarks')
            winreg.SetValueEx(key, '8', 0, winreg.REG_SZ, 'chrome://settings/importData')
            if self.default_url_block != 'disable':
                winreg.SetValueEx(key, '4', 0, winreg.REG_SZ, 'https://*')
                winreg.SetValueEx(key, '5', 0, winreg.REG_SZ, 'http://*')

            if self.mode != 'dev':
                winreg.SetValueEx(key, '9', 0, winreg.REG_SZ, 'devtools://*')
        except Exception as err:
            print('edit_regedit error: %s' % err)

    def cleanup_regedit(self):
        try:
            self._tmp_user_dir.cleanup()
            winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, r'Software\Policies\Google\Chrome\URLAllowlist')
            winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, r'Software\Policies\Google\Chrome\URLBlocklist')
            winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, r'Software\Policies\Google\Chrome')
        except Exception as err:
            print('cleanup error: %s' % err)

    def run(self):
        self.edit_regedit()
        app = Application(backend='uia')
        params = self._get_exec_params()
        app.start(r'%s %s' % (self.path, params))
        self.pid = app.process

    def wait(self):
        wait_pid(self.pid)
        self.cleanup_regedit()

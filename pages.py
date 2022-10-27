from seleniumpagefactory.Pagefactory import PageFactory
from bs4 import BeautifulSoup
import pandas as pd
import time

class LoginPage(PageFactory):
    def __init__(self, driver):
        self.driver = driver

    locators = {
        'input_user': ('ID', "usrname"),
        'input_password': ('ID', 'txtPwd'),
        'btn_login': ('ID', 'btnLogin')
    }

    def login(self, username, password):
        self.input_user.set_text(username)
        self.input_password.set_text(password)
        self.btn_login.click()

#======================================================

class MainPage(PageFactory):
    def __init__(self, driver):
        self.driver = driver

    locators = {
        'informations_tab': ('LINK_TEXT', "Informações"),
        'btn_logout': ('LINK_TEXT', "Sair"),
        'btn_confirm_logout': ('ID', "yesbtn")
    }

    def click_informations_tab(self):
        self.informations_tab.click()

    def logout(self):
        self.btn_logout.click()
        self.btn_confirm_logout.click()
        time.sleep(2)

#======================================================

class InformationsPage(PageFactory):
    def __init__(self, driver):
        self.driver = driver

    locators = {
        'stats_menu': ('LINK_TEXT', "Estatística")
    }

    def click_stats_menu(self):
        self.stats_menu.click()

#======================================================

class StatsPage(PageFactory):
    def __init__(self, driver):
        self.driver = driver

    locators = {
        'stats_data_table': ('ID', "dataTable")
    }

    def get_current_month_consumption(self):
        table_content = "NaNTB"
        while "NaNTB" in table_content:
            stats_table = self.stats_data_table
            table_content = stats_table.get_attribute('innerHTML')
            time.sleep(1)

        soup = BeautifulSoup(table_content, 'html.parser')
        table = soup.find(name='table')
        consumption = pd.read_html(str(table))[0].head(5).iloc[1]['Dados transferidos']
        return int(float(consumption.replace("GB", "")))
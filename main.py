from jproperties import Properties
from driver_factory import FirefoxDriver
from pages import *
from json_reader import JsonReader
import date_utils

#============================================================================
# load properties file
props = Properties()
with open('_.properties', 'rb') as config_file:
    props.load(config_file)

URL = props.get("URL").data
USERNAME = props.get("USERNAME").data
PASSWORD = props.get("PASSWORD").data
TIMEOUT = int(props.get("TIMEOUT").data)

#============================================================================
# get the current month consumption
driver = FirefoxDriver(TIMEOUT)
driver.get(URL)

LoginPage(driver).login(USERNAME, PASSWORD)
MainPage(driver).click_informations_tab()
InformationsPage(driver).click_stats_menu()
current_month_consumption = StatsPage(
    driver).get_current_month_consumption()
MainPage(driver).logout()
driver.close()

#============================================================================
# load json file
json = JsonReader("consumption.json")
month_consumption_when_reset = json.get_prop_value('monthConsumptionWhenReset')
month_consumption_when_last_day = json.get_prop_value('monthConsumptionWhenLastDay')
real_consumption_when_last_day_of_month = json.get_prop_value('realConsumptionWhenLastDayOfMonth')

#============================================================================
# calculate the consumption values
today_day = date_utils.get_today_day()
last_day_of_current_month = date_utils.get_last_day_of_current_month()
consumption_reset_day = int(props.get("CONSUMPTION_RESET_DAY").data)

if (today_day == consumption_reset_day):
    month_consumption_when_reset = current_month_consumption
    real_consumption = 0

if (today_day == last_day_of_current_month):
    month_consumption_when_last_day = current_month_consumption
    real_consumption = month_consumption_when_last_day - month_consumption_when_reset
    real_consumption_when_last_day_of_month = real_consumption
    
if ((today_day > consumption_reset_day) and (today_day < last_day_of_current_month)):
    real_consumption = current_month_consumption - month_consumption_when_reset

if (today_day < consumption_reset_day):
    real_consumption = current_month_consumption + real_consumption_when_last_day_of_month

#============================================================================
# update json properties
if ((today_day == consumption_reset_day) or (today_day == last_day_of_current_month)):
    json.set_prop_value('monthConsumptionWhenReset', month_consumption_when_reset)
    json.set_prop_value('monthConsumptionWhenLastDay', month_consumption_when_last_day)
    json.set_prop_value('realConsumptionWhenLastDayOfMonth', real_consumption_when_last_day_of_month)

#============================================================================
# calculate the recommended consumption per day
if today_day < consumption_reset_day:
    remaining_days = consumption_reset_day - today_day  

if today_day >= consumption_reset_day:
    remaining_days = (last_day_of_current_month - today_day) + consumption_reset_day

pkg_size = int(props.get("PKG_SIZE").data)
available_pkg = pkg_size - real_consumption
recommended_consumption_per_day = round(float(available_pkg / remaining_days), 2)

#============================================================================
# display values 
print (f"available_pkg = ", available_pkg, "GB")
print (f"recommended_consumption_per_day = ", recommended_consumption_per_day, "GB")
print (f"consumption_reset_day = ", consumption_reset_day)
print (f"pkg_size = ", pkg_size, "GB")
print (f"real_consumption = ", real_consumption, "GB")
print (f"real_consumption_when_last_day_of_month = ", real_consumption_when_last_day_of_month, "GB")
print (f"monthConsumptionWhenReset = ", month_consumption_when_reset, "GB")
print (f"monthConsumptionWhenLastDay = ", month_consumption_when_last_day, "GB")
print (f"realConsumptionWhenLastDayOfMonth = ", real_consumption_when_last_day_of_month, "GB")




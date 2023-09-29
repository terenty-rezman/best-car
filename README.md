# great car

## uart setup
on stm32 use usart2 in async mode with default settings

### uart interrupt receive
https://controllerstech.com/uart-receive-in-stm32/

### raspberry pinout uart
https://pinout.xyz/pinout/uart#

we use pins 8 & 10 & common ground !

connect stm32 RX (PA3) to raspbery TX (pin 8 GPIO 14) <br>
stm32 TX (PA2) to raspbery RX(pin 10 GPIO 15)

disable bluethooth & enable uart on raspbery <br>
https://dzen.ru/media/unpromresdept/vkliuchenie-interfeisov-uart-na-gpio-razeme-raspberry-pi-4-62ea15e6784eab257831e695

then use `minicom -D /dev/ttyAMA0` to connect to stm32 via uart

### listen on port 80
https://stackoverflow.com/questions/413807/is-there-a-way-for-non-root-processes-to-bind-to-privileged-ports-on-linux

### raspberry as wifi server

/etc/hostapd/hostapd.conf
```
country_code=RU

interface=wlan1
driver=nl80211
hw_mode=g
channel=9
wmm_enabled=1
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
ssid=best
wpa_passphrase=carcarcar

logger_syslog=-1
logger_syslog_level=0
logger_stdout=-1
logger_stdout_level=0
```

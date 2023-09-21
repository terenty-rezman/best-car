# great car

# uart setup
on stm32 use usart2 in async mode with default settings

### uart interrupt receive
https://controllerstech.com/uart-receive-in-stm32/

### raspberry pinout uart
https://pinout.xyz/pinout/uart#

we use pins 8 & 10 & common ground !

connect stm32 RX (PA3) to raspbery TX (pin 8 GPIO 14) <br>
stm32 TX (PA2) to raspbery RX(pin 10 GPIO 15)

disable bluethooth & enable uart on raspbery
https://dzen.ru/media/unpromresdept/vkliuchenie-interfeisov-uart-na-gpio-razeme-raspberry-pi-4-62ea15e6784eab257831e695

then use `minicom -D /dev/ttyAMA0` to connect to stm32 via uart


# Tricorder-RaspberryPi
The most advanced Tricorder device from Star Trek yet implemented. If you ever ask
yourself “is the sky more red at sunset?”, “how clean is my air?”, “how bright is my TV?”, “what flower is this?”, “how hot is this object?”, “how busy are the airwaves?”, and seek the answer in real-time, beautifully visualized 8-bit color, then this is the device for you.
# Docs
https://tricorder-raspberrypi.readthedocs.io/en/latest/

https://shivamkundan.godaddysites.com/tricorder

# Software 
C (Arduino IDE), \
Python, \
GUI: Pygame, \
Machine Learning: TensorFlow \
Linux commands and tweaks
# Hardware 

## List of parts
This project contains an incredible number of components. Pretty much every environmental sensor that is commercial off-the-shelf. 

Currently, the components use through-hole pins that are soldered manually using a soldering iron. Next step is to acquire Surface Mount Device (SMD) soldering/handling hardware which will drastically reduce the size, weight, and volume of the sensors.

The following is a list of parts used in the design. Note that almost every sensor senses more than one quantity, with some even having separate x,y,z channels for each (such as the IMU). This is why its difficult to say how many sensors are utilized, since the count is dependent upon what one considers to be a sensor. 

| Type                  | Model                      | # |
|-----------------------|----------------------------|---|
| Single board computer | RaspberryPi 4              | 1 |
| Touchscreen display   | Pimoroni Hyperpixel Square | 1 |
| Microprocessor w/ BT  | Adafruit ESP32 Feather V2  | 1 |
| Aux OLEDs             | Generic 128x64                   | 2 |
| Printed Circuit Boards| JLCPCB 2-layer             | 4 |
| Digital sensor boards | Multiple                   | 14|
| Analog sensors        | Multiple                   | 5 |
| Software Defined Radio (SDR) Dongle + 'DVB-T' antenna|  RTL2832U w/ R820T tuner      | 1 |
| I2C active extender & terminator | Adafruit LTC4311| 1 |
| I2C bi-directional isolator| Adafruit ISO1540      | 1 |
| IR-CUT Camera + IR blasters | Generic                   | 1 |
| N-Channel MOSFETs        | Generic                   | 3 |
| Bidirectional voltage shifter  | Generic                   | 2 |
| Buck-boost convertor         | Adafruit Powerboost 1000                   | 1 |
| Battery monitor & fuel gauge         | Adafruit LC709203                   | 1 |
| Lithium-polymer battery (for sensors+MCU)         | Adafruit 2500mAH                   | 1 |
| Battery bank w/ passthrough for raspberry pi  | 10,000mAH  | 1 |
| Neopixels (i.e., RGBW LEDS)  | Adafruit Neopixel Stick 8x-5050 ~4500K  | 1 |
| Magnet for optical/IR camera  | Adafruit magnetic pin back   | 1 |
| Assorted resistors, switches, etc.  | ---       | 1 |

## List of Sensors

After much experimentation and pondering, I try to buy Adafruit's version of parts whenever possible because of their incredible libraries. 

| Sensor                                                               | Type    |
|----------------------------------------------------------------------|---------|
| AS7341 10-channel photo spectrometer                                 | Digital |
| LTR390 UV sensor                                                     | Digital |
| TSL2591 infrared + visible light sensor                              | Digital |
| HTU31D temperature + humidity sensor                                 | Digital |
| BMP388 barometric pressure sensor                                    | Digital |
| SGP30 volatile organic compunds + CO2 sensor                         | Digital |
| MLX90640 IR thermal camera                                           | Digital |
| MAX9814 electret microphone amplifier with auto gain control (noise) | Analog  |
| Modern Devices Rev. C wind speed sensor                              | Analog  |
| BNO055 9-DOF absolute orientation inertial measurement unit          | Digital |
| PMSA003I particulate matter (dust) sensor                            | Digital |
| DFRobot Geiger counter (ionizing radiation)                          | Analog  |
| Garmin LIDAR-Lite V3 optical distance sensor                         | Digital |
| BN880 GPS/GLONASS/Beidou positioning sensor                          | Digital |
| INA260 voltage, current, power sensor                                | Digital |
| Force-Sensitive Resistor (FSR) - Alpha MF02A-N-221-A01 (weight)      | Analog  |
EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "Poop Valve Controller"
Date ""
Rev "0.2 (draft)"
Comp "Robert Ferguson Observatory"
Comment1 "v0.2 changed relay configuration"
Comment2 "v0.1 initial release"
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Connector:Raspberry_Pi_2_3 J?
U 1 1 6329DED7
P 7650 3100
F 0 "J?" H 6950 4450 50  0000 C CNN
F 1 "RaspberryPi" H 7000 4350 50  0000 C CNN
F 2 "" H 7650 3100 50  0001 C CNN
F 3 "https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3bplus_1p0_reduced.pdf" H 7650 3100 50  0001 C CNN
	1    7650 3100
	1    0    0    -1  
$EndComp
$Comp
L Isolator:4N25 U?
U 1 1 632A76B5
P 5400 2050
F 0 "U?" H 5400 2375 50  0000 C CNN
F 1 "4N25" H 5400 2284 50  0000 C CNN
F 2 "Package_DIP:DIP-6_W7.62mm" H 5200 1850 50  0001 L CIN
F 3 "https://www.vishay.com/docs/83725/4n25.pdf" H 5400 2050 50  0001 L CNN
	1    5400 2050
	1    0    0    -1  
$EndComp
$Comp
L Isolator:4N25 U?
U 1 1 632A8434
P 5400 2650
F 0 "U?" H 5400 2975 50  0000 C CNN
F 1 "4N25" H 5400 2884 50  0000 C CNN
F 2 "Package_DIP:DIP-6_W7.62mm" H 5200 2450 50  0001 L CIN
F 3 "https://www.vishay.com/docs/83725/4n25.pdf" H 5400 2650 50  0001 L CNN
	1    5400 2650
	1    0    0    -1  
$EndComp
$Comp
L Device:Battery BT?
U 1 1 632C7943
P 1950 6600
F 0 "BT?" V 2195 6600 50  0000 C CNN
F 1 "12V" V 2104 6600 50  0000 C CNN
F 2 "" V 1950 6660 50  0001 C CNN
F 3 "~" V 1950 6660 50  0001 C CNN
	1    1950 6600
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D?
U 1 1 632DE527
P 4400 2750
F 0 "D?" H 4393 2967 50  0000 C CNN
F 1 "LED" H 4393 2876 50  0000 C CNN
F 2 "" H 4400 2750 50  0001 C CNN
F 3 "~" H 4400 2750 50  0001 C CNN
	1    4400 2750
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D?
U 1 1 632DEC5A
P 4400 2150
F 0 "D?" H 4393 2367 50  0000 C CNN
F 1 "LED" H 4393 2276 50  0000 C CNN
F 2 "" H 4400 2150 50  0001 C CNN
F 3 "~" H 4400 2150 50  0001 C CNN
	1    4400 2150
	-1   0    0    1   
$EndComp
$Comp
L Connector:6P6C J?
U 1 1 632E13D0
P 1100 3500
F 0 "J?" H 1157 4067 50  0000 C CNN
F 1 "Valve" H 1157 3976 50  0000 C CNN
F 2 "" V 1100 3525 50  0001 C CNN
F 3 "~" V 1100 3525 50  0001 C CNN
	1    1100 3500
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_Coaxial_Power J?
U 1 1 632E443C
P 1400 6550
F 0 "J?" V 1625 6500 50  0000 C CNN
F 1 "Charger" V 1534 6500 50  0000 C CNN
F 2 "" H 1400 6500 50  0001 C CNN
F 3 "~" H 1400 6500 50  0001 C CNN
	1    1400 6550
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 632F805C
P 4100 2150
F 0 "R?" V 4300 2150 50  0000 C CNN
F 1 "330" V 4200 2150 50  0000 C CNN
F 2 "" V 4030 2150 50  0001 C CNN
F 3 "~" H 4100 2150 50  0001 C CNN
	1    4100 2150
	0    1    1    0   
$EndComp
$Comp
L Device:R R?
U 1 1 632F930A
P 4100 2750
F 0 "R?" V 4300 2750 50  0000 C CNN
F 1 "330" V 4200 2750 50  0000 C CNN
F 2 "" V 4030 2750 50  0001 C CNN
F 3 "~" H 4100 2750 50  0001 C CNN
	1    4100 2750
	0    1    1    0   
$EndComp
$Comp
L Switch:SW_DP3T SW?
U 2 1 633498EC
P 2300 4500
F 0 "SW?" H 2300 4175 50  0001 C CNN
F 1 "DP3T Momentary" H 2050 4350 50  0000 C CNN
F 2 "" H 1675 4675 50  0001 C CNN
F 3 "~" H 1675 4675 50  0001 C CNN
	2    2300 4500
	1    0    0    -1  
$EndComp
$Comp
L Switch:SW_DP3T SW?
U 1 1 6334755E
P 2300 4100
F 0 "SW?" H 2300 4291 50  0000 C CNN
F 1 "SW_DP3T" H 2300 3866 50  0001 C CNN
F 2 "" H 1675 4275 50  0001 C CNN
F 3 "~" H 1675 4275 50  0001 C CNN
	1    2300 4100
	1    0    0    -1  
$EndComp
Wire Wire Line
	2100 4100 1800 4100
Wire Wire Line
	1800 4100 1800 3600
Wire Wire Line
	1700 3700 1700 4500
Wire Wire Line
	1700 4500 2100 4500
Wire Wire Line
	3450 3200 3450 1950
Wire Wire Line
	3550 3300 3550 2550
Wire Wire Line
	7250 4400 7350 4400
Connection ~ 7350 4400
Wire Wire Line
	7350 4400 7450 4400
Connection ~ 7450 4400
Wire Wire Line
	7450 4400 7550 4400
Connection ~ 7550 4400
Wire Wire Line
	7550 4400 7650 4400
Connection ~ 7650 4400
Wire Wire Line
	7650 4400 7750 4400
Connection ~ 7750 4400
Wire Wire Line
	7750 4400 7850 4400
Connection ~ 7850 4400
Wire Wire Line
	7850 4400 7950 4400
$Comp
L power:GND #PWR?
U 1 1 6340BDEA
P 7950 4650
F 0 "#PWR?" H 7950 4400 50  0001 C CNN
F 1 "GND" H 7955 4477 50  0000 C CNN
F 2 "" H 7950 4650 50  0001 C CNN
F 3 "" H 7950 4650 50  0001 C CNN
	1    7950 4650
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR?
U 1 1 6340CC6A
P 7850 1600
F 0 "#PWR?" H 7850 1450 50  0001 C CNN
F 1 "+3.3V" H 7865 1773 50  0000 C CNN
F 2 "" H 7850 1600 50  0001 C CNN
F 3 "" H 7850 1600 50  0001 C CNN
	1    7850 1600
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR?
U 1 1 6340D925
P 7450 1600
F 0 "#PWR?" H 7450 1450 50  0001 C CNN
F 1 "+5V" H 7465 1773 50  0000 C CNN
F 2 "" H 7450 1600 50  0001 C CNN
F 3 "" H 7450 1600 50  0001 C CNN
	1    7450 1600
	1    0    0    -1  
$EndComp
Wire Wire Line
	7450 1800 7550 1800
Wire Wire Line
	7750 1800 7850 1800
Wire Wire Line
	7850 1800 7850 1600
Connection ~ 7850 1800
Wire Wire Line
	7450 1800 7450 1600
Connection ~ 7450 1800
$Comp
L power:+3.3V #PWR?
U 1 1 6341562C
P 5800 1950
F 0 "#PWR?" H 5800 1800 50  0001 C CNN
F 1 "+3.3V" H 5800 2100 50  0000 C CNN
F 2 "" H 5800 1950 50  0001 C CNN
F 3 "" H 5800 1950 50  0001 C CNN
	1    5800 1950
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR?
U 1 1 63417DAA
P 5800 2550
F 0 "#PWR?" H 5800 2400 50  0001 C CNN
F 1 "+3.3V" H 5800 2700 50  0000 C CNN
F 2 "" H 5800 2550 50  0001 C CNN
F 3 "" H 5800 2550 50  0001 C CNN
	1    5800 2550
	1    0    0    -1  
$EndComp
Wire Wire Line
	6050 3300 6850 3300
Wire Wire Line
	5950 3400 6850 3400
Wire Wire Line
	5700 2750 5950 2750
Wire Wire Line
	5950 2750 5950 3400
Wire Wire Line
	5700 2150 6050 2150
Wire Wire Line
	6050 2150 6050 3300
Wire Wire Line
	5800 2650 5800 2550
Wire Wire Line
	5700 2650 5800 2650
Wire Wire Line
	5700 2050 5800 2050
Wire Wire Line
	5800 2050 5800 1950
NoConn ~ 5700 1950
NoConn ~ 5700 2550
$Comp
L power:+3.3V #PWR?
U 1 1 634961D4
P 4950 3700
F 0 "#PWR?" H 4950 3550 50  0001 C CNN
F 1 "+3.3V" H 4965 3873 50  0000 C CNN
F 2 "" H 4950 3700 50  0001 C CNN
F 3 "" H 4950 3700 50  0001 C CNN
	1    4950 3700
	1    0    0    -1  
$EndComp
$Comp
L myLib:Relay_Module K?
U 1 1 632AF059
P 4450 5200
F 0 "K?" H 4400 4950 50  0000 L CNN
F 1 "Actuate Relay" H 4450 5384 50  0000 C CNN
F 2 "" H 4450 5200 50  0001 C CNN
F 3 "" H 4450 5200 50  0001 C CNN
	1    4450 5200
	-1   0    0    -1  
$EndComp
Wire Wire Line
	7950 4400 7950 4650
Connection ~ 7950 4400
Wire Wire Line
	1500 3700 1700 3700
Wire Wire Line
	1500 3600 1800 3600
Wire Wire Line
	1500 3400 3150 3400
Wire Wire Line
	1500 3300 3550 3300
Wire Wire Line
	1500 3200 3450 3200
$Comp
L power:+3.3V #PWR?
U 1 1 635DEA4F
P 9250 2900
F 0 "#PWR?" H 9250 2750 50  0001 C CNN
F 1 "+3.3V" H 9265 3073 50  0000 C CNN
F 2 "" H 9250 2900 50  0001 C CNN
F 3 "" H 9250 2900 50  0001 C CNN
	1    9250 2900
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 635DF8B4
P 9250 4000
F 0 "#PWR?" H 9250 3750 50  0001 C CNN
F 1 "GND" H 9255 3827 50  0000 C CNN
F 2 "" H 9250 4000 50  0001 C CNN
F 3 "" H 9250 4000 50  0001 C CNN
	1    9250 4000
	1    0    0    -1  
$EndComp
$Comp
L Analog_ADC:MCP3008 U?
U 1 1 635CD1CB
P 9450 3400
F 0 "U?" H 10000 3950 50  0000 C CNN
F 1 "MCP3008" H 9950 3850 50  0000 C CNN
F 2 "" H 9550 3500 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/21295d.pdf" H 9550 3500 50  0001 C CNN
	1    9450 3400
	-1   0    0    -1  
$EndComp
Wire Wire Line
	8450 3600 8650 3600
$Comp
L Connector:Conn_01x02_Male J?
U 1 1 6362E2EC
P 10750 3100
F 0 "J?" H 10800 3250 50  0000 R CNN
F 1 "V Sample" H 10950 2900 50  0000 R CNN
F 2 "" H 10750 3100 50  0001 C CNN
F 3 "~" H 10750 3100 50  0001 C CNN
	1    10750 3100
	-1   0    0    -1  
$EndComp
Wire Wire Line
	10050 3100 10550 3100
Wire Wire Line
	10550 3200 10400 3200
Wire Wire Line
	10400 4150 9550 4150
Wire Wire Line
	9550 4150 9550 4000
Wire Wire Line
	10400 3200 10400 4150
Wire Wire Line
	8850 3400 8450 3400
Wire Wire Line
	8850 3500 8450 3500
Wire Wire Line
	8650 3300 8650 3600
Wire Wire Line
	8650 3300 8850 3300
Wire Wire Line
	8550 3300 8550 3450
Wire Wire Line
	8550 3450 8750 3450
Wire Wire Line
	8750 3450 8750 3600
Wire Wire Line
	8450 3300 8550 3300
Wire Wire Line
	8750 3600 8850 3600
$Comp
L power:+5V #PWR?
U 1 1 636768E0
P 9550 2900
F 0 "#PWR?" H 9550 2750 50  0001 C CNN
F 1 "+5V" H 9565 3073 50  0000 C CNN
F 2 "" H 9550 2900 50  0001 C CNN
F 3 "" H 9550 2900 50  0001 C CNN
	1    9550 2900
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x04_Male J?
U 1 1 6367843A
P 10750 2400
F 0 "J?" H 10800 2650 50  0000 R CNN
F 1 "Grove LCD" H 10950 2100 50  0000 R CNN
F 2 "" H 10750 2400 50  0001 C CNN
F 3 "~" H 10750 2400 50  0001 C CNN
	1    10750 2400
	-1   0    0    -1  
$EndComp
Wire Wire Line
	8450 2600 10550 2600
Wire Wire Line
	8450 2500 10550 2500
$Comp
L power:GND #PWR?
U 1 1 636868F7
P 10350 2700
F 0 "#PWR?" H 10350 2450 50  0001 C CNN
F 1 "GND" H 10355 2527 50  0000 C CNN
F 2 "" H 10350 2700 50  0001 C CNN
F 3 "" H 10350 2700 50  0001 C CNN
	1    10350 2700
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR?
U 1 1 63687541
P 10450 2200
F 0 "#PWR?" H 10450 2050 50  0001 C CNN
F 1 "+5V" H 10465 2373 50  0000 C CNN
F 2 "" H 10450 2200 50  0001 C CNN
F 3 "" H 10450 2200 50  0001 C CNN
	1    10450 2200
	1    0    0    -1  
$EndComp
Wire Wire Line
	10550 2300 10350 2300
Wire Wire Line
	10350 2300 10350 2700
Wire Wire Line
	10550 2400 10450 2400
Wire Wire Line
	10450 2400 10450 2200
$Comp
L Device:R R?
U 1 1 63696CF2
P 4950 1950
F 0 "R?" V 4743 1950 50  0000 C CNN
F 1 "1000" V 4834 1950 50  0000 C CNN
F 2 "" V 4880 1950 50  0001 C CNN
F 3 "~" H 4950 1950 50  0001 C CNN
	1    4950 1950
	0    1    1    0   
$EndComp
$Comp
L Device:R R?
U 1 1 636976E4
P 4950 2550
F 0 "R?" V 4743 2550 50  0000 C CNN
F 1 "1000" V 4834 2550 50  0000 C CNN
F 2 "" V 4880 2550 50  0001 C CNN
F 3 "~" H 4950 2550 50  0001 C CNN
	1    4950 2550
	0    1    1    0   
$EndComp
Wire Wire Line
	4550 2750 4700 2750
Wire Wire Line
	3550 3400 4700 3400
Wire Wire Line
	4550 2150 4700 2150
Wire Wire Line
	4700 2150 4700 2750
Connection ~ 4700 2150
Wire Wire Line
	4700 2150 5100 2150
Connection ~ 4700 2750
Wire Wire Line
	4700 2750 4700 3400
Wire Wire Line
	4700 2750 5100 2750
Text Notes 1750 4800 0    50   ~ 0
(ON)-ON-(ON)
Wire Wire Line
	3450 1950 3850 1950
Wire Wire Line
	3550 2550 3850 2550
Wire Wire Line
	3850 1950 3850 2150
Wire Wire Line
	3850 2150 3950 2150
Connection ~ 3850 1950
Wire Wire Line
	3850 1950 4800 1950
Wire Wire Line
	3850 2550 3850 2750
Wire Wire Line
	3850 2750 3950 2750
Connection ~ 3850 2550
Wire Wire Line
	3850 2550 4800 2550
NoConn ~ 4000 5150
NoConn ~ 5200 2450
Text Notes 1500 3700 0    50   ~ 0
yellow
Text Notes 1500 3600 0    50   ~ 0
blue
NoConn ~ 1500 3500
Text Notes 1500 3400 0    50   ~ 0
black
Text Notes 1500 3300 0    50   ~ 0
red
Text Notes 1500 3200 0    50   ~ 0
green
Text Notes 4150 2050 0    50   ~ 0
Valve Open
Text Notes 4100 2650 0    50   ~ 0
Valve Closed
Text Notes 6400 3300 0    50   ~ 0
Valve Open
Text Notes 6350 3400 0    50   ~ 0
Valve Closed\n
Text Notes 6500 3700 0    50   ~ 0
Actuate
Wire Notes Line rgb(132, 132, 132)
	2300 4050 2300 4450
$Comp
L Device:Fuse_Small F?
U 1 1 63320CD5
P 2350 6400
F 0 "F?" H 2350 6585 50  0000 C CNN
F 1 "1A" H 2350 6494 50  0000 C CNN
F 2 "" H 2350 6400 50  0001 C CNN
F 3 "~" H 2350 6400 50  0001 C CNN
	1    2350 6400
	1    0    0    -1  
$EndComp
Wire Wire Line
	1400 6450 1400 6400
Wire Wire Line
	1400 6400 1950 6400
Connection ~ 1950 6400
Wire Wire Line
	1950 6400 2250 6400
Wire Wire Line
	2450 6400 3150 6400
Wire Wire Line
	1400 6750 1400 6800
Wire Wire Line
	1400 6800 1950 6800
Wire Wire Line
	1950 6800 3550 6800
Connection ~ 1950 6800
$Comp
L myLib:Relay_Module K?
U 1 1 63339078
P 4450 4050
F 0 "K?" H 4150 4200 50  0000 C CNN
F 1 "Open/Close Relays" H 4450 4400 50  0000 C CNN
F 2 "" H 4450 4050 50  0001 C CNN
F 3 "" H 4450 4050 50  0001 C CNN
	1    4450 4050
	-1   0    0    -1  
$EndComp
$Comp
L myLib:Relay_Module K?
U 1 1 63339FE4
P 4450 4450
F 0 "K?" H 4150 4200 50  0000 C CNN
F 1 "Polarity Reverse" H 4450 4150 50  0001 C CNN
F 2 "" H 4450 4450 50  0001 C CNN
F 3 "" H 4450 4450 50  0001 C CNN
	1    4450 4450
	-1   0    0    -1  
$EndComp
Wire Wire Line
	3150 3400 3150 4000
Wire Wire Line
	3550 3400 3550 4200
Wire Wire Line
	2500 4100 4000 4100
Wire Wire Line
	2500 4500 4000 4500
Wire Wire Line
	2500 4000 3150 4000
Connection ~ 3150 4000
Wire Wire Line
	2500 4200 3550 4200
Connection ~ 3550 4200
Wire Wire Line
	2500 4400 3550 4400
Connection ~ 3550 4400
Wire Wire Line
	3550 4400 3550 6800
Wire Wire Line
	2500 4600 3150 4600
Connection ~ 3150 4600
Wire Wire Line
	3150 4000 3150 4600
Wire Wire Line
	3150 5250 4000 5250
Connection ~ 3150 5250
Wire Wire Line
	3150 5250 3150 6400
Wire Wire Line
	3150 4600 3150 5250
Text Notes 6350 3600 0    50   ~ 0
Open/Close
$Comp
L power:GND #PWR?
U 1 1 6339FA56
P 5050 5450
F 0 "#PWR?" H 5050 5200 50  0001 C CNN
F 1 "GND" H 5055 5277 50  0000 C CNN
F 2 "" H 5050 5450 50  0001 C CNN
F 3 "" H 5050 5450 50  0001 C CNN
	1    5050 5450
	1    0    0    -1  
$EndComp
Wire Wire Line
	4900 4000 4950 4000
Wire Wire Line
	4950 4000 4950 4400
Wire Wire Line
	4950 4400 4900 4400
Connection ~ 4950 4000
Wire Wire Line
	4950 4400 4950 5150
Wire Wire Line
	4950 5150 4900 5150
Connection ~ 4950 4400
Wire Wire Line
	4900 4200 5050 4200
Wire Wire Line
	5050 4200 5050 4600
Wire Wire Line
	4900 4600 5050 4600
Connection ~ 5050 4600
Wire Wire Line
	5050 4600 5050 5350
Wire Wire Line
	4900 5350 5050 5350
Connection ~ 5050 5350
Wire Wire Line
	5050 5350 5050 5450
Wire Wire Line
	6850 3700 6050 3700
Wire Wire Line
	6050 3700 6050 5250
Wire Wire Line
	6050 5250 4900 5250
Wire Wire Line
	6850 3600 5950 3600
Wire Wire Line
	5950 3600 5950 4100
Wire Wire Line
	5950 4100 4900 4100
Wire Wire Line
	5950 4100 5950 4500
Wire Wire Line
	5950 4500 4900 4500
Connection ~ 5950 4100
Wire Wire Line
	4950 3700 4950 4000
Wire Wire Line
	3800 4000 3800 4600
Connection ~ 3800 4600
Wire Wire Line
	3800 4600 3800 5350
Wire Wire Line
	3800 4000 4000 4000
Wire Wire Line
	3800 4600 4000 4600
Wire Wire Line
	3800 5350 4000 5350
Wire Wire Line
	4000 4200 3900 4200
Wire Wire Line
	3900 4200 3900 4300
Wire Wire Line
	3900 4400 4000 4400
Wire Wire Line
	3550 4200 3550 4300
Wire Wire Line
	3900 4300 3550 4300
Connection ~ 3900 4300
Wire Wire Line
	3900 4300 3900 4400
Connection ~ 3550 4300
Wire Wire Line
	3550 4300 3550 4400
Wire Notes Line
	4050 3800 4050 4800
Wire Notes Line
	4050 4800 4850 4800
Wire Notes Line
	4850 4800 4850 3800
Wire Notes Line
	4850 3800 4050 3800
Text Notes 700  7350 0    50   ~ 0
Notes:\n1. SP3T switch is momenatry, closing pins 3-1 & 7-5 in one direction, 3-4 & 7-8 in the other, with return-to-center pins 3-2 & 7-6 when released.\n2. Open/Close relays operate in tandem and reverse the polarity of the 12VDC signal passing through the default (return-to-center) pins of the switch.\n3. Actuate relay conditionally supplies 12VDC to the Open/Close relays to actually operate the motor.
Text Notes 2500 4000 0    50   ~ 0
(open)
Text Notes 2500 4200 0    50   ~ 0
(close)
Text Notes 2500 4400 0    50   ~ 0
(open)
Text Notes 2500 4600 0    50   ~ 0
(close)
Text Notes 2500 4100 0    50   ~ 0
center
Text Notes 2500 4500 0    50   ~ 0
center
$EndSCHEMATC

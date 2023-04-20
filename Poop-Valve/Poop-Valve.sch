EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 1 1
Title "Poop Valve Controller"
Date "2023-04-19"
Rev "1.1"
Comp "Robert Ferguson Observatory"
Comment1 "v0.10 add Master Override switch"
Comment2 "v0.11 reconfigure 3.3v override relay drive"
Comment3 "v1.0 promote final draft to production"
Comment4 "v1.1 replace valve connector"
$EndDescr
$Comp
L Connector:Raspberry_Pi_2_3 J1
U 1 1 6329DED7
P 7650 3100
F 0 "J1" H 6950 4450 50  0000 C CNN
F 1 "RaspberryPi" H 7000 4350 50  0000 C CNN
F 2 "" H 7650 3100 50  0001 C CNN
F 3 "https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3bplus_1p0_reduced.pdf" H 7650 3100 50  0001 C CNN
	1    7650 3100
	1    0    0    -1  
$EndComp
$Comp
L Isolator:4N25 U1
U 1 1 632A76B5
P 5400 1450
F 0 "U1" H 5400 1775 50  0000 C CNN
F 1 "Opened" H 5400 1684 50  0000 C CNN
F 2 "Package_DIP:DIP-6_W7.62mm" H 5200 1250 50  0001 L CIN
F 3 "https://www.vishay.com/docs/83725/4n25.pdf" H 5400 1450 50  0001 L CNN
	1    5400 1450
	1    0    0    -1  
$EndComp
$Comp
L Isolator:4N25 U2
U 1 1 632A8434
P 5400 2050
F 0 "U2" H 5400 2375 50  0000 C CNN
F 1 "Closed" H 5400 2284 50  0000 C CNN
F 2 "Package_DIP:DIP-6_W7.62mm" H 5200 1850 50  0001 L CIN
F 3 "https://www.vishay.com/docs/83725/4n25.pdf" H 5400 2050 50  0001 L CNN
	1    5400 2050
	1    0    0    -1  
$EndComp
$Comp
L Device:Battery BT1
U 1 1 632C7943
P 950 9000
F 0 "BT1" H 950 8600 50  0000 C CNN
F 1 "12V" H 950 8700 50  0000 C CNN
F 2 "" V 950 9060 50  0001 C CNN
F 3 "~" V 950 9060 50  0001 C CNN
	1    950  9000
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D3
U 1 1 632DE527
P 7150 950
F 0 "D3" H 6850 900 50  0000 C CNN
F 1 "Valve Closed" H 6300 900 50  0000 L CNN
F 2 "" H 7150 950 50  0001 C CNN
F 3 "~" H 7150 950 50  0001 C CNN
	1    7150 950 
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D2
U 1 1 632DEC5A
P 7150 750
F 0 "D2" H 6850 700 50  0000 C CNN
F 1 "Valve Open" H 6350 700 50  0000 L CNN
F 2 "" H 7150 750 50  0001 C CNN
F 3 "~" H 7150 750 50  0001 C CNN
	1    7150 750 
	-1   0    0    1   
$EndComp
$Comp
L Connector:Conn_Coaxial_Power J3
U 1 1 632E443C
P 400 8950
F 0 "J3" H 400 8500 50  0000 C CNN
F 1 "Charger" H 400 8600 50  0000 C CNN
F 2 "" H 400 8900 50  0001 C CNN
F 3 "~" H 400 8900 50  0001 C CNN
	1    400  8950
	1    0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 632F805C
P 4150 750
F 0 "R2" V 4050 750 50  0000 C CNN
F 1 "330" V 4150 750 50  0000 C CNN
F 2 "" V 4080 750 50  0001 C CNN
F 3 "~" H 4150 750 50  0001 C CNN
	1    4150 750 
	0    1    1    0   
$EndComp
$Comp
L Device:R R3
U 1 1 632F930A
P 4150 950
F 0 "R3" V 4050 950 50  0000 C CNN
F 1 "330" V 4150 950 50  0000 C CNN
F 2 "" V 4080 950 50  0001 C CNN
F 3 "~" H 4150 950 50  0001 C CNN
	1    4150 950 
	0    1    1    0   
$EndComp
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
L power:GND #PWR016
U 1 1 6340BDEA
P 7950 4650
F 0 "#PWR016" H 7950 4400 50  0001 C CNN
F 1 "GND" H 7955 4477 50  0000 C CNN
F 2 "" H 7950 4650 50  0001 C CNN
F 3 "" H 7950 4650 50  0001 C CNN
	1    7950 4650
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR015
U 1 1 6340CC6A
P 7850 1600
F 0 "#PWR015" H 7850 1450 50  0001 C CNN
F 1 "+3.3V" H 7865 1773 50  0000 C CNN
F 2 "" H 7850 1600 50  0001 C CNN
F 3 "" H 7850 1600 50  0001 C CNN
	1    7850 1600
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR014
U 1 1 6340D925
P 7450 1600
F 0 "#PWR014" H 7450 1450 50  0001 C CNN
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
L power:+3.3V #PWR07
U 1 1 6341562C
P 5800 1350
F 0 "#PWR07" H 5800 1200 50  0001 C CNN
F 1 "+3.3V" H 5800 1500 50  0000 C CNN
F 2 "" H 5800 1350 50  0001 C CNN
F 3 "" H 5800 1350 50  0001 C CNN
	1    5800 1350
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR08
U 1 1 63417DAA
P 5800 1950
F 0 "#PWR08" H 5800 1800 50  0001 C CNN
F 1 "+3.3V" H 5800 2100 50  0000 C CNN
F 2 "" H 5800 1950 50  0001 C CNN
F 3 "" H 5800 1950 50  0001 C CNN
	1    5800 1950
	1    0    0    -1  
$EndComp
Wire Wire Line
	6050 3300 6850 3300
Wire Wire Line
	5950 3400 6850 3400
Wire Wire Line
	5700 2150 5950 2150
Wire Wire Line
	5700 1550 6050 1550
Wire Wire Line
	5800 2050 5800 1950
Wire Wire Line
	5700 2050 5800 2050
Wire Wire Line
	5700 1450 5800 1450
Wire Wire Line
	5800 1450 5800 1350
NoConn ~ 5700 1350
NoConn ~ 5700 1950
$Comp
L power:+3.3V #PWR010
U 1 1 634961D4
P 5150 3700
F 0 "#PWR010" H 5150 3550 50  0001 C CNN
F 1 "+3.3V" H 5150 3850 50  0000 C CNN
F 2 "" H 5150 3700 50  0001 C CNN
F 3 "" H 5150 3700 50  0001 C CNN
	1    5150 3700
	1    0    0    -1  
$EndComp
$Comp
L Poop-Valve-rescue:Relay_Module-myLib K3
U 1 1 632AF059
P 3800 5000
F 0 "K3" H 3450 5150 50  0000 L CNN
F 1 "Enable Relays" H 3800 5250 50  0000 C CNN
F 2 "" H 3800 5000 50  0001 C CNN
F 3 "" H 3800 5000 50  0001 C CNN
	1    3800 5000
	-1   0    0    -1  
$EndComp
Wire Wire Line
	7950 4400 7950 4650
Connection ~ 7950 4400
$Comp
L power:+3.3V #PWR018
U 1 1 635DEA4F
P 9700 5000
F 0 "#PWR018" H 9700 4850 50  0001 C CNN
F 1 "+3.3V" H 9715 5173 50  0000 C CNN
F 2 "" H 9700 5000 50  0001 C CNN
F 3 "" H 9700 5000 50  0001 C CNN
	1    9700 5000
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR017
U 1 1 635DF8B4
P 8200 5050
F 0 "#PWR017" H 8200 4800 50  0001 C CNN
F 1 "GND" H 8205 4877 50  0000 C CNN
F 2 "" H 8200 5050 50  0001 C CNN
F 3 "" H 8200 5050 50  0001 C CNN
	1    8200 5050
	1    0    0    -1  
$EndComp
$Comp
L Analog_ADC:MCP3008 U4
U 1 1 635CD1CB
P 9050 5200
F 0 "U4" V 9500 5750 50  0000 C CNN
F 1 "MCP3008" V 9600 5650 50  0000 C CNN
F 2 "" H 9150 5300 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/21295d.pdf" H 9150 5300 50  0001 C CNN
	1    9050 5200
	0    1    -1   0   
$EndComp
$Comp
L Connector:Conn_01x04_Male J16
U 1 1 6367843A
P 10000 2400
F 0 "J16" H 10050 2650 50  0000 R CNN
F 1 "Grove LCD" H 10300 2100 50  0000 R CNN
F 2 "" H 10000 2400 50  0001 C CNN
F 3 "~" H 10000 2400 50  0001 C CNN
	1    10000 2400
	-1   0    0    -1  
$EndComp
$Comp
L power:GND #PWR019
U 1 1 636868F7
P 9600 2700
F 0 "#PWR019" H 9600 2450 50  0001 C CNN
F 1 "GND" H 9605 2527 50  0000 C CNN
F 2 "" H 9600 2700 50  0001 C CNN
F 3 "" H 9600 2700 50  0001 C CNN
	1    9600 2700
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR020
U 1 1 63687541
P 9700 2200
F 0 "#PWR020" H 9700 2050 50  0001 C CNN
F 1 "+5V" H 9715 2373 50  0000 C CNN
F 2 "" H 9700 2200 50  0001 C CNN
F 3 "" H 9700 2200 50  0001 C CNN
	1    9700 2200
	1    0    0    -1  
$EndComp
Wire Wire Line
	9800 2300 9600 2300
Wire Wire Line
	9600 2300 9600 2700
Wire Wire Line
	9800 2400 9700 2400
Wire Wire Line
	9700 2400 9700 2200
$Comp
L Device:R R5
U 1 1 63696CF2
P 4950 1350
F 0 "R5" V 4850 1350 50  0000 C CNN
F 1 "1000" V 4950 1350 50  0000 C CNN
F 2 "" V 4880 1350 50  0001 C CNN
F 3 "~" H 4950 1350 50  0001 C CNN
	1    4950 1350
	0    1    1    0   
$EndComp
$Comp
L Device:R R6
U 1 1 636976E4
P 4950 1950
F 0 "R6" V 4850 1950 50  0000 C CNN
F 1 "1000" V 4950 1950 50  0000 C CNN
F 2 "" V 4880 1950 50  0001 C CNN
F 3 "~" H 4950 1950 50  0001 C CNN
	1    4950 1950
	0    1    1    0   
$EndComp
Connection ~ 4700 1550
Wire Wire Line
	4700 1550 5100 1550
Wire Wire Line
	4700 2150 5100 2150
Wire Wire Line
	3450 1350 3750 1350
Wire Wire Line
	3850 1950 4800 1950
NoConn ~ 3350 4950
Text Notes 1500 1550 2    50   ~ 0
black/white
Text Notes 2200 1350 0    50   ~ 0
Valve Opened
Text Notes 2200 1450 0    50   ~ 0
Valve Closed
Text Notes 6150 3300 0    50   ~ 0
Sense Valve Open
Text Notes 6100 3400 0    50   ~ 0
Sense Valve Closed\n
Text Notes 6550 3600 0    50   ~ 0
Enable
$Comp
L Device:Fuse_Small F1
U 1 1 63320CD5
P 1400 7150
F 0 "F1" H 1400 7335 50  0000 C CNN
F 1 "1A" H 1400 7244 50  0000 C CNN
F 2 "Fuse:Fuse_SunFuse-6HP" H 1400 7150 50  0001 C CNN
F 3 "~" H 1400 7150 50  0001 C CNN
	1    1400 7150
	1    0    0    -1  
$EndComp
Wire Wire Line
	400  8850 400  8800
Wire Wire Line
	400  8800 950  8800
Connection ~ 950  8800
Wire Wire Line
	400  9150 400  9200
Wire Wire Line
	400  9200 950  9200
Wire Wire Line
	950  9200 1400 9200
Connection ~ 950  9200
Text Notes 6300 3700 0    50   ~ 0
* Open-Close
Wire Wire Line
	4300 4950 4250 4950
Wire Wire Line
	4250 5150 4400 5150
$Comp
L Poop-Valve-rescue:Relay_Module-myLib K4
U 1 1 63423895
P 3800 5400
F 0 "K4" H 3500 5150 50  0000 C CNN
F 1 "Relay_Module" H 3800 5584 50  0001 C CNN
F 2 "" H 3800 5400 50  0001 C CNN
F 3 "" H 3800 5400 50  0001 C CNN
	1    3800 5400
	-1   0    0    -1  
$EndComp
Wire Wire Line
	4300 5350 4250 5350
Wire Wire Line
	4250 5550 4400 5550
Wire Notes Line
	3400 4700 4200 4700
Wire Notes Line
	4200 4700 4200 5700
Wire Notes Line
	4200 5700 3400 5700
Wire Notes Line
	3400 5700 3400 4700
NoConn ~ 3350 5350
$Comp
L Poop-Valve-rescue:Relay_Module-myLib K1
U 1 1 639015D0
P 3800 3850
F 0 "K1" H 3500 4000 50  0000 C CNN
F 1 "Override Relays" H 3800 4100 50  0000 C CNN
F 2 "" H 3800 3850 50  0001 C CNN
F 3 "" H 3800 3850 50  0001 C CNN
	1    3800 3850
	-1   0    0    -1  
$EndComp
$Comp
L Poop-Valve-rescue:Relay_Module-myLib K2
U 1 1 639015D6
P 3800 4250
F 0 "K2" H 3500 4000 50  0000 C CNN
F 1 "Polarity Reverse" H 3800 3950 50  0001 C CNN
F 2 "" H 3800 4250 50  0001 C CNN
F 3 "" H 3800 4250 50  0001 C CNN
	1    3800 4250
	-1   0    0    -1  
$EndComp
Wire Notes Line
	3400 3550 4200 3550
Wire Notes Line
	3400 4550 4200 4550
Wire Notes Line
	4200 3550 4200 4550
Wire Notes Line
	3400 3550 3400 4550
$Comp
L Poop-Valve-rescue:Relay_Module-myLib K5
U 1 1 63D2BA9E
P 3800 6150
F 0 "K5" H 3500 6300 50  0000 C CNN
F 1 "Direction Relays" H 3800 6400 50  0000 C CNN
F 2 "" H 3800 6150 50  0001 C CNN
F 3 "" H 3800 6150 50  0001 C CNN
	1    3800 6150
	-1   0    0    -1  
$EndComp
$Comp
L Poop-Valve-rescue:Relay_Module-myLib K6
U 1 1 63D2BAA4
P 3800 6550
F 0 "K6" H 3500 6300 50  0000 C CNN
F 1 "Polarity Reverse" H 3800 6250 50  0001 C CNN
F 2 "" H 3800 6550 50  0001 C CNN
F 3 "" H 3800 6550 50  0001 C CNN
	1    3800 6550
	-1   0    0    -1  
$EndComp
Wire Wire Line
	4250 6100 4300 6100
Wire Wire Line
	4300 6500 4250 6500
Wire Wire Line
	4250 6700 4400 6700
Wire Notes Line
	3400 5850 4200 5850
Wire Notes Line
	3400 6850 4200 6850
Wire Notes Line
	4200 5850 4200 6850
Wire Notes Line
	3400 5850 3400 6850
Wire Wire Line
	4300 6100 4300 6500
Connection ~ 4300 6100
Wire Wire Line
	4250 6300 4400 6300
Connection ~ 4400 6300
Wire Wire Line
	4400 6300 4400 6700
Wire Wire Line
	3350 6200 3300 6200
Wire Wire Line
	3300 5450 3350 5450
Wire Wire Line
	3350 6600 3200 6600
Wire Wire Line
	3200 6600 3200 5050
Wire Wire Line
	3200 5050 3350 5050
Text Notes 6150 4000 0    50   ~ 0
* GPIO26 logic:\n  Open is high\n  Close is low
Wire Wire Line
	6050 1550 6050 3300
Wire Wire Line
	5950 2150 5950 3400
Text Notes 5950 3500 0    50   ~ 0
Sense Override (invert)
$Comp
L Device:R R4
U 1 1 6366E688
P 4950 2500
F 0 "R4" V 4850 2500 50  0000 C CNN
F 1 "330" V 4950 2500 50  0000 C CNN
F 2 "" V 4880 2500 50  0001 C CNN
F 3 "~" H 4950 2500 50  0001 C CNN
	1    4950 2500
	0    1    1    0   
$EndComp
$Comp
L Device:LED D4
U 1 1 6366FF88
P 7150 1150
F 0 "D4" H 6850 1100 50  0000 C CNN
F 1 "Override" H 6450 1100 50  0000 L CNN
F 2 "" H 7150 1150 50  0001 C CNN
F 3 "~" H 7150 1150 50  0001 C CNN
	1    7150 1150
	-1   0    0    1   
$EndComp
Wire Wire Line
	8450 5000 8200 5000
Wire Wire Line
	8200 5000 8200 5050
Wire Wire Line
	9550 5000 9700 5000
Wire Wire Line
	9700 5000 9700 5300
Wire Wire Line
	9700 5300 9550 5300
Connection ~ 9700 5000
Wire Wire Line
	8450 3300 8850 3300
Wire Wire Line
	8850 3300 8850 4600
Wire Wire Line
	8450 3400 9050 3400
Wire Wire Line
	9050 3400 9050 4600
Wire Wire Line
	8450 3500 8950 3500
Wire Wire Line
	8950 3500 8950 4600
Wire Wire Line
	8450 3600 9150 3600
Wire Wire Line
	9150 3600 9150 4600
$Comp
L Connector:Conn_01x05_Female J12
U 1 1 639D2C62
P 4750 3900
F 0 "J12" H 4600 3600 50  0000 L CNN
F 1 "Relays" H 4600 4250 50  0000 L CNN
F 2 "" H 4750 3900 50  0001 C CNN
F 3 "~" H 4750 3900 50  0001 C CNN
	1    4750 3900
	-1   0    0    -1  
$EndComp
Wire Wire Line
	4250 5450 4500 5450
Wire Wire Line
	4950 3700 5050 3700
$Comp
L Connector:Conn_Coaxial_Power J6
U 1 1 63C5326A
P 1400 8950
F 0 "J6" V 1500 8900 50  0000 C CNN
F 1 "Power" H 1350 8550 50  0000 C CNN
F 2 "" H 1400 8900 50  0001 C CNN
F 3 "~" H 1400 8900 50  0001 C CNN
	1    1400 8950
	1    0    0    -1  
$EndComp
Wire Wire Line
	1400 8800 1400 8850
Wire Wire Line
	950  8800 1400 8800
Wire Wire Line
	1400 9200 1400 9150
$Comp
L Connector:Conn_01x02_Male J8
U 1 1 63C8A8CE
P 1950 7300
F 0 "J8" H 2000 7150 50  0000 C CNN
F 1 "Conn_01x02_Male" H 2150 6850 50  0001 C CNN
F 2 "" H 1950 7300 50  0001 C CNN
F 3 "~" H 1950 7300 50  0001 C CNN
	1    1950 7300
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Male J9
U 1 1 63C8CB61
P 2450 7300
F 0 "J9" H 2500 7150 50  0000 C CNN
F 1 "Conn_01x02_Male" H 2558 7390 50  0001 C CNN
F 2 "" H 2450 7300 50  0001 C CNN
F 3 "~" H 2450 7300 50  0001 C CNN
	1    2450 7300
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Male J11
U 1 1 63C97CE9
P 2900 7300
F 0 "J11" H 2950 7150 50  0000 C CNN
F 1 "Conn_01x02_Male" H 3008 7390 50  0001 C CNN
F 2 "" H 2900 7300 50  0001 C CNN
F 3 "~" H 2900 7300 50  0001 C CNN
	1    2900 7300
	-1   0    0    -1  
$EndComp
Wire Wire Line
	1150 7550 1150 7500
Wire Wire Line
	1150 7200 1150 7150
Wire Wire Line
	2700 7150 2700 7300
Wire Wire Line
	2700 7400 2700 7550
Connection ~ 2700 7400
Connection ~ 2700 7300
Wire Wire Line
	1750 7150 1750 7300
Connection ~ 1750 7150
Wire Wire Line
	1750 7400 1750 7550
Wire Wire Line
	1750 7150 2250 7150
Wire Wire Line
	1750 7550 2250 7550
Wire Wire Line
	2250 7300 2250 7150
Connection ~ 2250 7150
Wire Wire Line
	2250 7150 2700 7150
Wire Wire Line
	2250 7400 2250 7550
Connection ~ 2250 7550
Wire Wire Line
	2250 7550 2700 7550
Wire Wire Line
	2100 7400 1750 7400
Connection ~ 1750 7400
$Comp
L Switch:SW_SPDT_MSM SW3
U 1 1 6402D895
P 2400 4200
F 0 "SW3" H 2950 3500 50  0000 C CNN
F 1 "Open/Close" H 2900 3600 50  0000 C CNN
F 2 "" H 2400 4200 50  0001 C CNN
F 3 "~" H 2400 4200 50  0001 C CNN
	1    2400 4200
	-1   0    0    1   
$EndComp
Wire Notes Line
	2400 4150 2400 3850
Wire Wire Line
	2200 3900 2100 3900
Wire Wire Line
	2200 3700 2000 3700
Text Notes 1250 3750 0    50   ~ 0
Momentary
Wire Wire Line
	3100 3900 3350 3900
$Comp
L Switch:SW_SPDT_MSM SW2
U 1 1 6402D89B
P 2400 3800
F 0 "SW2" H 2400 3600 50  0001 C CNN
F 1 "SW_DPDT_x2" H 2400 3994 50  0001 C CNN
F 2 "" H 2400 3800 50  0001 C CNN
F 3 "~" H 2400 3800 50  0001 C CNN
	1    2400 3800
	-1   0    0    1   
$EndComp
Text Notes 2350 4400 0    50   ~ 0
Close
Text Notes 2350 3650 0    50   ~ 0
Open
Wire Wire Line
	2150 1350 3450 1350
Connection ~ 3450 1350
Connection ~ 3450 1550
Wire Wire Line
	7300 750  7300 850 
Wire Wire Line
	7300 950  7300 1050
Wire Wire Line
	7300 1150 7300 1250
Wire Wire Line
	4700 1550 4700 1050
Wire Wire Line
	4700 850  4700 1050
Connection ~ 4700 1050
Wire Wire Line
	6200 1150 6200 2500
Wire Wire Line
	3750 750  3750 1350
Connection ~ 3750 1350
Wire Wire Line
	3750 1350 4800 1350
Wire Wire Line
	3850 950  3850 1550
Wire Wire Line
	4700 1550 4700 2150
Connection ~ 3850 1550
Wire Wire Line
	3850 1550 3850 1950
Wire Wire Line
	3450 1550 3850 1550
Wire Wire Line
	3750 750  4000 750 
Wire Wire Line
	4000 950  3850 950 
Connection ~ 4700 2150
Wire Wire Line
	2900 6100 3350 6100
Wire Wire Line
	2900 6100 2900 6700
Connection ~ 2900 6700
Wire Wire Line
	2900 6700 3350 6700
Wire Wire Line
	2900 6700 2900 7300
Wire Wire Line
	2700 7300 2900 7300
Wire Wire Line
	1750 7300 2000 7300
Connection ~ 1750 7300
Text Notes 1750 4400 0    50   ~ 0
+12V
Text Notes 2850 6100 0    50   ~ 0
+12V
$Comp
L Connector:Conn_01x06_Male J13
U 1 1 64A6ADC2
P 6600 1050
F 0 "J13" H 6600 650 50  0000 C CNN
F 1 "LEDs" H 6650 1350 50  0000 C CNN
F 2 "" H 6600 1050 50  0001 C CNN
F 3 "~" H 6600 1050 50  0001 C CNN
	1    6600 1050
	-1   0    0    1   
$EndComp
Wire Wire Line
	4300 750  6400 750 
Wire Wire Line
	4700 850  6400 850 
Wire Wire Line
	4300 950  6400 950 
Wire Wire Line
	4700 1050 6400 1050
Wire Wire Line
	6300 1250 6400 1250
Connection ~ 6400 1050
Wire Wire Line
	6400 1050 7300 1050
Connection ~ 6400 950 
Wire Wire Line
	6400 950  7000 950 
Connection ~ 6400 850 
Wire Wire Line
	6400 850  7300 850 
Connection ~ 6400 750 
Wire Wire Line
	6400 750  7000 750 
Connection ~ 6400 1250
Wire Wire Line
	6400 1250 7300 1250
Wire Wire Line
	6200 1150 6400 1150
Connection ~ 6400 1150
Wire Wire Line
	6400 1150 7000 1150
$Comp
L power:+3.3V #PWR02
U 1 1 64418208
P 6450 5600
F 0 "#PWR02" H 6450 5450 50  0001 C CNN
F 1 "+3.3V" H 6465 5773 50  0000 C CNN
F 2 "" H 6450 5600 50  0001 C CNN
F 3 "" H 6450 5600 50  0001 C CNN
	1    6450 5600
	1    0    0    -1  
$EndComp
NoConn ~ 7250 5850
Text Notes 7400 6500 2    50   ~ 0
Inline (F)
$Comp
L Device:LED D1
U 1 1 63AE6C12
P 6800 4200
F 0 "D1" V 6850 4400 50  0000 R CNN
F 1 "Heart" V 6750 4500 50  0000 R CNN
F 2 "" H 6800 4200 50  0001 C CNN
F 3 "~" H 6800 4200 50  0001 C CNN
	1    6800 4200
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R8
U 1 1 63B22253
P 6800 4500
F 0 "R8" H 6600 4550 50  0000 L CNN
F 1 "470" V 6800 4450 50  0000 L CNN
F 2 "" V 6730 4500 50  0001 C CNN
F 3 "~" H 6800 4500 50  0001 C CNN
	1    6800 4500
	1    0    0    -1  
$EndComp
Wire Wire Line
	6800 3800 6850 3800
$Comp
L power:GND #PWR013
U 1 1 63B37882
P 6800 4650
F 0 "#PWR013" H 6800 4400 50  0001 C CNN
F 1 "GND" H 6805 4477 50  0000 C CNN
F 2 "" H 6800 4650 50  0001 C CNN
F 3 "" H 6800 4650 50  0001 C CNN
	1    6800 4650
	1    0    0    -1  
$EndComp
Wire Wire Line
	6800 4050 6800 3800
$Comp
L Device:R R9
U 1 1 63D72259
P 8750 6150
F 0 "R9" V 8850 6100 50  0000 L CNN
F 1 "250/2W" V 8650 6000 50  0000 L CNN
F 2 "" V 8680 6150 50  0001 C CNN
F 3 "~" H 8750 6150 50  0001 C CNN
	1    8750 6150
	0    1    1    0   
$EndComp
$Comp
L Connector:Conn_Coaxial_Power J15
U 1 1 641727E8
P 9550 6450
F 0 "J15" H 9750 6400 50  0000 C CNN
F 1 "Sensor" H 9750 6500 50  0000 C CNN
F 2 "" H 9550 6400 50  0001 C CNN
F 3 "~" H 9550 6400 50  0001 C CNN
	1    9550 6450
	1    0    0    1   
$EndComp
$Comp
L Connector:Conn_Coaxial_Power J14
U 1 1 641859E8
P 8050 6450
F 0 "J14" H 7850 6400 50  0000 C CNN
F 1 "24VDC" H 7850 6500 50  0000 C CNN
F 2 "" H 8050 6400 50  0001 C CNN
F 3 "~" H 8050 6400 50  0001 C CNN
	1    8050 6450
	1    0    0    1   
$EndComp
$Comp
L Device:Fuse_Small F2
U 1 1 642381A4
P 8750 6550
F 0 "F2" H 8750 6450 50  0000 C CNN
F 1 "1A" H 8750 6644 50  0000 C CNN
F 2 "Fuse:Fuse_SunFuse-6HP" H 8750 6550 50  0001 C CNN
F 3 "~" H 8750 6550 50  0001 C CNN
	1    8750 6550
	1    0    0    -1  
$EndComp
Wire Wire Line
	8250 5300 8450 5300
Connection ~ 8250 6150
Wire Wire Line
	8250 6150 8250 5300
Wire Wire Line
	9350 5800 9350 6150
Connection ~ 9350 6150
Wire Wire Line
	8050 6550 8650 6550
Wire Wire Line
	8850 6550 9550 6550
Wire Wire Line
	1150 7550 1650 7550
Connection ~ 1750 7550
Wire Wire Line
	1150 7150 1300 7150
Wire Wire Line
	1500 7150 1650 7150
Text Notes 8100 6350 0    50   ~ 0
Phono
Text Notes 9200 6350 0    50   ~ 0
Phono
Text Notes 1200 7450 0    50   ~ 0
5.5x2.1
$Comp
L Connector:Conn_Coaxial_Power J7
U 1 1 63C43814
P 1150 7300
F 0 "J7" H 900 7250 50  0000 C CNN
F 1 "12VDC" H 900 7150 50  0000 C CNN
F 2 "" H 1150 7250 50  0001 C CNN
F 3 "~" H 1150 7250 50  0001 C CNN
	1    1150 7300
	1    0    0    -1  
$EndComp
NoConn ~ 6850 2200
NoConn ~ 6850 2300
NoConn ~ 6850 2500
NoConn ~ 6850 2600
NoConn ~ 6850 2700
NoConn ~ 6850 2900
NoConn ~ 6850 3000
NoConn ~ 6850 3100
NoConn ~ 8450 3800
NoConn ~ 8450 3900
NoConn ~ 8450 3200
NoConn ~ 8450 3000
NoConn ~ 8450 2900
NoConn ~ 8450 2800
NoConn ~ 8450 2300
NoConn ~ 8450 2200
$Comp
L power:PWR_FLAG #FLG01
U 1 1 645312DE
P 3750 9050
F 0 "#FLG01" H 3750 9125 50  0001 C CNN
F 1 "PWR_FLAG" H 3750 9223 50  0000 C CNN
F 2 "" H 3750 9050 50  0001 C CNN
F 3 "~" H 3750 9050 50  0001 C CNN
	1    3750 9050
	1    0    0    1   
$EndComp
$Comp
L power:PWR_FLAG #FLG02
U 1 1 6453219E
P 4150 9050
F 0 "#FLG02" H 4150 9125 50  0001 C CNN
F 1 "PWR_FLAG" H 4150 9223 50  0000 C CNN
F 2 "" H 4150 9050 50  0001 C CNN
F 3 "~" H 4150 9050 50  0001 C CNN
	1    4150 9050
	1    0    0    1   
$EndComp
$Comp
L power:PWR_FLAG #FLG03
U 1 1 645333EA
P 4550 9050
F 0 "#FLG03" H 4550 9125 50  0001 C CNN
F 1 "PWR_FLAG" H 4550 9223 50  0000 C CNN
F 2 "" H 4550 9050 50  0001 C CNN
F 3 "~" H 4550 9050 50  0001 C CNN
	1    4550 9050
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR03
U 1 1 64534DD7
P 3750 9050
F 0 "#PWR03" H 3750 8900 50  0001 C CNN
F 1 "+3.3V" H 3765 9223 50  0000 C CNN
F 2 "" H 3750 9050 50  0001 C CNN
F 3 "" H 3750 9050 50  0001 C CNN
	1    3750 9050
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR04
U 1 1 64571F32
P 4150 9050
F 0 "#PWR04" H 4150 8900 50  0001 C CNN
F 1 "+5V" H 4165 9223 50  0000 C CNN
F 2 "" H 4150 9050 50  0001 C CNN
F 3 "" H 4150 9050 50  0001 C CNN
	1    4150 9050
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR05
U 1 1 645AE2AE
P 4550 9050
F 0 "#PWR05" H 4550 8800 50  0001 C CNN
F 1 "GND" H 4555 8877 50  0000 C CNN
F 2 "" H 4550 9050 50  0001 C CNN
F 3 "" H 4550 9050 50  0001 C CNN
	1    4550 9050
	1    0    0    -1  
$EndComp
Wire Wire Line
	8600 6150 8250 6150
Wire Wire Line
	8900 6150 9350 6150
Wire Wire Line
	9550 6150 9550 6250
Wire Wire Line
	9550 6150 9350 6150
Wire Wire Line
	8050 6250 8050 6150
Wire Wire Line
	8050 6150 8250 6150
NoConn ~ 7250 5950
NoConn ~ 7250 6050
NoConn ~ 6600 5950
NoConn ~ 6600 6050
Wire Wire Line
	7250 6150 6600 6150
Connection ~ 6600 6150
Connection ~ 6600 6250
Wire Wire Line
	5850 3500 6850 3500
Wire Wire Line
	5000 3000 5100 3000
Wire Wire Line
	5850 3000 5850 3500
Wire Wire Line
	5700 3000 5850 3000
$Comp
L Device:R R7
U 1 1 63562052
P 4950 2800
F 0 "R7" V 4850 2800 50  0000 C CNN
F 1 "1000" V 4950 2800 50  0000 C CNN
F 2 "" V 4880 2800 50  0001 C CNN
F 3 "~" H 4950 2800 50  0001 C CNN
	1    4950 2800
	0    1    1    0   
$EndComp
NoConn ~ 5700 2800
Wire Wire Line
	5800 2900 5800 2800
Wire Wire Line
	5700 2900 5800 2900
$Comp
L power:+3.3V #PWR09
U 1 1 63562048
P 5800 2800
F 0 "#PWR09" H 5800 2650 50  0001 C CNN
F 1 "+3.3V" H 5800 2950 50  0000 C CNN
F 2 "" H 5800 2800 50  0001 C CNN
F 3 "" H 5800 2800 50  0001 C CNN
	1    5800 2800
	1    0    0    -1  
$EndComp
$Comp
L Isolator:4N25 U3
U 1 1 63562042
P 5400 2900
F 0 "U3" H 5400 3225 50  0000 C CNN
F 1 "Override" H 5400 3134 50  0000 C CNN
F 2 "Package_DIP:DIP-6_W7.62mm" H 5200 2700 50  0001 L CIN
F 3 "https://www.vishay.com/docs/83725/4n25.pdf" H 5400 2900 50  0001 L CNN
	1    5400 2900
	1    0    0    -1  
$EndComp
NoConn ~ 8650 5800
NoConn ~ 8750 5800
NoConn ~ 8850 5800
NoConn ~ 8950 5800
NoConn ~ 9050 5800
NoConn ~ 9150 5800
NoConn ~ 9250 5800
Wire Wire Line
	4300 3800 4250 3800
Wire Wire Line
	4250 4200 4300 4200
Wire Wire Line
	4400 4000 4250 4000
Wire Wire Line
	4250 4400 4400 4400
Wire Wire Line
	4250 4300 4500 4300
Connection ~ 4950 4000
Wire Wire Line
	4250 6600 4500 6600
Wire Wire Line
	4250 6200 4500 6200
Connection ~ 4950 4100
Wire Wire Line
	4900 3700 4400 3700
Wire Wire Line
	4500 6200 4500 6600
Wire Wire Line
	4950 4000 5300 4000
Wire Wire Line
	4950 4100 5400 4100
Wire Wire Line
	3300 5450 3300 6200
Connection ~ 4300 4200
Connection ~ 4300 4950
Connection ~ 4300 5350
Connection ~ 4400 4400
Connection ~ 4400 5150
Connection ~ 4400 5550
Wire Wire Line
	4400 4400 4400 5150
Wire Wire Line
	4300 4200 4300 4950
Wire Wire Line
	4400 4000 4400 4400
Wire Wire Line
	4400 5150 4400 5550
Wire Wire Line
	4500 5050 4500 5450
Wire Wire Line
	5100 2500 6200 2500
Wire Wire Line
	4800 2800 4700 2800
Connection ~ 4950 3900
Wire Wire Line
	6600 6250 7250 6250
Connection ~ 7250 6250
Wire Wire Line
	7250 6150 7400 6150
Connection ~ 7250 6150
Wire Wire Line
	2000 4300 2200 4300
Wire Wire Line
	2200 4100 2100 4100
Wire Wire Line
	2100 3900 2100 4100
Wire Wire Line
	2000 3700 2000 4300
Wire Wire Line
	3100 5550 3100 4400
Wire Wire Line
	3100 4400 3350 4400
Wire Wire Line
	3100 5550 3350 5550
Wire Wire Line
	3000 5150 3000 4000
Wire Wire Line
	3000 4000 3350 4000
Wire Wire Line
	3000 5150 3350 5150
Wire Wire Line
	4250 5050 4500 5050
Wire Wire Line
	4300 4950 4300 5350
Wire Wire Line
	4300 3800 4300 4200
Wire Wire Line
	4250 3900 4500 3900
Connection ~ 2000 4300
Connection ~ 2100 4100
Wire Wire Line
	3200 4300 3350 4300
Text Notes 1100 3850 0    50   ~ 0
(open)-OFF-(close)
$Comp
L power:-12V #PWR06
U 1 1 65B0B563
P 3850 2200
F 0 "#PWR06" H 3850 2300 50  0001 C CNN
F 1 "-12V" H 3865 2373 50  0000 C CNN
F 2 "" H 3850 2200 50  0001 C CNN
F 3 "" H 3850 2200 50  0001 C CNN
	1    3850 2200
	-1   0    0    1   
$EndComp
$Comp
L power:-12V #PWR01
U 1 1 65B2F214
P 1650 7650
F 0 "#PWR01" H 1650 7750 50  0001 C CNN
F 1 "-12V" H 1665 7823 50  0000 C CNN
F 2 "" H 1650 7650 50  0001 C CNN
F 3 "" H 1650 7650 50  0001 C CNN
	1    1650 7650
	-1   0    0    1   
$EndComp
Wire Wire Line
	1650 7550 1650 7650
Wire Wire Line
	4700 2500 4700 2800
Wire Wire Line
	4700 2500 4800 2500
Wire Wire Line
	4950 3900 5200 3900
Wire Wire Line
	2100 4100 2100 7400
Wire Wire Line
	2000 4300 2000 7300
Wire Wire Line
	2600 3800 3350 3800
Wire Wire Line
	2600 4200 3350 4200
Wire Wire Line
	4300 5350 4300 6100
Wire Wire Line
	4400 5550 4400 6300
Connection ~ 4500 3900
Wire Wire Line
	4500 3900 4950 3900
Wire Wire Line
	4500 5050 4600 5050
Wire Wire Line
	4600 5050 4600 4000
Connection ~ 4500 5050
Wire Wire Line
	4600 4000 4950 4000
Wire Wire Line
	4500 6200 4700 6200
Wire Wire Line
	4700 6200 4700 4100
Connection ~ 4500 6200
Wire Wire Line
	4700 4100 4950 4100
Wire Wire Line
	4500 3900 4500 4300
Wire Wire Line
	5300 4000 5300 3600
Wire Wire Line
	5400 4100 5400 3700
Wire Wire Line
	5300 3600 6850 3600
Wire Wire Line
	5400 3700 6850 3700
$Comp
L Device:Q_NPN_CBE Q?
U 1 1 6627A4F5
P 5350 6250
AR Path="/65DFE627/6627A4F5" Ref="Q?"  Part="1" 
AR Path="/6627A4F5" Ref="Q1"  Part="1" 
F 0 "Q1" H 5540 6296 50  0000 L CNN
F 1 "2N2222" H 5540 6205 50  0000 L CNN
F 2 "" H 5550 6350 50  0001 C CNN
F 3 "~" H 5350 6250 50  0001 C CNN
	1    5350 6250
	-1   0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 6627A53E
P 5250 6450
AR Path="/65DFE627/6627A53E" Ref="#PWR?"  Part="1" 
AR Path="/6627A53E" Ref="#PWR021"  Part="1" 
F 0 "#PWR021" H 5250 6200 50  0001 C CNN
F 1 "GND" H 5255 6277 50  0000 C CNN
F 2 "" H 5250 6450 50  0001 C CNN
F 3 "" H 5250 6450 50  0001 C CNN
	1    5250 6450
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x04_Male J4
U 1 1 64618888
P 6800 6150
F 0 "J4" H 6950 5800 50  0000 R CNN
F 1 "Override" H 7000 6350 50  0000 R CNN
F 2 "" H 6800 6150 50  0001 C CNN
F 3 "~" H 6800 6150 50  0001 C CNN
	1    6800 6150
	-1   0    0    1   
$EndComp
$Comp
L Connector:Conn_01x05_Male J5
U 1 1 636591C4
P 7050 6050
F 0 "J5" H 7200 5700 50  0000 R CNN
F 1 "Ovr Switch" H 7400 6350 50  0000 R CNN
F 2 "" H 7050 6050 50  0001 C CNN
F 3 "~" H 7050 6050 50  0001 C CNN
	1    7050 6050
	1    0    0    1   
$EndComp
Wire Wire Line
	6450 6150 6600 6150
Text Notes 4750 6450 0    50   ~ 0
Ovr Shunt
$Comp
L Device:R R?
U 1 1 6659FCFC
P 6050 5400
AR Path="/65DFE627/6659FCFC" Ref="R?"  Part="1" 
AR Path="/6659FCFC" Ref="R11"  Part="1" 
F 0 "R11" H 5980 5446 50  0000 R CNN
F 1 "10k" H 5980 5355 50  0000 R CNN
F 2 "" V 5980 5400 50  0001 C CNN
F 3 "~" H 6050 5400 50  0001 C CNN
	1    6050 5400
	-1   0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 6659FD02
P 5650 5350
AR Path="/65DFE627/6659FD02" Ref="#PWR?"  Part="1" 
AR Path="/6659FD02" Ref="#PWR022"  Part="1" 
F 0 "#PWR022" H 5650 5100 50  0001 C CNN
F 1 "GND" H 5655 5177 50  0000 C CNN
F 2 "" H 5650 5350 50  0001 C CNN
F 3 "" H 5650 5350 50  0001 C CNN
	1    5650 5350
	-1   0    0    -1  
$EndComp
Wire Wire Line
	5000 3000 5000 3150
$Comp
L power:+3.3V #PWR011
U 1 1 6660F16D
P 4550 2450
F 0 "#PWR011" H 4550 2300 50  0001 C CNN
F 1 "+3.3V" H 4565 2623 50  0000 C CNN
F 2 "" H 4550 2450 50  0001 C CNN
F 3 "" H 4550 2450 50  0001 C CNN
	1    4550 2450
	1    0    0    -1  
$EndComp
Connection ~ 4700 2500
Wire Wire Line
	3850 2150 3850 2200
Wire Wire Line
	4550 2450 4550 2500
Wire Wire Line
	4550 2500 4700 2500
Wire Wire Line
	6300 1250 6300 3150
Connection ~ 6050 6250
Wire Wire Line
	6050 6250 6600 6250
Wire Wire Line
	5950 5150 6050 5150
Wire Wire Line
	6050 5150 6050 5250
Wire Wire Line
	7800 5950 7800 6250
Wire Wire Line
	7400 5950 7400 6150
Wire Wire Line
	7250 6250 7800 6250
$Comp
L Switch:SW_Push SW1
U 1 1 63F2028E
P 7600 5950
F 0 "SW1" H 7700 6250 50  0000 R CNN
F 1 "Override" H 7750 6150 50  0000 R CNN
F 2 "" H 7600 6150 50  0001 C CNN
F 3 "~" H 7600 6150 50  0001 C CNN
	1    7600 5950
	-1   0    0    -1  
$EndComp
Wire Wire Line
	5150 3800 5150 3700
Wire Wire Line
	5050 3700 5050 4150
Wire Wire Line
	4300 3800 4950 3800
Connection ~ 4300 3800
Connection ~ 4950 3800
Wire Wire Line
	4950 3800 5150 3800
Wire Wire Line
	4400 3700 4400 4000
Connection ~ 4400 4000
Text Notes 5750 5000 0    50   ~ 0
Ovr Sense
$Comp
L Device:Q_NPN_CBE Q?
U 1 1 6659FCF6
P 5750 5150
AR Path="/65DFE627/6659FCF6" Ref="Q?"  Part="1" 
AR Path="/6659FCF6" Ref="Q2"  Part="1" 
F 0 "Q2" H 5940 5196 50  0000 L CNN
F 1 "2N2222" H 5940 5105 50  0000 L CNN
F 2 "" H 5950 5250 50  0001 C CNN
F 3 "~" H 5750 5150 50  0001 C CNN
	1    5750 5150
	-1   0    0    -1  
$EndComp
$Comp
L Switch:SW_SPDT_SMALL SW4
U 1 1 66A95683
P 5200 4500
F 0 "SW4" V 5129 4598 50  0001 L CNN
F 1 "SW_SPDT_SMALL" V 5550 4100 50  0001 L CNN
F 2 "" H 5150 4270 50  0001 C CNN
F 3 "~" H 5150 4270 50  0001 C CNN
	1    5200 4500
	0    1    1    0   
$EndComp
Wire Wire Line
	5200 4300 5200 3900
Wire Wire Line
	5600 4300 5600 3150
Connection ~ 5600 3150
Wire Wire Line
	5600 3150 5000 3150
Wire Wire Line
	5600 3150 6300 3150
$Comp
L power:GND #PWR026
U 1 1 66BEBFAF
P 5550 4650
F 0 "#PWR026" H 5550 4400 50  0001 C CNN
F 1 "GND" H 5555 4477 50  0000 C CNN
F 2 "" H 5550 4650 50  0001 C CNN
F 3 "" H 5550 4650 50  0001 C CNN
	1    5550 4650
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR025
U 1 1 66BECFD3
P 5150 4650
F 0 "#PWR025" H 5150 4400 50  0001 C CNN
F 1 "GND" H 5155 4477 50  0000 C CNN
F 2 "" H 5150 4650 50  0001 C CNN
F 3 "" H 5150 4650 50  0001 C CNN
	1    5150 4650
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR012
U 1 1 65D19661
P 5050 4150
F 0 "#PWR012" H 5050 3900 50  0001 C CNN
F 1 "GND" H 5055 3977 50  0000 C CNN
F 2 "" H 5050 4150 50  0001 C CNN
F 3 "" H 5050 4150 50  0001 C CNN
	1    5050 4150
	1    0    0    -1  
$EndComp
Wire Notes Line
	5200 4450 5600 4450
Wire Wire Line
	6050 5550 6050 6250
Wire Wire Line
	5650 4650 5650 4950
Text Notes 5750 4650 0    50   ~ 0
Run
Text Notes 4950 4650 0    50   ~ 0
Ovr
$Comp
L Device:R R1
U 1 1 664501BE
P 5250 5900
F 0 "R1" H 5350 5850 50  0000 C CNN
F 1 "330" V 5250 5900 50  0000 C CNN
F 2 "" V 5180 5900 50  0001 C CNN
F 3 "~" H 5250 5900 50  0001 C CNN
	1    5250 5900
	-1   0    0    1   
$EndComp
Wire Wire Line
	5250 4650 5250 5700
Wire Wire Line
	6450 5600 6450 5700
Wire Wire Line
	5250 5700 6450 5700
Connection ~ 5250 5700
Wire Wire Line
	5250 5700 5250 5750
Connection ~ 6450 5700
Wire Wire Line
	6450 5700 6450 6150
$Comp
L power:+12V #PWR023
U 1 1 644D0E28
P 1650 7050
F 0 "#PWR023" H 1650 6900 50  0001 C CNN
F 1 "+12V" H 1665 7223 50  0000 C CNN
F 2 "" H 1650 7050 50  0001 C CNN
F 3 "" H 1650 7050 50  0001 C CNN
	1    1650 7050
	1    0    0    -1  
$EndComp
Connection ~ 1650 7550
Wire Wire Line
	1650 7550 1750 7550
Wire Wire Line
	1650 7050 1650 7150
Connection ~ 1650 7150
Wire Wire Line
	1650 7150 1750 7150
$Comp
L power:+12V #PWR024
U 1 1 645219CB
P 3600 1150
F 0 "#PWR024" H 3600 1000 50  0001 C CNN
F 1 "+12V" H 3615 1323 50  0000 C CNN
F 2 "" H 3600 1150 50  0001 C CNN
F 3 "" H 3600 1150 50  0001 C CNN
	1    3600 1150
	1    0    0    -1  
$EndComp
Wire Wire Line
	3450 1450 3600 1450
Wire Wire Line
	3600 1450 3600 1150
$Comp
L Connector:Conn_01x03_Male J10
U 1 1 6466C078
P 3250 1450
F 0 "J10" H 3400 1650 50  0000 C CNN
F 1 "O/C" H 3350 1250 50  0000 C CNN
F 2 "" H 3250 1450 50  0001 C CNN
F 3 "~" H 3250 1450 50  0001 C CNN
	1    3250 1450
	1    0    0    1   
$EndComp
Text Notes 3200 1450 2    50   ~ 0
red
Text Notes 3200 1350 2    50   ~ 0
yellow
Text Notes 3200 1550 2    50   ~ 0
black
$Comp
L Connector:Conn_01x05_Male J17
U 1 1 645FF66C
P 1950 1550
F 0 "J17" H 2050 2000 50  0000 C CNN
F 1 "Valve" H 2000 1900 50  0000 C CNN
F 2 "" H 1950 1550 50  0001 C CNN
F 3 "~" H 1950 1550 50  0001 C CNN
	1    1950 1550
	1    0    0    -1  
$EndComp
Wire Wire Line
	2150 1450 2700 1450
Wire Wire Line
	3450 1450 2800 1450
Wire Wire Line
	2700 1550 2150 1550
Connection ~ 3450 1450
Wire Wire Line
	2150 1650 3200 1650
Wire Wire Line
	2150 1750 3100 1750
Wire Wire Line
	2800 1450 2700 1550
Wire Wire Line
	2700 1450 2800 1550
Wire Wire Line
	2800 1550 3450 1550
$Comp
L Connector:Conn_01x05_Female J2
U 1 1 647E58BA
P 1750 1550
F 0 "J2" H 1650 2000 50  0000 L CNN
F 1 "Dongle" H 1500 1900 50  0000 L CNN
F 2 "" H 1750 1550 50  0001 C CNN
F 3 "~" H 1750 1550 50  0001 C CNN
	1    1750 1550
	1    0    0    -1  
$EndComp
Entry Wire Line
	900  1250 1000 1350
Entry Wire Line
	900  1350 1000 1450
Entry Wire Line
	900  1450 1000 1550
Entry Wire Line
	900  1550 1000 1650
Entry Wire Line
	900  1650 1000 1750
Wire Wire Line
	1550 1350 1000 1350
Wire Wire Line
	1000 1450 1550 1450
Wire Wire Line
	1550 1550 1000 1550
Wire Wire Line
	1000 1650 1550 1650
Wire Wire Line
	1000 1750 1550 1750
Text Notes 800  1000 0    50   ~ 0
To valve
Wire Wire Line
	3200 1650 3200 4300
Wire Wire Line
	3100 1750 3100 3900
Wire Wire Line
	3000 6300 3000 6500
Wire Wire Line
	3000 6300 3350 6300
Connection ~ 3000 6500
Wire Wire Line
	3000 6500 3350 6500
Wire Wire Line
	3000 6500 3000 7400
Wire Wire Line
	2700 7400 3000 7400
Text Notes 1500 1750 2    50   ~ 0
yellow
Text Notes 1500 1650 2    50   ~ 0
blue
Text Notes 1500 1450 2    50   ~ 0
red
Text Notes 1500 1350 2    50   ~ 0
green
Wire Wire Line
	5800 6250 6050 6250
$Comp
L Device:R R?
U 1 1 6627A51F
P 5650 6250
AR Path="/65DFE627/6627A51F" Ref="R?"  Part="1" 
AR Path="/6627A51F" Ref="R10"  Part="1" 
F 0 "R10" V 5550 6250 50  0000 C CNN
F 1 "10k" V 5650 6250 50  0000 C CNN
F 2 "" V 5580 6250 50  0001 C CNN
F 3 "~" H 5650 6250 50  0001 C CNN
	1    5650 6250
	0    -1   1    0   
$EndComp
$Comp
L Switch:SW_SPDT_SMALL SW2
U 1 1 66A5A149
P 5600 4500
F 0 "SW2" V 5400 4650 50  0001 L CNN
F 1 "Emergency Override" V 5600 4650 50  0001 L CNN
F 2 "" H 5550 4270 50  0001 C CNN
F 3 "~" H 5550 4270 50  0001 C CNN
	1    5600 4500
	0    1    1    0   
$EndComp
Text Notes 5750 4500 0    50   ~ 0
SW2\nEmergency\nOverride
Wire Wire Line
	3850 2150 4700 2150
Wire Wire Line
	8450 2500 9800 2500
Wire Wire Line
	8450 2600 9800 2600
Wire Bus Line
	900  1050 900  1650
$EndSCHEMATC

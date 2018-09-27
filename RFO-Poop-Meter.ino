// Arduino code for RFO septic ultrasonic sensor
//
// Author: David Kensiski
// Initial revision: 2018-03-01
//
// Required libraries:
// Grove RGB LCD: http://wiki.seeedstudio.com/Grove-LCD_RGB_Backlight/
// Bounce: https://playground.arduino.cc/Code/Bounce
// SoftReset: https://github.com/WickedDevice/SoftReset


#include <EEPROM.h>
#include <Wire.h>
#include <rgb_lcd.h>
#include <Bounce2.h>
#include <SoftReset.h>

String Version = "v1.4";


// Uncomment to slow things down and make it easier to debug
// #define DEBUG

/*
 *  Input/Output Pins
 */

#define heartLed	13		// onboard LED
#define poopPin   	1		// 0-5v analog
#define button1pin	4		// Menu button
#define button2pin	5		// Up button
#define button3pin	6		// Down button

#define EEPROM_MAGIC	0xCACA		// EEPROM bytes 0,1 to decect that we have valid data
#define EEPROM_CHECK_DELAY 3600000	// ms for regular check of eeprom updating (1h)
#define EEPROM_UPDATE_DELAY 60000	// ms to wait after a menu change before writing eeprom (60s)

#define DIM		0		// Display is currently dimmed
#define BRIGHT		1		// Display is currently bright
#define initTimeout	2000		// ms to display init screen
#define dimDelay	10000		// ms after button press to keep the display bright, then reset state machine
#define flashDelay	500		// ms between flashes
#define flashThreshold  96		// % full that will trigger flashing display
#define dimFactor	0.2		// how much to dim display
#define DEBOUNCE_MS	5		// how long our buttons can bounce
#define REBOOT_MS	86400000	// force a daily reboot
//#define REBOOT_MS	3600000		// 1h for testing

// Poop Level History:
// 9.2018: empty:450, full 935   -- Full dipped about 5" short of overflow
// 7.2018: empty:420, full:1010  -- Based on Greg's math
// 4.2018: empty:200, full:1024  -- Initial untested swags

#define POOP_HYSTERESIS	5		// Amount poopLevel may vary without reporting
#define POOP_EMPTY	420		// Raw value for empty tank
#define POOP_FULL	935		// Raw value for full tank



#define BUTTON_NONE	0		// no button pressed
#define BUTTON_MENU	2
#define BUTTON_UP	3
#define BUTTON_DN	4

#define UNPLUG_DELAY	5000		// ms delay for skipping hi/low water marks if sensor unplugged


/*
 *  Globals
 */

struct EEpromDataType {			// Data stored in EEPROM
	int magic;			// Value to ensure we have valid data
	int poopLowMark;		// Corresponding globals
	int poopHighMark;
	int poopEmpty;
	int poopFull;
	int greenMin;			// threshold[2][0]
	int yellowMin;			// threshold[1][0]
	int redMin;			// threshold[0][0]
	int flashMin;			// Global
	long writeCount;
} EEpromData;
unsigned long UpdateEepromTime = EEPROM_UPDATE_DELAY;	// when to write the EEPROM data
void printEeprom(String prefix);	// forward declaration so we can use it in setup()
long writeCount = 0;			// number of times EEPROM has been written

Bounce menuButton = Bounce();
Bounce upButton = Bounce();
Bounce dnButton = Bounce();

int heartBeatInterval = 500;		// ms between heart beat flashes
int poopReportInterval = 30000;		// ms between poop updates w/o change
int printInterval = 500;		// minimum millis between poopReport prints
unsigned long RebootMS = REBOOT_MS;	// in a global so we can extend if we're in a menu
unsigned long BootDelay = 5000;		// time to display boot message
unsigned long buttonTimeout = 0;	// time when button press times out (dimDelay)
int ButtonPressed = BUTTON_NONE;	// which button was pressed
unsigned long UnpluggedDelay = 0;	// Stop tracking hi/low water marks if sensor unplugged
bool SensorUnplugged = 0;		// Used to track notification of restore


int Brightness;				// Current display brightness (either DIM or BRIGHT)
int flashDisplay = 0;			// flag indicating whether or not we're flashing the display


// Finite State Machine to handle menus ------------------------------

// Note: to prevent name space conflicts:
// ...the enum varialbes start with uppercase S
// ...the function names start with lowcase s

typedef enum {S00_initialize = 0, S01_normal, S02_normal2, S02a_version, S02b_curPoop, S03_minPoop, S04_maxPoop, S05_emptyValue,
	S06_fullValue, S07_minGreenValue, S08_minYellowValue, S09_minRedValue, S10_minFlashValue, S11_resetDefaults,
	S12_confirmReset, S13_doReset, S99_reboot} State_type;
State_type curr_state;
State_type last_state;

// State Table definitions
void s00_initialize();  // forward declarations
void s01_normal();
void s02_normal2();
void s02a_version();
void s02b_curPoop();
void s03_minPoop();
void s04_maxPoop();
void s05_emptyValue();
void s06_fullValue();
void s07_minGreenValue();
void s08_minYellowValue();
void s09_minRedValue();
void s10_minFlashValue();
void s11_resetDefaults();
void s12_confirmReset();
void s13_doReset();
void s99_reboot();
void (*state_table[])() = {s00_initialize, s01_normal, s02_normal2, s02a_version, s02b_curPoop, s03_minPoop, s04_maxPoop, s05_emptyValue,
	s06_fullValue, s07_minGreenValue, s08_minYellowValue, s09_minRedValue, s10_minFlashValue, s11_resetDefaults,
	s12_confirmReset, s13_doReset, s99_reboot};



// Color LCD Stuff ------------------------------------------------------------

#define C_DEFAULT	0
#define C_OK		1
#define C_WARNING	2
#define C_PANIC		3

// Colors from https://www.w3schools.com/colors/colors_picker.asp
static int Color[4][4] = {
	{ 0, 0, 255 },		// C_DEFAULT: blue (used for boot)
	{ 0, 255, 0 },		// C_OK: green
	{ 255, 255, 0 },	// C_WARNING: yellow
	{ 255, 0, 0 },		// C_PANIC: red
};

static String ColorName[4] = {
	"Blue",
	"Green",
	"Yellow",
	"Red",
};

// Current color values -- global so we can dim
static int R;
static int G;
static int B;

// The actual LCD object!
rgb_lcd lcd;


// Poopy Stuff ------------------------------------------------------------

#define poopLevels 3
static int threshold[poopLevels][2] = {
	{ 75, C_PANIC },	// C_PANIC: red
	{ 50, C_WARNING },	// C_WARNING: orange
	{  0, C_OK },		// C_OK: green
};
int poopEmpty = POOP_EMPTY;	// Reading when empty
int poopFull = POOP_FULL;	// Reading when full
int poopLowMark = 9999;		// Lowest reading we've seen
int poopHighMark = -1;		// Highest reading we've seen
int poopLevel;			// Current poop level reading
int poopPercent;		// Current percent full between poopEmpty and poopFull
int flashMin = flashThreshold;	// % full when we start flashing


void setup()
{
	Serial.begin(115200);
	Serial.println("RFO Poop Meter " + Version);
	Serial.println("Preparing poopies!");
	Serial.println("Will update status every " + String(poopReportInterval / 1000, DEC) + " seconds");
	Serial.println("Will reboot every " + String(REBOOT_MS / 3600000, DEC) + " hours");
#ifdef DEBUG
	Serial.println("DEBUG mode enabled; recompile to turn off");
#endif

	lcd.begin(16, 2);
	R = Color[C_DEFAULT][0];
	G = Color[C_DEFAULT][1];
	B = Color[C_DEFAULT][2];
	lcd.setRGB(R,G,B);
	lcd.write("RFO Poop Meter");
	lcd.setCursor(0, 1);
	String msg1 = "Let's Poop! " + Version;
	lcd.write(msg1.c_str());

	Serial.println("Reading " + String(sizeof(EEpromData),DEC) + " bytes from EEPROM");
	EEPROM.get(0, EEpromData);
	printEeprom("<< ");
	if (EEpromData.magic == EEPROM_MAGIC) {
		Serial.println("EEPROM valid; populating data from EEPROM");
		poopLowMark = EEpromData.poopLowMark;
		poopHighMark = EEpromData.poopHighMark;
		poopEmpty = EEpromData.poopEmpty;
		poopFull = EEpromData.poopFull;
		threshold[2][0] = EEpromData.greenMin;
		threshold[1][0] = EEpromData.yellowMin;
		threshold[0][0] = EEpromData.redMin;
		flashMin = EEpromData.flashMin;
		writeCount = EEpromData.writeCount;
	} else {
		Serial.println("EEPROM not set; populating data with defaults");
		EEpromData.poopLowMark = poopLowMark;
		EEpromData.poopHighMark = poopHighMark;
		EEpromData.poopEmpty = poopEmpty;
		EEpromData.poopFull = poopFull;
		EEpromData.greenMin = threshold[2][0];
		EEpromData.yellowMin = threshold[1][0];
		EEpromData.redMin = threshold[0][0];
		EEpromData.flashMin = flashMin;
		EEpromData.writeCount = writeCount;
		UpdateEepromTime = millis() + 2000;  // flush to EEPROM after a few loops
	}

	pinMode(button1pin, INPUT);
	menuButton.attach(button1pin);
	menuButton.interval(DEBOUNCE_MS);

	pinMode(button2pin, INPUT);
	upButton.attach(button2pin);
	upButton.interval(DEBOUNCE_MS);

	pinMode(button3pin, INPUT);
	dnButton.attach(button3pin);
	dnButton.interval(DEBOUNCE_MS);

	pinMode(heartLed, OUTPUT);
	digitalWrite(heartLed, LOW);
}


// Flash the onboard LED so we know we're alive
void flashHeartBeat() {
	static int heartBeat = 0;	// toggle to flash onboard LED
	static unsigned long nextBeat = 0;
	if (millis() >= nextBeat) {
		heartBeat = !heartBeat;
		digitalWrite(heartLed, heartBeat ? HIGH : LOW);
		nextBeat = millis() + heartBeatInterval;
	}
}


// EEPROM functions -----------------------------------------------------------

void printEeprom(String prefix) {
	String msg = prefix +
		String(EEpromData.magic,HEX).c_str() +
		" L:" + String(EEpromData.poopLowMark,DEC).c_str() +
		" H:" + String(EEpromData.poopHighMark,DEC).c_str() +
		" E:" + String(EEpromData.poopEmpty,DEC).c_str() +
		" F:" + String(EEpromData.poopFull,DEC).c_str() +
		" G:" + String(EEpromData.greenMin,DEC).c_str() +
		" Y:" + String(EEpromData.yellowMin,DEC).c_str() +
		" R:" + String(EEpromData.redMin,DEC).c_str() +
		" X:" + String(EEpromData.flashMin,DEC).c_str() +
		" #:" + String(EEpromData.writeCount,DEC),c_str();
	Serial.println(msg);
}

// Update EEPROM immediately
void doEepromUpdate() {
	writeCount++;
	String msg = "Writing " + String(sizeof(EEpromData),DEC) + " bytes to EEPROM (" + String(writeCount,DEC) + " writes)";
	doPrint(msg);
	EEpromData.magic = EEPROM_MAGIC;
    	EEpromData.poopLowMark = poopLowMark;
	EEpromData.poopHighMark = poopHighMark;
	EEpromData.poopEmpty = poopEmpty;
	EEpromData.poopFull = poopFull;
	EEpromData.greenMin = threshold[2][0];
	EEpromData.yellowMin = threshold[1][0];
	EEpromData.redMin = threshold[0][0];
	EEpromData.flashMin = flashMin;
	EEpromData.writeCount = writeCount;
	printEeprom(">> ");
	EEPROM.put(0, EEpromData);
}

// Update EEPROM if timer has expired and data has changed
void maybeEepromUpdate() {
	if (millis() > UpdateEepromTime) {
		// Check if current data has changed from what's in eerpom
		EEpromDataType tempEEpromData;
		EEPROM.get(0, tempEEpromData);
		if (tempEEpromData.poopLowMark	<= poopLowMark &&
		    tempEEpromData.poopHighMark	>= poopHighMark &&
		    tempEEpromData.poopEmpty	== poopEmpty &&
		    tempEEpromData.poopFull	== poopFull &&
		    tempEEpromData.greenMin	== threshold[2][0] &&
		    tempEEpromData.yellowMin	== threshold[1][0] &&
		    tempEEpromData.redMin	== threshold[0][0] &&
		    tempEEpromData.flashMin	== flashMin &&
		    tempEEpromData.writeCount	== writeCount)
		{
		  	doPrint("EEPROM check: no update needed");
		} else {
			// And if so then write
			doEepromUpdate();
		}
		UpdateEepromTime = millis() + EEPROM_CHECK_DELAY;
	}
}

// Schedule EEPROM update real soon, but long enough out to prevent thrashing
void scheduleEepromUpdate() {
	UpdateEepromTime = millis() + EEPROM_UPDATE_DELAY;
}


// Status printing functions -----------------------------------------------------------

void doPrint(String msg) {
	Serial.println("[" + String(millis(),DEC) + "] " + msg);
}

// Check poop level and do stuff based on it
void checkPoopLevel() {
	static unsigned long nextPoopReport = 0;
	static unsigned long nextPrint = 0;
	static int lastColor = -1;
	static int lastPoopLevel = -1;
	
	// Read poop level
	poopLevel = analogRead(poopPin);

	// Detect unplugged sensor
	if (poopLevel == 0) {
		// Print log message when we first detect that sensor is unplugged
		if (!SensorUnplugged) {
			doPrint("Sensor appears to be unplugged");
			SensorUnplugged = 1;  // Watch for restore
		}
		// Skip tracking hi/low for a few seconds after restore to let sensor stabilize
		UnpluggedDelay = millis() + UNPLUG_DELAY;
	}

	// Track high/low water marks
	if (millis() >= UnpluggedDelay) {
		if (poopLevel > 0 && poopLevel < poopLowMark) {
			poopLowMark = poopLevel;
		}
		if (poopLevel > poopHighMark) {
			poopHighMark = poopLevel;
		}
	}

	// Watch for sensor restored
	if (SensorUnplugged && poopLevel > 0) {
		doPrint("Sensor restored");
		SensorUnplugged = 0;
	}

	// Calculate normalized percent full
	poopPercent = int((float)(poopLevel - poopEmpty) / (poopFull - poopEmpty) * 100);
	if (abs(lastPoopLevel - poopLevel) > POOP_HYSTERESIS) {   // prevent flapping
		lastPoopLevel = poopLevel;
		nextPoopReport = millis();  // report now
	}

	// Flash display if warranted
	if (poopPercent > flashMin) {
		flashDisplay = 1;
	} else {
		flashDisplay = 0;
	}

	int color;
	for (int i = 0; i < poopLevels; i++) {
		if (poopPercent >= threshold[i][0]) {
			color = threshold[i][1];
			break;
		}
	}

	if (millis() > BootDelay && color != lastColor) {
		BootDelay = 0;  // only during boot, right?
		R = Color[color][0];
		G = Color[color][1];
		B = Color[color][2];
		lcd.setRGB(R, G, B);
		lastColor = color;
		nextPoopReport = millis();  // report now
	}

	if (millis() >= nextPoopReport) {
		if (millis() >= nextPrint) {
			doPrint("Poop Code " + ColorName[color] + ": " + String(poopPercent, DEC) + "% (abs:" + String(poopLevel, DEC) + ")" +
				" Brt:" + String(Brightness,DEC) +
				" But:" + String(ButtonPressed,DEC) +
				" Low:" + String(poopLowMark,DEC) +
				" Hi:"  + String(poopHighMark,DEC) +
				" EEwrites:" + String(writeCount,DEC) +
				" Reboot:" + String((float)(RebootMS-millis())/3600000,2) + "h"
			);
			nextPrint = millis() + printInterval;  // prevent over-running serial port
		}
		nextPoopReport = millis() + poopReportInterval;
	}
}


void checkButtons() {
	menuButton.update();  // Required by Bounce
	upButton.update();
	dnButton.update();
	if (menuButton.rose()) {
		buttonTimeout = millis() + dimDelay;
		ButtonPressed = BUTTON_MENU;
	} else if (upButton.rose()) {
		buttonTimeout = millis() + dimDelay;
		ButtonPressed = BUTTON_UP;
	} else if (dnButton.rose()) {
		buttonTimeout = millis() + dimDelay;
		ButtonPressed = BUTTON_DN;
	}
}


// Dim display unless a condition exists to keep it bright
void dimDisplay() {
	static unsigned long nextFlash = 0;	

	// Button has been pressed
	if (millis() < buttonTimeout || millis() < BootDelay) {
		Brightness = BRIGHT;    

	// If we're flashing...
	} else if (flashDisplay) {
		// ...toggle brightness each flashDelay
		if (millis() > nextFlash) {
			Brightness = (Brightness == DIM) ? BRIGHT : DIM;
			nextFlash = millis() + flashDelay;
		}

	// Default is to dim display
	} else {
		Brightness = DIM;
		curr_state = (millis() < RebootMS) ? S01_normal : S99_reboot;   // And revert to normal or reboot
	}

	float factor = (Brightness==DIM) ? dimFactor : 1;
	int myR = R * factor;
	int myG = G * factor;
	int myB = B * factor;
	lcd.setRGB(int(R*factor), int(G*factor), int(B*factor));
}

void displayLCD(String msg0, String msg1) {
	if (millis() > BootDelay) {
		lcd.setCursor(0, 0);
		lcd.write((char *)msg0.c_str());
		lcd.setCursor(0, 1);
		lcd.write((char *)msg1.c_str());
	}
}


/*
 * 	State Machine ------------------------------------------------
 */


#define MSG_BOGUS	"Bogus Menu Entry"
#define MSG_MENU	"Menu            "
#define MSG_NEXT	"Next            "
#define MSG_NEXT_UP_DN	"Next   Up   Down"
#define MSG_NEXT_RESET	"Next       Reset"
#define MSG_CAN_RESET	"Cancel     Reset"

#define MSG_POOP  	"Poop level...   "
#define MSG_CUR_POOP  	"Cur poop        "
#define MSG_MIN_POOP  	"Low poop        "
#define MSG_MAX_POOP 	"High poop       "
#define MSG_EMPTY  	"Empty value     "
#define MSG_FULL  	"Full value      "
#define MSG_GREEN  	"Green min %     "
#define MSG_YELLOW  	"Yellow min %    "
#define MSG_RED  	"Red min %       "
#define MSG_FLASH  	"Flash min %     "
#define MSG_RESET  	"Reset defaults  "
#define MSG_CONFIRM  	"Are you f'sure? "
#define MSG_RESET1	"Resetting EEPROM"
#define MSG_RESET2	"...and rebooting"

#define MSG_REBOOT0	"SCHEDULED REBOOT"
#define MSG_REBOOT1	"Rebooting in    "
#define MSG_BOOM	"...snork!       "
  
void s00_initialize() {
	if (millis() > initTimeout) {
		curr_state = S01_normal;
	}
}

// Display code common to both S01 and S02
void s01_s02_display() {
	static int lastPoopLevel = -1;
	if (last_state != curr_state) {
		last_state = curr_state;
		ButtonPressed = BUTTON_NONE;
		lastPoopLevel = -1;  // force display update
	}
	if (lastPoopLevel != poopLevel) {
		String msg0 = "Poop level: " + String(poopPercent,DEC) + "%   ";
		displayLCD(msg0, MSG_MENU);
	}
}

void s01_normal() {
	s01_s02_display();
	//Serial.println("s01_normal: millis:" + String(millis(),DEC) + " reboot:" + String(REBOOT_MS,DEC));
	if (millis() > RebootMS) {
		curr_state = S99_reboot;
	}
	if (ButtonPressed != BUTTON_NONE) {
		curr_state = S02_normal2;
		ButtonPressed = BUTTON_NONE;
	}
}

void s02_normal2() {
	s01_s02_display();
	if (ButtonPressed == BUTTON_MENU) {
		curr_state = S02a_version;
		ButtonPressed = BUTTON_NONE;
	}
}

void s02a_version() {
	String msg0 = "Poop Meter " + Version + "  ";
	displayLCD(msg0, MSG_MENU);
	if (ButtonPressed == BUTTON_MENU) {
		curr_state = S02b_curPoop;
		ButtonPressed = BUTTON_NONE;
	}
}

void stringEmbed(String &msg, int value) {
	String valStr = String(value,DEC);
	msg.remove(msg.length() - valStr.length());
	msg.concat(valStr);
}

void s02b_curPoop() {
	if (last_state != curr_state) {
		last_state = curr_state;
		String msg0 = MSG_CUR_POOP;
		stringEmbed(msg0, poopLevel);
		displayLCD(msg0, MSG_NEXT);
	}
	if (ButtonPressed == BUTTON_MENU) {
		curr_state = S03_minPoop;
		ButtonPressed = BUTTON_NONE;
	}
}

void s03_minPoop() {
	if (last_state != curr_state) {
		last_state = curr_state;
		String msg0 = MSG_MIN_POOP;
		stringEmbed(msg0, poopLowMark);
		displayLCD(msg0, MSG_NEXT);
	}
	if (ButtonPressed == BUTTON_MENU) {
		curr_state = S04_maxPoop;
		ButtonPressed = BUTTON_NONE;
	}
}

void s04_maxPoop() {
	if (last_state != curr_state) {
		last_state = curr_state;
		String msg0 = MSG_MAX_POOP;
		stringEmbed(msg0, poopHighMark);
		displayLCD(msg0, MSG_NEXT);
	}
	if (ButtonPressed == BUTTON_MENU) {
		curr_state = S05_emptyValue;
		ButtonPressed = BUTTON_NONE;
	}
}

void doUpDown(String msg0, String msg1, int &var, int min, int max, State_type next) {
	if (last_state != curr_state) {
		last_state = curr_state;
		stringEmbed(msg0, var);
		displayLCD(msg0, msg1);
	}
	if (ButtonPressed == BUTTON_MENU) {
		curr_state = next;
	} else if (ButtonPressed == BUTTON_UP) {
		if (var < max) {
			var++;
			last_state = (State_type) -1;
			scheduleEepromUpdate();
		}
	} else if (ButtonPressed == BUTTON_DN) {
		if (var > min) {
			var--;
			last_state = (State_type) -1;
			scheduleEepromUpdate();
		}
	}
	ButtonPressed = BUTTON_NONE;
}

void s05_emptyValue() {
	doUpDown(MSG_EMPTY, MSG_NEXT_UP_DN, poopEmpty, 0, poopFull-1, S06_fullValue);
}

void s06_fullValue() {
	doUpDown(MSG_FULL, MSG_NEXT_UP_DN, poopFull, poopEmpty+1, 1024, S07_minGreenValue);
}

void s07_minGreenValue() {
	doUpDown(MSG_GREEN, MSG_NEXT_UP_DN, threshold[2][0], 0, threshold[1][0], S08_minYellowValue);
}

void s08_minYellowValue() {
	doUpDown(MSG_YELLOW, MSG_NEXT_UP_DN, threshold[1][0], threshold[2][0], threshold[0][0], S09_minRedValue);
}

void s09_minRedValue() {
	doUpDown(MSG_RED, MSG_NEXT_UP_DN, threshold[0][0], threshold[1][0], 100, S10_minFlashValue);
}

void s10_minFlashValue() {
	doUpDown(MSG_FLASH, MSG_NEXT_UP_DN, flashMin, threshold[0][0], 100, S11_resetDefaults);
}

void doYesNo(String msg0, String msg1, State_type next, State_type stateNo, State_type stateYes) {
	if (last_state != curr_state) {
		last_state = curr_state;
		displayLCD(msg0, msg1);
	}
	if (ButtonPressed == BUTTON_MENU) {
		curr_state = next;
	} else if (ButtonPressed == BUTTON_UP) {
		curr_state = stateNo;
	} else if (ButtonPressed == BUTTON_DN) {
		curr_state = stateYes;
	}
	ButtonPressed = BUTTON_NONE;
}
	
void s11_resetDefaults() {
	doYesNo(MSG_RESET, MSG_NEXT_RESET, S02_normal2, S11_resetDefaults, S12_confirmReset);
}

void s12_confirmReset() {
	doYesNo(MSG_CONFIRM, MSG_CAN_RESET, S02_normal2, S12_confirmReset, S13_doReset);
}

void s13_doReset() {
	displayLCD(MSG_RESET1, MSG_RESET2);
	String msg = "Zeroing out " + String(sizeof(EEpromData),DEC) + " bytes of EEPROM";
	Serial.println(msg);
	for (int a=0; a<=sizeof(EEpromData); a++) {
		EEPROM.write(a,0);
	}
	Serial.println("Rebooting");
	soft_restart();
}

void s99_reboot() {
	static int countdown = 10;
	static unsigned long nextCountdown = 0;
	if (last_state != curr_state) {
		countdown = 10;
		nextCountdown = millis()-1;
		last_state = curr_state;
	}
	if (ButtonPressed != BUTTON_NONE) {
		// Buttom press aborts countdown
		RebootMS = millis() + 11000;
		curr_state = S02_normal2;
		ButtonPressed = BUTTON_NONE;
	} else {
		if (millis() > nextCountdown) {
			if (countdown == 0) {
				UpdateEepromTime = 0;
				maybeEepromUpdate();
				displayLCD(MSG_REBOOT0, MSG_BOOM);
				Serial.println("Boom!");
				soft_restart();
			} else {
				String msg1 = MSG_REBOOT1;
				stringEmbed(msg1, countdown);
				displayLCD(MSG_REBOOT0, msg1);
				Serial.println("Scheduled reboot in " + String(countdown--,DEC) + " seconds");
				nextCountdown += 1000;
			}
		}
	}
}


/*
 * 	Main processing ------------------------------------------------
 */

void loop() {
	delay(100);
	flashHeartBeat();
	checkPoopLevel();
	checkButtons();
	dimDisplay();
	state_table[curr_state]();
	maybeEepromUpdate();

#ifdef DEBUG
	delay(100);  // Slow things down for sanity sake
#endif
}


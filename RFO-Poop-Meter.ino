// Arduino code for RFO septic ultrasonic sensor
//
// Author: David Kensiski
// Initial revision: 2018-03-01
//
// Required libraries:
// Grove RGB LCD: ???
// Bounce: https://playground.arduino.cc/Code/Bounce
// SoftReset: https://github.com/WickedDevice/SoftReset


#include <Wire.h>
#include <rgb_lcd.h>
#include <Bounce2.h>
#include <SoftReset.h>

rgb_lcd lcd;

// Uncomment to slow things down and make it easier to debug
// #define DEBUG

/*
 *  Input/Output Pins
 */

#define heartLed	13  // onboard LED
#define poopPin   	1   // 0-5v analog
#define button1pin	2   // Menu button
#define button2pin	3   // Up button
#define button3pin	4   // Down button


#define DIM		0   // Display is currently dimmed
#define BRIGHT		1   // Display is currently bright
#define initTimeout	2000   // ms to display init screen
#define dimDelay	10000  // ms after button press to keep the display bright, then reset state machine
#define flashDelay	500    // ms between flashes
#define flashThreshold  96     // % full that will trigger flashing display
#define dimFactor	0.2    // how much to dim display
#define DEBOUNCE_MS	5	// how long our buttons can bounce
//#define REBOOT_MS	2^32-3600000  // force a reboot 1h before our counter wraps
#define REBOOT_MS	3600000	// 1h for testing

#define POOP_HYSTERESIS 5	// Amount poopLevel may vary without reporting

#define BUTTON_NONE	0  // no button pressed
#define BUTTON_MENU	2
#define BUTTON_UP	3
#define BUTTON_DN	4


/*
 *  Globals
 */

Bounce menuButton = Bounce();
Bounce upButton = Bounce();
Bounce dnButton = Bounce();

int heartBeatInterval = 500;   // ms between heart beat flashes
int poopInterval = 30000;      // ms between poop updates w/o change
int doPrint;  // Flag to force maybePrint() to really print
unsigned long RebootMS = REBOOT_MS;  // in a global so we can extend if we're in a menu
unsigned long bootDelay = 5000;    // time to display boot message
unsigned long buttonTimeout = 0;   // time when button press times out (dimDelay)
int ButtonPressed = BUTTON_NONE;	   // which button was pressed


int Brightness;  // Current display brightness (either DIM or BRIGHT)
int flashDisplay = 0;  // flag indicating whether or not we're flashing the display


// Finite State Machine to handle menus ------------------------------

typedef enum {S00_Initialize = 0, S01_Normal, S02_Normal2, S03_MinPoop, S04_MaxPoop, S99_Reboot} State_type;
State_type curr_state;
State_type last_state;

// State Table definitions
void s00_initialize();  // forward declarations
void s01_normal();
void s02_normal2();
void s03_minPoop();
void s04_maxPoop();
void s99_reboot();
void (*state_table[])() = {s00_initialize, s01_normal, s02_normal2, s03_minPoop, s04_maxPoop, s99_reboot};



// Setup ------------------------------------------------------------

#define C_DEFAULT	0
#define C_OK		1
#define C_WARNING	2
#define C_PANIC		3


// Colors from https://www.w3schools.com/colors/colors_picker.asp
static int Color[4][4] = {
  { 0, 0, 255 },     // C_DEFAULT: blue (used for boot)
  { 0, 255, 0 },     // C_OK: green
  { 255, 255, 0 },   // C_WARNING: yellow
  { 255, 0, 0 },     // C_PANIC: red
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

#define poopLevels 3
static int threshold[poopLevels][2] = {
  { 75, C_PANIC },    // C_PANIC: red
  { 50, C_WARNING },  // C_WARNING: orange
  {  0, C_OK },       // C_OK: green
};
int poopLow  = 200;	// Reading when empty
int poopHigh = 1024;	// Reading when full
int poopLowMark = 9999;	// Lowest reading we've seen
int poopHighMark = -1;	// Highest reading we've seen
int poopLevel;		// Current poop level reading
int poopPercent;	// Current percent full between poopLow and poopHigh



void setup()
{
  // set up the LCD's number of columns and rows, set color, and write initial message:
  lcd.begin(16, 2);
//  color = C_DEFAULT;
  R = Color[C_DEFAULT][0];
  G = Color[C_DEFAULT][1];
  B = Color[C_DEFAULT][2];
  lcd.setRGB(R,G,B);
  lcd.write("RFO Poop Meter");
  lcd.setCursor(0, 1);
  lcd.write("Let's Poop! v0.1");

  Serial.begin(115200);
  Serial.println("Preparing poopies!");
  Serial.println("Will update status every " + String(poopInterval / 1000, DEC) + " seconds");
  Serial.println("Will reboot every " + String(REBOOT_MS / 3600000, DEC) + " hours");
#ifdef DEBUG
  Serial.println("DEBUG mode enabled; recompile to turn off");
#endif

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

// Print a message with timestamp -- regardless of throttling
// This is not currently in use: the algorithm is buggy and probably not worth the cycles anyway
// Let's let Python do that!
void dontPrint(String msg) {
  // format a timestamp
  unsigned long now = millis();
  int dec = int(now % 1000 / 100);  // pull off decimal seconds
  now = int(now / 1000);            // and convert to seconds
  int hh = int(now / 3600);
  int mm = int(int(now) % 3600 / 60);
  String mmz = mm < 10 ? "0" : "";
  int ss = int(now) % 60;
  String ssz = ss < 10 ? "0" : "";
  String timeStamp = String(hh, DEC) + ":" + mmz + String(mm, DEC) + ":" + ssz + String(ss, DEC) + "." + String(dec, DEC);
  // and print
  Serial.println(timeStamp + " " + msg);
}



static int printInterval = 500;  // millis between maybePrint()s
// Print a message but throttle so we don't overrun serial port
void maybePrint(String msg) {
  static unsigned long nextPrint = 0;
  if (millis() > nextPrint || doPrint == 1) {
    Serial.println("[" + String(millis(),DEC) + "] " + msg);
    doPrint = 0;
    nextPrint = millis() + printInterval;
  }
}


// Check poop level and do stuff based on it
void checkPoopLevel() {
  static unsigned long nextPoop = 0;
  static int lastColor = -1;
  static int lastPoopLevel = -1;

  // Read and normalize poop level
  poopLevel = analogRead(poopPin);
  if (poopLevel < poopLowMark) {
  	poopLowMark = poopLevel;
  }
  if (poopLevel > poopHighMark) {
  	poopHighMark = poopLevel;
  }

  // Calculate normalized percent full
  poopPercent = int((float)(poopLevel - poopLow) / (poopHigh - poopLow) * 100);
  if (abs(lastPoopLevel - poopLevel) > POOP_HYSTERESIS) {   // prevent flapping
    lastPoopLevel = poopLevel;
    nextPoop = millis();  // report now
  }

  // Flash display if warranted
  if (poopPercent > flashThreshold) {
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

  if (millis() > bootDelay && color != lastColor) {
    bootDelay = 0;  // only during boot, right?
    R = Color[color][0];
    G = Color[color][1];
    B = Color[color][2];
    lcd.setRGB(R, G, B);
    lastColor = color;
    nextPoop = millis();  // report now
  }

  if (millis() >= nextPoop || doPrint == 1) {
    maybePrint("Poop Code " + ColorName[color] + ": " + String(poopPercent, DEC) + "% (abs:" + String(poopLevel, DEC) + ") Brightness:" 
               + String(Brightness,DEC) + " ButtonPressed:" + String(ButtonPressed,DEC));
    nextPoop = millis() + poopInterval;
  }
}

int Menu = 0;

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
  if (millis() < buttonTimeout) {
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
    curr_state = (millis() < RebootMS) ? S01_Normal : S99_Reboot;   // And revert to normal or reboot
  }

  float factor = (Brightness==DIM) ? dimFactor : 1;
  int myR = R * factor;
  int myG = G * factor;
  int myB = B * factor;
  lcd.setRGB(int(R*factor), int(G*factor), int(B*factor));
}

void displayLCD(String msg0, String msg1) {
    lcd.setCursor(0, 0);
    lcd.write((char *)msg0.c_str());
    lcd.setCursor(0, 1);
    lcd.write((char *)msg1.c_str());
}
    

/*
 	State Machine ------------------------------------------------
*/


#define MSG_BOGUS	"Bogus Menu Entry"
#define MSG_MENU	"Menu            "
#define MSG_NEXT	"Next            "
#define MSG_NEXT_UP_DN	"Next   Up   Down"
#define MSG_NEXT_RESET	"Next       Reset"

#define MSG_POOP  	"Poop level...   "
#define MSG_MIN_POOP  	"Min poop        "
#define MSG_MAX_POOP 	"Max poop        "
#define MSG_EMPTY  	"Empty value     "
#define MSG_FULL  	"Full value      "
#define MSG_GREEN  	"Green max       "
#define MSG_YELLOW  	"Yellow min      "
#define MSG_RED  	"Red min         "
#define MSG_FLASH  	"Flash min       "
#define MSG_RESET  	"Reset defaults  "
#define MSG_CONFIRM  	"Are you sure?   "

#define MSG_REBOOT0	"SCHEDULED REBOOT"
#define MSG_REBOOT1	"Rebooting in    "
#define MSG_BOOM	"...snork!       "
  
void s00_initialize() {
	if (millis() > initTimeout) {
		curr_state = S01_Normal;
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
		curr_state = S99_Reboot;
	}
	if (ButtonPressed != BUTTON_NONE) {
		curr_state = S02_Normal2;
		ButtonPressed = BUTTON_NONE;
	}
}

void s02_normal2() {
	s01_s02_display();
	if (ButtonPressed == BUTTON_MENU) {
		curr_state = S03_MinPoop;
		ButtonPressed = BUTTON_NONE;
	}
}


void stringEmbed(String &msg, int value) {
	String valStr = String(value,DEC);
	msg.remove(msg.length() - valStr.length());
	msg.concat(valStr);
}

void s03_minPoop() {
	if (last_state != curr_state) {
		last_state = curr_state;
//		String value = String(poopLowMark,DEC);
//		String msg0 = MSG_MIN_POOP;
//		msg0.remove(msg0.length() - value.length());
//		msg0.concat(value);
		String msg0 = MSG_MIN_POOP;
		stringEmbed(msg0, poopLowMark);
		displayLCD(msg0, MSG_NEXT);
	}
	if (ButtonPressed == BUTTON_MENU) {
		curr_state = S04_MaxPoop;
		ButtonPressed = BUTTON_NONE;
	}
}

void s04_maxPoop() {
	if (last_state != curr_state) {
		last_state = curr_state;
		String msg0 = MSG_MAX_POOP;
		stringEmbed(msg0, poopHighMark);
//		String value = String(poopHighMark,DEC);
//		msg0.remove(msg0.length() - value.length());
//		msg0.concat(value);
		displayLCD(msg0, MSG_NEXT);
	}
	if (ButtonPressed == BUTTON_MENU) {
		curr_state = S02_Normal2;
		ButtonPressed = BUTTON_NONE;
	}
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
		curr_state = S02_Normal2;
		ButtonPressed = BUTTON_NONE;
	} else {
		if (millis() > nextCountdown) {
			if (countdown == 0) {
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
 	Main processing ------------------------------------------------
*/

void loop() {
  delay(100);
  flashHeartBeat();
  checkPoopLevel();
  checkButtons();
  dimDisplay();
  state_table[curr_state]();

#ifdef DEBUG
  delay(100);  // Slow things down for sanity sake
#endif
}


#include <Display.h>
#include <inttypes.h>
#include <Wire.h>

#define PEGGY_ADDRESS 1
#define I2C_INPUT_MAX_SIZE 26
#define WIDTH 25
#define TERMINATOR ';'
#define INITIATOR '^'

// This array of input must be global so that it can
// be accessed by the I2C library's service function
uint8_t i2cInput[I2C_INPUT_MAX_SIZE];
// Same is true of the inputCount
uint16_t inputCount = 0;
// The display object must be global so that it can be
// accessed inside the display refresh interrupt routine
Display disp;
  
void setup() {
  // I 2 C   S E T U P
  //Specify an address to set up Peggy as an I2C slave
  Wire.begin(PEGGY_ADDRESS);
  // Register the receiveEvent function with the library.
  Wire.onReceive(receiveEvent);

  // set pull up resistors on 4, 5 on PORTC.
  // These pins handle I2C comms.
  PORTC |= (1 << PC4) | (1 << PC5);

  // Call the display's initiatiion routine:
  disp.init();
}

void debugRow(char val) {
  if (val > WIDTH) 
    val = WIDTH;

  i2cInput[0] = 0;
  for (uint8_t col=0; col < val; col++) {
    i2cInput[col + 1] = 15;
  }
  for (uint8_t col=val; col < WIDTH; col++) {
    i2cInput[col + 1] = 0;
  }
  showRow();
}

void loop() {
  while(true) {
    disp.refresh();
    delay(2);
  }
}

/*
 * Read from the input, map onto display.
 */
void showRow() {
  uint8_t row = i2cInput[0];
  
  for (uint8_t col=0; col < WIDTH; col++) {
    
    disp.setCellBrightness(col, row, i2cInput[col + 1]);
  }
}

/*
 * Service function for the I2C library. When data is available
 * for receipt, this function will read it into a string.
 */
void receiveEvent(int numBytes) {
  while (Wire.available())
  {
    char c = Wire.receive();
    switch(c) {
      case INITIATOR:
        inputCount = 0;
        break;
      case TERMINATOR:
        inputCount = 0;
        showRow();
        break;
      default:
        i2cInput[inputCount++] = c;
    }
    if (inputCount >= I2C_INPUT_MAX_SIZE) {
      inputCount = 0;
    }
  }
}

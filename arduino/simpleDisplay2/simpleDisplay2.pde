#include <Peggy2.h>
#include <inttypes.h>
#include <Wire.h>

#define PEGGY_ADDRESS 1
#define WIDTH 25
#define INCR_Y '+'
#define START_FRAME '^'

Peggy2 frame1;
uint8_t y = 0;
uint8_t x = 0;

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
  frame1.HardwareInit();
}

void loop() {
  while(true) {
    frame1.RefreshAll(1);
    delay(1);
  }
}

void receiveEvent(int numBytes) {
  while (Wire.available())
  {
    char c = Wire.receive();
    if (c == START_FRAME) {
      y = 0;
      x = 0;
    }
    else if (c == INCR_Y) {
      x = 0;
      if (y < WIDTH)
        y++;

    }
    else {
      for (uint8_t i = 0; i < 8; i++) {
        if (x < WIDTH) {
          frame1.WritePoint(x, y, 1U & (c >> (7 - i)));
        }
        x++;
      }
    }
  }
}

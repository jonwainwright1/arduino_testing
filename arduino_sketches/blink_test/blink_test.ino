#include "Arduino_LED_Matrix.h"


ArduinoLEDMatrix matrix;
int y = 0;
int x = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(13, OUTPUT);
  matrix.begin();
}

void loop() {
  delay(50);
  // put your main code here, to run repeatedly:
  byte frame[8][12] = {
    {0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0}
  };


  frame[x][y] = 0;

  x += 1;

  if (x > 7) {
    x = 0;
    y += 1;
  }

  if (y > 11) {
    y = 0;
  }

  frame[x][y] = 1;

  matrix.renderBitmap(frame, 8, 12);
}

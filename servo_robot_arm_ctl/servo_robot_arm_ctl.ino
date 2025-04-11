#include <Servo.h>

#define KEY_PIN 19
#define ENC_S1_PIN 21
#define ENC_S2_PIN 20

#define BASE_SERVO_PIN 2 // PE4 (OC3B)
#define LINK1_SERVO_PIN 3 // PE5 (OC3C)
#define LINK2_SERVO_PIN 5 // PE3 (OC3A)

#define DUTY_MAX 125
#define DUTY_MIN 63

typedef enum {
  AXIS_NONE,
  AXIS_X,
  AXIS_Y,
  AXIS_Z,
  AXIS_MAX
} Axis_t;

/**
 * Create servo objects for each servo
 */
Servo baseServo, link1Servo, link2Servo;

int posBase = 90, posLink1 = 90, posLink2 = 90, posGripper = 90;
int posBaseSmoothed = 0, posLink1Smoothed = 0, posLink2Smoothed = 0;
int posBaseSmoothedPrev = 0, posLink1SmoothedPrev = 0, posLink2SmoothedPrev = 0;

Axis_t activeAxis = AXIS_NONE;

long keyPressedMillis = 0, actBlinkMillis = 0;

void setup() {
  Serial.begin(115200);

  // baseServo.attach(2);
  // link1Servo.attach(3);
  // link2Servo.attach(4);

  // baseServo.write(posBase);
  // link1Servo.write(posLink1);
  // link2Servo.write(posLink2);

  pinMode(LED_BUILTIN, OUTPUT);

  pinMode(BASE_SERVO_PIN, OUTPUT);
  pinMode(LINK1_SERVO_PIN, OUTPUT);
  pinMode(LINK2_SERVO_PIN, OUTPUT);
  int timerTop = 1250;

  // Set Fast PWM mode with TOP = ICR3
  TCCR3A |= (1 << WGM33) | (1 << WGM32);
  TCCR3B |= (1 << WGM31);

  // Clear 0C3A on compare match, set at BOTTOM (non-inverting mode)
  TCCR3A |= (1 << COM3A1) | (1 << COM3B1) | (1 << COM3C1);

  // Set TOP value
  ICR3 = timerTop;

  // Set duty cycle
  // OCR3B = 94;
  OCR3A = DUTY_MIN;
  OCR3B = DUTY_MIN;
  OCR3C = DUTY_MIN;

  // Start timer with prescaler 256
  TCCR3B |= (1 << CS32);

  EICRA |= (1 << ISC21);
  EIMSK |= (1 << INT0) | (1 << INT1) | (1 << INT2);

  sei();
}

void loop() {
  if (Serial.available() > 0)
  {
    String rawCmd = Serial.readStringUntil('\n');
    if (rawCmd.indexOf("BASE") != -1)
    {
      int basePos = 0;
      sscanf(rawCmd.c_str(), "BASE,%d\r\n", &basePos);
      // baseServo.write(basePos);
      OCR3B = basePos;

      Serial.println("Base move to: " + String(basePos));
    }
    if (rawCmd.indexOf("LINK1") != -1)
    {
      int link1Pos = 0;
      sscanf(rawCmd.c_str(), "LINK1,%d\r\n", &link1Pos);
      // link1Servo.write(link1Pos);
      OCR3C = link1Pos;

      Serial.println("Link 1 move to: " + String(link1Pos));
    }
    if (rawCmd.indexOf("LINK2") != -1)
    {
      int link2Pos = 0;
      sscanf(rawCmd.c_str(), "LINK2,%d\r\n", &link2Pos);
      // link2Servo.write(link2Pos);
      OCR3A = link2Pos;

      Serial.println("Link 2 move to: " + String(link2Pos));
    }
    if (rawCmd.indexOf("LED") != -1)
    {
      int ledDutyCycle = 0;
      sscanf(rawCmd.c_str(), "LED,%d\r\n", &ledDutyCycle);
      OCR0A = ledDutyCycle;

      Serial.println("LED duty: " + String(ledDutyCycle));
    }
  }

  if ((millis() - actBlinkMillis) > 2000)
  {
    actBlinkMillis = millis();
    // digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    Serial.println("TCCR3A: " + String(TCCR3A) + ", TCCR3B: " + String(TCCR3B) + ", ICR3: " + String(ICR3));
  }

}

ISR (INT1_vect, ISR_ALIASOF(INT0_vect));
ISR (INT0_vect)
{

}

ISR (INT2_vect)
{
  // Debounce key presses
  if ((millis() - keyPressedMillis) < 200) return;

  keyPressedMillis = millis();
  switch (activeAxis)
  {
    case AXIS_NONE:
    {
      activeAxis = AXIS_X;
      break;
    }
    case AXIS_X:
    {
      activeAxis = AXIS_Y;
      break;
    }
    case AXIS_Y:
    {
      activeAxis = AXIS_X;
      break;
    }
    default:
    {
      break;
    }
  }
}

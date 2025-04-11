
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#define KEY_PIN 19
#define ENC_S1_PIN 21
#define ENC_S2_PIN 20

#define BASE_SERVO_PIN 2 // PE4 (OC3B)
#define LINK1_SERVO_PIN 3 // PE5 (OC3C)
#define LINK2_SERVO_PIN 5 // PE3 (OC3A)

#define DUTY_MAX 125
#define DUTY_MIN 63

int main()
{
    int timerTop = 1250;

    DDRE |= (1 << DDE3) | (1 << DDE4) | (1 << DDE5);
    DDRB |= (1 << DD7);

    // Set Fast PWM mode with TOP = ICR3
    TCCR3A |= (1 << WGM33) | (1 << WGM32);
    TCCR3B |= (1 << WGM31);

    // Set Fast PWM mode with TOP = OCR0A
    TCCR0A |= (1 << WGM00) | (1 << WGM01);
    TCCR0B |= (1 << WGM02);

    // Clear 0C3A on compare match, set at BOTTOM (non-inverting mode)
    TCCR3A |= (1 << COM3A1) | (1 << COM3B1) | (1 << COM3C1);

    // Clear OCR0A on compare match, set at BOTTOM
    TCCR0A |= (1 << COM0A1);

    // Set TOP value
    ICR3 = timerTop;

    // Set TOP value
    OCR0A = 255;

    // Set duty cycle
    // OCR3B = 94;
    OCR3A = DUTY_MIN;
    OCR3B = DUTY_MIN;
    OCR3C = DUTY_MIN;

    // Set duty cycle
    OCR0A = 127;

    // Start timer with prescaler 256
    TCCR3B |= (1 << CS32);

    // Start timer with prescaler 1024
    TCCR0B |= (1 << CS00) | (1 << CS02);

    EICRA |= (1 << ISC21);
    EIMSK |= (1 << INT0) | (1 << INT1) | (1 << INT2);

    sei();

    while (1)
    {
        PORTB ^= (1 << PORTB7);
        _delay_ms(500);
    }
}

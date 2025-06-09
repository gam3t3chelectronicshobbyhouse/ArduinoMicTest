// Arduino UNO R3 Microphone check
// Created by Gam3t3ch Electronics
// Gam3t3ch.com  
// gam3t3ch@gmail.com
// https://www.youtube.com/gam3t3chelectronics
/ High?speed sampling (2 kHz), minimal overhead, raw ADC output


const uint8_t MIC_PIN = A0;
const unsigned long SAMPLE_INTERVAL_US = 500;  // 500µs ? 2000 Hz


void setup() {
  // Use highest serial speed to reduce latency
  Serial.begin(230400);
  // Speed up ADC: prescaler=32 ? ~38 kHz sample clock
  ADCSRA = (ADCSRA & ~0x07) | 0x05;
}


void loop() {
  unsigned long t0 = micros();
  int val = analogRead(MIC_PIN);
  Serial.println(val);
  // wait exactly SAMPLE_INTERVAL_US
  while (micros() - t0 < SAMPLE_INTERVAL_US) {}
}


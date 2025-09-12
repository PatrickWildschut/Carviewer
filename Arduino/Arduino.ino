// --- Pins ---
#define BRAKE_PIN   9
#define CLUTCH_PIN  10
#define RPM_AIN     A0    // RPM on analog A0
#define SPEED_AIN   A1    // Speed on analog A1

// --- Thresholds ---
// Counts = 1023 * V / 5.0 (Uno @ 5V)
// Wider hysteresis to mimic Schmitt behavior
const int RPM_HIGH_CNT     = 680;  // ~3.32 V
const int RPM_LOW_CNT      = 520;  // ~2.54 V
const int SPEED_HIGH_CNT   = 680;
const int SPEED_LOW_CNT    = 520;

// --- Pulse timing ---
const unsigned long MIN_PULSE_US     = 50;        // Ignore very short pulses
const unsigned long MAX_PULSE_US     = 1000000UL; // Ignore pulses > 1 sec
const unsigned long MIN_GLITCH_US    = 100;       // Filter glitch edges < 100 µs
const unsigned long RPM_TIMEOUT_US   = 1250000;   // 1.25 s = RPM 0
const unsigned long SPEED_TIMEOUT_US = 125000;    // 125 ms = Speed 0

// --- Channel state ---
struct PulseChan {
  uint8_t pin;
  int highCnt;
  int lowCnt;
  bool isHigh;
  unsigned long tRise;
  unsigned long lastWidth;
  unsigned long lastEdgeTime;
  unsigned long timeout;
  bool newWidth;
};

PulseChan rpmCh   = { RPM_AIN,   RPM_HIGH_CNT,   RPM_LOW_CNT,   false, 0, 0, 0, RPM_TIMEOUT_US,   false };
PulseChan speedCh = { SPEED_AIN, SPEED_HIGH_CNT, SPEED_LOW_CNT, false, 0, 0, 0, SPEED_TIMEOUT_US, false };

// --- Analog read with averaging ---
int analogReadAvg(uint8_t pin, uint8_t samples = 4) {
  long sum = 0;
  for (uint8_t i = 0; i < samples; i++) {
    sum += analogRead(pin);
  }
  return sum / samples;
}

// --- Update channel: pigpio-style edge detection ---
inline void updateChannel(PulseChan &ch) {
  int s = analogReadAvg(ch.pin, 4);  // 4-sample average
  unsigned long now = micros();

  if (!ch.isHigh) {
    // Wait for rising edge
    if (s >= ch.highCnt) {
      unsigned long delta = now - ch.lastEdgeTime;
      if (delta >= MIN_GLITCH_US) {
        ch.isHigh = true;
        ch.tRise = now;
        ch.lastEdgeTime = now;
      }
    } else {
      if (ch.timeout && (now - ch.lastEdgeTime > ch.timeout)) {
        ch.lastWidth = 0;
        ch.newWidth = true;
        ch.lastEdgeTime = now;
      }
    }
  } else {
    // Wait for falling edge
    if (s <= ch.lowCnt) {
      unsigned long delta = now - ch.lastEdgeTime;
      if (delta >= MIN_GLITCH_US) {
        unsigned long w = now - ch.tRise;
        if (w >= MIN_PULSE_US && w <= MAX_PULSE_US) {
          ch.lastWidth = w;
          ch.newWidth = true;
        }
        ch.isHigh = false;
        ch.lastEdgeTime = now;
      }
    } else {
      ch.lastEdgeTime = now;
    }
  }
}

// --- Convert pulse widths ---
inline float widthToRPM(unsigned long widthUs) {
  if (!widthUs) return 0.0f;
  float periodSec = widthUs / 1000000.0f;
  return (1.0f / periodSec) * 58.0f;
}

inline float widthToSpeed(unsigned long widthUs) {
  if (!widthUs) return 0.0f;
  float duration = widthUs / 10000.0f;
  return (1.0f / duration) * 36.0f;
}

// --- Setup ---
void setup() {
  Serial.begin(115200);
  pinMode(BRAKE_PIN,  INPUT);
  pinMode(CLUTCH_PIN, INPUT);

  // Faster ADC (prescaler /16 → ~13us per read)
  ADCSRA = (ADCSRA & 0xF8) | 0x04;

  rpmCh.lastEdgeTime = micros();
  speedCh.lastEdgeTime = rpmCh.lastEdgeTime;
}

// --- Main loop ---
void loop() {
  updateChannel(rpmCh);
  updateChannel(speedCh);

  static float rpm = 0.0f, speed = 0.0f;

  // --- If new pulse captured, convert ---
  if (rpmCh.newWidth) {
    float newRpm = widthToRPM(rpmCh.lastWidth);
    rpm = rpm * 0.8f + newRpm * 0.2f;  // smooth with alpha = 0.2
    rpmCh.newWidth = false;
  }

  if (speedCh.newWidth) {
    float newSpeed = widthToSpeed(speedCh.lastWidth);
    speed = speed * 0.8f + newSpeed * 0.2f;
    speedCh.newWidth = false;
  }

  // --- Read clutch and brake states ---
  bool clutch = digitalRead(CLUTCH_PIN);
  bool brake  = digitalRead(BRAKE_PIN);

  // --- Throttle print to 50 Hz (20 ms) ---
  static unsigned long nextPrint = 0;
  unsigned long now = micros();
  if ((long)(now - nextPrint) >= 0) {
    nextPrint = now + 20000UL;

    unsigned int rpm_u = (rpm < 0) ? 0u : (rpm > 9999 ? 9999u : (unsigned int)lroundf(rpm));

    char speedStr[8];
    dtostrf(speed, 5, 1, speedStr);  // format float
    for (int i = 0; i < 5; i++) { if (speedStr[i] == ' ') speedStr[i] = '0'; else break; }

    char buffer[20];
    snprintf(buffer, sizeof(buffer), "%s%04u%d%d", speedStr, rpm_u, clutch ? 1 : 0, brake ? 1 : 0);
    Serial.println(buffer);
  }
}

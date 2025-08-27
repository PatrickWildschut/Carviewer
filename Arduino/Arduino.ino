// --- Pins ---
#define BRAKE_PIN   9
#define CLUTCH_PIN  10
#define RPM_AIN     A0    // RPM on analog A0
#define SPEED_AIN   A1    // Speed on analog A1

// --- Thresholds (tune for each channel) ---
// Counts = 1023 * V / 5.0   (Uno @ 5V)
const int RPM_HIGH_CNT     = 640;  // ~3.12 V
const int RPM_LOW_CNT      = 560;  // ~2.73 V
const int SPEED_HIGH_CNT   = 640;  // ~3.12 V
const int SPEED_LOW_CNT    = 560;  // ~2.73 V

const unsigned long MIN_PULSE_US     = 50;       // ignore tiny glitches
const unsigned long RPM_TIMEOUT_US   = 125000;  // 1.25 s (no pulse -> 0)
const unsigned long SPEED_TIMEOUT_US = 125000;   // 125 ms

// --- Channel state machine ---
struct PulseChan {
  uint8_t pin;
  int highCnt;
  int lowCnt;
  bool  isHigh;
  unsigned long tRise;
  unsigned long lastWidth;    // last measured HIGH width (us)
  unsigned long lastEdgeTime; // last time we saw an edge (for timeout)
  unsigned long timeout;      // per-channel timeout
  bool  newWidth;             // flag: new pulse captured since last read
};

PulseChan rpmCh   = { RPM_AIN,   RPM_HIGH_CNT,   RPM_LOW_CNT,   false, 0, 0, 0, RPM_TIMEOUT_US,   false };
PulseChan speedCh = { SPEED_AIN, SPEED_HIGH_CNT, SPEED_LOW_CNT, false, 0, 0, 0, SPEED_TIMEOUT_US, false };

// Fast, non-blocking update: sample once and update state machine
inline void updateChannel(PulseChan &ch) {
  int s = analogRead(ch.pin);
  unsigned long now = micros();

  if (!ch.isHigh) {
    // Waiting for rising crossing
    if (s >= ch.highCnt) {
      ch.isHigh = true;
      ch.tRise = now;
      ch.lastEdgeTime = now;
    } else {
      // still low; check timeout → mark width=0 if stale
      if (ch.timeout && (now - ch.lastEdgeTime > ch.timeout)) {
        ch.lastWidth = 0;
        ch.newWidth = true; // report 0 once
        ch.lastEdgeTime = now;
      }
    }
  } else {
    // Currently high: waiting for falling crossing
    if (s <= ch.lowCnt) {
      unsigned long w = now - ch.tRise;
      if (w >= MIN_PULSE_US) {
        ch.lastWidth = w;
        ch.newWidth = true;
      }
      ch.isHigh = false;
      ch.lastEdgeTime = now;
    } else {
      // still high; keep alive to avoid false timeout
      ch.lastEdgeTime = now;
    }
  }
}

// Convert captured widths to your outputs (mirrors your original math)
inline float widthToRPM(unsigned long widthUs) {
  if (!widthUs) return 0.0f;
  float periodSec = widthUs / 1000000.0f;
  if (periodSec <= 0) return 0.0f;
  return (1.0f / periodSec) * 58.0f;
}

inline float widthToSpeed(unsigned long widthUs) {
  if (!widthUs) return 0.0f;
  float duration = widthUs / 10000.0f; // keep your original scaling path
  if (duration == 0.0f) return 0.0f;
  return (1.0f / duration) * 36.0f;
}

void setup() {
  Serial.begin(115200);
  pinMode(BRAKE_PIN,  INPUT);
  pinMode(CLUTCH_PIN, INPUT);

  // Speed up ADC: prescaler /16 (~13 µs per analogRead)
  // (Default is /128 ≈ 104 µs; /8 is faster but noisier—try /16 first.)
  ADCSRA = (ADCSRA & 0xF8) | 0x04; // 0x04 -> /16

  rpmCh.lastEdgeTime   = micros();
  speedCh.lastEdgeTime = rpmCh.lastEdgeTime;
}

void loop() {
  // Update both channels every loop (non-blocking, just one sample each)
  updateChannel(rpmCh);
  updateChannel(speedCh);

  static float rpm = 0.0f, speed = 0.0f;

  // If we captured a new pulse width, update the value
  if (rpmCh.newWidth) {
    rpm = widthToRPM(rpmCh.lastWidth);
    rpmCh.newWidth = false;
  }
  if (speedCh.newWidth) {
    speed = widthToSpeed(speedCh.lastWidth);
    speedCh.newWidth = false;
  }

  bool clutch = digitalRead(CLUTCH_PIN);
  bool brake  = digitalRead(BRAKE_PIN);

  // Throttle prints to, say, 50 Hz
  static unsigned long nextPrint = 0;
  unsigned long now = micros();
  if ((long)(now - nextPrint) >= 0) {
    nextPrint = now + 20000UL; // 20 ms

    unsigned int rpm_u = (rpm < 0) ? 0u : (rpm > 9999 ? 9999u : (unsigned int)lroundf(rpm));

    char speedStr[8];
    dtostrf(speed, 5, 1, speedStr);
    for (int i = 0; i < 5; i++) { if (speedStr[i] == ' ') speedStr[i] = '0'; else break; }

    char buffer[20];
    snprintf(buffer, sizeof(buffer), "%s%04u%d%d", speedStr, rpm_u, clutch ? 1 : 0, brake ? 1 : 0);
    Serial.println(buffer);
  }
}

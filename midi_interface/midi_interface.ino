#include <AccelStepper.h>

// Define step, direction, and enable pins for AccelStepper
#define STEP_X_PIN 2
#define DIR_X_PIN 5
#define ENABLE_PIN 8

#define STEP_Y_PIN 3
#define DIR_Y_PIN 6

#define STEP_Z_PIN 4
#define DIR_Z_PIN 7

#define STEP_A_PIN 12
#define DIR_A_PIN 13

#define STEP_B_PIN 11
#define DIR_B_PIN 10

// Create an AccelStepper object
AccelStepper stepperA(AccelStepper::DRIVER, STEP_X_PIN, DIR_X_PIN);
AccelStepper stepperB(AccelStepper::DRIVER, STEP_Z_PIN, DIR_Z_PIN);
AccelStepper stepperC(AccelStepper::DRIVER, STEP_Y_PIN, DIR_Y_PIN);
AccelStepper stepperD(AccelStepper::DRIVER, STEP_A_PIN, DIR_A_PIN);
AccelStepper stepperE(AccelStepper::DRIVER, STEP_B_PIN, DIR_B_PIN);

// Create motors array
AccelStepper motors[] = {stepperA, stepperB, stepperC, stepperD, stepperE};
// Make this dynamic in case motor array changes
bool motorsRunning[sizeof(motors) / sizeof(motors[0])] = {false};

void setup()
{
  // Enable the motors
  pinMode(ENABLE_PIN, OUTPUT);
  digitalWrite(ENABLE_PIN, LOW);
  Serial.begin(115200);
  for (unsigned int i = 0; i < sizeof(motors) / sizeof(motors[0]); i++)
  {
    motors[i].setMaxSpeed(2000);     // Set a default max speed
    motors[i].setAcceleration(1000); // Set a default acceleration
  }
}

void loop()
{
  if (Serial.available() > 0)
  {
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove any whitespace
    command.toLowerCase();

    if (command.startsWith("s"))
    {
      // Ensure the motors are enabled
      digitalWrite(ENABLE_PIN, LOW);
      // Command looks like "s,0,2000", as in start, motor 0, speed 2000
      int motorIndex = command.substring(2, 3).toInt();
      float speed = command.substring(4).toFloat();
      motors[motorIndex].setSpeed(speed); // Set the desired speed
      motors[motorIndex].runSpeed();      // Start the motor
      motorsRunning[motorIndex] = true;   // Set the flag to indicate the motor is running
    }
    else if (command.startsWith("e"))
    {
      // Command looks like "e,0", as in end, motor 0
      int motorIndex = command.substring(2).toInt();
      motors[motorIndex].stop();         // Initiate the stop
      motorsRunning[motorIndex] = false; // Clear the flag as the motor is not running anymore
    }
    else if (command.startsWith("d"))
    {
      // Disable the motors
      digitalWrite(ENABLE_PIN, HIGH);
    }
  }

  // Loop through the motors and check if they are running
  // If they are, ensure they are running at the set speed
  for (unsigned int i = 0; i < sizeof(motors) / sizeof(motors[0]); i++)
  {
    if (motorsRunning[i])
    {
      if (motors[i].isRunning())
      {
        motors[i].runSpeed();
      }
      else
      {
        motorsRunning[i] = false;
      }
    }
  }
}
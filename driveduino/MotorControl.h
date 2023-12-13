#ifndef MOTORCONTROL_H
#define MOTORCONTROL_H

#include "constants.h"
#include "Arduino.h"

void setupMotors();
void stop();
void setSpeed(int mot, int speed);
void setSpeedAll(const int speedArray[4]);
void driveMotor(int motor, bool direction, int speed);
void driveMotorAll(const int speedArray[4]);

void forwardSlow();
void reverseSlow();
void rightSlow();
void leftSlow();

void forwardFast();
void reverseFast();
void rightFast();
void leftFast();

void diagNESlow();
void diagSESlow();
void diagSWSlow();
void diagNWSlow();

#endif

#ifndef MOTORCONTROL_H
#define MOTORCONTROL_H

#include "constants.h"
#include "Arduino.h"

void setupMotors();
int stop();
void setSpeed(int mot, int speed);
void setSpeedAll(const int speedArray[4]);
void driveMotor(int motor, bool direction, int speed);
void driveMotorAll(const int speedArray[4]);

int forwardSlow();
int reverseSlow();
int rightSlow();
int leftSlow();

int forwardFast();
int reverseFast();
int rightFast();
int leftFast();

int diagNESlow();
int diagSESlow();
int diagSWSlow();
int diagNWSlow();

#endif

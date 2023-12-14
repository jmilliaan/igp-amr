#include "MotorControl.h"

void setupMotors(){
  for (int i = 0; i < numMotors; i++) {
    pinMode(motorPins[i][0], OUTPUT); // V
    pinMode(motorPins[i][1], OUTPUT); // A
    pinMode(motorPins[i][2], OUTPUT); // B

    // Initialize motors to a default state (e.g., low speed and stopped)
    analogWrite(motorPins[i][0], 64); // Default speed
    digitalWrite(motorPins[i][1], LOW);
    digitalWrite(motorPins[i][2], LOW);
  };
};

int stop(){
  int stopSpeedArray[] = {0, 0, 0, 0};
  setSpeedAll(stopSpeedArray);
  return 1;
};

void setSpeed(int mot, int speed){
  analogWrite(motorPins[mot-1][0], speed);
};

void setSpeedAll(const int speedArray[4]){
  for(int i = 0; i < numMotors; i++){
      setSpeed(i + 1, speedArray[i]);
  };
};

void driveMotor(int motor, bool direction, int speed){
  setSpeed(motor, speed);
  digitalWrite(motorPins[motor - 1][1], direction);
  digitalWrite(motorPins[motor - 1][2], !direction);
};

void driveMotorAll(const int speedArray[4], const int directionArray[4]){
  for (int i = 0; i < numMotors; i++){
      driveMotor(i + 1, directionArray[i], speedArray[i]);
  };
}; 

int forwardSlow(){
  int directionArray[4] = {1, 1, 1, 1}; 
  driveMotorAll(globalSlowSpeed_arr, directionArray);
  return 2;
};
int reverseSlow(){
  int directionArray[4] = {0, 0, 0, 0}; 
  driveMotorAll(globalSlowSpeed_arr, directionArray);
  return 3;
};
int rightSlow(){
  int directionArray[4] = {0, 1, 1, 0}; 
  driveMotorAll(globalSlowSpeed_arr, directionArray);
  return 4;
};
int leftSlow(){
  int directionArray[4] = {1, 0, 0, 1}; 
  driveMotorAll(globalSlowSpeed_arr, directionArray);
  return 5;
};

int forwardFast(){};
int reverseFast(){};
int rightFast(){};
int leftFast(){};

int diagNESlow(){};
int diagSESlow(){};
int diagSWSlow(){};
int diagNWSlow(){};



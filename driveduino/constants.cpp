#include "constants.h"

// MOTOR PINS
const int numMotors = 4;
int motorPins[4][3] = {
    {6, 2, 3},     // Motor 1: V (velocity), A (digital 1), B (digital 2)
    {9, 4, 5},     // Motor 2: V, A, B
    {11, 7, 8},    // Motor 3: V, A, B
    {10, 13, 12}   // Motor 4: V, A, B
};
int globalSlowSpeed = 100;
int globalHighSpeed = 200;
int globalSlowSpeed_arr[4] = {
    globalSlowSpeed, 
    globalSlowSpeed, 
    globalSlowSpeed, 
    globalSlowSpeed
    };

// SERIAL COMMUNICATION
const int baudRate = 9600;

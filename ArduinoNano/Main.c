#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <stdint.h>
  
Adafruit_BNO055 bno = Adafruit_BNO055(55);
 
void setup(void) 
{
  Serial.begin(115200);
  
  /* Initialise the sensor */
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    while(1);
      Serial.write(0x88);
  }
  
    
  bno.setExtCrystalUse(true);
}

// In DNA sequences, a protein sequence's beginning
// is denoted by a "TATA" group,
// which is the letters ATATATAT repeating,
// and my "TATA" group to signal over serial
// that a communication is beginning is 0xffaaffbb
uint32_t TATA_Value = 0xffaaffbb;
byte* TATA_Pointer = (byte*)&TATA_Value;

void loop(void) 
{
  sensors_event_t event; 
  bno.getEvent(&event);

  imu::Vector<3> grav = bno.getVector(Adafruit_BNO055::VECTOR_GRAVITY);
  imu::Vector<3> rot = bno.getVector(Adafruit_BNO055::VECTOR_EULER);
  imu::Vector<3> accel = bno.getVector(Adafruit_BNO055::VECTOR_LINEARACCEL);

  Serial.write(TATA_Pointer, 4);
  
  // I believe that each of these groups could be written in a single statement
  // But this works, and i'm tired of debugging arduinos
  Serial.write((byte*)&grav.x(), 4);
  Serial.write((byte*)&grav.y(), 4);
  Serial.write((byte*)&grav.z(), 4);
  
  Serial.write((byte*)&rot.x(), 4);
  Serial.write((byte*)&rot.y(), 4);
  Serial.write((byte*)&rot.z(), 4);
  
  Serial.write((byte*)&accel.x(), 4);
  Serial.write((byte*)&accel.y(), 4);
  Serial.write((byte*)&accel.z(), 4);
}

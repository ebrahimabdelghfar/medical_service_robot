#include<Arduino.h>
#include "PinChangeInterrupt.h"
// Pins Right motor
#define ENCA 2
#define ENCB 3
#define PWM 5
#define IN1 8
#define IN2 7
#define enable A0
//end

// Pins left motor
#define ENCC 12
#define ENCD 11
#define PWM2 6
#define IN3 4
#define IN4 9
#define enable_m2 A1
//end
volatile int pos_i = 0;
void readEncoder(){
  // Read encoder B when ENCD rises
  int b = digitalRead(ENCD);
  int increment = 0;
  if(b>0){
    // If B is high, increment forward
    increment = 1;
  }
  else{
    // Otherwise, increment backward
    increment = -1;
  }
  pos_i = pos_i + increment;
}

volatile int pos_i_L = 0;
void readEncoder_L(){
  // Read encoder B when ENCA rises
  int b = digitalRead(ENCB);
  int increment = 0;
  if(b>0){
    // If B is high, increment forward
    increment = 1;
  }
  else{
    // Otherwise, increment backward
    increment = -1;
  }
  pos_i_L = pos_i_L + increment;
}

void setMotor(int dir, int pwmVal, int pwm, int in1, int in2){
  analogWrite(pwm,pwmVal); // Motor speed
  if(dir == 1){ 
    // Turn one way
    digitalWrite(in1,HIGH);
    digitalWrite(in2,LOW);
  }
  else if(dir == -1){
    // Turn the other way
    digitalWrite(in1,LOW);
    digitalWrite(in2,HIGH);
  }
  else{
    // Or dont turn
    digitalWrite(in1,LOW);
    digitalWrite(in2,LOW);    
  }
}


void setup() {
  Serial.begin(9600);

  pinMode(ENCA,INPUT);
  pinMode(ENCB,INPUT);

  pinMode(ENCC,INPUT);
  pinMode(ENCD,INPUT);

  pinMode(PWM,OUTPUT);
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);

  pinMode(PWM2,OUTPUT);
  pinMode(IN3,OUTPUT);
  pinMode(IN4,OUTPUT);

  pinMode(enable,OUTPUT);
  pinMode(enable_m2,OUTPUT);

  digitalWrite(enable_m2,HIGH); 
  digitalWrite(enable,HIGH);

  attachInterrupt(digitalPinToInterrupt(ENCA),readEncoder_L,RISING);
  attachPCINT(digitalPinToPCINT(ENCC),readEncoder,RISING); 
}

// globals for motor_R
long prevT = 0;
float eprev = 0;
float vt = 44;
float cond=0;
int posPrev = 0;
float v1Filt = 0;
float v1Prev = 0;
float eintegral = 0;
//end
int PID_R(){
  int pos = 0;
  pos = pos_i;
  // Compute velocity with method 1
  long currT = micros();
  float deltaT = ((float) (currT-prevT))/1.0e6;
  float velocity1 = (pos - posPrev)/deltaT;
  posPrev = pos;
  prevT = currT;
  // Convert count/s to RPM
  float v1 = velocity1/320*60.0;
  // Low-pass filter (25 Hz cutoff)
  v1Filt = 0.854*v1Filt + 0.0728*v1 + 0.0728*v1Prev;
  v1Prev = v1;
  // Compute the control signal u
  float kp = 2.5;
  float ki = 0.5;
  float kd = 0.08;
  float e = vt-v1Filt;
  eintegral = eintegral + e*deltaT;
  float dedt = (e-eprev)/(deltaT);
  float u = kp*e + ki*eintegral+dedt*kd;
  eprev = e;
  return u;
}


// globals for motor_L
long prevT_L = 0;
float eprev_L = 0;
float vt_L = 44;
float cond_L=0;
int posPrev_L = 0;
float eintegral_L = 0;
float v2Filt = 0;
float v2Prev = 0;
//end
int PID_L(){
  int pos = 0;
  pos = pos_i_L;
  // Compute velocity with method 1
  long currT = micros();
  float deltaT = ((float) (currT-prevT_L))/1.0e6;
  float velocity2 = (pos - posPrev_L)/deltaT;
  posPrev_L = pos;
  prevT_L = currT;
  // Convert count/s to RPM
  float v2 = velocity2/320*60.0;
  // Low-pass filter (25 Hz cutoff)
  v2Filt = 0.854*v2Filt + 0.0728*v2 + 0.0728*v2Prev;
  v2Prev = v2;
  // Compute the control signal u
  float kp = 2.5;
  float ki = 0.5;
  float kd = 0.08;
  float e = vt-v2Filt;
  eintegral_L = eintegral_L + e*deltaT;
  float dedt = (e-eprev_L)/(deltaT);
  float u_L = kp*e + ki*eintegral_L+dedt*kd;
  eprev_L = e;
  return u_L;
}


void loop() {
  // Set a target
  if(Serial.available()>0){
      cond = Serial.parseFloat();              //Read user input and hold it in a variable
    }    
  if (cond>-10 && cond<10){
    vt=0;        
  }
  else if(cond>250){
    vt=250;
  }
  else if(cond<-250){
    vt=-250;
  }
  else{
    vt=cond;
  }
  // Set the motor speed and direction
  int pwr_R= PID_R();
  int pwr_l= PID_L();
  int dir = 1;
  int dir_l = 1;
  if (pwr_R<0){
    dir = -1;
  }
  if (pwr_l<0){
    dir_l = -1;
  }
   pwr_R =(int)fabs(pwr_R);
   pwr_l =(int)fabs(pwr_l);
  if(pwr_R > 255){
    pwr_R = 255;
  }

  if(pwr_l > 255){
    pwr_l = 255;
  }
  setMotor(dir_l,pwr_l,PWM,IN1,IN2);
  setMotor(dir,pwr_R,PWM2,IN3,IN4);
  int HE=255;
  Serial.println(v1Filt);
  Serial.print(" ");
  Serial.print(vt);
  Serial.print(" ");
  Serial.print(v2Filt);
  Serial.print(" ");
  Serial.print(HE);
  Serial.print(" ");
  delay(1);
}

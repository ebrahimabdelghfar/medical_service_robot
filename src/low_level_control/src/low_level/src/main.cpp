#include<Arduino.h>
// Pins
#define ENCA 3
#define ENCB 2
#define PWM 5
#define IN1 7
#define IN2 8
#define enable A0

// globals
long prevT = 0;
float eprev = 0;


  float vt = 44;
  float cond=0;



int posPrev = 0;
// Use the "volatile" directive for variables
// used in an interrupt
volatile int pos_i = 0;
volatile float velocity_i = 0;
volatile long prevT_i = 0;

float v1Filt = 0;
float v1Prev = 0;
float v2Filt = 0;
float v2Prev = 0;

float eintegral = 0;

void readEncoder(){
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
  pos_i = pos_i + increment;

  // Compute velocity with method 2
  long currT = micros();
  float deltaT = ((float) (currT - prevT_i))/1.0e6;
  velocity_i = increment/deltaT;
  prevT_i = currT;
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
  pinMode(PWM,OUTPUT);
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  pinMode(enable,OUTPUT);
  digitalWrite(enable,HIGH);    

  attachInterrupt(digitalPinToInterrupt(ENCA),readEncoder,RISING);
}

void loop() {

  int pos = 0;
  float velocity2 = 0;
  pos = pos_i;
  velocity2 = velocity_i;
  

  // Compute velocity with method 1
  long currT = micros();
  float deltaT = ((float) (currT-prevT))/1.0e6;
  float velocity1 = (pos - posPrev)/deltaT;
  posPrev = pos;
  prevT = currT;

  // Convert count/s to RPM
  float v1 = velocity1/320*60.0;
  float v2 = velocity2/320*60.0;

  // Low-pass filter (25 Hz cutoff)
  v1Filt = 0.854*v1Filt + 0.0728*v1 + 0.0728*v1Prev;
  v1Prev = v1;
  v2Filt = 0.854*v2Filt + 0.0728*v2 + 0.0728*v2Prev;
  v2Prev = v2;
  
  // Set a target
  //float vt = 250*sin(prevT/1e6);
  if(Serial.available()>0){
      cond = Serial.parseFloat();              //Read user input and hold it in a variable
    }    
    if (cond>-10 && cond<10){
      vt=0;        
    }else if(cond>250){
      vt=250;
    }else if(cond<-250){
      vt=-250;
    }else{
      vt=cond;}
  
  // Compute the control signal u
  float kp = 2.5;
  float ki = 0.5;
  float kd = 0.08;
  float e = vt-v1Filt;
  eintegral = eintegral + e*deltaT;
  float dedt = (e-eprev)/(deltaT);

  float u = kp*e + ki*eintegral+dedt*kd;

  // Set the motor speed and direction
  int dir = 1;
  if (u<0){
    dir = -1;
  }
  int pwr = (int) fabs(u);
  if(pwr > 255){
    pwr = 255;
  }
  setMotor(dir,pwr,PWM,IN1,IN2);
  eprev = e;
  
  int gra = 250;

  Serial.print(vt);
  Serial.print(" ");
  Serial.print(v1Filt);
  Serial.print(" ");

  Serial.print(gra);
  Serial.println();

  delay(1);
}
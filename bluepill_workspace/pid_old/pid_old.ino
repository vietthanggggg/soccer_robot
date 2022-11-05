// Pins Motor1
#define ENCA_1 PA4 
#define ENCB_1 PA5 
#define IN1_1 PB4
#define IN2_1 PB5
#define PWM_1 PB6

// Pins Motor2
#define ENCA_2 3
#define ENCB_2 8
#define PWM_2 9
#define IN1_2 10
#define IN2_2 11

float d=15;
unsigned long time=0;

// globals
long prevT = 0;
int posPrev = 0;

long prevP = 0;
int posPrevP = 0;

// Use the "volatile" directive for variables
// used in an interrupt
volatile int pos_i = 0;
volatile float velocity_i = 0;
volatile long prevT_i = 0;

volatile int pos_ip = 0;
volatile float velocity_ip = 0;
volatile long prevT_ip = 0;

float v1Filt = 0;
float v1Prev = 0;
float v2Filt = 0;
float v2Prev = 0;

float eintegral1 = 0,eintegral2 = 0;
float ederivative = 0;
float vtp ,vtt ;
//use in set motor
int dirt,pwrt,dirp,pwrp;
void setup() {
  Serial.begin(9600);
  
  pinMode(ENCA_1,INPUT);
  pinMode(ENCB_1,INPUT);
  pinMode(PWM_1,OUTPUT);
  pinMode(IN1_1,OUTPUT);
  pinMode(IN2_1,OUTPUT);
  pinMode(ENCA_2,INPUT);
  pinMode(ENCB_2,INPUT);
  pinMode(PWM_2,OUTPUT);
  pinMode(IN1_2,OUTPUT);
  pinMode(IN2_2,OUTPUT);

  attachInterrupt(digitalPinToInterrupt(ENCA_1),
                  readEncodertrai,RISING);
  attachInterrupt(digitalPinToInterrupt(ENCA_2),
                  readEncoderphai,FALLING);                 
}
void loop() {
  Serial.print(vtt);
  Serial.print("\t");
  Serial.println(v1Filt);
  PIDt (100);
  setMotort(dirt,pwrt,PWM_1,IN1_1,IN2_1);
  delay(10);
}




void setMotort(int dir, int pwmVal, int pwm, int in1, int in2){
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
void setMotorp(int dir, int pwmVal, int pwm, int in1, int in2){
  analogWrite(pwm,pwmVal); // Motor speed
  if(dir == 1){ 
     // Turn one way
    digitalWrite(in2,HIGH);
    digitalWrite(in1,LOW);
  }
  else if(dir == -1){
    // Turn the other way
    digitalWrite(in2,LOW);
    digitalWrite(in1,HIGH);
  }
  else{
    // Or dont turn
    digitalWrite(in1,LOW);
    digitalWrite(in2,LOW);    
  }
}

void readEncodertrai(){
  // Read encoder B when ENCA_1 rises
  int b = digitalRead(ENCB_1);
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
void readEncoderphai(){
  // Read encoder B when ENCA_1 rises
  int b = digitalRead(ENCB_2);
  int increment = 0;
  if(b>0){
    // If B is high, increment forward
    increment = 1;
  }
  else{
    // Otherwise, increment backward
    increment = -1;
  }
  pos_ip = pos_ip + increment;

}

//PID
void PIDt( float vtt)
{
// Compute the control signal u
int pos = 0;

  noInterrupts(); // disable interrupts temporarily while reading
  pos = pos_i;
  interrupts(); // turn interrupts back on
long currT = micros();
  float deltaT = ((float) (currT-prevT))/1.0e6;
  float velocity1 = (pos - posPrev)/deltaT;
  posPrev = pos;
  prevT = currT;

  // Convert count/s to RPM
  float v1 = velocity1/374.0*60.0;
  

  // Low-pass filter (25 Hz cutoff)
  v1Filt = 0.854*v1Filt + 0.0728*v1 + 0.0728*v1Prev;
  v1Prev = v1;
  
  float kp = 2.5;
  float ki = 15;
  float e1 = vtt-v1Filt;
  
//  float e = vt-v2;
//  float kd = 0.05;
  eintegral1 = eintegral1 + e1*deltaT;
  
//  ederivative = ederivative - e*deltaT;
  
//  float u = kp*e + ki*eintegral + kd*ederivative;
  float u1 = kp*e1 + ki*eintegral1;
 
  // Set the motor speed and direction
   dirt = 1;
  
  if (u1<0)
  {
    dirt = -1;
  }
  
   pwrt = (int) fabs(u1);

  if(pwrt > 255)
  {
    pwrt = 255;
  }

  
  
}
void PIDp( float vtp)
{
// Compute the control signal u
   int pos = 0;
  noInterrupts();
  pos = pos_ip;
  interrupts();
  long currT = micros();
  float deltaT = ((float) (currT-prevP))/1.0e6;
  float velocity2 = (pos - posPrevP)/deltaT;
  posPrevP = pos;
  prevP = currT;
  float v2 = velocity2/374.0*60.0;
  v2Filt = 0.854*v2Filt + 0.0728*v2 + 0.0728*v2Prev;
  v2Prev = v2;
  
  float kp = 2.5;
  float ki = 15;
  float e2 = vtp-v2Filt;
  
//  float e = vt-v2;
//  float kd = 0.05;
  eintegral2 = eintegral2 + e2*deltaT;
  
//  ederivative = ederivative - e*deltaT;
  
//  float u = kp*e + ki*eintegral + kd*ederivative;
  float u2 = kp*e2 + ki*eintegral2;
 
  // Set the motor speed and direction
   dirp = 1;
  
  if (u2<0)
  {
    dirp = -1;
  }
  
   pwrp = (int) fabs(u2);

  if(pwrp > 255)
  {
    pwrp = 255;
  } 
  
  
}

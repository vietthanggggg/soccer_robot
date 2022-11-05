#define ENCA PA4 
#define ENCB PA5 
#define IN1 PB4
#define IN2 PB5
#define PWM1 PB6

int pos=0;

volatile int posi = 0; // specify posi as volatile: https://www.arduino.cc/reference/en/language/variables/variable-scope-qualifiers/volatile/
//HardwareTimer pwmtimer4(4);
void setup() {
  Serial.begin(9600);
  pinMode(ENCA,INPUT);
  pinMode(ENCB,INPUT);
  attachInterrupt(digitalPinToInterrupt(ENCA),readEncoder,RISING);
  pinMode(PWM1, OUTPUT);
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
//  pwmtimer4.pause();
//  pwmtimer4.setPrescaleFactor(1);
//  pwmtimer4.setOverflow(1440000);
//  pwmtimer4.refresh();
//  pwmtimer4.resume();
  
}

void loop() {
  setMotor(1, 200, PWM1, IN1, IN2);
  delay(200);
  Serial.println(pos);
  setMotor(-1, 200, PWM1, IN1, IN2);
  delay(200);
  Serial.println(pos);
  setMotor(0, 200, PWM1, IN1, IN2);
  delay(20);
  Serial.println(pos);

}

void setMotor(int dir, int pwmVal, int pwm, int in1, int in2){
  
  if(dir == 1){
    digitalWrite(in1,HIGH);
    digitalWrite(in2,LOW);
    analogWrite(pwm,pwmVal);
  }
  else if(dir == -1){
    digitalWrite(in1,LOW);
    digitalWrite(in2,HIGH);
    analogWrite(pwm,pwmVal);
  }
  else{
    digitalWrite(in1,LOW);
    digitalWrite(in2,LOW);
    analogWrite(pwm,pwmVal);
  }
}

void readEncoder(){
  int b = digitalRead(ENCB);
  if(b > 0){
    pos++;
  }
  else{
    pos--;
  }
}

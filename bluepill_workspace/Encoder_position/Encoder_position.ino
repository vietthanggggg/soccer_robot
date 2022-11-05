#define ENCA PA4
#define ENCB PA5

int pos=0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(ENCA,INPUT);
  pinMode(ENCB,INPUT);
  attachInterrupt(digitalPinToInterrupt(ENCA),readEncoder,RISING);
}

void loop() {
  Serial.println(pos);
}

void readEncoder(){
  int b= digitalRead(ENCB);
  if(b>0){
    pos++;
  }
  else{
    pos--;
  }
}

#define ENCA PA4
#define ENCB PA5
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(ENCA,INPUT);
  pinMode(ENCB,INPUT);
}

void loop() {
  int a = digitalRead(ENCA);
  int b = digitalRead(ENCB);
  Serial.print(a*5); 
  Serial.print(" ");
  Serial.print(b*5);
  Serial.println();
}

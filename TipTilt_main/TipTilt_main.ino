#include <Servo.h>
#include <TimerInterrupt.h>

// Variabili globali
float T = 100; // Tempo di campionamento in millisecondi
float K, K1, K2, Kaw;
float P,I,D;
float u = 0;          // Segnale di comando
float umin = -255, umax = 255; // Limiti del segnale di comando
float pxmin = 0, pxmax = 0, pxtarget = 0; // Boundaries e set point del PID
float posmin = 1000, posmax = 2000, pxcurrent = 0;
float e[3] = {0, 0, 0}; // Errori (e[k], e[k-1], e[k-2])
float u_prev = 0;
float pos_float = 0;
int pos = 0;
int pos_zero = 1500;
bool enablePID = false;

// Variabili per la macchina a stati
enum State { OFF, TRACKING, ERROR };
State currentState = OFF;

void motorStep(){
  updatePIDCommand();
  updatePos();
  Serial.print("Posizione: ")
  Serial.println(pos);
}

void updatePos() {
  pos_float = pos_float + u;
  pos = (int) pos_float;

  // Clamping della posizione
  pos = max(min(pos, posmax), posmin);

  //myservo.write(pos);
  myservo.writeMicroseconds(pos); 
}

void updatePIDCommand() {
  if (enablePID) {
    // Aggiornamento dell'errore (e[k] = utarget - y, dove y è il secondo numero ricevuto)
    e[2] = e[1];
    e[1] = e[0];
    e[0] = pxcurrent - pxtarget;

    // Calcolo del segnale di comando PID
    float u_temp = u_prev + K * e[0] + K1 * e[1] + K2 * e[2];
    
    // Clamping del segnale
    if (u_temp > umax) {
      u = umax;
    } else if (u_temp < umin) {
      u = umin;
    } else {
      u = u_temp;
    }
    
    // Aggiornare il segnale di comando precedente
    u_prev = u;
  }
  else {
    u = 0;
  }
}

void checkPxBoundaries() {
  // Controlla se il comando u è all'interno dei limiti
  if (pxcurrent < pxmin || pxcurrent > pxmax) {
    return 1;  // Errore
  }
  return 0;  // Comando valido
}

String convertCommand(String input) {
  if (input == "O") {
    return "OFF";
  } else if (input == "M") {
    return "SAVEMAX";
  } else if (input == "N") {
    return "SAVEMIN";
  } else if (input == "S") {
    return "START";
  } else if (input == "R") {
    return "RESET";
  } else {
    return "ERROR";
  }
}

void calculatePIDCoefficients() {
    // Calcolo dei coefficienti
    K = P + I * T + (D / T);
    K1 = -P - 2 * (D / T);
    K2 = D / T;
}

// Funzione di setup
void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  myservo.attach(9);  // attaches the servo on pin 9 to the Servo object
  
  // Impostare i coefficienti PID e il guadagno anti-windup
  T = 1000; // Tempo di campionamento in millisecondi
  P = 0.01;
  I = 0.0;
  D = 0.0;
  calculatePIDCoefficients();
  Kaw = 0.1;
  
  // Inizializzare il Timer per l'aggiornamento periodico
  ITimer0.init();
  ITimer0.attachInterruptInterval(T * 1000, motorStep);

  // Inizializza lo stato a OFF (tramite RESET che porta il motore al centro)
  gotoRESET();
}

void gotoOFF(){
  currentState = OFF;
  enablePID = false;
  digitalWrite(LED_BUILTIN, LOW);
}

void gotoTRACKING(){
  currentState = TRACKING;
  enablePID = true;
  digitalWrite(LED_BUILTIN, HIGH);
}

void gotoERROR(){
  currentState = ERROR;
  enablePID = false;
}

void gotoRESET(){
  myservo.writeMicroseconds(1500); 
  gotoOFF();
}

void blinkLED(int N){
  for (int i = 0; i < N; i++) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(50);
    digitalWrite(LED_BUILTIN, LOW);
    delay(50);
  }
}

// Funzione di loop
void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();  // Rimuovere spazi bianchi e newline

    // Parsing del comando seriale
    int x = command.substring(0, command.indexOf(',')).toInt();
    int y = command.substring(command.indexOf(',') + 1, command.lastIndexOf(',')).toInt();
    String cmd_in = command.substring(command.lastIndexOf(',') + 1);
    String cmd = convertCommand(cmd_in); // Translate the command from single character to full word

    pxcurrent = (float) x;

    // Logica dello stato "OFF"
    if (currentState == OFF) {
      
      if (cmd == "SAVEMIN") {
        pxmin = x;
      } else if (cmd == "SAVEMAX") {
        pxmax = x;
      } else if (cmd == "SETZERO") {
        pxtarget = x;
      } else if (cmd == "START") {
        if (pxmin != 0 && pxmax != 0 && pxtarget != 0) {
          gotoTRACKING();
        } else {
          gotoERROR();
        }
      } else if (cmd == "RESET") {
        gotoRESET();
      }
    }
    
    // Logica dello stato "TRACKING"
    else if (currentState == TRACKING) {
      if(cmd == "RESET"){
        gotoRESET();
      }else if (cmd == "OFF") {
        gotoOFF();
      } else {
        if (checkPxBoundaries() == 1) {
          gotoERROR();
        }
      }
    }

    // Logica dello stato "ERROR"
    else if (currentState == ERROR) {
      if (cmd == "OFF") {
        gotoOFF();
      }
      else {
        blinkLED(10);
      }
    }
  }
  else {
    gotoERROR();
    blinkLED(2);
    delay(1000);
  }
}


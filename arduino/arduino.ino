#include <SoftwareSerial.h>
#include <DFRobotDFPlayerMini.h>
SoftwareSerial MP3Module(2, 3);
DFRobotDFPlayerMini MP3Player;
int buttonApin=9;
char flag=0;

void setup () {
  pinMode(buttonApin, INPUT_PULLUP);
  Serial.begin (9600);
  MP3Module.begin(9600);
  if (!MP3Player.begin(MP3Module)) { // MP3 모듈을 초기화합니다. 초기화에 실패하면 오류를 발생시킵니다.
    Serial.println(F("Unable to begin:"));
    Serial.println(F("1.Please recheck the connection!"));
    Serial.println(F("2.Please insert the SD card!"));
    while (true);
  }
  delay(1);
  MP3Player.volume(30);  // 볼륨을 조절합니다. 0~30까지 설정이 가능합니다.
}

void loop () {
  if (digitalRead(buttonApin) == LOW)
  { 
    Serial.println(100);
  }
  
  while(Serial.available()>0)
  {
    flag = Serial.read();
    if(flag == 'a'){
      MP3Player.play(4);  // 0004.mp3를 재생합니다.(재활용을 진행해주세요.)
      delay (2000);
    }
    else if(flag == 'b'){
      MP3Player.play(3);  // 0003.mp3를 재생합니다.(컵홀더를 제거해주세요.)
      delay (2000);
    }
    else if(flag == 'c'){
      MP3Player.play(2);  // 0002.mp3를 재생합니다.(빨대를 제거해주세요.)
      delay (2000);
    }
    else if(flag == 'd'){
      MP3Player.play(1);  // 0001.mp3를 재생합니다.(컵홀더와 빨대를 제거해주세요.)
      delay (2000);
    }
  }
  
}

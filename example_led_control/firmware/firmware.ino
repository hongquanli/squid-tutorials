#include <DueTimer.h>

/***************************************************************************************************/
/***************************************** Communications ******************************************/
/***************************************************************************************************/
static const int CMD_LENGTH = 2;
static const int MSG_LENGTH = 1;
byte buffer_rx[500];
byte buffer_tx[MSG_LENGTH];
int buffer_rx_ptr = 0;

// command sets
static const int CMD_LED_CONTROL = 0;

/***************************************************************************************************/
/********************************************* setup ***********************************************/
/***************************************************************************************************/

void setup() 
{

  // Initialize Native USB port
  //SerialUSB.begin(2000000);     
  //while(!SerialUSB);            // Wait until connection is established
  
  pinMode(LED_BUILTIN, OUTPUT); 
  digitalWrite(LED_BUILTIN,LOW);
  
}

/***************************************************************************************************/
/********************************************** loop ***********************************************/
/***************************************************************************************************/

void loop() {

  // read one meesage from the buffer
  while (SerialUSB.available()) 
  { 
    buffer_rx[buffer_rx_ptr] = SerialUSB.read();
    buffer_rx_ptr = buffer_rx_ptr + 1;
    if (buffer_rx_ptr == CMD_LENGTH) 
    {
      // one full command received, reset the buffer_rx_ptr
      buffer_rx_ptr = 0;

      // parse and execute the command
      switch(buffer_rx[0])
      {
        case CMD_LED_CONTROL:
        {
          if(buffer_rx[1]==0)
            digitalWrite(LED_BUILTIN,LOW);
          if(buffer_rx[1]>=1)
            digitalWrite(LED_BUILTIN,HIGH);
          break;
        }
        default:
          break;
      }
    }
  }
}

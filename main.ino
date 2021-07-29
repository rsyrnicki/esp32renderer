#include <TFT_eSPI.h>

TFT_eSPI tft = TFT_eSPI();  
const int leftBtn = 0;     
const int rightBtn =  35;   

const float rotatingSpeed = 0.2; 

bool updated;
bool wireframe;
int s;                    // scaling factor
float betaAngle;          // pitch angle
float gammaAngle;         // yaw angle

// -------------------------------------------------------------------------
// Setup
// -------------------------------------------------------------------------
void setup(void) {
  pinMode(leftBtn, INPUT);
  pinMode(rightBtn, INPUT);
  
  Serial.begin(115200);
  
  tft.init();
  tft.setRotation(0);
  tft.fillScreen(TFT_BLACK); 
  updated = false;
  wireframe = true; // true for wireframe image, false for a solid model (not working yet)
  s = 30;
  betaAngle = 0.0;
  gammaAngle = -90.0;
}

// -------------------------------------------------------------------------
// Main loop
// -------------------------------------------------------------------------
void loop()
{
  
  if (!updated) {
    float r11 = cos(betaAngle) * cos(gammaAngle);
    float r12 = cos(betaAngle) * (-sin(gammaAngle));
    float r13 = sin(betaAngle);
    float r21 = sin(gammaAngle);
    float r22 = cos(gammaAngle);
    float r23 = 0;
    float r31 = sin(betaAngle) * sin(gammaAngle);
    float r32 = sin(betaAngle) * (-sin(gammaAngle));
    float r33 = cos(betaAngle);
  
    const int rows = sizeof(vertices);
    float projectionMatrix[2][3] = {{r11*s, r12*s, r13*s}, {r21*s, r22*s, r23*s}};
    project(projectionMatrix, vertices);

    float normalMatrix[3][3] = {{r11, r12, r13}, {r21, r22, r23}, {r31, r32, r33}};
    if(!wireframe)
      multNormals(normalMatrix);

    tft.fillScreen(TFT_BLACK);
    for(int i = 0; i < numberFaces; i++) {
      int v1 = faces[i][0]-1;
      int v2 = faces[i][1]-1;
      int v3 = faces[i][2]-1;

      if(!wireframe) {
        float dotProdukt =  (normals[normalsToFaces[i]-1][0]) * (0.0) + 
                            (normals[normalsToFaces[i]-1][1]) * (0.0) + 
                            (normals[normalsToFaces[i]-1][2]) * (1.0);
        int r = round(40 * dotProdukt), g = round(150 * dotProdukt), b = round(255 * dotProdukt);
        if (dotProdukt > 0.) {
         
          tft.fillTriangle(   vertices2D[v1][0], vertices2D[v1][1], 
                              vertices2D[v2][0], vertices2D[v2][1], 
                              vertices2D[v3][0], vertices2D[v3][1],
                         tft.color565(r, g, b));
        
          
      
        }
      } else {
      
      tft.drawTriangle(   vertices2D[v1][0], vertices2D[v1][1], 
                            vertices2D[v2][0], vertices2D[v2][1], 
                            vertices2D[v3][0], vertices2D[v3][1],
                       tft.color565(200, 5, 160));
    }
    };
    
    updated = true;
  }
  
 //delay(500);
 if(digitalRead(leftBtn) == LOW) {
  betaAngle -= rotatingSpeed;
  updated = false;
 } else if (digitalRead(rightBtn) == LOW) {
  betaAngle += rotatingSpeed;
  updated = false;
 }
}


// -------------------------------------------------------------------------
// Matrix multiplication functions
// -------------------------------------------------------------------------
void project( float pMatrix[2][3], float vertices[][3] ) {
  //vertices
  for (int i = 0; i < numberVertices; i++) {
    int x =    round(pMatrix[0][0] * vertices[i][0]
                    + pMatrix[0][1] * vertices[i][1]
                    + pMatrix[0][2] * vertices[i][2]
                    + tft.width()  / 2 - 1); //x   
    int y =    round(pMatrix[1][0] * vertices[i][0]
                    + pMatrix[1][1] * vertices[i][1]
                    + pMatrix[1][2] * vertices[i][2]
                    + tft.width()  / 2 - 1); //y
     vertices2D[i][0] = x;
     vertices2D[i][1] = y;
  }
}

void multNormals(float pMatrix[3][3]) {
  //normals
  for (int i = 0; i < numberNormals; i++) {
    float x =    pMatrix[0][0] * rawNormals[i][0]
                    + pMatrix[0][1] * rawNormals[i][1]
                    + pMatrix[0][2] * rawNormals[i][2]; //x   
    float y =    pMatrix[1][0] * rawNormals[i][0]
                    + pMatrix[1][1] * rawNormals[i][1]
                    + pMatrix[1][2] * rawNormals[i][2]; //y
    float z =    pMatrix[2][0] * rawNormals[i][0]
                    + pMatrix[2][1] * rawNormals[i][1]
                    + pMatrix[2][2] * rawNormals[i][2]; //z
    // normalize the normal
    normals[i][0] = x / sqrt(x*x + y*y + z*z);
    normals[i][1] = y / sqrt(x*x + y*y + z*z);
    normals[i][2] = z / sqrt(x*x + y*y + z*z);
    /*
      Serial.println("Normals calculated: ");
      Serial.println(normals[i][0]);
      Serial.println(normals[i][1]);
      Serial.println(normals[i][2]);
      Serial.println("-------------");
    */
  }
}

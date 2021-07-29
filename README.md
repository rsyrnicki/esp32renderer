# esp32renderer
Display .obj 3D models on your microcontroller

TODO: 
 - Implement backface culling 
 - Implement simple shading (set directional light)
 - Import materials
 
What do you need?
 1. An arduino compatible microcontroller. More powerful boards can display more complex models.
 2. A screen that is compatible with both your board and the TFT_eSPI library
 3. The TFT_eSPI library. Can be found in the Arduino library-repository.
 4. Arduino IDE
 5. USB Cable

How to?
 1. Clone the repository.
 2. Put your model into the root directory. Be sure to export as .obj and select triangulate in blender.
 3. Open the root directory in cmd or terminal
 4. Type: "objToArduinoC.py {model_file_name_without_extention}" e.g. "objToArduinoC.py cube".
 5. Open esp32renderer.ino with Arduino IDE.
 6. Connect the screen, your board and upload the sketch.
 7. Message me if you find any errors ;)
# TheThingsNetwork IoT-Application-DemoApp
This repository contains a demonstrative dashboard for highlighting the system's key operation using the created En- & Decoder IoT software. The project's objective was to create an improved maintainable and scaleable IoT device-application structure, with the LoRaWAN and TheThingsNetwork technology. 

The scope of this project was within educational course of the Internet-of-Things LAB during semester 2324 class, for the Hogeschool Arnhem Nijmegen Embedded Systems Engineering (Applied Science, Bachelor) program. 

## Demo
*Here is an example of a dashboard*: 
![Example of the Dashboard](images/Demo%20APP.png)
On the left a simple dashboard using the Panda package plots figures. On the right a terminal (integrate in VScode) shows the log of the raw api fetched data and the parsed in the system's structure. 

## Engineering Constraints
Due to educational context were imposed on the project: 
- Arduino compatibility (interpreted as PlatformIO acceptable).
- Reduction of Library Footprint.
- Doxygen documentation.
- Use of the provided hardware: [KISS-NODE](https://gitlab.com/wlgrw/han-iot-kiss-lora) and [IOT-NODE](https://gitlab.com/wlgrw/han-iot-node). 
- Use of TheThingsNetwork for LoRaWAN backend solution.
- Refactoring of [CayenneLPP](https://github.com/myDevicesIoT/CayenneLPP) payload.
- Copyright 'licensed'.

The decive objective was however to learn and implement a reliable, maintainable and scaleable Low Power Wide-Area (LPWA) IoT deployment structure concept.   

## Operation Essentials
Here is a broad overview of how the this IoT setup works:
- **Encoder**: Defines the payload protocol structure based on CayenneLPP, more details are found in the respective repo [ENCODER](https://github.com/HAN-IoT-LAB/LoRaWAN-Payload-Sandbox/tree/main).
- Sending over LoRa to TheThingsNetwork (TTN) LoRaWAN server. 
- **Decoding**: On the TTN the payload is decoded using Javascript, more details are found in [TTN_Decoder](https://github.com/HAN-IoT-LAB/TTN-Decoder).
- **Applicational Distribution**: In this repo an example of a figurative dashboard is demonstrated, using the keepAndFetch TTN mechanism through the REST API.

## Conclusion
The repo acts as a Python based example for getting the data from TheThingsNetwork for applicational distrubution useage. This was outside of the initial assignement scope, however a crucial step in IoT to succeed at. 

The recommendation is to take this as a starting point for understanding how to fetch and parse data from TTN server.
The code is absolutely a not well designed, it is just created using 'quick and dirty' approach for because it was not a high priority. 

## License and Copyright
This Python TheThingsNetwork IoT App and its associated libraries are distributed under the terms of the Creative Commons Attribution-NonCommercial 4.0 International License (http://creativecommons.org/licenses/by-nc/4.0/), acknowledging the contributions of Tristan Bosveld, Klaasjan Wagenaar, and Richard Kroesen.

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.
# UNIHIKER-PAL

**PAL** is a simplified version of my python home assistant that I'm running in the DFRobot UNIHIKER which I'm releasing as free open-source.

This is just a demonstration for voice-recognition command-triggering simplicity using python and hopefully will serve as a guide for your own assistant.

![PAL_film](https://github.com/TheRoam/UNIHIKER-PAL/assets/63456390/8375603a-eb11-443d-ac79-f1a8a2a0c3f1)

## Features

Current version includes the following:

**Voice recognition:** using open-source SpeechRecognition python library, returns an array of all the recognised audio strings.

**Climate forecast:** using World Meteorological Organization API data, provides today's weather and the forecast for the 3 coming days. Includes WMO weather icons.

**Local temperature:** reads local BMP-280 temperature sensor to provide a room temperature indicator.

**IoT HTTP commands:** basic workflow to control IoT smart home devices using HTTP commands. Currently turns ON and OFF a Shelly2.5 smart switch.

**Power-save mode:** controls brightness to lower power consumption.

**Connection manager:** checks wifi and pings to the internet to restore connection when it's lost.

**PAL voice samples:** cloned voice of PAL from "The Mitchells vs. The Machines" using the AI voice model CoquiAI-TTS v2.

**UNIHIKER buttons:** button A enables a simple menu (this is thought to enable a more complex menu in the future).

**Touchscreen controls:** restore brightness, switch program, close program.

## Installation

1. Install dependencies for voice recognition:
**pip install SpeechRecognition pyyaml**

2. **Download** this repo.

3. Upload the files and folders to the UNIHIKER in **/root/upload/PAL/**

![PAL_Mind+](https://github.com/user-attachments/assets/646dcab9-4072-4f74-a407-9e3629b8a2e1)

5. **Configure** the **PAL_config.yaml** WIFI credentials, IoT devices, etc.

6. Run the python script **python /root/upload/PAL/PAL_v020.py** from the Mind+ terminal or from the UNIHIKER touch interface.

If you enable **Auto boot** from the Service Toggle menu , the script will run every time the UNIHIKER is restarted. 

## Configuration

For further configuration, check the blog post:
[https://theroamingworkshop.cloud/b/en/2486](https://theroamingworkshop.cloud/b/en/2486)

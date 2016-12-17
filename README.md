# Alexa Copilot
Alexa Copilot for FlightGear flight simulator. Fly planes using voice commands

# Interfacing to FG using Telnet
Code based on Python library developed by FG on Telnet Usage Wiki - https://sourceforge.net/p/flightgear/flightgear/ci/next/tree/scripts/python/

# Setting up Alexa Skill
Follow tutorial for flask-ask and ngrock - https://www.youtube.com/watch?v=cXL8FDUag-s

# Setting up communication between skill and FG interface
Use Hive MQTT and Paho python MQTT client

# Testing everything
Install Alexa on Mac/Pi using https://github.com/alexa/alexa-avs-sample-app/wiki/Linux
Start the Node JS server to communicated with Alexa
Start Companion App to use Alexa App
Following needed to be added to pom.xml in the javaClient - <argument>-Djna.library.path=/Applications/VLC.app/Contents/MacOS/lib/</argument>

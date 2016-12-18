# Alexa Copilot
Alexa Copilot is a voice controlled copilot for FlightGear flight simulator. The aim is to fully automate the tasks typically performed by copilot and reduce pilot's workload so that he/she can focus on flying. 

# Setup Instructions
Please follow our [setup wiki](https://github.com/aditya2592/alexa_copilot/wiki) to setup Alexa Copilot on your Linux/Mac machine. Since the code is based on Python and FlightGear it should work on Windows as well but it has't been tested.

# Running Alexa Copilot
Install Alexa on Mac/Pi using https://github.com/alexa/alexa-avs-sample-app/wiki/Linux
Start the Node JS server to communicated with Alexa
Start Companion App to use Alexa App
Following needed to be added to pom.xml in the javaClient - <argument>-Djna.library.path=/Applications/VLC.app/Contents/MacOS/lib/</argument>

#see https://hub.docker.com/r/nodered/node-red-docker
FROM nodered/node-red-docker:rpi-v8

# run node-red as root user as this is needed to get the HIDdevice node working.
# USER root

# Following command installs node-red-admin which is needed if you want to create a hashed password 
# for the node-red editor.  For that run command "node-red-admin hash-pw" in a terminal window
# for the node-red service in the BalenaCloud dashboard.
# RUN npm install -g --unsafe-perm node-red-admin

# installing editor nano 
RUN apt-get update && apt-get install nano

RUN npm install node-red-contrib-resinio
RUN npm install node-red-dashboard
RUN npm install node-red-contrib-credentials

#COPY ./settings.js /data/settings.js
#COPY ./flows.json  /data/flows.json
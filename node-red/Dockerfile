#see https://hub.docker.com/r/nodered/node-red-docker
FROM nodered/node-red:1.0.0-1-12-arm32v7

######### Changing to root as below commands should be run as root #############
USER root

# Following command installs node-red-admin which is needed if you want to create a hashed password 
# for the node-red editor.  For that run command "node-red-admin hash-pw" in a terminal window
# for the node-red service in the BalenaCloud dashboard.
RUN npm install -g --unsafe-perm node-red-admin

# see https://stackoverflow.com/questions/53026557/error-listen-eacces-0-0-0-080-when-deploying-docker-image-nodered-node-red-doc
RUN setcap 'cap_net_bind_service=+ep'  $(eval readlink -f `which node`)

######### Changing back to node-red user #####################
USER node-red

RUN npm install node-red-contrib-resinio
RUN npm install node-red-dashboard
RUN npm install node-red-contrib-credentials

RUN npm install node-red-node-pi-gpio
# see https://gpiozero.readthedocs.io/en/stable/remote_gpio.html#preparing-the-raspberry-pi
RUN sudo pip install gpiozero pigpio

COPY ./settings.js /data/settings.js

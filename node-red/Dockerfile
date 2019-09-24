#see https://hub.docker.com/r/nodered/node-red-docker
FROM nodered/node-red-docker:0.20.7-rpi-v8
#FROM nodered/node-red-docker:rpi-v8

# installing editor nano 
USER root
RUN apt-get update && apt-get install nano

# upgraded node.js to current latest version 8.16.1
# apparently the version in the docker image is pretty old.
RUN npm cache clean -f ; npm install -g n; n 8.16.1

# Following command installs node-red-admin which is needed if you want to create a hashed password 
# for the node-red editor.  For that run command "node-red-admin hash-pw" in a terminal window
# for the node-red service in the BalenaCloud dashboard.
RUN npm install -g --unsafe-perm node-red-admin

# see https://stackoverflow.com/questions/53026557/error-listen-eacces-0-0-0-080-when-deploying-docker-image-nodered-node-red-doc
RUN sudo setcap 'cap_net_bind_service=+ep'  $(eval readlink -f `which node`)
USER node-red

RUN npm install node-red-contrib-resinio
RUN npm install node-red-dashboard
RUN npm install node-red-contrib-credentials

COPY ./settings.js /data/settings.js
#COPY ./flows.json  /data/flows.json
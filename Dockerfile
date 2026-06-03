ARG IMAGE=intersystemsdc/irishealth-community
FROM $IMAGE

WORKDIR /home/irisowner/dev

COPY --chown=${ISC_PACKAGE_MGRUSER}:${ISC_PACKAGE_IRISGROUP} . ./

USER root
ENV IRISUSERNAME="_SYSTEM" \
    IRISPASSWORD="SYS"

RUN chmod 777 /home/irisowner/dev

USER ${ISC_PACKAGE_MGRUSER}
RUN iris start IRIS \
    && iris session IRIS < iris.script \
    && iris stop IRIS quietly

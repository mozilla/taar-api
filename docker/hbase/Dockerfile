FROM java:8

# Versions of hbase to use for our testing environment
ENV HBASE_VERSION=1.3.1

# install hbase
RUN wget --progress=dot https://archive.apache.org/dist/hbase/$HBASE_VERSION/hbase-$HBASE_VERSION-bin.tar.gz
RUN tar -zxf hbase-$HBASE_VERSION-bin.tar.gz && ln -s hbase-$HBASE_VERSION hbase

COPY ./run_hbase /opt/

# hbase.rest.port
EXPOSE 8080
# hbase.rest.info.port
EXPOSE 8085
# hbase.regionserver.thrift.port
EXPOSE 9090
# hbase.thrift.info.port
EXPOSE 9095
# hbase.zookeeper.property.clientPort
EXPOSE 2181
# hbase.master.info.port
EXPOSE 16010

CMD ["/opt/run_hbase"]

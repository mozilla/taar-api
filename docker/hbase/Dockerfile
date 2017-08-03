FROM java:8

# Versions of hbase to use for our testing environment
ENV HBASE_VERSION=1.2.3

# install hbase
RUN wget -nv https://archive.apache.org/dist/hbase/$HBASE_VERSION/hbase-$HBASE_VERSION-bin.tar.gz
RUN tar -zxf hbase-$HBASE_VERSION-bin.tar.gz

EXPOSE 9090 9091

COPY ./run_hbase /opt/

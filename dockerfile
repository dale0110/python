version: '2'
services:
 controller-node-192-168-1-2_1532509632:
  hostname: controller-node-192-168-1-2_1532509632
  container_name: controller-node-192-168-1-2_1532509632
  restart: always
#  networks:
#   default:
#    ipv4_address: 192.168.1.2
  image: sdon-cluster:latest
  environment:
   - SERVER_IP=192.168.1.2
   - JAVA_MIN_MEM=1G
   - JAVA_MAX_MEM=8G
   - TZ=Asia/Shanghai
  entrypoint:
   - bash
  expose:
   - "8443"
   - "8101"
   - "2830"
   - "1830"
   - "6633"
   - "8999"
   - "8181"
   - "8185"
  ports:
   - "15000:8443"
   - "15001:8101"
   - "15002:2830"
   - "15003:1830"
   - "15004:6633"
   - "15005:8999"
   - "15006:8181"
   - "15007:8185"
  tty: true
  stdin_open: true
#networks:
# default:
#  external:
#   name: oscp-network


ubuntu@ubuntu:~/release_for_1.20.013[17:09]$ cat Dockerfile
FROM oscp:0.4.4-2.00.10R3B10
MAINTAINER zhang.chaowei "zhang.chaowei@zte.com.cn"

RUN    yum update –y \
        && yum install -y tar \
        && yum install -y expect \
        && yum clean all \
        && rm -rf oscp

ADD  karaf/sdotn-distribution/target/sdotn-karaf-distribution-3.0.0-SNAPSHOT.tar.gz  .

RUN    mv sdotn-karaf-distribution-3.0.0-SNAPSHOT oscp  \
        #&& sed  -i '$d' /opt/startup \
        && rm /opt/startup \
        && echo "#!/bin/bash" >>/opt/startup \
        && echo "cd /opt/oscp/bin/" >> /opt/startup \
        #&& echo "/bin/bash" >> /opt/startup \
        && echo "/bin/bash startvelcom" >> /opt/startup \
        && echo "sleep 3" >> /opt/startup \
        && echo "/bin/bash ./client -a 8101 -h 127.0.0.1 -u karaf" >> /opt/startup \
        && echo "sleep 3" >> /opt/startup \
        #&& echo "tail -f /dev/null"  >> /opt/startup \
        #&& echo "/bin/bash" >> /opt/oscp/bin/startvelcom \
        && sed -i "/exit/d" /opt/oscp/bin/startnetconf \
        && chmod +x /opt/oscp/bin/client \
        && chmod +x /opt/oscp/bin/startvelcom \
        && chmod +x /opt/startup


ENTRYPOINT ["/bin/bash","/opt/startup"]

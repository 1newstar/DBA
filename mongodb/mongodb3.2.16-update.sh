#!/bin/bash
echo "begin install mongodb3.2.16"
SRC_URI="https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.2.16.tgz"
PKG_NAME=`basename $SRC_URI`
DIR=`pwd`
DATE=`date +%Y%m%d%H%M%S`

\mv /alidata/mongodb /alidata/mongodb.bak.$DATE &> /dev/null

if [ ! -s $PKG_NAME ]; then
  wget -c $SRC_URI
fi

mkdir -p /alidata/mongodb

rm -rf mongodb-linux-x86_64-3.2.16/
tar vxf mongodb-linux-x86_64-3.2.16.tgz 
mv mongodb-linux-x86_64-3.2.16/* /alidata/mongodb
rm -rf mongodb-linux-x86_64-3.2.16
rm -rf mongodb-linux-x86_64-3.2.16.tgz

#add PATH
if ! cat /etc/profile | grep 'export PATH=$PATH:/alidata/mongodb/bin' &> /dev/null;then
        echo 'export PATH=$PATH:/alidata/mongodb/bin' >> /etc/profile
fi

cd $DIR
source /etc/profile
bash
echo "successful install mongodb3.2.16"
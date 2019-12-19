#!/bin/bash
set -x

if hostname | grep -q namenode; then
  cd /users
  i=0
  while read line
  do
    array[ $i ]="$line"
    (( i++ ))
  done < <(find . -mindepth 1 -maxdepth 1 -type d \( ! -iname ".*" \) | sed 's|^\./||g')

  groupadd hadoop
  for j in "${array[@]}"
  do
    usermod -a -G hadoop $j
  done
    
  for j in "${array[@]}"
  do
    sudo -H -u hdfs bash -c "hdfs dfs -mkdir -p /user/$j"
    sudo -H -u hdfs bash -c "hdfs dfs -chown $j:hadoop /user/$j"
    sudo -H -u hdfs bash -c "hdfs dfs -chmod 755 /user/$j"
  done
  
#  sudo -H -u hdfs bash -c "wget -P /landing https://cs.wcupa.edu/lngo/data/airlines.tgz"
#  sudo -H -u hdfs bash -c "cd /landing; tar xzf airlines.tgz"
# https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
fi


    2  ping baidu.com
 
    6  ifconfig
    7  ip addr
    8  cd /etc/sysconfig/
    9  ls
    10  cd network-scripts/
    11  ls
    12  cat ifcfg-ens33 
    13  vim
    14  vi ifcfg-ens33 
    ONBOOT=no ---> yes
    
    15  shutdown -r
    16  ping baidu.com
   
    19  ls
    20  pwd
    21  mkdir work

    30  cd work/
    31  ls
    33  yum install wget
    34  wget  http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm
    35  ls
    36  rpm -ivh nginx-release-centos-7-0.el7.ngx.noarch.rpm
    37  yum install nginx
    38  systemctl start nginx
    39  cat /etc/nginx/nginx.conf 
    40  yum install vim
    41  ls /etc/nginx/
    42  vim /etc/nginx/nginx.conf 
    43  ls
    44  ls /etc/nginx/
    45  vim /etc/nginx/conf.d/default.conf 
    server_name  192.168.18.248;
     
    46  nginx -s reload

    55  ip addr show ens33 | grep inet | awk '{ print $2; }' | sed 's/\/.*$//'

    65  cat /etc/nginx/conf.d/default.conf 

    67  ps -aux | grep 'nginx'

    69  firewall-cmd --zone=public --add-port=80/tcp --permanent
    70  systemctl restart firewalld.service

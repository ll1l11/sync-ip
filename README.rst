=======
sync-ip
=======

用途, linux服务器没有显示器, 使用dhcp获取ip, 经常更改


这个工程做的是:

- 将ifconfig获取的信息scp到服务器

- 使用[dnspod api](http://www.dnspod.cn/docs/records.html#record-modify)接口修改dns的一个domain

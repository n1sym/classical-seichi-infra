インフラ周りのやつ

## 初期設定

https://docs.aws.amazon.com/ja_jp/corretto/latest/corretto-17-ug/amazon-linux-install.html

~~~
ssh -i ~/.ssh/minecraft-ec2.pem ec2-user@

sudo yum install java-17-amazon-corretto

$ java -version
openjdk version "17.0.4" 2022-07-19 LTS
OpenJDK Runtime Environment Corretto-17.0.4.8.1 (build 17.0.4+8-LTS)
OpenJDK 64-Bit Server VM Corretto-17.0.4.8.1 (build 17.0.4+8-LTS, mixed mode, sharing)

pwd
/home/ec2-user/minecraft
wget https://api.papermc.io/v2/projects/paper/versions/1.19/builds/61/downloads/paper-1.19-61.jar

sqlite3 development.db

sqlite> CREATE TABLE account (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, uuid BLOB NOT NULL UNIQUE);
sqlite> CREATE TABLE account_name (id INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL);
sqlite> CREATE TABLE seichi_count (id INTEGER NOT NULL PRIMARY KEY, count INTEGER NOT NULL);

sudo yum update -y
sudo yum install git -y
git version
~~~

## EC2起動後にレコード配置

雑ポリシー

~~~
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "route53:ChangeResourceRecordSets",
                "route53:ListResourceRecordSets"
            ],
            "Resource": "*"
        }
    ]
}
~~~

イベント

~~~
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "instance-id": ["i-06**********82"],
    "state": ["running", "stopping"]
  }
}
~~~

## インスタンス起動時にマイクラサーバを自動起動する

ちゃんと詳しく調べる

~~~
sudo vim /etc/systemd/system/minecraft.service
~~~

~~~
[Unit]
Description=Minecraft Server
After=network-online.target

[Service]
WorkingDirectory=/home/ec2-user/minecraft
User=ec2-user

ExecStart=/bin/bash -c '/bin/screen -DmS minecraft /bin/java -Xms2G -Xmx2G -jar paper-1.19-61.jar --nogui'

ExecReload=/bin/screen -p 0 -S minecraft -X eval 'stuff "reload"\\015'

ExecStop=/bin/screen -p 0 -S minecraft -X eval 'stuff "say Server Shutdown. Saving map..."\\015'
ExecStop=/bin/screen -p 0 -S minecraft -X eval 'stuff "save-all"\\015'
ExecStop=/bin/screen -p 0 -S minecraft -X eval 'stuff "stop"\\015'
ExecStop=/bin/sleep 10

Restart=on-failure
RestartSec=60s

[Install]
WantedBy=network-online.target
~~~

~~~
sudo systemctl daemon-reload
sudo systemctl status minecraft
sudo systemctl start minecraft
sudo systemctl status minecraft
screen -r minecraft
# exit: Ctrl+A > d
sudo systemctl enable minecraft
~~~

## dynmap の初期設定

~~~
dynmap purgemap world_1 cave
dmap mapdelete world_1:cave
dynmap purgemap world_1_the_end flat
dmap mapdelete world_1_the_end:flat
dmap worldset world_1_the_end enabled:false
dynmap fullrender world_1
~~~
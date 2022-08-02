インフラ周りのやつ

memo

https://docs.aws.amazon.com/ja_jp/corretto/latest/corretto-17-ug/amazon-linux-install.html

~~~
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

~~~
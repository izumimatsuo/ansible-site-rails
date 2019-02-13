# ansible-site-rails

Rails アプリケーションを開発する際に必要な環境を構築する。
以下のソフトウェアで構成する。

* CentOS
* Apache Httpd
* Ruby
* Phusion Passenger
* PostgreSQL

なお、Rails はアプリケーションプロジェクトの vendor/bundle にインストールする。

## 環境構築手順

```
# git clone https://github.com/izumimatsuo/ansible-site-rails
# cd ansible-site-rails
# ./provision.sh
```

## アプリケーション作成例

### PostgreSQL の設定

管理者パスワードの設定とアプリケーション用のユーザロールを追加する。

```
# su - postgres -c psql
postgres=# alter role postgres with password 'postgres';
postgres=# create role demo with createdb login password 'demo';
postgres=# \q
```

local の認証方式を peer から md5 へ変更する。

```
# sed -i 's/\(^local.*\)peer/\1md5/g' /var/lib/pgsql/9.6/data/pg_hba.conf
# systemctl restart postgresql-9.6
```

### アプリケーション作成

アプリケーションプロジェクト（実行環境）を作成する。

```
# cd /var/www/html
# mkdir demo
# cd demo
# bundle init
# sed -i 's/#\s*\(.*rails\)/\1/g' Gemfile
# bundle install --path vendor/bundle
# bundle exec rails new . -B -d postgresql --skip-turbolinks --skip-test
# sed -i 's/#\s*\(.*mini_racer\)/\1/g' Gemfile
# export PATH=/usr/pgsql-9.6/bin:$PATH
# bundle install
```

簡易なアプリケーションを自動生成する。

```
# bundle exec rails generate scaffold Blog title:string content:text
```

データベースのマイグレーション処理を実行する。

```
# sed -i 's/#\(username:\)/\1/g' config/database.yml
# sed -i 's/#\(password:\)/\1 demo/g' config/database.yml
# bundle exec rake db:create RAILS_ENV=development
# bundle exec rake db:migrate RAILS_ENV=development
```

アプリケーションの実行権限を調整する。

```
# cd ..
# chown -R apache:apache demo
```

アプリケーションを Web で実行できるように設定する。

```
# cat <<EOF > /etc/httpd/conf.d/rails.conf
<VirtualHost *:80>
   RailsEnv development
   PassengerEnabled on
   DocumentRoot /var/www/html/demo/public
   <Directory /var/www/html/demo/public>
      AllowOverride all
      Options -MultiViews
   </Directory>
</VirtualHost>
EOF

# systemctl restart httpd
```

http://localhost:8080/blogs へアクセスしてアプリケーションの動作確認をする。

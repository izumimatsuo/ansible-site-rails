# ansible-site-rails

Rails アプリケーションを開発する際に必要な環境を構築する。
以下のソフトウェアで構成。

* CentOS 7.6
* Apache Httpd 2.4
* Phusion Passenger (mod_rails) 5.2
* Ruby on Rails 5.2 (ruby 2.5)
* PostgreSQL 9.6

## 環境構築手順

```
# git clone https://github.com/izumimatsuo/ansible-site-rails
# ce ansible-site-rails
# ./provision.sh
```

## アプリケーション開発例

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

### アプリケーションの生成

土台となる雛形を生成する。

```
# cd /var/www/html
# rails new demo -d postgresql
# cd demo
# sed -i 's/#\s*\(.*mini_racer\)/\1/g' Gemfile
# export PATH=/usr/pgsql-9.6/bin:$PATH
# bundle install
```

簡易なブログアプリケーションを生成する。

```
# rails generate scaffold Blog title:string content:text
```

データベースのマイグレーション処理を実行する。

```
# sed -i 's/#\(username:\)/\1/g' config/database.yml
# sed -i 's/#\(password:\)/\1 demo/g' config/database.yml
# rake db:create RAILS_ENV=development
# rake db:migrate RAILS_ENV=development
```

アプリケーションの実行権限を調整する。

```
# cd ..
# chown -R postgres:postgres demo
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


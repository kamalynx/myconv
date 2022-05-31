# MySQL/MariaDB engine converter

С помощью этого скрипта вы можете изменить тип таблиц в базе данных.

Скрипт запускается со следующими параметрами:

 - `--database` &mdash; имя базы данных
 - `--user` &mdash; пользователь базы данных (по умолчанию **root**)
 - `--host` &mdash; имя или ip сервера (по умолчанию **localhost**)
 - `--password` &mdash; пароль, если требуется
 - `--unix_socket` &mdash; путь к unix сокету (по умолчанию */run/mysqld/mysqld.sock*); полезно при аутентификации системных пользователей через unix сокеты, как в случае с root
 - `--old` &mdash; старый тип *engine* таблицы (по умолчанию **MyISAM**)
 - `--new` &mdash; новый тип *engine* (по умолчанию **InnoDB**)
 - `--charset` &mdash; кодировка (по умолчанию **utf8mb4**)

Например, у вас есть база с таблицами в MyISAM. И их нужно конвертировать в InnoDB. Для этого запускается скрипт следующим образом:

```bash
python3 myconv.py --database=somedb --user=someuser --password=qwerty
```

В данном случае параметры `--old` и `--new` указывать не обязательно. См. значения по умолчанию.

Однако, их нужно указать, если, например, вы хотите конвертировать таблицы InnoDB в Aria.

```bash
python3 myconv.py --database somedb --user someuser --password passw0rd --old innodb --new aria
```

Знак = не обязателен, порядок аргументов тоже.


Предоставляется **как есть**. :)
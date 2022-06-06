import argparse
import logging
from typing import Optional
import sys

import pymysql


logging.basicConfig(format='[ %(levelname)s ]\t%(message)s', level=logging.INFO)


class Database:
    def __init__(self) -> None:
        mysql_engines = ('MyISAM', 'InnoDB', 'Aria', 'ROCKSDB')

        parser = argparse.ArgumentParser(
            description="""С помощью этого скрипта можно изменить тип таблиц
            базы данных MySQL. Например, с MyISAM на InnoDB.
            """
        )
        parser.add_argument(
            '--database', default='test', help='database', type=str,
            required=True
        )
        parser.add_argument(
            '--host', default='localhost', help='hostname', type=str
        )
        parser.add_argument(
            '--user', default='root', help='username', type=str
        )
        parser.add_argument(
            '--password', help='password', type=str
        )
        parser.add_argument(
            '--unix_socket', default='/var/run/mysqld/mysqld.sock',
            help='path to unix socket', type=str

        )
        parser.add_argument(
            '--old', default='MyISAM', help='old engine', type=str,
            choices=mysql_engines
        )
        parser.add_argument(
            '--new', default='InnoDB', help='new engine', type=str,
            choices=mysql_engines
        )
        parser.add_argument(
            '--charset', default='utf8mb4', help='connection charset',
            type=str
        )
        self.args = parser.parse_args()

    def __enter__(self):
        conn_params = {
            'database': self.args.database,
            'host': self.args.host,
            'user': self.args.user,
            'password': self.args.password,
            'unix_socket': self.args.unix_socket,
            'cursorclass': pymysql.cursors.DictCursor
        }
        try:
            self.connection = pymysql.connect(**conn_params)
        except pymysql.Error as err:
            code, message = err.args
            logging.error('Код ошибки: %s', code)
            logging.error('Сообщение: %s', message)
            return sys.exit(1)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> Optional[str]:
        self.connection.close()
        if exc_value:
            return logging.info('%s', exc_value)

    @property
    def list_tables(self) -> list:
        """Получить список таблиц указанной базы данных."""
        with self.connection.cursor() as cur:
            _query = 'SHOW TABLE STATUS WHERE ENGINE = %s'
            cur.execute(_query, (self.args.old, ))
            tables = cur.fetchall()
            self.table_list = [table['Name'] for table in tables]
            return self.table_list

    def get_current_state(self) -> None:
        """Получить информацию о существующих таблицах в базе данных."""
        with self.connection.cursor() as cur:
            cur.execute('SHOW TABLE STATUS')
            tables = cur.fetchall()
            for table in tables:
                logging.info(
                    'Таблица: %s, движок: %s',
                    table['Name'], table['Engine']
                )

    def change_engine(self, tables: list = None):
        for table in tables:
            with self.connection.cursor() as cur:
                logging.info(
                    'Изменение движка для таблицы "%s" с <%s> на <%s>',
                    table, self.args.old, self.args.new
                )
                _query = 'ALTER TABLE `{0}` ENGINE = %s'.format(table)
                cur.execute(_query, (self.args.new, ))
                cur.execute('SHOW TABLE STATUS WHERE Name = %s', (table,))
                current_table = cur.fetchone()
                logging.info(
                    'Новый движок таблицы "%s": %s',
                    current_table.get('Name'), current_table.get('Engine')
                )


if __name__ == '__main__':
    with Database() as db:
        db.change_engine(db.list_tables)
        db.get_current_state()

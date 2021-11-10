"""Convert all tables in selected database from old engine to new."""
from sys import exit
try:
    import click
    import pymysql
except ModuleNotFoundError as err:
    print('Cannot run script:', err)
    exit(1)

choices = ('MyISAM', 'InnoDB', 'Aria', 'ROCKSDB')


@click.command()
@click.option(
    '--old', default='MyISAM', help='set old database engine',
    type=click.Choice(choices, case_sensitive=False)
)
@click.option(
    '--new', default='InnoDB', help='set new database engine',
    type=click.Choice(choices, case_sensitive=False)
    )
@click.option('--database', type=str, help='database name')
@click.option('--user', type=str, help='database user')
@click.option('--host', default='localhost', help='DB server IP or hostname')
@click.option(
    '--unix-socket', default='/run/mysqld/mysqld.sock',
    help='path to mysql/mariadb socket'
)
@click.password_option()
def main(old: str, new: str, **conn_param):
    """
    Get list of tables and convert each table to new engine.

    :param old: define old database engine

    :param new: define new database engine
    """
    try:
        with pymysql.connect(**conn_param) as conn, conn.cursor() as cur:
            cur.execute('SHOW TABLE STATUS WHERE ENGINE = %s', (old, ))
            tables = cur.fetchall()
            for table in tables:
                _sql = 'ALTER TABLE `{0}` ENGINE = %s'
                click.echo(
                    f'Change engine for {table[0]} from {old} to {new}.'
                )
                cur.execute(_sql.format(table[0]), (new))
    except pymysql.Error as err:
        print(err.args)


if __name__ == '__main__':
    main()

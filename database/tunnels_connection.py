from Resumeaiogram import config
import sshtunnel
import psycopg2


def readTable():
    sshtunnel.SSH_TIMEOUT = 10.0
    sshtunnel.TUNNEL_TIMEOUT = 10.0
    postgres_hostname = config.Server_host
    postgres_host_port = 13055
    try:
        with sshtunnel.SSHTunnelForwarder(('ssh.pythonanywhere.com'),
                ssh_username=config.Ssh_username,
                ssh_password=config.Ssh_password,
                remote_bind_address=(postgres_hostname, postgres_host_port)) as tunnel:
            connection = psycopg2.connect(
                user=config.Server_username, password=config.Server_password,
                host='127.0.0.1', port=tunnel.local_bind_port,
                database=config.Database)
            cur = connection.cursor()
            cur.execute("""SELECT * FROM public.resume_db1 WHERE id = 1""")
            result = cur.fetchall()
            print(result)
            connection.close()
            cur.close()
            return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

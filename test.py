import asyncio
import asyncpg
import sshtunnel


async def read2():
    sshtunnel.SSH_TIMEOUT = 10.0
    sshtunnel.TUNNEL_TIMEOUT = 10.0
    postgres_hostname = 'goiteens-3055.postgres.pythonanywhere-services.com'
    postgres_host_port = 13055
    with sshtunnel.SSHTunnelForwarder(('ssh.pythonanywhere.com'),
                                      ssh_username='goiteens',
                                      ssh_password='productionteam123',
                                      remote_bind_address=(postgres_hostname, postgres_host_port)) as tunnel:
        conn = await asyncpg.connect(user='super', password='kxfs!9E26VGnpzK',
                                 database='postgres', host='127.0.0.1', port=tunnel.local_bind_port)
        values = await conn.fetch(
            """SELECT *
            FROM public.resume_db;""",
            )
        right_values = []
        for item in values:
            right_values.append(tuple(item))
        print(right_values)
        await conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(read2())

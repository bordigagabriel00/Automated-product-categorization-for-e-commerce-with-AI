import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from dotenv import load_dotenv

load_dotenv()

cluster_ips = [os.getenv('SCYLLA_CLUSTER', '127.0.0.1')]
keyspace = os.getenv('SCYLLA_KEYSPACE', 'default_ks')
username = os.getenv('SCYLLA_USER', 'admin_usr')
password = os.getenv('SCYLLA_PASSWORD', 'mypassword')

auth_provider = PlainTextAuthProvider(username='cassandra', password='scylla')
cluster = Cluster(cluster_ips, auth_provider=auth_provider)
session = cluster.connect()

# Create keyspace
session.execute(f"""
CREATE KEYSPACE IF NOT EXISTS {keyspace}
WITH replication = {{'class': 'SimpleStrategy', 'replication_factor' : 3}};
""")

# Create user with password
session.execute(f"CREATE ROLE IF NOT EXISTS {username} WITH PASSWORD = '{password}' AND LOGIN = TRUE;")

# Grant permissions to the user
session.execute(f"GRANT ALL PERMISSIONS ON KEYSPACE {keyspace} TO {username};")

print("Database initialized successfully.")

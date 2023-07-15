import paramiko
import os
from dotenv import load_dotenv
from tqdm import tqdm
from datetime import date
from functools import partial

load_dotenv()
paramiko.util.log_to_file("paramiko.log")


def progress_callback(transferred, total, progress):
    progress.update(transferred - progress.n)


def download_from_server(host, port, username, password):
    today = date.today()
    date_format = today.strftime("%d-%m-%Y")

    transport = paramiko.Transport((host, port))
    transport.connect(None, username, password)

    sftp = paramiko.SFTPClient.from_transport(transport)

    if host != os.getenv('host2'):
        remote_filepath = f"backup-system_{date_format}.tar.gz"
        local_filepath = f"C:/Users/alexi/Desktop/dossier vide/raspberry/{remote_filepath}"
    elif host == os.getenv('host2'):
        remote_filepath = f"backup_{date_format}.tar.gz"
        local_filepath = f"C:/Users/alexi/Desktop/dossier vide/dapp/{remote_filepath}"

    remote_file_size = sftp.stat(remote_filepath).st_size

    bar_format = 'Downloading: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}, {rate_fmt}{postfix}]'

    with tqdm(total=remote_file_size, unit='B', unit_scale=True, ncols=80, bar_format=bar_format) as progress:
        progress.set_description('Downloading')
        sftp.get(remote_filepath, local_filepath, callback=partial(progress_callback, progress=progress))

    if sftp:
        sftp.close()
    if transport:
        transport.close()


host1, port1 = os.getenv('host'), 22222
username1, password1 = os.getenv('user'), os.getenv('password')
download_from_server(host1, port1, username1, password1)

host2, port2 = os.getenv('host2'), 22
username2, password2 = os.getenv('user2'), os.getenv('password2')
download_from_server(host2, port2, username2, password2)

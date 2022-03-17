import shutil
import zipfile
from datetime import datetime

from pandas_cria_xlxs import pandas_cria_xlsx


def descompacta(tmp_folder, arquivo):

    nome_data_e_hora = str(datetime.now()).replace(":", "-").replace(" ", "-")

    print(nome_data_e_hora)

    old_file_name = tmp_folder + arquivo

    new_filename = tmp_folder + nome_data_e_hora + ".zip"
    shutil.copy(old_file_name, new_filename)

    with zipfile.ZipFile(tmp_folder + nome_data_e_hora+".zip", "r") as zip_ref:
        zip_ref.extractall(tmp_folder)

    pandas_cria_xlsx(nome_data_e_hora)

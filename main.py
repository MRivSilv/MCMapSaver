import os
import zipfile
import shutil
from git import Repo, RemoteProgress

class MyProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if max_count:
            percent = (cur_count / max_count) * 100
            print(f'Progreso: {percent:.2f}%')
        else:
            print(f'Progreso: {cur_count}')

def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_path))

# Ruta de la carpeta a comprimir
folder_path = r'C:\\Users\\matia\\AppData\\Roaming\\.minecraft\\saves\\TeniaTanto'
# Ruta donde se guardará el archivo zip
zip_path = r'C:\\Users\\matia\\AppData\\Roaming\\.minecraft\\saves\\TeniaTanto.zip'

# Comprimir la carpeta
zip_folder(folder_path, zip_path)

print(f"La carpeta {folder_path} ha sido comprimida y guardada en {zip_path}.")

# Ruta del repositorio de GitHub
repo_path = r'C:\\Users\\matia\\AppData\\Roaming\\.minecraft\\saves\\TeniaTanto_repo'

# Clonar el repositorio si no existe
if not os.path.exists(repo_path):
    Repo.clone_from('https://github.com/tu_usuario/tu_repositorio.git', repo_path, progress=MyProgress())

# Crear una instancia del repositorio
repo = Repo(repo_path)

# Copiar el archivo zip al repositorio
shutil.copy(zip_path, repo_path)

# Agregar el archivo al repositorio y hacer commit
repo.git.add('TeniaTanto.zip')
repo.index.commit('Añadir archivo TeniaTanto.zip')

# Subir los cambios a GitHub con progreso
origin = repo.remote(name='origin')
origin.push(progress=MyProgress())

print(f"El archivo {zip_path} ha sido subido a GitHub.")
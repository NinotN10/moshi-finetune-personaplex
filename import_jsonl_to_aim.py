import json
import os
import sys
from aim import Run

# Configuration
jsonl_path = 'runs/french_moshi/metrics.train.jsonl'
log_path = 'runs/french_moshi/train.log'  # <--- Le nouveau fichier
aim_repo = 'aim_data'

if not os.path.exists(jsonl_path):
    print(f"ERREUR : Fichier introuvable : {jsonl_path}")
    sys.exit(1)

print(f"--- Importation Metrics + Logs ---")

# Initialiser le run
run = Run(repo=aim_repo, experiment='french_moshi')

# 1. Importer les métriques (votre code existant)
with open(jsonl_path, 'r') as f:
    for i, line in enumerate(f):
        try:
            data = json.loads(line.strip())
            step = data.get('step', data.get('epoch', i))
            for key, value in data.items():
                if isinstance(value, (int, float)) and key not in ['step', 'epoch']:
                    run.track(value, name=key, step=step)
        except:
            pass

# 2. Attacher les logs textuels (NOUVEAU)
if os.path.exists(log_path):
    print(f"Attachement des logs : {log_path}")
    # Cela va rendre le fichier téléchargeable et visible dans l'onglet "Artifacts"
    run.track_artifact(log_path, name="train_console.log")
else:
    print(f"Pas de fichier log trouvé à {log_path}")

print("--- Terminé ---")
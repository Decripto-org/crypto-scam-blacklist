import argparse
import os

# Definizione della funzione per aggiungere il dominio alla lista
def add_domain_to_blocklist(domain, filename='crypto_scam_blocklist.txt'):
    formatted_domain = f'||{domain}^'
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
        lines = [line.strip() for line in lines]
        # Assicurarsi che il dominio non sia già presente nella lista
        if formatted_domain in lines:
            print(f"{domain} è già presente nella blocklist.")
            return
        lines.append(formatted_domain)
        lines.sort()
    else:
        lines = [formatted_domain]
    with open(filename, 'w') as file:
        for line in lines:
            file.write(f"{line}\n")
    print(f"{domain} è stato aggiunto alla blocklist.")

# Analisi degli argomenti da linea di comando
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Aggiungi un dominio alla blocklist di scam crypto.')
    parser.add_argument('-d', '--domain', type=str, required=True, help='Il dominio da aggiungere alla blocklist.')
    args = parser.parse_args()
    add_domain_to_blocklist(args.domain)

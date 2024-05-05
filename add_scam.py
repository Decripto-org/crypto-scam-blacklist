import argparse
import os

# Definizione della funzione per aggiungere il dominio alla lista
def add_domain_to_blocklist(domain, filename='crypto_scam_blocklist.txt'):
    # Rimozione di 'www.' se presente nel dominio
    if domain.startswith("www."):
        domain = domain[4:]  # Rimuove i primi quattro caratteri 'www.'

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
    else:
        lines = [formatted_domain]
    # Rimozione dei duplicati e ordinamento della lista
    lines = list(set(lines))
    lines.sort()
    with open(filename, 'w') as file:
        for line in lines:
            file.write(f"{line}\n")
    print(f"{domain} è stato aggiunto alla blocklist.")

# Funzione per importare i domini da un file
def import_domains_from_file(file_path, filename='crypto_scam_blocklist.txt'):
    if not os.path.exists(file_path):
        print(f"Errore: il file {file_path} non esiste.")
        return
    with open(file_path, 'r') as file:
        domains = file.readlines()
    domains = [domain.strip() for domain in domains if domain.strip() != '']
    for domain in domains:
        add_domain_to_blocklist(domain, filename)

# Analisi degli argomenti da linea di comando
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Aggiungi domini alla blocklist di scam crypto.')
    parser.add_argument('-d', '--domain', type=str, help='Il dominio da aggiungere alla blocklist.')
    parser.add_argument('-f', '--file', type=str, help='File contenente i domini da aggiungere alla blocklist.')
    args = parser.parse_args()

    if args.domain:
        add_domain_to_blocklist(args.domain)
    elif args.file:
        import_domains_from_file(args.file)
    else:
        print("Errore: è necessario specificare un dominio con -d o un file con -f.")

# import argparse
# import os

# # Definizione della funzione per aggiungere il dominio alla lista
# def add_domain_to_blocklist(domain, filename='crypto_scam_blocklist.txt'):
#     # Rimozione di 'www.' se presente nel dominio
#     if domain.startswith("www."):
#         domain = domain[4:]  # Rimuove i primi quattro caratteri 'www.'

#     formatted_domain = f'||{domain}^'
#     if os.path.exists(filename):
#         with open(filename, 'r') as file:
#             lines = file.readlines()
#         lines = [line.strip() for line in lines]
#         # Assicurarsi che il dominio non sia già presente nella lista
#         if formatted_domain in lines:
#             print(f"{domain} è già presente nella blocklist.")
#             return
#         lines.append(formatted_domain)
#     else:
#         lines = [formatted_domain]
#     # Rimozione dei duplicati e ordinamento della lista
#     lines = list(set(lines))
#     lines.sort()
#     with open(filename, 'w') as file:
#         for line in lines:
#             file.write(f"{line}\n")
#     print(f"{domain} è stato aggiunto alla blocklist.")

# # Funzione per importare i domini da un file
# def import_domains_from_file(file_path, filename='crypto_scam_blocklist.txt'):
#     if not os.path.exists(file_path):
#         print(f"Errore: il file {file_path} non esiste.")
#         return
#     with open(file_path, 'r') as file:
#         domains = file.readlines()
#     domains = [domain.strip() for domain in domains if domain.strip() != '']
#     for domain in domains:
#         add_domain_to_blocklist(domain, filename)

# # Analisi degli argomenti da linea di comando
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Aggiungi domini alla blocklist di scam crypto.')
#     parser.add_argument('-d', '--domain', type=str, help='Il dominio da aggiungere alla blocklist.')
#     parser.add_argument('-f', '--file', type=str, help='File contenente i domini da aggiungere alla blocklist.')
#     args = parser.parse_args()

#     if args.domain:
#         add_domain_to_blocklist(args.domain)
#     elif args.file:
#         import_domains_from_file(args.file)
#     else:
#         print("Errore: è necessario specificare un dominio con -d o un file con -f.")



import argparse
import os
from tqdm import tqdm

def add_domains_to_blocklist(domains, filename='crypto_scam_blocklist.txt', verbose=False):
    # Leggere i domini esistenti nel file di blocklist, se esiste
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            existing_domains = set(line.strip() for line in file)
    else:
        existing_domains = set()

    # Preparare i nuovi domini rimuovendo 'www.' e formattando
    new_domains = set(f'||{domain[4:] if domain.startswith("www.") else domain}^' for domain in domains)

    # Unire i set e scrivere solo se ci sono nuovi domini
    combined_domains = existing_domains.union(new_domains)
    total_added = 0
    if combined_domains != existing_domains:
        with open(filename, 'w') as file:
            # Setup tqdm with total number of domains to be written
            progress_bar = tqdm(sorted(combined_domains), total=len(combined_domains), desc="Scrivendo blocklist")
            for domain in progress_bar:
                file.write(f"{domain}\n")
                if verbose and (domain in new_domains):
                    print(f"Aggiunto: {domain}")
                # Increment the progress bar description on the fly
                if domain in new_domains:
                    total_added += 1
                    progress_bar.set_description(f"Aggiunti {total_added} di {len(new_domains)}")
        print(f"Totale {total_added} nuovi domini aggiunti alla blocklist.")
    else:
        print("Nessun nuovo dominio aggiunto.")

def import_domains_from_file(file_path, filename='crypto_scam_blocklist.txt', verbose=False):
    if not os.path.exists(file_path):
        print(f"Errore: il file {file_path} non esiste.")
        return
    
    with open(file_path, 'r') as file:
        domains = [line.strip() for line in file if line.strip()]

    tqdm.write(f"Elaborazione di {len(domains)} domini...")
    add_domains_to_blocklist(domains, filename, verbose)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Aggiungi domini alla blocklist di scam crypto.')
    parser.add_argument('-d', '--domain', type=str, help='Il dominio da aggiungere alla blocklist.')
    parser.add_argument('-f', '--file', type=str, help='File contenente i domini da aggiungere alla blocklist.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Mostra dettagli dei domini man mano che vengono aggiunti.')
    args = parser.parse_args()

    if args.domain:
        add_domains_to_blocklist([args.domain], verbose=args.verbose)
    elif args.file:
        import_domains_from_file(args.file, verbose=args.verbose)
    else:
        print("Errore: è necessario specificare un dominio con -d o un file con -f.")

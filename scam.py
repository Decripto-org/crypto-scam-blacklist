import argparse
import os
from tqdm import tqdm
import json

def format_domain(domain):
    return f'||{domain[4:] if domain.startswith("www.") else domain}^'

def add_domains_to_blocklist(domains, filename='crypto_scam_blocklist.txt', verbose=False):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            existing_domains = set(line.strip() for line in file)
    else:
        existing_domains = set()

    new_domains = set(format_domain(domain) for domain in domains)
    combined_domains = existing_domains.union(new_domains)
    if combined_domains != existing_domains:
        with open(filename, 'w') as file:
            for domain in tqdm(sorted(combined_domains), desc="Writing blocklist", total=len(combined_domains)):
                file.write(f"{domain}\n")
                if verbose and (domain in new_domains):
                    print(f"Added: {domain}")
        print(f"Total {len(new_domains - existing_domains)} new domains added to blocklist.")
    else:
        print("No new domain added.")

def remove_domains_from_blocklist(domains, filename='crypto_scam_blocklist.txt', verbose=False):
    if not os.path.exists(filename):
        print(f"Error: blocklist file {filename} does not exist.")
        return
    
    with open(filename, 'r') as file:
        existing_domains = set(line.strip() for line in file)

    formatted_domains = set(format_domain(domain) for domain in domains)
    updated_domains = existing_domains - formatted_domains
    if updated_domains != existing_domains:
        with open(filename, 'w') as file:
            for domain in tqdm(sorted(updated_domains), desc="Updating blocklist", total=len(updated_domains)):
                file.write(f"{domain}\n")
                if verbose and (domain in formatted_domains):
                    print(f"Removed: {domain}")
        print(f"Total {len(existing_domains - updated_domains)} domains removed from blocklist.")
    else:
        print("No domain removed.")

def import_domains_from_file(file_path, operation, filename='crypto_scam_blocklist.txt', verbose=False):
    if not os.path.exists(file_path):
        print(f"Error: file {file_path} does not exist.")
        return
    
    with open(file_path, 'r') as file:
        domains = [line.strip() for line in file if line.strip()]
    
    if operation == 'add':
        add_domains_to_blocklist(domains, filename, verbose)
    elif operation == 'remove':
        remove_domains_from_blocklist(domains, filename, verbose)

def clean_domains(input_file, output_file):
    print("Updating JSON file...")
    cleaned_domains = set()

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            domain = line.split('||')[-1].split('^')[0].strip()
            cleaned_domains.add(domain)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(list(cleaned_domains), f, indent=4)
        print("JSON file updated.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manage domains in the crypto scam blocklist.')
    parser.add_argument('-d', '--domain', type=str, help='Domain to add or remove from the blocklist.')
    parser.add_argument('-f', '--file', type=str, help='File containing domains to add or remove from the blocklist.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show details of domains as they are processed.')
    parser.add_argument('-r', '--remove', action='store_true', help='Remove domains from the blocklist using the specified domain or file.')
    
    args = parser.parse_args()

    if args.domain:
        if args.remove:
            remove_domains_from_blocklist([args.domain], verbose=args.verbose)
        else:
            add_domains_to_blocklist([args.domain], verbose=args.verbose)
    elif args.file:
        if args.remove:
            import_domains_from_file(args.file, 'remove', verbose=args.verbose)
        else:
            import_domains_from_file(args.file, 'add', verbose=args.verbose)
    else:
        print("Error: You must specify a domain with -d or a file with -f.")

    input_file = 'crypto_scam_blocklist.txt'
    output_file = 'json_domains.json'
    clean_domains(input_file, output_file)
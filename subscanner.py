#!/usr/bin/env python3
"""
Advanced Subdomain Scanner - Passive Reconnaissance Tool (v3.8.1)
"""

import os
import re
import json
import argparse
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

init(autoreset=True)

VERSION = "3.8.1"
AUTHOR = "Unknown Destroyer"
BANNER = f"""
{Fore.CYAN}
EEEEEEEEEEEEEEEEEEEEEE                 HHHHHHHHH     HHHHHHHHH                                     kkkkkkkk           
E::::::::::::::::::::E                 H:::::::H     H:::::::H                                     k::::::k           
E::::::::::::::::::::E                 H:::::::H     H:::::::H                                     k::::::k           
EE::::::EEEEEEEEE::::E                 HH::::::H     H::::::HH                                     k::::::k           
  E:::::E       EEEEEEzzzzzzzzzzzzzzzzz  H:::::H     H:::::H    aaaaaaaaaaaaa      cccccccccccccccc k:::::k    kkkkkkk
  E:::::E             z:::::::::::::::z  H:::::H     H:::::H    a::::::::::::a   cc:::::::::::::::c k:::::k   k:::::k 
  E::::::EEEEEEEEEE   z::::::::::::::z   H::::::HHHHH::::::H    aaaaaaaaa:::::a c:::::::::::::::::c k:::::k  k:::::k  
  E:::::::::::::::E   zzzzzzzz::::::z    H:::::::::::::::::H             a::::ac:::::::cccccc:::::c k:::::k k:::::k   
  E:::::::::::::::E         z::::::z     H:::::::::::::::::H      aaaaaaa:::::ac::::::c     ccccccc k::::::k:::::k    
  E::::::EEEEEEEEEE        z::::::z      H::::::HHHHH::::::H    aa::::::::::::ac:::::c              k:::::::::::k     
  E:::::E                 z::::::z       H:::::H     H:::::H   a::::aaaa::::::ac:::::c              k:::::::::::k     
  E:::::E       EEEEEE   z::::::z        H:::::H     H:::::H  a::::a    a:::::ac::::::c     ccccccc k::::::k:::::k    
EE::::::EEEEEEEE:::::E  z::::::zzzzzzzzHH::::::H     H::::::HHa::::a    a:::::ac:::::::cccccc:::::ck::::::k k:::::k   
E::::::::::::::::::::E z::::::::::::::zH:::::::H     H:::::::Ha:::::aaaa::::::a c:::::::::::::::::ck::::::k  k:::::k  
E::::::::::::::::::::Ez:::::::::::::::zH:::::::H     H:::::::H a::::::::::aa:::a cc:::::::::::::::ck::::::k   k:::::k 
EEEEEEEEEEEEEEEEEEEEEEzzzzzzzzzzzzzzzzzHHHHHHHHH     HHHHHHHHH  aaaaaaaaaa  aaaa   cccccccccccccccckkkkkkkk    kkkkkkk
{Style.RESET_ALL}
v{VERSION} by {AUTHOR}
"""

NOTICE = (
    "⚠️ IMPORTANT NOTICE ⚠️\n"
    "EZHACK WILL BECOME A COMPLETELY NEW TOOL IN THE FUTURE.\n"
    "THIS FILE MAY BE AUTOMATICALLY DELETED SOON.\n"
    "IF YOU NOTICE THAT SUBSCANNER IS NOT WORKING LATER,\n"
    "IT MEANS THE TOOL IS BEING REPLACED WITH THE NEW VERSION!\n"
)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_help():
    clear_terminal()
    print(BANNER)
    print(f"{Fore.RED}{NOTICE}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Usage: subscanner.py -d DOMAIN [-o OUTPUT_FILE]{Style.RESET_ALL}")
    print("\nOptions:")
    print(f"{Fore.GREEN}{'-d, --domain':<20}{Style.RESET_ALL} Target domain to scan (required)")
    print(f"{Fore.GREEN}{'-o, --output':<20}{Style.RESET_ALL} Output file to save results")
    print(f"{Fore.GREEN}{'-h, --help':<20}{Style.RESET_ALL} Show this help message")
    print("\nExample:")
    print(f"  {Fore.CYAN}python3 main.py -d example.com -o results.txt{Style.RESET_ALL}")

def get_crtsh_subdomains(domain):
    subdomains = set()
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        response = requests.get(url, timeout=15, verify=False)
        if response.status_code == 200:
            data = json.loads(response.text)
            for entry in data:
                names = entry['name_value'].split('\n')
                for name in names:
                    sub = name.strip().lower()
                    if sub.endswith(f".{domain}") and '*' not in sub:
                        subdomains.add(sub)
    except Exception as e:
        print(f"{Fore.RED}[!] Error fetching crt.sh: {str(e)}{Style.RESET_ALL}")
    return subdomains

def get_dnsdumpster_subdomains(domain):
    subdomains = set()
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        session = requests.Session()
        
        # CSRF token
        resp = session.get("https://dnsdumpster.com", headers=headers)
        soup = BeautifulSoup(resp.text, 'html.parser')
        csrf_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        
        if not csrf_input:
            print(f"{Fore.RED}[!] DNSDumpster CSRF token bulunamadı{Style.RESET_ALL}")
            return subdomains
            
        csrf = csrf_input['value']
        
        # POST
        data = {'csrfmiddlewaretoken': csrf, 'targetip': domain}
        resp = session.post("https://dnsdumpster.com/", data=data, headers=headers)
        
        # parse
        soup = BeautifulSoup(resp.text, 'html.parser')
        for td in soup.find_all('td', class_='col-md-4'):
            subdomain = td.text.strip().split()[0]
            if subdomain.endswith(f".{domain}"):
                subdomains.add(subdomain)
    except Exception as e:
        print(f"{Fore.RED}[!] Error fetching DNSDumpster: {str(e)}{Style.RESET_ALL}")
    return subdomains

def get_threatcrowd_subdomains(domain):
    subdomains = set()
    try:
        # ssl cerft
        url = f"http://threatcrowd.org/searchApi/v2/domain/report/?domain={domain}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for sub in data.get('subdomains', []):
                sub = sub.strip().lower()
                if sub.endswith(f".{domain}"):
                    subdomains.add(sub)
    except Exception as e:
        print(f"{Fore.RED}[!] Error fetching ThreatCrowd: {str(e)}{Style.RESET_ALL}")
    return subdomains

def get_hackertarget_subdomains(domain):
    subdomains = set()
    try:
        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            for line in response.text.split('\n'):
                if ',' in line:
                    sub = line.split(',')[0].strip()
                    if sub.endswith(f".{domain}"):
                        subdomains.add(sub)
    except Exception as e:
        print(f"{Fore.RED}[!] Error fetching HackerTarget: {str(e)}{Style.RESET_ALL}")
    return subdomains

def validate_domain(domain):
    # verif
    pattern = r"^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,7}$"
    return re.match(pattern, domain)

def main():
    # parse again
    parser = argparse.ArgumentParser(
        description="Advanced Subdomain Scanner",
        add_help=False,
        usage="python3 subscanner.py -d DOMAIN [-o OUTPUT_FILE]"
    )
    
    parser.add_argument(
        "-d", "--domain",
        help="Target domain to scan (required)",
        type=str,
        required=False
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file to save results",
        type=str,
        required=False
    )
    
    parser.add_argument(
        "-h", "--help",
        action="store_true",
        help="Show help message and exit"
    )

    args = parser.parse_args()

    if args.help or not args.domain:
        print_help()
        return

    if not validate_domain(args.domain):
        print(f"{Fore.RED}[!] Geçersiz domain formatı. Örnek: example.com{Style.RESET_ALL}")
        return

    clear_terminal()
    print(BANNER)
    print(f"{Fore.RED}{NOTICE}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Starting scan for: {args.domain}{Style.RESET_ALL}")
    
    subdomains = set()
    subdomains.update(get_crtsh_subdomains(args.domain))
    subdomains.update(get_dnsdumpster_subdomains(args.domain))
    subdomains.update(get_threatcrowd_subdomains(args.domain))
    subdomains.update(get_hackertarget_subdomains(args.domain))

    valid_subs = sorted([sub for sub in subdomains if validate_domain(sub)])
    
    # show da result
    print(f"\n{Fore.GREEN}[+] Found {len(valid_subs)} subdomains:{Style.RESET_ALL}")
    for sub in valid_subs:
        print(f"  {Fore.CYAN}-{Style.RESET_ALL} {sub}")

    # save 2 da file
    if args.output:
        with open(args.output, 'w') as f:
            f.write('\n'.join(valid_subs))
        print(f"\n{Fore.GREEN}[+] Results saved to: {args.output}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Scan paused by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[!] Unexpected error: {str(e)}{Style.RESET_ALL}")


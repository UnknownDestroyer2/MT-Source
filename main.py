import os
import requests
import json
from colorama import Fore, Style, init

init(autoreset=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_repo_files():
    try:
        repo_api = "https://api.github.com/repos/UnknownDestroyer2/MT-Source/contents/"
        response = requests.get(repo_api, timeout=10)
        response.raise_for_status()
        files = response.json()
        
        file_list = []
        for file_info in files:
            if file_info.get("type") == "file":
                file_list.append(file_info.get("name"))
        return file_list
    except Exception as e:
        print(Fore.RED + f"✗ Failed to fetch repo files: {e}")
        return []

def remove_all_installed_files():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        repo_files = get_repo_files()
        
        if not repo_files:
            print(Fore.YELLOW + "Could not fetch repo file list, using fallback method")
            repo_files = [
                "cms_detector.py", "dns_resolver.py", "harvester.py", 
                "port_scanner.py", "proxssscanner.py", "reverse_ip_lookup.py",
                "sqlinjectscanner.py", "subscanner.py", "usernameosint.py",
                "vulnerability_scanner.py", "whois.py"
            ]
        
        removed_count = 0
        current_script = os.path.basename(__file__)
        
        for filename in repo_files:
            if filename == current_script:
                continue
                
            file_path = os.path.join(current_dir, filename)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(Fore.GREEN + f"✓ Removed {filename}")
                    removed_count += 1
                except Exception as e:
                    print(Fore.RED + f"✗ Failed to remove {filename}: {e}")
        
        return removed_count
        
    except Exception as e:
        print(Fore.RED + f"✗ Error removing installed files: {e}")
        return 0

def remove_startup_shortcut():
    try:
        startup_dir = os.path.join(os.getenv("APPDATA"), r"Microsoft\Windows\Start Menu\Programs\Startup")
        shortcut_path = os.path.join(startup_dir, "MultiTool.lnk")
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)
            print(Fore.GREEN + "✓ Removed startup shortcut")
        else:
            print(Fore.YELLOW + "Startup shortcut not found")
    except Exception as e:
        print(Fore.RED + f"✗ Failed to remove startup shortcut: {e}")

def remove_updater_files():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        files_to_remove = ["updater.log", ".file_hashes.json"]
        
        for file in files_to_remove:
            file_path = os.path.join(current_dir, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(Fore.GREEN + f"✓ Removed {file}")
            else:
                print(Fore.YELLOW + f"{file} not found")
    except Exception as e:
        print(Fore.RED + f"✗ Failed to remove updater files: {e}")

def remove_main_script():
    try:
        current_script = os.path.abspath(__file__)
        print(Fore.GREEN + f"✓ Main script marked for deletion: {os.path.basename(current_script)}")
        return current_script
    except Exception as e:
        print(Fore.RED + f"✗ Failed to mark main script for deletion: {e}")
        return None

def revert_installation():
    print(Fore.RED + Style.BRIGHT + "\n[!] REVERTING INSTALLATION [!]")
    print(Fore.RED + "This will remove ALL MultiTool files including this main script.\n")
    
    confirm = input(Fore.YELLOW + "Are you sure? Type 'YES' to confirm: ")
    if confirm != "YES":
        print(Fore.BLUE + "Revert cancelled.")
        return
    
    print(Fore.RED + "\nStarting removal process...")
    
    remove_startup_shortcut()
    remove_updater_files()
    files_removed = remove_all_installed_files()
    script_to_delete = remove_main_script()
    
    print(Fore.GREEN + Style.BRIGHT + f"\n✓ Revert completed! Removed {files_removed} files.")
    print(Fore.YELLOW + "The MultiTool has been completely removed from your system.")
    
    if script_to_delete:
        print(Fore.RED + "\nThis window will close in 5 seconds...")
        import time
        time.sleep(5)
        
        try:
            os.remove(script_to_delete)
        except:
            pass
        
    exit()

def banner():
    print(Fore.MAGENTA + Style.BRIGHT + """

   ▄▄▄▄███▄▄▄▄   ███    █▄   ▄█           ███      ▄█      ███      ▄██████▄   ▄██████▄   ▄█       
 ▄██▀▀▀███▀▀▀██▄ ███    ███ ███       ▀█████████▄ ███  ▀█████████▄ ███    ███ ███    ███ ███       
 ███   ███   ███ ███    ███ ███          ▀███▀▀██ ███▌    ▀███▀▀██ ███    ███ ███    ███ ███       
 ███   ███   ███ ███    ███ ███           ███   ▀ ███▌     ███   ▀ ███    ███ ███    ███ ███       
 ███   ███   ███ ███    ███ ███           ███     ███▌     ███     ███    ███ ███    ███ ███       
 ███   ███   ███ ███    ███ ███           ███     ███      ███     ███    ███ ███    ███ ███       
 ███   ███   ███ ███    ███ ███▌    ▄     ███     ███      ███     ███    ███ ███    ███ ███▌    ▄ 
  ▀█   ███   █▀  ████████▀  █████▄▄██    ▄████▀   █▀      ▄████▀    ▀██████▀   ▀██████▀  █████▄▄██ 
                            ▀                                                            ▀         

                     """
                     + Fore.CYAN
                     + "v1.3 by Unknown Destroyer."
                     + Style.RESET_ALL
          )

def menu():
    tools = {
        "1": "cms_detector.py",
        "2": "dns_resolver.py",
        "3": "harvester.py",
        "4": "port_scanner.py",
        "5": "proxssscanner.py",
        "6": "reverse_ip_lookup.py",
        "7": "sqlinjectscanner.py",
        "8": "subscanner.py",
        "9": "usernameosint.py",
        "10": "vulnerability_scanner.py",
        "11": "whois.py",
        "0": "LEAVE",
        "99": "Delete the tool from device"
    }

    while True:
        clear()
        banner()
        print(Fore.YELLOW + Style.BRIGHT + "Input the tool you want to run:\n")
        for key, val in tools.items():
            print(f" {Fore.GREEN}[{key}]{Fore.RESET} {val}")

        secim = input(Fore.CYAN + "\n > ")

        if secim == "0":
            print(Fore.RED + "\nLeaving.")
            break
        elif secim == "99":
            revert_installation()
            break
        elif secim in tools:
            tool_name = tools[secim]
            print(Fore.BLUE + f"\nSelected: {tool_name}")
            arguman = input(Fore.CYAN + "What is the arguments? (e.g.: -h to get help): ")
            komut = f'python {tool_name} {arguman}'
            print(Fore.LIGHTMAGENTA_EX + f"\n> Running: {komut}\n")
            os.system(komut)
            input(Fore.YELLOW + "\nPress ENTER to continue.")
        else:
            print(Fore.RED + "\nJust select a valid number. Thats not that hard!")
            input("Press da enter to go back...")

menu()

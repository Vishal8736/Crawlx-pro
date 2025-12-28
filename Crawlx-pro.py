#!/usr/bin/env python3
import sys
import os
import subprocess
import argparse
import requests
import concurrent.futures

# --- Colors for UI ---
G = "\033[32m" # Green
B = "\033[34m" # Blue
Y = "\033[33m" # Yellow
R = "\033[31m" # Red
RESET = "\033[0m"

def banner():
    print(f"""{B}
    ██████╗██████╗  █████╗ ██╗    ██╗██╗     ██╗  ██╗      ██████╗ ██████╗  ██████╗ 
   ██╔════╝██╔══██╗██╔══██╗██║    ██║██║     ╚██╗██╔╝      ██╔══██╗██╔══██╗██╔═══██╗
   ██║     ██████╔╝███████║██║ █╗ ██║██║      ╚███╔╝ █████╗██████╔╝██████╔╝██║   ██║
   ██║     ██╔══██╗██╔══██║██║███╗██║██║      ██╔██╗ ╚════╝██╔═══╝ ██╔══██╗██║   ██║
   ╚██████╗██║  ██║██║  ██║╚███╔███╔╝███████╗██╔╝ ██╗      ██║     ██║  ██║╚██████╔╝
    ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝      ╚═╝     ╚═╝  ╚═╝ ╚═════╝ 
    {Y}Combined Subdomain Hunter & Wayback Crawler Automation{RESET}
    """)

class CrawlXPro:
    def __init__(self):
        self.all_subs = set()

    def fetch_subdomains(self, domain):
        """Fetch from crt.sh and OTX"""
        # Source 1: crt.sh
        try:
            r = requests.get(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=15)
            if r.status_code == 200:
                for item in r.json():
                    name = item['name_value'].lower()
                    for n in name.split("\n"):
                        self.all_subs.add(n.strip().replace("*.", ""))
        except: pass

        # Source 2: AlienVault OTX
        try:
            r = requests.get(f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns", timeout=15)
            if r.status_code == 200:
                for res in r.json().get("passive_dns", []):
                    hostname = res.get("hostname")
                    if hostname: self.all_subs.add(hostname.lower())
        except: pass

    def run_wayback(self, subdomains_file):
        """Pass the subdomains to wayback_urls_deep.sh"""
        if os.path.exists("wayback_urls_deep.sh"):
            print(f"\n{G}[+] Starting Wayback Deep Crawl...{RESET}")
            # Bash command execution
            cmd = ["bash", "wayback_urls_deep.sh", "-f", subdomains_file]
            subprocess.run(cmd)
        else:
            print(f"\n{R}[!] Error: wayback_urls_deep.sh not found in current directory!{RESET}")

    def start(self, targets, output_file):
        print(f"{G}[+] Hunting subdomains for {len(targets)} target(s)...{RESET}")
        
        for domain in targets:
            print(f"{B}[*] Scanning: {domain}{RESET}")
            self.fetch_subdomains(domain)

        # Save unique subdomains to a temp file
        sub_file = "temp_subs.txt"
        with open(sub_file, "w") as f:
            for sub in sorted(list(self.all_subs)):
                if sub: f.write(sub + "\n")
        
        print(f"{G}[✔] Found {len(self.all_subs)} unique subdomains.{RESET}")
        
        # Now trigger the Wayback Tool
        self.run_wayback(sub_file)
        
        # Cleanup temp file if you want, or keep it
        print(f"{Y}[i] Final subdomains list saved in: {sub_file}{RESET}")

if __name__ == "__main__":
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", help="Single domain")
    parser.add_argument("-i", "--input", help="File with domains")
    args = parser.parse_args()

    targets = []
    if args.domain: targets.append(args.domain)
    elif args.input and os.path.exists(args.input):
        with open(args.input, "r") as f:
            targets = [l.strip() for l in f if l.strip()]
    
    if not targets:
        print(f"{R}[!] No targets provided. Use -d or -i{RESET}")
        sys.exit()

    pro = CrawlXPro()
    pro.start(targets, "final_subs.txt")
                      

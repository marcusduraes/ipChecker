import ipaddress
import subprocess


def get_ip_infos(ip, mask):
    ip = ipaddress.IPv4Network(f'{ip}/{mask}', strict=False)
    return {
        'network': ip.network_address,
        'hosts': list(ip.hosts()),
        'broadcast': ip.broadcast_address
    }


def check_gw(ip):
    gw_out = subprocess.check_output(f'nmap -sn {ip}', text=True)
    return gw_out


def main(ip, mask):
    result = get_ip_infos(ip, mask)
    network, hosts, broadcast = result['network'], result['hosts'], result['broadcast']
    is_pppoe = len(hosts) == 1
    ip_out = subprocess.check_output(f'nmap -sn {hosts[-1]}', text=True)

    if not is_pppoe and 'Host is up' not in str(ip_out):
        text = f'{check_gw(hosts[0])}\n\nGW: {hosts[0]} (✅ UP)\nFW: {hosts[-1]} (❌ DOWN)'
        return text if 'Host is up' in text else None
    else:
        return ip_out if 'Host is up' in ip_out else None

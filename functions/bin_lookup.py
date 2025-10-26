import requests
import json

def get_bin_info(bin_number):
    try:
        url = f"https://bins.antipublic.cc/bins/{bin_number}"
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            result = {
                'bin': bin_number,
                'brand': data.get('brand', 'Unknown').upper(),
                'type': data.get('type', 'Unknown').upper(),
                'level': data.get('level', 'Unknown').upper(),
                'bank': data.get('bank', 'Unknown'),
                'country': data.get('country_name', 'Unknown'),
                'country_code': data.get('country', 'XX'),
                'country_flag': data.get('country_flag', '🏳️'),
                'prepaid': 'Yes' if data.get('prepaid', False) else 'No'
            }
            return result
        else:
            return {
                'bin': bin_number,
                'brand': 'Unknown',
                'type': 'Unknown',
                'level': 'Unknown',
                'bank': 'Unknown',
                'country': 'Unknown',
                'country_code': 'XX',
                'country_flag': '🏳️',
                'prepaid': 'Unknown'
            }
    except Exception as e:
        print(f"[ERROR] BIN lookup failed: {e}")
        return {
            'bin': bin_number,
            'brand': 'Unknown',
            'type': 'Unknown',
            'level': 'Unknown',
            'bank': 'Unknown',
            'country': 'Unknown',
            'country_code': 'XX',
            'country_flag': '🏳️',
            'prepaid': 'Unknown'
        }

def get_country_flag(country_code):
    flag_map = {
        'US': '🇺🇸', 'GB': '🇬🇧', 'CA': '🇨🇦', 'IN': '🇮🇳',
        'AU': '🇦🇺', 'DE': '🇩🇪', 'FR': '🇫🇷', 'BR': '🇧🇷',
        'RU': '🇷🇺', 'CN': '🇨🇳', 'JP': '🇯🇵', 'MX': '🇲🇽',
    }
    return flag_map.get(country_code, '🏳️')

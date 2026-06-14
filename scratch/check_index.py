with open('f:/pe/public_html/test-migration/sitepro/index.php', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

idx = content.find('oQoaQ:')
if idx != -1:
    print(content[idx:idx+2000])
else:
    print("oQoaQ not found")

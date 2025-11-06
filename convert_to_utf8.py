import shutil, sys, os
p = r"C:\Users\Osamah Mohammed\Desktop\django\skinsense\models.py"
if not os.path.exists(p):
    print('File not found:', p); sys.exit(1)
bak = p + '.bak'
shutil.copy2(p, bak)
with open(p, 'rb') as f:
    b = f.read()
# detect BOM / encoding
try:
    if b.startswith(b'\xff\xfe') or b.startswith(b'\xfe\xff'):
        txt = b.decode('utf-16')
    elif b.startswith(b'\xef\xbb\xbf'):
        txt = b.decode('utf-8-sig')
    else:
        try:
            txt = b.decode('utf-8')
        except Exception:
            # fallback
            txt = b.decode('latin-1')
except Exception as e:
    print('Decoding failed, using replacement characters:', e)
    try:
        txt = b.decode('utf-8', errors='replace')
    except:
        txt = b.decode('latin-1', errors='replace')
with open(p, 'w', encoding='utf-8', newline='\n') as f:
    f.write(txt)
print('Converted', p, 'to UTF-8; backup at', bak)

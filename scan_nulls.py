import os,sys
root = r"C:\Users\Osamah Mohammed\Desktop\django"
found = []
for rootdir, dirs, files in os.walk(root):
    for f in files:
        if f.endswith('.py'):
            fp = os.path.join(rootdir, f)
            try:
                with open(fp, 'rb') as fh:
                    b = fh.read()
            except Exception as e:
                print('ERR', fp, e)
                continue
            if b'\x00' in b:
                idx = b.find(b'\x00')
                start = max(0, idx - 16)
                snippet = b[start: start + 64]
                print('NULL:', fp)
                print(' offset:', idx)
                print(' hex:', snippet.hex())
                found.append(fp)
if not found:
    print('No NUL bytes found in any .py files.')
else:
    print('\nFound', len(found), 'files with NUL bytes.')

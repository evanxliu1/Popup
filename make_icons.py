from PIL import Image
import os

# Paths
src = 'downloaded_images/IMG_4278.JPG'
icns_out = 'app_icon.icns'
ico_out = 'app_icon.ico'

# Required icon sizes for ICNS
icns_sizes = [16, 32, 64, 128, 256, 512, 1024]
iconset = {}

img = Image.open(src).convert('RGBA')

# Generate PNGs for all sizes and collect for icnsutil
for size in icns_sizes:
    fname = f'icon_{size}.png'
    img_resized = img.resize((size, size), Image.LANCZOS)
    img_resized.save(fname, format='PNG', quality=100)
    iconset[size] = fname

# Create ICO (Windows)
img.save(ico_out, format='ICO', sizes=[(256,256), (128,128), (64,64), (32,32), (16,16)])

# Create ICNS (Mac) using icnsutil if available
try:
    import icnsutil
    from icnsutil import IconSet, IcnsFile
    iconset_obj = IconSet()
    for size, fname in iconset.items():
        iconset_obj.add_icon(size, fname)
    icns = IcnsFile.from_iconset(iconset_obj)
    with open(icns_out, 'wb') as f:
        icns.write(f)
    print('ICNS icon created!')
except ImportError:
    print('Install icnsutil to create .icns: pip install icnsutil')
    print('PNG and ICO created.')

print('Done.')

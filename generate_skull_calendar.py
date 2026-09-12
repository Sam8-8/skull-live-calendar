from PIL import Image, ImageDraw, ImageFont, ImageFilter
from datetime import date, datetime
import os, calendar, argparse

BASE = os.path.dirname(__file__)
BG = os.path.join(BASE, 'a73878054e629d404eff3240bf3483d1.jpg')
OUT = os.path.join(BASE, 'skull_live_calendar.png')
W, H = 1080, 2400
MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']

def font(size, bold=False):
    paths = ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
             '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']
    for p in paths:
        if os.path.exists(p): return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def cover(im, size):
    scale=max(size[0]/im.width, size[1]/im.height)
    r=im.resize((round(im.width*scale),round(im.height*scale)), Image.Resampling.LANCZOS)
    x,y=(r.width-size[0])//2,(r.height-size[1])//2
    return r.crop((x,y,x+size[0],y+size[1]))

def make(target):
    bg=cover(Image.open(BG).convert('RGB'),(W,H)).convert('RGBA')
    # A large, faint calendar layer centered behind the skull. The top 300 px stay empty for the clock.
    layer=Image.new('RGBA',(980,1150),(0,0,0,0))
    d=ImageDraw.Draw(layer)
    month=MONTHS[target.month-1]
    # Very restrained title, intentionally behind the illustration.
    title=month.upper()
    tb=d.textbbox((0,0),title,font=font(46))
    d.text(((980-(tb[2]-tb[0]))//2,28),title,font=font(46),fill=(210,207,190,92))
    yyear=82
    yfont=font(19)
    yb=d.textbbox((0,0),str(target.year),font=yfont)
    d.text(((980-(yb[2]-yb[0]))//2,yyear),str(target.year),font=yfont,fill=(178,181,166,65))
    start=calendar.monthrange(target.year,target.month)[0]
    days=calendar.monthrange(target.year,target.month)[1]
    # Large 7-column grid, spread across the skull area.
    left,top,dx,dy,radius=90,155,132,86,13
    for day in range(1,days+1):
        idx=start+day-1; row,col=idx//7,idx%7
        cx,cy=left+col*dx,top+row*dy
        current=date(target.year,target.month,day)
        # Palette sampled conceptually from the wallpaper: bone-white past days,
        # muted terracotta for today, and desaturated sage-gray for future days.
        if current<target: color=(205,207,193,92)
        elif current==target: color=(164,112,83,170)
        else: color=(116,128,119,68)
        d.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),fill=color)
    # Soft blur and low opacity make the calendar read as part of the background.
    layer=layer.filter(ImageFilter.GaussianBlur(1.2))
    # Position behind the skull's face, not in the clock area.
    bg.alpha_composite(layer,(50,360))
    bg.convert('RGB').save(OUT,quality=95)
    return OUT

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--date',default=None)
    args=ap.parse_args()
    target=date.fromisoformat(args.date) if args.date else datetime.now().date()
    print(make(target)); print(target.isoformat())

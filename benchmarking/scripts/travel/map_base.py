"""Draw a plain lower-48 US map (Albers equal-area) as a PNG, and give the projection used, so logos can be placed on
top of it in PowerPoint at the right spots. Output: slides/travel/us_map.png and slides/travel/map_meta.json."""
import shapefile,json,math,os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
os.makedirs('slides/travel',exist_ok=True)
lat1,lat2,lat0,lon0=map(math.radians,(29.5,45.5,23.0,-96.0))
n=(math.sin(lat1)+math.sin(lat2))/2; C=math.cos(lat1)**2+2*n*math.sin(lat1); r0=math.sqrt(C-2*n*math.sin(lat0))/n
def proj(lat,lon):
    la,lo=math.radians(lat),math.radians(lon); r=math.sqrt(C-2*n*math.sin(la))/n; th=n*(lo-lon0)
    return r*math.sin(th), r0-r*math.cos(th)
sf=shapefile.Reader('data/geo/states/cb_2024_us_state_20m.shp')
fig=plt.figure(figsize=(9.0,5.2),dpi=300); ax=fig.add_axes([0,0,1,1]); ax.set_axis_off()
xs=[];ys=[]
for rec,shp in zip(sf.records(),sf.shapes()):
    if rec['STUSPS'] in ('AK','HI','PR'): continue
    pts=shp.points; parts=list(shp.parts)+[len(pts)]
    for a,b in zip(parts[:-1],parts[1:]):
        P=[proj(y,x) for x,y in pts[a:b]]; xs+= [p[0] for p in P]; ys+=[p[1] for p in P]
        ax.add_patch(Polygon(P,closed=True,facecolor='#E3E3E3',edgecolor='#FFFFFF',linewidth=0.6))
pad=0.01; x0,x1,y0,y1=min(xs)-pad,max(xs)+pad,min(ys)-pad,max(ys)+pad
# keep the figure's aspect equal to the data's
w,h=x1-x0,y1-y0; fig.set_size_inches(9.0,9.0*h/w); ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); ax.set_aspect('equal')
fig.savefig('slides/travel/us_map.png',dpi=300,transparent=True)
json.dump(dict(x0=x0,x1=x1,y0=y0,y1=y1,aspect=h/w,lat1=29.5,lat2=45.5,lat0=23.0,lon0=-96.0),open('slides/travel/map_meta.json','w'))
print('map aspect',round(h/w,3))

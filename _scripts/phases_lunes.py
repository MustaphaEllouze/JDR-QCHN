import matplotlib.pyplot as plt
from math import cos, sin, pi, acos
import matplotlib.animation as animation
import numpy as np

POS_VELTA_X=0.0
POS_VELTA_Y=0.0
RAYON_LUNES=1.0
RAYON_SOLEIL=2.0
RAYON_INTER_LUNES=0.1
ORBITE_SOLEIL=198
ORBITE_LUNES=99
ORBITE_INTER_LUNES=18# Dans le référentiel de velta
ORBITE_INTER_LUNES_ABSOLU=2*ORBITE_INTER_LUNES/(1+2*ORBITE_INTER_LUNES/ORBITE_LUNES)
ITERATIONS=200
LISTE_TEMPS=[
       2*i*ORBITE_SOLEIL/ITERATIONS
        for i in range(0,ITERATIONS)
    ]

LISTE_TEMPS=[
    49.5
]

# MATPLOTLIB
fig,(ax,ax2)=plt.subplots(nrows=1,ncols=2)

# Velta
ax.scatter(
    [POS_VELTA_X],
    [POS_VELTA_Y],
    color='black', 
    marker='x',     
    label='Velta',
    )

# Soleil
positions_soleil_x=[
    RAYON_SOLEIL*cos(2*pi*temps/ORBITE_SOLEIL)
    for temps in LISTE_TEMPS
]

positions_soleil_y=[
    RAYON_SOLEIL*sin(2*pi*temps/ORBITE_SOLEIL)
    for temps in LISTE_TEMPS
]

scat_soleil=ax.scatter(  
    positions_soleil_x, 
    positions_soleil_y,  
    color='gray',  
    marker='o', 
    label='Soleil',
)

# Centre lunes

positions_clune_x=[RAYON_LUNES*cos(2*pi*temps/ORBITE_LUNES) for temps in LISTE_TEMPS]
positions_clune_y=[RAYON_LUNES*sin(2*pi*temps/ORBITE_LUNES) for temps in LISTE_TEMPS]

scat_centre_lune=ax.scatter(  
    positions_clune_x, 
    positions_clune_y,
    color='green', 
    marker='.', 
    label='Centre lunes',
)

# Portion éclairée des lunes

# -- Ceci contient les angles d'illumination : 
# --- 0° == Nouvelle lune
# --- 0° -> 90° --> Premier croissant
# --- 90° -> 180° --> Lune gibbeuse
# --- 180° ==  Pleine lune
# --- 180° -> 270° --> Lune gibbeuse
# --- 270° -> 360° --> Dernier croissant
portion_eclairee=[(2*pi*temps/ORBITE_LUNES-2*pi*temps/ORBITE_SOLEIL)%(2*pi) for temps in LISTE_TEMPS]

# --- On doit passer à ceci 
# --- 0°-> 180 == négatif, 0 -> 1
# --- 180°-> 360 == positif, 1 -> 0

parametres_eclaire = [
    (-1, port/pi)
    if port<=pi
    else (1, (pi-port)/pi+1)
    for port in portion_eclairee
]

def calc_crescent_pos(r1,r2,mn):
    # mn = Illuminated percentage of the moon
    # r1 = radius of the moon circle
    # r2 = radius of the shadow circle
    lune=0
    d=r2-r1
    area=np.pi*r1**2 # area of the moon circle
    while lune/area < mn: #increase separation between the 2 circles, until the area of the moon crescent is equal to the illuminated percentage of the moon
        try: 
            d=d+0.01
            lune = 2*(np.sqrt( (r1+r2+d) * (r2+d-r1) * (d+r1-r2) * (r1+r2-d))/ 4) + r1**2 * acos( (r2**2-r1**2-d**2) / (2*r1*d) ) - r2**2 * acos( (r2**2+d**2-r1**2) / (2*r2*d))                                     
        except : break
    return d-0.01


#Circle1; full moon
theta=np.linspace(0, 2*np.pi, 100)
# the radius of the circle
r1 = np.sqrt(1)
c1x = r1*np.cos(theta)
c1y = r1*np.sin(theta)

#Circle 2; Shadow
r2 = np.sqrt(2)
c2x = r2*np.cos(theta)
c2y = r2*np.sin(theta)

#Circle to hide all circles
# the radius of the circle
r = np.sqrt(4)
c3x = r*np.cos(theta)
c3y = r*np.sin(theta)

# Geshn 

position_geshn_x=[   pos_c_x+RAYON_INTER_LUNES*cos(2*pi*temps/ORBITE_INTER_LUNES_ABSOLU)   for pos_c_x,temps in zip(positions_clune_x,LISTE_TEMPS)]

position_geshn_y=[   pos_c_y+RAYON_INTER_LUNES*sin(2*pi*temps/ORBITE_INTER_LUNES_ABSOLU)   for pos_c_y,temps in zip(positions_clune_y,LISTE_TEMPS)]

scat_geshn=ax.scatter( 
    position_geshn_x, 
    position_geshn_y,  
    color='red',  
    marker='o',  
    label='Geshn',
)

# Kelr 
position_kelr_x=[   pos_c_x+RAYON_INTER_LUNES*cos(2*pi*temps/ORBITE_INTER_LUNES_ABSOLU+pi)   for pos_c_x,temps in zip(positions_clune_x,LISTE_TEMPS)]
position_kelr_y=[   pos_c_y+RAYON_INTER_LUNES*sin(2*pi*temps/ORBITE_INTER_LUNES_ABSOLU+pi)   for pos_c_y,temps in zip(positions_clune_y,LISTE_TEMPS)]
scat_kelr=ax.scatter(
    position_kelr_x,  
    position_kelr_y, 
    color='blue', 
    marker='o', 
    label='Kelr',
)

def show_phase_at_this(
        eclairage:float,
        facteur:int,
)->None:
    # Phases
    ax2.cla()
    ax2.plot(c1x, c1y,color='k',lw=2)
    xmn=calc_crescent_pos(r1,r2,eclairage)
    ax2.fill(c2x+xmn*facteur, c2y,color='k',lw=2)

    ax2.plot(c3x, c3y,color='w')

    ax2.fill_between(c3x,c3y,c1y,color='w',zorder=2)
    ax2.fill_betweenx(c1x,c1y,c3y,color='w',zorder=2)
    
    ax2.set_xlim(-1., 1)
    ax2.set_ylim(-1., 1)
    

def update(frame):   

    psx=positions_soleil_x[frame%ITERATIONS]
    psy=positions_soleil_y[frame%ITERATIONS]
    scat_soleil.set_offsets((psx,psy))

    pclx=positions_clune_x[frame%ITERATIONS]
    pcly=positions_clune_y[frame%ITERATIONS]
    scat_centre_lune.set_offsets((pclx,pcly))

    gx=position_geshn_x[frame%ITERATIONS]
    gy=position_geshn_y[frame%ITERATIONS]
    scat_geshn.set_offsets((gx,gy))

    gx=position_kelr_x[frame%ITERATIONS]
    gy=position_kelr_y[frame%ITERATIONS]
    scat_kelr.set_offsets((gx,gy))

    # Phases
    show_phase_at_this(
        eclairage=parametres_eclaire[frame%ITERATIONS][1],
        facteur=parametres_eclaire[frame%ITERATIONS][0],
    )

    return (
        scat_soleil,
        scat_centre_lune,
        scat_geshn,
        scat_kelr,
    )

# ani=animation.FuncAnimation(fig=fig,func=update,frames=ITERATIONS,interval=30)

if len(LISTE_TEMPS)==1:
    show_phase_at_this(
        eclairage=parametres_eclaire[0][1],
        facteur=parametres_eclaire[0][0],
    )

# Configuration
ax.legend()
ax.set_xlim(-RAYON_SOLEIL-0.1, RAYON_SOLEIL+0.1)
ax.set_ylim(-RAYON_SOLEIL-0.1, RAYON_SOLEIL+0.1)
ax.set_aspect('equal')
ax2.set_aspect('equal')
plt.show()


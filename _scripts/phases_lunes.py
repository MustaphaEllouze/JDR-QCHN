import matplotlib.pyplot as plt
from math import cos, sin, pi
import matplotlib.animation as animation

POS_VELTA_X=0.0
POS_VELTA_Y=0.0
RAYON_LUNES=1.0
RAYON_SOLEIL=2.0
RAYON_INTER_LUNES=0.1
ORBITE_SOLEIL=198
ORBITE_LUNES=99
ORBITE_INTER_LUNES=18# Dans le référentiel de velta
ORBITE_INTER_LUNES_ABSOLU=2*ORBITE_INTER_LUNES/(1+2*ORBITE_INTER_LUNES/ORBITE_LUNES)
ITERATIONS=1000
LISTE_TEMPS=[
       2*i*ORBITE_SOLEIL/ITERATIONS
        for i in range(0,ITERATIONS)
    ]

LISTE_TEMPS = [
    9*(12-1)
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
                 label='Soleil',)

# Centre lunes

positions_clune_x=[RAYON_LUNES*cos(2*pi*temps/ORBITE_LUNES) for temps in LISTE_TEMPS]
positions_clune_y=[RAYON_LUNES*sin(2*pi*temps/ORBITE_LUNES) for temps in LISTE_TEMPS]

scat_centre_lune=ax.scatter(  
     positions_clune_x, 
         positions_clune_y,
               color='green', 
                   marker='.', 
                       label='Centre lunes',)

# Portion éclairée des lunes
portion_eclairee=[2*pi*temps/ORBITE_LUNES-2*pi*temps/ORBITE_SOLEIL for temps in LISTE_TEMPS]

def calcule_eclaire(theta:float): 
    if theta<=pi:
        pass
    else :
        passpourcentage_eclairee=[]

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
    return(scat_soleil,scat_centre_lune,scat_geshn,scat_kelr)

# ani=animation.FuncAnimation(fig=fig,func=update,frames=ITERATIONS,interval=30)

# Configuration
ax.legend()
plt.show()
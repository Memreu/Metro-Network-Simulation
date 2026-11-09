"""Örnek metro ağını ve A* ile bulunan en hızlı rotayı çizer.

Kullanım:  python scripts/readme_grafikleri.py
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid", font="DejaVu Sans")
plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 110, "axes.titleweight": "bold", "axes.titlesize": 13,
    "axes.labelsize": 11, "axes.spines.top": False, "axes.spines.right": False,
})
BLUE="#2E5EAA"; RED="#C0392B"; ORANGE="#E67E22"; GREEN="#29A36A"; GREY="#8C8C8C"; GOLD="#F2A900"
def save(fig, path):
    fig.tight_layout(); fig.savefig(path, bbox_inches="tight", facecolor="white"); plt.close(fig); print("kaydedildi:", path)

import sys,os
R=str(Path(__file__).resolve().parents[1]); os.makedirs(R+'/images',exist_ok=True)
sys.path.insert(0,R); import importlib; ms=importlib.import_module('metro_simulation')
m=ms.MetroAgi()
st=[("K1","Kızılay","Kırmızı Hat"),("K2","Ulus","Kırmızı Hat"),("K3","Demetevler","Kırmızı Hat"),("K4","OSB","Kırmızı Hat"),
("M1","AŞTİ","Mavi Hat"),("M2","Kızılay","Mavi Hat"),("M3","Sıhhiye","Mavi Hat"),("M4","Gar","Mavi Hat"),
("T1","Batıkent","Turuncu Hat"),("T2","Demetevler","Turuncu Hat"),("T3","Gar","Turuncu Hat"),("T4","Keçiören","Turuncu Hat")]
for s in st: m.istasyon_ekle(*s)
E=[("K1","K2",4),("K2","K3",6),("K3","K4",8),("M1","M2",5),("M2","M3",3),("M3","M4",4),("T1","T2",7),("T2","T3",9),("T3","T4",5),("K1","M2",2),("K3","T2",3),("M4","T3",2)]
for a,b,w in E: m.baglanti_ekle(a,b,w)
rota,sure=m.en_hizli_rota_bul("M1","K4"); path=[i.idx for i in rota]; print(path,sure)
pos={"K1":(4,4),"K2":(2.5,5.2),"K3":(1,4.2),"K4":(-0.8,4.2),"M1":(6,5.5),"M2":(4.6,3.6),"M3":(4.6,2.2),"M4":(3.6,1),"T1":(-0.6,1.9),"T2":(1,2.9),"T3":(3,0.6),"T4":(4.6,-0.4)}
col={"Kırmızı Hat":RED,"Mavi Hat":BLUE,"Turuncu Hat":ORANGE}
hat={i:h for i,_,h in st}; ad={i:a for i,a,_ in st}
fig,ax=plt.subplots(figsize=(11,7))
pe=set(zip(path,path[1:]))|set(zip(path[1:],path))
for a,b,w in E:
    x=[pos[a][0],pos[b][0]]; y=[pos[a][1],pos[b][1]]
    same=hat[a]==hat[b]
    if (a,b) in pe: ax.plot(x,y,color="#2ECC71",lw=13,alpha=.35,solid_capstyle="round",zorder=1)
    ax.plot(x,y,color=col[hat[a]] if same else GREY,lw=5 if same else 2,ls="-" if same else ":",zorder=2)
    ax.text(sum(x)/2+(.25 if x[0]==x[1] else 0),sum(y)/2+(0 if x[0]==x[1] else .13),f"{w} dk",ha="center",fontsize=9,color="#333",bbox=dict(fc="white",ec="none",pad=1),zorder=4)
for n,(x,y) in pos.items():
    ax.scatter(x,y,s=260,color="white",edgecolor=col[hat[n]],lw=3,zorder=5)
    off={"M2":(.3,0,"left","center"),"M3":(.3,0,"left","center"),"K3":(0,.33,"center","bottom"),"K2":(0,.33,"center","bottom")}.get(n,(0,-.33,"center","top"))
    ax.text(x+off[0],y+off[1],f"{ad[n]}\n({n})",ha=off[2],va=off[3],fontsize=9,zorder=6)
from matplotlib.lines import Line2D
h=[Line2D([0],[0],color=c,lw=5,label=k) for k,c in col.items()]+[Line2D([0],[0],color=GREY,lw=2,ls=":",label="Aktarma"),Line2D([0],[0],color="#2ECC71",lw=10,alpha=.4,label=f"En hızlı rota AŞTİ → OSB ({sure} dk)")]
ax.legend(handles=h,loc="lower left",fontsize=9); ax.set_axis_off(); ax.set_title("Örnek metro ağı ve A* ile bulunan en hızlı rota")
ax.set_xlim(-1.6,6.8); ax.set_ylim(-1.3,6.1)
save(fig,R+'/images/01_metro_agi.png')

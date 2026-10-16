"""Draw the six-burst common interior release directly as a vector PDF."""
import argparse
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir",type=Path,default=Path(__file__).resolve().parents[1]/"figures")
    args=parser.parse_args()
    args.outdir.mkdir(parents=True,exist_ok=True)
    try:
        font_manager.findfont("Times New Roman",fallback_to_default=False)
        font="Times New Roman"
    except ValueError:
        font="STIXGeneral"
    plt.rcParams.update({"font.family":font,"font.size":8,"mathtext.fontset":"stix",
                         "pdf.fonttype":42,"ps.fonttype":42,"text.usetex":False})
    fig,ax=plt.subplots(figsize=(3.35,1.82))
    fig.subplots_adjust(left=.11,right=.98,bottom=.25,top=.88)
    for j in range(6):
        ax.plot([j,j+6],[-j,-j],color="black",linewidth=.8)
        ax.plot([j,j],[-j-.13,-j+.13],color="black",linewidth=.7)
        ax.plot([j+6,j+6],[-j-.13,-j+.13],color="black",linewidth=.7)
        ax.plot(5,-j,"o",color="black",markersize=3)
    ax.axvline(5,color="black",linestyle="--",linewidth=.7)
    ax.text(5,.8,r"$t=5$",ha="center",va="center")
    ax.set(xlim=(-.4,11.5),ylim=(-5.7,.35),xticks=[0,5,6,11],
           yticks=list(range(0,-6,-1)),yticklabels=[f"j={j}" for j in range(6)],
           xlabel="Time (service units)")
    ax.tick_params(axis="y",length=0,pad=3)
    ax.tick_params(axis="x",length=2,pad=2)
    for side in ("left","right","top"):ax.spines[side].set_visible(False)
    fig.canvas.draw()
    bounds=fig.bbox
    for label in [*ax.get_xticklabels(),*ax.get_yticklabels(),ax.xaxis.label,*ax.texts]:
        box=label.get_window_extent()
        if box.x0<bounds.x0-1 or box.x1>bounds.x1+1 or box.y0<bounds.y0-1 or box.y1>bounds.y1+1:
            raise ValueError("Label outside figure: "+label.get_text())
    fig.savefig(args.outdir/"windows.pdf",metadata={"CreationDate":None,"ModDate":None})
    plt.close(fig)
    print("windows.pdf: six closed windows and their common release at t=5")
if __name__=="__main__":
    main()

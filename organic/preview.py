"""Preview from actual STL triangle geometry, including a true middle cross-section."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as MplPath
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def preview(mesh, spec, filepath):
    fig = plt.figure(figsize=(12, 5), dpi=140)
    fig.patch.set_facecolor('#f6f8fa')
    ax = fig.add_subplot(121)
    ax.set_facecolor('#f6f8fa')
    section = mesh.section(plane_origin=[0, 0, 0], plane_normal=[0, 1, 0])
    if section is None:
        raise RuntimeError('No center-section through mesh; verify node Y positions')
    outlines = [curve[:, [0, 2]] for curve in section.discrete]
    def area(p):
        return abs(float(np.dot(p[:, 0], np.roll(p[:, 1], -1))
                         - np.dot(p[:, 1], np.roll(p[:, 0], -1))) / 2)
    outlines.sort(key=area, reverse=True)
    for idx, poly in enumerate(outlines):
        point=poly[0]
        parents=sum(MplPath(larger).contains_point(point) for larger in outlines[:idx])
        color = '#5b879d' if parents % 2 == 0 else '#f6f8fa'
        ax.fill(poly[:,0], poly[:,1], facecolor=color,
                edgecolor='#21465b', linewidth=1.1, antialiased=True)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(mesh.bounds[0,0]-6,mesh.bounds[1,0]+6)
    ax.set_ylim(mesh.bounds[0,2]-6,mesh.bounds[1,2]+6)
    ax.set_xlabel('X (mm)'); ax.set_ylabel('Z (mm)')
    ax.set_title('Actual center section (Y = 0)')
    ax.grid(alpha=.12)
    ax3=fig.add_subplot(122,projection='3d')
    tris3=mesh.triangles
    normals=mesh.face_normals
    sun=np.array([.4,-.7,.6]);sun/=np.linalg.norm(sun)
    brightness=np.clip(.42+.50*np.abs(normals@sun),.20,1)
    colors=np.stack((.34*brightness,.56*brightness,.72*brightness,np.ones_like(brightness)),axis=1)
    collection=Poly3DCollection(tris3,facecolors=colors,linewidths=0,edgecolors='none', zsort='average')
    ax3.add_collection3d(collection)
    ext=mesh.bounds
    for f,lo,hi in [(ax3.set_xlim,ext[0,0],ext[1,0]),(ax3.set_ylim,ext[0,1],ext[1,1]),(ax3.set_zlim,ext[0,2],ext[1,2])]:
        f(lo,hi)
    ax3.set_box_aspect((1.8,.35,1.0),zoom=0.87)
    ax3.view_init(elev=24,azim=-64)
    ax3.set_axis_off()
    ax3.set_title('Actual triangulated solid')
    fig.suptitle(spec['name'].replace('_',' ').title()+' · topology-inspired study',fontweight='bold')
    fig.tight_layout()
    fig.savefig(filepath,dpi=140,bbox_inches='tight')
    plt.close(fig)

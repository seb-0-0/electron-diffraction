from utils import*
from postprocess import*
from utils import displayStandards as dsp
from crystals import Crystal
import multislice as mupy
import postprocess as pp
import sys,numpy,os
import rotating_crystal as rcc
import importlib as imp
imp.reload(mupy)
imp.reload(rcc)

plt.close('all')
path = 'dat/biotin/'
file = path+'biotin.cif'

# rcc.show_cell(file,x0=-1)

def create_xyz(opts='gp'):
    nz = np.array([1,2,1,1,1,1,1,1 ,1,1 ])#,1)
    nx = np.array([0,1,1,2,3,4,6,8 ,12,24])#,1,7,12,24])
    angles = np.arctan(nx/(4*nz))*180/np.pi
    if opts:
        # rcc.import_cif(file,path+'biotin001.xyz')
        Nx,Nz=[(1,1),(30,5)]['g' in opts]
        rcc.rotate_xyz(file,nx,nz,Nx=Nx,Nz=Nz,opt=opts)
    data = ['biotin%d0%d.xyz' %(n,m) for n,m in zip(nx,nz)]
    for dat,a in zip(data,angles) : rcc.show_grid(path+dat,title=dat+' %.1f' %a)
    print('angles:',angles)
    return data,angles


def run_simus(thick=5000,nts=91,ssh=''):
    cols  = ['host','state','dat','angle','tilt']
    df    = pd.DataFrame(columns=cols+pp.info_cols)
    tilts = np.linspace(0,90,nts)
    Nx = np.array(np.round(lats[:,0].max()/lats[:,0]),dtype=int)
    Ny = np.array(np.round(Nx*lats[:,0]/lats[:,1]),dtype=int)
    Nz = np.array(np.round(thick/lats[:,2]),dtype=int)
    for i in range(nts):
        pad   = int(np.log10(nts))+1
        istr  = ('%d' %i).zfill(pad)
        iD    = np.abs(tilts[i]-angles).argmin()
        tx    = tilts[i]-angles[iD]
        multi = mupy.Multislice(path,data=data[iD],tail=istr,
            mulslice=False,keV=200,tilt=[tx*np.pi/180/1000,0],
            NxNy=512,slice_thick=1.0,Nhk=5,repeat=[Nx[iD],Ny[iD],Nz[iD]],
            #TDS=True,T=300,n_TDS=15,
            opt='sr',fopt='',v='nctr',#nctrdDR',
            ssh=ssh,
            )
        df.loc[multi.outf['obj']] = [np.nan]*len(df.columns)
        df.loc[multi.outf['obj']][cols] = [ssh,'start',data[iD],tilts[i],tx]
        df.to_pickle(path+'df.pkl')
        print(green+'Dataframe saved : '+yellow+path+'df.pkl'+black)

        # multi.wait_simu(ssh_alias='tarik-CCP4home')
        # multi.print_log()
        # multi.postprocess(ppopt='uwP',ssh_alias='tarik-CCP4home')

def update_patterns():
    df = pp.update_df_info(path+'df.pkl')
    for dat in df.index:
        multi=pp.load_multi_obj(path+dat)
        # multi.ssh_get(ssh_alias,'pattern')
        multi.save_pattern()

def get_figs():
    df = pd.read_pickle(path+'df.pkl')
    cs = dsp.getCs('Blues',3)#,dsp.getCs('Reds'),dsp.getCs('Greens')
    plts = [[],[],[]]
    pad = int(np.log10(df.index.size))+1
    for i,dat in enumerate(df.index):
        multi=pp.load_multi_obj(path+dat)
        multi.pattern(tol=1e-6,Iopt='Ins',caxis=[0,1],Nmax=100,
            cmap='binary',imOpt='hc',pOpt='t',rings=[0.1,0.2],#,1],
            opt='ps',name=path+'figures/%s_pattern.png' %dat.replace('.pkl',''))
        # multi.beam_vs_thickness()
    #     for j in range(len(hk)):plts[j]+=[[t,I[j,:],cs[i],'']]
    # for j in range(3):
    #     dsp.stddisp(plts[j],title='hk=%s' %hk[j],
    #         imOpt='ch',cmap='Blues',caxis=[0,90],pOpt='tG')


data,angles = create_xyz(opts='')
lats = np.array([rcc.show_grid(path+dat,opt='')[0] for dat in data])
# multi = run_simus(thick=100,nts=3,ssh='')#'tarik-CCP4home')
# update_patterns()
# get_figs()
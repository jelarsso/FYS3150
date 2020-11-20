import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import subprocess as sb
from IPython import embed

def read_datafile(filename):
    with open(filename,"r") as infile:
        l = infile.readline().split(" ")
        n_spins = int(l[1]) 
        n_mc = int(l[3])
    return n_spins,n_mc,np.loadtxt(filename)



def p4a_analytical():
    filename = "p4c.data"
    nspins = 2
    n_mc = 100000
    start_temp = 1.0
    stop_temp = 2.6
    step_temp = 0.05

    beta = 1/np.arange(start_temp,stop_temp+step_temp,step_temp)
    Z = (12 + 4*np.cosh(8*beta))
    mean_E = -32*np.sinh(8*beta)/Z
    mean_E2 = 4*64*np.cosh(8*beta)/Z
    mean_M = (16+8*np.exp(8*beta))/Z
    mean_M2 = 32*(1+np.exp(8*beta))/Z

    fig = make_subplots(rows=2, cols=2, subplot_titles=("Average Energy","Mean Magnetization", "Specific heat", "Susceptibility"),vertical_spacing=0.2,horizontal_spacing=0.10)
    
    fig.add_trace(go.Scatter(name="Analytical",x=1/beta,y=mean_E/nspins/nspins,line=dict(color="Crimson")),row=1,col=1)
    fig.add_trace(go.Scatter(x=1/beta,y=mean_M/nspins/nspins,showlegend=False,line=dict(color="Crimson")),row=1,col=2)
    fig.add_trace(go.Scatter(x=1/beta,y=beta*beta*(mean_E2-mean_E**2)/nspins/nspins,showlegend=False,line=dict(color="Crimson")),row=2,col=1)
    fig.add_trace(go.Scatter(x=1/beta,y=beta*(mean_M2-mean_M**2)/nspins/nspins,showlegend=False,line=dict(color="Crimson")),row=2,col=2)

    sb.run(["./spins2", filename, str(n_mc), str(start_temp),str(stop_temp),str(step_temp)])
    ns,nmc,data = read_datafile(filename)

    fig.add_trace(go.Scatter(name="Simulated",x=data[:,0],y=data[:,1],mode="markers",marker=dict(color="MediumPurple")),row=1,col=1)
    fig.add_trace(go.Scatter(x=data[:,0],y=data[:,5],mode="markers",showlegend=False,marker=dict(color="MediumPurple")),row=1,col=2)
    fig.add_trace(go.Scatter(x=data[:,0],y=data[:,2],mode="markers",showlegend=False,marker=dict(color="MediumPurple")),row=2,col=1)
    fig.add_trace(go.Scatter(x=data[:,0],y=data[:,4],mode="markers",showlegend=False,marker=dict(color="MediumPurple")),row=2,col=2)

    fig.update_xaxes(title="Temperature")
    fig.update_yaxes(title="Energy/spin",row=1,col=1)
    fig.update_yaxes(title="Magnetization/spin",row=1,col=2)
    fig.update_yaxes(title="Specific Heat",row=2,col=1)
    fig.update_yaxes(title="Susceptibility",row=2,col=2)
    fig.update_yaxes(title_standoff=1)
    fig.update_layout(font_family="lmodern",font_size=12)
    fig.write_image("exval4c.pdf",width=600*1.41,height=600,scale=2)
    #fig.show()

def p4c_comapre_nmc():
    filename = "p4c.data"
    n_mc = np.logspace(1,7,50)
    temp = 1
    d = []


    nspins = 2

    beta = 1
    Z = (12 + 4*np.cosh(8*beta))
    mean_E = -32*np.sinh(8*beta)/Z
    mean_E2 = 4*64*np.cosh(8*beta)/Z
    mean_M = (16+8*np.exp(8*beta))/Z
    mean_M2 = 32*(1+np.exp(8*beta))/Z

    fig = make_subplots(rows=2, cols=2, subplot_titles=("Average Energy","Mean Magnetization", "Specific heat", "Susceptibility"))
    fig.add_trace(go.Scatter(mode="lines",name="Analytical",x=[np.log10(n_mc[0]),np.log10(n_mc[-1])], y=[mean_E/nspins/nspins,mean_E/nspins/nspins],line=dict(color="Crimson")),row=1,col=1)
    fig.add_trace(go.Scatter(mode="lines",showlegend=False,x=[np.log10(n_mc[0]),np.log10(n_mc[-1])], y=[mean_M/nspins/nspins,mean_M/nspins/nspins],line=dict(color="Crimson")),row=1,col=2)
    fig.add_trace(go.Scatter(mode="lines",showlegend=False,x=[np.log10(n_mc[0]),np.log10(n_mc[-1])], y=[beta*beta*(mean_E2-mean_E**2)/nspins/nspins,beta*beta/nspins/nspins*(mean_E2-mean_E**2)],line=dict(color="Crimson")),row=2,col=1)
    fig.add_trace(go.Scatter(mode="lines",showlegend=False,x=[np.log10(n_mc[0]),np.log10(n_mc[-1])], y=[beta/nspins/nspins*(mean_M2-mean_M**2), beta/nspins/nspins*(mean_M2-mean_M**2)],line=dict(color="Crimson")),row=2,col=2)
    
    for n in n_mc:
        sb.run(["./spins2", filename, str(n), str(temp),str(temp),str(1)])
        ns,nmc,data = read_datafile(filename)
        d.append(data[:])
    d = np.asarray(d)
    fig.add_trace(go.Scatter(name="Simulated",x=np.log10(n_mc),y=d[:,1],mode="lines+markers",marker=dict(color="MediumPurple")),row=1,col=1)
    fig.add_trace(go.Scatter(x=np.log10(n_mc),y=d[:,5],mode="lines+markers",showlegend=False,marker=dict(color="MediumPurple")),row=1,col=2)
    fig.add_trace(go.Scatter(x=np.log10(n_mc),y=d[:,2],mode="lines+markers",showlegend=False,marker=dict(color="MediumPurple")),row=2,col=1)
    fig.add_trace(go.Scatter(x=np.log10(n_mc),y=d[:,4],mode="lines+markers",showlegend=False,marker=dict(color="MediumPurple")),row=2,col=2)

    fig.update_xaxes(title="log(Number of Monte Carlo cycles)")
    fig.update_yaxes(title="Energy/spin",row=1,col=1)
    fig.update_yaxes(title="Magnetization/spin",row=1,col=2)
    fig.update_yaxes(title="Specific Heat",row=2,col=1)
    fig.update_yaxes(title="Susceptibility",row=2,col=2)
    fig.update_yaxes(title_standoff=1)
    fig.update_layout(font_family="lmodern",font_size=12)
    fig.write_image("nmc4c.pdf",width=600*1.41,height=600,scale=2)
    #fig.show()

def p4e_pde():

    with open("pde.data","r") as infile:
        infile.readline()
        infile.readline()
        infile.readline()
        pde_1 = np.asarray([float(x) for x in infile.readline().split()])
        infile.readline()
        infile.readline()
        pde_24 = np.asarray([float(x) for x in infile.readline().split()])
    
    fig = go.Figure(data=[go.Histogram(x=pde_24[5000:], histnorm='probability density')])
    fig.show()


def p4f_many_spin():
    filename = "p4c.data"
    n_mc = 20000
    L = 100
    start_temp = 2.0
    stop_temp = 2.6
    step_temp = 0.05

    
    fig = make_subplots(rows=2, cols=2, subplot_titles=("Average Energy","Mean Magnetization", "Specific heat", "Susceptibility"))
    
    
    sb.run(["./spins", filename, str(n_mc),str(L), str(start_temp),str(stop_temp),str(step_temp)])
    ns,nmc,data = read_datafile(filename)

    fig.add_trace(go.Scatter(x=data[:,0],y=data[:,1]),row=1,col=1)
    fig.add_trace(go.Scatter(x=data[:,0],y=data[:,5]),row=1,col=2)
    fig.add_trace(go.Scatter(x=data[:,0],y=data[:,2]),row=2,col=1)
    fig.add_trace(go.Scatter(x=data[:,0],y=data[:,4]),row=2,col=2)

    fig.show()     


if __name__ == "__main__":
    #p4a_analytical()
    #p4c_comapre_nmc()
    p4e_pde()
    #p4f_many_spin()
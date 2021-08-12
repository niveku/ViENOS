import numpy as np
import pandas as pd

def degToCompass(num, mode=0, divisiones=16):
    
    if mode == 0:
        direc=list(np.linspace(0,360-360/divisiones,divisiones))
        direc=[round(e,2)for e in direc]
    else:
        direc=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
        
    if not np.isnan(num): 
        val=int((num/22.5)+.5)  
        return direc[(val % divisiones)]
    else:
        print(num)
        return(direc[0])
    
def rose_df(df, mode=0):
    
    direc=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]

    df2=df[df.Wdir.notnull()].copy()
    bins = [0, 1, 2, 3, 4, np.inf]
    names = ['<1', '1-2', '2-3', '3-4', '4+']
    
    df2['direction'] = df2.Wdir.apply(degToCompass,mode=mode)
    df2.sort_values(['direction','Wvel'],ascending=False,inplace=True)
    df2['speed'] = pd.cut(df2['Wvel'], bins, labels=names)
    df2['frequency'] = 1
    df2 = df2.groupby(['direction','speed']).agg({'frequency':'count'}).reset_index()
    df2.frequency = round(df2.frequency*100/df2.frequency.sum(),2)
    #df2.direction = pd.Categorical(df2.direction, categories=direc, ordered=True)
    #df2.sort_values(['direction','speed'],ascending=False,inplace=True)
    return df2
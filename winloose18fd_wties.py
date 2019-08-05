# 2018 version calculates two pageranks: one for wins and one for losses
# then substract the second from first

# reverted to original pagerank method

# uses football-data API instead of openliga-db

import csv
import numpy as np
import os

import http.client
import json


#import django

#sys.path.append('~/Dropbox/Program/Ranking/')

#os.environ["DJANGO_SETTINGS_MODULE"] = "ranko.settings"

#django.setup()

#import matplotlib.pyplot as plt
#import matplotlib.mlab as mlab
import math

#from ranko.models import Ranking, LeagueRanking


from scipy.sparse import csc_matrix

def pageRank(G, s = 1.0, maxerr = .001):
    """
    Computes the pagerank for each of the n states.

    Here original version taking into account sinks 
    


    Args
    ----------
    G: matrix representing state transitions
       Gij can be a boolean or non negative real number representing the
       transition weight from state i to j.
    Kwargs
    ----------
    s: probability of following a teleportation 
       to another state. Defaults to 1.0.
       The influence of teleportation decreases if the number 
       of real links increases. Perhaps this should be adjusted.

    maxerr: if the sum of pageranks between iterations is below this we will
            have converged. Defaults to 0.001
    """
    n = G.shape[0]

    
    M = csc_matrix(G,dtype=np.float)   # save as sparse matrix (only nonzero elements)
    rsums = np.array(M.sum(1))[:,0]         # sums the rows, zero if no loss occurs for the node
    ci, ri = M.transpose().nonzero()   # transposed in order to change order of indices, then colums are rows
    M.data /= rsums[ri]

    # Compute pagerank r until we converge
    ro, r = np.zeros(n), np.ones(n)

    for i in range(0,n): 
        r[i]=1.0/n

    Ti = np.ones(n) / float(n)

    sink = rsums==0

    while np.sum(np.abs(r-ro)) > maxerr:
        ro = r.copy()
        # calculate each pagerank at a time
        for i in range(0,n):
            # inlinks of state i
            Ii = np.array(M[:,i].todense())[:,0]    # fetch i-th column of M
            # outlinks of state i
#            Oi = np.array(M[i,:].todense())[:,0]    # fetch i-th column of M
            # account for sink states  (Is this in original pagerank method?)
            Si = sink / float(n)            # account for teleportation to state i

            r[i] = ro.dot( Ii*s + Si*s + Ti*(1-s) )  # multiply vector ro with sum (from left?)
#            r[i] = ro.dot( Ii + Ti*s ) /(rsums[i]+s) # multiply vector ro with sum (from left?)
 
    # return normalized pagerank
    return r/sum(r)


#if __name__=='__main__':



G = np.zeros((98,98))
ng = [0] * 98     # number of games played
teamnr = [0] *98
teams = [-1]*10000
tname = []
counter=0


connection = http.client.HTTPConnection('api.football-data.org')
headers = { 'X-Auth-Token': 'bcfade959cf64306942ba5365de89c3a' }

connection.request('GET', '/v2/competitions/PL/teams?season=2018', None, headers )
response = json.loads(connection.getresponse().read().decode())
for team in response['teams']:
    print (counter,team['id'],team['shortName'])
    teams[team['id']]=counter
    teamnr[counter]=team['id']
    tname.append(team['shortName'])
    counter+=1
connection.request('GET', '/v2/competitions/BL1/teams?season=2018', None, headers )
response = json.loads(connection.getresponse().read().decode())
for team in response['teams']:
    print (counter,team['id'],team['shortName'])
    teams[team['id']]=counter
    teamnr[counter]=team['id']
    tname.append(team['shortName'])
    counter+=1
connection.request('GET', '/v2/competitions/SA/teams?season=2018', None, headers )
response = json.loads(connection.getresponse().read().decode())
for team in response['teams']:
    print (counter,team['id'],team['shortName'])
    teams[team['id']]=counter
    teamnr[counter]=team['id']
    tname.append(team['shortName'])
    counter+=1
connection.request('GET', '/v2/competitions/PD/teams?season=2018', None, headers )
response = json.loads(connection.getresponse().read().decode())
for team in response['teams']:
    print (counter,team['id'],team['shortName'])
    teams[team['id']]=counter
    teamnr[counter]=team['id']
    tname.append(team['shortName'])
    counter+=1
connection.request('GET', '/v2/competitions/FL1/teams?season=2018', None, headers )
response = json.loads(connection.getresponse().read().decode())
for team in response['teams']:
    print (counter,team['id'],team['shortName'])
    teams[team['id']]=counter
    teamnr[counter]=team['id']
    tname.append(team['shortName'])
    counter+=1


connection.request('GET', '/v2/competitions/PL/matches?season=2018', None, headers )
response = json.loads(connection.getresponse().read().decode())
for match in response['matches']:
    if match['status'] == 'FINISHED':
        grow=teams[match['homeTeam']['id']]
        gcolumn=teams[match['awayTeam']['id']]
        if grow>=0 and gcolumn>=0:
            G[grow,gcolumn] += (match['score']['fullTime']['awayTeam']>match['score']['fullTime']['homeTeam'])
            G[grow,gcolumn] += 0.5*(match['score']['fullTime']['awayTeam']==match['score']['fullTime']['homeTeam'])
            G[gcolumn,grow] += (match['score']['fullTime']['homeTeam']>match['score']['fullTime']['awayTeam'])
            G[gcolumn,grow] += 0.5*(match['score']['fullTime']['homeTeam']==match['score']['fullTime']['awayTeam'])
            ng[grow] += 1
            ng[gcolumn] += 1
connection.request('GET', '/v2/competitions/BL1/matches?season=2018', None, headers )
response = json.loads(connection.getresponse().read().decode())
for match in response['matches']:
    if match['status'] == 'FINISHED':
        grow=teams[match['homeTeam']['id']]
        gcolumn=teams[match['awayTeam']['id']]
        if grow>=0 and gcolumn>=0:
            G[grow,gcolumn] += (match['score']['fullTime']['awayTeam']>match['score']['fullTime']['homeTeam'])
            G[grow,gcolumn] += 0.5*(match['score']['fullTime']['awayTeam']==match['score']['fullTime']['homeTeam'])
            G[gcolumn,grow] += (match['score']['fullTime']['homeTeam']>match['score']['fullTime']['awayTeam'])
            G[gcolumn,grow] += 0.5*(match['score']['fullTime']['homeTeam']==match['score']['fullTime']['awayTeam'])
            ng[grow] += 1
            ng[gcolumn] += 1
connection.request('GET', '/v2/competitions/SA/matches?season=2018', None, headers )
response = json.loads(connection.getresponse().read().decode())
for match in response['matches']:
    if match['status'] == 'FINISHED':
        grow=teams[match['homeTeam']['id']]
        gcolumn=teams[match['awayTeam']['id']]
        if grow>=0 and gcolumn>=0:
            G[grow,gcolumn] += (match['score']['fullTime']['awayTeam']>match['score']['fullTime']['homeTeam'])
            G[grow,gcolumn] += 0.5*(match['score']['fullTime']['awayTeam']==match['score']['fullTime']['homeTeam'])
            G[gcolumn,grow] += (match['score']['fullTime']['homeTeam']>match['score']['fullTime']['awayTeam'])
            G[gcolumn,grow] += 0.5*(match['score']['fullTime']['homeTeam']==match['score']['fullTime']['awayTeam'])
            ng[grow] += 1
            ng[gcolumn] += 1
connection.request('GET', '/v2/competitions/PD/matches?season=2018', None, headers )
response = json.loads(connection.getresponse().read().decode())
for match in response['matches']:
    if match['status'] == 'FINISHED':
        grow=teams[match['homeTeam']['id']]
        gcolumn=teams[match['awayTeam']['id']]
        if grow>=0 and gcolumn>=0:
            G[grow,gcolumn] += (match['score']['fullTime']['awayTeam']>match['score']['fullTime']['homeTeam'])
            G[gcolumn,grow] += (match['score']['fullTime']['homeTeam']>match['score']['fullTime']['awayTeam'])
            G[grow,gcolumn] += 0.5*(match['score']['fullTime']['awayTeam']==match['score']['fullTime']['homeTeam'])
            G[gcolumn,grow] += 0.5*(match['score']['fullTime']['homeTeam']==match['score']['fullTime']['awayTeam'])
            ng[grow] += 1
            ng[gcolumn] += 1
connection.request('GET', '/v2/competitions/FL1/matches?season=2018', None, headers )
response = json.loads(connection.getresponse().read().decode())
for match in response['matches']:
    if match['status'] == 'FINISHED':
        grow=teams[match['homeTeam']['id']]
        gcolumn=teams[match['awayTeam']['id']]
        if grow>=0 and gcolumn>=0:
            G[grow,gcolumn] += (match['score']['fullTime']['awayTeam']>match['score']['fullTime']['homeTeam'])
            G[gcolumn,grow] += (match['score']['fullTime']['homeTeam']>match['score']['fullTime']['awayTeam'])
            G[grow,gcolumn] += 0.5*(match['score']['fullTime']['awayTeam']==match['score']['fullTime']['homeTeam'])
            G[gcolumn,grow] += 0.5*(match['score']['fullTime']['homeTeam']==match['score']['fullTime']['awayTeam'])
            ng[grow] += 1
            ng[gcolumn] += 1
connection.request('GET', '/v2/competitions/CL/matches?season=2018', None, headers )
response = json.loads(connection.getresponse().read().decode())
for match in response['matches']:
    if match['status'] == 'FINISHED':
        grow=teams[match['homeTeam']['id']]
        gcolumn=teams[match['awayTeam']['id']]
        if grow>=0 and gcolumn>=0:
            G[grow,gcolumn] += (match['score']['fullTime']['awayTeam']>match['score']['fullTime']['homeTeam'])
            G[gcolumn,grow] += (match['score']['fullTime']['homeTeam']>match['score']['fullTime']['awayTeam'])
            G[grow,gcolumn] += 0.5*(match['score']['fullTime']['awayTeam']==match['score']['fullTime']['homeTeam'])
            G[gcolumn,grow] += 0.5*(match['score']['fullTime']['homeTeam']==match['score']['fullTime']['awayTeam'])
            ng[grow] += 1
            ng[gcolumn] += 1



# add data from europa league
with open('el2018.csv') as csvfile:
        footballreader = csv.reader(csvfile, delimiter=',',quotechar='|')
        next(footballreader)    
        for row in footballreader:
            grow=int(row[1])
            gcolumn=int(row[2])
            G[grow,gcolumn] += (row[4]>row[3])
            G[gcolumn,grow] += (row[3]>row[4])
            G[grow,gcolumn] += 0.5*(row[4]==row[3])
            G[gcolumn,grow] += 0.5*(row[3]==row[4])
            ng[grow] += 1
            ng[gcolumn] += 1

#print(G[20])
#print (G[96,:])
#print (G[85,:])

#print([int(rowg[96]) for rowg in G])
#print([int(rowg[85]) for rowg in G])

rankslistG = pageRank(G,s=0.85)
rankslistV = pageRank(np.transpose(G),s=0.85)

rankslist = rankslistG - rankslistV
sortlist=sorted(range(len(rankslist)), key=lambda k: rankslist[k])


#r=Ranking.objects.all()
variab = np.zeros(98)
diffr=0
for i in range(0,98):
    nout=0
    diffout=0.0
    for l in range(0,98):
        diffr=rankslist[i]-rankslist[l]
        if G[i,l]> 0 and diffr>0:
            nout = nout+1
            diffout = diffout +diffr*diffr
            if i==23:
                print (diffr)
        if G[l,i]> 0 and diffr<0:
            nout = nout+1
            diffout = diffout +diffr*diffr
            if i==23:
                print (diffr)

    if nout > 1:
        variab[i]=np.sqrt(diffout/(nout-1))



j=98
for i in sortlist:
    print(j,tname[i],teamnr[i],ng[i],i,rankslist[i],"sigma=", variab[i]/np.sqrt(2),"W:",rankslistG[i],"L:",rankslistV[i])
#    r=Ranking.objects.get(team_name=tname[i])
#    r.rank=j
#    r.points=round(100*rankslist[i],2)
#    r=Ranking(team_name=tname[i],rank=j)     # use to initialize table
#    r.save()
    j=j-1

#aver = [0.0] * 5
#i=0

#liga_short =  ["BL","PL","PD","L1","SA"]
#for liga in liga_short:
#    aver[i] = 0.0    
##    rliga=LeagueRanking.objects.get(name=liga)
#    rl=Ranking.objects.filter(league=liga)
#    for r in rl:
#        aver[i] += r.points
#    print (aver[i])
#    aver[i]=round(aver[i],2)
#    i = i+1

#sortlist_liga=sorted(range(len(aver)), key=lambda k: aver[k])

#r=Ranking.objects.all()

#liga_names = ["Bundesliga", "Premier League", "Primera Division", "Ligue 1", "Serie A"  ] 
#j=5
#for i in sortlist_liga:
#    print(j,liga_short[i],aver[i])
#    r=LeagueRanking.objects.get(short=liga_short[i])
#    r.rank=j
#    r.points=aver[i]
##    r=LeagueRanking(name=liga_names[i],short=liga_short[i], rank=j, points=aver[i])     # use to initialize table
#    r.save()
#    j=j-1


exit()

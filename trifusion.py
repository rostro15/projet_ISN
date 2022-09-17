#coding: utf-8-

def fusion(liste1,liste2):
    liste=[]
    k,l=len(liste1),len(liste2)
    i,j=0,0
    while i<k and j<l:
        if liste1[i][1]>=liste2[j][1]:
            liste.append(liste1[i])
            i=i+1
        else:
            liste.append(liste2[j])
            j=j+1
    if i==k and j<l:
        liste=liste+liste2[j:]
    elif i<k and j==l:
        liste=liste+liste1[i:]
    return liste

def tri_fusion(liste):
    if len(liste)==1:
        return liste
    else:
        m=len(liste)//2
        liste1=liste[:m]
        liste2=liste[m:]
        liste_div1=tri_fusion(liste1)
        liste_div2=tri_fusion(liste2)
        return fusion(liste_div1,liste_div2)





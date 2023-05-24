import pandas as pd

class Invert:
    def __init__(self,data):
        self.data=data
    
    def invert(self):
        #cumpliendo el minimo de las validaciones
        investingData = pd.DataFrame(columns=['NameClass','Name','Protocol','Chain','TVL_$','APY_%','Inverted','PorcentInvested'])


        totalDataClass=totalDataClass.sort_values(by=['APY_%'],  ascending=False)

        #the minimum of class A is reversed
        varInvesting=investing
        varInvestingClassA=investing*classInvesting[0]['porcentMin']
        for index,row in totalDataClass.iterrows():
            if varInvesting>0 and row['NameClass']=='Class A':
                if varInvestingClassA>0: #it is verified that it is left for investment                   
                    if  row['TVL_$']<=varInvestingClassA: #if it does not reach the investment limit
                        row['Inverted'] = row['TVL_$']
                        row['PorcentInvested'] = row['Inverted']/investing
                        investingData=investingData.append(row)  
                        varInvestingClassA = varInvestingClassA-row['Inverted']
                    else: #if you reach or want to go over the investment limit
                        row['Inverted'] = varInvestingClassA
                        row['PorcentInvested'] = row['Inverted']/investing
                        investingData=investingData.append(row)  
                        varInvestingClassA = 0 
                else:
                    row['Inverted'] = 0
                    row['PorcentInvested'] = 0
                    investingData=investingData.append(row)  
            else:
                row['Inverted'] = 0
                row['PorcentInvested'] = 0
                investingData=investingData.append(row)  

        def validate_investment(investingData,classInvesting):
            validate={}
            a =investingData[investingData['NameClass']=='Class A']['PorcentInvested'].sum()
            b =investingData[investingData['NameClass']=='Class B']['PorcentInvested'].sum()
            c =investingData[investingData['NameClass']=='Class C']['PorcentInvested'].sum()
            #print('Total Porcent:'+str(investingData['PorcentInvested'].sum()))
            #print('Total inverted:'+str(investingData['Inverted'].sum()))
            if (classInvesting[0]['porcentMin']<=a and a <= 1-b-c):
                bypercentageMaximumLimit=1-b-c-a
                validate[classInvesting[0]['name']]=bypercentageMaximumLimit
            if  (classInvesting[1]['porcentMax']>=b and b <= 1-a-c):
                bypercentageMaximumLimit=classInvesting[1]['porcentMax']-b
                validate[classInvesting[1]['name']]=bypercentageMaximumLimit
            if  (classInvesting[2]['porcentMax']>=c and c <= 1-a-b):
                bypercentageMaximumLimit=classInvesting[2]['porcentMax']-c
                validate[classInvesting[2]['name']]=bypercentageMaximumLimit
            return validate
        investingData=investingData.sort_values(by=['APY_%'],  ascending=False)

        varInvesting=investing-investing*classInvesting[0]['porcentMin']
        #print(varInvesting)

        for index,row in investingData.iterrows():

            listValid=validate_investment(investingData,classInvesting)
            
            if varInvesting>0 and row['TVL_$']>=row['Inverted'] and row['NameClass'] in listValid :
                
                posibleInversion=row['TVL_$']-row['Inverted']
                if posibleInversion<=listValid[row['NameClass']]*investing:
                    pass
                else:
                    posibleInversion=listValid[row['NameClass']]*investing
                if  (posibleInversion)<=varInvesting : #if it does not reach the investment limit
                    
                    investingData.loc[index,'Inverted']=row['Inverted']+ posibleInversion
                    investingData.loc[index,'PorcentInvested'] = investingData.loc[index,'Inverted']/investing

                    varInvesting = varInvesting-(row['TVL_$']-row['Inverted'])
                else: #if you reach or want to go over the investment limit
                    investingData.loc[index,'Inverted']=row['Inverted']+ varInvesting
                    investingData.loc[index,'PorcentInvested']=investingData.loc[index,'Inverted']/investing

                    varInvesting = 0

        print(investingData.loc[:,['NameClass','Name','Protocol','Chain','TVL_$','APY_%','Inverted','PorcentInvested']].sort_values(by=['Inverted'],  ascending=False).iloc[0:5,:])

        print('Total Porcent Class A:'+str(investingData[investingData['NameClass']=='Class A']['PorcentInvested'].sum()))
        print('Total Porcent Class B:'+str(investingData[investingData['NameClass']=='Class B']['PorcentInvested'].sum()))
        print('Total Porcent Class C:'+str(investingData[investingData['NameClass']=='Class C']['PorcentInvested'].sum()))
        print('Total Porcent:'+str(investingData['PorcentInvested'].sum()))
        print('Total inverted:'+str(investingData['Inverted'].sum()))
        if investingData[investingData['NameClass']=='Class A']['PorcentInvested'].sum()<classInvesting[0]['porcentMin']:
            print('No se cumple minimo de invercion Clase A')
        else:
            print('Se cumple minimo de invercion Clase A')



'''totalDataClass=totalDataClass.sort_values(by=['APY_%'],  ascending=False)
    #cumpliendo el minimo de las validaciones
    investingData = pd.DataFrame(columns=['NameClass','Name','Protocol','Chain','TVL_$','APY_%','Inverted','PorcentInvested'])
    #validacion del minimo de la clase a
    porcentMin=classInvesting[0]['porcentMin']
    print('Class A invirtiendo lo minimo')
    varInvesting=investing
    totalDataClassA=totalDataClass[totalDataClass['NameClass']=='Class A']
    for index,row in totalDataClassA.iterrows():
        if varInvesting>=0: #se comprueba que quede para invertir           
            
            if row['TVL_$']/varInvesting<=1: #si no llega al limite de invercion
                porcentInvesting=row['TVL_$']/investing
                porcentMin=porcentMin-porcentInvesting

                row['Inverted'] = row['TVL_$']
                row['PorcentInvested'] = porcentInvesting
                investingData=investingData.append(row)  
                totalDataClass=totalDataClass.remove(row)
                varInvesting = varInvesting-row['TVL_$']   
            else: #si llega o quiere pasar el limite de la invercion
                porcentInvesting=porcentMin
                porcentMin=porcentMin-porcentInvesting
                
                row['Inverted'] = varInvesting
                row['PorcentInvested'] = porcentInvesting
                investingData=investingData.append(row)
                varInvesting = 0     
        else:
            if porcentMin>0:
                print('No se cumple minimo de invercion Clase A')
            elif porcentMin==0:
                print('Se cumple minimo de invercion Clase A')'''

        
        

    '''def investing_function(totalInvesting,dataClass):
        way = pd.DataFrame(columns=['Name','Protocol','Chain','TVL_$','Base_APY_$','Reward_APY_%','Rewards','APY_%','7d_ago_%'])
        if totalInvesting==0 or len(dataClass)==0:
            return way
        elif dataClass.iloc[0]['TVL_$']>=totalInvesting:            
            d=dataClass.iloc[0]
            d['inverted'] = totalInvesting
            way=way.append(d)
            totalInvesting=0
        elif dataClass.iloc[0]['TVL_$']<totalInvesting:            
            d=dataClass.iloc[0]
            d['inverted'] = dataClass.iloc[0]['TVL_$']
            way=way.append(d)            
            totalInvesting=totalInvesting-dataClass.iloc[0]['TVL_$']
            dataClass= dataClass.iloc[1:]
        #print(totalInvesting)
        #print(way)
        return way.append(investing_function(totalInvesting,dataClass))
'''
    
    '''tabs_ = list(st.tabs(list(map(lambda x: x['name'],classInvesting))))
    dataCobined=None
    for i, tab_ in enumerate(tabs_):    
        with tab_:  
            cI=classInvesting[i]
            totalInvesting=int(investing*cI['porcent'])
            name=cI['name']
            st.subheader(f'Total Investing in {name}: ${totalInvesting}')
            dataClass=data[(data['TVL_$']<cI['less_than']) & (data['TVL_$']>=cI['greater_than'])].sort_values(by=['APY_%'],  ascending=False)
            dataClass['inverted'] = pd.Series() 
            dataClassInvest=investing_function(totalInvesting,dataClass)
            if dataCobined is None:
                dataCobined=dataClassInvest
            else:
                dataCobined=dataCobined.append(dataClassInvest)
            grid=view_data(dataClassInvest,300)
            download_csv_investment_buttons(grid,cI['name'].replace(' ','_'))'''
from cgitb import enable
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import pandas as pd
import time
from ExtractorCoindixStablecoins import ExtractorCoindixStablecoins
st.set_page_config(layout="wide",
                page_title="Technical Business Case Problem  Solution Challenge",
                menu_items={'Get help': 'https://www.linkedin.com/in/lucas-agustin-gonzalez-9807a9170/'})
def title(fileName):


    st.title('Technical Business Case Problem  Solution Challenge')

    st.header("Risk Analysis on Stable Coins in DeFi")

    st.subheader(fileName.replace('_',' ').split('.')[0].upper())
    
@st.experimental_memo
def load_data(filePath):    
    return pd.read_csv(filePath)
@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')

def view_data(data,height=600):
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gridOptions = gb.build()

    grid_response = AgGrid(
        data,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT', 
        update_mode='MODEL_CHANGED', 
        fit_columns_on_grid_load=True,
        theme='blue',
        enable_enterprise_modules=True,
        height=height, 
        width='80%',
        reload_data=True
    )
    return grid_response
def download_csv_buttons(grid_response,nameClass):
    data = grid_response['data']
    csv = convert_df(data)
    st.download_button(
    "Download Full CSV",
    csv,
    nameClass+'_'+fileName,
    "text/csv",
    key=nameClass+'_download-full-csv')
def download_csv_investment_buttons(grid_response,nameClass):
    data = grid_response['data']
    csv = convert_df(data)
    st.download_button(
    "Download investment CSV",
    csv,
    nameClass+'_investment_'+fileName,
    "text/csv",
    key=nameClass+'_investment_'+'download-investment-csv')


def update_data_button(filePath):
        state=st.button("Update Data")
        if state:            
            extractor = ExtractorCoindixStablecoins(csvOutput=filePath)
            extractor.extract()
            #return extractor.getDataFrame()
            st.balloons()
        return state
filePath='data_Coindix_StableCoins.csv'
fileName=filePath.split('/')[-1]
classInvesting= [{'name':'Class A','greater_than':50000000,'less_than':99999999999999999999999999999, 'porcentMin':0.35,'porcentMax':1},
                {'name':'Class B','greater_than':10000000,'less_than':50000000, 'porcentMin':0,'porcentMax':0.35},
                {'name':'Class C','greater_than':0,'less_than':10000000, 'porcentMin':0,'porcentMax':0.30}]
with st.container():
    title(fileName)
    updateData=update_data_button(filePath)  

    totalDataClass=None
    tabs_ = list(st.tabs(list(map(lambda x: x['name'],classInvesting))))
    for i, tab_ in enumerate(tabs_):    
        with tab_:  
            data = load_data(filePath)
            data=data[(data['TVL_$']<classInvesting[i]['less_than']) & (data['TVL_$']>=classInvesting[i]['greater_than'])].sort_values(by=['APY_%'],  ascending=False)
            data['NameClass']=classInvesting[i]['name']
            grid=view_data(data, 350)
            if totalDataClass is None:
                totalDataClass=data
            else:
                totalDataClass=totalDataClass.append(data)
            download_csv_buttons(grid,classInvesting[i]['name'].replace(' ','_'))

with st.container():    
    st.subheader('investment simulation'.upper())
    investing = int(st.text_input('Money to invest', 10000000))
    #cumpliendo el minimo de las validaciones
    investingData = pd.DataFrame(columns=['NameClass','Name','Protocol - Chain','TVL_$','APY_%','Invested','PorcentInvested'])
    totalDataClass=totalDataClass.sort_values(by=['APY_%'],  ascending=False)
    #the minimum of class A is reversed
    varInvesting=investing
    varInvestingClassA=investing*classInvesting[0]['porcentMin']
    for index,row in totalDataClass.iterrows():
        if varInvesting>0 and row['NameClass']=='Class A':
            if varInvestingClassA>0: #it is verified that it is left for investment                   
                if  row['TVL_$']<=varInvestingClassA: #if it does not reach the investment limit
                    row['Invested'] = row['TVL_$']
                    row['PorcentInvested'] = row['Invested']/investing
                    investingData=investingData.append(row)  
                    varInvestingClassA = varInvestingClassA-row['Invested']
                else: #if you reach or want to go over the investment limit
                    row['Invested'] = varInvestingClassA
                    row['PorcentInvested'] = row['Invested']/investing
                    investingData=investingData.append(row)  
                    varInvestingClassA = 0 
            else:
                row['Invested'] = 0
                row['PorcentInvested'] = 0
                investingData=investingData.append(row)  
        else:
            row['Invested'] = 0
            row['PorcentInvested'] = 0
            investingData=investingData.append(row)  

    def validate_investment(investingData,classInvesting):
        #{'Class A':porcentaje,'Class B':porcentaje,'Class C':porcentaje}
        validate={}
        a =investingData[investingData['NameClass']=='Class A']['PorcentInvested'].sum()
        b =investingData[investingData['NameClass']=='Class B']['PorcentInvested'].sum()
        c =investingData[investingData['NameClass']=='Class C']['PorcentInvested'].sum()
        #print('Total Porcent:'+str(investingData['PorcentInvested'].sum()))
        #print('Total Invested:'+str(investingData['Invested'].sum()))
        if (classInvesting[0]['porcentMin']<=a and a <= 1-b-c ):
            bypercentageMaximumLimit=1-b-c-a            
            validate[classInvesting[0]['name']]=bypercentageMaximumLimit
        if  (classInvesting[1]['porcentMax']>=b and b <= 1-a-c ):
            bypercentageMaximumLimit=classInvesting[1]['porcentMax']-b
            validate[classInvesting[1]['name']]=bypercentageMaximumLimit
        if  (classInvesting[2]['porcentMax']>=c and c <= 1-a-b ):
            bypercentageMaximumLimit=classInvesting[2]['porcentMax']-c
            validate[classInvesting[2]['name']]=bypercentageMaximumLimit
        return validate

    investingData=investingData.sort_values(by=['APY_%'],  ascending=False)

    varInvesting=investing-investing*classInvesting[0]['porcentMin']
    porcentInvested=round(investingData['PorcentInvested'].sum()*100,2)
    while porcentInvested<100:
        print(investingData)
        print(porcentInvested)
        for index,row in investingData.iterrows():            
            listValid=validate_investment(investingData,classInvesting)                
            if varInvesting>0 and row['TVL_$']>=row['Invested'] and listValid[row['NameClass']]>0:
                posibleInversion=row['TVL_$']-row['Invested']
                if posibleInversion>listValid[row['NameClass']]*investing:
                    posibleInversion=listValid[row['NameClass']]*investing

                if  posibleInversion<=varInvesting : #if it does not reach the investment limit
                    
                    investingData.loc[index,'Invested']=row['Invested']+ posibleInversion
                    investingData.loc[index,'PorcentInvested'] = investingData.loc[index,'Invested']/investing
                    #print(row['NameClass'],row['TVL_$'],row['Invested'])
                    if (row['TVL_$']-row['Invested']) <=posibleInversion:
                        varInvesting = varInvesting-(row['TVL_$']-row['Invested'])
                    else:
                        varInvesting = varInvesting-posibleInversion
                else: #if you reach or want to go over the investment limit
                    investingData.loc[index,'Invested']=row['Invested']+ varInvesting
                    investingData.loc[index,'PorcentInvested']=investingData.loc[index,'Invested']/investing
                    #print(row['NameClass'],row['TVL_$'],row['Invested'])
                    varInvesting = 0
        porcentInvested=round(investingData['PorcentInvested'].sum()*100,2)

    
    print(investingData.loc[:,['NameClass','Name','Protocol - Chain','TVL_$','APY_%','Invested','PorcentInvested']].sort_values(by=['Invested'],  ascending=False).iloc[0:5,:])


    a='Total Porcent Class A: '+str(round(investingData[investingData['NameClass']=='Class A']['PorcentInvested'].sum()*100,2))
    b='Total Porcent Class B: '+str(round(investingData[investingData['NameClass']=='Class B']['PorcentInvested'].sum()*100,2))
    c='Total Porcent Class C: '+str(round(investingData[investingData['NameClass']=='Class C']['PorcentInvested'].sum()*100,2))
    totalP='Total Porcent:' +str(round(investingData['PorcentInvested'].sum()*100,2))
    totalInvested='Total Invested: '+str(round(investingData['Invested'].sum(),2))
    printList=[a,b,c,totalP,totalInvested]
    
    print('\t-\t'.join(printList))
    st.write('\t-\t'.join(printList))
    if investingData[investingData['NameClass']=='Class A']['PorcentInvested'].sum()<classInvesting[0]['porcentMin']:
        print('No se cumple minimo de invercion Clase A')
    else:
        print('Se cumple minimo de invercion Clase A')
    investingData['PorcentInvested']= investingData['PorcentInvested']*100
    grid=view_data(investingData[investingData['Invested']>0].loc[:,['NameClass','Name','Protocol - Chain','TVL_$','APY_%','Invested','PorcentInvested']],300)
    
    download_csv_investment_buttons(grid,'')
    if st.button("CALC TOTAL APY"):
        totalAPY=investingData['APY_%']*investingData['Invested']/investing
        totalAPY=totalAPY.sum()
        st.subheader(f'Weighted combined APY : {round(totalAPY,2)}%')
        
        


    


    
        


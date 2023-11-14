import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(layout='wide',page_title='StartUp Funding')

df=pd.read_csv('startup_funding_cleaned')
def to_inr(dollar):
    inr=dollar*88.0
    return inr/10000000

df['amount']=df['amount'].apply(to_inr)

#---------------------------------------------------------------------------------------------------------------------------------------
#PreProcessing Area
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month']=df['date'].dt.month
df['year']=df['date'].dt.year
df.info()
#-------------------------------------------------------------------------------------------------------------------------------------------------
#Functions Area
def loadoverallanalysis():
    st.title('Overall Analysis')

    col1,col2,col3,col4=st.columns(4)

    with col1:
      #total amount invested in indian startup
      total = df['amount'].sum()
      # Format the total value with one decimal point using f-string
      formatted_total = f"{total:.1f}"

      # Display the metric with the formatted total
      st.metric('Total', f"{formatted_total} Cr")

    with col2:
        #max funding
        max_funding=df.groupby('startup')['amount'].sum().max()
        st.metric('Max Funding',str(max_funding)+'Cr')

    with col3:
        #avg funding
        avg_funding=df.groupby('startup')['amount'].sum().mean()
        formatted_avg = f"{avg_funding:.1f}"
        st.metric('Avg', f"{formatted_avg} Cr")

    with col4:
        #Total Funded Startup
        total_funded_startup=df['startup'].nunique()
        st.metric('Total Startup',total_funded_startup)
    
    #MoM graph
    st.header('Year On Year Graph')
    selected_opt=st.selectbox('Select Type',['Total','Count'])

    if selected_opt=='Total':
        tempdf=df.groupby('year')['amount'].sum().reset_index()
    
        
        fig7,ax7=plt.subplots()
        fig7.patch.set_facecolor('none')
        #setting bg color transparent
        ax7.set_facecolor('none')

        # Set tick labels to white
        ax7.tick_params(axis='both', colors='white')

        ax7.plot(tempdf['year'],tempdf['amount'])
        st.pyplot(fig7)

    if selected_opt=='Count':
        tempdf=tempdf=df.groupby('year')['startup'].count().reset_index()

        
        fig8,ax8=plt.subplots()
        fig8.patch.set_facecolor('none')
        #setting bg color transparent
        ax8.set_facecolor('none')

        # Set tick labels to white
        ax8.tick_params(axis='both', colors='white')

        ax8.plot(tempdf['year'],tempdf['startup'])
        st.pyplot(fig8)


    col5,col6=st.columns(2)
    with col5:
        #making city-wise
        st.header('City Wise Funding')
        temdf2=df.groupby('city')['amount'].sum().reset_index().sort_values('amount',ascending=False).reset_index()
        st.dataframe(temdf2,hide_index=True)
     
    with col6:
        #year wise top startups
        st.header('Year Wise top Startups')
        idx_max_amount = df.groupby('year')['amount'].idxmax()
        result_df = df.loc[idx_max_amount, ['year', 'startup', 'amount']].reset_index(drop=True)
        
        st.dataframe(result_df[['year', 'startup', 'amount']],hide_index=True)
    
    col1, col2 = st.columns(2)

    with col1:
        st.header('Top Investors')
        df_top_inv = df.groupby('investors')['amount'].sum().reset_index().sort_values('amount',ascending=False).head(5)
        st.dataframe(df_top_inv, hide_index=True)

    # Add other content to col2 or leave it blank
    with col2:
        # Add content to the second column if needed
        pass
    
    #Sector Analysis Pie
    st.header('Sectors Pie-Chart')
    temdf1=df.groupby('vertical')['startup'].count().reset_index()
    #Making white bg transparent
    fig9,ax9=plt.subplots()
    fig9.patch.set_facecolor('none')

        

    ax9.pie(temdf1['startup'],labels=temdf1['vertical'],labeldistance=2.05,autopct="%0.01f", textprops={'color': 'white'})
    st.pyplot(fig9)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def loadcompany(company):
    st.title(company)
    
        

    matching_rows = df[df['startup'].str.contains(company)]
    if not matching_rows.empty:
        col1,col2,col3,col4=st.columns(4)
        with col1:
            company_name = matching_rows['startup'].iloc[0]
            st.metric('Company Name', str(company_name))
        with col2:
            vertical=df[df['startup'].str.contains(company)]['vertical'].iloc[0]
            st.metric('Industry',str(vertical))
        with col3:
            subvertical=df[df['startup'].str.contains(company)]['subvertical'].iloc[0]
            st.metric('SubIndustry',str(subvertical))
        with col4:
            location=df[df['startup'].str.contains(company)]['city'].iloc[0]
            st.metric('Location',str(location))

        st.header('Summary')
        abc=df.groupby('startup')[['startup','round','date','investors']]
        vr=abc.head()
        vv = pd.DataFrame(vr)
        filtered_df = vv[vv['startup'].str.contains(company)][['round', 'date', 'investors']]
        st.dataframe(filtered_df,hide_index=True)
    else:
        st.warning(f"No matching companies found for '{company}'")
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def loadinvestor(investor):
    st.title(investor)


    #load top 5 recent investments
    
    last5_df=df[df['investors'].str.contains(investor)].head(5)[['date','startup','vertical','city','round','amount']]
    st.subheader('Top Recent Investments')
    st.dataframe(last5_df)

    #--------------------------------------------------------------------------------------
    col1,col2=st.columns(2)
    with col1:
        #biggest investment
        big_series=df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investment')
        fig,ax=plt.subplots()
        fig.patch.set_facecolor('none')

        ax.set_facecolor('none')
        ax.xaxis.set_visible(True)

        # Removing spines (borders) around the plot
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Setting the color of tick labels

        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Invested in')
        
        #Making white bg transparent
        fig1,ax1=plt.subplots()
        fig1.patch.set_facecolor('none')

        

        ax1.pie(vertical_series,labels=vertical_series.index,labeldistance=1.05,autopct="%0.01f", textprops={'color': 'white'})
        st.pyplot(fig1)

    col3,col4=st.columns(2)
    
    #amount per round investment pie chart
    with col3:
        df_roundseries=df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Per Round Investment')
        
        #Making white bg transparent
        fig2,ax2=plt.subplots()
        fig2.patch.set_facecolor('none')

        

        ax2.pie(df_roundseries,labels=df_roundseries.index,labeldistance=1.05,autopct="%0.01f", textprops={'color': 'white'})
        st.pyplot(fig2)

    #city invested in
    with col4:
        df_city_inves_series=df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('City Invested In')

        #Making white bg transparent
        fig3,ax3=plt.subplots()
        fig3.patch.set_facecolor('none')

        

        ax3.pie(df_city_inves_series,labels=df_city_inves_series.index,labeldistance=1.05,autopct="%0.01f", textprops={'color': 'white'})
        st.pyplot(fig3)


    col5,col6=st.columns(2)

    with col5:
        df_year_investment_series=df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        st.subheader('YearOnYear Investment')
       
        #Making white bg transparent
        fig4,ax4=plt.subplots()
        fig4.patch.set_facecolor('none')

        #setting bg color transparent
        ax4.set_facecolor('none')

        # Set tick labels to white
        ax4.tick_params(axis='both', colors='white')

        #plotting line plot
        ax4.plot(df_year_investment_series.index,df_year_investment_series.values)
        st.pyplot(fig4)




#------------------------------------------------------------------------------------------------------------------------------
#Dashboard Area
st.sidebar.title('StartUp Funding Analysis')

option=st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option =='Overall Analysis':
        loadoverallanalysis()
elif option=='Startup':
    
    company=st.sidebar.selectbox('Select StartUp', sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Startup Details')
    if btn1:
        loadcompany(company)
else:
    investor=st.sidebar.selectbox('Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2=st.sidebar.button('Investor Details')
    if btn2:
        loadinvestor(investor)


import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import plotly.express as px
import pandas as pd
import requests
import json
from PIL import Image

# Establish database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sandy@2914",
    auth_plugin="mysql_native_password",
    database='Phonepe_data'
)

# Retrieve data from the database tables
cursor = db.cursor()
db.commit()
cursor.execute("select * from Phonepe_data.agg_trans ")
Table1 = cursor.fetchall()
Agg_trans = pd.DataFrame(Table1, columns=("States", "Years", "Quarter", "Trans_type", "Trans_count", "Trans_amount"))

cursor = db.cursor()
db.commit()
cursor.execute("select * from Phonepe_data.agg_user ")
Table2 = cursor.fetchall()
Agg_user = pd.DataFrame(Table2, columns=("States", "Years", "Quarter", "Brand", "Trans_count", "Percentage"))

cursor = db.cursor()
db.commit()
cursor.execute("select * from Phonepe_data.map_trans ")
Table3 = cursor.fetchall()
map_trans = pd.DataFrame(Table3, columns=("States", "Years", "Quarter", "District", "Trans_count", "Trans_amount"))

cursor = db.cursor()
db.commit()
cursor.execute("select * from Phonepe_data.map_users ")
Table4 = cursor.fetchall()
map_user = pd.DataFrame(Table4, columns=("States", "Years", "Quarter", "District", "Registered_users", "AppOpens"))

cursor = db.cursor()
db.commit()
cursor.execute("select * from Phonepe_data.top_trans ")
Table5 = cursor.fetchall()
Top_trans = pd.DataFrame(Table5, columns=("States", "Years", "Quarter", "Pincode", "Trans_count", "Trans_amount"))

cursor = db.cursor()
db.commit()
cursor.execute("select * from Phonepe_data.top_user ")
Table6 = cursor.fetchall()
Top_user = pd.DataFrame(Table6, columns=("States", "Years", "Quarter", "Pincode", "Registered_users"))


def Trans_amt_count_year(df, year):

    Trans_amt_count_year = df[df["Years"] == year]
    Trans_amt_count_year.reset_index(drop=True, inplace=True)

    Trans_amt_count_year_G = Trans_amt_count_year.groupby("States")[["Trans_count", "Trans_amount"]].sum()
    Trans_amt_count_year_G.reset_index(inplace=True)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    States_names = []

    for features in data1["features"]:
        States_names.append(features["properties"]['ST_NM'])
    States_names.sort()

    col1,col2=st.columns(2)
    with col1:
        India_fig1 = px.choropleth(Trans_amt_count_year_G, 
                                        geojson=data1, 
                                        locations="States",
                                        featureidkey="properties.ST_NM",
                                        color="Trans_amount", 
                                        color_continuous_scale="Sunsetdark",
                                        range_color=(Trans_amt_count_year_G["Trans_amount"].min(), Trans_amt_count_year_G["Trans_amount"].max()),
                                        hover_name="States",
                                        title=f"{year} TRANSACTION AMOUNT",
                                        fitbounds="locations",
                                        width=600, 
                                        height=600)
        India_fig1.update_geos(visible=False)
        st.plotly_chart(India_fig1)
        
    with col2:
        India_fig2 = px.choropleth(Trans_amt_count_year_G, 
                                        geojson=data1, 
                                        locations="States",
                                        featureidkey="properties.ST_NM",
                                        color="Trans_count", 
                                        color_continuous_scale="tealrose",
                                        range_color=(Trans_amt_count_year_G["Trans_count"].min(), Trans_amt_count_year_G["Trans_count"].max()), 
                                        hover_name="States",
                                        title=f"{year} TRANSACTION COUNT",
                                        fitbounds="locations",
                                        width=600, 
                                        height=600)
        India_fig2.update_geos(visible=False)
        st.plotly_chart(India_fig2)
    
    return Trans_amt_count_year


def Trans_amt_count_year_Q(df, quarter):

    Trans_amt_count_year = df[df["Quarter"] == quarter]
    Trans_amt_count_year.reset_index(drop=True, inplace=True)

    Trans_amt_count_year_G = Trans_amt_count_year.groupby("States")[["Trans_count", "Trans_amount"]].sum()
    Trans_amt_count_year_G.reset_index(inplace=True)

 
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    States_names = []

    for features in data1["features"]:
        States_names.append(features["properties"]['ST_NM'])
    States_names.sort()

    col1,col2=st.columns(2)
    with col1:

        India_fig1 = px.choropleth(Trans_amt_count_year_G, 
                                        geojson=data1, 
                                        locations="States",
                                        featureidkey="properties.ST_NM",
                                        color="Trans_amount", 
                                        color_continuous_scale="Sunsetdark",
                                        range_color=(Trans_amt_count_year_G["Trans_amount"].min(), Trans_amt_count_year_G["Trans_amount"].max()),
                                        hover_name="States",
                                        title=f"{Trans_amt_count_year['Years'].unique()} {quarter} QUARTER TRANSACTION AMOUNT",
                                        fitbounds="locations",
                                        width=650, 
                                        height=600)
        India_fig1.update_geos(visible=False)
        st.plotly_chart(India_fig1)
    with col2:
    
        India_fig2 = px.choropleth(Trans_amt_count_year_G, 
                                        geojson=data1, 
                                        locations="States",
                                        featureidkey="properties.ST_NM",
                                        color="Trans_count", 
                                        color_continuous_scale="tealrose",
                                        range_color=(Trans_amt_count_year_G["Trans_count"].min(), Trans_amt_count_year_G["Trans_count"].max()), 
                                        hover_name="States",
                                        title=f"{Trans_amt_count_year['Years'].unique()} {quarter} QUARTER TRANSACTION COUNT",
                                        fitbounds="locations",
                                        width=650, 
                                        height=600)
        India_fig2.update_geos(visible=False)
        st.plotly_chart(India_fig2)
    
    return Trans_amt_count_year

def Agg_trans_Trans_type(df, states):

    Trans_amt_count_year = df[df["States"] == states]
    Trans_amt_count_year.reset_index(drop=True, inplace=True)

    Trans_amt_count_year_G = Trans_amt_count_year.groupby("Trans_type")[["Trans_count", "Trans_amount"]].sum()
    Trans_amt_count_year_G.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        pie_fig1 = px.pie(data_frame=Trans_amt_count_year_G, names="Trans_type", values="Trans_amount", width=600, title=f"{states} Transaction Amount", color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(pie_fig1)

    with col2:
        pie_fig2 = px.pie(data_frame=Trans_amt_count_year_G, names="Trans_type", values="Trans_count", width=600, title=f"{states} Transaction Count", color_discrete_sequence=px.colors.sequential.Agsunset_r)
        st.plotly_chart(pie_fig2)


def Agg_user_plot(df, year):
    Agg_user_year = df[df["Years"] == year]
    Agg_user_year.reset_index(drop=True, inplace=True)
    Agg_user_year = pd.DataFrame(Agg_user_year.groupby("Brand")["Trans_count"].sum())
    Agg_user_year.reset_index(inplace=True)
    Agg_user_fig1 = px.bar(Agg_user_year, x="Brand", y="Trans_count", title=f"{year} Brands & Transaction Count", color_discrete_sequence=px.colors.sequential.Sunsetdark_r)
    st.plotly_chart(Agg_user_fig1)

def Agg_user_year_Quarter(df, quarter):
    Agg_user_year_Q = df[df["Quarter"] == quarter]
    Agg_user_year_Q.reset_index(drop=True, inplace=True)
    Agg_user_year_Grp = pd.DataFrame(Agg_user_year_Q.groupby("Brand")["Trans_count"].sum())
    Agg_user_year_Grp.reset_index(inplace=True)
    Agg_user_fig2 = px.bar(Agg_user_year_Grp, x="Brand", y="Trans_count", title=f"{quarter} Quarter Brands & Transaction Count", color_discrete_sequence=px.colors.sequential.Sunsetdark_r)
    st.plotly_chart(Agg_user_fig2)
    return Agg_user_year_Q

def Agg_user_year_States(df, states):
    Agg_user_year_S = df[df["States"] == states]
    Agg_user_year_S.reset_index(drop=True, inplace=True)
    Agg_user_year_S_grp = Agg_user_year_S.groupby("Brand")["Trans_count"].sum().reset_index()
    pie_fig1 = px.line(data_frame=Agg_user_year_S_grp, x="Brand", y="Trans_count", width=600, title=f"{states} Transaction Count",color_discrete_sequence=px.colors.sequential.Agsunset,markers=True)
    st.plotly_chart(pie_fig1)
    return Agg_user_year_S


def Map_trans_district(df,states):

    Map_amt_count_year=df[df["States"]==states]
    Map_amt_count_year.reset_index(drop=True,inplace=True)

    Map_amt_count_year_G= Map_amt_count_year.groupby("District")[["Trans_count","Trans_amount"]].sum()
    Map_amt_count_year_G.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        bar_fig1=px.bar(data_frame=Map_amt_count_year_G,x="Trans_amount",y="District",width=600,title=f"{states} Dristrict & Transaction Amount",color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(bar_fig1)

   
    with col2:
        bar_fig2=px.bar(data_frame=Map_amt_count_year_G,x="Trans_amount",y="District",width=600,title=f"{states} Dristrict & Transaction Count",color_discrete_sequence=px.colors.sequential.Agsunset_r)
        st.plotly_chart(bar_fig2)

def Map_user_plot(df, year):
    Map_user_year = df[df["Years"] == year]
    Map_user_year_G = Map_user_year.groupby("States")[["Registered_users", "AppOpens"]].sum()
    Map_user_year_G.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        Map_user_fig1 = px.line(Map_user_year_G, x="States", y="Registered_users", title="Registered Users", color_discrete_sequence=px.colors.sequential.Sunsetdark_r, markers=True)
        st.plotly_chart(Map_user_fig1)
    with col2:
        Map_user_fig2 = px.line(Map_user_year_G, x="States", y="AppOpens", title="App Opens", color_discrete_sequence=px.colors.sequential.Pinkyl_r, markers=True)
        st.plotly_chart(Map_user_fig2)
    return Map_user_year

def Map_user_quarter(df,quarter):
    Map_user_Quarter = df[df["Quarter"] == quarter]
    Map_user_Quarter.reset_index(drop=True, inplace=True)
    Map_user_Quarter_G =Map_user_Quarter.groupby("States")[["Registered_users","AppOpens"]].sum()
    Map_user_Quarter_G.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        Map_user_fig1 = px.line(Map_user_Quarter_G, x="States", y=["Registered_users"],title=f"{quarter} Quarter Registered User", color_discrete_sequence=px.colors.sequential.Sunsetdark_r,markers=True)
        st.plotly_chart(Map_user_fig1)
    with col2:
        Map_user_fig2 = px.line(Map_user_Quarter_G, x="States", y=["AppOpens"],title=f"{quarter} Quarter AppOpens", color_discrete_sequence=px.colors.sequential.Pinkyl_r,markers=True)
        st.plotly_chart(Map_user_fig2)
    return Map_user_Quarter


def Map_user_district(df, states):
    Map_user_State = df[df["States"] == states]
    Map_user_State.reset_index(drop=True, inplace=True)

    bar_fig = px.bar(data_frame=Map_user_State,
                     x=["Registered_users", "AppOpens"],
                     y="District",
                     width=800,
                     title=f"{states} District & Registered Users/AppOpens",
                     color_discrete_sequence=px.colors.sequential.Agsunset,
                     orientation="h")
  
    st.plotly_chart(bar_fig)



def Top_trans_State(df,state):
    Top_trans_State = df[df["States"] == state]
    Top_trans_State.reset_index(drop=True, inplace=True)
    Top_trans_State_sorted = Top_trans_State.sort_values(by="Trans_amount", ascending=True)  # or "Trans_count" for transaction count

    col1,col2=st.columns(2)
    with col1:
       
        Top_trans_fig1 = px.bar(Top_trans_State, x="Quarter", y="Trans_amount",title=" Transaction_amount", color_discrete_sequence=px.colors.sequential.Sunsetdark_r,hover_data="Pincode",)
        st.plotly_chart(Top_trans_fig1)
    with col2:
        Top_trans_fig2 = px.bar(Top_trans_State, x="Quarter", y="Trans_count",title=" Transaction_count", color_discrete_sequence=px.colors.sequential.Pinkyl_r,hover_data="Pincode")
        st.plotly_chart(Top_trans_fig2)

def Top_user_plot1(df,year):
    Top_user_year = df[df["Years"] == year]
    Top_user_year.reset_index(drop=True, inplace=True)
    Top_user_year_G = pd.DataFrame(Top_user_year.groupby(["States", "Quarter"])["Registered_users"].sum()).reset_index()
    Agg_user_fig1 = px.bar(Top_user_year_G, x="States", y="Registered_users", color="Quarter", title="Registered Users", color_discrete_sequence=px.colors.sequential.Reds_r,height=800,width=800)
    st.plotly_chart(Agg_user_fig1)
    return Top_user_year

def Top_user_plot2(df,state):
    Top_user_state = df[df["States"] == state]
    Top_user_state.reset_index(drop=True, inplace=True)
    Top_user_fig1 = px.bar(Top_user_state, x="Quarter", y="Registered_users",color="Registered_users", title="Registered Users,Quarter,Pincodes", color_discrete_sequence=px.colors.sequential.Magenta_r,hover_name="Pincode")
    st.plotly_chart(Top_user_fig1)
    return Top_user_state


def Top_chart1(table_name):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sandy@2914",
        auth_plugin="mysql_native_password",
        database='Phonepe_data')

    cursor = db.cursor()

    query1 = '''SELECT States, SUM(Trans_amount) AS Total_Trans_amount
                FROM phonepe_data.top_trans 
                GROUP BY States
                ORDER BY Total_Trans_amount desc limit 10;'''

    cursor.execute(query1)
    table = cursor.fetchall()
    db.commit()
    df1 = pd.DataFrame(table, columns=("States", "Total_Trans_amount"))
    col1,col2=st.columns(2)
    with col1:
      df1
    with col2:
    
        fig1 = px.bar(df1, x="States", y="Total_Trans_amount", title="Transaction Amount", color_discrete_sequence=px.colors.sequential.Reds_r,height=600,width=650)
        st.plotly_chart(fig1)

def Top_chart2(table_name):
    query2 = '''SELECT States, SUM(Trans_amount) AS Total_Trans_amount
                FROM phonepe_data.top_trans 
                GROUP BY States
                ORDER BY Total_Trans_amount asc limit 10;'''

    cursor.execute(query2)
    table = cursor.fetchall()
    db.commit()
    df2 = pd.DataFrame(table, columns=("States", "Total_Trans_amount"))
    col1,col2=st.columns(2)
    with col1:
      df2
    with col2:
        fig2 = px.bar(df2, x="States", y="Total_Trans_amount", title="Least 10 Transaction Amount", color_discrete_sequence=px.colors.sequential.Magenta_r,height=600,width=650)
        st.plotly_chart(fig2)


def Top_chart3(table_name):
    query3 = '''SELECT District, SUM(Trans_amount) as Trans_amount_sum
            FROM phonepe_data.map_trans
            group by DISTRICT
            order by Trans_amount_sum desc limit 10;'''

    cursor.execute(query3)
    table = cursor.fetchall()
    db.commit()
    df3 = pd.DataFrame(table, columns=("District", "Total_Trans_amount"))
    col1,col2=st.columns(2)
    with col1:
      df3
    with col2:
        fig3 = px.bar(df3, x="District", y="Total_Trans_amount", title="Top 10 Transaction Amount", color_discrete_sequence=px.colors.sequential.Blugrn_r,height=600,width=650)
        st.plotly_chart(fig3)


def Top_chart4(table_name):
    query4 = '''SELECT District, SUM(Trans_amount) as Trans_amount_sum
                FROM phonepe_data.map_trans
                GROUP BY District
                ORDER BY Trans_amount_sum ASC
                LIMIT 10;'''

    cursor.execute(query4)
    table = cursor.fetchall()
    db.commit()
    df4 = pd.DataFrame(table, columns=("District", "Trans_amount_sum"))
    col1,col2=st.columns(2)
    with col1:
        df4
    with col2:
        fig4 = px.bar(df4, x="District", y="Trans_amount_sum", title="Least 10 Transaction Amount", color_discrete_sequence=px.colors.sequential.Mint_r, height=600, width=650)
        st.plotly_chart(fig4)
    

def Top_chart5(table_name):
        query5 = '''SELECT States, sum(AppOpens ) as Total_AppOpens
                    from phonepe_data.map_users
                    group by States
                    order by Total_AppOpens desc limit 10;'''

        cursor.execute(query5)
        table = cursor.fetchall()
        db.commit()
        df5 = pd.DataFrame(table, columns=("States", "Total_AppOpens"))
        col1,col2=st.columns(2)
        with col1:
           df5
        with col2:
        
            fig5 = px.bar(df5, x="States", y="Total_AppOpens", title="Top 10 App opens", color_discrete_sequence=px.colors.sequential.Mint_r,height=600,width=650)
            st.plotly_chart(fig5)

def Top_chart6(table_name):
    query6 = '''SELECT States, sum(AppOpens) as Total_AppOpens
                FROM phonepe_data.map_users
                GROUP BY States
                ORDER BY Total_AppOpens ASC LIMIT 10;'''

    cursor.execute(query6)
    table = cursor.fetchall()
    db.commit()
    df6 = pd.DataFrame(table, columns=("States", "Total_AppOpens"))
    col1,col2=st.columns(2)
    with col1:
        df6
    with col2:
        fig6 = px.bar(df6, x="States", y="Total_AppOpens", title="Least 10 App opens", color_discrete_sequence=px.colors.sequential.Mint_r, height=600, width=650)
        st.plotly_chart(fig6)

def Top_chart7(table_name):
        query7= '''SELECT District, sum(Registered_users) as Total_Registered_users
                            from phonepe_data.map_users
                            group by District
                            order by Total_Registered_users desc limit 10;'''

        cursor.execute(query7)
        table = cursor.fetchall()
        db.commit()
        df7 = pd.DataFrame(table, columns=("District", "Total_Registered_users"))
        col1,col2=st.columns(2)
        with col1:
           df7
        with col2:
            fig7=px.bar(df7, x="District", y="Total_Registered_users", title="Top 10 Registered Users Based On District", color_discrete_sequence=px.colors.sequential.Mint_r,height=600,width=650)
            st.plotly_chart(fig7)


def Top_chart8(table_name):
        query8= '''SELECT District, sum(Registered_users) as Total_Registered_users
                            from phonepe_data.map_users
                            group by District
                            order by Total_Registered_users asc limit 10;'''

        cursor.execute(query8)
        table = cursor.fetchall()
        db.commit()
        df8 = pd.DataFrame(table, columns=("District", "Total_Registered_users"))
        col1,col2=st.columns(2)
        with col1:
           df8
        with col2:
            fig8=px.bar(df8, x="District", y="Total_Registered_users", title="Least 10 Registered Users Based On District", color_discrete_sequence=px.colors.sequential.Mint_r,height=600,width=650)
            st.plotly_chart(fig8)


def Top_chart9(table_name):
        query9= '''SELECT States,  SUM(Trans_count) AS Total_Trans_count
                    FROM phonepe_data.agg_trans
                    GROUP BY States
                    ORDER BY Total_Trans_count DESC LIMIT 10;;'''

        cursor.execute(query9)
        table = cursor.fetchall()
        db.commit()
        df9 = pd.DataFrame(table, columns=("States", "Total_Trans_count"))
        col1,col2=st.columns(2)
        with col1:
           df9
        with col2:
            fig9=px.bar(df9, x="States", y="Total_Trans_count", title="Top 10 State Total Transaction Count ", color_discrete_sequence=px.colors.sequential.Mint_r,height=600,width=650)
            st.plotly_chart(fig9)

def Top_chart10(table_name):
        query10= '''SELECT States,  SUM(Trans_count) AS Total_Trans_count
                    FROM phonepe_data.agg_trans
                    GROUP BY States
                    ORDER BY Total_Trans_count ASC LIMIT 10;'''

        cursor.execute(query10)
        table = cursor.fetchall()
        db.commit()
        df10 = pd.DataFrame(table, columns=("States", "Total_Trans_count"))
        col1,col2=st.columns(2)
        with col1:
            df10
        with col2:
            fig10=px.bar(df10, x="States", y="Total_Trans_count", title="Least 10 State Total Transaction Count ", color_discrete_sequence=px.colors.sequential.YlGn_r,height=600,width=650)
            st.plotly_chart(fig10)

def Top_chart11(table_name):
    query11 = '''SELECT trans_type, MIN(Trans_amount) AS min_Trans_amount
                 FROM phonepe_data.agg_trans
                 GROUP BY trans_type
                 ORDER BY MIN(Trans_amount)
                 LIMIT 10;'''

    cursor.execute(query11)
    table = cursor.fetchall()
 
    df11 = pd.DataFrame(table, columns=["trans_type", "min_Trans_amount"])

    col1, col2 = st.columns(2)
    with col1:
        st.write(df11)  
    with col2:
        pie_fig11 = px.pie(
            data_frame=df11, 
            names="trans_type", 
            values="min_Trans_amount", 
            width=600, 
            title="Minimum Transaction Amount for Transaction Type", 
            color_discrete_sequence=px.colors.sequential.Agsunset_r
        )
        st.plotly_chart(pie_fig11)

def Top_chart12(table_name):
    query12= '''SELECT trans_type, Max(Trans_amount) AS max_Trans_amount
                 FROM phonepe_data.agg_trans
                 GROUP BY trans_type
                 ORDER BY Max(Trans_amount)
                 desc LIMIT 10 ;'''

    cursor.execute(query12)
    table = cursor.fetchall()
 
    df12= pd.DataFrame(table, columns=["trans_type", "max_Trans_amount"])

    col1, col2 = st.columns(2)
    with col1:
        st.write(df12)  
    with col2:
        pie_fig12 = px.pie(
            data_frame=df12, 
            names="trans_type", 
            values="max_Trans_amount", 
            width=600, 
            title="Maximum Transaction Amount for Transaction Type", 
            color_discrete_sequence=px.colors.sequential.Agsunset_r
        )
        st.plotly_chart(pie_fig12)



st.set_page_config(layout="wide")

st.image(r"C:\Users\sandh\OneDrive\Desktop\download.png", width=80)

st.markdown("<h1 style='display: flex; align-items: center; font-size: 27px; margin: 0;'>PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION</h1>", unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu("Menu", ["Home","Explore Data","Top Charts"], 
                icons=["house","bar-chart-line","graph-up-arrow", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
    


if selected == "Home":
    
    col1, col2 = st.columns(2)

    with col1:

        st.header(" ")
        st.write("""
        PhonePe is a prominent Indian digital payments and financial services company founded in December 2015. 
        It provides a comprehensive platform for mobile payments, allowing users to make instant money transfers, 
        pay bills, recharge mobile phones, and shop online through its seamless interface. Leveraging the Unified Payments 
        Interface (UPI), PhonePe has revolutionized the digital transaction landscape in India, offering secure and 
        efficient financial solutions. With millions of active users and a wide array of services, PhonePe continues 
        to drive the adoption of digital payments, enhancing financial inclusion and convenience across the country.
        """)
        st.subheader("Features:")
        st.write("1.Seamless UPI payments for instant money transfers.")
        st.write("2.Diverse financial services including insurance and mutual funds.")
        st.write("3.Secure digital wallet for storing and managing funds.")
        st.write("4.Extensive merchant network for payments at local stores and online platforms")
        st.write("5.Quick bill payments and mobile recharges for added convenience.")
       


    with col2:
 
        st.image(r"C:\Users\sandh\OneDrive\Desktop\image_processing20200114-26356-1dzvejl.gif")


        st.download_button("⬇️ Download The App", "https://www.phonepe.com/app-download/")

        
elif selected == "Explore Data":
    tab1, tab2, tab3 = st.tabs(["AGGREATED ANALYSIS", "MAP ANALYSIS", "TOP ANALYSIS" ])
    with tab1:
        col1,col2,col3,col4,col5=st.columns(5)
        with col1:
         option1 = st.selectbox("Select an option", ["Aggregated Tansaction", "Aggregated User"])

        if option1 == "Aggregated Tansaction":
            col1,col2,col3,col4,col5,col6,col7=st.columns(7)
            with col1:
                
             year = st.selectbox("Select The Year", Agg_trans["Years"].unique())
            Tacy = Trans_amt_count_year(Agg_trans, year)
            col1,col2,col3,col4,col5=st.columns(5)
            with col1:
               
             states = st.selectbox("Select The States", Tacy["States"].unique())
            Agg_trans_Trans_type(Tacy, states)
            col1,col2,col3,col4,col5=st.columns(5)
            with col1:
                quarters = st.slider("Select The Quarters", Tacy["Quarter"].min(), Tacy["Quarter"].max(), Tacy["Quarter"].min())
            Trans_acyq = Trans_amt_count_year_Q(Tacy, quarters)
        
            col1,col2,col3,col4,col5=st.columns(5)
            with col1:   
            
             states = st.selectbox("Select The State for Trans_type", Trans_acyq["States"].unique())
            Agg_trans_Trans_type(Trans_acyq, states)

        elif option1 == "Aggregated User":
            col1,col2,col3,col4,col5=st.columns(5)
            with col1:
             year = st.selectbox("Select The Year", Agg_user["Years"].unique())
            Agg_user_Y = Agg_user_plot(Agg_user, year)

            
            col1,col2,col3,col4,col5=st.columns(5)
            with col1:

             quarters = st.slider("Select The Quarter", Agg_user["Quarter"].min(), Agg_user["Quarter"].max(), Agg_user["Quarter"].min())
            Agg_user_Y_Q = Agg_user_year_Quarter(Agg_user, quarters)

            
            col1,col2,col3,col4,col5=st.columns(5)
            with col1:

             state = st.selectbox("Select The State", Agg_user_Y_Q["States"].unique())
            Agg_user_year_States(Agg_user_Y_Q, state)



    with tab2:
        col1,col2,col3,col4,col5=st.columns(5)
        with col1:
          option2=st.selectbox("Select an option", ["Map Tansaction","Map User"])
        if option2=="Map Tansaction":
            col1,col2,col3,col4,col5,col6=st.columns(6)
            with col1:
            
             year = st.selectbox("Select the Year", map_trans["Years"].unique())
            Map_trans_year = Trans_amt_count_year(map_trans, year)

            col1,col2,col3,col4,col5=st.columns(5)
            with col1:


             states = st.selectbox("Select The State:", Map_trans_year["States"].unique())
            
            Map_trans_district(Map_trans_year,states)
            col1,col2,col3,col4,col5=st.columns(5)
            with col1:
             quarters = st.slider("Select the Quarters", Map_trans_year["Quarter"].min(), Map_trans_year["Quarter"].max(), Map_trans_year["Quarter"].min())
            Map_acyq = Trans_amt_count_year_Q(Map_trans_year, quarters)
            
            col1,col2=st.columns(2)
            with col1:
              states = st.selectbox("Select the state", Map_acyq["States"].unique())
            Map_trans_district(Map_acyq,states)


        elif option2 == "Map User":
            col1,col2,col3,col4,col5=st.columns(5)
            with col1:
              year = st.selectbox("Select the Year", map_user["Years"].unique())
            Map_user_Y=Map_user_plot(map_user,year)

            col1,col2,col3,col4,col5=st.columns(5)
            with col1:
             quarters = st.slider("Select the Quarters", Map_user_Y["Quarter"].min(), Map_user_Y["Quarter"].max(), Map_user_Y["Quarter"].min())

            Map_user_Q=Map_user_quarter(Map_user_Y,quarters)

            col1,col2,col3,col4,col5=st.columns(5)
            with col1:
              states = st.selectbox("Select the state", Map_user_Q["States"].unique())
            Map_user_D=Map_user_district(Map_user_Q,states)

    with tab3:
        col1,col2,col3,col4,col5=st.columns(5)
        with col1:
           option3=st.selectbox("Select an option", ["TOP Tansaction","TOP User"])
        if option3=="TOP Tansaction":
            col1,col2,col3,col4,col5=st.columns(5)
            with col1:
            
             year = st.selectbox("Select the Year.", Top_trans["Years"].unique())
            Top_trans_Y=Trans_amt_count_year(Top_trans,year)

            

            col1,col2,col3,col4,col5=st.columns(5)
            with col1:
             quarters = st.slider("Select the Quarter", Top_trans_Y["Quarter"].min(), Top_trans_Y["Quarter"].max(), Top_trans_Y["Quarter"].min())
            Top_acyq=Trans_amt_count_year_Q(Top_trans_Y,quarters)

            col1,col2,col3,col4,col5=st.columns(5)
            with col1:
              states = st.selectbox("Select the state!!!", Top_trans_Y["States"].unique())
            Top_trans_State(Top_trans_Y,states)
            

        elif option3=="TOP User":
            col1,col2,col3,col4,col5=st.columns(5)
            with col1:
            
             year = st.selectbox("Select the Year.", Top_user["Years"].unique())
            Top_user_Y=Top_user_plot1(Top_user,year)

            col1,col2,col3,col4,col5=st.columns(5)
            with col1:
              states = st.selectbox("Select the State!!!", Top_user_Y["States"].unique())
            Top_user_plot2(Top_user_Y,states)            

            
elif selected == "Top Charts":
    Question = st.selectbox("To know more, Select the Questions:", [
        "1. Top 10 states based on the transaction amount",
        "2. Least 10 states based on the transaction amount",
        "3. Top 10 districts & Transaction amount",
        "4. Least 10 districts & Transaction amount",
        "5. Top 10 states of app users",
        "6. Least 10 states of app users",
        "7. Top registered users based on district",
        "8. Least registered users based on district",
        "9. Top states transaction count based on transaction types",
        "10. Least states transaction count based on transaction types",
        "11. Minimun transaction amount for Transaction type",
        "12. Maximum transaction amount for Transaction type"
    ])
    if Question=="1. Top 10 states based on the transaction amount":
       Top_chart1(Agg_trans)
    elif Question=="2. Least 10 states based on the transaction amount":
       Top_chart2(Agg_trans)
    elif Question=="3. Top 10 districts & Transaction amount":
       Top_chart3(map_trans)
    elif Question=="4. Least 10 districts & Transaction amount":
       Top_chart4(map_trans)
    elif Question=="5. Top 10 states of app users":
       Top_chart5(map_user)
    elif Question=="6. Least 10 states of app users":
       Top_chart6(map_user)
    elif Question=="7. Top registered users based on district":
       Top_chart7(map_user)
    elif Question=="8. Least registered users based on district":
       Top_chart8(map_user)
    elif Question=="9. Top states transaction count based on transaction types":
       Top_chart9(Agg_trans)
    elif Question=="10. Least states transaction count based on transaction types":
       Top_chart10(Agg_trans)
    elif Question=="11. Minimun transaction amount for Transaction type":
       Top_chart11(Agg_trans)
    elif Question=="12. Maximum transaction amount for Transaction type":
       Top_chart12(Agg_trans)

       
       

import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
st.set_page_config(layout='wide')
df=pd.read_csv("heart_disease_ubdate.csv")
tab1 , tab2 , tab3 = st.tabs(["catigorical","numrical","dynamic"])
gender = st.sidebar.multiselect("Select gender",df["Gender"].unique(),default=df["Gender"].unique())
mask1 = df["Gender"].isin(gender)
##create table##
def create_responsive_table(data, title):
    table_fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(data.columns),
            fill_color='navy',
            font=dict(color='white', size=12),
            align='center'
        ),
        cells=dict(
            values=[data[col] for col in data.columns],
            fill_color='lightgrey',
            font=dict(color='black',size=11),
            align='center'
        )
    )])
    table_fig.update_layout(
        width=400,  
        height=200,  
        margin=dict(l=0, r=0, t=0, b=0)  
    )
    return table_fig

#line of ages in sidebar
age_range = st.sidebar.slider(
    "select the age:",
    min_value=18,  
    max_value=80,  
    value=(18, 80),  
    step=1  
)
mask2 = df["Age"].between(age_range[0],age_range[1])
column_name1 = st.sidebar.multiselect("select columns analysis1",df.select_dtypes("O").columns,default=["Alcohol Consumption","Smoking"])
column_name2 = st.sidebar.multiselect("select columns analysis2",df.select_dtypes("O").columns,default=["Stress Level","Smoking"])
df_filter = df[mask1&mask2]
newdf =df
#fun to merge columns
def mix(columns):
    
    if len(columns) < 2:
        st.write("⚠️ Please select at least two columns to display the data.")
    
    
    combined_col = " & ".join(columns)
    newdf[combined_col] = newdf[list(columns)].astype(str).agg(" & ".join, axis=1)
    
   
    return px.histogram(
        data_frame=newdf,
        x=combined_col,
        y="Heart Disease Status",
        color="Age_Group",
        barmode="group"
    )

with tab1:
    col1,col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.pie(data_frame=df_filter,names="Age_Group",values="Heart Disease Status",title="Heart Disease Status by Age Group"))
        
    with col2:
        age_group_counts = df_filter["Age_Group"].value_counts().reset_index()
        fig = ff.create_table(age_group_counts)
        st.plotly_chart(fig)
        fig1 = ff.create_table(df["Heart Disease Status"].value_counts().to_frame().T.rename(columns={0:"No heart disease",1:"heart disease sufferers"}))
        st.plotly_chart(fig1)
    st.plotly_chart(px.pie(data_frame=df_filter,names="Smoking",values="Heart Disease Status",facet_col="Age_Group",hole=.4,title="Heart Disease Status by Smoking and Age Group"))
    col3,col4 = st.columns(2)
    mask = df["Smoking"]=="Yes"
    with col3:
        fig3=ff.create_table(pd.pivot_table(data=df_filter[mask],index="Gender",values="Smoking",aggfunc="count").reset_index().sort_values(by=["Gender"],ascending=False).head(1))
        st.plotly_chart(fig3)
    with col4:
        fig4=ff.create_table(pd.pivot_table(data=df_filter[mask],index="Age_Group",values="Smoking",aggfunc="count").reset_index().sort_values(by=["Age_Group"],ascending=False).head(1))
        st.plotly_chart(fig4)
   
    
    
    st.plotly_chart(px.pie(data_frame=df_filter[mask],names="Alcohol Consumption",values="Heart Disease Status",facet_col="Age_Group",hole=.4,title="Heart Disease Status by Alcohol and Age Group"))
    col5,col6,col7 = st.columns(3)
    mask = df["Alcohol Consumption"]=="High"
    mask2=df["Alcohol Consumption"]=="Medium"
    mask3=df["Alcohol Consumption"]=="Low"
    with col5:
        fig3=create_responsive_table(pd.pivot_table(data=df_filter[mask],index="Gender",values="Alcohol Consumption",aggfunc="count").reset_index().sort_values(by=["Gender"],ascending=False).rename(columns={"Alcohol Consumption":"Alcohol Consumption(H)"}),"High Consumption")
        st.plotly_chart(fig3,use_container_width=True)
    with col6:
        fig4=create_responsive_table(pd.pivot_table(data=df_filter[mask2],index="Gender",values="Alcohol Consumption",aggfunc="count").reset_index().sort_values(by=["Gender"],ascending=False).rename(columns={"Alcohol Consumption":"Alcohol Consumption(M)"}),"medium Consumption")
        st.plotly_chart(fig4,use_container_width=True)
    with col7:
        fig5=create_responsive_table(pd.pivot_table(data=df_filter[mask3],index="Gender",values="Alcohol Consumption",aggfunc="count").reset_index().sort_values(by=["Gender"],ascending=False).rename(columns={"Alcohol Consumption":"Alcohol Consumption(L)"}),"low Consumption")
        st.plotly_chart(fig5,use_container_width=True)


    
    st.plotly_chart(px.pie(data_frame=df_filter,names="Stress Level",values="Heart Disease Status",facet_col="Age_Group",hole=.4,title="Heart Disease Status by Stress Level and Age Group") )
    col8,col9,col10 = st.columns(3)
    mask4 = df["Stress Level"]=="High"
    mask5=df["Stress Level"]=="Medium"
    mask6=df["Stress Level"]=="Low"
    with col8:
        fig6=create_responsive_table(pd.pivot_table(data=df_filter[mask4],index="Gender",values="Stress Level",aggfunc="count").reset_index().sort_values(by=["Gender"],ascending=False).rename(columns={"Stress Level":"Stress Level(H)"}),"Stress Level H")
        st.plotly_chart(fig6,use_container_width=True)
    with col9:
        fig7=create_responsive_table(pd.pivot_table(data=df_filter[mask5],index="Gender",values="Stress Level",aggfunc="count").reset_index().sort_values(by=["Gender"],ascending=False).rename(columns={"Stress Level":"Stress Level(M)"}),"Stress Level M")
        st.plotly_chart(fig7,use_container_width=True)
    with col10:
        fig8=create_responsive_table(pd.pivot_table(data=df_filter[mask6],index="Gender",values="Stress Level",aggfunc="count").reset_index().sort_values(by=["Gender"],ascending=False).rename(columns={"Stress Level":"Stress Level(L)"}),"Stress Level L")
        st.plotly_chart(fig8,use_container_width=True)

    st.plotly_chart(px.pie(data_frame=df_filter,names="Exercise Habits",values="Heart Disease Status",facet_col="Age_Group",hole=.4,title="Heart Disease Status by Exercise Habits and Age Group") )
    
    
    st.plotly_chart(px.pie(data_frame=df_filter,names="Diabetes",values="Heart Disease Status",facet_col="Age_Group",hole=.4,title="Heart Disease Status by Diabetes and Age Group"))
    col11,col12=st.columns(2)
    with col11:
        st.plotly_chart(px.line(data_frame=df.sample(n=100, random_state=30).sort_index() ,y="Triglyceride Level",color="Diabetes",markers=True,color_discrete_sequence=["red","green"],title="Diabetes and Triglyceride Level"))
    with col12:
        st.markdown("<p style='margin-top: 10%;'>Number of diabetics of each gender</p>",unsafe_allow_html=True)
        fig9=ff.create_table(pd.pivot_table(data=df,index="Gender",values="Diabetes",aggfunc="count").T.reset_index().drop(["index"],axis=1)) 
        st.plotly_chart(fig9,use_container_width=True)
        
    st.plotly_chart(px.pie(data_frame=df_filter,names="High Blood Pressure",values="Heart Disease Status",facet_col="Age_Group",hole=.4,title="Heart Disease Status by High Blood Pressure and Age Group"))
    st.plotly_chart(px.histogram(data_frame=df,x="Sugar Consumption",y="Heart Disease Status",color="Age_Group",barmode="group",text_auto=True,title="Heart Disease Status by Sugar Consumption and Age Group"))
    col13,col14 = st.columns(2)
    with col13:
        st.plotly_chart(px.histogram(data_frame=df,x="Low HDL Cholesterol",y="Heart Disease Status",color="Age_Group",barmode="group",text_auto=True,title="Heart Disease Status by Low HDL Cholesterol and Age Group"))
        st.plotly_chart(px.histogram(data_frame=df_filter,x="Family Heart Disease",y="Heart Disease Status",title="Heart Disease Status by Family Heart Disease and Age Group"))
    with col14:
        st.plotly_chart(px.histogram(data_frame=df,x="High LDL Cholesterol",y="Heart Disease Status",color="Age_Group",barmode="group",text_auto=True,title="Heart Disease Status by High LDL Cholesterol and Age Group"))
        st.plotly_chart(px.histogram(data_frame=df,x="Exercise Habits",y="Heart Disease Status",title="Heart Disease Status by Exercise Habits"))
with tab2:
    col1,col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.box(data_frame=df, x='Age_Group', y='Blood Pressure',color='Heart Disease Status',title="Heart Disease Status by Blood Pressure and Age Group"))
        st.plotly_chart(px.box(data_frame=df, x='Age_Group', y='BMI', color='Heart Disease Status',title="Heart Disease Status by BMI and Age Group"))
        st.plotly_chart(px.box(data_frame=df, x='Age_Group', y='CRP Level', color='Heart Disease Status',title="Heart Disease Status by CRP Level and Age Group"))
        st.plotly_chart(px.box(data_frame=df, x='Age_Group', y='Homocysteine Level', color='Heart Disease Status',title="Heart Disease Status by Homocysteine Level and Age Group"))
   
    with col2:
        st.markdown("<p style='margin-top: 10%;'>Heart Disease Status by Age_Group</p>",unsafe_allow_html=True)
        fig10=ff.create_table(pd.pivot_table(data=df,index="Age_Group",values="Heart Disease Status",aggfunc="sum").reset_index())
        st.plotly_chart(fig10,use_container_width=True)
        st.markdown("<p style='margin-top: 27%;'></p>",unsafe_allow_html=True)
        st.plotly_chart(px.box(data_frame=df, x='Age_Group', y='Cholesterol Level', color='Heart Disease Status',title="Heart Disease Status by Cholesterol Level and Age Group"))
        st.plotly_chart(px.box(data_frame=df, x='Age_Group', y='Sleep Hours', color='Heart Disease Status',title="Heart Disease Status by Sleep Hours and Age Group"))
        st.plotly_chart(px.box(data_frame=df, x='Age_Group', y='Triglyceride Level', color='Heart Disease Status',title="Heart Disease Status by Triglyceride Level and Age Group"))
        st.plotly_chart(px.box(data_frame=df, x='Age_Group', y='Fasting Blood Sugar', color='Heart Disease Status',title="Heart Disease Status by Fasting Blood Sugar and Age Group"))
    


with tab3:
    col1,col2 = st.columns(2)
    with col1:
        st.plotly_chart(mix(column_name1))
    with col2:
        st.plotly_chart(mix(column_name2))
    

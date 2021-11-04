import pandas as pd
import streamlit as st

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')
        
tab = st.container()
upl = st.container()
with upl:
    table = st.file_uploader(label='העלאת דוח פעילים',type=['csv'])

with tab:
    try:
        st.title('!עמדת קליטה')
        st.title('')
        df = pd.read_csv(table)
        df = df.filter(['שם משפחה', 'שם פרטי','תאריך אישור הורים ותקנון','שנת פעילות 2021-22'])
        df = df.iloc[:, ::-1]
        show1 = st.checkbox('הצגת טבלה מקורית')
        if show1:
            st.dataframe(df)
        
        df2 = df
        filt = st.selectbox('בחירת מסנן',['None','הרשמה שנתית תקפה','אישור הורים תקף'],index=2)
        if filt == 'הרשמה שנתית תקפה':
            df2 = df2.loc[df['שנת פעילות 2021-22'] == 1.0000]
            activate_search=st.checkbox('לחצי לחיפוש')
            if activate_search:
                search = st.text_input('הכניסי שם פרטי או משפחה, לא שם מלא')
                df2=df2[df2['שם פרטי'].str.contains(search) | ['שם משפחה'].str.contains(search)]
            st.dataframe(df2)
        elif filt == 'אישור הורים תקף':
            df2=df2[df2['תאריך אישור הורים ותקנון'].str.contains('2021', na = False)]
            df2=df2[df2['תאריך אישור הורים ותקנון'].str[3:5:].isin(['09','10','11','12'])]
            activate_search=st.checkbox('לחצי לחיפוש')
            if activate_search:
                search = st.text_input('הכניסי שם פרטי')
                df2=df2[df2['שם פרטי'].str.contains(search)]
            st.dataframe(df2)
        save = st.checkbox('save?')
        if save:
            csv = convert_df(df2)
        st.download_button(label="הורדת קובץ",data=csv,file_name='krembo list.csv',mime='text/csv')

    except:
        pass
    

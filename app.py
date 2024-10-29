import streamlit as st
from boxer import boxer

config = {'equity' : 1000000,
        'bonds' : 1000000,
        'property' : 1000000,
        'equity_return' : 0.062,
        'bonds_return' : 0.035,
        'property_return' : 0.06,
        'inflation' : 0.02,
        'box2Rate_slice1' : 0.245,
        'box2Rate_slice2' : 0.31,
        'box2_slices_at' : 67000,
        'box3Rate' : 0.36,
        'box3_freezone' : 2500,
        'vpbRate_slice1' : 0.19,
        'vpbRate_slice2' : 0.258,
        'vpb_slices_at' : 200000,
        'bv_fees' : 3000,
        'term' : 5
        }

      
st.title("Box 2 vs Box 3")

with st.form('inputs', enter_to_submit=False):
    header = st.columns([1,2,2])
    header[1].subheader('Investering')
    header[2].subheader('Rendement')
    
    row1 = st.columns([1,1])
    equity_amount = row1[0].number_input("Aandelen", min_value=0, value=100000, step=25000, placeholder='Waarde aandelen')
    equity_return = row1[1].slider("",float(0), float(0.2), float(0.062), step=0.005)

    row2 = st.columns([1,1])
    bonds_amount = row2[0].number_input("Obligaties",min_value=0, value=100000, step=25000, placeholder='Waarde obligaties')
    bonds_return = row2[1].slider("",float(0), float(0.2), float(0.035), step=0.005)
    
    row3 = st.columns([1,1])
    property_amount = row3[0].number_input("Vastgoed",min_value=0, value=100000, step=25000, placeholder='Waarde vastgoed')
    property_return = row3[1].slider("", float(0), float(0.2), float(0.06), step=0.005)

    submitted = st.form_submit_button('Doorrekenen')
    
if submitted:

    config = {'equity' : equity_amount,
                'bonds' : bonds_amount,
                'property' : property_amount,
                'equity_return' : equity_return,
                'bonds_return' : bonds_return,
                'property_return' : property_return,
                'inflation' : 0.02,
                'box2Rate_slice1' : 0.245,
                'box2Rate_slice2' : 0.31,
                'box2_slices_at' : 67000,
                'box3Rate' : 0.36,
                'box3_freezone' : 2500,
                'vpbRate_slice1' : 0.19,
                'vpbRate_slice2' : 0.258,
                'vpb_slices_at' : 200000,
                'bv_fees' : 3000,
                'term' : 50
                }

    df = boxer(**config).output().astype('int')    
    df_voor_netto_waarde = df[['Portefeuille_Box2', 'Portefeuille_Box3', 'Netto_Box2', 'Netto_Box3']]
    df_voor_cum_tax = df[['Cum_Tax_Box2', 'Cum_Tax_Box3']]
    
    df_box2 = boxer(**config)._box2_calc().astype('int')
    df_box3 = boxer(**config)._box3_calc().astype('int')
    
    with st.container():
    
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Portefeuille", "📈 Cumulatieve belasting", "🗃 Output", "🗃 Box 2", "🗃 Box 3"])
        
        tab1.subheader("Portefeuille Box 2 en Box 3 na Exit")
        tab1.line_chart(df_voor_netto_waarde, height=800)

        tab2.subheader("Cumulatief Betaalde Belasting na Exit")
        tab2.line_chart(df_voor_cum_tax, height=800)

        tab3.subheader("Output v/d Modellen")
        tab3.dataframe(df, height=800)
        
        tab4.subheader("Box 2 model")
        tab4.dataframe(df_box2, height=800)
        
        tab5.subheader("Box 3 model")
        tab5.dataframe(df_box3, height=800)
    
with st.sidebar:
    header = st.columns([1,1])
    header[0].subheader('Item')
    header[1].subheader('Waarde')
    
    row1 = st.columns([1,1])
    row1[0].caption("Inflatie:")
    row1[1].caption(config['inflation'])
    
    row2 = st.columns([1,1])
    row2[0].caption("Box 2 - 1e schijf:")
    row2[1].caption(config['box2Rate_slice1'])

    row3 = st.columns([1,1])
    row3[0].caption("Box 2 - 2e schijf:")
    row3[1].caption(config['box2Rate_slice2'])
    
    row4 = st.columns([1,1])
    row4[0].caption("Box 2 - schijfgrens:")
    row4[1].caption(config['box2_slices_at'])
    
    row5 = st.columns([1,1])
    row5[0].caption("Vpb - 1e schijf:")
    row5[1].caption(config['vpbRate_slice1'])

    row6 = st.columns([1,1])
    row6[0].caption("Vpb - 2e schijf:")
    row6[1].caption(config['vpbRate_slice2'])
    
    row7 = st.columns([1,1])
    row7[0].caption("Vpb - schijfgrens:")
    row7[1].caption(config['vpb_slices_at'])
    
    row8 = st.columns([1,1])
    row8[0].caption("BV admin fee:")
    row8[1].caption(config['bv_fees'])
    
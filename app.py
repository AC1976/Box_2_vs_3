import streamlit as st
from Box2_model import Box2
from Box3_model import Box3

st.set_page_config(layout="wide")

st.title("Box 2 of Box 3")

with st.form('inputs', enter_to_submit=False):
    header = st.columns([1,1])
    header[0].subheader('Portefeuille (aanvang)')
    header[1].subheader('Rendement (per jaar in %)')
    
    row1 = st.columns([1,1])
    equity_amount = row1[0].number_input("Aandelen", min_value=0, value=100000, step=25000)
    equity_return = row1[1].slider("Waardestijging",float(0), float(0.2), float(0.06), step=0.01)
    
    row11 = st.columns([1,1])
    equity_dividend = row11[1].slider("Dividend",float(0), float(0.2), float(0.02), step=0.01)

    row2 = st.columns([1,1])
    bonds_amount = row2[0].number_input("Obligaties",min_value=0, value=100000, step=25000)
    bonds_return = row2[1].slider("Coupon",float(0), float(0.2), float(0.035), step=0.005)
    
    row3 = st.columns([1,1])
    property_amount = row3[0].number_input("Vastgoed",min_value=0, value=100000, step=25000)
    property_return = row3[1].slider("Huurrendement", float(0), float(0.2), float(0.06), step=0.005)

    row4 = st.columns([1,1])
    expense = row4[0].slider("Kosten BV", min_value=0, value=2500, step=500)
    inflatie = row4[1].slider("Inflatie", float(0), float(0.2), float(0.02), step=0.01)

    row44 = st.columns([1,1])
    getrouwd = row44[0].toggle("Getrouwd?")
    mtm = row44[1].toggle("Mark-to-market?")

    row6 = st.columns([1,1])
    termijn = row6[0].slider("Aantal jaar", int(0), int(50), int(20), step=1)
    submitted = row6[1].form_submit_button('Doorrekenen')
    
    if submitted:

        box_2 = Box2(initial_equity=equity_amount, initial_bonds=bonds_amount, initial_property=property_amount,
                    market_return_rate=equity_return,
                    dividend_yield=equity_dividend,
                    coupon=bonds_return,
                    rental_return=property_return,
                    fee_amount=expense,
                    inflation=inflatie,
                    partners=getrouwd,
                    mtm=mtm)
        
        ##box_2_df = box_2.run_model(termijn)
        ##box_2_df_chart = box_2.chart_data(termijn)

        box_3 = Box3(initial_equity=equity_amount, initial_bonds=bonds_amount, initial_property=property_amount,
                market_return_rate=equity_return,
                dividend_yield=equity_dividend,
                coupon=bonds_return,
                rental_return=property_return,
                inflation=inflatie,
                partners=getrouwd,
                )
        
        ##box_3_df = box_3.run_model(termijn)
        ##box_3_df_chart = box_2.chart_data(termijn)
        
    with st.container():
        
        tab1, tab2, tab3, tab4 = st.tabs(["🗃 Box 2", "🗃 Box 3", "Box 2 Chart", 'Box 3 Chart'])
        
        tab1.subheader("Box 2")
        tab1.dataframe(box_2.run_model(termijn), height=800)
        
        tab2.subheader("Box 3")
        tab2.dataframe(box_3.run_model(termijn), height=800)

        tab3.subheader("Box 2 chart")
        tab3.line_chart(box_2.chart_data(termijn-termijn))

        tab4.subheader("Box 3 chart")
        tab4.line_chart(box_3.chart_data(termijn-termijn))

    
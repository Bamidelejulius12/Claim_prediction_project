import streamlit as st
import pandas as pd

def customer_overview(claims_data):
    st.title("🏠 Customer Claims Overview")
    st.markdown("### Comprehensive view of insurance claims data and key metrics")
    
    # -------- Top KPIs --------
    st.subheader("📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        min_claim = claims_data['Ultimate_Claim_Amount'].min()
        st.metric(
            label="Lowest Claim Amount",
            value=f"${min_claim:,.2f}"
        )
    
    with col2:
        max_claim = claims_data['Ultimate_Claim_Amount'].max()
        st.metric(
            label="Highest Claim Amount",
            value=f"${max_claim:,.2f}"
        )
    
    with col3:
        youngest_driver = claims_data['Driver_age'].min()
        st.metric(
            label="Youngest Driver Age",
            value=f"{youngest_driver} yrs"
        )
    
    with col4:
        oldest_driver = claims_data['Driver_age'].max()
        st.metric(
            label="Oldest Driver Age",
            value=f"{oldest_driver} yrs"
        )

    st.markdown("---")

    # -------- Claim Type Analysis --------
    st.subheader("📋 Claim Type Analysis")
    
    claim_type_analysis = claims_data.groupby("Claim_Type").agg({
        'Estimated_Claim_Amount': ['sum', 'mean', 'count'],
        'Ultimate_Claim_Amount': ['sum', 'mean']
    }).round(2)
    
    claim_type_analysis.columns = ['Est_Total', 'Est_Avg', 'Claim_Count', 'Ult_Total', 'Ult_Avg']
    claim_type_analysis = claim_type_analysis.reset_index()
    
    # Display in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Claim Type Summary**")
        st.dataframe(
            claim_type_analysis,
            use_container_width=True,
            hide_index=True
        )
    
    with col2:
        st.markdown("**Key Insights**")
        
        highest_claim_type = claim_type_analysis.loc[claim_type_analysis['Ult_Total'].idxmax()]
        lowest_claim_type = claim_type_analysis.loc[claim_type_analysis['Ult_Total'].idxmin()]
        
        st.info(f"**Highest Cost Type**: {highest_claim_type['Claim_Type']} (${highest_claim_type['Ult_Total']:,.2f})")
        st.warning(f"**Lowest Cost Type**: {lowest_claim_type['Claim_Type']} (${lowest_claim_type['Ult_Total']:,.2f})")
        
        total_claims = claim_type_analysis['Claim_Count'].sum()
        st.success(f"**Total Claims Analyzed**: {total_claims:,}")

    st.markdown("---")

    # -------- Traffic & Weather Conditions --------
    st.subheader("🌦️ Environmental Conditions Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Traffic Condition Distribution**")
        traffic_counts = claims_data['Traffic_Condition'].value_counts()
        st.dataframe(
            traffic_counts.reset_index().rename(
                columns={'index': 'Traffic Condition', 'Traffic_Condition': 'Count'}
            ),
            use_container_width=True,
            hide_index=True
        )
    
    with col2:
        st.markdown("**Weather Condition Distribution**")
        weather_counts = claims_data['Weather_Condition'].value_counts()
        st.dataframe(
            weather_counts.reset_index().rename(
                columns={'index': 'Weather Condition', 'Weather_Condition': 'Count'}
            ),
            use_container_width=True,
            hide_index=True
        )

    st.markdown("---")

    # -------- Weather Impact Analysis --------
    st.subheader("📈 Weather Impact on Claims")
    
    weather_impact = claims_data.groupby("Weather_Condition").agg({
        'Estimated_Claim_Amount': ['sum', 'mean', 'count'],
        'Ultimate_Claim_Amount': ['sum', 'mean']
    }).round(2)
    
    weather_impact.columns = ['Est_Total', 'Est_Avg', 'Claim_Count', 'Ult_Total', 'Ult_Avg']
    weather_impact = weather_impact.reset_index().sort_values('Ult_Total', ascending=False)
    
    st.dataframe(
        weather_impact,
        use_container_width=True,
        hide_index=True
    )
    
    # Additional summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_estimated = claims_data['Estimated_Claim_Amount'].sum()
        st.metric("Total Estimated Claims", f"${total_estimated:,.2f}")
    
    with col2:
        total_ultimate = claims_data['Ultimate_Claim_Amount'].sum()
        st.metric("Total Ultimate Claims", f"${total_ultimate:,.2f}")
    
    with col3:
        avg_difference = ((total_ultimate - total_estimated) / total_estimated * 100)
        st.metric("Avg Difference", f"{avg_difference:+.1f}%")
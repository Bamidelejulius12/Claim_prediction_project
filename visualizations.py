import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def Customer_Visual(claims_data):
    st.title("📈 Data Visualizations")
    st.markdown("### Interactive charts and insights from claims data")
    
    # Visualization selection
    st.subheader("🎯 Select Visualization Type")
    
    viz_type = st.selectbox(
        "Choose a visualization:",
        [
            "Categorical Distributions",
            "Monthly Claims Trends", 
            "Claim Amount Analysis",
            "Driver Demographics"
        ],
        index=0
    )
    
    st.markdown("---")
    
    if viz_type == "Categorical Distributions":
        show_categorical_visualizations(claims_data)
    elif viz_type == "Monthly Claims Trends":
        show_monthly_trends(claims_data)
    elif viz_type == "Claim Amount Analysis":
        show_claim_amount_analysis(claims_data)
    elif viz_type == "Driver Demographics":
        show_driver_demographics(claims_data)

def show_categorical_visualizations(claims_data):
    st.subheader("📊 Categorical Data Distributions")
    
    # Create four charts
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Claims Data Distribution Analysis', fontsize=16, fontweight='bold')
    
    # Weather Condition
    weather_data = claims_data["Weather_Condition"].value_counts()
    bars1 = ax1.bar(weather_data.index, weather_data.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    ax1.set_title('Weather Condition Distribution', fontweight='bold')
    ax1.set_xlabel('Weather Type')
    ax1.set_ylabel('Number of Claims')
    ax1.tick_params(axis='x', rotation=45)
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom')
    
    # Traffic Condition
    traffic_data = claims_data["Traffic_Condition"].value_counts()
    bars2 = ax2.bar(traffic_data.index, traffic_data.values, color=['#FFA07A', '#20B2AA', '#778899'])
    ax2.set_title('Traffic Condition Distribution', fontweight='bold')
    ax2.set_xlabel('Traffic Condition')
    ax2.set_ylabel('Number of Claims')
    ax2.tick_params(axis='x', rotation=45)
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom')
    
    # Claim Type
    claim_data = claims_data["Claim_Type"].value_counts()
    bars3 = ax3.bar(claim_data.index, claim_data.values, color=['#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9'])
    ax3.set_title('Claim Type Distribution', fontweight='bold')
    ax3.set_xlabel('Claim Type')
    ax3.set_ylabel('Number of Claims')
    ax3.tick_params(axis='x', rotation=45)
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom')
    
    # Vehicle Type
    vehicle_data = claims_data["Vehicle_Type"].value_counts()
    bars4 = ax4.bar(vehicle_data.index, vehicle_data.values, color=['#F1948A', '#7FB3D5', '#76D7C4', '#F7DC6F'])
    ax4.set_title('Vehicle Type Distribution', fontweight='bold')
    ax4.set_xlabel('Vehicle Type')
    ax4.set_ylabel('Number of Claims')
    ax4.tick_params(axis='x', rotation=45)
    for bar in bars4:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Additional insights
    st.markdown("#### 📋 Distribution Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Most Common Weather**: {weather_data.index[0]} ({weather_data.iloc[0]} claims)")
        st.write(f"**Most Common Traffic**: {traffic_data.index[0]} ({traffic_data.iloc[0]} claims)")
    with col2:
        st.write(f"**Most Common Claim Type**: {claim_data.index[0]} ({claim_data.iloc[0]} claims)")
        st.write(f"**Most Common Vehicle**: {vehicle_data.index[0]} ({vehicle_data.iloc[0]} claims)")

def show_monthly_trends(claims_data):
    st.subheader("📈 Monthly Claims & Settlements Trends")
    
    # Prepare data
    claims_data['Accident_Date'] = pd.to_datetime(claims_data['Accident_Date'])
    claims_data['Settlement_Date'] = pd.to_datetime(claims_data['Settlement_Date'])
    claims_data['Accident_YearMonth'] = claims_data['Accident_Date'].dt.strftime('%Y-%m')
    claims_data['Settlement_YearMonth'] = claims_data['Settlement_Date'].dt.strftime('%Y-%m')
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Monthly claims
    monthly_claims = claims_data.groupby('Accident_YearMonth').size()
    ax1.plot(monthly_claims.index.astype(str), monthly_claims.values, 
             marker='o', linewidth=2.5, color='#E74C3C', markersize=6)
    ax1.set_title("Monthly Claims Frequency", fontweight='bold', fontsize=14)
    ax1.set_xlabel("Year-Month")
    ax1.set_ylabel("Number of Claims")
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    ax1.fill_between(monthly_claims.index.astype(str), monthly_claims.values, alpha=0.3, color='#E74C3C')
    
    # Monthly settlements
    settlement_permonth = claims_data.groupby('Settlement_YearMonth').size()
    ax2.plot(settlement_permonth.index.astype(str), settlement_permonth.values, 
             marker='s', linewidth=2.5, color='#3498DB', markersize=6)
    ax2.set_title("Monthly Settlements Frequency", fontweight='bold', fontsize=14)
    ax2.set_xlabel("Year-Month")
    ax2.set_ylabel("Number of Settlements")
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)
    ax2.fill_between(settlement_permonth.index.astype(str), settlement_permonth.values, alpha=0.3, color='#3498DB')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Trend analysis
    st.markdown("#### 📊 Trend Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        claim_growth = ((monthly_claims.iloc[-1] - monthly_claims.iloc[0]) / monthly_claims.iloc[0]) * 100
        st.metric("Claims Growth", f"{monthly_claims.iloc[-1]}", 
                 delta=f"{claim_growth:+.1f}%")
    
    with col2:
        settlement_growth = ((settlement_permonth.iloc[-1] - settlement_permonth.iloc[0]) / settlement_permonth.iloc[0]) * 100
        st.metric("Settlements Growth", f"{settlement_permonth.iloc[-1]}", 
                 delta=f"{settlement_growth:+.1f}%")

def show_claim_amount_analysis(claims_data):
    st.subheader("💰 Claim Amount Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Histogram of claim amounts
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        ax1.hist(claims_data['Ultimate_Claim_Amount'], bins=30, alpha=0.7, color='#2E86C1', edgecolor='black')
        ax1.set_title('Distribution of Ultimate Claim Amounts', fontweight='bold')
        ax1.set_xlabel('Claim Amount ($)')
        ax1.set_ylabel('Frequency')
        ax1.grid(True, alpha=0.3)
        st.pyplot(fig1)
    
    with col2:
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.hist(claims_data['Estimated_Claim_Amount'], bins=30, alpha=0.7, color='#2E86C1', edgecolor='black')
        ax2.set_title('Distribution of Ultimate Claim Amounts', fontweight='bold')
        ax2.set_xlabel('Claim Amount ($)')
        ax2.set_ylabel('Frequency')
        ax2.grid(True, alpha=0.3)
        st.pyplot(fig2)
    
    # Statistical summary
    st.markdown("#### 📋 Statistical Summary")
    col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
    
    with col_stats1:
        st.metric("Mean", f"${claims_data['Ultimate_Claim_Amount'].mean():,.2f}")
    with col_stats2:
        st.metric("Median", f"${claims_data['Ultimate_Claim_Amount'].median():,.2f}")
    with col_stats3:
        st.metric("Std Dev", f"${claims_data['Ultimate_Claim_Amount'].std():,.2f}")
    with col_stats4:
        st.metric("Total", f"${claims_data['Ultimate_Claim_Amount'].sum():,.2f}")

def show_driver_demographics(claims_data):
    st.subheader("👥 Driver Demographics Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Driver age distribution
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        ax1.hist(claims_data['Driver_age'], bins=20, alpha=0.7, color='#27AE60', edgecolor='black')
        ax1.set_title('Driver Age Distribution', fontweight='bold')
        ax1.set_xlabel('Driver Age')
        ax1.set_ylabel('Frequency')
        ax1.grid(True, alpha=0.3)
        st.pyplot(fig1)
    
    with col2:
        # License age vs claim amount scatter
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.scatter(claims_data['License_age'], claims_data['Ultimate_Claim_Amount'], 
                   alpha=0.6, color='#8E44AD')
        ax2.set_title('License Age vs Claim Amount', fontweight='bold')
        ax2.set_xlabel('License Age (years)')
        ax2.set_ylabel('Claim Amount ($)')
        ax2.grid(True, alpha=0.3)
        st.pyplot(fig2)
    
    # Demographic insights
    st.markdown("#### 📊 Demographic Insights")
    col_insight1, col_insight2 = st.columns(2)
    
    with col_insight1:
        avg_driver_age = claims_data['Driver_age'].mean()
        st.metric("Average Driver Age", f"{avg_driver_age:.1f} years")
    
    with col_insight2:
        avg_license_age = claims_data['License_age'].mean()
        st.metric("Average License Age", f"{avg_license_age:.1f} years")
    
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page config
st.set_page_config(
    page_title="Math Model Evaluation Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define data for each section
abstract_algebra_data = pd.DataFrame({
    'Metric': ['Correctness', 'Mathematical Reasoning', 'Solution Completeness', 
               'Explanation Quality', 'Coherence', 'Time Efficiency', 'Final Score'],
    'GPT4': [0.83, 0.40, 0.425, 0.65, 0.675, 0.90, 0.71],
    'TinyLlama': [0.00, 0.10, 0.00, 0.10, 0.00, 0.30, 0.05],
    'Difference': [0.83, 0.30, 0.425, 0.55, 0.675, 0.60, 0.66]
})

college_math_data = pd.DataFrame({
    'Metric': ['Correctness', 'Mathematical Reasoning', 'Solution Completeness', 
               'Explanation Quality', 'Coherence', 'Time Efficiency', 'Final Score'],
    'GPT4': [0.85, 0.70, 0.45, 0.50, 0.45, 0.85, 0.74],
    'TinyLlama': [0.35, 0.05, 0.05, 0.10, 0.05, 0.70, 0.18],
    'Difference': [0.50, 0.65, 0.40, 0.40, 0.40, 0.15, 0.56]
})

elementary_math_data = pd.DataFrame({
    'Metric': ['Correctness', 'Mathematical Reasoning', 'Solution Completeness', 
               'Explanation Quality', 'Coherence', 'Time Efficiency', 'Final Score'],
    'GPT4': [0.80, 0.55, 0.35, 0.40, 0.30, 0.90, 0.59],
    'TinyLlama': [0.30, 0.05, 0.02, 0.05, 0.02, 0.65, 0.19],
    'Difference': [0.50, 0.50, 0.33, 0.35, 0.28, 0.25, 0.40]
})

high_school_math_data = pd.DataFrame({
    'Metric': ['Correctness', 'Mathematical Reasoning', 'Solution Completeness', 
               'Explanation Quality', 'Coherence', 'Time Efficiency', 'Final Score'],
    'GPT4': [0.85, 0.75, 0.40, 0.45, 0.35, 0.85, 0.76],
    'TinyLlama': [0.40, 0.10, 0.05, 0.08, 0.05, 0.65, 0.26],
    'Difference': [0.45, 0.65, 0.35, 0.37, 0.30, 0.20, 0.50]
})

overall_metrics = pd.DataFrame({
    'Metric': ['Correctness', 'Mathematical Reasoning', 'Solution Completeness', 
               'Explanation Quality', 'Coherence', 'Time Efficiency', 'Final Score'],
    'GPT4': [0.833, 0.628, 0.388, 0.449, 0.363, 0.880, 0.684],
    'TinyLlama': [0.317, 0.047, 0.029, 0.055, 0.032, 0.658, 0.183],
    'Difference': [0.517, 0.581, 0.360, 0.393, 0.331, 0.222, 0.501]
})

def create_metrics_table(data, title):
    st.subheader(title)
    formatted_df = data.copy()
    for col in ['GPT4', 'TinyLlama', 'Difference']:
        formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:.3f}")
        if col == 'Difference':
            formatted_df[col] = formatted_df[col].apply(lambda x: f"+{x}" if float(x) > 0 else x)
    st.dataframe(formatted_df, hide_index=True, use_container_width=True)

def create_radar_chart(data, title):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=data['GPT4'][:-1],
        theta=data['Metric'][:-1],
        fill='toself',
        name='GPT-4'
    ))
    fig.add_trace(go.Scatterpolar(
        r=data['TinyLlama'][:-1],
        theta=data['Metric'][:-1],
        fill='toself',
        name='TinyLlama'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title=title
    )
    st.plotly_chart(fig, use_container_width=True)

def create_bar_chart(data, title):
    fig = go.Figure(data=[
        go.Bar(name='GPT-4', x=data['Metric'], y=data['GPT4']),
        go.Bar(name='TinyLlama', x=data['Metric'], y=data['TinyLlama'])
    ])
    fig.update_layout(
        title=title,
        xaxis_title="Metrics",
        yaxis_title="Score",
        barmode='group',
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)

# Main app layout
st.title("Math Model Evaluation Dashboard")

tabs = st.tabs([
    "Subject Performance",
    "Detailed Analysis"
])

with tabs[0]:
    # Summary of performance across subjects
    st.header("Performance Across Subjects")
    
    subjects_summary = pd.DataFrame({
        'Subject': ['Abstract Algebra', 'College Mathematics', 'Elementary Mathematics', 'High School Mathematics'],
        'GPT4': [0.71, 0.74, 0.59, 0.76],
        'TinyLlama': [0.05, 0.18, 0.19, 0.26]
    })
    
    fig = go.Figure(data=[
        go.Bar(name='GPT-4', x=subjects_summary['Subject'], y=subjects_summary['GPT4']),
        go.Bar(name='TinyLlama', x=subjects_summary['Subject'], y=subjects_summary['TinyLlama'])
    ])
    fig.update_layout(
        title="Model Performance by Subject",
        xaxis_title="Subject",
        yaxis_title="Score",
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Overall metrics
    st.header("Overall Performance Metrics")
    create_metrics_table(overall_metrics, "")
    create_radar_chart(overall_metrics, "Overall Performance Radar")

with tabs[1]:
    subject_tabs = st.tabs([
        "Abstract Algebra",
        "College Mathematics",
        "Elementary Mathematics",
        "High School Mathematics"
    ])
    
    with subject_tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            create_metrics_table(abstract_algebra_data, "Abstract Algebra Metrics")
        with col2:
            create_radar_chart(abstract_algebra_data, "Abstract Algebra Performance Radar")
        create_bar_chart(abstract_algebra_data, "Abstract Algebra Performance Comparison")
    
    with subject_tabs[1]:
        col1, col2 = st.columns(2)
        with col1:
            create_metrics_table(college_math_data, "College Mathematics Metrics")
        with col2:
            create_radar_chart(college_math_data, "College Mathematics Performance Radar")
        create_bar_chart(college_math_data, "College Mathematics Performance Comparison")
    
    with subject_tabs[2]:
        col1, col2 = st.columns(2)
        with col1:
            create_metrics_table(elementary_math_data, "Elementary Mathematics Metrics")
        with col2:
            create_radar_chart(elementary_math_data, "Elementary Mathematics Performance Radar")
        create_bar_chart(elementary_math_data, "Elementary Mathematics Performance Comparison")
    
    with subject_tabs[3]:
        col1, col2 = st.columns(2)
        with col1:
            create_metrics_table(high_school_math_data, "High School Mathematics Metrics")
        with col2:
            create_radar_chart(high_school_math_data, "High School Mathematics Performance Radar")
        create_bar_chart(high_school_math_data, "High School Mathematics Performance Comparison")

# Footer
st.markdown("---")
st.markdown("Dashboard created to visualize model evaluation results and compare model performance")

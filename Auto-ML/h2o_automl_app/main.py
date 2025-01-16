import streamlit as st
import h2o
from h2o.automl import H2OAutoML
import pandas as pd
import os
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import shutil

# Define persistent storage paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'h2o_storage'))
MODEL_DIR = os.path.join(BASE_DIR, 'models')
REGISTRY_FILE = os.path.join(BASE_DIR, 'model_registry.json')

def init_h2o():
    """Initialize H2O and create necessary directories"""
    try:
        if not h2o.connection():
            h2o.init()
        
        # Create directories if they don't exist
        os.makedirs(MODEL_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(REGISTRY_FILE), exist_ok=True)
        
        if not os.path.exists(REGISTRY_FILE):
            with open(REGISTRY_FILE, 'w') as f:
                json.dump({}, f)
    except Exception as e:
        st.error(f"Error initializing H2O: {str(e)}")
        return False
    return True

def validate_model_name(name):
    """Validate model name for filesystem compatibility and uniqueness"""
    if not name:
        return False, "Model name cannot be empty"
    
    # Check for invalid characters
    invalid_chars = '<>:"/\\|?*'
    if any(char in name for char in invalid_chars):
        return False, f"Model name cannot contain any of these characters: {invalid_chars}"
    
    # Check if name already exists
    try:
        with open(REGISTRY_FILE, 'r') as f:
            registry = json.load(f)
            if name in registry:
                return False, "A model with this name already exists"
    except:
        pass
    
    return True, ""

def delete_model(model_name):
    """Delete a model and its registry entry"""
    try:
        # Load registry
        with open(REGISTRY_FILE, 'r') as f:
            registry = json.load(f)
        
        if model_name not in registry:
            return False, "Model not found in registry"
        
        # Delete model files
        model_path = os.path.dirname(registry[model_name]['path'])
        if os.path.exists(model_path):
            shutil.rmtree(model_path)
        
        # Remove from registry
        del registry[model_name]
        
        # Save updated registry
        with open(REGISTRY_FILE, 'w') as f:
            json.dump(registry, f)
        
        return True, "Model deleted successfully"
    except Exception as e:
        return False, f"Error deleting model: {str(e)}"

def describe_model_performance(metrics):
    """Convert technical metrics into user-friendly descriptions"""
    descriptions = []
    
    if 'r2' in metrics and metrics['r2'] is not None:
        r2_percentage = max(0, metrics['r2'] * 100)
        if r2_percentage >= 90:
            quality = "excellent"
        elif r2_percentage >= 70:
            quality = "good"
        elif r2_percentage >= 50:
            quality = "moderate"
        else:
            quality = "limited"
        descriptions.append(f"The model shows {quality} performance, explaining {r2_percentage:.1f}% of the variation in the data.")
    
    if 'accuracy' in metrics and metrics['accuracy'] is not None:
        acc_percentage = metrics['accuracy'] * 100
        descriptions.append(f"The model achieves {acc_percentage:.1f}% prediction accuracy.")
    
    if descriptions:
        return " ".join(descriptions)
    return "Model performance metrics are not available."

def analyze_column_types(df):
    """Analyze and store column types for future validation"""
    column_types = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            column_types[col] = 'numeric'
        else:
            column_types[col] = 'categorical'
    return column_types

def create_visualizations(actual, predicted, problem_type):
    """Create performance visualizations"""
    figs = []
    
    if problem_type == 'regression':
        # Create subplot for regression analysis
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Actual vs Predicted Values', 'Prediction Errors Distribution'),
            vertical_spacing=0.15
        )
        
        # Actual vs Predicted scatter plot
        fig.add_trace(
            go.Scatter(
                x=actual,
                y=predicted,
                mode='markers',
                marker=dict(
                    color=actual,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title='Actual Values')
                ),
                name='Predictions'
            ),
            row=1, col=1
        )
        
        # Add diagonal line for perfect predictions
        min_val = min(min(actual), min(predicted))
        max_val = max(max(actual), max(predicted))
        fig.add_trace(
            go.Scatter(
                x=[min_val, max_val],
                y=[min_val, max_val],
                mode='lines',
                line=dict(color='red', dash='dash'),
                name='Perfect Prediction'
            ),
            row=1, col=1
        )
        
        # Add residuals histogram
        residuals = actual - predicted
        fig.add_trace(
            go.Histogram(
                x=residuals,
                nbinsx=30,
                marker_color='rgb(55, 83, 109)',
                name='Error Distribution'
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            height=800,
            showlegend=True,
            title_text="Model Performance Analysis",
            template='plotly_white'
        )
        
        figs.append(fig)
        
    else:  # Classification
        # Confusion Matrix
        conf_matrix = pd.crosstab(actual, predicted)
        fig_cm = px.imshow(
            conf_matrix,
            labels=dict(x="Predicted", y="Actual"),
            title='Confusion Matrix',
            color_continuous_scale='RdYlBu',
            aspect='auto'
        )
        
        fig_cm.update_layout(
            template='plotly_white',
            height=600,
            width=600
        )
        
        figs.append(fig_cm)
    
    return figs
def manage_models():
    """Add a model management section"""
    st.header("Model Management")
    
    try:
        with open(REGISTRY_FILE, 'r') as f:
            registry = json.load(f)
    except:
        st.warning("No models found in registry.")
        return
    
    if not registry:
        st.warning("No models available to manage.")
        return
    
    # Display model list with delete buttons
    st.write("### Available Models")
    
    for model_name in registry:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{model_name}**")
            st.write(f"Created: {registry[model_name]['timestamp']}")
            st.write(f"Problem Type: {registry[model_name]['problem_type']}")
        with col2:
            if st.button("Delete", key=f"delete_{model_name}", type="secondary"):
                if st.session_state.get('confirm_delete') != model_name:
                    st.session_state.confirm_delete = model_name
                    st.warning(f"Are you sure you want to delete {model_name}? Click delete again to confirm.")
                else:
                    success, message = delete_model(model_name)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                    st.session_state.confirm_delete = None

def train_model():
    st.header("Train New Model")
    
    uploaded_file = st.file_uploader("Upload training dataset (CSV)", type=['csv'])
    if not uploaded_file:
        return
    
    try:
        # Read and display data
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:", df.head())
        
        # Model configuration
        target = st.selectbox("Select target variable", df.columns)
        
        # Initialize session state for model naming if not exists
        if 'custom_model_name' not in st.session_state:
            st.session_state.custom_model_name = ""
        
        # Model naming with better UX
        model_name = st.text_input(
            "Model Name",
            value=st.session_state.custom_model_name,
            placeholder="Enter a descriptive name (e.g., sales_predictor_v1)",
            help="Enter a unique name for your model. Use letters, numbers, and underscores."
        )
        
        # Update session state
        st.session_state.custom_model_name = model_name
        
        # Generate default name if empty
        if not model_name.strip():
            model_name = f"model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            st.info(f"No name provided. Using default name: {model_name}")
        
        # Validate model name
        is_valid, error_message = validate_model_name(model_name)
        if not is_valid:
            st.error(error_message)
            return
        
        # Training parameters
        col1, col2 = st.columns(2)
        with col1:
            max_runtime = st.slider("Maximum runtime (minutes)", 1, 30, 10)
            train_size = st.slider("Training data size (%)", 50, 90, 80)
        with col2:
            max_models = st.number_input("Maximum number of models", 1, 20, 5)
        
        if not st.button("Train Model"):
            return
        
        with st.spinner("Training model... This may take a few minutes."):
            # Analyze column types
            column_types = analyze_column_types(df)
            features = [col for col in df.columns if col != target]
            
            # Convert to H2O frame and split data
            hf = h2o.H2OFrame(df)
            train, valid, test = hf.split_frame([train_size/100, (100-train_size)/2/100])
            
            # Determine problem type
            problem_type = 'regression' if pd.api.types.is_numeric_dtype(df[target]) else 'classification'
            
            # Train AutoML
            aml = H2OAutoML(
                max_runtime_secs=max_runtime*60,
                max_models=max_models,
                seed=1
            )
            
            aml.train(x=features, y=target, training_frame=train, validation_frame=valid)
            
            # Save model
            model_path = os.path.join(MODEL_DIR, model_name)
            os.makedirs(model_path, exist_ok=True)
            saved_path = h2o.save_model(aml.leader, path=model_path, force=True)
            
            # Get performance metrics
            perf = aml.leader.model_performance(test)
            metrics = {
                'r2': float(perf.r2()) if problem_type == 'regression' else None,
                'rmse': float(perf.rmse()) if problem_type == 'regression' else None,
                'mae': float(perf.mae()) if problem_type == 'regression' else None,
                'accuracy': float(perf.accuracy()) if problem_type == 'classification' else None
            }
            
            # Save to registry
            registry_data = {
                'path': saved_path,
                'target': target,
                'features': features,
                'column_types': column_types,
                'problem_type': problem_type,
                'metrics': metrics,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            with open(REGISTRY_FILE, 'r') as f:
                registry = json.load(f)
            
            registry[model_name] = registry_data
            with open(REGISTRY_FILE, 'w') as f:
                json.dump(registry, f)
            
            # Clear the custom name after successful training
            st.session_state.custom_model_name = ""
            
            # Display results
            st.success(f"Model '{model_name}' trained successfully!")
            st.info(describe_model_performance(metrics))
            st.write("Technical Metrics:", metrics)
            
            # Show leaderboard
            st.write("Model Leaderboard:")
            leaderboard_df = aml.leaderboard.as_data_frame()
            st.dataframe(leaderboard_df.style.highlight_max(axis=0, color='lightgreen'))
            
    except Exception as e:
        st.error(f"Error during training: {str(e)}")
        import traceback
        st.error(f"Detailed error: {traceback.format_exc()}")

def predict():
    st.header("Make Predictions")
    
    try:
        with open(REGISTRY_FILE, 'r') as f:
            registry = json.load(f)
    except Exception as e:
        st.warning("No models found. Please train a model first.")
        return
    
    if not registry:
        st.warning("No models available. Please train a model first.")
        return
    
    model_name = st.selectbox("Select Model", list(registry.keys()))
    model_info = registry[model_name]
    
    st.write("Model Information:")
    display_info = {k: v for k, v in model_info.items() if k != 'path'}
    st.json(display_info)
    
    uploaded_file = st.file_uploader("Upload test dataset (CSV)", type=['csv'])
    if not uploaded_file:
        return
    
    try:
        # Read test data
        test_df = pd.read_csv(uploaded_file)
        st.write("Test Data Preview:", test_df.head())
        
        # Validate required features
        missing_features = [col for col in model_info['features'] if col not in test_df.columns]
        if missing_features:
            st.error(f"Missing required features: {', '.join(missing_features)}")
            return
        
        # Validate data types and convert if necessary
        for col in model_info['features']:
            expected_type = model_info['column_types'][col]
            if expected_type == 'numeric':
                try:
                    test_df[col] = pd.to_numeric(test_df[col], errors='coerce')
                except Exception as e:
                    st.error(f"Could not convert column '{col}' to numeric type: {str(e)}")
                    return
                
                # Check for NaN values after conversion
                if test_df[col].isna().any():
                    st.warning(f"Column '{col}' contains invalid numeric values that were converted to NaN")
            
            elif expected_type == 'categorical':
                test_df[col] = test_df[col].astype(str)
        
        if st.button("Generate Predictions"):
            # Convert to H2O frame
            test_h2o = h2o.H2OFrame(test_df)
            
            # Load model and make predictions
            model = h2o.load_model(model_info['path'])
            preds = model.predict(test_h2o)
            
            # Prepare results
            result_df = test_df.copy()
            preds_df = h2o.as_list(preds)
            result_df['predicted_value'] = preds_df['predict']
            
            # Save predictions
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(BASE_DIR, f'predictions_{timestamp}.csv')
            result_df.to_csv(output_path, index=False)
            
            st.success("Predictions generated successfully!")
            
            # Display predictions preview
            st.write("Predictions Preview:")
            numeric_cols = result_df.select_dtypes(include=['float64', 'int64']).columns
            styled_df = result_df.head().style.highlight_max(subset=numeric_cols, axis=1, color='lightgreen')
            st.dataframe(styled_df)
            
            # Create visualizations if target exists in test data
            if model_info['target'] in test_df.columns:
                st.write("### Prediction Analysis")
                figs = create_visualizations(
                    test_df[model_info['target']],
                    preds_df['predict'],
                    model_info['problem_type']
                )
                
                for fig in figs:
                    st.plotly_chart(fig, use_container_width=True)
            
            # Download button
            with open(output_path, 'rb') as f:
                st.download_button(
                    label="Download Predictions",
                    data=f,
                    file_name=f'predictions_{timestamp}.csv',
                    mime='text/csv'
                )
            
    except Exception as e:
        st.error(f"Error during prediction: {str(e)}")
        import traceback
        st.error(f"Detailed error: {traceback.format_exc()}")

def main():
    st.set_page_config(page_title="H2O AutoML Dashboard", layout="wide")
    
    # Custom styling
    st.markdown("""
        <style>
        .stApp {
            background-color: #f5f7f9;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        .stProgress .st-bo {
            background-color: #4CAF50;
        }
        .delete-button>button {
            background-color: #ff4444;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("H2O AutoML Dashboard")
    
    # Initialize H2O
    if not init_h2o():
        st.error("Failed to initialize H2O. Please restart the application.")
        return
    
    # Updated navigation
    page = st.sidebar.radio("Navigation", ["Train Model", "Make Predictions", "Manage Models"])
    
    if page == "Train Model":
        train_model()
    elif page == "Make Predictions":
        predict()
    else:
        manage_models()
    
    # Debug information
    if st.sidebar.checkbox("Show Debug Info"):
        st.sidebar.write("Model Directory:", MODEL_DIR)
        st.sidebar.write("Registry File:", REGISTRY_FILE)
        if os.path.exists(REGISTRY_FILE):
            with open(REGISTRY_FILE, 'r') as f:
                st.sidebar.json(json.load(f))

if __name__ == "__main__":
    main()

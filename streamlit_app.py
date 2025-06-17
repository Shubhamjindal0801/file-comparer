#!/usr/bin/env python3

import streamlit as st
import tempfile
import os
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from document_diff import EnhancedDocumentComparer
import json
from datetime import datetime
import time
import hashlib

# Page configuration
st.set_page_config(
    page_title="Enhanced Document Comparison Tool",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add meta tags to prevent caching
st.markdown("""
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
""", unsafe_allow_html=True)

# Custom CSS with cache busting
def load_css():
    # Create a cache-busting hash based on current time
    cache_buster = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
    
    css = f"""
    <style data-version="{cache_buster}">
        /* Cache buster: {cache_buster} */
        .main-header {{
            font-size: 2.5rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: bold;
        }}
        .comparison-card {{
            background-color: #e8f4fd;
            padding: 1.5rem;
            border-radius: 0.8rem;
            margin: 1rem 0;
            border: 2px solid #1f77b4;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .metric-card {{
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 0.8rem;
            border: 2px solid #ddd;
            margin: 0.5rem;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .similarity-high {{ 
            color: #155724; 
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }}
        .similarity-medium {{ 
            color: #856404; 
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }}
        .similarity-low {{ 
            color: #721c24; 
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }}
        .diff-addition {{
            background-color: #c3e6cb !important;
            border: 2px solid #28a745 !important;
            color: #155724 !important;
            font-weight: 500 !important;
        }}
        .diff-deletion {{
            background-color: #f5c6cb !important;
            border: 2px solid #dc3545 !important;
            color: #721c24 !important;
            font-weight: 500 !important;
        }}
        .diff-change {{
            background-color: #ffeaa7 !important;
            border: 2px solid #ffc107 !important;
            color: #856404 !important;
            font-weight: 500 !important;
        }}
        .similarity-display {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
        }}
        .refresh-btn {{
            background-color: #28a745;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.3rem;
            cursor: pointer;
            font-weight: bold;
        }}
        .refresh-btn:hover {{
            background-color: #218838;
        }}
    </style>
    """
    return css

# Load CSS with cache busting
st.markdown(load_css(), unsafe_allow_html=True)

class StreamlitDocumentComparer:
    def __init__(self):
        self.comparer = EnhancedDocumentComparer()
        
    def main(self):
        # Initialize session state for refresh
        if 'last_refresh' not in st.session_state:
            st.session_state.last_refresh = time.time()
        
        # Header with refresh button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("🔄 Refresh UI", help="Click to refresh the user interface and apply latest changes"):
                st.session_state.last_refresh = time.time()
                st.rerun()
        
        with col2:
            st.markdown('<h1 class="main-header">📄 Enhanced Document Comparison Tool</h1>', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"<small>Last updated: {datetime.fromtimestamp(st.session_state.last_refresh).strftime('%H:%M:%S')}</small>", unsafe_allow_html=True)
        
        # Force CSS reload on refresh
        if time.time() - st.session_state.last_refresh < 1:
            st.markdown(load_css(), unsafe_allow_html=True)
        
        # Sidebar configuration
        with st.sidebar:
            st.header("⚙️ Configuration")
            
            algorithm = st.selectbox(
                "Comparison Algorithm",
                options=['unified', 'context', 'levenshtein', 'jaro_winkler', 'semantic'],
                help="Choose the algorithm for document comparison"
            )
            
            export_formats = st.multiselect(
                "Export Formats",
                options=['docx', 'html', 'json', 'markdown'],
                default=['docx'],
                help="Select formats to export the comparison results"
            )
            
            st.markdown("---")
            st.markdown("### 🔧 Advanced Options")
            
            show_metadata = st.checkbox("Show File Metadata", value=True)
            show_statistics = st.checkbox("Show Statistics", value=True)
            show_visualizations = st.checkbox("Show Visualizations", value=True)
            max_differences = st.slider("Max Differences to Display", 10, 500, 100)
            
            st.markdown("---")
            st.markdown("### 🛠️ Developer Options")
            
            auto_refresh = st.checkbox("Auto-refresh UI", value=False, help="Automatically refresh the UI every 5 seconds")
            
            if auto_refresh:
                time.sleep(5)
                st.rerun()
            
            if st.button("🧹 Clear Cache", help="Clear browser cache and refresh"):
                st.cache_data.clear()
                st.session_state.clear()
                st.rerun()
        
        # Main content area
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📁 File 1")
            file1 = st.file_uploader(
                "Choose first document",
                type=['docx', 'pdf', 'txt'],
                key="file1",
                help="Upload the first document for comparison"
            )
            
            if file1:
                st.success(f"✅ {file1.name} uploaded successfully")
                file1_details = {
                    "Name": file1.name,
                    "Size": f"{file1.size:,} bytes",
                    "Type": file1.type
                }
                if show_metadata:
                    st.json(file1_details)
        
        with col2:
            st.subheader("🗂️ File 2")
            file2 = st.file_uploader(
                "Choose second document",
                type=['docx', 'pdf', 'txt'],
                key="file2",
                help="Upload the second document for comparison"
            )
            
            if file2:
                st.success(f"✅ {file2.name} uploaded successfully")
                file2_details = {
                    "Name": file2.name,
                    "Size": f"{file2.size:,} bytes",
                    "Type": file2.type
                }
                if show_metadata:
                    st.json(file2_details)
        
        # Comparison button
        if file1 and file2:
            st.markdown("---")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔍 Compare Documents", type="primary", use_container_width=True):
                    self.compare_documents(file1, file2, algorithm, export_formats, 
                                         show_statistics, show_visualizations, max_differences)
        
        # Help section
        with st.expander("ℹ️ How to Use"):
            st.markdown("""
            1. **Upload Files**: Use the file uploaders to select two documents for comparison
            2. **Choose Algorithm**: Select comparison algorithm from the sidebar
            3. **Configure Options**: Set export formats and display options
            4. **Compare**: Click the "Compare Documents" button to start analysis
            5. **Review Results**: View statistics, visualizations, and detailed differences
            6. **Export**: Download results in your preferred format(s)
            
            **Supported Formats**: DOCX, PDF, TXT
            
            **Algorithms**:
            - **Unified**: Standard line-by-line comparison
            - **Context**: Shows more context around changes
            - **Levenshtein**: Character-level edit distance
            - **Jaro-Winkler**: String similarity algorithm
            - **Semantic**: Multiple semantic similarity metrics
            """)
    
    def compare_documents(self, file1, file2, algorithm, export_formats, 
                         show_statistics, show_visualizations, max_differences):
        """Perform document comparison and display results"""
        
        with st.spinner("🔄 Processing documents..."):
            try:
                # Save uploaded files to temporary locations
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file1.name).suffix) as tmp1:
                    tmp1.write(file1.getvalue())
                    tmp1_path = tmp1.name
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file2.name).suffix) as tmp2:
                    tmp2.write(file2.getvalue())
                    tmp2_path = tmp2.name
                
                # Perform comparison
                results = self.comparer.compare_documents(tmp1_path, tmp2_path, algorithm)
                
                # Display results
                self.display_results(results, show_statistics, show_visualizations, max_differences)
                
                # Generate exports
                self.generate_exports(results, export_formats, file1.name, file2.name)
                
                # Cleanup temporary files
                os.unlink(tmp1_path)
                os.unlink(tmp2_path)
                
            except Exception as e:
                st.error(f"❌ Error during comparison: {str(e)}")
                st.exception(e)
    
    def display_results(self, results, show_statistics, show_visualizations, max_differences):
        """Display comparison results with rich formatting"""
        
        st.markdown("---")
        st.header("📊 Comparison Results")
        
        # Similarity score (prominent display)
        similarity = results['statistics'].get('similarity_percentage', 0)
        
        if similarity > 80:
            similarity_class = "similarity-high"
            emoji = "🟢"
        elif similarity > 50:
            similarity_class = "similarity-medium"
            emoji = "🟡"
        else:
            similarity_class = "similarity-low"
            emoji = "🔴"
        
        st.markdown(f"""
        <div class="similarity-display" style="text-align: center; padding: 2.5rem; border-radius: 1rem; margin: 1rem 0; box-shadow: 0 6px 12px rgba(0,0,0,0.15);">
            <h2 style="margin: 0; font-size: 1.8rem;">{emoji} Overall Similarity</h2>
            <h1 style="font-size: 4rem; margin: 0.5rem 0; font-weight: bold;">{similarity:.1f}%</h1>
            <p style="margin: 0; font-size: 1.2rem; opacity: 0.9;">Document Comparison Score</p>
        </div>
        """, unsafe_allow_html=True)
        
        if show_statistics:
            self.display_statistics(results)
        
        if show_visualizations:
            self.display_visualizations(results)
        
        # Display differences
        self.display_differences(results, max_differences)
    
    def display_statistics(self, results):
        """Display detailed statistics"""
        
        st.subheader("📈 Document Statistics")
        
        stats = results['statistics']
        
        # Create metrics columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Characters (File 1)",
                f"{stats['text1']['characters']:,}",
                delta=None
            )
        
        with col2:
            st.metric(
                "Characters (File 2)",
                f"{stats['text2']['characters']:,}",
                delta=f"{stats['text2']['characters'] - stats['text1']['characters']:+,}"
            )
        
        with col3:
            st.metric(
                "Words (File 1)",
                f"{stats['text1']['words']:,}",
                delta=None
            )
        
        with col4:
            st.metric(
                "Words (File 2)",
                f"{stats['text2']['words']:,}",
                delta=f"{stats['text2']['words'] - stats['text1']['words']:+,}"
            )
        
        # Changes summary
        changes = stats['differences']
        if changes['total_changes'] > 0:
            st.subheader("🔄 Changes Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Changes", changes['total_changes'])
            with col2:
                st.metric("Additions", changes['additions'], delta=changes['additions'], delta_color="normal")
            with col3:
                st.metric("Deletions", changes['deletions'], delta=-changes['deletions'], delta_color="inverse")
            with col4:
                st.metric("Modifications", changes['modifications'])
    
    def display_visualizations(self, results):
        """Display interactive visualizations"""
        
        st.subheader("📊 Visual Analysis")
        
        stats = results['statistics']
        
        # Document comparison chart
        fig_comparison = go.Figure(data=[
            go.Bar(name='File 1', x=['Characters', 'Words', 'Lines'], 
                   y=[stats['text1']['characters'], stats['text1']['words'], stats['text1']['lines']],
                   marker_color='#1f77b4'),
            go.Bar(name='File 2', x=['Characters', 'Words', 'Lines'], 
                   y=[stats['text2']['characters'], stats['text2']['words'], stats['text2']['lines']],
                   marker_color='#ff7f0e')
        ])
        
        fig_comparison.update_layout(
            title="Document Size Comparison",
            xaxis_title="Metrics",
            yaxis_title="Count",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Changes pie chart
        changes = stats['differences']
        if changes['total_changes'] > 0:
            fig_changes = go.Figure(data=[go.Pie(
                labels=['Additions', 'Deletions', 'Modifications'],
                values=[changes['additions'], changes['deletions'], changes['modifications']],
                hole=.3,
                marker_colors=['#2e7d32', '#c62828', '#f57c00']
            )])
            
            fig_changes.update_layout(
                title="Distribution of Changes",
                height=400
            )
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig_changes, use_container_width=True)
            
            with col2:
                # Similarity gauge
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=stats.get('similarity_percentage', 0),
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Similarity Score"},
                    delta={'reference': 80},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#1f77b4"},
                        'steps': [
                            {'range': [0, 50], 'color': "#ffcccb"},
                            {'range': [50, 80], 'color': "#fff2cc"},
                            {'range': [80, 100], 'color': "#c8e6c9"}
                        ],
                        'threshold': {
                            'line': {'color': "#d32f2f", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                
                fig_gauge.update_layout(height=400)
                st.plotly_chart(fig_gauge, use_container_width=True)
    
    def display_differences(self, results, max_differences):
        """Display detailed differences"""
        
        st.subheader("🔍 Detailed Differences")
        
        differences = results['differences'][:max_differences]
        
        if not differences:
            st.info("🎉 No differences found between the documents!")
            return
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📝 Line by Line", "📊 Summary", "🗂️ Raw Data"])
        
        with tab1:
            st.markdown("### Line-by-Line Changes")
            
            for i, diff in enumerate(differences):
                if diff.get('type') == 'addition':
                    st.markdown(f"""
                    <div class="diff-addition" style="padding: 1rem; margin: 0.5rem 0; border-radius: 0.5rem;">
                        <strong style="font-size: 1.1rem;">➕ Addition:</strong><br/>
                        <span style="font-family: monospace; background-color: rgba(255,255,255,0.3); padding: 0.2rem; border-radius: 0.2rem;">
                        {diff.get('content', '')[:300]}{'...' if len(diff.get('content', '')) > 300 else ''}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                
                elif diff.get('type') == 'deletion':
                    st.markdown(f"""
                    <div class="diff-deletion" style="padding: 1rem; margin: 0.5rem 0; border-radius: 0.5rem;">
                        <strong style="font-size: 1.1rem;">➖ Deletion:</strong><br/>
                        <span style="font-family: monospace; background-color: rgba(255,255,255,0.3); padding: 0.2rem; border-radius: 0.2rem;">
                        {diff.get('content', '')[:300]}{'...' if len(diff.get('content', '')) > 300 else ''}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                
                elif diff.get('type') in ['replacement', 'change']:
                    st.markdown(f"""
                    <div class="diff-change" style="padding: 1rem; margin: 0.5rem 0; border-radius: 0.5rem;">
                        <strong style="font-size: 1.1rem;">🔄 Change:</strong><br/>
                        <span style="font-family: monospace; background-color: rgba(255,255,255,0.3); padding: 0.2rem; border-radius: 0.2rem;">
                        {diff.get('content', '')[:300]}{'...' if len(diff.get('content', '')) > 300 else ''}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab2:
            # Algorithm-specific summaries
            if results['algorithm'] == 'levenshtein':
                summary_data = [d for d in differences if d.get('type') == 'summary']
                if summary_data:
                    st.json(summary_data[0])
            
            elif results['algorithm'] == 'jaro_winkler':
                similarity_data = [d for d in differences if d.get('type') == 'similarity_score']
                if similarity_data:
                    st.metric("Jaro-Winkler Similarity", similarity_data[0].get('percentage', 'N/A'))
            
            elif results['algorithm'] == 'semantic':
                semantic_data = [d for d in differences if d.get('type') == 'semantic_score']
                if semantic_data:
                    df = pd.DataFrame(semantic_data)
                    st.dataframe(df)
        
        with tab3:
            st.json({"total_differences": len(results['differences']), 
                    "showing": len(differences),
                    "differences": differences})
    
    def generate_exports(self, results, export_formats, file1_name, file2_name):
        """Generate and provide download links for exports"""
        
        if not export_formats:
            return
        
        st.subheader("💾 Download Results")
        
        # Create temporary directory for exports
        temp_dir = Path(tempfile.mkdtemp())
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"comparison_{Path(file1_name).stem}_vs_{Path(file2_name).stem}_{timestamp}"
            
            for format_type in export_formats:
                try:
                    output_path = temp_dir / f"{base_filename}.{format_type}"
                    self.comparer.export_results(results, str(output_path), format_type)
                    
                    with open(output_path, 'rb') as f:
                        st.download_button(
                            label=f"📥 Download {format_type.upper()} Report",
                            data=f.read(),
                            file_name=f"{base_filename}.{format_type}",
                            mime=self.get_mime_type(format_type),
                            key=f"download_{format_type}"
                        )
                
                except Exception as e:
                    st.warning(f"⚠️ Could not generate {format_type.upper()} export: {str(e)}")
        
        except Exception as e:
            st.error(f"❌ Error generating exports: {str(e)}")
    
    def get_mime_type(self, format_type):
        """Get MIME type for different formats"""
        mime_types = {
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'html': 'text/html',
            'json': 'application/json',
            'markdown': 'text/markdown'
        }
        return mime_types.get(format_type, 'application/octet-stream')


def main():
    app = StreamlitDocumentComparer()
    app.main()


if __name__ == "__main__":
    main() 
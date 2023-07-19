from flask import Flask, render_template, request, flash, redirect, url_for
import pandas as pd
import plotly.graph_objects as go
import os
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))

    # Check if the file has an allowed extension (Excel or CSV)
    allowed_extensions = {'xlsx', 'xls', 'csv'}
    if not file.filename.lower().endswith(tuple(allowed_extensions)):
        flash('Invalid file format. Please upload an Excel or CSV file.', 'error')
        return redirect(url_for('index'))

    # Save the uploaded file to the 'uploads' folder
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    try:
        # Read the data from the file using pandas
        df = pd.read_excel(file_path)  # Make sure pandas is installed
    except Exception as e:
        flash('Error reading the file: {}'.format(str(e)), 'error')
        return redirect(url_for('index'))

    # Data manipulation and visualization
    try:
        # Ensure 'Category' column is accessed case-insensitively
        category_column = df['Category'] if 'Category' in df.columns else df['category']

        # Custom colors for the bar chart
        bar_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

        # Create individual charts using Plotly
        fig1 = go.Figure(data=[go.Bar(x=category_column, y=df['Value'], marker_color=bar_colors)])
        fig1.update_layout(
            title='Bar Chart',
            xaxis_title='Category',
            yaxis_title='Value',
            template='plotly_dark'  # Use a dark theme for aesthetics
        )
        chart_path1 = os.path.join('static', 'chart1.html')
        fig1.write_html(chart_path1)

        fig2 = go.Figure(data=[go.Line(x=category_column, y=df['Value'])])
        fig2.update_layout(
            title='Line Chart',
            xaxis_title='Category',
            yaxis_title='Value',
            template='plotly_dark'  # Use a dark theme for aesthetics
        )
        chart_path2 = os.path.join('static', 'chart2.html')
        fig2.write_html(chart_path2)

        fig3 = go.Figure(data=[go.Pie(labels=category_column, values=df['Value'])])
        fig3.update_layout(
            title='Pie Chart',
            template='plotly_dark'  # Use a dark theme for aesthetics
        )
        chart_path3 = os.path.join('static', 'chart3.html')
        fig3.write_html(chart_path3)

        fig4 = go.Figure(data=[go.Scatter(x=category_column, y=df['Value'], mode='markers')])
        fig4.update_layout(
            title='Scatter Plot',
            xaxis_title='Category',
            yaxis_title='Value',
            template='plotly_dark'  # Use a dark theme for aesthetics
        )
        chart_path4 = os.path.join('static', 'chart4.html')
        fig4.write_html(chart_path4)

        # Remove the temporary file after a brief pause to release the file handle
        time.sleep(1)  # Wait for a second to ensure the file handle is released
        os.remove(file_path)

        # Render the visualization template and pass the chart paths to display the charts
        return render_template('visualization.html',
                               chart_path1=chart_path1,
                               chart_path2=chart_path2,
                               chart_path3=chart_path3,
                               chart_path4=chart_path4)

    except Exception as e:
        flash('Error processing the file: {}'.format(str(e)), 'error')
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)

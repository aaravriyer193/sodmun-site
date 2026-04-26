import os
import re
from flask import Flask, redirect, url_for, make_response
from datetime import datetime

app = Flask(__name__)

TEMPLATES_DIR = os.path.join(app.root_path, 'templates')

def remove_html_comments(text):
    # Removes including multi-line ones
    return re.sub(r'', '', text, flags=re.DOTALL)

@app.route('/', defaults={'page': 'index'})
@app.route('/<path:page>')
def serve_pages(page):
    # Ensure we are looking for an .html file
    if not page.endswith('.html'):
        page_file = f"{page}.html"
    else:
        page_file = page
    
    file_path = os.path.join(TEMPLATES_DIR, page_file)
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Strip comments
        clean_content = remove_html_comments(content)
        
        # Create the response object
        response = make_response(clean_content)
        response.headers['Content-Type'] = 'text/html'
        
        # --- HARD RELOAD HEADERS ---
        # Forces the browser to ignore its cache entirely
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = 'Sat, 01 Jan 2000 00:00:00 GMT' # Date in the past
        response.headers['Last-Modified'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        return response
    
    # 404 Catch-all: Redirect back to index
    return redirect(url_for('serve_pages', page='index'))

if __name__ == '__main__':
    # Setting debug=True ensures the Flask server restarts when app.py changes
    app.run(debug=True, port=5000)
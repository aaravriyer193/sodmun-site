import os
import re
from flask import Flask, redirect, url_for, make_response
from datetime import datetime

app = Flask(__name__)

TEMPLATES_DIR = os.path.join(app.root_path, 'templates')

def remove_html_comments(text):
    return re.sub(r'', '', text, flags=re.DOTALL)

@app.route('/', defaults={'page': 'index'})
@app.route('/<path:page>')
def serve_pages(page):
    if not page.endswith('.html'):
        page_file = f"{page}.html"
    else:
        page_file = page
    
    file_path = os.path.join(TEMPLATES_DIR, page_file)
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        clean_content = remove_html_comments(content)
        
        response = make_response(clean_content)
        response.headers['Content-Type'] = 'text/html'
        
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = 'Sat, 01 Jan 2000 00:00:00 GMT' # Date in the past
        response.headers['Last-Modified'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        return response
    
    return redirect(url_for('serve_pages', page='index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
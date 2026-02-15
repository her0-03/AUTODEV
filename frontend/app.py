from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

BACKEND_URL = os.environ.get('BACKEND_API_URL', 'http://localhost:8000')

@app.route('/')
def index():
    if 'token' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        response = requests.post(f'{BACKEND_URL}/api/v1/auth/login', json={
            'email': email,
            'password': password
        })
        
        if response.status_code == 200:
            data = response.json()
            session['token'] = data['access_token']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        response = requests.post(f'{BACKEND_URL}/api/v1/auth/register', json={
            'email': email,
            'password': password
        })
        
        if response.status_code == 200:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed', 'error')
    
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'token' not in session:
        return redirect(url_for('login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    response = requests.get(f'{BACKEND_URL}/api/v1/projects', headers=headers)
    
    if response.status_code == 200:
        projects = response.json()
        return render_template('dashboard.html', projects=projects)
    
    return redirect(url_for('login'))

@app.route('/project/<project_id>')
def project_detail(project_id):
    if 'token' not in session:
        return redirect(url_for('login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    response = requests.get(f'{BACKEND_URL}/api/v1/projects/{project_id}', headers=headers)
    
    if response.status_code == 200:
        project = response.json()
        return render_template('project_detail.html', project=project)
    
    return redirect(url_for('dashboard'))

@app.route('/advanced')
def advanced_features():
    if 'token' not in session:
        return redirect(url_for('login'))
    return render_template('advanced.html')

@app.route('/editor/<job_id>')
def visual_editor(job_id):
    if 'token' not in session:
        return redirect(url_for('login'))
    return render_template('visual_editor.html', job_id=job_id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

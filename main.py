from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_session import Session
import os
from supabase import create_client, Client
from datetime import datetime
import uuid

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

# Initialize session
Session(app)

# Initialize Supabase client
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_ANON_KEY')

if supabase_url and supabase_key:
    supabase: Client = create_client(supabase_url, supabase_key)
else:
    print("Warning: Supabase credentials not found. Please set SUPABASE_URL and SUPABASE_ANON_KEY environment variables.")
    supabase = None

# Helper functions
def get_current_user():
    """Get current logged-in user from session"""
    if 'user_id' in session:
        try:
            response = supabase.table('users').select('*').eq('id', session['user_id']).execute()
            if response.data:
                return response.data[0]
        except Exception as e:
            print(f"Error fetching user: {e}")
    return None

def require_auth():
    """Decorator to require authentication"""
    def decorator(f):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not supabase:
            flash('Authentication service unavailable', 'error')
            return render_template('login.html')
        
        try:
            # Authenticate with Supabase
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                # Get user profile from database
                user_response = supabase.table('users').select('*').eq('email', email).execute()
                if user_response.data:
                    user = user_response.data[0]
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['email'] = user['email']
                    flash('Login successful!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('User profile not found', 'error')
            else:
                flash('Invalid email or password', 'error')
                
        except Exception as e:
            flash(f'Login failed: {str(e)}', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        display_name = request.form.get('display_name', username)
        
        if not supabase:
            flash('Authentication service unavailable', 'error')
            return render_template('register.html')
        
        try:
            # Register with Supabase Auth
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if auth_response.user:
                # Create user profile in database
                user_data = {
                    'username': username,
                    'email': email,
                    'display_name': display_name,
                    'firebase_uid': auth_response.user.id,
                    'daily_goal': 500,
                    'current_streak': 0
                }
                
                profile_response = supabase.table('users').insert(user_data).execute()
                
                if profile_response.data:
                    flash('Registration successful! Please log in.', 'success')
                    return redirect(url_for('login'))
                else:
                    flash('Failed to create user profile', 'error')
            else:
                flash('Registration failed', 'error')
                
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'error')
    
    return render_template('register.html')

@app.route('/dashboard')
@require_auth()
def dashboard():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    # Get user's projects
    projects = []
    writing_stats = {
        'total_words': 0,
        'projects_count': 0,
        'chapters_count': 0,
        'daily_progress': 0
    }
    
    if supabase:
        try:
            # Fetch projects
            projects_response = supabase.table('projects').select('*').eq('user_id', user['id']).execute()
            projects = projects_response.data or []
            
            # Calculate stats
            writing_stats['projects_count'] = len(projects)
            writing_stats['total_words'] = sum(p.get('word_count', 0) for p in projects)
            
            # Fetch chapters count
            for project in projects:
                chapters_response = supabase.table('chapters').select('id').eq('project_id', project['id']).execute()
                writing_stats['chapters_count'] += len(chapters_response.data or [])
            
        except Exception as e:
            print(f"Error fetching dashboard data: {e}")
    
    return render_template('dashboard.html', 
                         user=user, 
                         projects=projects[:5],  # Recent 5 projects
                         writing_stats=writing_stats)

@app.route('/projects')
@require_auth()
def projects():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    projects = []
    if supabase:
        try:
            response = supabase.table('projects').select('*').eq('user_id', user['id']).execute()
            projects = response.data or []
        except Exception as e:
            print(f"Error fetching projects: {e}")
    
    return render_template('projects.html', projects=projects, user=user)

@app.route('/create-project', methods=['GET', 'POST'])
@require_auth()
def create_project():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description', '')
        word_goal = int(request.form.get('word_goal', 50000))
        status = request.form.get('status', 'draft')
        
        if not supabase:
            flash('Service unavailable', 'error')
            return render_template('create_project.html')
        
        try:
            project_data = {
                'user_id': user['id'],
                'title': title,
                'description': description,
                'word_goal': word_goal,
                'status': status,
                'word_count': 0
            }
            
            response = supabase.table('projects').insert(project_data).execute()
            
            if response.data:
                flash('Project created successfully!', 'success')
                return redirect(url_for('projects'))
            else:
                flash('Failed to create project', 'error')
                
        except Exception as e:
            flash(f'Error creating project: {str(e)}', 'error')
    
    return render_template('create_project.html')

@app.route('/community')
@require_auth()
def community():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    # Mock data for community features
    community_stats = {
        'active_writers': 156,
        'posts_today': 23,
        'beta_requests': 12,
        'writing_tips': 45
    }
    
    posts = []
    beta_requests = []
    
    return render_template('community.html', 
                         user=user, 
                         community_stats=community_stats,
                         posts=posts,
                         beta_requests=beta_requests)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('login'))

# API Routes
@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
@require_auth()
def delete_project(project_id):
    user = get_current_user()
    if not user or not supabase:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Verify project ownership
        project_response = supabase.table('projects').select('*').eq('id', project_id).eq('user_id', user['id']).execute()
        
        if not project_response.data:
            return jsonify({'error': 'Project not found'}), 404
        
        # Delete project
        delete_response = supabase.table('projects').delete().eq('id', project_id).execute()
        
        if delete_response.data:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Failed to delete project'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

NoteTrail Flask App - Deployment Package

This package contains all the files needed to deploy your NoteTrail writing platform to Render with the correct folder structure.

Folder Structure (Render Required)

notetrail-platform/
├── main.py               # Main Flask application (must be main.py)
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── README.txt           # This file
├── templates/           # Templates folder (must be lowercase)
│   ├── login.html       # Login page
│   ├── signup.html      # Registration page (renamed from register.html)
│   ├── dashboard.html   # User dashboard
│   ├── base.html        # Base template with navigation
│   ├── projects.html    # Projects listing
│   ├── create_project.html # Create new project
│   └── community.html   # Community features
└── static/
    ├── css/
    │   └── main.css     # Complete CSS with NoteTrail branding
    ├── js/
    │   └── main.js      # Interactive features and auto-save
    └── images/
        └── logo.png     # NoteTrail logo

Key Changes Made

1. File renamed: app.py → main.py (Render requirement)
2. Route updated: /register → /signup with signup.html template
3. Folder structure: All lowercase templates/ folder as required
4. render_template(): All routes properly use Flask's render_template function

Render Deployment Instructions

1. Upload to Render:
   - Create a new Web Service on Render
   - Connect your GitHub repository or upload these files
   - Build command: pip install -r requirements.txt
   - Start command: python main.py

2. Environment Variables (Set in Render Dashboard):
   SECRET_KEY=your-secret-key-here
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your-supabase-anon-key

3. Custom Domain Setup:
   - In Render dashboard: Settings > Custom Domains
   - Add: www.notetrail.co.uk
   - Update DNS as instructed by Render

Features Included

- Authentication: User signup/login with Supabase
- Dashboard: Writing statistics and project overview
- Project Management: Create, view, and manage writing projects
- Community: Social features and beta reader requests
- Responsive Design: Works on mobile, tablet, and desktop
- Auto-save: Writing workspace with automatic content saving
- NoteTrail Branding: Complete CSS with brand colors (#738063)

Important Notes

- Templates folder MUST be lowercase templates/
- Main file MUST be named main.py
- All routes use render_template() function correctly
- Static files served from /static/ directory
- Sessions stored in filesystem (suitable for single-instance deployment)

This structure follows Render's exact requirements for Flask deployment.
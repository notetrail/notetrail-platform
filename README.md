# NoteTrail Flask App - Deployment Package

This package contains all the files needed to deploy your NoteTrail writing platform to Render.

## Quick Start

1. **Upload to Render:**
   - Create a new Web Service on Render
   - Connect your GitHub repository or upload these files
   - Set the build command: `pip install -r requirements.txt`
   - Set the start command: `python app.py`

2. **Environment Variables:**
   - Copy `.env.example` to `.env`
   - Add your Supabase credentials in Render's environment variables:
     - `SUPABASE_URL`: Your Supabase project URL
     - `SUPABASE_ANON_KEY`: Your Supabase anonymous key
     - `SECRET_KEY`: Generate a random secret key for Flask sessions

3. **Domain Setup:**
   - In Render dashboard, go to Settings > Custom Domains
   - Add your domain: `www.notetrail.co.uk`
   - Update your DNS settings as instructed by Render

## File Structure

```
notetrail_flask_export/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
├── static/
│   ├── css/
│   │   └── main.css      # Complete CSS with NoteTrail branding
│   ├── js/
│   │   └── main.js       # Interactive features and auto-save
│   └── images/
│       └── logo.png      # NoteTrail logo
└── templates/
    ├── base.html         # Base template with navigation
    ├── login.html        # Login page
    ├── register.html     # Registration page
    ├── dashboard.html    # User dashboard
    ├── projects.html     # Projects listing
    ├── create_project.html # Create new project
    └── community.html    # Community features
```

## Features Included

### Authentication
- User registration and login with Supabase
- Session management
- Protected routes

### Dashboard
- Writing statistics
- Recent projects
- Quick actions
- Progress tracking

### Project Management
- Create and manage writing projects
- Word count tracking
- Progress visualization
- Project status management

### Community Features
- Community posts
- Beta reader requests
- Activity feed
- Social interactions

### Writing Tools
- Auto-save functionality
- Word count tracking
- Version history ready
- Responsive design

## Deployment Notes

- The app is configured to run on port 5000
- All static files are served from the `/static` directory
- Templates use Jinja2 templating engine
- Sessions are stored in the filesystem (suitable for single-instance deployment)

## Support

For any issues with deployment or configuration, refer to the Render documentation or contact support.
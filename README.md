# STRIDE RUN CLUB

A clean, minimal, and user-friendly running club website built with Flask and MySQL. This is a real-world application that running clubs can actually use to manage runs and registrations.

## 📋 Project Purpose

STRIDE RUN CLUB is a web application that allows running clubs to:
- Display upcoming runs with details
- Allow runners to register for runs
- Manage runs through an admin dashboard
- Track community statistics
- Provide information about the club

## 🚀 Features

### User Features
- **Home Page**: Hero section, next run countdown, community statistics
- **Runs Page**: View all upcoming runs with details
- **Run Details**: Detailed information about each run
- **Registration**: Simple form to join runs
- **About Page**: Club information, values, beginner-friendly content
- **Success Page**: Confirmation and tips for new runners

### Admin Features
- **Admin Dashboard**: Overview of runs, members, and registrations
- **Run Management**: Add, edit, and delete runs
- **Registration Tracking**: View recent registrations
- **Statistics**: Community metrics

### Design Features
- **Mobile-First**: Optimized for mobile devices
- **Clean Minimal Design**: Lots of whitespace, strong typography
- **Fast Performance**: Lightweight and quick to load
- **Responsive**: Works on mobile, tablet, and desktop
- **User-Friendly**: Simple forms and clear navigation

## 🛠️ Tech Stack

### Frontend
- **HTML5** - Structure and content
- **CSS3** - Clean minimal design
- **Vanilla JavaScript** - Interactive functionality

### Backend
- **Python** - Programming language
- **Flask** - Web framework

### Database
- **MySQL 8.0** - Relational database

## 📁 Folder Structure

```
stride-run-club/
│
├── app.py                      # Main Flask application
├── database.py                 # MySQL database connection
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .env                        # Environment variables (configured)
├── README.md                   # This file
│
├── database/
│   └── schema.sql              # Database schema and sample data
│
├── templates/                  # HTML templates
│   ├── base.html               # Base template with navbar
│   ├── index.html              # Home page
│   ├── runs.html               # Runs listing page
│   ├── run_details.html        # Individual run details
│   ├── about.html              # About page
│   ├── join.html               # Registration form
│   ├── success.html            # Registration success
│   ├── login.html              # Admin login
│   └── admin.html              # Admin dashboard
│
└── static/                     # Static assets
    ├── css/
    │   └── style.css           # Styles
    ├── js/
    │   └── script.js           # JavaScript
    └── images/                 # Image folder
```

## 🔧 How Flask Works

Flask is a micro web framework that handles:
- **Routing**: Maps URLs to Python functions using decorators like `@app.route('/')`
- **Templates**: Uses Jinja2 to render dynamic HTML
- **Sessions**: Manages user authentication state
- **Requests**: Handles HTTP methods (GET, POST)
- **Flash Messages**: Displays temporary messages to users

## 🗄️ How MySQL Works

MySQL is a relational database that:
- **Stores Data**: Organizes data in tables (runs, members, registrations)
- **Relationships**: Uses foreign keys to connect related data
- **SQL**: Uses Structured Query Language for data operations
- **Security**: Uses parameterized queries to prevent SQL injection

## 📦 Installation Instructions

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

### Step 1: Navigate to Project Directory

```bash
cd C:\Users\veer\stride-run-club
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Flask-MySQL (database integration)
- python-dotenv (environment variables)
- Werkzeug (security utilities)
- mysql-connector-python (MySQL driver)

## 🗄️ MySQL Setup

### Step 1: Install MySQL (if not already installed)

1. Download MySQL Community Server from https://dev.mysql.com/downloads/mysql/
2. Run the installer and follow the setup wizard
3. Set a root password during installation
4. Start the MySQL service

### Step 2: Create the Database

**Option A: Using MySQL Command Line**

1. Open MySQL Command Line Client
2. Login with your root password:
   ```bash
   mysql -u root -p
   ```
3. Execute the schema file:
   ```bash
   source C:/Users/veer/stride-run-club/database/schema.sql
   ```

**Option B: Using MySQL Workbench**

1. Open MySQL Workbench
2. Connect to your MySQL server
3. Go to File → Run SQL Script
4. Select `database/schema.sql`
5. Execute the script

**Option C: Using Command Line (single command)**
```bash
mysql -u root -p < C:/Users/veer/stride-run-club/database/schema.sql
```

This will:
- Create `stride_run_club` database
- Create all required tables (runs, members, registrations)
- Add sample upcoming runs

### Step 3: Configure Environment Variables

The `.env` file is already configured with default settings. If your MySQL has a password, update it:

**Edit `.env` file:**
```
SECRET_KEY=stride-run-club-secret-key-2024
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_NAME=stride_run_club
```

**Important:**
- If your MySQL has no password, leave `DB_PASSWORD` empty
- Never commit the `.env` file to version control
- Use a strong SECRET_KEY in production

## 🚀 Running the Application

### Step 1: Ensure Virtual Environment is Active

```bash
venv\Scripts\activate
```

### Step 2: Run the Flask Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000/`

### Step 3: Access the Website

Open your browser and go to: `http://127.0.0.1:5000`

## 🔑 Admin Access

### Default Admin Credentials
- **Email:** admin@stride.com
- **Password:** admin123

### Admin Dashboard Features
- View community statistics
- Add new runs
- Edit existing runs
- Delete runs
- View recent registrations

### Access Admin Panel
1. Go to `http://127.0.0.1:5000/login`
2. Enter admin credentials
3. Access the admin dashboard

## 🔄 Registration Flow

1. **User browses runs** on the Runs page
2. **User views run details** for a specific run
3. **User clicks "JOIN RUN"** button
4. **User fills registration form** with:
   - Name
   - Email
   - Phone (optional)
   - Running experience
   - Preferred distance
5. **System checks** if email already exists in database
6. **If new user**: Creates member record
7. **If existing user**: Uses existing member ID
8. **System checks** for duplicate registration (email + run ID)
9. **If duplicate**: Shows error message
10. **If new registration**: Creates registration record
11. **User sees success page** with run day tips

## 🔌 Flask-MySQL Communication

The Flask backend communicates with MySQL through:

1. **Database Connection** (`database.py`):
   - Uses `mysql-connector-python` to connect
   - Reads credentials from `.env` file
   - Creates connection pool for efficiency

2. **Query Execution**:
   - `fetch_all()` - Retrieve multiple records
   - `fetch_one()` - Retrieve single record
   - `execute_query()` - Insert/Update/Delete operations

3. **Parameterized Queries**:
   - Prevents SQL injection attacks
   - Separates SQL logic from user input
   - Example: `SELECT * FROM runs WHERE id = %s`, (run_id,)

4. **Error Handling**:
   - Catches MySQL connection errors
   - Provides helpful error messages
   - Handles transaction rollbacks

## 📱 Responsive Design

The website is designed to work on:
- **Mobile** (< 480px) - Primary focus for runners on the go
- **Tablet** (481px - 768px) - Optimized touch targets
- **Desktop** (> 768px) - Full feature set

Mobile features:
- Hamburger menu navigation
- Large, tap-friendly buttons
- Simplified layouts
- Touch-optimized forms

## 🧪 Testing the Application

### Manual Testing Checklist

#### User Features
- [ ] Homepage loads with hero section
- [ ] Next run countdown works
- [ ] Navigation menu is responsive
- [ ] Runs page displays upcoming runs
- [ ] Run details page shows complete information
- [ ] Registration form validates inputs
- [ ] Registration creates member record
- [ ] Registration prevents duplicates
- [ ] Success page displays correctly
- [ ] About page content is complete

#### Admin Features
- [ ] Admin login works
- [ ] Admin dashboard loads
- [ ] Statistics display correctly
- [ ] Add run functionality works
- [ ] Edit run functionality works
- [ ] Delete run functionality works
- [ ] Recent registrations display

#### Database
- [ ] MySQL connection established
- [ ] Sample runs loaded correctly
- [ ] Member records created
- [ ] Registration records created
- [ ] Foreign key constraints work
- [ ] Duplicate prevention works

## 🐛 Troubleshooting

### MySQL Connection Issues

**Error:** "Access denied for user 'root'@'localhost'"

**Solution:** 
- Check your MySQL password in `.env` file
- Ensure MySQL service is running
- Verify username and password

**Error:** "Unknown database 'stride_run_club'"

**Solution:** 
- Run the schema.sql file to create the database
- Check that database name matches in `.env`

### Python Issues

**Error:** "Module not found"

**Solution:** 
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`
- Check Python version (3.8+)

**Error:** "Port 5000 already in use"

**Solution:** 
- Change port in app.py: `app.run(debug=True, port=5001)`
- Stop other applications using port 5000

### Template Issues

**Error:** "Template not found"

**Solution:** 
- Ensure templates folder is in correct location
- Check template names match exactly

## 📝 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| SECRET_KEY | Flask secret key for session security | `stride-run-club-secret-key-2024` |
| DB_HOST | MySQL server host | `localhost` |
| DB_USER | MySQL username | `root` |
| DB_PASSWORD | MySQL password | `your_password` |
| DB_NAME | Database name | `stride_run_club` |

## 🔒 Security Notes

1. **Change admin password** before production use
2. **Use strong SECRET_KEY** in production
3. **Enable HTTPS** in production
4. **Keep dependencies updated**
5. **Regular database backups**
6. **Never commit .env file** to version control

## 📄 License

This project is created for educational and real-world use.

## 🙏 Acknowledgments

- Flask documentation
- MySQL documentation
- Web development community

## 📞 Support

For issues or questions, check the troubleshooting section above.

---

**Built with simplicity and real-world usability in mind.**

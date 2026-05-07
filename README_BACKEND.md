# Makai Backend Setup

## Virtual Environment Setup

To create the virtual environment:
```bash
py -m venv venv
```

To activate the virtual environment:

**Git Bash:**
```bash
source venv/Scripts/activate
```

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Command Prompt:**
```cmd
venv\Scripts\activate
```


Push & deploy, then visit:
URL	What it does
https://makai-2-0.onrender.com/api/docs/	Swagger UI — interactive API explorer
https://makai-2-0.onrender.com/api/redoc/	Redoc — clean API reference docs
https://makai-2-0.onrender.com/admin/	Django admin panel
To test authenticated endpoints in Swagger:
Call POST /api/v1/auth/login/ (or register) to get a JWT token
Click "Authorize" at the top of Swagger UI
Enter Bearer <your_token>
All locked endpoints will now be accessible
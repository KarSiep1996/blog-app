import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))    

class Config:
   SECRET_KEY = os.environ.get("SECRET_KEY") or "remember-to-add-secret-key"    
   SQLALCHEMY_DATABASE_URI = (                           
           os.environ.get('DATABASE_URL') or
           'sqlite:///' + os.path.join(BASE_DIR, 'blog.db')
   )
   SQLALCHEMY_TRACK_MODIFICATIONS = False
   ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
   ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "change-me")
   MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
   MAIL_PORT = os.environ.get("MAIL_PORT", 465)
   MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "ancymonka1996@gmail.com")
   MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "Misiaczek@12")
   MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", False)
   MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", True)
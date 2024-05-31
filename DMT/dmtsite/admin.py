from django.contrib import admin

# Register your models here.
class cf_admin_panel(admin.AdminSite):
    site_header = "CF ADMIN"
    login_template = "login.html"
    
cf_admin = cf_admin_panel(name="CfAdmin")
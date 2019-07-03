from flask_principal import Principal, Permission, RoleNeed

principal = Principal()

permission_admin = Permission(RoleNeed('admin'))
permission_poster = Permission(RoleNeed('poster'))
permission_default = Permission(RoleNeed('default'))
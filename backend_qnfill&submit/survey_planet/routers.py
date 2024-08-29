class SessionRouter:
    def db_for_read(self, model, **hints):
        if model._meta.db_table == 'django_session':
            return 'session_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.db_table == 'django_session':
            return 'session_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.db_table == 'django_session' or obj2._meta.db_table == 'django_session':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'sessions':
            return db == 'session_db'
        return db == 'default'

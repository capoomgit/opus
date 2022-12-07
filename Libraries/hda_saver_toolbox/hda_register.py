from database import CursorFromConnectionFromPool

class hda_register:
    def __init__(self, name, all_parms, parms_default, parms_min, parms_max, parms_type, parms_override, version, id=None):
        self.name = name
        self.all_parms = all_parms
        self.parms_default = parms_default
        self.parms_min = parms_min
        self.parms_max = parms_max
        self.parms_type = parms_type
        self.parms_override = parms_override
        self.id = id
        self.version = version
        
     
    def __repr__(self): # This is a special method that is called when you try to print an object
        return f"User('{self.name}', '{self.all_parms}', '{self.parms_default}', '{self.parms_min}', '{self.parms_max}', {self.id})"

    def save_to_db(self): 
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO public."Hdas" (hda_name, parm_names, parm_mins, parm_maxes, parm_types, parm_defaults, parm_override_mode, hda_version) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING hda_id',
                            (self.name, self.all_parms, self.parms_min, self.parms_max, self.parms_type, self.parms_default, self.parms_override, self.version))
            return cursor.fetchone()[0]


    @classmethod
    def load_from_db_by_name(cls, name):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM "Hdas" WHERE name=%s', (name,))
            user_data = cursor.fetchone()
            return cls(name=user_data[1], all_parms=user_data[2], parms_default=user_data[3], parms_min=user_data[4], parms_max=user_data[5], parm_type=user_data[6], dependencies=user_data[7], id=user_data[0])


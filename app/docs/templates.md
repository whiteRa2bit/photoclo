# Template for config files
### database_config.yaml:
    
Example:

    database:
    - ENGINE:
        'django.db.backends.postgresql_psycopg2'
      NAME:
        'photoclo'
      USER:
        'photoclo_django'
      PASSWORD:
        !!python/none
      HOST:
        'localhost'
     PORT:
        '5432'
    
### settings.yaml:

    secret key:
      T_G;:I_`$mdJ6IaEwM=Z_*e[jde)W7%z=EJ"#D[9PtCg<C!h&-
    debug:
      !!bool False
    allowed hosts:
      []

### face_detection_config.yaml:

    face detection url:
      http://localhost:5000/recognize
    compressed photo storage:
      http://localhost:8000

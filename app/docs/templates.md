# Template for config files
### database.config:
    1) database driver
    2) name
    3) username
    4) password
    5) url
    6) port
    
Example:

    django.db.backends.postgresql_psycopg2
    photoclo
    photoclo_django
    12345678910
    localhost
    5432
    
### secret_key
One line with the secret key for django project.

Example:

    T_G;:I_`$mdJ6IaEwM=Z_*e[jde)W7%z=EJ"#D[9PtCg<C!h&-

### debug
Empty file, working like trigger for debug option.
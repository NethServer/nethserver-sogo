CONNECT mysql;

REPLACE INTO user (host, user, password)
    VALUES (
        'localhost',
        'sogo',
        password('{$sogod{DbPassword}}')
    );

REPLACE INTO db (host, db, user, select_priv, insert_priv, update_priv,
                 delete_priv, create_priv, drop_priv, alter_priv, index_priv,
                 references_priv)
    VALUES (
        'localhost',
        'sogo',
        'sogo',
        'Y', 'Y', 'Y', 'Y',
        'Y', 'Y', 'Y', 'Y',
        'Y'
    );

FLUSH PRIVILEGES;

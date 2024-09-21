def migration_sql():
    from django.db import connection, transaction
    cursor = connection.cursor()

    # Data modifying operation - commit required
    try:
        cursor.execute("""
            CREATE TABLE authtoken_token (
                "key" varchar(40) NOT NULL,
                created timestamptz NOT NULL,
                user_id int4 NOT NULL,
                CONSTRAINT authtoken_token_pkey PRIMARY KEY (key),
                CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id));
            CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);

            ALTER TABLE authtoken_token ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_auth_user_id 
            FOREIGN KEY (user_id) REFERENCES public.customers_customuser(id) DEFERRABLE INITIALLY DEFERRED;
                    """)
        transaction.commit()
    except:
        pass
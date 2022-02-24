from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_bicycle_content_search_and_more'),
    ]

    migration = '''
        CREATE TRIGGER content_search_update BEFORE INSERT OR UPDATE
        ON catalog_bicycle FOR EACH ROW EXECUTE FUNCTION
        tsvector_update_trigger(content_search, 'pg_catalog.english', name);

        -- Force triggers to run and populate the text_search column.
        UPDATE catalog_bicycle set ID = ID;
    '''

    reverse_migration = '''
        DROP TRIGGER content_search_update ON catalog_bicycle;
    '''

    operations = [
        migrations.RunSQL(migration, reverse_migration)
    ]

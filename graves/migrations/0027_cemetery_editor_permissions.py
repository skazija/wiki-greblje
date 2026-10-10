from django.db import migrations


def grant_editor_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    db_alias = schema_editor.connection.alias

    group, _ = Group.objects.using(db_alias).get_or_create(
        name="Urednici"
    )

    content_type = ContentType.objects.using(db_alias).get(
        app_label="graves",
        model="cemetery",
    )

    permissions = Permission.objects.using(db_alias).filter(
        content_type=content_type,
        codename__in=[
            "view_cemetery",
            "change_cemetery",
        ],
    )

    group.permissions.add(*permissions)


class Migration(migrations.Migration):

    dependencies = [
        ("graves", "0026_cemetery_created_by_cemetery_status"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.RunPython(
            grant_editor_permissions,
            migrations.RunPython.noop,
        ),
    ]
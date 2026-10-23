from django.db import migrations


def grant_editor_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    db_alias = schema_editor.connection.alias

    group, _ = Group.objects.using(db_alias).get_or_create(
        name="Urednici"
    )

    content_type, _ = ContentType.objects.using(db_alias).get_or_create(
        app_label="graves",
        model="cemetery",
    )

    permissions = []
    for codename, name in [
        ("view_cemetery", "Can view cemetery"),
        ("change_cemetery", "Can change cemetery"),
    ]:
        permission, _ = Permission.objects.using(db_alias).get_or_create(
            content_type=content_type,
            codename=codename,
            defaults={"name": name},
        )
        permissions.append(permission)

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

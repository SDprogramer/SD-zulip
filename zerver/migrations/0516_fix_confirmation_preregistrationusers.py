# Generated by Django 5.0.5 on 2024-04-29 19:24

from django.db import migrations

TOO_MANY_CONFIRMATIONS = """
DELETE FROM confirmation_confirmation
WHERE  id IN (WITH too_many_confirmations
                   AS (SELECT object_id,
                              MIN(confirmation_confirmation.id) AS exclude_id,
                              COUNT(*)
                       FROM   confirmation_confirmation
                       JOIN   zerver_preregistrationuser
                       ON     content_type_id = (SELECT id
                                                 FROM   django_content_type
                                                 WHERE  app_label = 'zerver'
                                                 AND    model = 'preregistrationuser')
                       AND    object_id = zerver_preregistrationuser.id
                       WHERE  referred_by_id IS NOT NULL
                       GROUP  BY object_id
                       HAVING COUNT(*) > 1)
              SELECT id
               FROM  confirmation_confirmation
                     JOIN too_many_confirmations
                       ON too_many_confirmations.object_id = confirmation_confirmation.object_id
                       AND content_type_id = (SELECT id
                                              FROM   django_content_type
                                              WHERE  app_label = 'zerver'
                                              AND    model = 'preregistrationuser')
                       AND id != exclude_id
)
"""

NO_CONFIRMATIONS = """
DELETE FROM zerver_preregistrationuser
 WHERE NOT EXISTS(SELECT 1
                    FROM confirmation_confirmation
                   WHERE content_type_id = (SELECT id
                                            FROM   django_content_type
                                            WHERE  app_label = 'zerver'
                                            AND    model = 'preregistrationuser')
                     AND object_id = zerver_preregistrationuser.id)
   AND referred_by_id IS NOT NULL
"""


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        (
            "zerver",
            "0515_rename_named_group_can_mention_group_namedusergroup_can_mention_group_and_more",
        ),
    ]

    operations = [
        migrations.RunSQL(TOO_MANY_CONFIRMATIONS, elidable=True),
        migrations.RunSQL(NO_CONFIRMATIONS, elidable=True),
    ]
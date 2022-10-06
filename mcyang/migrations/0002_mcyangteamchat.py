# Generated by Django 4.0.7 on 2022-09-25 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mcyang', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='McyangTeamChat',
            fields=[
                ('GroupChat_id', models.AutoField(default=1, primary_key=True, serialize=False)),
                ('TeamLeader_id', models.IntegerField()),
                ('ChatRoom', models.CharField(max_length=100, null=True)),
                ('crtTime', models.DateTimeField(auto_now_add=True)),
                ('Course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcyang.mcyangcourse')),
                ('TeamDesc_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcyang.mcyangteamdesc')),
            ],
            options={
                'db_table': 'mc_Teamchat',
            },
        ),
    ]
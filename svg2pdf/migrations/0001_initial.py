# Generated by Django 4.1.1 on 2022-09-06 08:16
# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=invalid-name
# pylint: disable=missing-class-docstring

from django.db import migrations, models
import django.db.models.deletion
import svg2pdf.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faktura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa_faktury', models.CharField(max_length=8)),
                ('numer_faktury', models.CharField(max_length=15)),
                ('data_sprzedazy', models.DateField()),
                ('data_wystawienia', models.DateField()),
                ('termin_platnosci', models.DateField()),
                ('zaplacono', models.FloatField(default=0, validators=[svg2pdf.models.validate_neg, svg2pdf.models.validate_num])),
                ('termin_platnosci_dni', models.PositiveIntegerField(default=1)),
                ('fakture_wystawil', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Firma',
            fields=[
                ('nazwa', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('nip', models.CharField(max_length=13)),
                ('ulica', models.CharField(max_length=45)),
                ('adres', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='JednostkaM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(default='Szt', max_length=8)),
                ('dziesietna', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='SposobPlat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(default='Przelew na konto', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Pozycjafaktury',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.TextField()),
                ('ilosc', models.FloatField(default=1, validators=[svg2pdf.models.validate_neg, svg2pdf.models.validate_zero])),
                ('cena_Netto', models.FloatField(validators=[svg2pdf.models.validate_neg, svg2pdf.models.validate_num, svg2pdf.models.validate_zero])),
                ('podatek', models.IntegerField(default=23, validators=[svg2pdf.models.validate_neg, svg2pdf.models.validate_zero])),
                ('faktura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pozycja_rel', to='svg2pdf.faktura')),
                ('jednostka', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='svg2pdf.jednostkam')),
            ],
        ),
        migrations.AddField(
            model_name='faktura',
            name='firma_klient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nabywca', to='svg2pdf.firma'),
        ),
        migrations.AddField(
            model_name='faktura',
            name='firma_sprzedawca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sprzedawca', to='svg2pdf.firma'),
        ),
        migrations.AddField(
            model_name='faktura',
            name='sposob_platnosci',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='svg2pdf.sposobplat'),
        ),
    ]

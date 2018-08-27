# -*- coding: utf-8

import logging
import subprocess
from flask import flash, redirect, url_for, render_template

from app import app
from app.forms import RegistrationForm
from app.utils import rutranslit

PS_COMMAND_TEMPLATE = """New-ADUser -Name {!r} -AccountPassword(ConvertTo-SecureString 'Qwerty123' -AsPlainText -Force) -ChangePasswordAtLogon 1 -Company {!r} -Department {!r} -DisplayName {!r} -EmailAddress {!r} -Enabled 1 -GivenName {!r} -SurName {!r} -ProfilePath '\\\\POSEIDON\\movedUsers$\\%%username%%' -SamAccountName {!r} -UserPrincipalName {} -MobilePhone {} -Path 'OU=PersonaledUsers,DC=ippo,DC=mirea,DC=ru"""


@app.route('/registration', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    if form.validate_on_submit():
        ps_command = PS_COMMAND_TEMPLATE.format(
            rutranslit(f'{form.name.data}.{form.surname.data}'),
            rutranslit(form.department.data),
            rutranslit(form.group.data),
            rutranslit(
                f'{form.surname.data} {form.name.data}'), form.email.data,
            rutranslit(f'{form.name.data} {form.lastname.data}'),
            rutranslit(form.surname.data),
            rutranslit(f'{form.name.data}.{form.surname.data}'),
            '{}@ippo.mirea.ru'.format(rutranslit(
                f'{form.name.data}.{form.surname.data}')),
            form.phone.data
        )
        ps = subprocess.Popen(['powershell', ps_command],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, err = ps.communicate()
        rc = ps.returncode
        if rc != 0:
            flash('Произошла системная ошибка. Позовите администратора.')
            logging.error(err.decode('utf-8'))
            return redirect(url_for('index'))
        else:
            flash(('Поздравляем! Вы зарегестрированы как {!r} с временным паролем {!r}. Пароль надо будет сменить при входе в систему').format(
                rutranslit(f'{form.name.data}.{form.surname.data}'), 'Qwerty123'))
            logging.info('Cоздан новый аккаунт: {!r}. Команда для создания пользователя: {!r}'.format(rutranslit(f'{form.name.data}.{form.surname.data}'), ps_command))
            return redirect(url_for('index'))
    return render_template('index.html', form=form)

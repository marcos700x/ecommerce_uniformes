from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Usuario
from .forms import UsuarioForm, NombreApellidoForm, RegistroForm
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        login_input = request.POST['login']  # Cambiado a 'login'
        password = request.POST['password']

        user = None
        if '@' in login_input:
            try:
                user_obj = User.objects.get(email=login_input)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        else:
            user = authenticate(request, username=login_input, password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})

    return render(request, 'login.html')



def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('index')


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if len(password) < 6:
                form.add_error('password', 'La contraseña debe tener al menos 6 caracteres.')
                return render(request, 'registro.html', {'form': form})

            user = form.save(commit=False)
            user.set_password(password)
            user.save()

            # Crear perfil extendido Usuario
            usuario, created = Usuario.objects.get_or_create(user=user)

            login(request, user)
            messages.success(request, 'Registro exitoso. ¡Bienvenido!')
            return redirect('index')
        else:
            return render(request, 'registro.html', {'form': form})

    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})



@login_required
def perfil_view(request):
    usuario = Usuario.objects.get(user=request.user)
    user = request.user

    if request.method == 'POST':
        form_usuario = UsuarioForm(request.POST, instance=usuario)
        form_nombre = NombreApellidoForm(request.POST, instance=user)

        if form_usuario.is_valid() and form_nombre.is_valid():
            form_usuario.save()
            form_nombre.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
    else:
        form_usuario = UsuarioForm(instance=usuario)
        form_nombre = NombreApellidoForm(instance=user)

    return render(request, 'perfil.html', {
        'form': form_usuario,
        'form_nombre': form_nombre,
        'user': user,
    })

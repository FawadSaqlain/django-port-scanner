from django.shortcuts import render, redirect
from django import forms
from .show_port import scan_port, get_process_info
from .port_open import open_port
from .port_close import port_close

class CreateForm(forms.Form):
    ipaddress = forms.CharField(
        label='IP Address:',
        required=True,
        widget=forms.TextInput(attrs={'required': 'required'})
    )
    portno = forms.IntegerField(
        label='Port no:',
        required=True,
        widget=forms.NumberInput(attrs={'required': 'required'})
    )

def showport(request):
    try:
        if 'ipaddress' not in request.session or 'portno' not in request.session:
            request.session['ipaddress'] = ''
            request.session['portno'] = 0

        if not request.session['ipaddress'] or not request.session['portno']:
            result = "IP address or port number not provided."
        else:
            result = scan_port(request.session['ipaddress'], request.session['portno'])
        process = get_process_info(request.session['portno'])
        return render(request, 'showport.html', {'result': result, 'port': request.session['portno'], 'ipaddress': request.session['ipaddress'], 'process': process})
    except Exception as e:
        return render(request, 'error.html', {'error_message': f"An error occurred: {e}"})

def openport(request):
    try:
        if 'ipaddress' not in request.session or 'portno' not in request.session:
            request.session['ipaddress'] = ''
            request.session['portno'] = 0

        result = open_port(request.session['ipaddress'], request.session['portno'])
        
        # Adding delay to ensure fake server process starts
        import time
        time.sleep(1)  # Sleep for 1 second to allow the fake server to start
        
        process = get_process_info(request.session['portno'])
        return render(request, 'openport.html', {'ipaddress': request.session['ipaddress'], 'port': request.session['portno'], 'result': result, 'process': process})
    except Exception as e:
        return render(request, 'error.html', {'error_message': f"An error occurred: {e}"})

def closeport(request):
    try:
        if 'ipaddress' not in request.session or 'portno' not in request.session:
            request.session['ipaddress'] = ''
            request.session['portno'] = 0
        results = port_close(request.session['ipaddress'], request.session['portno'])
        return render(request, 'closeport.html', {'results': results})
    except Exception as e:
        return render(request, 'error.html', {'error_message': f"An error occurred: {e}"})

def manu(request):
    try:
        # Clear the session data
        request.session.flush()
        if request.method == "POST":
            form = CreateForm(request.POST)
            if form.is_valid():
                ipaddress = form.cleaned_data['ipaddress']
                portno = form.cleaned_data['portno']
                request.session["ipaddress"] = ipaddress
                request.session["portno"] = portno

                return redirect('portscanner:showport')
            else:
                return render(request, 'manu.html', {'form': form})
        else:
            form = CreateForm()
        return render(request, 'manu.html', {'form': form})
    except Exception as e:
        return render(request, 'error.html', {'error_message': f"An error occurred: {e}"})

import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from yeelight import Bulb
from lights.models import Light
from .forms import LightForm



def control_panel(request):
    lights = Light.objects.all()
    
    # Initialize bulb_status to "on"
    bulb_status = "on"
    
    # Check if at least one bulb is off
    for light in lights:
        if not light.status:  # If the status of any light is False (off)
            bulb_status = "off"
            break  # No need to check further if any bulb is found off
    
    # Pass the lights queryset and bulb_status in the context
    context = {
        'lights': lights,
        'bulb_status': bulb_status,
    }
    
    return render(request, 'lights/control_panel.html', context)

def add_light(request):
    if request.method == 'POST':
        form = LightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('control_panel')
    else:
        form = LightForm()
    return render(request, 'lights/add_light.html', {'form': form})


def turn_on_all_lights(request):
    # Fetch all light instances from the database
    lights = Light.objects.all()

    # Iterate over each light instance
    for light in lights:
        # Assuming your Light model has an attribute named 'ip_address' to store the IP
        bulb_ip = light.bulb_ip  # Replace 'ip_address' with the actual field name
        bulb = Bulb(bulb_ip)
        light.status = 1
        light.save()
        bulb.turn_on()

    # Return a JsonResponse indicating success
    return render(request, 'lights/control_panel.html', {'lights': lights})


def turn_off_all_lights(request):
    # Fetch all light instances from the database
    lights = Light.objects.all()

    # Iterate over each light instance
    for light in lights:
        # Assuming your Light model has an attribute named 'ip_address' to store the IP
        bulb_ip = light.bulb_ip  # Replace 'ip_address' with the actual field name
        bulb = Bulb(bulb_ip)
        light.status = 0
        light.save()
        bulb.turn_off()

    # Return a JsonResponse indicating success
    return render(request, 'lights/control_panel.html', {'lights': lights})


from django.http import HttpResponseRedirect
from django.urls import reverse

def set_color(request):
    if request.method == 'POST':
        color = request.POST.get('color')  # Get the color value from the form
        color = color.lstrip('#')  # Remove '#' from the color value
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))  # Convert to RGB
        
        # Assuming you have a way to select which light(s) to change.
        # This example changes all lights for simplicity.
        lights = Light.objects.all()
        for light in lights:
            bulb_ip = light.bulb_ip  # Make sure this matches your model
            bulb = Bulb(bulb_ip)
            bulb.set_rgb(r, g, b)

        # Redirect back to the control panel or another appropriate page
        return HttpResponseRedirect(reverse('control_panel'))
    else:
        # If not a POST request, redirect to form or handle accordingly
        return HttpResponseRedirect(reverse('color_picker'))

def set_all_white(request):

        # Fetch all light instances from the database
    lights = Light.objects.all()

    # Iterate over each light instance
    for light in lights:
        # Assuming your Light model has an attribute named 'ip_address' to store the IP
        bulb_ip = light.bulb_ip  # Replace 'ip_address' with the actual field name
        bulb = Bulb(bulb_ip)
        light.status = 0
        light.save()
        color_temp = 6500
        # Set brightness to 100%
        bulb.set_brightness(100)
        bulb.set_color_temp(color_temp)

    # Return a JsonResponse indicating success
    return render(request, 'lights/control_panel.html', {'lights': lights})



def set_white(request,bulb_id):
    # Fetch all light instances from the database
    lights = Light.objects.all()
    try:
        light = Light.objects.get(id=bulb_id)
        bulb_ip = light.bulb_ip
        bulb = Bulb(bulb_ip)
        color_temp = 6500
        bulb.set_brightness(100)
        bulb.set_color_temp(color_temp)
        light.save()
    except Light.DoesNotExist:
        # Handle the case where the light doesn't exist
        pass
    # Return a JsonResponse indicating success
    return render(request, 'lights/control_panel.html', {'lights': lights})


def set_light_color(request, light_id):
    if request.method == 'POST':
        color = request.POST.get('color')
        color = color.lstrip('#')  # Remove '#' from the color value
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))  # Convert to RGB
        
        try:
            light = Light.objects.get(id=light_id)
            bulb_ip = light.bulb_ip
            bulb = Bulb(bulb_ip)
            bulb.set_rgb(r, g, b)
            # Assuming 'status' should reflect the light being on after color change
            light.status = True
            light.save()
        except Light.DoesNotExist:
            # Handle the case where the light doesn't exist
            pass

        # Redirect back to the control panel
        return HttpResponseRedirect(reverse('control_panel'))
    else:
        # If not a POST request, redirect to form or handle accordingly
        return HttpResponseRedirect(reverse('control_panel'))
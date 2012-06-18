from django.conf import settings

def branding_variables(request):
    brand_dict = {
        'brand_copyright': settings.BRAND_COPYRIGHT,
        'brand_title' : settings.BRAND_SITE_TITLE,
        'brand_logo' : settings.BRAND_LOGO,
        'brand_ga_code' : settings.BRAND_GA_CODE,
        'brand_background_image' : settings.BRAND_BACKGROUND_IMAGE,
        'brand_background_color' : settings.BRAND_BACKGROUND_COLOR,
    }
    return brand_dict

def user_vars(request):
    user_vars = {
        'login_url' : settings.LOGIN_URL,
        
    }
    return user_vars

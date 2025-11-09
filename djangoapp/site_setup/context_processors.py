from site_setup.models import SiteSetup


def context_processor_example(request):
    return {
        'example': 'Veio do context processor (example)',
    }


def site_setup(request):
    """Return the latest SiteSetup instance as `site_setup`.

    The template expects `site_setup` to be the model instance so
    templates can use `site_setup.favicon.url`. Previously this returned
    a dict which prevented access to attributes like `.favicon`.
    """
    setup = SiteSetup.objects.order_by('-id').first()
    return {
        'site_setup': setup
    }

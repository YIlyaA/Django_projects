from django import template

register = template.Library()

# Register a filter to re-formt the 'wizard forms'


@register.filter(name="insert_classes")
def insert_classes(value, arg):
    # Obtain the input field and transform it into a string
    the_classes = value.field.widget.attrs.get("class", "")
    # Check if there are classes that are available
    # If there are no classes then set up a list and assign it to a class
    if the_classes:
        the_classes = the_classes.split(" ")
    else:
        the_classes = []

    my_new_classes = arg.split(" ")

    # If there are no classes then set up a list and assign it to a class
    for cs in my_new_classes:
        if cs not in the_classes:
            the_classes.append(cs)

    # Take the class peripherals and input it as a string and return it accordingly
    return value.as_widget(attrs={"class": " ".join(the_classes)})

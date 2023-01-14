from AkaMed import AkaMed   # you import your main program during the initialisation of your script


def create_instance(c_instance):    # this function tells live that you create a new midi remote script
    return AkaMed(c_instance)      # the initialisation result is the calling of the main function of your script.
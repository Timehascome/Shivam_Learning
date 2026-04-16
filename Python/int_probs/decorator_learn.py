def decorator_function(original_function):
    def wrapper_function(*args, **kwargs):
        print("Wrapper executed before {}".format(original_function.__name__))
        args = list(args)
        print(args)
        if len(args)>=2:
            args[0],args[1] = args[1],args[0]
        return original_function(*args, **kwargs)
    return wrapper_function
@decorator_function
def display(a,b,c):
    print(f"Display function executed : {a,b,c}")  
display(1,2,3)
import prefect


def log(msg):
    """ 
    mostra a msg no log do prefect
    """
    prefect.context.logger.info(msg)



    

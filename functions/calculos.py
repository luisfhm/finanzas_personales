def ahorro_total(ahorro_mensual, meses):
    return [ahorro_mensual * (i+1) for i in range(meses)]

def poder_adquisitivo(ahorro_list, inflacion_mensual):
    return [ah / ((1 + inflacion_mensual) ** (i+1)) for i, ah in enumerate(ahorro_list)]

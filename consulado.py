import requests
import json
import datetime 
import locale
#locale.setlocale(locale.LC_ALL,'es_ES.UTF-8')
locale.setlocale(locale.LC_TIME,'es_ES')
requests.packages.urllib3.disable_warnings()

headers = {'Referer': 'https://app.bookitit.com/es/hosteds/widgetdefault/2c6277fc2bf43562ccce5c647ff1db4eb'}

# def get_services():
#     params = {
#         'callback': '',
#         'type': 'default',
#         'publickey': '2c6277fc2bf43562ccce5c647ff1db4eb',
#         'lang': 'es',
#         'src': 'https://app.bookitit.com/es/hosteds/widgetdefault/2c6277fc2bf43562ccce5c647ff1db4eb',
#     }
#     res = requests.get('https://app.bookitit.com/onlinebookings/getservices/', params=params, headers=headers,verify=False).content.decode()
#     a,b=res.find('{'),res.rfind('}')+1
#     j=json.loads(res[a:b])
#     # print(json.dumps(j, indent=4))
#     return j

# def get_agendas(service_id):
    
#     params = {
#         'callback': '',
#         'type': 'default',
#         'publickey': '2c6277fc2bf43562ccce5c647ff1db4eb',
#         'lang': 'es',
#         'services[]': service_id,
#         'src': 'https://app.bookitit.com/es/hosteds/widgetdefault/2c6277fc2bf43562ccce5c647ff1db4eb',
#     }

#     res = requests.get('https://app.bookitit.com/onlinebookings/getagendas/', params=params, headers=headers,verify=False).content.decode()
#     a,b=res.find('{'),res.rfind('}')+1
#     j=json.loads(res[a:b])
#     # print(json.dumps(j, indent=4))
#     return j

def get_dates(servicio,agenda,month):
    params = {
        'callback': '',
        'type': 'default',
        'publickey': '2c6277fc2bf43562ccce5c647ff1db4eb',
        'lang': 'es',
        'services[]': servicio,
        'agendas[]': agenda,
        'src': 'https://app.bookitit.com/es/hosteds/widgetdefault/2c6277fc2bf43562ccce5c647ff1db4eb',
        'start': month,
        'end': month,
    }

    res = requests.get('https://app.bookitit.com/onlinebookings/datetime/', params=params, headers=headers,verify=False).content.decode()
    a,b=res.find('{'),res.rfind('}')+1
    j=json.loads(res[a:b])
    # print('req',month)
    return j

def parse_available(dates_raw):
    return {day['date']:[day['times'][time]['time'] for time in day['times']] for day in dates_raw['Slots'] if day['times']}


def gen_future_months():
    today = datetime.datetime.now()
    year = today.year
    month = today.month-1 # months 0 to 11
    while True:
        yield f'{year}-{month+1:02}-01'
        month += 1
        if month == 12:
            month = 0
            year +=1

def get_next_available(servicio): 
    # servicio= ['bkt144496','bkt70279','VENTANILLA B','INSCRIPCIÓN CONSULAR']
    servicio_id,agenda_id = servicio[:2]
    month = gen_future_months() #generator
    availables = {}
    for i in range(4):
        availables = parse_available(get_dates(servicio_id,agenda_id,next(month)))
        if availables:
            break
    return availables

def format_date(date):
    return datetime.datetime.strptime(date,'%Y-%m-%d').strftime('*%A, %-d* de %B')

# SERVICIOS 
# REAL REQUEST
# services = get_services()["Services"]
# services = [[s['id'],s['groups_id'],s['name']] for s in services]
#
# CACHED REQUEST 
# services = [['bkt767151', 'bkt77', '<br/>'], ['bkt144562', 'bkt78683', '[A]... AUTORIZACIONES ANTE LA  DGT'], ['bkt144540', 'bkt78683', '[B]... AUTORIZACIONES ANTECEDENTES PENALES'], ['bkt415514', 'bkt78683', '[C]... AUTORIZACION VIAJE MENORES'], ['bkt144474', 'bkt78672', '[D]... N.I.E. ( NUMERO DE IDENTIFICACIÓN  EXTRANJEROS)'], ['bkt144529', 'bkt78672', '[E]... CERTIFICADO DIGITAL'], ['bkt144518', 'bkt78672', '[F]... COMPULSA'], ['bkt144507', 'bkt78672', '[G]... FE DE VIDA'], ['bkt796873', 'bkt78672', '[H] ... AUTORIZACIÓN PASAPORTE MENORES'], ['bkt796884', 'bkt78672', '[I] ... REGISTRO DE SOLICITUDES Y DOCUMENTOS'], ['bkt144485', 'bkt78672', '[J]... NUMERO DE IDENTIFICACIÓN FISCAL (N.I.F.)'], ['bkt144496', 'bkt78661', '[K]... INSCRIPCIÓN CONSULAR'], ['bkt144463', 'bkt78661', '[L]... PASAPORTE ( SOLO INSCRITOS COMO RESIDENTE EN EL CONSULADO'], ['bkt144551', 'bkt130559', '[M]... VISADO/ VISA']]
#
# ['bkt767151', 'bkt77', '<br/>']
# ['bkt144562', 'bkt78683', '[A]... AUTORIZACIONES ANTE LA  DGT']
# ['bkt144540', 'bkt78683', '[B]... AUTORIZACIONES ANTECEDENTES PENALES']
# ['bkt415514', 'bkt78683', '[C]... AUTORIZACION VIAJE MENORES']
# ['bkt144474', 'bkt78672', '[D]... N.I.E. ( NUMERO DE IDENTIFICACIÓN  EXTRANJEROS)']
# ['bkt144529', 'bkt78672', '[E]... CERTIFICADO DIGITAL']
# ['bkt144518', 'bkt78672', '[F]... COMPULSA']
# ['bkt144507', 'bkt78672', '[G]... FE DE VIDA']
# ['bkt796873', 'bkt78672', '[H] ... AUTORIZACIÓN PASAPORTE MENORES']
# ['bkt796884', 'bkt78672', '[I] ... REGISTRO DE SOLICITUDES Y DOCUMENTOS']
# ['bkt144485', 'bkt78672', '[J]... NUMERO DE IDENTIFICACIÓN FISCAL (N.I.F.)']
# ['bkt144496', 'bkt78661', '[K]... INSCRIPCIÓN CONSULAR']
# ['bkt144463', 'bkt78661', '[L]... PASAPORTE ( SOLO INSCRITOS COMO RESIDENTE EN EL CONSULADO']
# ['bkt144551', 'bkt130559', '[M]... VISADO/ VISA']


# AGENDAS
# REAL REQUEST
# agendas =  {s[0]:get_agendas(s[0]) for s in services}
#
# CACHED REQUEST 
# agendas = {'bkt767151': {'Agendas': []}, 'bkt144562': {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]}, 'bkt144540': {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]}, 'bkt415514': {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]}, 'bkt144474': {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]}, 'bkt144529': {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]}, 'bkt144518': {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]}, 'bkt144507': {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]}, 'bkt796873': {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]}, 'bkt796884': {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]}, 'bkt144485': {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]}, 'bkt144496': {'Agendas': [{'id': 'bkt70279', 'name': 'VENTANILLA B ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]}, 'bkt144463': {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}, {'id': 'bkt70279', 'name': 'VENTANILLA B ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]}, 'bkt144551': {'Agendas': [{'id': 'bkt70301', 'name': 'Visados (una cita por persona)', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]}}
#
# ('bkt767151', {'Agendas': []})
# ('bkt144562', {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]})
# ('bkt144540', {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]})
# ('bkt415514', {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]})
# ('bkt144474', {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]})
# ('bkt144529', {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]})
# ('bkt144518', {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]})
# ('bkt144507', {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]})
# ('bkt796873', {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]})
# ('bkt796884', {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]})
# ('bkt144485', {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]})
# ('bkt144496', {'Agendas': [{'id': 'bkt70279', 'name': 'VENTANILLA B ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]})
# ('bkt144463', {'Agendas': [{'id': 'bkt70312', 'name': 'VENTANILLA A ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}, {'id': 'bkt70279', 'name': 'VENTANILLA B ', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]})
# ('bkt144551', {'Agendas': [{'id': 'bkt70301', 'name': 'Visados (una cita por persona)', 'photo': 'https://app.bookitit.com/images/global/add_photo.png'}]})

# PAR SERVICIO-AGENDA (VENTANA) 
#
# servicio_ventana = []
# for s in services[1:]:
#     service_id = s[0]
#     for ventana in agendas[service_id]['Agendas']:
#         servicio_ventana.append([service_id,ventana['id'],ventana['name'],s[2].split('... ')[1]])
#
# RESULTADO
# servicio  AGENDA  n. ventana    nombre servicio
# bkt144562 bkt70312 VENTANILLA A  AUTORIZACIONES ANTE LA  DGT
# bkt144540 bkt70312 VENTANILLA A  AUTORIZACIONES ANTECEDENTES PENALES
# bkt415514 bkt70312 VENTANILLA A  AUTORIZACION VIAJE MENORES
# bkt144474 bkt70312 VENTANILLA A  N.I.E. ( NUMERO DE IDENTIFICACIÓN  EXTRANJEROS)
# bkt144529 bkt70312 VENTANILLA A  CERTIFICADO DIGITAL
# bkt144518 bkt70312 VENTANILLA A  COMPULSA
# bkt144507 bkt70312 VENTANILLA A  FE DE VIDA
# bkt796873 bkt70312 VENTANILLA A  AUTORIZACIÓN PASAPORTE MENORES
# bkt796884 bkt70312 VENTANILLA A  REGISTRO DE SOLICITUDES Y DOCUMENTOS
# bkt144485 bkt70312 VENTANILLA A  NUMERO DE IDENTIFICACIÓN FISCAL (N.I.F.)
# bkt144496 bkt70279 VENTANILLA B  INSCRIPCIÓN CONSULAR
# bkt144463 bkt70312 VENTANILLA A  PASAPORTE ( SOLO INSCRITOS COMO RESIDENTE EN EL CONSULADO
# bkt144463 bkt70279 VENTANILLA B  PASAPORTE ( SOLO INSCRITOS COMO RESIDENTE EN EL CONSULADO
# bkt144551 bkt70301 Visados (una cita por persona) VISADO/ VISA        



def fetch_citas(servicios):
    # states: list with four strings one for each 
    citas = []
    for s in servicios:
        first_month = get_next_available(s)
        if first_month:
            first_day = list(first_month.items())[0]
            plural = 's' if len(first_day[1])>1 else ''
            citas.append(f'{s[2]}:\n\tEl {format_date(first_day[0])} hay {len(first_day[1])} cita{plural}')
        else:
            citas.append(f'{s[2]}:\n\tEn este momento *NO* hay citas')
    return citas
    


# TELEGRAM
# API Documentation https://core.telegram.org/bots/api#sendmessage
def telegram_command(token,method_name, data):
    url = f'https://api.telegram.org/bot{token}/{method_name}'
    return requests.post(url=url, json=data)

def telegram_sendMessage(token,chat_id: str,text: str):
    return telegram_command(token,'sendMessage', {
        'text': text,
        'chat_id': chat_id,
        'parse_mode': 'markdown',
        })

# unused
#
# def telegram_getUpdates(token):
#     return telegram_command(token,'getUpdates',{})
#
# def telegram_update_message(token,chat_id,msg_id,msg):
#     return telegram_command(token,'editMessageText',{'chat_id':chat_id,'message_id':msg_id,'text':msg})    
#

def load_state():
    with open('bot-status.json','r') as f:
        return json.load(f)

def save_state(data):
    with open('bot-status.json','w') as f:
        json.dump(data,f)


def main():
    
    data = load_state()
    token = data['token']
    servicios = [['bkt144496','bkt70279','Inscripción y Pasaporte (_B_)'],['bkt144463','bkt70312','Pasaporte y Otros (_A_)'],['bkt144474','bkt70312','NIE ']]
    new_text = '\n\n'.join(fetch_citas(servicios))
    if new_text != data.get('last_message',''):
        telegram_sendMessage(token,data['chat_id'],new_text)
        data['last_message'] = new_text

    # for i,msg in enumerate(citas):
    #     if msg!=data['last_messages']:
    #         telegram_sendMessage(token,data['chat_id'],msg)
    #         data['last_messages'][i]=msg
    save_state(data)


if __name__ == "__main__":
    main()

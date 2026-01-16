with open('metodos.py', 'r') as f:
    content = f.read()

# Insert the functions after import re
insert_pos = content.find('import re\n') + len('import re\n')
functions = '''
def validar_email(email: str) -> bool:
    """Valida el formato de un correo electrónico"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None


def validar_rfc(rfc: str) -> bool:
    """Valida el formato de un RFC mexicano"""
    # RFC para personas físicas: 13 caracteres (4 letras + 6 dígitos + 3 alfanuméricos)
    # RFC para personas morales: 12 caracteres (3 letras + 6 dígitos + 3 alfanuméricos)
    patron = r'^[A-ZÑ&]{3,4}[0-9]{6}[A-Z0-9]{3}$'
    return re.match(patron, rfc.upper()) is not None

'''

new_content = content[:insert_pos] + functions + content[insert_pos:]

with open('metodos.py', 'w') as f:
    f.write(new_content)

print('Functions added')
#反射机制哦
class GetTicket():
    ticket=None


setattr(GetTicket,'ticket','100119002021112600016378987465404835992348557666')
print(getattr(GetTicket,'ticket'))
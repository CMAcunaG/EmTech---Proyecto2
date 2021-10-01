def Valida_User(User):
    #
    # users [ UserName, Password]
    #
    users = [
		[ "Luis", "1234"],
		[ "Juan", "2345"], 
		[ "Jorge", "3456"],
		[ "Carlos", "4567"],
		[ "admin", "admin"],
		[ "Admin", "Admin"],
		[ "ADMIN", "ADMIN"]
		]
    #user = input("Dame el usuario : ")
    ok = False
    for valid in users:
        if User == valid[0]:
            ok = True
            break
    if ok:
        print("Usuario " + User + " es valido")
        pas = input("Dame el password del usuario : ")
        if pas == valid[1]:
            ok = True
        else:
            ok = False
            print("El password de " + User + " NO valido")
    else:
        print("Usuario " + User + " NO valido")
    return (ok)

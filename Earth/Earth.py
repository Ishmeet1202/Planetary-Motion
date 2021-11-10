import numpy as np
from scipy.integrate import odeint

def func(initial,t):  # CREATE A FUNCTION FOR SCIPY ODEINT FUNCTION
    x = initial[0]
    y = initial[1]
    vx = initial[2]
    vy = initial[3]

    dvxdt = -(GM * (x/((x**2 + y**2)**(3/2)))) # DIFFERENTIAL EQUATIONS FOR OUR PROBLEM
    dvydt = -(GM * (y/((x**2 + y**2)**(3/2))))
    
    return [vx,vy,dvxdt,dvydt] # RETURN AN ARRAY CONTAINS SLOPE (ACCn AND VELOCITY) FOR CALCULATING POSITION AND VELOCITY

def leap_frog(x,y,vx,vy,acc_x,acc_y,r,t,h,GM): # CREATE A FUNCTION FOR LEAP FROG METHOD
    list_1 = []
    vx_cord = vx[0] ; vy_cord = vy[0] ; time = t[0] ; x_cord = x[0] ; y_cord = y[0] # INITIALISE ARRAY
    while y_cord>=0:			# RUNNING A LOOP WHILE Y COORDINATE >= 0 i.e. HALF ORBIT
        x_cord = x_cord + h * vx_cord # CALCULATING X COORDINATE
        y_cord = y_cord + h * vy_cord # CALCULATING Y COORDINATE
        time = time + h 		# INCREASING TIME BY STEP SIZE

        r_cord = np.sqrt(x_cord**2 + y_cord**2) # CALCULATING POSITION VECTOR
        accx_cord = -(GM * (x_cord/(r_cord)**3)) # CALCULATING ACCELERATION X COORDINATE
        accy_cord = -(GM * (y_cord/(r_cord)**3)) # CALCULATING ACCELERATION Y COORDINATE

        vx_cord = vx_cord + h * accx_cord # CALCULATING VELOCITY X COORDINATE
        vy_cord = vy_cord + h * accy_cord # CALCULATING VELOCITY Y COORDINATE

        if x_cord not in x:  		# ALL BELOW CONDITIONS ARE APPLIED TO STORE THE GENERATED DATA IN THEIR RESPECTIVE ARRAY
            x.append(x_cord)
        if y_cord not in y:
            y.append(y_cord)
        if r_cord not in r:
            r.append(r_cord) 
        if time not in t:
            t.append(time)
        if accx_cord not in acc_x:
            acc_x.append(accx_cord)
        if accy_cord not in acc_y:
            acc_y.append(accy_cord)
        if vx_cord not in vx:
            vx.append(vx_cord)
        if vy_cord not in vy:
            vy.append(vy_cord)
    
    while y_cord<=0:				# SAME PROCEDURE BUT NOW FOR Y COORDINATE <= 0 i.e. REMAINING HALF ORBIT
        x_cord = x_cord + h * vx_cord 
        y_cord = y_cord + h * vy_cord
        time = time + h

        r_cord = np.sqrt(x_cord**2 + y_cord**2)
        accx_cord = -(GM * (x_cord/(r_cord)**3))
        accy_cord = -(GM * (y_cord/(r_cord)**3))

        vx_cord = vx_cord + h * accx_cord
        vy_cord = vy_cord + h * accy_cord

        if x_cord not in x:
            x.append(x_cord)
        if y_cord not in y:
            y.append(y_cord)
        if r_cord not in r:
            r.append(r_cord) 
        if time not in t:
            t.append(time)
        if accx_cord not in acc_x:
            acc_x.append(accx_cord)
        if accy_cord not in acc_y:
            acc_y.append(accy_cord)
        if vx_cord not in vx:
            vx.append(vx_cord)
        if vy_cord not in vy:
            vy.append(vy_cord)
    list_1.extend([x,y,vx,vy,acc_x,acc_y,t,r])
    return list_1

def angular_momentum(mu,vx,vy,r): 		# CREATE A FUNCTION FOR CALCULATING ANGULAR MOMENTUM AT EVERY POSITION
    L_list = []
    for i in range(len(vx)):
        L = mu*(np.sqrt(vx[i]**2 + vy[i]**2))*r[i]
        L_list.append(L)
    return L_list

def first_law(semiminor,semimajor,x,y):	# CREATE A FUNCTION FOR CALCULATING FIRST LAW
    print("\nKEPLER'S FIRST LAW:")
    check1 = ((x[6]-center_x)**2)/((semimajor)**2) + ((y[6]-0.0)**2)/((semiminor)**2) # SATISFYING THE ELLIPSE EQUATION
    print("\nValue of ellipse equation is:",check1)
    ecc = np.sqrt(1 - (semiminor**2/semimajor**2)) 		# CALCULATING ECCENTRICITY OF THE ORBIT
    print("\nValue of eccentricity of the orbit is:",ecc)

def second_law(ang_m,mu,t,h,x,y,N1,N2,N3,N4):		# CREATE A FUNCTION FOR CALCULATING SECOND LAW
    a1 = 0 ; a2 = 0 ; x_list = [] ; y_list = [] ; ox = [0,0,0,0] ; oy = [0,0,0,0]
    for i in range(len(t)):
        if t[i] >= N1*h and t[i] <= N2*h:
            a1 = a1 + 0.5*(ang_m[i]/mu)*h		# CALCULATING AREA 1 IN GIVEN TIME PERIOD (MULTIPLE OF STEP SIZE)
        if np.allclose(t[i],N1*h):
            x_list.extend([x[i]]) ; y_list.extend([y[i]]) # STORING THE VALUE OF X,Y CORRESPONDS TO THE STARTING AND ENDING POINT FOR TIME PERIOD
        elif np.allclose(t[i],N2*h):				# FOR AREA 1
            x_list.extend([x[i]]) ; y_list.extend([y[i]])
        if t[i] >= N3*h and t[i] <= N4*h:
            a2 = a2 + 0.5*(ang_m[i]/mu)*h		# CALCULATING AREA 2 IN GIVEN TIME PERIOD (MULTIPLE OF STEP SIZE)
        if np.allclose(t[i],N3*h):
            x_list.extend([x[i]]) ; y_list.extend([y[i]]) # STORING THE VALUE OF X,Y CORRESPONDS TO THE STARTING AND ENDING POINT FOR TIME PERIOD
        elif np.allclose(t[i],N4*h):				# FOR AREA 2
            x_list.extend([x[i]]) ; y_list.extend([y[i]])  
    data = np.column_stack([ox,oy,x_list,y_list])
    file = np.savetxt("/home/ishmeet/BSc physics/Computational Physics/Project OP/Area.txt",data,header = "Ox,Oy,Px,Py")
    print("\nKEPLER'S SECOND LAW:")
    print("\nValue of area 1 swept in (",N1,"* h to",N2,"* h) is:",a1,"meters sqaure or",a1 / 10**18,"million Km square")
    print("\nValue of area 2 swept in (",N3,"* h to",N4,"* h) is:",a2,"meters sqaure or",a2 / 10**18,"million Km square")

def third_law(t,GM,semimajor):	# CREATE A FUNCTION FOR CALCULATING THIRD LAW
    print("\nKEPLER'S THIRD LAW:")
    print("\nValue of orbital period is:",t[-1],"seconds or",t[-1]/(24*60*60),"days") # ORBITAL PERIOD OF EARTH
    lhs = (t[-1]**2/semimajor**3) 								# LHS (RATIO OF T^2/a^3)
    rhs = (4*np.pi*np.pi)/GM 									# RHS (4*PI^2/GM)
    print("\nValue of LHS:",lhs)
    print("\nValue of RHS:",rhs)
    
def comparision(sol_an,x,y,vx,vy): # CREATE A FUNCTION FOR COMPARING THE DATA OF CREATED LEAP FROG AND SCIPY ODEINT FUNCTION
    print("\nCOMPARISION BETWEEN SCIPY ODEINT FUNCTION AND LEAP FROG METHOD:")
    error_x = abs(np.array(sol_an[:,0]) - np.array(x))
    error_y = abs(np.array(sol_an[:,1]) - np.array(y))
    error_vx = abs(np.array(sol_an[:,2]) - np.array(vx))
    error_vy = abs(np.array(sol_an[:,3]) - np.array(vy))
    print("\nAverage of absolute error in x coordinate (b/w odeint and leap frog) is:",np.mean(error_x),"meters") # AVERAGE OF (|X_scipy - X_leapfrog|)
    print("\nAverage of absolute error in y coordinate (b/w odeint and leap frog) is:",np.mean(error_y),"meters") # AVERAGE OF (|Y_scipy - Y_leapfrog|)
    print("\nAverage of absolute error in velocity x coordinate (b/w odeint and leap frog) is:",np.mean(error_vx),"meter per second") # AVERAGE OF (|VELOCIY_X_scipy - VELOCIY_X_leapfrog|)
    print("\nAverage of absolute error in velocity y coordinate (b/w odeint and leap frog) is:",np.mean(error_vy),"meter per second") # AVERAGE OF (|VELOCIY_Y_scipy - VELOCIY_Y_leapfrog|)

def text_files(x,y,vx,vy,acc_x,acc_y,r,t,sol_an,t1): # CREATE A FUNCTION FOR STORING GENERATED DATA IN TEXT FILES 
    data1 = np.column_stack([t,x,y])
    f1 = np.savetxt("/home/ishmeet/BSc physics/Computational Physics/Project OP/Position_cord.txt",data1,header = "Time,X,Y")
    data2 = np.column_stack([t,vx,vy])
    f2 = np.savetxt("/home/ishmeet/BSc physics/Computational Physics/Project OP/Velocity_cord.txt",data2,header = "Time,Vx,Vy")
    data3 = np.column_stack([t,acc_x,acc_y])
    f3 = np.savetxt("/home/ishmeet/BSc physics/Computational Physics/Project OP/Acceleration_cord.txt",data3,header = "Time,ACCx,ACCy")
    data4 = np.column_stack([t,r])
    f4 = np.savetxt("/home/ishmeet/BSc physics/Computational Physics/Project OP/Positon_Vector.txt",data4,header = "Time,R")
    data5 = np.reshape([0,0,x[40],y[40]],(1,4))
    f5 = np.savetxt("/home/ishmeet/BSc physics/Computational Physics/Project OP/Sun.txt",data5,header = "Sx,Sy,Ex,Ey")
    data6 = np.column_stack([t1,sol_an[:,0],sol_an[:,1],sol_an[:,2],sol_an[:,3]])
    f6 = np.savetxt("/home/ishmeet/BSc physics/Computational Physics/Project OP/Scipy.txt",data6,header = "Time,X,Y,Vx,Vy")
    
if __name__ == "__main__":
    h = 0.5 * 24 * 60 * 60 # STEP SIZE

    N1 = int(input("\nEnter the starting point (multiple of step size) for area 1: "))
    N2 = int(input("\nEnter the ending point (multiple of step size) for area 1: "))
    N3 = int(input("\nEnter the starting point (multiple of step size) for area 2: "))
    N4 = int(input("\nEnter the ending point (multiple of step size) for area 2: "))

    # INITIAL CONDITIONS
    x_initial = 147092000000 # IN METER
    y_initial = 0.0
    vx_initial = 0.0
    vy_initial = 30.29 * 10**3 # IN METER PER SECOND
    time = 0
    GM = (6.67430 * 10**(-11) * 1.989 * 10**30) # CONSTANT G*M 
    me = 5.97219 * 10**24 ; M = 1.989 * 10**30 # MASS OF EARTH AND SUN IN Kg
    mu = me*M/(me+M) # REDUCED MASS

    #LIST INITIALISATION AND CALCULATIONS FOR 0th element
    x = [x_initial] ; y = [y_initial]
    vx = [] ; vy = []
    acc_x = [] ; acc_y = []
    r = []
    t = [time]
    initial = [x_initial,y_initial,vx_initial,vy_initial] #CREATE AN ARRAY OF INITIAL CONDITIONS FOR ODEINT FUNCTION

    r.append(np.sqrt(x[0]**2 + y[0]**2))		# APPENDING THE FIRST DATA VALUES IN THEIR RESPECTIVE ARRAYS
    acc_x.append(-(GM * (x[0]/(r[0])**3)))
    acc_y.append(-(GM * (y[0]/(r[0])**3)))
    vx.append(vx_initial + h/2 * acc_x[0])
    vy.append(vy_initial + h/2 * acc_y[0])
    
    sol = leap_frog(x,y,vx,vy,acc_x,acc_y,r,t,h,GM) 		# LEAP FROG METHOD SOLUTION
    
    t1 = np.arange(0,t[-1]+h,h) 				# TIME RANGE FOR ODEINT FUNCTION    
    sol_an = odeint(func,initial,t1)				 # SCIPY ODEINT SOLUTION
    
    center_x = (min(x)+x_initial)/2 				# CENTER OF THE ELLIPSE

    # MAJOR AXIS
    major_x = [min(x),x_initial] ; major_y = [0.0,y_initial]
    a = np.sqrt((major_y[1]-major_y[0])**2 + (major_x[1]-major_x[0])**2)
    data_major = np.column_stack([major_x,major_y])
    file1 = np.savetxt("/home/ishmeet/BSc physics/Computational Physics/Project OP/Major.txt",data_major,header = "Xc,Yc")
    semimajor = a/2

    # MINOR AXIS
    minor_x = [center_x,center_x] ; minor_y = [max(y),min(y)]
    b = np.sqrt((minor_y[1]-minor_y[0])**2 + (minor_x[1]-minor_x[0])**2)
    data_minor = np.column_stack([minor_x,minor_y])
    file2 = np.savetxt("/home/ishmeet/BSc physics/Computational Physics/Project OP/Minor.txt",data_minor,header = "Xc,Yc")
    semiminor = b/2

    print("\n----------------------------------------------------------------------------------")
    print("\nValue of semi major axis is:",semimajor,"meters or",semimajor / 10**9,"million Km")
    print("\nValue of semi minor axis is:",semiminor,"meters or",semiminor / 10**9,"million Km")
    print("\nValue of Perihelion distance is:",min(r),"meters or",min(r) / 10**9,"million Km")
    print("\nValue of Aphelion distance is:",max(r),"meters or",max(r) / 10**9,"million Km")
    print("\n----------------------------------------------------------------------------------")

    ang_m = angular_momentum(mu,vx,vy,r)
    law1 = first_law(semiminor,semimajor,x,y)
    print("\n----------------------------------------------------------------------------------")
    law2 = second_law(ang_m,mu,t,h,x,y,N1,N2,N3,N4)
    print("\n----------------------------------------------------------------------------------")
    law3 = third_law(t,GM,semimajor)
    print("\n----------------------------------------------------------------------------------")
    comparision(sol_an,x,y,vx,vy)
    text_files(x,y,vx,vy,acc_x,acc_y,r,t,sol_an,t1)
 
